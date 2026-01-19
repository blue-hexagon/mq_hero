import os

from dotenv import load_dotenv

load_dotenv()


class AppSettings:
    DEVICE_NAME_LEN_MAX = 8


class Store:
    MQTT_HOST = os.getenv("MQTT_HOST")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
    MQTT_USERNAME = os.getenv("MQTT_USERNAME")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

    KEEP_ALIVE = os.getenv("KEEP_ALIVE", 600)

    ENV = os.getenv("ENV", "dev")
    settings = AppSettings
    if ENV == "dev":
        print("[i] Running in development mode.")
