import json
import random

import paho.mqtt.client as mqtt

from src.v2.domain.entities.device import Device
from src.v2.domain.entities.mqtt_broker import MqttBroker
from src.v2.infrastructure.clock.timestamp import TimeStamp


class MqttClient:
    def __init__(self, device: Device) -> None:
        self.device = device
        self.mqtt_client: mqtt.Client | None = None
        self.mqtt_broker: MqttBroker | None = None

    def create_client(self, broker: MqttBroker) -> mqtt.Client:
        mqtt_client = mqtt.Client(client_id=self.device.id, clean_session=False)
        mqtt_client.reconnect_delay_set(min_delay=1, max_delay=30)
        if broker.mqtt_username:
            mqtt_client.username_pw_set(
                broker.mqtt_username,
                broker.mqtt_password
            )
        mqtt_client.on_connect = MqttClient.on_connect
        mqtt_client.on_disconnect = MqttClient.on_disconnect
        mqtt_client.on_message = MqttClient.on_message

        self.mqtt_client = mqtt_client
        self.mqtt_broker = broker
        return mqtt_client

    def connect(self) -> bool | Exception:
        if self.mqtt_client is None:
            raise RuntimeError("MQTT Client has not been initialized!")

        self.mqtt_client.connect(self.mqtt_broker.mqtt_host, self.mqtt_broker.mqtt_port)
        self.mqtt_client.loop_start()
        return True

    def pub(self) -> None:
        while True:
            payload = {
                "sensor_id": self.device.id,
                "ts": TimeStamp.get_utc_isof(),
                "soil_moisture": round(random.uniform(20, 60), 2),
                "temperature": round(random.uniform(10, 30), 2),
                "battery": round(random.uniform(3.5, 4.2), 2)
            }

            self.mqtt_client.publish("topic", json.dumps(payload), qos=1, retain=False)

    def sub(self, topic):
        self.mqtt_client.subscribe(topic, qos=1)

    @staticmethod
    def on_connect(client: mqtt.Client, userdata, flags, rc):  # noqa
        print(f"[+] Connected:", rc)

    @staticmethod
    def on_disconnect(client: mqtt.Client, userdata, rc):  # noqa
        print("[!] Disconnected – retrying")

    @staticmethod
    def on_message(client, userdata, msg):  # noqa
        data = json.loads(msg.payload.decode())
        print(f"[/] {msg.topic}: {data}")
