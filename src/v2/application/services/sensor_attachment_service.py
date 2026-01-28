from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from src.v2.application.services.sensor_factory import SensorFactory
from src.v2.domain.entities.tenant import Tenant
from src.v2.application.services.topic_generation_service import TopicGenerationService
from src.v2.infrastructure.iot.attachable import Attachable

T_Attachable = TypeVar("T_Attachable", bound=Attachable)


class AttachmentService(Generic[T_Attachable], ABC):
    """ Attaches an 'attachable' to a DeviceClass """

    @abstractmethod
    async def attach(self, target: T_Attachable) -> None:
        """Attach runtime behavior to the target"""
        ...

    @abstractmethod
    async def detach(self, target: T_Attachable) -> None:
        """Optional: clean up behavior"""
        pass


# class DeviceAttachmentService(AttachmentService[Tenant]):
class ModuleAttachmentService():

    def attach_modules(self, tenant: Tenant):  # noqa; TODO:
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
