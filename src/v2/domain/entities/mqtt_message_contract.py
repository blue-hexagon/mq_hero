from dataclasses import dataclass
from enum import Enum

from src.v2.domain.topics.topic_level import TopicLevel
from src.v2.domain.topics.topic_segment import TopicSegment


@dataclass(frozen=True, slots=True)
class MessageClass:
    id: str
    topic: str

    def get_topic_segment(self) -> TopicSegment:
        return TopicSegment(TopicLevel.MESSAGE_CLASS, self.topic)



