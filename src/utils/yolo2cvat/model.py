from enum import Enum
from dataclasses import dataclass


class Class(Enum):
    PLAYER = 0
    BALL = 1
    REFEREE = 2


@dataclass
class CVATBox:
    label: str
    xtl: int
    ytl: int
    xbr: int
    ybr: int
    occluded: int = 0
    source: str = "auto"


@dataclass
class CVATImage:
    frame_id: int
    width: int
    height: int
    boxes: list[CVATBox]


@dataclass
class YoLoAnnotationRow:
    annotation_class: Class
    x_center: float
    y_center: float
    width: float
    height: float
    confidence: float

    def yolo_to_cvat_box(self, img_width: int, img_height: int) -> CVATBox:

        # YoLo normalizes values, I de-normalize them
        x_center = self.x_center * img_width
        y_center = self.y_center * img_height
        width = self.width * img_width
        height = self.height * img_height

        # min and max used to not go out of the image
        box: CVATBox = CVATBox(
            self.annotation_class.name.lower(),
            max(0, int(x_center - width / 2)),
            max(0, int(y_center - height / 2)),
            min(img_width - 1, int(x_center + width / 2)),
            min(img_height - 1, int(y_center + height / 2)),
        )
        return box
