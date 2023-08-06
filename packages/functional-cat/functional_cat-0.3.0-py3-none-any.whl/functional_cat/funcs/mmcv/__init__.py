try:
    import mmcv  # noqa: F401
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "`MMCV` is not installed. Please see the instructions here: "
        "https://github.com/open-mmlab/mmcv#installation for installing for your specific environment."
    )

from .mmocr import MMOCRTextDetector

__all__ = ["MMOCRTextDetector"]
