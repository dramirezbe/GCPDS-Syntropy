import threading
import time
import unittest

try:
    import numpy as np
    import torch
except ImportError:
    np = torch = None

from mcp_server.config import CNNConfig
from mcp_server.model import build_cnn
from mcp_server.realtime import IQDSP, RingBuffer, Cancelled, RealtimePipeline, SigMFReplay


@unittest.skipUnless(np is not None, "numpy is not installed")
class RealtimePrimitivesTest(unittest.TestCase):
    def test_dsp_preserves_contract_and_normalizes_power(self):
        result = IQDSP().process(np.array([1 + 0j, 0 + 1j], dtype=np.complex64))
        self.assertEqual(result.shape, (2, 2))
        self.assertEqual(result.dtype, np.float32)
        self.assertAlmostEqual(float(np.mean(result * result)), 1.0, places=6)

    def test_ring_buffer_cancel_wakes_blocked_put_and_get(self):
        buffer = RingBuffer(1)
        buffer.put("first")
        outcome = []
        thread = threading.Thread(target=lambda: self._capture(lambda: buffer.put("second"), outcome))
        thread.start()
        time.sleep(0.05)
        buffer.cancel()
        thread.join(1)
        self.assertTrue(outcome and isinstance(outcome[0], Cancelled))

    def test_sigmf_replay_reads_small_chunks_from_standard_metadata(self):
        import json
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            np.arange(16, dtype=np.int8).tofile(root / "capture.sigmf-data")
            (root / "capture.sigmf-meta").write_text(json.dumps({
                "global": {"core:datatype": "ci8_le"},
                "captures": [{"core:sample_start": 0, "core:frequency": 98_000_000}],
            }))
            chunks = list(SigMFReplay(root / "capture.sigmf-meta", 2).chunks())
            self.assertEqual([chunk.sample_start for chunk in chunks], [0, 2, 4, 6])
            self.assertEqual(chunks[0].samples.shape, (2, 2))

    @staticmethod
    def _capture(function, outcome):
        try:
            function()
        except Exception as exc:
            outcome.append(exc)


@unittest.skipUnless(np is not None and torch is not None, "numpy and torch are not installed")
class RealtimePipelineTest(unittest.TestCase):
    def test_injection_runs_inference_and_cancels_workers(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            checkpoint = Path(directory) / "model.pt"
            model = build_cnn(CNNConfig(), 16)
            torch.save({"model": model.state_dict()}, checkpoint)
            pipeline = RealtimePipeline()
            pipeline.configure(checkpoint_path=str(checkpoint), window_length=16, stride=16, chunk_size=16)
            pipeline.start()
            pipeline.inject(np.ones((32, 2), dtype=np.float32), 10)
            deadline = time.time() + 5
            while not pipeline.predictions() and time.time() < deadline:
                time.sleep(0.02)
            self.assertTrue(pipeline.predictions())
            prediction = pipeline.predictions()[0]
            self.assertEqual(set(prediction), {"timestamp", "sample_start", "window_length", "label", "class_id", "confidence", "probabilities"})
            self.assertGreaterEqual(pipeline.metrics()["inferences"], 1)
            self.assertEqual(pipeline.stop()["status"], "cancelled")


if __name__ == "__main__":
    unittest.main()
