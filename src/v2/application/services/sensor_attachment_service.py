from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Protocol

from src.v2.application.services.sensor_factory import SensorFactory
from src.v2.domain.entities.tenant import Tenant
from src.v2.application.services.topic_generation_service import TopicGenerationService
from src.v2.infrastructure.iot.attachable import Attachable

T = TypeVar("T", bound=Attachable)


class AttachmentService(ABC, Generic[T]):
    @abstractmethod
    def attach(self, target: Generic[T]) -> None:
        pass


class DeviceAttachmentService(AttachmentService[Tenant]):

    def attach(self, tenant: Generic[Tenant]):
        topic_service = TopicGenerationService(tenant)
        all_topics = topic_service.generate_topics()

        for farm in tenant.farms.values():
            for device in farm.devices.values():

                if device.device_class.id != "sensor":
                    continue

                device.sensors = []

                topics = [t for t in all_topics if f"/{device.id}/" in t]

                sensor = SensorFactory.create(device=device, topics=topics)
                device.sensors.append(sensor)
