from dataclasses import dataclass
from typing import Optional, Callable, Any

from src.v2.domain.entities.message_class import MessageClass
from src.v2.domain.topics.topic_segment import TopicSegment
from src.v2.infrastructure.mqtt.types import MqttDirection, QoS


@dataclass
class MqttMessageContract:
    """ Bridges the API and MQTT """
    message_class: MessageClass
    direction: MqttDirection
    handler: Optional[Callable[[Any], str]] = None
    qos: QoS = 0
    retained: bool = False

    def get_topic_segment(self) -> TopicSegment:
        return TopicSegment(kind="message", token=self.message_class.id)

    def attach_handler(self, handler: Callable[[Any], str]) -> None:
        self.handler = handler

    def __post_init__(self):
        if self.qos not in (0, 1, 2):
            raise ValueError("qos must be 0, 1, or 2")

    def __str__(self) -> str:
        return (f"MessageContract(msg_class={self.message_class.id}, dir={self.direction.value}, qos={self.qos}"
                f", retained={self.retained})")
