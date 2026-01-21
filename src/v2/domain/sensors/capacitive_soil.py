import asyncio
import random

from src.v2.domain.sensors.base_sensor import SensorModel


class CapacitiveSoil(SensorModel):
    DEFAULT_INTERVAL = 300  # 5 min

    async def read(self):
        await asyncio.sleep(0.01)
        return {
            "soil_moisture": random.randint(20, 70)
        }
