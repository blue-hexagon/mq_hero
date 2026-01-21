from dataclasses import dataclass

from src.v2.domain.entities.device import DeviceClass
from src.v2.domain.entities.mqtt_message_contract import MessageClass


@dataclass(frozen=True)
class Topic:
    tenant_id: str
    farm_id: str
    device_class: DeviceClass
    device_id: str
    message_class: MessageClass

    def render(self) -> str:
        return "/".join([
            self.tenant_id,
            self.farm_id,
            self.device_class.value,
            self.device_id,
            self.message_class.value,
        ])
