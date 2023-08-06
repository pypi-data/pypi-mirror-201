from abc import ABC, abstractmethod
from enum import Enum
from typing import List

from PIL import Image

from functional_cat.data_types import (
    Detection,
    DetectionWithKeypoints,
    ImageInput,
    InstanceSegmentation,
)

__all__ = ["ObjectDetector", "InstanceSegmentationModel", "KeyPointDetector"]

colors = [
    "#e6194b",
    "#3cb44b",
    "#ffe119",
    "#4363d8",
    "#f58231",
    "#911eb4",
    "#46f0f0",
    "#f032e6",
    "#bcf60c",
    "#fabebe",
    "#008080",
    "#e6beff",
    "#9a6324",
    "#fffac8",
    "#800000",
    "#aaffc3",
    "#808000",
    "#ffd8b1",
    "#000075",
    "#808080",
    "#ffffff",
    "#000000",
]


class Task(Enum):
    OBJECT_DETECTION = "Object Detection"
    INSTANCE_SEGMENTATION = "Instance Segmentation"
    KEYPOINT_DETECTION = "KeyPoint Detection"


class ObjectDetector(ABC):
    """Base class for object detectors. These objects are all callable and take in
    a list of `PIL.Image` objects and output a list of bounding box detections.
    """

    task = Task.OBJECT_DETECTION

    @property
    @abstractmethod
    def class_labels(self) -> List[str]:
        pass

    @abstractmethod
    def __call__(
        self, imgs: ImageInput, score_thres: float
    ) -> List[List[Detection]]:
        pass

    @staticmethod
    def draw_output_on_img(
        img: Image.Image, dets: List[Detection], **kwargs
    ) -> Image.Image:
        for i, det in enumerate(dets):
            img = det.draw_on_image(img, inplace=i != 0, **kwargs)
        return img


class InstanceSegmentationModel(ObjectDetector):
    task = Task.INSTANCE_SEGMENTATION

    @abstractmethod
    def __call__(self, imgs: ImageInput) -> List[List[InstanceSegmentation]]:
        pass

    @staticmethod
    def draw_output_on_img(
        img: Image.Image, dets: List[InstanceSegmentation]
    ) -> Image.Image:
        for i, det in enumerate(dets):
            img = det.draw_on_image(
                img, inplace=i != 0, draw_mask=True, draw_bbox=False
            )
        for i, det in enumerate(dets):
            img = det.draw_on_image(
                img, inplace=i != 0, draw_mask=False, draw_bbox=True
            )

        return img


class KeyPointDetector(ObjectDetector):
    task = Task.KEYPOINT_DETECTION

    @abstractmethod
    def __call__(self, imgs: ImageInput) -> List[List[DetectionWithKeypoints]]:
        pass

    @property
    @abstractmethod
    def key_point_labels(self) -> List[str]:
        pass

    def draw_output_on_img(
        self, img: Image.Image, dets: List[DetectionWithKeypoints]
    ) -> Image.Image:
        color_map = {k: colors[i] for i, k in enumerate(self.key_point_labels)}
        return super().draw_output_on_img(img, dets, color_map=color_map)
