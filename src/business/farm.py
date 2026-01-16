import re
from typing import Set, Optional

from src.business.excp import DeviceAlreadyExists
from src.data.device import Device




class Farm:
    FARM_LIST = dict()

    def __init__(self, farm_id: str, name: str, city: str) -> None:
        self.id = farm_id.lower()
        assert re.match(r'^[a-z0-9\-]+$', farm_id)
        self.name = name
        self.city = city
        self.devices: dict[str, Device] = {}

    def topic_root(self, company_topic: str) -> str:
        return f"{company_topic}/{self.id}"
    def add_device(self, device: Device):
        if device.id in self.devices:
            raise DeviceAlreadyExists("TODO")
        self.devices[device.id] = device

    def get_device_by_id(self, device_id) -> Optional[Device]:
        for device in self.devices:
            if device.id == device_id:
                return device
        return None
