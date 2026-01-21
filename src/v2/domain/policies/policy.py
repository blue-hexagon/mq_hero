from dataclasses import dataclass

from src.v2.domain.entities.device import DeviceClass
from src.v2.domain.entities.mqtt_message_contract import MessageClass
from src.v2.infrastructure.mqtt.types import MqttDirection


@dataclass(frozen=True)
class Policy:
    device_class: DeviceClass
    message_class: MessageClass
    direction: MqttDirection
