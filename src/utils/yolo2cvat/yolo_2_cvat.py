from pathlib import Path

from utils.yolo2cvat.model import YoLoAnnotationRow, Class

PREDICTIONS_DIR = (
    Path(__file__).resolve().parents[3] / "runs" / "detect" / "predictions"
)
IMG_WIDTH = 0
IMG_HEIGHT = 0

CONFIDENCE_THRESHOLD = 0


def extract_frame_id(stem: str) -> int:
    # clipA_000120 → 120
    return int(stem.split("_")[-1])


def parse_yolo_line(line: str) -> YoLoAnnotationRow:
    parts = line.strip().split()

    return YoLoAnnotationRow(
        annotation_class=Class(int(parts[0])),
        x_center=float(parts[1]),
        y_center=float(parts[2]),
        width=float(parts[3]),
        height=float(parts[4]),
        confidence=float(parts[5]),
    )


if not PREDICTIONS_DIR.exists():
    raise FileNotFoundError(f"Incorrect directory: {PREDICTIONS_DIR}")

for txt_file in PREDICTIONS_DIR.glob("**/*.txt"):
    frame_id = extract_frame_id(txt_file.stem)

    with open(txt_file, "r") as f:
        for line in f:
            print(line)
            row = parse_yolo_line(line)

            if row.confidence < CONFIDENCE_THRESHOLD:
                continue

            box = row.yolo_to_cvat_box(IMG_WIDTH, IMG_HEIGHT)

            # store box grouped by frame_id
