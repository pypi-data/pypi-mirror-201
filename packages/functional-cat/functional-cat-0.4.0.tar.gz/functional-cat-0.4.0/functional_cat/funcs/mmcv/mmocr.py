import os
from typing import List

try:
    from mmocr.apis import inference, init_detector
    from mmocr.datasets.pipelines import (  # necessary to register transforms # noqa: F401
        loading,
    )
    from mmocr.utils.model import revert_sync_batchnorm
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "`MMOCR` is not installed. Please see the instructions here: "
        " https://github.com/open-mmlab/mmocr#installation for installing for your specific environment."
    )
import numpy as np
import torch

from functional_cat.data_types import (
    BoundingPolygon,
    Detection,
    ImageInput,
    Point,
)
from functional_cat.interfaces import ObjectDetector


class MMOCRTextDetector(ObjectDetector):
    CLASS_LABEL = "text"

    MODEL_NAME_TO_CONFIG = {
        "PS_IC15": "configs/textdet/psenet/psenet_r50_fpnf_600e_icdar2015.py"
    }

    MODEL_NAME_TO_CKPT = {
        "PS_IC15": "https://download.openmmlab.com/mmocr/textdet/psenet/psenet_r50_fpnf_600e_icdar2015_pretrain-eefd8fe6.pth"
    }

    def _get_config_path(self, model_name: str) -> str:
        return os.path.join(
            os.path.dirname(__file__), self.MODEL_NAME_TO_CONFIG[model_name]
        )

    def _get_checkpoint(self, model_name: str) -> str:
        return self.MODEL_NAME_TO_CKPT[model_name]

    def __init__(self, model_name: str) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = revert_sync_batchnorm(
            init_detector(
                self._get_config_path(model_name),
                checkpoint=self._get_checkpoint(model_name),
                device=self.device,
            )
        )

    @property
    def class_labels(self) -> List[str]:
        return [self.CLASS_LABEL]

    def __call__(
        self, imgs: ImageInput, score_thres: float
    ) -> List[List[Detection]]:
        img_arrays = [np.array(img)[:, :, [2, 1, 0]] for img in imgs]
        out = inference.model_inference(
            self.model, img_arrays, batch_mode=True
        )
        return [
            self._postprocess_single_output(x, score_thres=score_thres)
            for x in out
        ]

    def mmcv_single_det_to_detection(self, det: List[float]) -> Detection:
        pts, score = det[:-1], det[-1]
        xs, ys = pts[::2], pts[1::2]
        boundary = BoundingPolygon(
            points=[Point(x=x, y=y) for x, y in zip(xs, ys)]
        )
        return Detection(
            boundary=boundary, class_label=self.CLASS_LABEL, score=score
        )

    def _postprocess_single_output(
        self, x, score_thres: float
    ) -> List[Detection]:
        dets = [
            self.mmcv_single_det_to_detection(det)
            for det in x["boundary_result"]
        ]
        return [d for d in dets if d.score > score_thres]
