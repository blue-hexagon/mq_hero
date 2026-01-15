from typing import Set

from src.data.device import Device

class FarmAlreadyExistsWithId(Exception):
    def __init__(self, message):
        pass


class Farm:
    FARM_LIST = dict()

    def __init__(self, farm_id: str, name: str, city: str) -> None:
        self.id = farm_id
        self.name = name
        self.city = city
        self.devices: Set[Device] = set()


    def add_device(self, device: Device):
        self.devices.add(device)

    def get_device_by_id(self, device_id) -> bool | Device:
        for device in self.devices:
            if device.id == device_id:
                return device
        return False
