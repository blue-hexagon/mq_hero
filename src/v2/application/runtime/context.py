from src.v2.infrastructure.config.settings import AppSettings


class RuntimeContext:
    """
    RuntimeContext:\n
    - Holds runtime state and long-lived resources
    - Must be explicitly constructed at the composition root
    - Must never read environment variables
    - Must never contain domain logic
    """
    def __init__(self, settings: AppSettings):
        self.settings = settings
        self.clients: dict[str, object] = {}