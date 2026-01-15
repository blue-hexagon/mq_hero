from src.business.farm import Farm, FarmAlreadyExistsWithId


class Company:
    def __init__(self, company_full_name: str, company_short_name: str):
        self.full_name = company_full_name
        self.short_name = company_short_name  # Used for topic building
        self.farms = dict()

    def get_company_topic_str(self) -> str:
        return self.short_name.replace(' ', '_')

    def add_farm(self, farm: Farm):
        if any([i for i in self.farms.keys() if farm.id == i]):
            raise FarmAlreadyExistsWithId("Invalid ID used!")
        self.farms[farm.id] = farm

    def add_farms(self, *farms: [Farm]) -> None:
        [self.add_farm(f) for f in farms]
