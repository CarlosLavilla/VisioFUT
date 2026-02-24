from abc import ABC, abstractmethod
from dataclasses import dataclass
import xml.etree.ElementTree as ET


class CVATElement(ABC):

    @abstractmethod
    def to_xml(self, parent: ET.Element) -> ET.Element:
        pass


@dataclass
class CVATTrackedBox(CVATElement):
    frame: int
    xtl: float
    ytl: float
    xbr: float
    ybr: float
    outside: int = 0
    occluded: int = 0
    keyframe: int = 0
    z_order: int = 0

    def to_xml(self, parent: ET.Element):
        return ET.SubElement(
            parent,
            "box",
            {
                "frame": str(self.frame),
                "xtl": f"{self.xtl:.2f}",
                "ytl": f"{self.ytl:.2f}",
                "xbr": f"{self.xbr:.2f}",
                "ybr": f"{self.ybr:.2f}",
                "outside": str(self.outside),
                "occluded": str(self.occluded),
                "keyframe": str(self.keyframe),
                "z_order": str(self.z_order),
            },
        )


@dataclass
class CVATTrack(CVATElement):
    track_id: int
    label: str
    tracked_boxes: list[CVATTrackedBox]
    source: str = "auto"

    def to_xml(self, parent: ET.Element):
        track_xml: ET.Element = ET.SubElement(
            parent,
            "track",
            {"id": str(self.track_id), "label": self.label, "source": self.source},
        )
        for tracked_box in sorted(self.tracked_boxes, key=lambda b: b.frame):
            tracked_box.to_xml(track_xml)

        return track_xml
