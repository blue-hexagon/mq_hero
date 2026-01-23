from dataclasses import dataclass
from typing import Optional

from src.v2.domain.entities.device import DeviceClass
from src.v2.domain.entities.farm import Farm
from src.v2.domain.entities.message_class import MessageClass
from src.v2.infrastructure.mqtt.types import MqttDirection


@dataclass(frozen=True,repr=False)
class Policy:
    name: str
    farm: Optional[Farm]
    device_class: DeviceClass
    message_class: MessageClass
    direction: MqttDirection

    def __repr__(self) -> str:
        return f"Policy(name={self.name}, farm={self.farm.name}, device_class={self.device_class}, message_class={self.message_class}, direction={self.direction})"



