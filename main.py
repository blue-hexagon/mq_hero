import logging
from pathlib import Path
from pprint import pprint

from src.v2.application.services.tenant_assembler import TenantAssembler
from src.v2.application.services.tenant_config_service import TenantConfigService
from src.v2.infrastructure.config.settings import AppSettings
from src.v2.infrastructure.filesystem.vfs import VirtualFS
from src.v2.infrastructure.loaders.schema_validator import SchemaValidator
from src.v2.infrastructure.loaders.yaml_loader import YamlLoader
from src.v2.application.services.topic_generation_service import TopicGenerationService
from src.v2.domain.entities.registry import DomainRegistry
from src.v2.infrastructure.logging.logger import setup_logging
from dotenv import load_dotenv
import os


def compose():
    tcs = TenantConfigService(
        fs=VirtualFS(
            root=Path("src/v2/")
        ),
        tenant_assembler=TenantAssembler(
            registry=DomainRegistry()
        ),
        yaml_loader=YamlLoader(),
        schema_validator=SchemaValidator(),
    )

    tcs.load()
    return tcs


if __name__ == '__main__':
    load_dotenv()
    settings = AppSettings(
        mqtt_host=os.getenv("MQTT_HOST"),
        mqtt_port=int(os.getenv("MQTT_PORT", 1883)),
        mqtt_username=os.getenv("MQTT_USERNAME"),
        mqtt_password=os.getenv("MQTT_PASSWORD"),
        keep_alive=int(os.getenv("KEEP_ALIVE", 600)),
    )

    setup_logging(
        level=logging.INFO,
        enable_debug_modules=[
            "src.v2.domain.policies",
            "src.v2.infrastructure.mqtt",
            "src.v2.domain.entities.tenant"
        ],
    )

    tenant_config_service = compose()
    registry = tenant_config_service.tenant_assembler.registry

    for ten in registry.iter_tenants():
        topics = TopicGenerationService(tenant=ten)
        for pol in registry.iter_policies(ten.id):
            print(pol)
        print(topics.generate_topics())

    # pex.allow(farm=...,device_class=...,message_class=...,mqtt_direction=MqttDirection.PUB)
    # print(pex.get_rules())
    # TopicFactory(policy=pex)
    # TopicBuilder()
