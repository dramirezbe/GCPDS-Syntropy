"""Configurable 1-D CNN with a parameter-count guard."""

from ._optional import require_torch
from .config import CNNConfig


def build_cnn(config: CNNConfig, window_length: int):
    torch = require_torch()
    config.validate()
    if window_length <= 0:
        raise ValueError("window_length must be positive")
    layers = []
    in_channels = 2
    for out_channels in config.channels:
        layers.extend([
            torch.nn.Conv1d(in_channels, out_channels, config.kernel_size, padding=config.kernel_size // 2),
            _activation(torch, config.activation),
            torch.nn.MaxPool1d(2),
        ])
        in_channels = out_channels
    layers.append(torch.nn.AdaptiveAvgPool1d(1))
    features = torch.nn.Sequential(*layers)
    model = torch.nn.Sequential(features, torch.nn.Flatten(), torch.nn.Dropout(config.dropout), torch.nn.Linear(in_channels, 2))
    parameters = sum(parameter.numel() for parameter in model.parameters())
    if parameters > config.max_parameters:
        raise ValueError(f"CNN has {parameters} parameters; limit is {config.max_parameters}")
    model.parameter_count = parameters
    return model


def _activation(torch, name: str):
    activations = {
        "relu": torch.nn.ReLU,
        "gelu": torch.nn.GELU,
        "sigmoid": torch.nn.Sigmoid,
        "tanh": torch.nn.Tanh,
    }
    try:
        return activations[name]()
    except KeyError as exc:
        raise ValueError(f"unsupported activation: {name}") from exc
