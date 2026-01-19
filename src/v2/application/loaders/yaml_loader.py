import uuid
from pathlib import Path
from typing import Dict

import yaml

from src.v2.domain.entities.company import Company
from src.v2.domain.entities.device import Device, DeviceClass
from src.v2.domain.entities.farm import Farm
from src.v2.utils.singleton import Singleton


class YamlLoader(metaclass=Singleton):

    def __init__(self, fp: Path = r"C:\Users\T\Desktop\DevProjects\mqtt-test\src\v2\playbooks\msp.yml"):
        self.filepath = Path(fp)

        self.companies: Dict[str, Company] = {}
        self.device_index: Dict[str, Device] = {}
        self.farm_index: Dict[str, Farm] = {}

        self._load()

    """ Public API """
    def get_company(self, key: str) -> Company:
        return self.companies[key]

    def get_farm(self, farm_id: str) -> Farm:
        return self.farm_index[farm_id]

    def get_device(self, device_id: str) -> Device:
        return self.device_index[device_id]

    def all_devices(self):
        return self.device_index.values()

    def all_farms(self):
        return self.farm_index.values()

    def all_companies(self):
        return self.companies.values()

    """ Loading """
    def _load(self):
        if not self.filepath.exists():
            raise FileNotFoundError(self.filepath)

        with open(self.filepath, "rt") as f:
            raw = yaml.safe_load(f)

        self._parse_companies(raw["companies"])

    def _parse_companies(self, companies_cfg: dict):
        for company_key, cfg in companies_cfg.items():
            company = Company(
                id=cfg['short_name'],
                short_name=cfg["short_name"],
                full_name=cfg["full_name"],
                api_version=cfg["api_version"],
                description=cfg.get("description", ""),
            )

            for farm_cfg in cfg.get("farms", []):
                farm = Farm(
                    id=str(uuid.uuid4())[:2] + "_" + farm_cfg['name'],
                    name=farm_cfg["name"],
                    city=farm_cfg["city"],
                )

                for dev_cfg in farm_cfg.get("devices", []):
                    device = Device(
                        id=dev_cfg.get("id"),
                        device_class=DeviceClass(dev_cfg["type"]),
                    )
                    farm.add_device(device)

                    # indexes
                    if device.id in self.device_index:
                        raise ValueError(f"Duplicate device id: {device.id}")

                    self.device_index[device.id] = device

                company.add_farm(farm)
                self.farm_index[farm.id] = farm

            self.companies[company_key] = company

