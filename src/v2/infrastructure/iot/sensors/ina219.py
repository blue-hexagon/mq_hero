import asyncio
import random

from src.v2.application.services.sensor_factory import SensorFactory
from src.v2.infrastructure.iot.sensors.base_sensor import SensorModel

@SensorFactory.register("ina219.py")
class INA219(SensorModel):

    async def read_metrics(self):
        await asyncio.sleep(0.005)
        voltage = round(random.uniform(228, 232), 1)
        current = round(random.uniform(0.2, 2.1), 2)
        return {
            "voltage": voltage,
            "current": current,
            "power": round(voltage * current, 2)
        }
