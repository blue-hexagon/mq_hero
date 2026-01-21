import asyncio
import random

from src.v2.domain.sensors.base_sensor import SensorModel


class INA219(SensorModel):
    DEFAULT_INTERVAL = 5

    async def read(self):
        await asyncio.sleep(0.005)
        voltage = round(random.uniform(228, 232), 1)
        current = round(random.uniform(0.2, 2.1), 2)
        return {
            "voltage": voltage,
            "current": current,
            "power": round(voltage * current, 2)
        }
