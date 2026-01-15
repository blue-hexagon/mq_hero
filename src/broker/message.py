from datetime import datetime
from typing import NamedTuple, Callable

from src.broker.topic import Topic


class Message(NamedTuple):
    topic: Topic
    timestamp: datetime
    qos: int
    retain: bool
    payload: Callable