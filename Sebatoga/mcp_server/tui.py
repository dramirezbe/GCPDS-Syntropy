"""Dependency-free terminal dashboard for the realtime CNN pipeline."""

from __future__ import annotations

import argparse
import sys
import time
from typing import Any, TextIO

from . import server

try:
    import curses
except ImportError:  # pragma: no cover - platform dependent.
    curses = None  # type: ignore[assignment]


def _value(result: dict[str, Any], key: str, default: Any) -> Any:
    return result.get(key, default) if result.get("ok", True) else default


def render_dashboard(status: dict[str, Any], metrics: dict[str, Any],
                     predictions: list[dict[str, Any]], config: dict[str, Any],
                     width: int = 100, height: int = 24) -> list[str]:
    """Return a bounded, terminal-safe snapshot suitable for curses or ANSI."""
    width, height = max(1, width), max(1, height)
    state = status.get("status", "unknown")
    latest = predictions[-1] if predictions else None
    buffers = metrics.get("buffer") or {}

    def shorten(value: Any) -> str:
        text = str(value)
        return text if len(text) <= width else text[: max(0, width - 3)] + "..."

    lines = [
        "Realtime CNN Dashboard",
        f"State: {state}"
        + (f" | Error: {status.get('error')}" if status.get("error") else ""),
        f"Source: {config.get('source', '-')} | Checkpoint: {config.get('checkpoint_path', '-')}",
        f"Window/stride/chunk: {config.get('window_length', '-')} / {config.get('stride', '-')} / {config.get('chunk_size', '-')}",
        f"Samples: {metrics.get('samples_received', 0)} | Chunks: {metrics.get('chunks_received', 0)} | Windows: {metrics.get('windows', 0)} | Inferences: {metrics.get('inferences', 0)}",
        f"Throughput: {metrics.get('throughput_samples_per_second', 0.0):.2f} samples/s | Latency: {_latency(metrics):.4f} s",
        f"Buffers: raw {_buffer_text(buffers.get('raw'))} | processed {_buffer_text(buffers.get('processed'))} | Drops: {metrics.get('drops', 0)}",
        f"Latest: {_prediction_text(latest)}",
        "Recent predictions:",
    ]
    if predictions:
        lines.extend(f"  {item.get('timestamp', '-')} {item.get('label', '-')} ({float(item.get('confidence', 0.0)):.3f}) @ {item.get('sample_start', '-') }" for item in predictions[-5:])
    else:
        lines.append("  none")
    lines.append("Keys: [i] inject fixture  [r] refresh  [s] stop  [q/Esc] quit")
    return [shorten(line) for line in lines[:height]]


def _latency(metrics: dict[str, Any]) -> float:
    values = metrics.get("latencies_seconds") or []
    return sum(values) / len(values) if values else 0.0


def _buffer_text(buffer: dict[str, Any] | None) -> str:
    if not buffer:
        return "-"
    return f"{buffer.get('depth', 0)}/{buffer.get('capacity', 0)}"


def _prediction_text(prediction: dict[str, Any] | None) -> str:
    if not prediction:
        return "none"
    return f"{prediction.get('label', '-')} ({float(prediction.get('confidence', 0.0)):.3f})"


def key_action(key: int | str) -> str | None:
    """Map curses keys to actions; kept pure for direct unit testing."""
    if key in (27, "q", "Q"):
        return "quit"
    if key in (ord("s"), ord("S"), "s", "S"):
        return "stop"
    if key in (ord("r"), ord("R"), "r", "R"):
        return "refresh"
    if key in (ord("i"), ord("I"), "i", "I"):
        return "inject"
    return None


def injection_fixture(window_length: int) -> list[list[float]]:
    """Create deterministic I/Q pairs containing at least one full window."""
    if window_length <= 0:
        raise ValueError("window_length must be positive")
    return [[1.0 if index % 2 == 0 else 0.5, -0.25] for index in range(window_length)]


def _snapshot(config: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    status_result = server.get_pipeline_status()
    metrics_result = server.get_pipeline_metrics()
    predictions_result = server.get_predictions(5)
    return (_value(status_result, "status", {}), _value(metrics_result, "metrics", {}),
            _value(predictions_result, "predictions", []))


def _inject(config: dict[str, Any]) -> None:
    server.inject_iq(injection_fixture(int(config["window_length"])), 0)


def _draw(stdscr: Any, lines: list[str]) -> None:
    stdscr.erase()
    try:
        rows, columns = stdscr.getmaxyx()
        for row, line in enumerate(lines[: max(0, rows - 1)]):
            stdscr.addnstr(row, 0, line, max(0, columns - 1))
        stdscr.refresh()
    except (AttributeError, curses.error if curses else Exception):
        # Resizing and very small terminals can race with drawing.
        return


def _curses_loop(stdscr: Any, config: dict[str, Any], refresh: float) -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    while True:
        status, metrics, predictions = _snapshot(config)
        _draw(stdscr, render_dashboard(status, metrics, predictions, config, *stdscr.getmaxyx()))
        if status.get("status") == "completed":
            return
        key = stdscr.getch()
        action = key_action(key)
        if action == "quit":
            return
        if action == "stop":
            return
        if action == "inject":
            _inject(config)
        time.sleep(refresh)


def _ansi_loop(config: dict[str, Any], refresh: float, output: TextIO, once: bool) -> None:
    while True:
        status, metrics, predictions = _snapshot(config)
        output.write("\033[2J\033[H" + "\n".join(render_dashboard(status, metrics, predictions, config)) + "\n")
        output.flush()
        if once or status.get("status") == "completed":
            return
        time.sleep(refresh)


def run_dashboard(config: dict[str, Any], refresh: float = 1.0, *, fixture: bool = False,
                  input_stream: TextIO | None = None, output: TextIO | None = None) -> None:
    """Configure and run the dashboard, always stopping the public pipeline wrapper."""
    input_stream = input_stream or sys.stdin
    output = output or sys.stdout
    try:
        result = server.configure_pipeline(**config)
        if not result.get("ok", True):
            raise RuntimeError(result.get("error", result))
        result = server.start_realtime_pipeline()
        if not result.get("ok", True):
            raise RuntimeError(result.get("error", result))
        if fixture:
            _inject(config)
            if not (output.isatty() and input_stream.isatty()):
                time.sleep(min(max(refresh, 0.05), 1.0))
        if curses is not None and output.isatty() and input_stream.isatty():
            curses.wrapper(lambda stdscr: _curses_loop(stdscr, config, refresh))
        else:
            _ansi_loop(config, refresh, output, once=True)
    except KeyboardInterrupt:
        return
    finally:
        # The wrapper is deliberately called even when setup or rendering fails.
        server.stop_realtime_pipeline()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--source", choices=("injection", "sigmf"), default="injection")
    parser.add_argument("--sigmf-meta")
    parser.add_argument("--window-length", type=int, default=1024)
    parser.add_argument("--stride", type=int)
    parser.add_argument("--chunk-size", type=int, default=1024)
    parser.add_argument("--buffer-capacity", type=int, default=8)
    parser.add_argument("--overflow-policy", choices=("block", "drop_oldest"), default="block")
    parser.add_argument("--refresh", type=float, default=1.0)
    parser.add_argument("--inject-fixture", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = {"checkpoint_path": args.checkpoint, "source": args.source,
              "sigmf_meta_path": args.sigmf_meta, "window_length": args.window_length,
              "stride": args.stride or args.window_length, "chunk_size": args.chunk_size,
              "buffer_capacity": args.buffer_capacity, "overflow_policy": args.overflow_policy}
    run_dashboard(config, max(0.01, args.refresh), fixture=args.inject_fixture)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
