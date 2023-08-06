try:
    import onnxruntime  # noqa: F401
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        f"`functional-cat` was not installed with onnx support so the module `{__name__}` cannot be used. "
        "Please run `pip install functional-cat[onnx-cpu]` or `pip install functional-cat[onnx-gpu]` to install."
    )

from .tiny_yolov3 import TinyYoloV3
from .yolov4 import YoloV4

__all__ = ["YoloV4", "TinyYoloV3"]
