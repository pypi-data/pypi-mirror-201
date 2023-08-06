from typing import List, Tuple

import numpy as np
import onnxruntime as ort
from PIL import Image
from scipy import special

from functional_cat.data_types import BoundingPolygon, Detection, ImageInput
from functional_cat.interfaces import ObjectDetector
from functional_cat.io import FileFromGithubLFS, download_to_cache

ANCHORS = np.array(
    [
        [[12.0, 16.0], [19.0, 36.0], [40.0, 28.0]],
        [[36.0, 75.0], [76.0, 55.0], [72.0, 146.0]],
        [[142.0, 110.0], [192.0, 243.0], [459.0, 401.0]],
    ],
    dtype=np.float32,
)
STRIDES = [8, 16, 32]
XYSCALE = [1.2, 1.1, 1.05]


def postprocess_bbbox(pred_bbox):
    """define anchor boxes"""
    for i, pred in enumerate(pred_bbox):
        conv_shape = pred.shape
        output_size = conv_shape[1]
        conv_raw_dxdy = pred[:, :, :, :, 0:2]
        conv_raw_dwdh = pred[:, :, :, :, 2:4]
        xy_grid = np.meshgrid(np.arange(output_size), np.arange(output_size))
        xy_grid = np.expand_dims(np.stack(xy_grid, axis=-1), axis=2)

        xy_grid = np.tile(np.expand_dims(xy_grid, axis=0), [1, 1, 1, 3, 1])
        xy_grid = xy_grid.astype(float)

        pred_xy = (
            (special.expit(conv_raw_dxdy) * XYSCALE[i])
            - 0.5 * (XYSCALE[i] - 1)
            + xy_grid
        ) * STRIDES[i]
        pred_wh = np.exp(conv_raw_dwdh) * ANCHORS[i]
        pred[:, :, :, :, 0:4] = np.concatenate([pred_xy, pred_wh], axis=-1)

    pred_bbox = [np.reshape(x, (-1, np.shape(x)[-1])) for x in pred_bbox]
    pred_bbox = np.concatenate(pred_bbox, axis=0)
    return pred_bbox


def postprocess_boxes(pred_bbox, org_img_shape, input_size, score_threshold):
    """remove boundary boxs with a low detection probability"""
    valid_scale = [0, np.inf]
    pred_bbox = np.array(pred_bbox)

    pred_xywh = pred_bbox[:, 0:4]
    pred_conf = pred_bbox[:, 4]
    pred_prob = pred_bbox[:, 5:]

    # (1) (x, y, w, h) --> (xmin, ymin, xmax, ymax)
    pred_coor = np.concatenate(
        [
            pred_xywh[:, :2] - pred_xywh[:, 2:] * 0.5,
            pred_xywh[:, :2] + pred_xywh[:, 2:] * 0.5,
        ],
        axis=-1,
    )
    # (2) (xmin, ymin, xmax, ymax) -> (xmin_org, ymin_org, xmax_org, ymax_org)
    org_h, org_w = org_img_shape
    resize_ratio = min(input_size / org_w, input_size / org_h)

    dw = (input_size - resize_ratio * org_w) / 2
    dh = (input_size - resize_ratio * org_h) / 2

    pred_coor[:, 0::2] = 1.0 * (pred_coor[:, 0::2] - dw) / resize_ratio
    pred_coor[:, 1::2] = 1.0 * (pred_coor[:, 1::2] - dh) / resize_ratio

    # (3) clip some boxes that are out of range
    pred_coor = np.concatenate(
        [
            np.maximum(pred_coor[:, :2], [0, 0]),
            np.minimum(pred_coor[:, 2:], [org_w - 1, org_h - 1]),
        ],
        axis=-1,
    )
    invalid_mask = np.logical_or(
        (pred_coor[:, 0] > pred_coor[:, 2]),
        (pred_coor[:, 1] > pred_coor[:, 3]),
    )
    pred_coor[invalid_mask] = 0

    # (4) discard some invalid boxes
    bboxes_scale = np.sqrt(
        np.multiply.reduce(pred_coor[:, 2:4] - pred_coor[:, 0:2], axis=-1)
    )
    scale_mask = np.logical_and(
        (valid_scale[0] < bboxes_scale), (bboxes_scale < valid_scale[1])
    )

    # (5) discard some boxes with low scores
    classes = np.argmax(pred_prob, axis=-1)
    scores = pred_conf * pred_prob[np.arange(len(pred_coor)), classes]
    score_mask = scores > score_threshold
    mask = np.logical_and(scale_mask, score_mask)
    coors, scores, classes = pred_coor[mask], scores[mask], classes[mask]

    return np.concatenate(
        [coors, scores[:, np.newaxis], classes[:, np.newaxis]], axis=-1
    )


def bboxes_iou(boxes1, boxes2):
    """calculate the Intersection Over Union value"""
    boxes1 = np.array(boxes1)
    boxes2 = np.array(boxes2)

    boxes1_area = (boxes1[..., 2] - boxes1[..., 0]) * (
        boxes1[..., 3] - boxes1[..., 1]
    )
    boxes2_area = (boxes2[..., 2] - boxes2[..., 0]) * (
        boxes2[..., 3] - boxes2[..., 1]
    )

    left_up = np.maximum(boxes1[..., :2], boxes2[..., :2])
    right_down = np.minimum(boxes1[..., 2:], boxes2[..., 2:])

    inter_section = np.maximum(right_down - left_up, 0.0)
    inter_area = inter_section[..., 0] * inter_section[..., 1]
    union_area = boxes1_area + boxes2_area - inter_area
    ious = np.maximum(1.0 * inter_area / union_area, np.finfo(np.float32).eps)

    return ious


def nms(bboxes, iou_threshold, sigma=0.3, method="nms"):
    """
    :param bboxes: (xmin, ymin, xmax, ymax, score, class)

    Note: soft-nms, https://arxiv.org/pdf/1704.04503.pdf
          https://github.com/bharatsingh430/soft-nms
    """
    classes_in_img = list(set(bboxes[:, 5]))
    best_bboxes = []

    for cls in classes_in_img:
        cls_mask = bboxes[:, 5] == cls
        cls_bboxes = bboxes[cls_mask]

        while len(cls_bboxes) > 0:
            max_ind = np.argmax(cls_bboxes[:, 4])
            best_bbox = cls_bboxes[max_ind]
            best_bboxes.append(best_bbox)
            cls_bboxes = np.concatenate(
                [cls_bboxes[:max_ind], cls_bboxes[max_ind + 1 :]]
            )
            iou = bboxes_iou(best_bbox[np.newaxis, :4], cls_bboxes[:, :4])
            weight = np.ones((len(iou),), dtype=np.float32)

            assert method in ["nms", "soft-nms"]

            if method == "nms":
                iou_mask = iou > iou_threshold
                weight[iou_mask] = 0.0

            if method == "soft-nms":
                weight = np.exp(-(1.0 * iou**2 / sigma))

            cls_bboxes[:, 4] = cls_bboxes[:, 4] * weight
            score_mask = cls_bboxes[:, 4] > 0.0
            cls_bboxes = cls_bboxes[score_mask]

    return best_bboxes


def preprocess(
    image: Image.Image, size: Tuple[int, int] = (416, 416)
) -> np.ndarray:
    """resize image with unchanged aspect ratio using padding"""
    iw, ih = image.size
    w, h = size
    scale = min(w / iw, h / ih)
    nw = int(iw * scale)
    nh = int(ih * scale)

    image = image.resize((nw, nh), Image.Resampling.BICUBIC)
    new_image = Image.new("RGB", size, (128, 128, 128))
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))
    return np.expand_dims(np.array(new_image).astype(np.float32) / 255, 0)


class YoloV4(ObjectDetector):
    FILE = FileFromGithubLFS(
        organisation="onnx",
        repo="models",
        path="vision/object_detection_segmentation/yolov4/model/yolov4.onnx",
        md5="2e0eeb4de8da2a0663ae3eb4a0dabbce",
    )

    @property
    def class_labels(self) -> List[str]:
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
            "potted plant",
            "bed",
            "dining table",
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
        img_arrays = np.concatenate([preprocess(img) for img in imgs])
        img_shapes = [(img.height, img.width) for img in imgs]

        output = self.ort_sess.run(None, {"input_1:0": img_arrays})

        return [
            self._process_single_output(
                [
                    output[0][i : i + 1],
                    output[1][i : i + 1],
                    output[2][i : i + 1],
                ],
                img_shape,
                score_thres,
            )
            for i, img_shape in enumerate(img_shapes)
        ]

    def _process_single_output(
        self,
        output: List[np.ndarray],
        img_shape: Tuple[int, int],
        score_thres: float,
    ) -> List[Detection]:
        preds = postprocess_bbbox(output)
        preds = postprocess_boxes(preds, img_shape, 416, 0.25)
        preds = nms(preds, 0.213, method="nms")

        return [
            Detection(
                boundary=BoundingPolygon.from_bbox(
                    xmin=pred[0], ymin=pred[1], xmax=pred[2], ymax=pred[3]
                ),
                class_label=self.class_labels[int(pred[5])],
                score=pred[4],
            )
            for pred in preds
        ]
