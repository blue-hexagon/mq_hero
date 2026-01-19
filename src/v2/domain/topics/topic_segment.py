from dataclasses import dataclass
from typing import Protocol

from src.v2.domain.topics.topic_level import TopicLevel


@dataclass(frozen=True)
class TopicSegment:
    level: TopicLevel
    token: str  # concrete id | "+" | "#"

    def __post_init__(self):
        if self.token == "#":
            return

        if self.token == "+":
            return

        # concrete identifier validation
        if "/" in self.token or "+" in self.token or "#" in self.token:
            raise ValueError(f"Invalid topic token: {self.token}")

        if not self.token:
            raise ValueError("Token must not be empty")

    @property
    def is_wildcard(self) -> bool:
        return self.token in ("+", "#")

    @property
    def is_recursive(self) -> bool:
        return self.token == "#"


class TopicRenderable(Protocol):
    def topic_segment(self) -> "TopicSegment": ...
