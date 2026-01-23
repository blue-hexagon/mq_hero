import asyncio
import random
from typing import Dict

from src.v2.application.services.sensor_factory import SensorFactory
from src.v2.infrastructure.iot.sensors.base_sensor import SensorModel


@SensorFactory.register("capacitive_soil.py")
class CapacitiveSoil(SensorModel):
    LOW = 25.0
    HIGH = 65.0

    async def read_metrics(self) -> Dict[str, float]:
        await asyncio.sleep(0.01)
        return {
            "soil_moisture": float(random.randint(20, 70))
        }

    async def check_alerts(self, metrics: Dict[str, float]) -> list[dict]:
        alerts = []
        value = float(metrics.get("soil_moisture", 0.0))

        if value < self.LOW:
            alerts.append({
                "type": "soil_moisture_low",
                "metric": "soil_moisture",
                "value": value,
                "threshold": self.LOW,
                "severity": "warning",
            })

        elif value > self.HIGH:
            alerts.append({
                "type": "soil_moisture_high",
                "metric": "soil_moisture",
                "value": value,
                "threshold": self.HIGH,
                "severity": "critical",
            })

        return alerts
