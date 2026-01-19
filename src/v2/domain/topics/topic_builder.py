from typing import List, Literal, Union
from typing import TypeVar, Generic

from src.v2.domain.topics.topic_scope import TopicScope
from src.v2.domain.topics.topic_segment import TopicRenderable, TopicSegment

T = TypeVar("T", bound=TopicRenderable)
Wildcard = Literal["+", "#"]
Token = Union[str, Wildcard]


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
