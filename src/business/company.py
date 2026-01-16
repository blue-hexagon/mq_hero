import re
from typing import Optional

from src.business.excp import FarmAlreadyExistsWithId
from src.business.farm import Farm


class Company:
    def __init__(self, full_name: str, short_name: str, api_version: int = 1):
        self.description = None
        self.full_name = full_name
        self.short_name = short_name  # Used for topic building
        self.farms = dict()
        self.api_version = api_version

    def topic_root(self) -> str:
        safe = self.short_name.lower()
        safe = re.sub(r'[^a-z0-9_]+', '_', safe)
        return f"{safe.strip('_')}/v{self.api_version}"

    def add_farm(self, farm: Farm):
        if farm.id in self.farms:
            raise FarmAlreadyExistsWithId("Invalid ID used!")
        self.farms[farm.id] = farm
        return self

