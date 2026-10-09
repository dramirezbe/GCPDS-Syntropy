"""Non-blocking, cancellable training service and JSON report generation."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
import threading
import time
from typing import Any

from ._optional import require_numpy, require_torch
from .config import TrainingConfig
from .dataset import DatasetBundle, SigMFLoader
from .model import build_cnn


@dataclass
class RunState:
    status: str = "idle"
    epoch: int = 0
    batch: int = 0
    message: str | None = None
    report: dict[str, Any] | None = None


class TrainingService:
    """Run one training job in a worker thread while serving status snapshots."""

    def __init__(self):
        self._lock = threading.RLock()
        self._cancel = threading.Event()
        self._thread: threading.Thread | None = None
        self._state = RunState()

    def start(self, dataset: DatasetBundle, config: TrainingConfig) -> None:
        config.validate()
        self._launch(self._run, dataset, config)

    def start_loader(self, loader: SigMFLoader, config: TrainingConfig) -> None:
        """Load and train in the worker so callers never block on capture I/O."""
        config.validate()
        self._launch(self._run_loader, loader, config)

    def _launch(self, target: Any, *args: Any) -> None:
        with self._lock:
            if self._thread and self._thread.is_alive():
                raise RuntimeError("a training run is already active")
            self._cancel.clear()
            self._state = RunState(status="starting")
            self._thread = threading.Thread(target=target, args=args, daemon=True)
            self._thread.start()

    def cancel(self) -> None:
        self._cancel.set()

    def status(self) -> dict[str, Any]:
        with self._lock:
            return {"status": self._state.status, "epoch": self._state.epoch, "batch": self._state.batch, "message": self._state.message, "report_available": self._state.report is not None}

    def system_metrics(self) -> dict[str, Any]:
        metrics: dict[str, Any] = {"timestamp": datetime.now(timezone.utc).isoformat()}
        try:
            import psutil
            metrics["cpu_percent"] = psutil.cpu_percent(interval=None)
            metrics["memory_percent"] = psutil.virtual_memory().percent
        except ImportError:
            metrics["psutil"] = "unavailable"
        try:
            torch = require_torch()
            if torch.cuda.is_available():
                metrics["gpu_memory_allocated_bytes"] = int(torch.cuda.memory_allocated())
                metrics["gpu_memory_reserved_bytes"] = int(torch.cuda.memory_reserved())
        except RuntimeError:
            metrics["torch"] = "unavailable"
        return metrics

    def report(self) -> dict[str, Any] | None:
        with self._lock:
            return json.loads(json.dumps(self._state.report)) if self._state.report is not None else None

    def save_report(self, path: str | Path) -> Path:
        """Write the last report as indented JSON and return its path."""
        report = self.report()
        if report is None:
            raise RuntimeError("no training report is available")
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return destination

    def wait(self, timeout: float | None = None) -> None:
        """Wait for the current worker, primarily useful to CLI and tests."""
        thread = self._thread
        if thread is not None:
            thread.join(timeout)

    def _run(self, dataset: DatasetBundle, config: TrainingConfig) -> None:
        started = time.time()
        report: dict[str, Any] = {
            "dataset": dataset.metadata,
            "configuration": config.to_dict(),
            "epoch_history": [],
            "started_at": datetime.now(timezone.utc).isoformat(),
            "system_metrics": [],
        }
        try:
            torch = require_torch()
            np = require_numpy()
            device = self._device(torch, config.device)
            model = build_cnn(config.cnn, int(dataset.samples.shape[2])).to(device)
            report["device"] = str(device)
            report["parameter_count"] = model.parameter_count
            x = torch.from_numpy(np.asarray(dataset.samples)).float()
            y = torch.from_numpy(np.asarray(dataset.labels)).long()
            optimizer = self._optimizer(torch, config.optimizer, model, config.learning_rate)
            loss_fn = torch.nn.CrossEntropyLoss()
            train_indices, validation_indices, test_indices = self._split_indices(len(y), int(dataset.metadata.get("seed", 0)))
            train_loader = torch.utils.data.DataLoader(torch.utils.data.Subset(torch.utils.data.TensorDataset(x, y), train_indices), batch_size=config.batch_size, shuffle=False)
            with self._lock:
                self._state.status = "running"
            for epoch in range(1, config.epochs + 1):
                if self._cancel.is_set():
                    report["stop_reason"] = "cancelled before epoch"
                    break
                model.train()
                total_loss = correct = seen = 0
                for batch_index, (batch_x, batch_y) in enumerate(train_loader, 1):
                    if self._cancel.is_set():
                        report["stop_reason"] = "cancelled between batches"
                        break
                    batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                    optimizer.zero_grad()
                    output = model(batch_x)
                    loss = loss_fn(output, batch_y)
                    loss.backward()
                    optimizer.step()
                    total_loss += loss.item() * len(batch_y)
                    correct += int((output.argmax(1) == batch_y).sum().item())
                    seen += len(batch_y)
                    with self._lock:
                        self._state.epoch, self._state.batch = epoch, batch_index
                report["epoch_history"].append({"epoch": epoch, "loss": total_loss / max(seen, 1), "accuracy": correct / max(seen, 1), "validation": self._evaluate(model, x, y, validation_indices, loss_fn, device)})
                report["system_metrics"].append(self._metrics(torch, device))
                if report.get("stop_reason"):
                    break
                self._save_checkpoint(model, optimizer, epoch, config)
            final_epoch = report["epoch_history"][-1] if report["epoch_history"] else {}
            report["final_metrics"] = {"train": {"loss": final_epoch.get("loss"), "accuracy": final_epoch.get("accuracy")}, "validation": final_epoch.get("validation", {}), "test": self._evaluate(model, x, y, test_indices, loss_fn, device)}
            report.setdefault("stop_reason", "completed")
            with self._lock:
                self._state.status = "cancelled" if report["stop_reason"].startswith("cancelled") else "completed"
        except Exception as exc:  # Preserve a structured report for callers.
            report["stop_reason"] = "failed"
            report["error"] = f"{type(exc).__name__}: {exc}"
            report.setdefault("final_metrics", {})
            with self._lock:
                self._state.status = "failed"
                self._state.message = report["error"]
        report["duration_seconds"] = round(time.time() - started, 6)
        report["finished_at"] = datetime.now(timezone.utc).isoformat()
        with self._lock:
            self._state.report = report

    def _run_loader(self, loader: SigMFLoader, config: TrainingConfig) -> None:
        try:
            dataset = loader.load()
        except Exception as exc:
            self._failure_report(config, loader.config.path, exc)
            return
        self._run(dataset, config)

    def _failure_report(self, config: TrainingConfig, dataset_path: str, exc: Exception) -> None:
        report = {"dataset": {"dataset_path": dataset_path}, "configuration": config.to_dict(), "epoch_history": [], "final_metrics": {}, "stop_reason": "failed", "error": f"{type(exc).__name__}: {exc}", "finished_at": datetime.now(timezone.utc).isoformat()}
        with self._lock:
            self._state.status = "failed"
            self._state.message = report["error"]
            self._state.report = report

    @staticmethod
    def _optimizer(torch: Any, name: str, model: Any, learning_rate: float) -> Any:
        optimizers = {"adam": torch.optim.Adam, "sgd": torch.optim.SGD, "rmsprop": torch.optim.RMSprop}
        try:
            options = {"lr": learning_rate}
            if name == "sgd":
                options["momentum"] = 0.9
            return optimizers[name](model.parameters(), **options)
        except KeyError as exc:
            raise ValueError(f"unsupported optimizer: {name}") from exc

    @staticmethod
    def _split_indices(size: int, seed: int) -> tuple[list[int], list[int], list[int]]:
        indices = list(range(size))
        # The parameter limit is stable and avoids another configuration dependency.
        import random
        random.Random(seed).shuffle(indices)
        train_end = max(1, int(size * 0.6))
        validation_end = max(train_end + 1, int(size * 0.8)) if size > 1 else train_end
        return indices[:train_end], indices[train_end:validation_end], indices[validation_end:]

    @staticmethod
    def _evaluate(model: Any, x: Any, y: Any, indices: list[int], loss_fn: Any, device: Any) -> dict[str, Any]:
        if not indices:
            return {"loss": None, "accuracy": None, "samples": 0}
        model.eval()
        with __import__("torch").no_grad():
            output = model(x[indices].to(device))
            labels = y[indices].to(device)
            return {"loss": float(loss_fn(output, labels).item()), "accuracy": float((output.argmax(1) == labels).float().mean().item()), "samples": len(indices)}

    @staticmethod
    def _device(torch: Any, requested: str) -> Any:
        if requested == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("CUDA was requested but is unavailable")
        return torch.device("cuda" if requested == "cuda" or (requested == "auto" and torch.cuda.is_available()) else "cpu")

    @staticmethod
    def _save_checkpoint(model: Any, optimizer: Any, epoch: int, config: TrainingConfig) -> None:
        directory = Path(config.checkpoint_dir)
        directory.mkdir(parents=True, exist_ok=True)
        torch = require_torch()
        torch.save({"epoch": epoch, "model": model.state_dict(), "optimizer": optimizer.state_dict()}, directory / f"epoch-{epoch:03d}.pt")

    @staticmethod
    def _metrics(torch: Any, device: Any) -> dict[str, Any]:
        metrics: dict[str, Any] = {"timestamp": datetime.now(timezone.utc).isoformat(), "device": str(device)}
        try:
            import psutil

            metrics["cpu_percent"] = psutil.cpu_percent(interval=None)
            metrics["memory_percent"] = psutil.virtual_memory().percent
        except ImportError:
            metrics["psutil"] = "unavailable"
        if str(device).startswith("cuda") and torch.cuda.is_available():
            metrics["gpu_memory_allocated_bytes"] = torch.cuda.memory_allocated(device)
            metrics["gpu_memory_reserved_bytes"] = torch.cuda.memory_reserved(device)
        return metrics
