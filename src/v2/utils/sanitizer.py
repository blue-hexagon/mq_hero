import re


class Sanitizer:
    @staticmethod
    def sanitize_mqtt_topic(topic_str) -> str:
        safe = topic_str.lower()
        safe = re.sub(r'[^a-z0-9_]+', '_', safe)
        return safe
