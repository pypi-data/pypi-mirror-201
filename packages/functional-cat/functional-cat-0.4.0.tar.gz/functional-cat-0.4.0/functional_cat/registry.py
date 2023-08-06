from dataclasses import dataclass
from enum import Enum
from typing import Any, List

from PIL import Image

from functional_cat.interfaces import Task


class Framework(Enum):
    PYTORCH = "PyTorch"
    ONNX = "ONNX"
    MMCV = "MMCV"
    DLIB = "dlib"


@dataclass
class ModelMeta:
    name: str
    class_: type
    constructor_args: dict
    description: str
    framework: Framework
    install_snippet: str
    gpu_support: bool
    cpu_support: bool
    colab_link: str = None
    example_img: Image.Image = None

    @property
    def task(self) -> Task:
        return self.class_.task

    def load_model(self) -> Any:
        return self.class_(**self.constructor_args)


def create_torchvision_model_metas(
    detection_example_img: Image.Image = None,
    keypoint_example_img: Image.Image = None,
) -> List[ModelMeta]:
    from functional_cat.funcs.torchvision import (
        TorchvisionDetector,
        TorchvisionInstanceSegmentation,
        TorchvisionKeyPointDetector,
    )

    example_img = {
        TorchvisionDetector: detection_example_img,
        TorchvisionInstanceSegmentation: detection_example_img,
        TorchvisionKeyPointDetector: keypoint_example_img,
    }

    return [
        ModelMeta(
            name=name,
            class_=class_,
            constructor_args={"model_name": name},
            description=f"{name} model from torchvision. See https://pytorch.org/vision/stable/models.html",
            framework=Framework.PYTORCH,
            install_snippet="pip install functional-cat[torch]",
            gpu_support=True,
            cpu_support=True,
            example_img=example_img[class_],
            colab_link="https://colab.research.google.com/drive/1QxpsKWEM6y-ULuBL2g4xBvosl4lSowfg",
        )
        for class_, name in [
            (TorchvisionDetector, "fasterrcnn_resnet50_fpn"),
            (TorchvisionDetector, "fasterrcnn_resnet50_fpn_v2"),
            (TorchvisionDetector, "fasterrcnn_mobilenet_v3_large_fpn"),
            (TorchvisionDetector, "fasterrcnn_mobilenet_v3_large_320_fpn"),
            (TorchvisionDetector, "fcos_resnet50_fpn"),
            (TorchvisionDetector, "retinanet_resnet50_fpn"),
            (TorchvisionDetector, "ssd300_vgg16"),
            (TorchvisionDetector, "ssdlite320_mobilenet_v3_large"),
            (TorchvisionInstanceSegmentation, "maskrcnn_resnet50_fpn_v2"),
            (TorchvisionKeyPointDetector, "keypointrcnn_resnet50_fpn"),
        ]
    ]


def create_onnx_model_metas(
    example_img: Image.Image = None,
) -> List[ModelMeta]:
    from functional_cat.funcs.onnx import TinyYoloV3, YoloV4

    onnx_install_snippet = (
        'pip install "functional-cat[onnx]" # or [onnx-gpu] for GPU support.'
    )

    return [
        ModelMeta(
            name="yolov4",
            class_=YoloV4,
            constructor_args={},
            description="YoloV4 from the ONNX model zoo. See https://github.com/onnx/models/tree/main/vision/object_detection_segmentation/yolov4",
            framework=Framework.ONNX,
            install_snippet=onnx_install_snippet,
            cpu_support=True,
            gpu_support=True,
            example_img=example_img,
            colab_link="https://colab.research.google.com/drive/1zolH3JooXbAKVPXLGJ6LcDLOFjf-MYYH",
        ),
        ModelMeta(
            name="tiny-yolov3",
            class_=TinyYoloV3,
            constructor_args={},
            description="Tiny YoloV3  from the ONNX model zoo. See https://github.com/onnx/models/tree/main/vision/object_detection_segmentation/yolov4",
            framework=Framework.ONNX,
            install_snippet=onnx_install_snippet,
            cpu_support=True,
            gpu_support=True,
            example_img=example_img,
            colab_link="https://colab.research.google.com/drive/1zolH3JooXbAKVPXLGJ6LcDLOFjf-MYYH",
        ),
    ]


def create_mmcv_model_metas(
    example_img: Image.Image = None,
) -> List[ModelMeta]:
    mmocr_install_snippet = (
        "# Please see https://mmocr.readthedocs.io/en/latest/install.html for installing MMOCR.\n"
        "# Then run:\n"
        "pip install functional-cat"
    )
    from functional_cat.funcs.mmcv import MMOCRTextDetector

    return [
        ModelMeta(
            name="ps_ic15",
            class_=MMOCRTextDetector,
            constructor_args={"model_name": "PS_IC15"},
            description="PS_IC15 text detector from MMOCR. See https://mmocr.readthedocs.io/en/stable/textdet_models.html",
            framework=Framework.MMCV,
            install_snippet=mmocr_install_snippet,
            cpu_support=True,
            gpu_support=True,
            example_img=example_img,
            colab_link="https://colab.research.google.com/drive/1k7L7pJCPgltSwLf6N-cW2KvCF5pprU3W",
        )
    ]


def create_glip_model_metas(
    example_img: Image.Image = None,
) -> List[ModelMeta]:
    description = (
        "GLIP is a zero-shot object detector: it can run object detection on arbitrary"
        ' class labels, which here get passed in model instantiation. GLIP-T is the "tiny" version'
        " and GLIP-L is the larger version."
    )

    glip_install_snippet = 'pip install "functional-cat[glip]"'
    try:
        from functional_cat.funcs.glip import GLIP
    except ModuleNotFoundError:
        GLIP = None

    return [
        ModelMeta(
            name=name,
            class_=GLIP,
            constructor_args={
                "model_name": name,
                "class_labels": ["cat", "person", "bike", "bottle"],
            },
            description=description,
            framework=Framework.PYTORCH,
            install_snippet=glip_install_snippet,
            cpu_support=False,
            gpu_support=True,
            example_img=example_img,
            colab_link="https://colab.research.google.com/drive/1GKMq4Z-7tD3cNWubWCqMuQ81D-nAFIaD",
        )
        for name in ["GLIP-T", "GLIP-L"]
    ]


def create_dlib_model_metas(
    example_img: Image.Image = None,
) -> List[ModelMeta]:
    from functional_cat.funcs.dlib import DLibFaceDetector

    return [
        ModelMeta(
            name="cnn_face_detection_model_v1",
            class_=DLibFaceDetector,
            constructor_args={},
            description="cnn_face_detection_model_v1 from dlib",
            framework=Framework.DLIB,
            install_snippet="pip install functional-cat[dlib]",
            cpu_support=True,
            gpu_support=True,
            example_img=example_img,
        )
    ]
