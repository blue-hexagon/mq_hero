from dataclasses import field, dataclass
from typing import List

from src.v2.domain.entities.farm import Farm
from src.v2.domain.exceptions import FarmAlreadyExistsWithId
from src.v2.domain.topics.topic_level import TopicLevel
from src.v2.domain.topics.topic_segment import TopicSegment


@dataclass
class Company:
    id: str
    short_name: str
    full_name: str
    api_version: int
    description: str
    farms: List[Farm] = field(default_factory=list)

    def topic_segment(self) -> TopicSegment:
        return TopicSegment(TopicLevel.COMPANY, self.id)

    def add_farm(self, farm: Farm) -> None:
        for f in self.farms:
            if f.id == farm.id:
                raise FarmAlreadyExistsWithId("Invalid ID used!")
        self.farms.append(farm)

    def __str__(self) -> str:
        return f"Company(id={self.id}, short={self.short_name}, api=v{self.api_version}, farms={len(self.farms)})"
