import pytest
from PIL import Image

from functional_cat.funcs.onnx import TinyYoloV3, YoloV4


@pytest.fixture
def yolov4():
    return YoloV4()


@pytest.fixture
def tiny_yolov3():
    return TinyYoloV3()


@pytest.fixture
def img1():
    return Image.open("sample_imgs/cat.jpg")


@pytest.fixture
def img2():
    return Image.open("sample_imgs/gang.jpg").convert("RGB")


def test_yolov4_batch_processing(
    yolov4: YoloV4,
    img1: Image,
    img2: Image,
    check_detection_batch_processing,  # defined in conftest.py
):

    check_detection_batch_processing(
        model=yolov4, img1=img1, img2=img2, score_thres=0.5
    )


def test_tiny_yolov3_batch_processing(
    tiny_yolov3: TinyYoloV3,
    img1: Image,
    img2: Image,
    check_detection_batch_processing,  # defined in conftest.py
):

    check_detection_batch_processing(
        model=tiny_yolov3, img1=img1, img2=img2, score_thres=0.5
    )
