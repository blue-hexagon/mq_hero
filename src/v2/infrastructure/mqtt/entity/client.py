import json
import logging

import paho.mqtt.client as mqtt

from src.v2.infrastructure.mqtt.entity.broker import MqttBroker


class MqttClient:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.client: mqtt.Client | None = None
        self.broker: MqttBroker | None = None

    def create(self, broker: MqttBroker, client_id: str) -> None:
        client = mqtt.Client(client_id=client_id, clean_session=False)
        client.reconnect_delay_set(min_delay=1, max_delay=30)

        if broker.mqtt_username:
            client.username_pw_set(broker.mqtt_username, broker.mqtt_password)

        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message

        self.client = client
        self.broker = broker

    def connect(self) -> None:
        if not self.client or not self.broker:
            raise RuntimeError("MQTT client not initialized")

        self.client.connect(self.broker.mqtt_host, self.broker.mqtt_port)
        self.client.loop_start()

    def publish(self, topic: str, payload: dict, qos: int = 1, retain: bool = False):
        if not self.client:
            raise RuntimeError("MQTT client not connected")

        self.client.publish(topic, json.dumps(payload), qos=qos, retain=retain)

    def subscribe(self, topic: str, qos: int = 1):
        self.client.subscribe(topic, qos=qos)

    # ---- callbacks ----

    @classmethod
    def on_connect(cls, client, userdata, flags, rc):
        cls.logger.info(f"[MQTT] Connected rc={rc}")

    @classmethod
    def on_disconnect(cls, client, userdata, rc):
        cls.logger.info("[MQTT] Disconnected – retrying")

    @staticmethod
    def on_message(client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
        except Exception:
            data = msg.payload.decode()
        print(f"[MQTT] {msg.topic}: {data}")
