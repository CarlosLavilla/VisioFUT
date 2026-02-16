from pathlib import Path
import xml.etree.ElementTree as ET

from utils.yolo2cvat.model import YoloAnnotationRow, Class, CVATBox, CVATImage

PREDICTIONS_DIR = (
    Path(__file__).resolve().parents[3] / "runs" / "detect" / "predictions"
)
IMG_WIDTH = 1920
IMG_HEIGHT = 1080

# Different thresholds for each category due to different difficulties on detection
CONFIDENCE_THRESHOLD: dict[Class, float] = {
    Class.PLAYER: 0.5,
    Class.REFEREE: 0.4,
    Class.BALL: 0.3,
}


def extract_frame_id(stem: str) -> int:
    # clipA_000120 → 120
    return int(stem.split("_")[-1])


def parse_yolo_line(line: str) -> YoloAnnotationRow:
    parts = line.strip().split()

    return YoloAnnotationRow(
        annotation_class=Class(int(parts[0])),
        x_center=float(parts[1]),
        y_center=float(parts[2]),
        width=float(parts[3]),
        height=float(parts[4]),
        confidence=float(parts[5]),
    )


def generate_xml(frames: dict[int, CVATImage]) -> ET.ElementTree:
    # Create root XML element
    root = ET.Element("annotations")

    # Create header (metadata)
    meta = ET.SubElement(root, "meta")
    task = ET.SubElement(meta, "task")
    labels = ET.SubElement(task, "labels")

    # Place the classes
    for cls in Class:
        label = ET.SubElement(labels, "label")
        name = ET.SubElement(label, "name")
        name.text = cls.name.lower()

    # Place the annotations
    for frame_id in sorted(frames.keys()):
        image_element = frames[frame_id].cvat_img_to_xml()
        root.append(image_element)

    return ET.ElementTree(root)


if not PREDICTIONS_DIR.exists():
    raise FileNotFoundError(f"Incorrect directory: {PREDICTIONS_DIR}")

frames: dict[int, CVATImage] = {}

for txt_file in PREDICTIONS_DIR.glob("**/*.txt"):
    frame_id = extract_frame_id(txt_file.stem)

    with open(txt_file, "r") as f:
        for line in f:
            row: YoloAnnotationRow = parse_yolo_line(line)

            if row.confidence < CONFIDENCE_THRESHOLD[row.annotation_class]:
                continue

            box: CVATBox = row.yolo_to_cvat_box(IMG_WIDTH, IMG_HEIGHT)

            # store box grouped by frame_id
            frames.setdefault(
                frame_id, CVATImage(frame_id, IMG_WIDTH, IMG_HEIGHT, [])
            ).boxes.append(box)

xml_file: ET.ElementTree = generate_xml(frames)

xml_file.write("annotations.xml", encoding="utf-8", xml_declaration=True)
