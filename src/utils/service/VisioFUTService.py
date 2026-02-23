from pathlib import Path
from typing import Iterable, Iterator
import xml.etree.ElementTree as ET

from ultralytics import YOLO
from ultralytics.engine.results import Results

import cv2

from utils.model.CVATElement import CVATTrack, CVATTrackedBox
from utils.model.enum import MyYoloLabel

IMG_WIDTH = 1920
IMG_HEIGHT = 1080

# Different thresholds for each category due to different difficulties on detection
CONFIDENCE_THRESHOLD: dict[MyYoloLabel, float] = {
    MyYoloLabel.PLAYER: 0.5,
    MyYoloLabel.REFEREE: 0.4,
    MyYoloLabel.BALL: 0.3,
}


class VisioFUTService:

    def __init__(self, model_path: Path) -> None:
        self._model = YOLO(str(model_path))

    def track_video(self, video_path: Path) -> Iterator[int]:
        results: Iterable[Results] = self._model.track(
            source=video_path, persist=True, stream=True, device=0, conf=0.25
        )

        total_frames = self._get_total_frames(video_path)

        yield from self._create_xml_predictions(
            results=results, total_frames=total_frames
        )

    def _get_total_frames(self, video_path: Path):
        cap = cv2.VideoCapture(str(video_path))
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        return total

    def _create_xml_predictions(
        self, results: Iterable[Results], total_frames: int
    ) -> Iterator[int]:
        tracks: dict[str, CVATTrack] = {}

        # Progress tracking by frames
        processed_frames: int = 0

        for frame_id, result in enumerate(results):

            boxes = result.boxes

            if boxes is None or boxes.id is None:
                continue

            self._process_frame(tracks, frame_id, boxes)

            # Increment progress
            processed_frames += 1

            # Yield percentage progress
            if total_frames is not None and total_frames > 0:
                percent: int = int((processed_frames / total_frames) * 100)
                yield min(percent, 100)
            else:
                # Fallback for indeterminate progress
                yield processed_frames

        xml_file: ET.ElementTree = self._generate_xml(tracks)

        xml_file.write("annotations.xml", encoding="utf-8", xml_declaration=True)

        # Complete progress
        yield 100

    def _process_frame(self, tracks, frame_id, boxes):
        for box_index in range(len(boxes)):
            track_id: int = int(boxes.id[box_index])
            class_id: int = int(boxes.cls[box_index])

            confidence: float = float(boxes.conf[box_index])

            if confidence < CONFIDENCE_THRESHOLD[MyYoloLabel(class_id)]:
                continue

            xyxy = boxes.xyxy[box_index].tolist()
            x1, y1, x2, y2 = xyxy

            cvat_box: CVATTrackedBox = CVATTrackedBox(frame_id, x1, y1, x2, y2)

            key: str = f"{class_id}-{track_id}"

            tracks.setdefault(
                key,
                CVATTrack(track_id, str(class_id), []),
            ).tracked_boxes.append(cvat_box)

    def _generate_xml(self, tracks: dict[str, CVATTrack]) -> ET.ElementTree:
        # Create root XML element
        root = ET.Element("annotations")
        version = ET.SubElement(root, "version")
        version.text = "1.1"

        # Create header (metadata)
        meta = ET.SubElement(root, "meta")
        task = ET.SubElement(meta, "task")
        labels = ET.SubElement(task, "labels")

        # Place the classes
        for cls in MyYoloLabel:
            label = ET.SubElement(labels, "label")
            name = ET.SubElement(label, "name")
            name.text = cls.name.lower()

        # Place the annotations
        for key in sorted(tracks.keys()):
            _ = tracks[key].to_xml(root)

        return ET.ElementTree(root)
