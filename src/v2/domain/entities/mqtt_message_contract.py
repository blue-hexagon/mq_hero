from dataclasses import dataclass
from enum import Enum
from typing import Literal, Optional, Callable, Any
from src.v2.domain.topics.topic_level import TopicLevel
from src.v2.domain.topics.topic_segment import TopicSegment


class MessageClass(str, Enum):
    METRICS = "metrics"  # aggregated indicators
    EVENTS = "events"  # discrete occurrences
    STATE = "state"  # persistent device state
    ALERT = "alert"  # urgent events
    COMMAND = "cmd"  # control plane
    LOGS = "logs"  # diagnostics
    IMAGE = "image"  # binary payload


class MqttDirection(str, Enum):
    PUB = "publish"
    SUB = "subscribe"


QoS = Literal[0, 1, 2]


@dataclass
class MqttMessageContract:
    """ Bridges the API and MQTT """
    msg_type: MessageClass
    direction: MqttDirection
    handler: Optional[Callable[[Any], str]] = None
    qos: QoS = 0
    retained: bool = False

    def topic_segment(self) -> TopicSegment:
        return TopicSegment(TopicLevel.MESSAGE_TYPE, self.msg_type.value)

    def attach_handler(self, handler: Callable[[Any], str]) -> None:
        self.handler = handler

    def __post_init__(self):
        if self.qos not in (0, 1, 2):
            raise ValueError("qos must be 0, 1, or 2")

    def __str__(self) -> str:
        return f"MessageContract(type={self.msg_type.value}, dir={self.direction.value}, qos={self.qos}, retained={self.retained})"
