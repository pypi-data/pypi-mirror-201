from typing import List

import torch
from torchvision.models import detection
from torchvision.transforms import ToTensor

from functional_cat.data_types import (
    BoundingPolygon,
    Detection,
    DetectionWithKeypoints,
    ImageInput,
    InstanceSegmentation,
    Keypoint,
)
from functional_cat.interfaces import (
    InstanceSegmentationModel,
    KeyPointDetector,
    ObjectDetector,
)

COCO_INSTANCE_CATEGORY_NAMES = [
    "__background__",
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "N/A",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "N/A",
    "backpack",
    "umbrella",
    "N/A",
    "N/A",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "N/A",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "N/A",
    "dining table",
    "N/A",
    "N/A",
    "toilet",
    "N/A",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "N/A",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]

COCO_PERSON_KEYPOINT_NAMES = [
    "nose",
    "left_eye",
    "right_eye",
    "left_ear",
    "right_ear",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
]

MODEL_NAME_TO_WEIGHTS = {
    "fasterrcnn_resnet50_fpn": detection.FasterRCNN_ResNet50_FPN_Weights.COCO_V1,
    "fasterrcnn_resnet50_fpn_v2": detection.FasterRCNN_ResNet50_FPN_V2_Weights.COCO_V1,
    "fasterrcnn_mobilenet_v3_large_fpn": detection.FasterRCNN_MobileNet_V3_Large_FPN_Weights.COCO_V1,
    "fasterrcnn_mobilenet_v3_large_320_fpn": detection.FasterRCNN_MobileNet_V3_Large_320_FPN_Weights.COCO_V1,
    "fcos_resnet50_fpn": detection.FCOS_ResNet50_FPN_Weights.COCO_V1,
    "maskrcnn_resnet50_fpn_v2": detection.MaskRCNN_ResNet50_FPN_V2_Weights.COCO_V1,
    "retinanet_resnet50_fpn": detection.RetinaNet_ResNet50_FPN_Weights.COCO_V1,
    "ssd300_vgg16": detection.SSD300_VGG16_Weights.COCO_V1,
    "ssdlite320_mobilenet_v3_large": detection.SSDLite320_MobileNet_V3_Large_Weights.COCO_V1,
    "keypointrcnn_resnet50_fpn": detection.KeypointRCNN_ResNet50_FPN_Weights.COCO_V1,
}


def torch_box_to_boundary(box: torch.Tensor) -> BoundingPolygon:
    return BoundingPolygon.from_bbox(*box.cpu().tolist())


class TorchvisionDetector(ObjectDetector):
    def __init__(self, model_name: str):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if model_name not in MODEL_NAME_TO_WEIGHTS:
            raise ValueError(
                f"Got invalid `model_name`: {model_name}. Available "
                f"models are {list(MODEL_NAME_TO_WEIGHTS.keys())}"
            )
        self.model = (
            getattr(detection, model_name)(
                weights=MODEL_NAME_TO_WEIGHTS[model_name]
            )
            .eval()
            .to(self.device)
        )

    def _preprocess(self, imgs: ImageInput):
        to_tensor = ToTensor()
        return [to_tensor(img).to(self.device) for img in imgs]

    @staticmethod
    def _postprocess_single_output(x, score_thres):
        return [
            Detection(
                boundary=torch_box_to_boundary(box),
                score=score.item(),
                class_label=COCO_INSTANCE_CATEGORY_NAMES[label],
            )
            for box, score, label in zip(x["boxes"], x["scores"], x["labels"])
            if score > score_thres
        ]

    @property
    def class_labels(self) -> List[str]:
        return [
            s
            for s in COCO_INSTANCE_CATEGORY_NAMES
            if s not in ["__background__", "N/A"]
        ]

    def __call__(
        self, imgs: ImageInput, score_thres: float
    ) -> List[List[Detection]]:
        with torch.no_grad():
            torch_output = self.model(self._preprocess(imgs))
        return [
            self._postprocess_single_output(out, score_thres=score_thres)
            for out in torch_output
        ]


class TorchvisionKeyPointDetector(TorchvisionDetector, KeyPointDetector):
    @property
    def class_labels(self) -> List[str]:
        return ["person"]

    @property
    def key_point_labels(self) -> List[str]:
        return COCO_PERSON_KEYPOINT_NAMES

    def _postprocess_single_output(
        self, x, score_thres
    ) -> List[DetectionWithKeypoints]:
        return [
            DetectionWithKeypoints(
                boundary=torch_box_to_boundary(box),
                score=score,
                class_label=COCO_INSTANCE_CATEGORY_NAMES[label],
                keypoints=[
                    Keypoint(
                        class_label=COCO_PERSON_KEYPOINT_NAMES[i],
                        x=k[0].item(),
                        y=k[1].item(),
                        visible=k[2].item() == 1,
                        score=ks.item(),
                    )
                    for i, (k, ks) in enumerate(
                        zip(key_points, keypoints_scores)
                    )
                ],
            )
            for box, score, label, key_points, keypoints_scores in zip(
                x["boxes"],
                x["scores"],
                x["labels"],
                x["keypoints"],
                x["keypoints_scores"],
            )
            if score > score_thres
        ]


class TorchvisionInstanceSegmentation(
    TorchvisionDetector, InstanceSegmentationModel
):
    def _postprocess_single_output(self, x, score_thres):
        return [
            InstanceSegmentation(
                boundary=torch_box_to_boundary(box),
                score=score,
                class_label=COCO_INSTANCE_CATEGORY_NAMES[label],
                mask=mask[0].cpu().numpy().tolist(),
            )
            for box, score, label, mask in zip(
                x["boxes"], x["scores"], x["labels"], x["masks"]
            )
            if score > score_thres
        ]
