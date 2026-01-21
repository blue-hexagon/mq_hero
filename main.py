import logging
from pprint import pprint

from src.v2.infrastructure.config.settings import AppSettings
from src.v2.infrastructure.loaders.yaml_loader import YamlLoader
from src.v2.application.services.topic_generation_service import TopicGenerationService
from src.v2.domain.entities.registry import DomainRegistry
from src.v2.infrastructure.logging.logger import setup_logging
from dotenv import load_dotenv
import os

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

    dom_reg = DomainRegistry()
    loader = YamlLoader(domain_registry=dom_reg,)
    loader.load()

    for ten in dom_reg.iter_tenants():
        topics = TopicGenerationService(tenant=ten)
        for pol in dom_reg.iter_policies(ten.id):
            pprint(pol, indent=1)
        pprint(topics.generate_topics())

    #
    # pex.allow(farm=...,device_class=...,message_class=...,mqtt_direction=MqttDirection.PUB)
    # print(pex.get_rules())
    # TopicFactory(policy=pex)
    # TopicBuilder()
