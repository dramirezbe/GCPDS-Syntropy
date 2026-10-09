import unittest
import json

from mcp_server import server


class MCPConfigurationTest(unittest.TestCase):
    def test_configuration_tools_return_json_friendly_results(self):
        result = server.configure_cnn(channels=[4, 8], activation="gelu", dropout=0.2)
        self.assertTrue(result["ok"])
        self.assertEqual(result["cnn"]["channels"], (4, 8))
        result = server.configure_training(optimizer="sgd", batch_size=4, epochs=1)
        self.assertTrue(result["ok"])
        self.assertEqual(result["training"]["optimizer"], "sgd")
        json.dumps(server.get_current_configuration())

    def test_invalid_configuration_is_clear_and_does_not_apply(self):
        before = server.get_current_configuration()["configuration"]["training"]["optimizer"]
        result = server.configure_training(optimizer="not-an-optimizer")
        self.assertFalse(result["ok"])
        self.assertIn("optimizer", result["error"]["message"])
        self.assertEqual(server.get_current_configuration()["configuration"]["training"]["optimizer"], before)

    def test_start_without_dataset_reports_error_in_background(self):
        server.configure_dataset(path="/definitely/missing/dataset")
        result = server.start_training()
        self.assertTrue(result["ok"])
        server._service.wait(timeout=2)
        report = server.get_final_report()
        self.assertTrue(report["ok"])
        self.assertEqual(report["report"]["stop_reason"], "failed")
        self.assertTrue(
            "does not exist" in report["report"]["error"]
            or "requires numpy" in report["report"]["error"]
        )
        self.assertEqual(server.get_live_status()["status"]["status"], "failed")


if __name__ == "__main__":
    unittest.main()
