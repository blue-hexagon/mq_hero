import re

from src.business.company import Company
from src.business.excp import CompanyAlreadyExists
from src.hero.singleton import Singleton


class EnterpriseManager(metaclass=Singleton):
    def __init__(self, msp_name: str):
        self.msp_name = msp_name
        self.companies = dict()

    def get_company(self, short_name: str):
        return

    def topic_root(self) -> str:
        safe = self.msp_name.lower()
        safe = re.sub(r'[^a-z0-9_]+', '_', safe)
        return f"{safe.strip('_')}/"

    def add_company(self, new_company: Company):
        for existing_company in self.companies:
            if new_company.short_name == existing_company.short_name:
                raise CompanyAlreadyExists("Invalid short_name: already exists!")
        self.companies[new_company.short_name] = new_company
