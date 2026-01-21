import random

from src.v2.domain.sensors.base_sensor import SensorModel


class MHZ19B(SensorModel):
    def read(self):
        return {
            "co2": random.randint(420, 1800)
        }
