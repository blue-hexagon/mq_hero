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
            "amperage": round(random.uniform(1.0, 80.0), 2),
            "voltage": round(random.uniform(385.0, 415.0), 2),
            "wattage": round(random.uniform(1.0, 60000.0), 2),
        }
