from dataclasses import dataclass

from utils.yolo2cvat.model.CVATElement import CVATTrackedBox
from utils.yolo2cvat.model.Enum import MyYoloLabel


@dataclass
class YoloAnnotationRow:
    annotation_class: MyYoloLabel
    x_center: float
    y_center: float
    width: float
    height: float
    confidence: float
    track_id: int

    def yolo_to_cvat_track_box(
        self, frame_id: int, img_width: int, img_height: int
    ) -> CVATTrackedBox:
        """
        Converts a YoLo .txt annotation file into a representation of what CVAT expects for importing.

        :param self: YoloAnnotationRow instance
        :param frame_id: id of the frame
        :type frame_id: int
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
        track_box: CVATTrackedBox = CVATTrackedBox(
            frame_id,
            max(0, x_center - width / 2),
            max(0, y_center - height / 2),
            min(img_width - 1, x_center + width / 2),
            min(img_height - 1, y_center + height / 2),
        )
        return track_box
