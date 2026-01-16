import re
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import Callable
from typing import List


class DeviceType(str, Enum):
    SENSOR = "sensor"
    ACTUATOR = "actuator"
    DRONE = "drone"


class TopicCategory(str, Enum):
    STATE = "state"
    EVENTS = "events"
    CMD = "cmd"
    METRICS = "metrics"
    LOGS = "logs"


@dataclass(frozen=True)
class MessageContract:
    category: TopicCategory
    direction: str  # "publish" or "subscribe"
    handler: Callable | None = None
    qos: int = 0
    retained: bool = False


@dataclass
class Device:
    id: str
    type: str
    model: str | None = None
    location: str | None = None


@dataclass
class Farm:
    id: str
    name: str
    city: str
    devices: List[Device] = field(default_factory=list)


@dataclass
class Company:
    id: str
    short_name: str
    full_name: str
    api_version: int
    description: str
    farms: List[Farm] = field(default_factory=list)

    def topic_root(self) -> str:
        safe = self.short_name.lower()
        safe = re.sub(r'[^a-z0-9_]+', '_', safe)
        return f"{safe.strip('_')}/v{self.api_version}"