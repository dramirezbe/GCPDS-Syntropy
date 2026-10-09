"""Small helpers keeping optional ML imports out of module import time."""


def require_numpy():
    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError(
            "M1 training requires numpy. Install the project's ML dependencies "
            "before loading SigMF captures."
        ) from exc
    return np


def require_torch():
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError(
            "M1 training requires torch. Install a CPU or CUDA PyTorch build "
            "before starting a training run."
        ) from exc
    return torch
