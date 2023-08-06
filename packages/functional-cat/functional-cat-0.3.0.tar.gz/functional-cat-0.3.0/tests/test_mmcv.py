import pytest
from PIL import Image

from functional_cat.funcs.mmcv import MMOCRTextDetector


@pytest.fixture
def model():
    return MMOCRTextDetector(model_name="PS_IC15")


@pytest.fixture
def img1():
    return Image.open("sample_imgs/street_sign.jpg")


@pytest.fixture
def img2():
    return Image.open("sample_imgs/letter_box.jpg").convert("RGB")


def test_batch_processing(
    model: MMOCRTextDetector,
    img1: Image,
    img2: Image,
    check_detection_batch_processing,  # defined in conftest.py
):

    check_detection_batch_processing(
        model=model, img1=img1, img2=img2, score_thres=0.5
    )
