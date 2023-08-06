from typing import List

import torch
from glip.engine.predictor_glip import make_glip_l, make_glip_t
from glip.structures.bounding_box import BoxList

from functional_cat.data_types import BoundingPolygon, Detection
from functional_cat.interfaces import ImageInput, ObjectDetector
from functional_cat.io import FileFromURL, download_to_cache


class GLIP(ObjectDetector):
    MODEL_NAME_TO_WEIGHT = {
        "GLIP-T": FileFromURL(
            url="https://github.com/ekorman/GLIP/releases/download/v0.0.1-alpha/glip_tiny_model_o365_goldg_cc_sbu_model_only.pth",
            md5="b57fe1e9f194840c22337fbe77faa78b",
        ),
        "GLIP-L": FileFromURL(
            url="https://github.com/ekorman/GLIP/releases/download/v0.0.1-alpha/glip_large_model_model_only.pth",
            md5="2befd9660fe12bb69d02e1716bc9ac34",
        ),
    }

    def __init__(
        self,
        model_name: str,
        class_labels: List[str] = None,
        min_image_size: int = 800,
    ):
        if model_name not in self.MODEL_NAME_TO_WEIGHT.keys():
            raise ValueError(
                f"model_name must be one of {list(self.MODEL_NAME_TO_WEIGHT.keys())}"
            )

        weight_path = download_to_cache(self.MODEL_NAME_TO_WEIGHT[model_name])

        self.glip_model = (
            make_glip_l if model_name == "GLIP-L" else make_glip_t
        )(
            device=torch.device(
                "cuda" if torch.cuda.is_available() else "cpu"
            ),
            model_weight_path=weight_path,
            min_image_size=min_image_size,
        )

        self._class_labels = class_labels

    @property
    def class_labels(self) -> List[str]:
        return self._class_labels

    def __call__(
        self,
        imgs: ImageInput,
        score_thres: float,
        class_labels: List[str] = None,
    ) -> List[List[Detection]]:
        class_labels = class_labels or self.class_labels
        if class_labels is None:
            raise RuntimeError(
                "`class_labels` must be passed since they were not set when invoking the model."
            )
        box_lists = self.glip_model(
            imgs, class_labels=class_labels, thresh=score_thres
        )
        return [
            self._box_list_to_detections(box_list, class_labels)
            for box_list in box_lists
        ]

    @staticmethod
    def _box_list_to_detections(
        box_list: BoxList, class_labels: List[str]
    ) -> List[Detection]:
        bboxes = box_list.bbox.tolist()
        scores = box_list.get_field("scores")
        labels = box_list.get_field("labels")

        return [
            Detection(
                boundary=BoundingPolygon.from_bbox(*bbox),
                class_label=class_labels[label - 1],
                score=score.item(),
            )
            for bbox, score, label in zip(bboxes, scores, labels)
        ]
