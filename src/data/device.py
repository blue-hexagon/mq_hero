import uuid
from collections import namedtuple
from typing import Callable

from src.app_store import Store
from src.broker.topic import TopicCategory


class Device:
    def __init__(self, device_id: str, category: DeviceCategory):
        if device_id:
            if len(device_id) >= Store.settings.DEVICE_NAME_LEN_MAX:
                raise ValueError("Device ID length exceeded")
            self.id = device_id

        if self.id is None:
            self.id = str(uuid.uuid4())[:Store.settings.DEVICE_NAME_LEN_MAX]

        self.category = category
        self.topics = set()
        self.messages = namedtuple("message", ["topic", "datasource"])

    def add_message(self, topic: TopicCategory, datasource: Callable):
        self.messages()
        self.topics.add(topic)

    def list_topics(self):
        print([t for t in self.topics])
