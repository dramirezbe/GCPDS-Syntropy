import json
from pathlib import Path
import threading
import unittest
from http.client import HTTPConnection
from unittest.mock import patch

from mcp_server import web_server


class WebServerTest(unittest.TestCase):
    def setUp(self):
        self.state = web_server.DashboardState({"checkpoint_path": "model.pt"})
        self.httpd = web_server.DashboardHTTPServer(("127.0.0.1", 0), self.state)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.connection = HTTPConnection("127.0.0.1", self.httpd.server_port)

    def tearDown(self):
        self.connection.close()
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(2)

    def request(self, method, path, body=None, headers=None):
        payload = None if body is None else json.dumps(body)
        request_headers = headers or {}
        if payload is not None:
            request_headers = {"Content-Type": "application/json", **request_headers}
        self.connection.request(method, path, payload, request_headers)
        response = self.connection.getresponse()
        raw = response.read()
        return response, (json.loads(raw) if response.getheader("Content-Type", "").startswith("application/json") else raw)

    def test_health_index_and_headers(self):
        response, data = self.request("GET", "/api/health")
        self.assertEqual(response.status, 200)
        self.assertTrue(data["ok"])
        self.assertIn("no-store", response.getheader("Cache-Control"))
        response, body = self.request("GET", "/")
        self.assertEqual(response.status, 200)
        self.assertIn(b"Realtime CNN dashboard", body)
        self.assertIn("text/html", response.getheader("Content-Type"))

    def test_json_api_and_limit_validation(self):
        with patch.object(web_server.server, "get_pipeline_status", return_value={"ok": True, "status": {"status": "idle"}}), \
             patch.object(web_server.server, "get_pipeline_metrics", return_value={"ok": True, "metrics": {"windows": 2}}), \
             patch.object(web_server.server, "get_predictions", return_value={"ok": True, "predictions": []}) as predictions:
            self.assertEqual(self.request("GET", "/api/status")[1]["ok"], True)
            self.assertEqual(self.request("GET", "/api/metrics")[1]["metrics"]["windows"], 2)
            self.assertTrue(self.request("GET", "/api/predictions?limit=20")[1]["ok"])
            predictions.assert_called_with(20)
        for limit in ("0", "101", "bad"):
            response, data = self.request("GET", f"/api/predictions?limit={limit}")
            self.assertEqual(response.status, 400)
            self.assertFalse(data["ok"])

    def test_methods_content_type_and_invalid_json(self):
        response, data = self.request("POST", "/api/start", {}, {"Content-Type": "text/plain"})
        self.assertEqual(response.status, 400)
        self.assertEqual(data["error"]["type"], "ValueError")
        response, data = self.request("POST", "/api/start", None)
        self.assertEqual(response.status, 400)
        response, data = self.request("POST", "/api/start", "not-an-object")
        self.assertEqual(response.status, 400)
        response, data = self.request("PUT", "/api/health")
        self.assertEqual(response.status, 501)

    def test_controls_delegate_to_public_wrappers(self):
        with patch.object(web_server.server, "configure_pipeline", return_value={"ok": True, "status": {"status": "configured"}}) as configure, \
             patch.object(web_server.server, "start_realtime_pipeline", return_value={"ok": True}) as start, \
             patch.object(web_server.server, "stop_realtime_pipeline", return_value={"ok": True}) as stop, \
             patch.object(web_server.server, "inject_iq", return_value={"ok": True, "accepted_samples": 2}) as inject:
            response, data = self.request("POST", "/api/configure", {"window_length": 512})
            self.assertEqual(response.status, 200)
            configure.assert_called_once()
            self.assertEqual(data["ok"], True)
            self.assertTrue(self.request("POST", "/api/start", {})[1]["ok"])
            self.assertTrue(self.request("POST", "/api/stop", {})[1]["ok"])
            self.assertTrue(self.request("POST", "/api/inject", {"samples": [[1, 2], [3, 4]]})[1]["ok"])
            self.assertTrue(self.request("POST", "/api/fixture", {})[1]["ok"])
            start.assert_called_once()
            stop.assert_called_once()
            self.assertEqual(inject.call_count, 2)

    def test_static_path_traversal_is_rejected(self):
        for path in ("/../web_server.py", "/%2e%2e/web_server.py", "/styles.css/../web_server.py"):
            response, data = self.request("GET", path)
            self.assertEqual(response.status, 404)
            self.assertFalse(data["ok"])

    def test_cleanup_removes_bootstrap(self):
        resolution = type("Resolution", (), {"cleanup": unittest.mock.Mock()})()
        state = web_server.DashboardState(resolution=resolution)
        state.cleanup()
        resolution.cleanup.assert_called_once()
        self.assertIsNone(state.resolution)


class WebServerResolutionTest(unittest.TestCase):
    def test_explicit_checkpoint_is_resolved_before_server(self):
        with patch.object(web_server, "resolve_checkpoint", side_effect=FileNotFoundError("checkpoint not found")):
            with self.assertRaisesRegex(FileNotFoundError, "checkpoint not found"):
                web_server.run_server(port=0, checkpoint="missing.pt")


if __name__ == "__main__":
    unittest.main()
