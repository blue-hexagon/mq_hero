from dataclasses import field, dataclass
from typing import Dict, Optional

from src.v2.domain.entities.device import Device
from src.v2.domain.exceptions import DeviceAlreadyExists
from src.v2.domain.topics.topic_level import TopicLevel
from src.v2.domain.topics.topic_segment import TopicSegment


@dataclass
class Farm:
    id: str
    name: str
    city: str
    devices: Dict[Device] = field(default_factory=dict)

    def topic_segment(self) -> TopicSegment:
        return TopicSegment(TopicLevel.FARM, self.id)

    def add_device(self, device: Device):
        if device.id in self.devices:
            raise DeviceAlreadyExists("TODO")
        self.devices[device.id] = device

    def get_device_by_id(self, device_id) -> Optional[Device]:
        for device in self.devices:
            if device.id == device_id:
                return device
        return None

    def __str__(self) -> str:
        return f"Farm(id={self.id}, name={self.name}, city={self.city}, devices={len(self.devices)})"


