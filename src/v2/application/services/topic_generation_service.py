import functools
import logging
import re
from pprint import pprint
from time import sleep
from typing import Iterable

from src.v2.domain.entities.tenant import Tenant
from src.v2.domain.topics.topic import TopicScope
from src.v2.domain.topics.topic_segment import TopicSegment
from src.v2.infrastructure.mqtt.message_contract import MqttMessageContract
from src.v2.infrastructure.mqtt.types import MqttDirection

TOKEN_PATTERN = re.compile(r"^[a-z0-9_-]+$")


class TopicGenerationService:
    DEFAULT_ORDER = [
        "tenant",
        "farm",
        "dcls",
        "device",
        "message",
    ]

    def __init__(self, tenant: Tenant):
        self._tenant = tenant
        self._topic_order = getattr(tenant, "topic_order", self.DEFAULT_ORDER)

    def build(self, segments: Iterable[TopicSegment]) -> str:
        segments = list(segments)

        self._validate_required_segments(segments)
        ordered = self._order_segments(segments)
        self._validate_wildcards(ordered)

        return "/".join(seg.token for seg in ordered)

    @staticmethod
    def _validate_required_segments(segments: list[TopicSegment]) -> None:
        required = {"tenant", "farm", "device", "message"}
        present = {s.kind for s in segments}

        missing = required - present
        if missing:
            raise ValueError(f"Missing topic segments: {missing}")

    @staticmethod
    def _validate_wildcards(segments: list[TopicSegment]) -> None:
        for i, seg in enumerate(segments):
            if seg.token == "#" and i != len(segments) - 1:
                raise ValueError("# wildcard must be last segment")

    @staticmethod
    def _validate(segments: list[TopicSegment]) -> None:
        for i, seg in enumerate(segments):

            # Recursive wildcard must be last
            if seg.token == "#" and i != len(segments) - 1:
                raise ValueError("# wildcard must be last segment")

            # Wildcards are otherwise valid
            if seg.token in ("+", "#"):
                continue

            # Validate concrete token
            if not TOKEN_PATTERN.fullmatch(seg.token):
                raise ValueError(
                    f"Invalid token '{seg.token}': "
                    "must match ^[a-z0-9_-]+$"
                )

    def _order_segments(self, segments: Iterable[TopicSegment]) -> list[TopicSegment]:
        logging.getLogger(__name__).debug(msg=segments)
        order = {k: i for i, k in enumerate(self._topic_order)}
        return sorted(
            segments,
            key=lambda s: order.get(s.kind, 999)
        )

    @staticmethod
    def apply_scope(base: TopicSegment, scope: TopicScope) -> TopicSegment:
        if scope is TopicScope.SINGLE:
            return base
        if scope is TopicScope.ALL:
            return TopicSegment(base.kind, "+")
        if scope is TopicScope.ALL_RECURSIVE:
            return TopicSegment(base.kind, "#")
        raise ValueError("Invalid scope")

    @functools.lru_cache
    def generate_topics(self) -> list[str]:
        topics = []

        for farm in self._tenant.farms.values():
            for device in farm.devices.values():
                for message_class in self._tenant.message_classes.values():
                    if not (self._tenant.policy_engine().is_allowed(
                            farm=farm,
                            device=device,
                            msg_class=message_class,
                            direction=MqttDirection.PUB)):
                        logger = logging.getLogger(__name__)
                        logger.debug("topic disallowed")
                        continue
                    contract = MqttMessageContract(
                        message_class=message_class,
                        direction=MqttDirection.PUB,
                    )

                    segments = [
                        self.apply_scope(self._tenant.get_topic_segment(), TopicScope.SINGLE),
                        self.apply_scope(farm.get_topic_segment(), TopicScope.SINGLE),
                        self.apply_scope(device.device_class.get_topic_segment(), TopicScope.SINGLE),
                        self.apply_scope(device.get_topic_segment(), TopicScope.SINGLE),
                        self.apply_scope(contract.get_topic_segment(), TopicScope.SINGLE),
                    ]
                    topics.append(self.build(segments))

        return topics
