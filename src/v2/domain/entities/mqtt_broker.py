from dataclasses import dataclass


@dataclass(frozen=True)
class MqttBroker:
    tenant_id: str
    ref: str
    mqtt_host: str | None
    mqtt_port: int
    mqtt_username: str | None
    mqtt_password: str | None
    keepalive: int
