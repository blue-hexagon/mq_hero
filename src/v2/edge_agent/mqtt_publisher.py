from src.v2.application.services.topic_generation_service import TopicGenerationService
from src.v2.domain.entities.device import Device
from src.v2.infrastructure.mqtt.entity.client import MqttClient


class MqttPublisher:

    def __init__(self, mqtt_client: MqttClient, topic_service: TopicGenerationService):
        self.client = mqtt_client
        self.topic_service = topic_service

    def publish_metric(self, device: Device, payload: dict):
        topic = self.topic_service.metric_topic(device)
        self.client.publish(topic, payload)

    def publish_alert(self, device: Device, payload: dict):
        topic = self.topic_service.alert_topic(device)
        self.client.publish(topic, payload)
