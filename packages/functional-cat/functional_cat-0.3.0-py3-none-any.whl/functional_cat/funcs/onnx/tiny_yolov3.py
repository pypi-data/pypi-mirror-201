""" tiny yolov3 from https://github.com/onnx/models/tree/main/vision/object_detection_segmentation/tiny-yolov3
"""
from typing import List, Tuple

import numpy as np
import onnxruntime as ort
from PIL import Image

from functional_cat.data_types import BoundingPolygon, Detection, ImageInput
from functional_cat.interfaces import ObjectDetector
from functional_cat.io import FileFromGithubLFS, download_to_cache


# this function is from yolo3.utils.letterbox_image
def letterbox_image(image: Image.Image, size: Tuple[int, int]):
    """resize image with unchanged aspect ratio using padding"""
    iw, ih = image.size
    w, h = size
    scale = min(w / iw, h / ih)
    nw = int(iw * scale)
    nh = int(ih * scale)

    image = image.resize((nw, nh), Image.Resampling.BICUBIC)
    new_image = Image.new("RGB", size, (128, 128, 128))
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))
    return new_image


def preprocess(img: Image.Image) -> np.ndarray:
    model_image_size = (416, 416)
    boxed_image = letterbox_image(img, tuple(reversed(model_image_size)))
    image_data = np.array(boxed_image, dtype="float32")
    image_data /= 255.0
    image_data = np.transpose(image_data, [2, 0, 1])
    image_data = np.expand_dims(image_data, 0)
    return image_data


class TinyYoloV3(ObjectDetector):
    FILE = FileFromGithubLFS(
        organisation="onnx",
        repo="models",
        path="vision/object_detection_segmentation/tiny-yolov3/model/tiny-yolov3-11.onnx",
        md5="af6ede7ccab07676b97a487ffe43dcc7",
    )

    @property
    def class_labels(self):
        return [
            "person",
            "bicycle",
            "car",
            "motorbike",
            "aeroplane",
            "bus",
            "train",
            "truck",
            "boat",
            "traffic light",
            "fire hydrant",
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
            "backpack",
            "umbrella",
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
            "sofa",
            "pottedplant",
            "bed",
            "diningtable",
            "toilet",
            "tvmonitor",
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
            "book",
            "clock",
            "vase",
            "scissors",
            "teddy bear",
            "hair drier",
            "toothbrush",
        ]

    def __init__(self):
        model_path = download_to_cache(self.FILE)
        self.ort_sess = ort.InferenceSession(model_path)

    def __call__(
        self, imgs: ImageInput, score_thres: float
    ) -> List[List[Detection]]:
        img_arrays = [preprocess(img) for img in imgs]
        img_shapes = [
            np.array([img.size[1], img.size[0]], dtype=np.float32).reshape(
                1, 2
            )
            for img in imgs
        ]

        outputs = [
            self.ort_sess.run(
                None, {"input_1": img_array, "image_shape": img_shape}
            )
            for img_array, img_shape in zip(img_arrays, img_shapes)
        ]

        return [
            self._process_single_output(output, score_thres)
            for output in outputs
        ]

    def _process_single_output(
        self, output: List[np.ndarray], score_thres: float
    ) -> List[Detection]:
        boxes, scores, indices = output
        ret = []
        for idx_ in indices[0]:
            score = scores[tuple(idx_)]
            if score < score_thres:
                continue
            idx_1 = (idx_[0], idx_[2])
            bbox = boxes[idx_1]
            ret.append(
                Detection(
                    boundary=BoundingPolygon.from_bbox(
                        xmin=bbox[1], ymin=bbox[0], xmax=bbox[3], ymax=bbox[2]
                    ),
                    class_label=self.class_labels[idx_[1]],
                    score=score,
                )
            )
        return ret
