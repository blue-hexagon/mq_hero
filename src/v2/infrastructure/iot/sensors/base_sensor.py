from abc import ABC, abstractmethod
from typing import Dict, Any, List
import time

from src.v2.domain.entities.device import Device
from src.v2.domain.entities.location import Location


class SensorModel(ABC):

    def __init__(self, *, device: Device, device_id: str, location: Location, topics: List[str], interval: int):
        self.device = device
        self.device_id = device_id
        self.location = location
        self.topics = topics
        self.interval = interval

    # ---------- Metrics ----------

    @abstractmethod
    async def read_metrics(self) -> Dict[str, Any]:
        """Return metric_name -> value"""
        pass

    async def read(self) -> Dict[str, Any]:
        """Return standardized metric payload"""

        metrics = await self.read_metrics()
        ts = int(time.time())

        return {
            "schema": "sensor.metric.v1",
            "ts": ts,
            "device_id": self.device_id,
            "location": self._location_payload(),
            "metrics": metrics,
        }

    # ---------- Alerts ----------

    async def check_alerts(self, metrics: Dict[str, Any]) -> List[dict]:
        """Return list of alert objects. Default: no alerts."""
        return []

    def build_alert_payload(self, alert: dict, ts: int) -> Dict[str, Any]:
        """Build standardized alert payload"""

        return {
            "schema": "sensor.alert.v1",
            "ts": ts,
            "device_id": self.device_id,
            "location": self._location_payload(),
            "alert": alert,
        }

    # ---------- Helpers ----------

    def _location_payload(self) -> dict:
        return {
            "farm": self.location.name.split(".")[0],
            "area": self.location.name.split(".")[1],
            "lat": self.location.latitude,
            "lng": self.location.longitude,
        }
