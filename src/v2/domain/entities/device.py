from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List

from src.v2.domain.entities.message_contract import MessageContract
from src.v2.domain.topics.topic_level import TopicLevel
from src.v2.domain.topics.topic_segment import TopicSegment

class DeviceClass(str, Enum):
    MACHINE = "machine"
    SENSOR = "sensor"
    DRONE = "drone"

    def topic_segment(self) -> TopicSegment:
        return TopicSegment(TopicLevel.DEVICE_CLASS, self.value)


@dataclass
class Device:
    id: str
    device_class: DeviceClass
    model: Optional[str] = None
    location: Optional[str] = None
    messages: List[MessageContract] = field(default_factory=list)

    def topic_segment(self) -> TopicSegment:
        return TopicSegment(TopicLevel.DEVICE, self.id)

    def add_message(self, contract: MessageContract):
        self.messages.append(contract)

    def __str__(self) -> str:
        return f"Device(id={self.id}, class={self.device_class.value}, model={self.model}, location={self.location}, topic_segment={self.topic_segment()})"
