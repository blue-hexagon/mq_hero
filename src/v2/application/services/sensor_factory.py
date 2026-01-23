from src.v2.application.services.topic_generation_service import TopicGenerationService
from src.v2.domain.entities.tenant import Tenant


class SensorFactory:
    REGISTRY = {}

    @classmethod
    def register(cls, model_name: str):
        def decorator(sensor_cls):
            cls.REGISTRY[model_name] = sensor_cls
            return sensor_cls
        return decorator

    @classmethod
    def create(cls, *, device, topics):
        if device.model not in cls.REGISTRY:
            raise ValueError(f"No sensor registered for model '{device.model}'")

        sensor_cls = cls.REGISTRY[device.model]

        return sensor_cls(
            device=device,
            device_id=device.id,
            location=device.location,
            topics=topics,
            interval=device.interval,
        )

