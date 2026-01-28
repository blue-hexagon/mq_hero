import random
import asyncio
from typing import Dict

from src.v2.application.services.sensor_factory import SensorFactory
from src.v2.infrastructure.iot.sensors.base_sensor import SensorModel


@SensorFactory.register("dht22.py")
class DHT22(SensorModel):

    async def read_metrics(self) -> Dict[str, float]:
        await asyncio.sleep(0.02)

        return {
            "room_temperature": round(random.uniform(18.0, 30.0), 2),
            "room_humidity": round(random.uniform(40.0, 85.0), 2),
        }
