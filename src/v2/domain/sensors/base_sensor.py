# models/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any


class SensorModel(ABC):
    DEFAULT_INTERVAL = 60  # seconds

    def __init__(self, config: Dict[str, Any]):
        self.id = config["id"]
        self.location = config.get("location")

        self.interval = config.get(
            "interval",
            self.DEFAULT_INTERVAL
        )

    @abstractmethod
    async def read(self) -> Dict[str, Any]:
        pass
