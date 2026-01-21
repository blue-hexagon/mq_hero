from src.v2.domain.entities.device import DeviceClass, Device
from src.v2.domain.entities.mqtt_message_contract import MessageClass
from src.v2.domain.policies.policy import Policy
from src.v2.infrastructure.mqtt.types import MqttDirection


class PolicyEngine:
    """Business logic + security rules (policy table)
       The policy table binds MessageClass to DeviceClass
    """

    def __init__(self):
        self.rules: list[Policy] = []

    def allow(self, /, device_class: DeviceClass, message_class: MessageClass, mqtt_direction: MqttDirection):
        self.rules.append(
            Policy(
                device_class=device_class,
                message_class=message_class,
                direction=mqtt_direction
            )
        )

    def is_allowed(self, device: Device, msg_class: MessageClass, direction: MqttDirection) -> bool:
        return any(
            rule.device_class == device.device_class and
            rule.message_class == msg_class and
            rule.direction == direction
            for rule in self.rules
        )
