import json

import unittest

try:
    import numpy as np
except ImportError:  # Optional ML dependency; the test remains discoverable.
    np = None

from mcp_server.config import DatasetConfig
from mcp_server.dataset import SigMFLoader


@unittest.skipUnless(np is not None, "numpy is not installed")
class DatasetTest(unittest.TestCase):
    def test_sigmf_core_keys_preserve_iq_window_shape_and_capture_metadata(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            meta_path = tmp_path / "capture.sigmf-meta"
            data_path = tmp_path / "capture.sigmf-data"
            (np.array([1, 0, 2, 0, 3, 0, 4, 0], dtype=np.int8)).tofile(data_path)
            meta_path.write_text(json.dumps({
                "global": {"core:datatype": "ci8_le"},
                "captures": [{"core:sample_start": 0, "core:frequency": 98_000_000}],
            }))
            bundle = SigMFLoader(DatasetConfig(path=str(tmp_path), window_length=2, stride=2, seed=7)).load()
            self.assertEqual(bundle.samples.shape, (4, 2, 2))
            self.assertEqual(bundle.samples.dtype, np.float32)
            self.assertTrue(np.allclose(np.mean(bundle.samples[:3] ** 2, axis=(1, 2)), 1.0))
            self.assertEqual(bundle.labels.tolist(), [1, 1, 0, 0])
            self.assertEqual(bundle.metadata["captures"][0]["window_count"], 2)
            self.assertEqual(bundle.metadata["captures"][0]["sample_start"], 0)
            self.assertEqual(bundle.metadata["captures"][0]["frequency"], 98_000_000)

    def test_legacy_unqualified_keys_remain_supported(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            (np.array([1, 0, 2, 0], dtype=np.int8)).tofile(tmp_path / "capture.sigmf-data")
            (tmp_path / "capture.sigmf-meta").write_text(json.dumps({
                "global": {"datatype": "ci8_le"},
                "captures": [{"sample_start": 0, "frequency": 99_000_000}],
            }))
            bundle = SigMFLoader(DatasetConfig(path=str(tmp_path), window_length=2, stride=2)).load()
            self.assertEqual(bundle.samples.shape, (2, 2, 2))
            self.assertEqual(bundle.metadata["captures"][0]["frequency"], 99_000_000)
