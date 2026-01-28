import logging
from enum import Enum
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
import os

BASE_PREFIX = "MQ_HERO"
ROOT_ENV_KEY = "ROLE"
logger = logging.getLogger(__name__)


class RuntimeRole(str, Enum):
    CLIENT = f"{BASE_PREFIX}_CLIENT"
    SERVER = f"{BASE_PREFIX}_SERVER"
    BROKER = f"{BASE_PREFIX}_BROKER"

    @property
    def prefix(self) -> str:
        """ Returns a distinct role-prefix """
        return f"{self.value}"


class RuntimeSettings(BaseSettings):
    runtime_role: RuntimeRole
    debug: bool = False

    model_config = SettingsConfigDict(
        extra="forbid",
        env_nested_delimiter="__",
    )


class ClientRuntimeSettings(RuntimeSettings):
    runtime_role: Literal[RuntimeRole.CLIENT] = RuntimeRole.CLIENT

    model_config = SettingsConfigDict(
        env_prefix=f"{RuntimeRole.CLIENT.prefix}_",
        extra="forbid",
    )


class ServerRuntimeSettings(RuntimeSettings):
    runtime_role: Literal[RuntimeRole.SERVER] = RuntimeRole.SERVER

    model_config = SettingsConfigDict(
        env_prefix=f"{RuntimeRole.SERVER.prefix}_",
        extra="forbid",
    )


class RuntimeContext:
    """
    RuntimeContext:
    - Holds runtime state and long-lived resources
    - Must be explicitly constructed at the composition root
    - Must never read environment variables
    - Must never contain domain logic
    """

    def __init__(self):
        self.settings = load_runtime_settings()
        logger.debug(f"Finished loading runetime_settings and attached it to RunetimeContext")

    def is_client(self) -> bool:
        return self.settings.runtime_role is RuntimeRole.CLIENT

    def is_server(self) -> bool:
        return self.settings.runtime_role is RuntimeRole.SERVER


def load_runtime_settings() -> RuntimeSettings:
    role_raw = os.environ.get(ROOT_ENV_KEY)
    logger.debug(f".env-file key: {ROOT_ENV_KEY} has value: {role_raw}")

    if not role_raw:
        logger.debug(f"Failed to assign role - did you set it?")
        raise RuntimeError("MQ_HERO_ROLE not set")

    try:
        role = RuntimeRole(role_raw)
    except ValueError:
        logger.debug(f"Failed to assign role because of a ValueError - see this file for available roles.")
        raise RuntimeError(f"Invalid MQ_HERO_ROLE: {role_raw}; supported roles: {RuntimeRole.CLIENT.prefix}")

    if role is RuntimeRole.CLIENT:
        logger.debug(f"RuntimeRole={role}")
        return ClientRuntimeSettings()
    if role is RuntimeRole.SERVER:
        logger.debug(f"RuntimeRole={role}")
        return ServerRuntimeSettings()
    raise RuntimeError(f"Unsupported role: {role}")



