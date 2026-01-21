from dataclasses import dataclass
from typing import Optional, Callable, Any

from src.v2.domain.entities.mqtt_message_contract import MessageClass
from src.v2.domain.topics.topic_level import TopicLevel
from src.v2.domain.topics.topic_segment import TopicSegment
from src.v2.infrastructure.mqtt.types import MqttDirection, QoS


@dataclass
class MqttMessageContract:
    """ Bridges the API and MQTT """
    msg_type: MessageClass
    direction: MqttDirection
    handler: Optional[Callable[[Any], str]] = None
    qos: QoS = 0
    retained: bool = False

    def get_topic_segment(self) -> TopicSegment:
        return TopicSegment(TopicLevel.MESSAGE_CLASS, self.msg_type.value)

    def attach_handler(self, handler: Callable[[Any], str]) -> None:
        self.handler = handler

    def __post_init__(self):
        if self.qos not in (0, 1, 2):
            raise ValueError("qos must be 0, 1, or 2")

    def __str__(self) -> str:
        return f"MessageContract(type={self.msg_type.value}, dir={self.direction.value}, qos={self.qos}, retained={self.retained})"
