from src.v2.domain.entities.device import Device
from src.v2.domain.entities.location import Location
from typing import Protocol, Dict, Any, List


class Attachable(Protocol):
    device: Device
    device_id: str
    location: Location
    topics: List[str]


class EmitsMetrics(Protocol):
    interval: int

    async def read_metrics(self) -> Dict[str, Any]:
        ...

class EmitsAlerts(Protocol):
    async def check_alerts(self, metrics: Dict[str, Any]) -> list[dict]:
        ...
class AcceptsCommands(Protocol):
    async def execute(self, command: str, payload: dict) -> None:
        ...
class Mobile(Protocol):
    async def move_to(self, location: Location) -> None:
        ...

    async def get_position(self) -> Location:
        ...