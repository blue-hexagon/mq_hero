from src.v2.domain.entities.device import Device
from src.v2.domain.entities.message_contract import MessageClass, MqttDirection
from src.v2.domain.entities.topic import Topic
from src.v2.domain.policies.message_policy import PolicyEngine


class TopicFactory:
    def __init__(self, policy: PolicyEngine):
        self.policy = policy

    def build(self, device: Device, msg_type: MessageClass, direction: MqttDirection) -> Topic:
        if not self.policy.is_allowed(device, msg_type, direction):
            raise PermissionError(
                f"Device {device.device_class.name} not allowed to {msg_type.name} {direction.name}"
            )

        return Topic(
            tenant=device.tenant,
            farm_id=device.farm_id,
            device_type=device.device_type,
            device_id=device.device_id,
            message_type=msg_type.name,
        )