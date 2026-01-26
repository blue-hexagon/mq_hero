import logging
from dataclasses import field, dataclass
from typing import Union, List

from src.v2.domain.entities.device import Device, DeviceClass
from src.v2.domain.entities.farm import Farm
from src.v2.domain.entities.location import Location
from src.v2.domain.entities.message_class import MessageClass
from src.v2.domain.errors import LocationAlreadyExists
from src.v2.infrastructure.mqtt.entity.broker import MqttBroker
from src.v2.domain.policies.policy import Policy
from src.v2.domain.policies.policy_engine import PolicyEngine
from src.v2.domain.policies.policy_key import PolicyKey
from src.v2.domain.topics.topic_segment import TopicSegment


@dataclass
class Tenant:
    id: str
    short_name: str
    full_name: str
    api_version: int
    description: str
    farms: dict[str, Farm] = field(default_factory=dict)
    mqtt_brokers: dict[str, MqttBroker] = field(default_factory=dict)
    device_classes: dict[str, DeviceClass] = field(default_factory=dict)
    message_classes: dict[str, MessageClass] = field(default_factory=dict)
    locations: dict[str, Location] = field(default_factory=dict)
    policies: dict[PolicyKey, Policy] = field(default_factory=dict)
    _policy_engine = None

    def get_topic_segment(self) -> TopicSegment:
        return TopicSegment(kind="tenant", token=self.id)

    def policy_engine(self) -> PolicyEngine:
        if self._policy_engine is None:
            self._policy_engine = PolicyEngine(self.policies.values())
        return self._policy_engine

    def register_mqtt_broker(self, mqtt_broker: MqttBroker):
        if mqtt_broker.ref in self.mqtt_brokers:
            raise Exception("")
        self.mqtt_brokers[mqtt_broker.ref] = mqtt_broker

    def register_farm(self, farm: Farm) -> None:
        if farm.id in self.farms:
            raise ValueError(
                f"Farm '{farm.id}' already exists in tenant '{self.id}'"
            )
        self.farms[farm.id] = farm

    def register_device(self, farm_id: str, device: Device) -> None:
        farm = self.get_farm(farm_id)

        if device.id in farm.devices:
            raise ValueError(
                f"Device '{device.id}' already exists in farm '{farm.id}'"
            )
        farm.devices[device.id] = device

    def register_location(self, location: Location):
        if location.name in self.locations:
            raise LocationAlreadyExists(f"{location.name} already exists in tenant '{self.short_name}")
        else:
            self.locations[location.name] = location

    def register_policy(self, policy: Policy) -> None:
        logger = logging.getLogger(__name__)

        pkey = PolicyKey(
            tenant_id=self.id,
            farm_id=policy.farm.id if policy.farm else None,
            device_class_id=policy.device_class.id,
            message_class_id=policy.message_class.id,
            direction=policy.direction,
        )
        if pkey in self.policies.keys():
            raise ValueError(
                f"Duplicate policy in tenant '{self.id}': "
                f"{policy.device_class.id} → {policy.message_class.id} → "
                f"{policy.direction} "
                f"{'in farm ' + policy.farm.id if policy.farm else '(global)'} "
                f"(policy name: {policy.name})"
            )
        # pkey is a dataclass and gets a unique hash that is used
        self.policies[pkey] = policy
        self._policy_engine = None  # invalidate cache

        logger.debug(
            "policy created (allow)",
            extra={
                "tenant": self.short_name,
                "farm": policy.farm.city,
                "device_class": policy.device_class.id,
                "message_class": policy.message_class.id,
                "direction": policy.direction.name,
            },
        )

    def get_farm(self, farm_id: str) -> Union[Farm | List[Farm]]:
        if farm_id == '*':
            print(list(self.farms.values()))
            return list(self.farms.values())
        else:
            try:
                return self.farms[farm_id]
            except KeyError:
                raise KeyError(f"Farm '{farm_id}' not found in tenant '{self.id}'")

    def get_mqtt_broker(self, ref: str) -> MqttBroker:
        try:
            return self.mqtt_brokers[ref]
        except KeyError:
            raise KeyError(f"MqttBroker '{ref}' not found in tenant '{self.id}'")

    def register_device_class(self, dc: DeviceClass) -> None:
        if dc.id in self.device_classes:
            raise ValueError(f"Duplicate device class '{dc.id}'")
        self.device_classes[dc.id] = dc

    def get_device_class(self, ref: str) -> DeviceClass:
        try:
            return self.device_classes[ref]
        except KeyError:
            raise KeyError(
                f"DeviceClass '{ref}' not defined in tenant '{self.id}'"
            )

    def register_message_class(self, mc: MessageClass) -> None:
        if mc.id in self.message_classes:
            raise ValueError(f"Duplicate message class '{mc.id}'")
        self.message_classes[mc.id] = mc

    def get_message_class(self, ref: str) -> MessageClass:
        try:
            return self.message_classes[ref]
        except KeyError:
            raise KeyError(
                f"MessageClass '{ref}' not defined in tenant '{self.id}'"
            )

    def __str__(self) -> str:
        return f"Company(id={self.id}, short={self.short_name}, api=v{self.api_version}, farms={len(self.farms)})"
