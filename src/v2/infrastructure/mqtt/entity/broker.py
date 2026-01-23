from dataclasses import dataclass


@dataclass(frozen=True, repr=False)
class MqttBroker:
    tenant_id: str
    ref: str
    mqtt_host: str | None
    mqtt_port: int
    mqtt_username: str | None
    mqtt_password: str | None
    keepalive: int

    def __repr__(self) -> str:
        return (
            f"MqttBroker(ref={self.ref}, host={self.mqtt_host}, "
            f"port={self.mqtt_port}, user={self.mqtt_username}, "
            f"password=***, keepalive={self.keepalive})"
        )
