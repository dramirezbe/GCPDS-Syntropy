"""Validated, JSON-friendly configuration for the training core."""

from dataclasses import asdict, dataclass, field
import os
from typing import Any


DEFAULT_DATASET_PATH = os.environ.get(
    "SYNTROPY_DATASET_PATH", "<set SYNTROPY_DATASET_PATH to the external SigMF database>"
)
MAX_PARAMETERS = 250_000
MAX_BATCH_SIZE = 256
MAX_EPOCHS = 20


@dataclass(frozen=True)
class DatasetConfig:
    path: str = DEFAULT_DATASET_PATH
    window_length: int = 1024
    stride: int = 1024
    noise_ratio: float = 1.0
    seed: int = 0
    max_windows: int | None = 2048
    max_captures: int | None = None

    def validate(self) -> None:
        if not self.path:
            raise ValueError("dataset path must not be empty")
        if self.window_length <= 0 or self.stride <= 0:
            raise ValueError("window_length and stride must be positive")
        if self.noise_ratio < 0:
            raise ValueError("noise_ratio must be non-negative")
        if self.max_windows is not None and self.max_windows <= 0:
            raise ValueError("max_windows must be positive or None for full data")
        if self.max_captures is not None and self.max_captures <= 0:
            raise ValueError("max_captures must be positive or None for all captures")


@dataclass(frozen=True)
class CNNConfig:
    channels: tuple[int, ...] = (8, 16)
    kernel_size: int = 5
    dropout: float = 0.1
    activation: str = "relu"
    max_parameters: int = MAX_PARAMETERS

    def validate(self) -> None:
        if not self.channels or any(channel <= 0 for channel in self.channels):
            raise ValueError("channels must contain positive values")
        if self.kernel_size < 1 or self.kernel_size % 2 == 0:
            raise ValueError("kernel_size must be a positive odd number")
        if not 0 <= self.dropout < 1:
            raise ValueError("dropout must be in [0, 1)")
        if self.activation not in {"relu", "gelu", "sigmoid", "tanh"}:
            raise ValueError("activation must be one of: relu, gelu, sigmoid, tanh")
        if self.max_parameters <= 0:
            raise ValueError("max_parameters must be positive")
        if self.max_parameters > MAX_PARAMETERS:
            raise ValueError(f"max_parameters cannot exceed {MAX_PARAMETERS}")


@dataclass(frozen=True)
class TrainingConfig:
    cnn: CNNConfig = field(default_factory=CNNConfig)
    epochs: int = 20
    batch_size: int = 32
    learning_rate: float = 1e-3
    checkpoint_dir: str = "checkpoints"
    device: str = "auto"
    optimizer: str = "adam"
    max_epochs: int = MAX_EPOCHS
    max_batch_size: int = MAX_BATCH_SIZE

    def validate(self) -> None:
        self.cnn.validate()
        if self.max_epochs != MAX_EPOCHS or self.max_batch_size != MAX_BATCH_SIZE:
            raise ValueError("training validation limits are fixed at 20 epochs and batch size 256")
        if not 1 <= self.epochs <= MAX_EPOCHS:
            raise ValueError(f"epochs must be between 1 and {MAX_EPOCHS}")
        if not 1 <= self.batch_size <= MAX_BATCH_SIZE:
            raise ValueError(f"batch_size must be between 1 and {MAX_BATCH_SIZE}")
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if self.device not in {"auto", "cpu", "cuda"}:
            raise ValueError("device must be auto, cpu, or cuda")
        if self.optimizer not in {"adam", "sgd", "rmsprop"}:
            raise ValueError("optimizer must be one of: adam, sgd, rmsprop")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
