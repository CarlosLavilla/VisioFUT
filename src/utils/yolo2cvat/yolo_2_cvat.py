from pathlib import Path
import xml.etree.ElementTree as ET

from utils.yolo2cvat.model.CVATElement import CVATTrack, CVATTrackedBox
from utils.yolo2cvat.model.YoloAnnotation import YoloAnnotationRow
from utils.yolo2cvat.model.Enum import MyYoloLabel

PREDICTIONS_DIR = (
    Path(__file__).resolve().parents[3] / "runs" / "detect" / "predictions"
)
IMG_WIDTH = 1920
IMG_HEIGHT = 1080

# Different thresholds for each category due to different difficulties on detection
CONFIDENCE_THRESHOLD: dict[MyYoloLabel, float] = {
    MyYoloLabel.PLAYER: 0.5,
    MyYoloLabel.REFEREE: 0.4,
    MyYoloLabel.BALL: 0.3,
}


def extract_frame_id(stem: str) -> int:
    # clipA_000120 → 119 (0-based)
    return int(stem.split("_")[-1]) - 1


def parse_yolo_line(line: str) -> YoloAnnotationRow:
    parts = line.strip().split()

    return YoloAnnotationRow(
        annotation_class=MyYoloLabel(int(parts[0])),
        x_center=float(parts[1]),
        y_center=float(parts[2]),
        width=float(parts[3]),
        height=float(parts[4]),
        confidence=float(parts[5]),
        track_id=int(parts[6]),
    )


def generate_xml(tracks: dict[str, CVATTrack]) -> ET.ElementTree:
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


if not PREDICTIONS_DIR.exists():
    raise FileNotFoundError(f"Incorrect directory: {PREDICTIONS_DIR}")

tracks: dict[str, CVATTrack] = {}

for txt_file in PREDICTIONS_DIR.glob("**/*.txt"):
    frame_id = extract_frame_id(txt_file.stem)

    with open(txt_file, "r") as f:
        for line in f:
            row: YoloAnnotationRow = parse_yolo_line(line)

            if row.confidence < CONFIDENCE_THRESHOLD[row.annotation_class]:
                continue

            box: CVATTrackedBox = row.yolo_to_cvat_track_box(
                frame_id, IMG_WIDTH, IMG_HEIGHT
            )

            key: str = f"{row.annotation_class.name}-{row.track_id}"

            # store box grouped by track_id
            tracks.setdefault(
                key,
                CVATTrack(row.track_id, row.annotation_class.name.lower(), []),
            ).tracked_boxes.append(box)

xml_file: ET.ElementTree = generate_xml(tracks)

xml_file.write("annotations.xml", encoding="utf-8", xml_declaration=True)
