from enum import Enum
from typing import Literal


class MqttDirection(str, Enum):
    PUB = "publish"
    SUB = "subscribe"


QoS = Literal[0, 1, 2]
