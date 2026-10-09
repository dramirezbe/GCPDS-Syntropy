"""SigMF ci8_le loading and deterministic FM/noise window construction."""

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from ._optional import require_numpy
from .config import DatasetConfig


@dataclass
class DatasetBundle:
    """A model-ready dataset and provenance describing how it was built."""

    samples: Any
    labels: Any
    metadata: dict[str, Any]


class SigMFLoader:
    """Load SigMF captures and create balanced-ish binary FM/noise examples."""

    def __init__(self, config: DatasetConfig):
        config.validate()
        self.config = config

    def load(self) -> DatasetBundle:
        np = require_numpy()
        root = Path(self.config.path).expanduser()
        if not root.exists():
            raise FileNotFoundError(f"SigMF dataset path does not exist: {root}")
        metadata_files = sorted(root.glob("*.sigmf-meta"))
        if root.is_file() and root.name.endswith(".sigmf-meta"):
            metadata_files = [root]
        if not metadata_files:
            raise FileNotFoundError(f"No *.sigmf-meta files found under {root}")

        fm_windows: list[Any] = []
        captures: list[dict[str, Any]] = []
        capture_limit = self.config.max_captures
        windows_truncated = False
        for metadata_path in metadata_files:
            with metadata_path.open(encoding="utf-8") as handle:
                meta = json.load(handle)
            datatype = meta.get("global", {}).get("datatype", "").lower()
            if datatype != "ci8_le":
                raise ValueError(f"{metadata_path.name} has unsupported datatype {datatype!r}; expected ci8_le")
            data_path = metadata_path.with_name(metadata_path.name.removesuffix("-meta") + "-data")
            if not data_path.exists():
                raise FileNotFoundError(f"Missing SigMF data file for {metadata_path.name}: {data_path.name}")
            # memmap avoids materializing the external multi-gigabyte capture.
            raw = np.memmap(data_path, dtype=np.int8, mode="r")
            if raw.size % 2:
                raise ValueError(f"Odd number of int8 values in {data_path.name}")
            iq = raw.reshape(-1, 2).astype(np.float32)
            capture_entries = meta.get("captures") or [{"sample_start": 0}]
            for index, capture in enumerate(capture_entries):
                if capture_limit is not None and len(captures) >= capture_limit:
                    windows_truncated = True
                    break
                if self.config.max_windows is not None and len(fm_windows) >= self.config.max_windows:
                    windows_truncated = True
                    break
                start = int(capture.get("sample_start", 0))
                end = int(capture_entries[index + 1].get("sample_start", iq.shape[0]) if index + 1 < len(capture_entries) else iq.shape[0])
                remaining = None if self.config.max_windows is None else self.config.max_windows - len(fm_windows)
                windows = self._window(iq[start:end], np, remaining)
                fm_windows.extend(windows)
                captures.append({
                    "file": metadata_path.name,
                    "capture_index": index,
                    "sample_start": start,
                    "sample_end": end,
                    "frequency": capture.get("frequency"),
                    "window_count": len(windows),
                })
            if windows_truncated:
                break

        if not fm_windows:
            raise ValueError("SigMF captures did not contain a complete window")
        fm = np.stack(fm_windows).astype(np.float32)
        count = int(round(len(fm) * self.config.noise_ratio))
        rng = np.random.default_rng(self.config.seed)
        noise = rng.standard_normal((count, 2, self.config.window_length), dtype=np.float32)
        noise = self._normalize(noise, np)
        samples = np.concatenate((fm, noise), axis=0).astype(np.float32)
        labels = np.concatenate((np.ones(len(fm), dtype=np.int64), np.zeros(count, dtype=np.int64)))
        metadata = {
            "dataset_path": str(root),
            "datatype": "ci8_le",
            "window_length": self.config.window_length,
            "stride": self.config.stride,
            "seed": self.config.seed,
            "label_strategy": "fm=1 from SigMF captures; noise=0 from seeded synthetic Gaussian IQ",
            "captures": captures,
            "fm_windows": len(fm),
            "noise_windows": count,
            "max_windows": self.config.max_windows,
            "max_captures": self.config.max_captures,
            "windows_truncated": windows_truncated,
        }
        return DatasetBundle(samples=samples, labels=labels, metadata=metadata)

    def _window(self, iq: Any, np: Any, limit: int | None = None) -> list[Any]:
        length = self.config.window_length
        windows: list[Any] = []
        for start in range(0, len(iq) - length + 1, self.config.stride):
            windows.append(self._normalize(np.asarray(iq[start : start + length].T)[None, ...], np)[0])
            if limit is not None and len(windows) >= limit:
                break
        return windows

    @staticmethod
    def _normalize(samples: Any, np: Any) -> Any:
        power = np.sqrt(np.mean(np.square(samples), axis=(1, 2), keepdims=True))
        return (samples / np.maximum(power, np.float32(1e-12))).astype(np.float32)
