from typing import Dict, Any

from src.v2.application.services.sensor_attachment_service import Attachable
from src.v2.infrastructure.iot.attachable import EmitsMetrics, EmitsAlerts


class SensorDht21(Attachable, EmitsMetrics, EmitsAlerts):
    def __init__(self, *, device, device_id, location, topics, interval):
        self.device = device
        self.device_id = device_id
        self.location = location
        self.topics = topics
        self.interval = interval

    async def read_metrics(self) -> Dict[str, Any]:
        pass

    async def read_metrics(self) -> Dict[str, Any]:
        ...