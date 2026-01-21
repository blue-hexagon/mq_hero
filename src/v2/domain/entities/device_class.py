from dataclasses import dataclass

from src.v2.domain.topics.topic_segment import TopicSegment


@dataclass(frozen=True, slots=True)
class DeviceClass:
    id: str

    def get_topic_segment(self) -> TopicSegment:
        return TopicSegment(kind="dcls", token=self.id)