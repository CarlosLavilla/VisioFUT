from enum import Enum
from dataclasses import dataclass
import xml.etree.ElementTree as ET


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

    def cvat_box_to_xml(self, element: ET.Element) -> ET.Element:
        """
        Transforms the CVAT box representation into XML format.

        :param self: the CVAT box instance
        :param element: parent element in the XML hierarchy.
        :type element: ET.Element
        :return: XML subelement representing a CVAT box
        :rtype: Element[str]
        """
        return ET.SubElement(
            element,
            "box",
            {
                "label": self.label,
                "xtl": str(self.xtl),
                "ytl": str(self.ytl),
                "xbr": str(self.xbr),
                "ybr": str(self.ybr),
                "occluded": str(self.occluded),
                "source": self.source,
            },
        )


@dataclass
class CVATImage:
    frame_id: int
    width: int
    height: int
    boxes: list[CVATBox]

    def cvat_img_to_xml(self) -> ET.Element:
        """
        Transforms a CVAT Image (frame) into its XML representation.

        :param self: CVAT image instance.
        :return: XML representation of the image.
        :rtype: Element[str]
        """
        image_element = ET.Element(
            "image",
            {
                "id": str(self.frame_id),
                "name": f"frame_{self.frame_id:06d}.jpg",
                "width": str(self.width),
                "height": str(self.height),
            },
        )

        for box in self.boxes:
            box.cvat_box_to_xml(image_element)

        return image_element


@dataclass
class YoloAnnotationRow:
    annotation_class: Class
    x_center: float
    y_center: float
    width: float
    height: float
    confidence: float

    def yolo_to_cvat_box(self, img_width: int, img_height: int) -> CVATBox:
        """
        Converts a YoLo .txt annotation file into a representation of what CVAT expects for importing.

        :param self: YoloAnnotationRow instance
        :param img_width: width of the image
        :type img_width: int
        :param img_height: height of the image
        :type img_height: int
        :return: CVAT representation of the YoLo .txt file
        :rtype: CVATBox
        """
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
