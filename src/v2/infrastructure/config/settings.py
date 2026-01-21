from dataclasses import dataclass


@dataclass(frozen=True)
class AppSettings:
    mqtt_host: str | None
    mqtt_port: int
    mqtt_username: str | None
    mqtt_password: str | None
    keep_alive: int
