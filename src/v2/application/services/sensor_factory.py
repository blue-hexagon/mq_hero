from src.v2.edge_agent.errors import MissingModuleError


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
            # import os
            #
            # files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            # f"Available sensors: {}"
            raise MissingModuleError(f"No sensor registered for model '{device.model}'")

        sensor_cls = cls.REGISTRY[device.model]

        return sensor_cls(
            device=device,
            device_id=device.id,
            location=device.location,
            topics=topics,
            interval=device.interval,
        )
