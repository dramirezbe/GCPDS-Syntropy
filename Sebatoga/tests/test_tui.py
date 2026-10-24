import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from mcp_server import tui


class TuiRendererTest(unittest.TestCase):
    def test_renderer_handles_running_and_failed_states(self):
        config = {"source": "injection", "checkpoint_path": "model.pt", "window_length": 8,
                  "stride": 8, "chunk_size": 8}
        metrics = {"samples_received": 8, "chunks_received": 1, "windows": 1, "inferences": 1,
                   "throughput_samples_per_second": 10.0, "latencies_seconds": [0.02], "drops": 0,
                   "buffer": {"raw": {"depth": 0, "capacity": 2}, "processed": {"depth": 0, "capacity": 2}}}
        prediction = {"label": "fm", "confidence": 0.9, "sample_start": 0, "timestamp": "now"}
        running = tui.render_dashboard({"status": "running"}, metrics, [prediction], config)
        failed = tui.render_dashboard({"status": "failed", "error": "boom"}, metrics, [], config)
        self.assertTrue(any("State: running" in line for line in running))
        self.assertTrue(any("State: failed" in line and "boom" in line for line in failed))

    def test_renderer_crops_small_terminal(self):
        lines = tui.render_dashboard({"status": "running"}, {}, [], {}, width=8, height=3)
        self.assertEqual(len(lines), 3)
        self.assertTrue(all(len(line) <= 8 for line in lines))


class TuiControlsTest(unittest.TestCase):
    def test_parser_has_safe_zero_argument_defaults(self):
        args = tui.build_parser().parse_args([])
        self.assertEqual((args.source, args.window_length, args.stride, args.chunk_size),
                         ("injection", 1024, None, 1024))
        self.assertEqual((args.buffer_capacity, args.overflow_policy, args.refresh), (8, "block", 1.0))
        self.assertTrue(args.inject_fixture)
        self.assertFalse(tui.build_parser().parse_args(["--no-inject-fixture"]).inject_fixture)

    def test_key_mapping(self):
        self.assertEqual(tui.key_action("q"), "quit")
        self.assertEqual(tui.key_action(27), "quit")
        self.assertEqual(tui.key_action("s"), "stop")
        self.assertEqual(tui.key_action("r"), "refresh")
        self.assertEqual(tui.key_action("i"), "inject")

    def test_parser_builds_injection_and_sigmf_configuration(self):
        args = tui.build_parser().parse_args(["--checkpoint", "m.pt", "--window-length", "16"])
        self.assertEqual((args.source, args.window_length), ("injection", 16))
        args = tui.build_parser().parse_args(["--checkpoint", "m.pt", "--source", "sigmf",
                                              "--sigmf-meta", "capture.sigmf-meta", "--stride", "4",
                                              "--overflow-policy", "drop_oldest"])
        self.assertEqual((args.source, args.sigmf_meta, args.stride, args.overflow_policy),
                         ("sigmf", "capture.sigmf-meta", 4, "drop_oldest"))

    def test_fixture_is_deterministic_and_covers_window(self):
        self.assertEqual(tui.injection_fixture(4), tui.injection_fixture(4))
        self.assertEqual(len(tui.injection_fixture(4)), 4)

    def test_explicit_missing_checkpoint_fails_clearly(self):
        with self.assertRaisesRegex(FileNotFoundError, "checkpoint not found"):
            tui.resolve_checkpoint("does-not-exist.pt", 8)

    def test_checkpoint_resolution_prefers_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            checkpoint = Path(directory) / "trained.pt"
            checkpoint.touch()
            with patch.dict(os.environ, {"SYNTROPY_CHECKPOINT": str(checkpoint)}):
                resolution = tui.resolve_checkpoint(None, 8)
            self.assertEqual(resolution.path, checkpoint)
            self.assertFalse(resolution.bootstrap)

    def test_bootstrap_checkpoint_is_temporary_and_cleaned(self):
        resolution = tui.resolve_checkpoint(None, 8)
        try:
            self.assertTrue(resolution.bootstrap)
            self.assertTrue(resolution.path.is_file())
        finally:
            resolution.cleanup()
        self.assertFalse(resolution.path.exists())

    def test_non_terminal_lifecycle_stops_in_finally(self):
        config = {"checkpoint_path": "m.pt", "source": "injection", "window_length": 4,
                  "stride": 4, "chunk_size": 4, "buffer_capacity": 2, "overflow_policy": "block"}
        output = io.StringIO()
        output.isatty = lambda: False
        stdin = io.StringIO()
        stdin.isatty = lambda: False
        with patch.object(tui.server, "configure_pipeline", return_value={"ok": True}), \
             patch.object(tui.server, "start_realtime_pipeline", return_value={"ok": True}), \
             patch.object(tui.server, "inject_iq", return_value={"ok": True}) as inject, \
             patch.object(tui.server, "get_pipeline_status", return_value={"ok": True, "status": {"status": "running"}}), \
             patch.object(tui.server, "get_pipeline_metrics", return_value={"ok": True, "metrics": {}}), \
             patch.object(tui.server, "get_predictions", return_value={"ok": True, "predictions": []}), \
             patch.object(tui.server, "stop_realtime_pipeline", return_value={"ok": True}) as stop:
            tui.run_dashboard(config, fixture=True, input_stream=stdin, output=output)
        inject.assert_called_once()
        stop.assert_called_once()


if __name__ == "__main__":
    unittest.main()
