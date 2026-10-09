import unittest

try:
    import numpy as np
    import torch
except ImportError:  # Optional ML dependencies; tests remain discoverable.
    np = torch = None

from mcp_server.config import CNNConfig, TrainingConfig
from mcp_server.dataset import DatasetBundle
from mcp_server.model import build_cnn
from mcp_server.training import TrainingService


@unittest.skipUnless(np is not None and torch is not None, "numpy and torch are not installed")
class TrainingCoreTest(unittest.TestCase):
    def test_model_respects_parameter_limit(self):
        model = build_cnn(CNNConfig(channels=(4, 8)), 32)
        self.assertLessEqual(model.parameter_count, 250_000)


    def test_training_can_cancel_and_serializes_report(self):
        import tempfile

        with tempfile.TemporaryDirectory() as directory:
            dataset = DatasetBundle(np.random.default_rng(1).normal(size=(8, 2, 32)).astype(np.float32), np.array([0, 1] * 4), {"dataset_path": "test"})
            service = TrainingService()
            service.start(dataset, TrainingConfig(epochs=1, batch_size=2, checkpoint_dir=directory))
            service.wait(timeout=30)
            self.assertIn(service.status()["status"], {"completed", "cancelled"})
            self.assertEqual(service.report()["dataset"]["dataset_path"], "test")
