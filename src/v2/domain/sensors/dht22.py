# models/dht22.py
import random
import asyncio

from src.v2.domain.sensors.base_sensor import SensorModel


class DHT22(SensorModel):
    DEFAULT_INTERVAL = 60

    async def read(self):
        await asyncio.sleep(0.02)
        return {
            "temperature": round(random.uniform(18.0, 30.0), 2),
            "humidity": round(random.uniform(40.0, 85.0), 2)
        }
