from dataclasses import field, dataclass
from typing import List

from src.v2.domain.entities.device import Device, DeviceClass
from src.v2.domain.entities.farm import Farm
from src.v2.domain.entities.mqtt_message_contract import MessageClass
from src.v2.domain.topics.topic_level import TopicLevel
from src.v2.domain.topics.topic_segment import TopicSegment


@dataclass
class Tenant:
    id: str
    short_name: str
    full_name: str
    api_version: int
    description: str
    farms: dict[str, Farm] = field(default_factory=dict)
    _device_classes: dict[str, DeviceClass] = field(default_factory=dict)
    _message_classes: dict[str, MessageClass] = field(default_factory=dict)

    def get_topic_segment(self) -> TopicSegment:
        return TopicSegment(TopicLevel.TENANT, self.id)

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

    def get_farm(self, farm_id: str) -> Farm:
        try:
            return self.farms[farm_id]
        except KeyError:
            raise KeyError(f"Farm '{farm_id}' not found in tenant '{self.id}'")

    def register_device_class(self, dc: DeviceClass) -> None:
        if dc.id in self._device_classes:
            raise ValueError(f"Duplicate device class '{dc.id}'")
        self._device_classes[dc.id] = dc

    def get_device_class(self, id: str) -> DeviceClass:
        try:
            return self._device_classes[id]
        except KeyError:
            raise KeyError(
                f"DeviceClass '{id}' not defined in tenant '{self.id}'"
            )

    def register_message_class(self, mc: MessageClass) -> None:
        if mc.id in self._message_classes:
            raise ValueError(f"Duplicate message class '{mc.id}'")
        self._message_classes[mc.id] = mc

    def get_message_class(self, id: str) -> MessageClass:
        try:
            return self._message_classes[id]
        except KeyError:
            raise KeyError(
                f"MessageClass '{id}' not defined in tenant '{self.id}'"
            )
    def __str__(self) -> str:
        return f"Company(id={self.id}, short={self.short_name}, api=v{self.api_version}, farms={len(self.farms)})"
