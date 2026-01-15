from enum import Enum
from typing import Set

from src.app_store import Store
from src.data.device import Device
from src.business.farm import Farm


class RootTopic:


class DeviceCategory(Enum):
    MACHINE = "machines"
    SENSOR = "sensors"
    DRONE = "drones"


class TopicCategory(Enum):
    DATA = "data"
    STATUS = "status"
    ALERT = "alert"
    COMMAND = "cmd"
    IMAGE = "image"
    TELEMETRY = "telemetry"


class TopicBuilder:
    """
    Format:
        company/farm/device_type/device_id/topic
        company: AgriTech|RingstedIT
        farm: FarmID
        device_type: Drone, Machine, Sensor
    """

    def __init__(self, company_name: str, farms: Set[Farm] | None) -> None:
        self.company_name = company_name
        self.farms = farms

    def add_farm(self, farm: Farm) -> str:
        self.farms.add(farm)
        return farm.id

    def add_device(self, farm_id: str, device: Device):
        ...

    @staticmethod
    def _base(device_type: str, device_id: str) -> str:
        return f"{Store.COMPANY_NAME}/{Store.FARM_ID}/{device_type}/{device_id}"

    # ---------- Sensors ----------

    @staticmethod
    def sensor_data(device: Device) -> str:
        return f"{Topic._base('sensors', device.id)}/{TopicCategory.DATA.value}"

    @staticmethod
    def sensor_status(device: Device) -> str:
        return f"{Topic._base('sensors', device.id)}/{TopicCategory.STATUS.value}"

    @staticmethod
    def sensor_alerts(device: Device) -> str:
        return f"{Topic._base('sensors', device.id)}/{TopicCategory.ALERT.value}"

    @staticmethod
    def sensor_command(device: Device) -> str:
        return f"{Topic._base('sensors', device.id)}/{TopicCategory.COMMAND.value}"

    # ---------- Drones ----------

    @staticmethod
    def drone_image(drone_id: str) -> str:
        return f"{Topic._base('drones', drone_id)}/{TopicCategory.IMAGE.value}"

    @staticmethod
    def drone_telemetry(drone_id: str) -> str:
        return f"{Topic._base('drones', drone_id)}/{TopicCategory.TELEMETRY.value}"

    @staticmethod
    def drone_status(drone_id: str) -> str:
        return f"{Topic._base('drones', drone_id)}/{TopicCategory.STATUS.value}"

    # ---------- Machines ----------

    @staticmethod
    def machine_telemetry(machine_id: str) -> str:
        return f"{Topic._base('machines', machine_id)}/{TopicCategory.TELEMETRY.value}"

    @staticmethod
    def machine_status(machine_id: str) -> str:
        return f"{Topic._base('machines', machine_id)}/{TopicCategory.STATUS.value}"

    # ---------- Subscriptions (backend / dashboards) ----------

    @staticmethod
    def all_farm() -> str:
        """Subscribe to everything from one farm"""
        return f"{Store.COMPANY_NAME}/{Store.FARM_ID}/#"

    @staticmethod
    def all_sensors() -> str:
        return f"{Store.COMPANY_NAME}/{Store.FARM_ID}/{DeviceCategory.SENSOR.value}/+/{TopicCategory.DATA.value}"

    @staticmethod
    def all_status() -> str:
        return f"{Store.COMPANY_NAME}/{Store.FARM_ID}/+/+/{TopicCategory.STATUS.value}"

    @staticmethod
    def all_alerts() -> str:
        return f"{Store.COMPANY_NAME}/{Store.FARM_ID}/+/+/{TopicCategory.ALERT.value}"

    @staticmethod
    def everything_all_farms() -> str:
        """For central backend"""
        return f"{Store.COMPANY_NAME}/+/+/+/+"
