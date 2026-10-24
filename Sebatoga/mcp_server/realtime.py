"""Small bounded raw-IQ replay, DSP, and CNN inference pipeline."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import threading
import time
from typing import Any, Iterable

from ._optional import require_numpy, require_torch
from .config import CNNConfig
from .model import build_cnn


class Cancelled(Exception):
    """Raised when a blocking pipeline operation is cancelled."""


@dataclass
class IQChunk:
    sample_start: int
    samples: Any


class RingBuffer:
    """Bounded FIFO with blocking and drop-oldest overflow policies."""

    def __init__(self, capacity: int, policy: str = "block") -> None:
        if capacity <= 0 or policy not in {"block", "drop_oldest"}:
            raise ValueError("capacity must be positive and policy must be block or drop_oldest")
        self.capacity, self.policy = capacity, policy
        self._items: deque[Any] = deque()
        self._condition = threading.Condition()
        self._cancelled = False
        self._closed = False
        self.drops = 0

    def put(self, item: Any, timeout: float | None = None) -> None:
        with self._condition:
            deadline = None if timeout is None else time.monotonic() + timeout
            while len(self._items) >= self.capacity and self.policy == "block":
                self._wait(deadline)
            self._check()
            if self._closed:
                raise RuntimeError("buffer is closed")
            if len(self._items) >= self.capacity:
                self._items.popleft()
                self.drops += 1
            self._items.append(item)
            self._condition.notify_all()

    def get(self, timeout: float | None = None) -> Any:
        with self._condition:
            deadline = None if timeout is None else time.monotonic() + timeout
            while not self._items:
                if self._closed:
                    raise EOFError("buffer is closed")
                self._wait(deadline)
            self._check()
            item = self._items.popleft()
            self._condition.notify_all()
            return item

    def cancel(self) -> None:
        with self._condition:
            self._cancelled = True
            self._condition.notify_all()

    def close(self) -> None:
        with self._condition:
            self._closed = True
            self._condition.notify_all()

    def snapshot(self) -> dict[str, int]:
        with self._condition:
            return {"depth": len(self._items), "capacity": self.capacity, "drops": self.drops}

    def _check(self) -> None:
        if self._cancelled:
            raise Cancelled()

    def _wait(self, deadline: float | None) -> None:
        self._check()
        remaining = None if deadline is None else deadline - time.monotonic()
        if remaining is not None and remaining <= 0:
            raise TimeoutError("buffer operation timed out")
        self._condition.wait(remaining)


class SigMFReplay:
    """Chunked SigMF replay; only the current memmap slice is materialized."""

    def __init__(self, metadata_path: str | Path, chunk_size: int) -> None:
        self.metadata_path, self.chunk_size = Path(metadata_path), chunk_size

    def chunks(self) -> Iterable[IQChunk]:
        np = require_numpy()
        meta = json.loads(self.metadata_path.read_text(encoding="utf-8"))
        datatype = meta.get("global", {}).get("core:datatype", "").lower()
        if datatype != "ci8_le":
            raise ValueError("replay requires global.core:datatype=ci8_le")
        data_path = self.metadata_path.with_name(self.metadata_path.name.removesuffix("-meta") + "-data")
        raw = np.memmap(data_path, dtype=np.int8, mode="r").reshape(-1, 2)
        captures = meta.get("captures") or [{"core:sample_start": 0}]
        for index, capture in enumerate(captures):
            start = int(capture.get("core:sample_start", 0))
            end = int((captures[index + 1] if index + 1 < len(captures) else {}).get("core:sample_start", len(raw)))
            for offset in range(start, min(end, len(raw)), self.chunk_size):
                yield IQChunk(offset, raw[offset : min(offset + self.chunk_size, end)])


class IQDSP:
    """Convert raw complex IQ or I/Q pairs to the CNN's normalized 2-channel input."""

    def process(self, samples: Any) -> Any:
        np = require_numpy()
        array = np.asarray(samples)
        if np.iscomplexobj(array):
            channels = np.stack((array.real, array.imag))
        elif array.ndim == 2 and array.shape[1] == 2:
            channels = array.T
        elif array.ndim == 2 and array.shape[0] == 2:
            channels = array
        else:
            raise ValueError("IQ samples must be complex (L,), (L,2), or (2,L)")
        channels = channels.astype(np.float32, copy=False)
        power = np.sqrt(np.mean(channels * channels, dtype=np.float32))
        return (channels / max(float(power), 1e-12)).astype(np.float32)


class RealtimePipeline:
    """Singleton-friendly three-stage source, DSP, and inference service."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._cancel = threading.Event()
        self._threads: list[threading.Thread] = []
        self._status = "idle"
        self._error: str | None = None
        self._config: dict[str, Any] = {}
        self._predictions: deque[dict[str, Any]] = deque(maxlen=100)
        self._metrics: dict[str, Any] = {}
        self._raw: RingBuffer | None = None
        self._processed: RingBuffer | None = None

    def configure(self, **values: Any) -> dict[str, Any]:
        if self.is_running():
            raise RuntimeError("pipeline is running")
        checkpoint = values.get("checkpoint_path")
        if not checkpoint or not Path(checkpoint).exists():
            raise FileNotFoundError("checkpoint_path must point to an existing checkpoint")
        values.setdefault("source", "injection")
        values.setdefault("chunk_size", 1024)
        values.setdefault("window_length", 1024)
        values.setdefault("stride", values["window_length"])
        values.setdefault("buffer_capacity", 8)
        values.setdefault("overflow_policy", "block")
        if values["source"] not in {"injection", "sigmf"} or values["window_length"] <= 0 or values["stride"] <= 0:
            raise ValueError("invalid source, window_length, or stride")
        if values["source"] == "sigmf" and not values.get("sigmf_meta_path"):
            raise ValueError("sigmf_meta_path is required for replay")
        if values["overflow_policy"] not in {"block", "drop_oldest"}:
            raise ValueError("overflow_policy must be block or drop_oldest")
        with self._lock:
            self._config = dict(values)
            self._status = "configured"
        return self.status()

    def start(self) -> dict[str, Any]:
        with self._lock:
            if self.is_running():
                raise RuntimeError("pipeline is already running")
            if not self._config:
                raise RuntimeError("pipeline is not configured")
            self._cancel.clear()
            self._started_at = time.time()
            self._error = None
            self._predictions.clear()
            self._metrics = {"samples_received": 0, "chunks_received": 0, "windows": 0, "inferences": 0,
                             "latencies_seconds": [], "throughput_samples_per_second": 0.0}
            self._raw = RingBuffer(self._config["buffer_capacity"], self._config["overflow_policy"])
            self._processed = RingBuffer(self._config["buffer_capacity"], self._config["overflow_policy"])
            self._status = "starting"
            self._threads = [threading.Thread(target=self._source_loop, daemon=True), threading.Thread(target=self._dsp_loop, daemon=True), threading.Thread(target=self._inference_loop, daemon=True)]
            for thread in self._threads:
                thread.start()
        return self.status()

    def inject(self, samples: Any, sample_start: int = 0) -> dict[str, Any]:
        if self._raw is None or not self.is_running():
            raise RuntimeError("pipeline is not running")
        np = require_numpy()
        array = np.asarray(samples)
        count = array.shape[-1] if array.ndim == 2 and array.shape[0] == 2 else array.shape[0]
        self._raw.put(IQChunk(int(sample_start), array))
        return {"accepted_samples": int(count)}

    def stop(self) -> dict[str, Any]:
        self._cancel.set()
        for buffer in (self._raw, self._processed):
            if buffer:
                buffer.cancel()
        self._join()
        return self.status()

    def status(self) -> dict[str, Any]:
        with self._lock:
            return {"status": self._status, "error": self._error, "configured": bool(self._config), "predictions": len(self._predictions), "latest_prediction_timestamp": self._predictions[-1]["timestamp"] if self._predictions else None}

    def metrics(self) -> dict[str, Any]:
        with self._lock:
            result = dict(self._metrics)
            result["latencies_seconds"] = list(result.get("latencies_seconds", []))
            result["buffer"] = {"raw": self._raw.snapshot() if self._raw else None, "processed": self._processed.snapshot() if self._processed else None}
            result["drops"] = sum(value["drops"] for value in result["buffer"].values() if value)
            return result

    def predictions(self, limit: int = 20) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._predictions)[-max(1, min(limit, 100)):]

    def is_running(self) -> bool:
        return self._status in {"starting", "running", "stopping"}

    def _source_loop(self) -> None:
        try:
            if self._config["source"] == "sigmf":
                for chunk in SigMFReplay(self._config["sigmf_meta_path"], self._config["chunk_size"]).chunks():
                    if self._cancel.is_set():
                        raise Cancelled()
                    self._raw.put(chunk)
                self._raw.close()
            else:
                with self._lock:
                    self._status = "running"
                while not self._cancel.wait(0.1):
                    pass
        except (Cancelled, EOFError):
            pass
        except Exception as exc:
            self._fail(exc)
        finally:
            if self._config.get("source") == "sigmf" and self._raw:
                self._raw.close()

    def _dsp_loop(self) -> None:
        try:
            while not self._cancel.is_set():
                try:
                    chunk = self._raw.get(0.2)
                except TimeoutError:
                    continue
                except EOFError:
                    break
                processed = IQChunk(chunk.sample_start, IQDSP().process(chunk.samples))
                self._processed.put(processed)
                with self._lock:
                    self._metrics["chunks_received"] += 1
                    self._metrics["samples_received"] += int(processed.samples.shape[-1])
            self._processed.close()
        except (Cancelled, EOFError):
            pass
        except Exception as exc:
            self._fail(exc)

    def _inference_loop(self) -> None:
        try:
            torch = require_torch()
            np = require_numpy()
            config = self._config
            device = torch.device("cpu")
            model = build_cnn(CNNConfig(), config["window_length"]).to(device)
            checkpoint = torch.load(config["checkpoint_path"], map_location=device, weights_only=False)
            state = checkpoint.get("model", checkpoint) if isinstance(checkpoint, dict) else checkpoint
            model.load_state_dict(state)
            model.eval()
            pending = np.empty((2, 0), dtype=np.float32)
            pending_start = 0
            first = True
            while not self._cancel.is_set():
                try:
                    chunk = self._processed.get(0.2)
                except TimeoutError:
                    continue
                except EOFError:
                    break
                if first:
                    pending_start, first = chunk.sample_start, False
                pending = np.concatenate((pending, chunk.samples), axis=1)
                while len(pending[0]) >= config["window_length"]:
                    window = pending[:, :config["window_length"]]
                    started = time.perf_counter()
                    with torch.inference_mode():
                        probabilities = torch.softmax(model(torch.from_numpy(window[None]).to(device)), dim=1)[0].cpu().numpy()
                    latency = time.perf_counter() - started
                    class_id = int(probabilities.argmax())
                    prediction = {"timestamp": datetime.now(timezone.utc).isoformat(), "sample_start": int(pending_start), "window_length": config["window_length"], "label": "fm" if class_id == 1 else "noise", "class_id": class_id, "confidence": float(probabilities[class_id]), "probabilities": {"noise": float(probabilities[0]), "fm": float(probabilities[1])}}
                    with self._lock:
                        self._predictions.append(prediction)
                        self._metrics["windows"] += 1
                        self._metrics["inferences"] += 1
                        self._metrics["latencies_seconds"].append(latency)
                        elapsed = max(time.time() - getattr(self, "_started_at", time.time()), 1e-9)
                        self._metrics["throughput_samples_per_second"] = self._metrics["samples_received"] / elapsed
                    pending = pending[:, config["stride"]:]
                    pending_start += config["stride"]
            if not self._cancel.is_set():
                with self._lock:
                    self._status = "completed"
        except (Cancelled, EOFError):
            pass
        except Exception as exc:
            self._fail(exc)

    def _fail(self, exc: Exception) -> None:
        with self._lock:
            self._error, self._status = f"{type(exc).__name__}: {exc}", "failed"
        self._cancel.set()
        for buffer in (self._raw, self._processed):
            if buffer:
                buffer.cancel()

    def _join(self) -> None:
        with self._lock:
            if self._status not in {"failed", "completed"}:
                self._status = "stopping"
        for thread in self._threads:
            thread.join(timeout=5)
        with self._lock:
            if self._status == "stopping":
                self._status = "cancelled"
