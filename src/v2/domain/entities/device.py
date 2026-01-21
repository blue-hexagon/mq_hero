from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List

from src.v2.domain.topics.topic_level import TopicLevel
from src.v2.domain.topics.topic_segment import TopicSegment
from src.v2.infrastructure.mqtt.message_contract import MqttMessageContract



@dataclass(frozen=True, slots=True)
class DeviceClass:
    id: str

    def get_topic_segment(self) -> TopicSegment:
        return TopicSegment(TopicLevel.DEVICE_CLASS, self.id)
@dataclass
class Device:
    id: str
    device_class: DeviceClass
    model: Optional[str] = None
    location: Optional[str] = None
    messages: List[MqttMessageContract] = field(default_factory=list)

    def get_topic_segment(self) -> TopicSegment:
        return TopicSegment(TopicLevel.DEVICE, self.id)

    def _add_message(self, contract: MqttMessageContract):
        self.messages.append(contract)

    def __str__(self) -> str:
        return f"Device(id={self.id}, class={self.device_class.value}, model={self.model}, location={self.location}, topic_segment={self.topic_segment()})"
