import random

from src.v2.application.services.sensor_factory import SensorFactory
from src.v2.infrastructure.iot.sensors.base_sensor import SensorModel


@SensorFactory.register("mh_z19b.py")
class MHZ19B(SensorModel):
    async def read_metrics(self):
        return {
            "co2": random.randint(420, 1800)
        }
