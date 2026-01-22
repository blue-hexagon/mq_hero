from src.v2.domain.entities.mqtt_broker import MqttBroker


class RuntimeContext:
    """
    RuntimeContext:\n
    - Holds runtime state and long-lived resources
    - Must be explicitly constructed at the composition root
    - Must never read environment variables
    - Must never contain domain logic
    """
    def __init__(self, settings: MqttBroker):
        self.settings = settings
        self.clients: dict[str, object] = {}

