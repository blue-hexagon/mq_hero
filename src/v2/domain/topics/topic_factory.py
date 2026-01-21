from src.v2.domain.entities.device import Device
from src.v2.domain.entities.mqtt_message_contract import MessageClass
from src.v2.domain.topics.topic import Topic
from src.v2.domain.policies.policy_engine import PolicyEngine
from src.v2.infrastructure.mqtt.types import MqttDirection


class TopicFactory:
    def __init__(self, policy: PolicyEngine):
        self.policy = policy

    def build(self, device: Device, msg_class: MessageClass, direction: MqttDirection) -> Topic:
        if not self.policy.is_allowed(device, msg_class, direction):
            raise PermissionError(
                f"Device {device.device_class.name} not allowed to {msg_class.name} {direction.name}"
            )

        return Topic(
            tenant_id=device.id,
            farm_id=device.get_farm_parent().id,
            device_class=device.device_class,
            device_id=device.id,
            message_class=msg_class,
        )
