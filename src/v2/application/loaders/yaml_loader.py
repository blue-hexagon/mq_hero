import uuid
from pathlib import Path
from typing import Dict

import yaml

from src.v2.domain.entities.registry import DomainRegistry
from src.v2.domain.entities.tenant import Tenant
from src.v2.domain.entities.device import Device, DeviceClass
from src.v2.domain.entities.farm import Farm
from src.v2.utils.singleton import Singleton
import yaml
from jsonschema import Draft202012Validator



class YamlLoader:

    def __init__(self, domain_registry: DomainRegistry,
                 fp: Path = r"C:\Users\T\Desktop\DevProjects\mqtt-test\src\v2\playbooks\tenants.yml"):
        self.filepath = Path(fp)

        self.tenants: Dict[str, Tenant] = {}
        self.device_index: Dict[str, Device] = {}
        self.farm_index: Dict[str, Farm] = {}
        self.registry = domain_registry

    def verify_yaml(path: str) -> dict:
        with open(path, "r") as f:
            schema = yaml.safe_load("schemas/tenant.schema.yaml")
            validator = Draft202012Validator(schema)

            errors = sorted(
                validator.iter_errors(config),
                key=lambda e: e.path
            )

            if errors:
                for error in errors:
                    print(f"Schema error at {list(error.path)}:")
                    print(f"  {error.message}")
                raise ValueError("Invalid tenant configuration")

    def get_tenant(self, key: str) -> Tenant:
        return self.tenants[key]

    def get_farm(self, farm_id: str) -> Farm:
        return self.farm_index[farm_id]

    def get_device(self, device_id: str) -> Device:
        return self.device_index[device_id]

    def all_devices(self):
        return self.device_index.values()

    def all_farms(self):
        return self.farm_index.values()

    def all_tenants(self):
        return self.tenants.values()

    """ Loading """

    def load(self):
        if not self.filepath.exists():
            raise FileNotFoundError(self.filepath)

        with open(self.filepath, "rt") as f:
            raw = yaml.safe_load(f)

        self._parse_tenants(raw["tenants"])

    def _parse_tenants(self, tenants_cfg: dict):
        for tenant_key, cfg in tenants_cfg.items():
            tenant = Tenant(
                id=cfg['short_name'],
                short_name=cfg["short_name"],
                full_name=cfg["full_name"],
                api_version=cfg["api_version"],
                description=cfg.get("description", ""),
            )
            self.registry.register_tenant(tenant)
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
                    farm._add_device(device)

                    # indexes
                    if device.id in self.device_index:
                        raise ValueError(f"Duplicate device id: {device.id}")

                    self.device_index[device.id] = device

                tenant.add_farm(farm)
                self.farm_index[farm.id] = farm

            self.tenants[tenant_key] = tenant
