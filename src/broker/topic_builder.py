from dataclasses import dataclass
from enum import Enum
from typing import Protocol, List, Literal, Union
from typing import TypeVar, Generic


class TopicRenderable(Protocol):
    def topic_segment(self) -> "TopicSegment": ...


T = TypeVar("T", bound=TopicRenderable)
Wildcard = Literal["+", "#"]
Token = Union[str, Wildcard]


class TopicScope(Enum):
    SINGLE = "single"
    ALL = "all"
    ALL_RECURSIVE = "recursive"


class TopicLevel(Enum):
    MSP = "msp_id"
    COMPANY = "company_id"
    FARM = "farm_id"
    DEVICE_CLASS = "device_class"
    DEVICE = "device_id"
    MESSAGE_TYPE = "message_type"


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

class TopicBuilder(Generic[T]):
    def __init__(self):
        self.segments: List[TopicSegment] = []

    def validate(self):
        for i, seg in enumerate(self.segments):
            if seg.token == "#" and i != len(self.segments) - 1:
                raise ValueError("# wildcard must be last segment")

    def build(self) -> str:
        self.validate()
        return "/".join(seg.token for seg in self.segments)

    def add(self, scope: TopicScope, entity: T) -> "TopicBuilder":
        base = entity.topic_segment()  # TopicSegment(level, token)

        if scope is TopicScope.SINGLE:
            self.segments.append(base)

        elif scope is TopicScope.ALL:
            self.segments.append(
                TopicSegment(base.level, "+")
            )

        elif scope is TopicScope.ALL_RECURSIVE:
            self.segments.append(
                TopicSegment(base.level, "#")
            )

        else:
            raise ValueError("Invalid TopicScope")

        return self


