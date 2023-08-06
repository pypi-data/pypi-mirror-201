import bz2
import tempfile
from typing import Any, List

import numpy as np
from dlib import (
    cnn_face_detection_model_v1,
    full_object_detection,
    mmod_rectangle,
    rectangle,
    shape_predictor,
)

from functional_cat.data_types import (
    BoundingPolygon,
    Detection,
    DetectionWithKeypoints,
    ImageInput,
    Keypoint,
)
from functional_cat.interfaces import KeyPointDetector
from functional_cat.io import FileFromURL, download_to_cache


def _convert_rectangle(rect: rectangle) -> BoundingPolygon:
    return BoundingPolygon.from_bbox(
        xmin=rect.left(),
        ymin=rect.top(),
        xmax=rect.right(),
        ymax=rect.bottom(),
    )


def _load_dlib_model(constructor: callable, file: FileFromURL) -> Any:
    model_bz_path = download_to_cache(file)
    with bz2.open(
        model_bz_path, "rb"
    ) as f, tempfile.NamedTemporaryFile() as tmp_file:
        model_data = f.read()
        tmp_file.write(model_data)
        tmp_file.seek(0)

        return constructor(tmp_file.name)


class DLibFaceDetector(KeyPointDetector):
    DETECTOR_FILE = FileFromURL(
        url="https://raw.githubusercontent.com/davisking/dlib-models/master/mmod_human_face_detector.dat.bz2",
        md5="5edccec8ac713d743be4865ff6ead7f7",
    )

    SHAPE_PREDICTOR_FILE = FileFromURL(
        url="https://raw.githubusercontent.com/davisking/dlib-models/master/shape_predictor_5_face_landmarks.dat.bz2",
        md5="ef591cf713630226b35b11d0e1733118",
    )

    CLASS_LABEL = "face"

    def __init__(self):
        self.model = _load_dlib_model(
            cnn_face_detection_model_v1, self.DETECTOR_FILE
        )
        self.sp = _load_dlib_model(shape_predictor, self.SHAPE_PREDICTOR_FILE)

    def __call__(
        self,
        imgs: ImageInput,
        score_thres: float,
        upsample_factor: int = 1,
    ) -> List[List[Detection]]:
        """
        Parameters
        ----------
        imgs
            list of images
        score_thres
            the confidence threshold to determine a detection
        upsample_factor
            will upsample the image by this factor before running detection.
            this can help find more faces but will also cause a longer runtime
        """
        img_arrays = [np.array(img) for img in imgs]
        dlib_out = self.model(img_arrays, upsample_factor)

        filtered_dlib_out = [
            [det for det in dets if det.confidence >= score_thres]
            for dets in dlib_out
        ]
        sp_preds = [
            [self.sp(img_array, det.rect) for det in dets]
            for dets, img_array in zip(filtered_dlib_out, img_arrays)
        ]

        return [
            [
                self._get_detection_with_keypoint(det, sp_out)
                for det, sp_out in zip(dets, sp_outs)
            ]
            for dets, sp_outs in zip(filtered_dlib_out, sp_preds)
        ]

    def _get_detection_with_keypoint(
        self, det: mmod_rectangle, sp_out: full_object_detection
    ) -> DetectionWithKeypoints:

        keypoints = [
            Keypoint(class_label=self.key_point_labels[i], x=p.x, y=p.y)
            for i, p in enumerate(sp_out.parts())
        ]

        return DetectionWithKeypoints(
            boundary=_convert_rectangle(det.rect),
            class_label=self.CLASS_LABEL,
            score=det.confidence,
            keypoints=keypoints,
        )

    @property
    def class_labels(self) -> List[str]:
        return [self.CLASS_LABEL]

    @property
    def key_point_labels(self) -> List[str]:
        return [
            "left_eye_outer_corner",
            "left_eye_inner_corner",
            "right_eye_outer_corner",
            "right_eye_inner_corner",
            "nose",
        ]
