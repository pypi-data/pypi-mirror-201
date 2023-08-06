try:
    import torch  # noqa: F401
    import torchvision  # noqa: F401
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        f"`functional-cat` was not installed with PyTorch support so the module `{__name__}` cannot be used. "
        "Please run `pip install functional-cat[torch]` to install."
    )

from .detection import (
    TorchvisionDetector,
    TorchvisionInstanceSegmentation,
    TorchvisionKeyPointDetector,
)

__all__ = [
    "TorchvisionDetector",
    "TorchvisionInstanceSegmentation",
    "TorchvisionKeyPointDetector",
]
