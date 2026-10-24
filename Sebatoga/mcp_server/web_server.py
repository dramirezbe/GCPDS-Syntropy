"""Dependency-free local HTTP dashboard for the realtime CNN pipeline."""

from __future__ import annotations

import argparse
import json
import mimetypes
from pathlib import Path
import signal
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit
from typing import Any

from . import server
from .tui import injection_fixture, resolve_checkpoint


STATIC_ROOT = Path(__file__).with_name("static").resolve()
MAX_BODY_BYTES = 2 * 1024 * 1024
DEFAULT_CONFIG = {
    "source": "injection",
    "window_length": 1024,
    "stride": 1024,
    "chunk_size": 1024,
    "buffer_capacity": 8,
    "overflow_policy": "block",
}


def _error(exc: Exception) -> dict[str, Any]:
    return {"ok": False, "error": {"type": type(exc).__name__, "message": str(exc)}}


class DashboardState:
    """Small web-owned state holder; the pipeline itself remains in server.py."""

    def __init__(self, config: dict[str, Any] | None = None, resolution: Any = None) -> None:
        self.lock = threading.RLock()
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.resolution = resolution

    def cleanup(self) -> None:
        if self.resolution is not None:
            self.resolution.cleanup()
            self.resolution = None


def _result(value: Any, key: str | None = None) -> dict[str, Any]:
    if isinstance(value, dict) and "ok" in value:
        return value
    return {"ok": True, **({key: value} if key else {})}


class DashboardHandler(BaseHTTPRequestHandler):
    """Serve static assets and a deliberately small JSON API."""

    server_version = "SyntropyDashboard/1.0"
    state: DashboardState

    def log_message(self, format: str, *args: Any) -> None:  # pragma: no cover - noisy server default
        return

    @property
    def dashboard(self) -> DashboardState:
        return self.server.dashboard_state  # type: ignore[attr-defined]

    def _send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, exc: Exception, status: int = 400) -> None:
        self._send_json(_error(exc), status)

    def _read_json(self) -> dict[str, Any]:
        content_type = self.headers.get_content_type()
        if content_type != "application/json":
            raise ValueError("Content-Type must be application/json")
        try:
            length = int(self.headers.get("Content-Length", "-1"))
        except ValueError as exc:
            raise ValueError("Content-Length must be an integer") from exc
        if length < 0 or length > MAX_BODY_BYTES:
            raise ValueError(f"request body must be between 0 and {MAX_BODY_BYTES} bytes")
        try:
            value = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("request body must contain valid JSON") from exc
        if not isinstance(value, dict):
            raise ValueError("JSON body must be an object")
        return value

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlsplit(self.path)
        if parsed.path.startswith("/api/"):
            self._api_get(parsed.path, parse_qs(parsed.query, keep_blank_values=True))
        else:
            self._static(parsed.path)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlsplit(self.path)
        if not parsed.path.startswith("/api/"):
            self._send_error(ValueError("POST is only supported for API routes"), 405)
            return
        if parsed.path not in {"/api/configure", "/api/start", "/api/stop", "/api/inject", "/api/fixture"}:
            self._send_error(ValueError("API route not found"), 404)
            return
        try:
            body = self._read_json()
            result = self._api_post(parsed.path, body)
            self._send_json(result)
        except Exception as exc:
            self._send_error(exc)

    def _api_get(self, path: str, query: dict[str, list[str]]) -> None:
        try:
            if path == "/api/health":
                self._send_json({"ok": True, "service": "syntropy-realtime-dashboard"})
            elif path == "/api/status":
                self._send_json(_result(server.get_pipeline_status()))
            elif path == "/api/metrics":
                self._send_json(_result(server.get_pipeline_metrics()))
            elif path == "/api/predictions":
                raw_limit = query.get("limit", ["20"])[0]
                limit = int(raw_limit)
                if not 1 <= limit <= 100:
                    raise ValueError("limit must be between 1 and 100")
                self._send_json(_result(server.get_predictions(limit)))
            elif path == "/api/config":
                with self.dashboard.lock:
                    self._send_json({"ok": True, "config": dict(self.dashboard.config)})
            else:
                self._send_error(ValueError("API route not found"), 404)
        except (TypeError, ValueError) as exc:
            self._send_error(exc)

    def _api_post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        if path == "/api/configure":
            allowed = {"checkpoint_path", "source", "sigmf_meta_path", "window_length", "stride",
                       "chunk_size", "buffer_capacity", "overflow_policy"}
            values = {key: value for key, value in body.items() if key in allowed}
            if "checkpoint_path" not in values:
                with self.dashboard.lock:
                    values["checkpoint_path"] = self.dashboard.config.get("checkpoint_path")
            result = server.configure_pipeline(**values)
            if result.get("ok", True):
                with self.dashboard.lock:
                    self.dashboard.config.update(values)
                    self.dashboard.config.update(result.get("status", {}))
            return result
        if path == "/api/start":
            return _result(server.start_realtime_pipeline())
        if path == "/api/stop":
            return _result(server.stop_realtime_pipeline())
        if path == "/api/inject":
            samples = body.get("samples")
            if not isinstance(samples, list):
                raise ValueError("samples must be a list")
            sample_start = body.get("sample_start", 0)
            return _result(server.inject_iq(samples, int(sample_start)))
        if path == "/api/fixture":
            with self.dashboard.lock:
                length = int(body.get("window_length", self.dashboard.config["window_length"]))
            return _result(server.inject_iq(injection_fixture(length), int(body.get("sample_start", 0))))
        raise ValueError("API route not found")

    def _static(self, path: str) -> None:
        if path == "/":
            path = "/index.html"
        if "\\" in path or ".." in Path(path).parts:
            self._send_error(ValueError("unsafe static path"), 404)
            return
        relative = Path(path.lstrip("/"))
        candidate = (STATIC_ROOT / relative).resolve()
        try:
            candidate.relative_to(STATIC_ROOT)
        except ValueError:
            self._send_error(ValueError("unsafe static path"), 404)
            return
        if not candidate.is_file():
            self._send_error(FileNotFoundError("static file not found"), 404)
            return
        body = candidate.read_bytes()
        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class DashboardHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True

    def __init__(self, address: tuple[str, int], state: DashboardState) -> None:
        super().__init__(address, DashboardHandler)
        self.dashboard_state = state


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--checkpoint")
    return parser


def run_server(host: str = "127.0.0.1", port: int = 8765, checkpoint: str | None = None) -> int:
    resolution = resolve_checkpoint(checkpoint, DEFAULT_CONFIG["window_length"])
    config = {**DEFAULT_CONFIG, "checkpoint_path": str(resolution.path), "checkpoint_bootstrap": resolution.bootstrap}
    state = DashboardState(config, resolution)
    httpd = DashboardHTTPServer((host, port), state)
    stopped = False

    def shutdown(signum: int, _frame: Any) -> None:
        nonlocal stopped
        if stopped:
            return
        stopped = True
        server.stop_realtime_pipeline()
        state.cleanup()
        threading.Thread(target=httpd.shutdown, daemon=True).start()

    old_handlers = {item: signal.getsignal(item) for item in (signal.SIGINT, signal.SIGTERM)}
    try:
        for item in old_handlers:
            signal.signal(item, shutdown)
        print(f"Syntropy dashboard listening on http://{host}:{httpd.server_port}")
        httpd.serve_forever()
    finally:
        server.stop_realtime_pipeline()
        state.cleanup()
        httpd.server_close()
        for item, handler in old_handlers.items():
            signal.signal(item, handler)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return run_server(args.host, args.port, args.checkpoint)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
