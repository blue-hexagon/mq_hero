from dataclasses import dataclass
from enum import Enum

from src.v2.domain.entities.device import DeviceClass
from src.v2.domain.entities.message_class import MessageClass


class TopicScope(str, Enum):
    SINGLE = "single"
    ALL = "all"
    ALL_RECURSIVE = "recursive"


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
            self.device_class.id,
            self.device_id,
            self.message_class.id,
        ])
