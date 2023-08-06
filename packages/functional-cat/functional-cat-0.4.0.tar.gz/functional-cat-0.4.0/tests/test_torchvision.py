import pytest
from PIL import Image

from functional_cat.funcs.torchvision import TorchvisionDetector


@pytest.fixture
def model():
    return TorchvisionDetector(
        model_name="fasterrcnn_mobilenet_v3_large_320_fpn"
    )


@pytest.fixture
def img1():
    return Image.open("sample_imgs/cat.jpg")


@pytest.fixture
def img2():
    return Image.open("sample_imgs/gang.jpg").convert("RGB")


def test_batch_processing(
    model: TorchvisionDetector,
    img1: Image,
    img2: Image,
    check_detection_batch_processing,  # defined in conftest.py
):

    check_detection_batch_processing(
        model=model, img1=img1, img2=img2, score_thres=0.5
    )
