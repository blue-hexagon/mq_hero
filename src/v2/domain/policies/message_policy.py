from typing import List

from src.v2.domain.entities.device import DeviceClass, Device
from src.v2.domain.entities.message_contract import MessageClass, MqttDirection
from src.v2.domain.entities.policy import Policy


class PolicyEngine:
    """Business logic + security rules (policy table)
       The policy table binds MessageClass to DeviceClass
    """

    def __init__(self):
        self.rules: list[Policy] = []

    def allow(self, *, dc: DeviceClass, mc: MessageClass, direction: MqttDirection):
        self.rules.append(
            Policy(
                device_class=dc,
                message_class=mc,
                direction=direction
            )
        )

    def is_allowed(self, device: Device, msg_class: MessageClass, direction: MqttDirection) -> bool:
        return any(
            rule.device_class == device.device_class and
            rule.message_class == msg_class and
            rule.direction == direction
            for rule in self.rules
        )
