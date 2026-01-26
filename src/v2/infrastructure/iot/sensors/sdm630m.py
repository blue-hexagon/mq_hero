import random
import asyncio
from typing import Dict

from src.v2.application.services.sensor_factory import SensorFactory
from src.v2.infrastructure.iot.sensors.base_sensor import SensorModel


@SensorFactory.register("sdm630m.py")
class SDM630M(SensorModel):

    async def read_metrics(self) -> Dict[str, float]:
        await asyncio.sleep(0.02)

        return {
            "temperature": round(random.uniform(18.0, 30.0), 2),
            "humidity": round(random.uniform(40.0, 85.0), 2),
        }
