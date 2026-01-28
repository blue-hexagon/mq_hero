import random
import asyncio
from typing import Dict

from src.v2.application.services.sensor_factory import SensorFactory
from src.v2.infrastructure.iot.sensors.base_sensor import SensorModel


@SensorFactory.register("ds18b20.py")
class DS18B20(SensorModel):

    async def read_metrics(self) -> Dict[str, float]:
        await asyncio.sleep(0.02)

        return {
            "soil_temperature": round(random.uniform(18.0, 30.0), 2)
        }
