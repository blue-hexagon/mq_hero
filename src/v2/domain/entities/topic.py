from dataclasses import dataclass

from src.v2.domain.entities.message_contract import MessageClass


@dataclass
class Topic:
    @dataclass(frozen=True)
    class Topic:
        tenant: str
        farm_id: str
        device_type: str
        device_id: str
        message_type: MessageClass

        def render(self) -> str:
            return "/".join([
                self.tenant,
                self.farm_id,
                self.device_type,
                self.device_id,
                self.message_type.value,
            ])
