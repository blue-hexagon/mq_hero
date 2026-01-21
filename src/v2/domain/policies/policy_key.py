from dataclasses import dataclass
from typing import Optional

from src.v2.infrastructure.mqtt.types import MqttDirection


@dataclass(frozen=True, slots=True)
class PolicyKey:
    tenant_id: str
    farm_id: Optional[str]  # None = global
    device_class_id: str
    message_class_id: str
    direction: MqttDirection
