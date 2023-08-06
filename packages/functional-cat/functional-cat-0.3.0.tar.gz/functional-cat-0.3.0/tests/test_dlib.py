import pytest
from PIL import Image

from functional_cat.funcs.dlib import DLibFaceDetector


@pytest.fixture
def model():
    return DLibFaceDetector()


@pytest.fixture
def img1():
    return Image.open("sample_imgs/mona_lisa.jpeg")


@pytest.fixture
def img2():
    return Image.open("sample_imgs/gang.jpg").convert("RGB")


def test_batch_processing_neg(
    model: DLibFaceDetector,
    img1: Image,
    img2: Image,
):
    with pytest.raises(RuntimeError) as excinfo:
        model([img1, img2], score_thres=0.5)

    assert "must all have the same dimensions" in str(excinfo.value)


def test_batch_processing_po(
    model: DLibFaceDetector,
    img1: Image,
    img2: Image,
    check_detection_batch_processing,  # defined in conftest.py
):
    img1 = img1.resize((128, 128))
    img2 = img2.resize((128, 128))

    check_detection_batch_processing(
        model=model, img1=img1, img2=img2, score_thres=0.5
    )
