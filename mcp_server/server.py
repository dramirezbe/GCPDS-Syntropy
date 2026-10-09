"""Stdio MCP adapter for the configurable M1 training service.

The MCP SDK is optional at import time so configuration and dependency errors
are returned as ordinary JSON objects instead of obscure import failures.
"""

from dataclasses import replace
import json
import sys
from typing import Any

from .config import CNNConfig, DatasetConfig, TrainingConfig
from .dataset import SigMFLoader
from .training import TrainingService

try:  # MCP SDK 1.x; retain fallbacks for newer/re-exported APIs.
    from mcp.server.fastmcp import FastMCP
except ImportError:  # pragma: no cover - depends on the optional SDK version.
    try:
        from mcp.server import FastMCP
    except ImportError:  # pragma: no cover - exercised when MCP is absent.
        try:
            from mcp.server import MCPServer as FastMCP
        except ImportError:
            FastMCP = None


MCP_AVAILABLE = FastMCP is not None


class _LocalServer:
    """Small decorator-compatible stand-in used by dependency-aware tests."""

    def tool(self):
        def decorate(function):
            return function
        return decorate

    def run(self):
        raise RuntimeError("MCP SDK is unavailable; install the 'mcp' package to launch the stdio server")


mcp = FastMCP("syntropy-cnn") if MCP_AVAILABLE else _LocalServer()
_dataset = DatasetConfig()
_training = TrainingConfig()
_service = TrainingService()


def _ok(data: dict[str, Any]) -> dict[str, Any]:
    return {"ok": True, **data}


def _error(exc: Exception) -> dict[str, Any]:
    return {"ok": False, "error": {"type": type(exc).__name__, "message": str(exc)}}


def _configuration() -> dict[str, Any]:
    return {"dataset": _dataset.__dict__.copy(), "training": _training.to_dict(), "mcp_available": MCP_AVAILABLE}


@mcp.tool()
def get_current_configuration() -> dict[str, Any]:
    """Return the current dataset, CNN, optimizer, and runtime configuration."""
    try:
        return _ok({"configuration": _configuration()})
    except Exception as exc:
        return _error(exc)


@mcp.tool()
def configure_dataset(path: str | None = None, window_length: int | None = None, stride: int | None = None,
                      noise_ratio: float | None = None, seed: int | None = None,
                      max_windows: int | None = None, max_captures: int | None = None,
                      full_data: bool = False) -> dict[str, Any]:
    """Update dataset settings; max_windows=None intentionally enables full data."""
    global _dataset
    try:
        values = {key: value for key, value in {"path": path, "window_length": window_length, "stride": stride,
                 "noise_ratio": noise_ratio, "seed": seed, "max_windows": max_windows,
                 "max_captures": max_captures}.items() if value is not None}
        if full_data:
            values["max_windows"] = None
        candidate = replace(_dataset, **values)
        candidate.validate()
        _dataset = candidate
        return _ok({"dataset": _dataset.__dict__.copy()})
    except Exception as exc:
        return _error(exc)


@mcp.tool()
def configure_cnn(channels: list[int] | None = None, kernel_size: int | None = None,
                  activation: str | None = None, dropout: float | None = None) -> dict[str, Any]:
    """Update CNN channels, kernel size, activation, and dropout with validation."""
    global _training
    try:
        current = _training.cnn
        values = {key: value for key, value in {"channels": tuple(channels) if channels is not None else None,
                 "kernel_size": kernel_size, "activation": activation, "dropout": dropout}.items() if value is not None}
        cnn = replace(current, **values)
        cnn.validate()
        _training = replace(_training, cnn=cnn)
        return _ok({"cnn": cnn.__dict__.copy()})
    except Exception as exc:
        return _error(exc)


@mcp.tool()
def configure_training(learning_rate: float | None = None, batch_size: int | None = None,
                       epochs: int | None = None, optimizer: str | None = None,
                       device: str | None = None, checkpoint_dir: str | None = None) -> dict[str, Any]:
    """Update training hyperparameters and validate course limits."""
    global _training
    try:
        values = {key: value for key, value in {"learning_rate": learning_rate, "batch_size": batch_size,
                 "epochs": epochs, "optimizer": optimizer, "device": device,
                 "checkpoint_dir": checkpoint_dir}.items() if value is not None}
        candidate = replace(_training, **values)
        candidate.validate()
        _training = candidate
        return _ok({"training": _training.to_dict()})
    except Exception as exc:
        return _error(exc)


@mcp.tool()
def start_training() -> dict[str, Any]:
    """Start one background dataset-load and training run."""
    try:
        _dataset.validate()
        _training.validate()
        _service.start_loader(SigMFLoader(_dataset), _training)
        return _ok({"status": _service.status()})
    except Exception as exc:
        return _error(exc)


@mcp.tool()
def get_live_status() -> dict[str, Any]:
    """Return non-blocking progress for the current run."""
    try:
        return _ok({"status": _service.status()})
    except Exception as exc:
        return _error(exc)


@mcp.tool()
def stop_training() -> dict[str, Any]:
    """Request cancellation; the worker observes it between batches and epochs."""
    try:
        _service.cancel()
        return _ok({"status": _service.status(), "message": "cancellation requested"})
    except Exception as exc:
        return _error(exc)


@mcp.tool()
def get_system_metrics() -> dict[str, Any]:
    """Return current CPU, memory, and available GPU metrics."""
    try:
        return _ok({"metrics": _service.system_metrics()})
    except Exception as exc:
        return _error(exc)


@mcp.tool()
def get_final_report() -> dict[str, Any]:
    """Retrieve the last structured report, including provenance and split metrics."""
    try:
        report = _service.report()
        if report is None:
            return _error(RuntimeError("no training report is available"))
        return _ok({"report": report})
    except Exception as exc:
        return _error(exc)


@mcp.tool()
def save_final_report(path: str) -> dict[str, Any]:
    """Save the last structured report as JSON at the requested local path."""
    try:
        destination = _service.save_report(path)
        return _ok({"path": str(destination)})
    except Exception as exc:
        return _error(exc)


def main() -> int:
    if not MCP_AVAILABLE:
        print("MCP SDK is unavailable. Install it with: python3 -m pip install mcp", file=sys.stderr)
        return 2
    mcp.run()
    return 0


if __name__ == "__main__":  # pragma: no cover - stdio process entry point.
    raise SystemExit(main())
