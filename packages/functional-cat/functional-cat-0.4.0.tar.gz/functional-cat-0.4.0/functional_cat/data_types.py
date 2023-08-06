import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

import numpy as np
from PIL import Image, ImageDraw, ImageFont

MaskType = List[List[float]]
ImageInput = List[Image.Image]
NumberType = Union[float, int]


__all__ = ["Detection", "InstanceSegmentation"]


@dataclass
class Point:
    x: NumberType
    y: NumberType

    def resize(
        self, og_img_h: int, og_img_w: int, new_img_h: int, new_img_w: int
    ) -> "Point":
        h_factor, w_factor = new_img_h / og_img_h, new_img_w / og_img_w
        return Point(x=w_factor * self.x, y=h_factor * self.y)

    def int(self):
        return Point(x=int(self.x), y=int(self.y))


@dataclass
class BoundingPolygon:
    """Class for representing a bounding region."""

    points: List[Point]

    def draw_on_image(
        self,
        img: Image.Image,
        inplace: bool = False,
        text: str = None,
        font_size: int = 24,
        color: Tuple[int, int, int] = (255, 0, 0),
    ) -> Image.Image:
        img = img if inplace else img.copy()
        img_draw = ImageDraw.Draw(img)

        img_draw.polygon(
            [(p.x, p.y) for p in self.points],
            outline=color,
        )

        if text is not None:
            _write_text_on_bbox(
                font_size=font_size,
                text=text,
                boundary=self,
                draw=img_draw,
                color=color,
            )
        return img

    def int(self):
        return BoundingPolygon(points=[p.int() for p in self.points])

    @property
    def xmin(self):
        return min(p.x for p in self.points)

    @property
    def ymin(self):
        return min(p.y for p in self.points)

    @property
    def xmax(self):
        return max(p.x for p in self.points)

    @property
    def ymax(self):
        return max(p.y for p in self.points)

    def resize(
        self, og_img_h: int, og_img_w: int, new_img_h: int, new_img_w: int
    ) -> "BoundingPolygon":
        return BoundingPolygon(
            points=[
                p.resize(
                    og_img_h=og_img_h,
                    og_img_w=og_img_w,
                    new_img_h=new_img_h,
                    new_img_w=new_img_w,
                )
                for p in self.points
            ]
        )

    @classmethod
    def from_bbox(
        cls, xmin: float, ymin: float, xmax: float, ymax: float
    ) -> "BoundingPolygon":
        return cls(
            points=[
                Point(x=xmin, y=ymin),
                Point(x=xmin, y=ymax),
                Point(x=xmax, y=ymax),
                Point(x=xmax, y=ymin),
            ]
        )


@dataclass
class Detection:
    """Class representing a single object detection in an image."""

    boundary: BoundingPolygon
    class_label: str
    score: float

    def draw_on_image(
        self,
        img: Image.Image,
        inplace: bool = False,
        color: Tuple[int, int, int] = (255, 0, 0),
    ) -> Image.Image:
        img = self.boundary.draw_on_image(
            img,
            inplace=inplace,
            text=f"{self.class_label} {self.score:0.2f}",
            color=color,
        )
        return img

    def resize(
        self, og_img_h: int, og_img_w: int, new_img_h: int, new_img_w: int
    ) -> "Detection":
        return Detection(
            boundary=self.boundary.resize(
                og_img_h=og_img_h,
                og_img_w=og_img_w,
                new_img_h=new_img_h,
                new_img_w=new_img_w,
            ),
            class_label=self.class_label,
            score=self.score,
        )

    def int(self):
        return Detection(
            boundary=self.boundary.int(),
            class_label=self.class_label,
            score=self.score,
        )


@dataclass
class InstanceSegmentation(Detection):
    mask: MaskType

    def draw_on_image(
        self,
        img: Image.Image,
        draw_bbox: bool = True,
        draw_mask: bool = True,
        inplace: bool = False,
        color: Tuple[int, int, int] = (255, 0, 0),
    ) -> Image.Image:
        if draw_bbox:
            img = super().draw_on_image(img, inplace, color=color)
        else:
            img = img if inplace else img.copy()

        if draw_mask:
            bin_mask = np.array(self.mask) > 0.5

            mask_arr = np.zeros(
                (bin_mask.shape[0], bin_mask.shape[1], 3), dtype=np.uint8
            )
            mask_arr[bin_mask] = color
            mask_img = Image.fromarray(mask_arr)
            blend = Image.blend(img, mask_img, alpha=0.4)
            img.paste(blend, (0, 0), mask=Image.fromarray(bin_mask))

        return img


@dataclass
class Keypoint:
    class_label: str
    x: float
    y: float
    score: float = None
    visible: bool = None

    def draw_on_image(
        self,
        img: Image.Image,
        inplace: bool = False,
        radius: int = 2,
        color: Tuple[int, int, int] = (255, 0, 0),
    ) -> Image.Image:
        img = img if inplace else img.copy()
        img_draw = ImageDraw.Draw(img)
        img_draw.ellipse(
            (
                self.x - radius,
                self.y - radius,
                self.x + radius,
                self.y + radius,
            ),
            fill=color,
        )

        return img


@dataclass
class DetectionWithKeypoints(Detection):
    keypoints: List[Keypoint]

    def draw_on_image(
        self,
        img: Image.Image,
        inplace: bool = False,
        color_map: Dict[str, Tuple[int, int, int]] = None,
    ) -> Image.Image:
        img = super().draw_on_image(img=img, inplace=inplace)
        for keypoint in self.keypoints:
            if color_map is not None:
                img = keypoint.draw_on_image(
                    img, color=color_map[keypoint.class_label]
                )
            else:
                img = keypoint.draw_on_image(img)

        return img


def _get_font(font_size: int):
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        try:
            font = ImageFont.truetype("Arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

    return font


def _write_text_on_bbox(
    font_size: int,
    text: str,
    boundary: BoundingPolygon,
    draw: ImageDraw.Draw,
    color: str,
):
    font = _get_font(font_size)
    text_width, text_height = font.getsize(text)
    if boundary.ymin > text_height:
        text_bottom = boundary.ymin
    else:
        text_bottom = boundary.ymax + text_height

    margin = math.ceil(0.05 * text_height) - 1
    draw.rectangle(
        [
            (boundary.xmin, text_bottom - text_height - 2 * margin),
            (boundary.xmin + text_width, text_bottom),
        ],
        fill=color,
    )
    draw.text(
        (boundary.xmin + margin, text_bottom - text_height - margin),
        text,
        fill="black",
        font=font,
    )
