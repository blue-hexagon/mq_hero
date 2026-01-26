import logging

from src.v2.edge_agent.errors import MissingModuleError


class SensorFactory:
    REGISTRY = {}
    logger = logging.getLogger(__name__)
    @classmethod
    def register(cls, model_name: str):
        def decorator(sensor_cls):
            cls.REGISTRY[model_name] = sensor_cls
            return sensor_cls

        return decorator

    @classmethod
    def create(cls, *, device, topics):
        cls.logger.debug(device)
        driver_file = f"{device.driver}.py" # YAML doesn't use filetypes, just a driver name.
        if driver_file not in cls.REGISTRY:
            # import os
            #
            # files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            # f"Available sensors: {}"
            cls.logger.debug(cls.REGISTRY.keys())
            raise MissingModuleError(f"No sensor registered for model '{device.driver}'")

        sensor_cls = cls.REGISTRY[driver_file]

        return sensor_cls(
            device=device,
            device_id=device.id,
            location=device.location,
            topics=topics,
            interval=device.interval,
        )
