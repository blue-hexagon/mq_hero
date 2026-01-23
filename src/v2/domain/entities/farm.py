from dataclasses import field, dataclass
from typing import Dict

from src.v2.domain.entities.device import Device
from src.v2.domain.topics.topic_segment import TopicSegment


@dataclass
class Farm:
    id: str
    name: str
    city: str
    devices: Dict[str, Device] = field(default_factory=dict)

    def get_topic_segment(self) -> TopicSegment:
        return TopicSegment(kind="farm", token=self.id)

    def get_device(self, device_id: str) -> Device:
        try:
            return self.devices[device_id]
        except KeyError:
            raise KeyError(
                f"Device '{device_id}' not found in farm '{self.id}'"
            )

    def __str__(self) -> str:
        return f"Farm(id={self.id}, name={self.name}, city={self.city}, devices={len(self.devices)})"
    def __repr__(self) -> str:
        return f"{self.name}::{self.devices}"