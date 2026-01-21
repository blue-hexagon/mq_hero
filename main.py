from pprint import pprint

from src.v2.application.loaders.yaml_loader import YamlLoader
from src.v2.domain.entities.registry import DomainRegistry
from src.v2.domain.policies.policy_engine import PolicyEngine
from src.v2.domain.topics.topic_builder import TopicBuilder
from src.v2.domain.topics.topic_factory import TopicFactory
from src.v2.infrastructure.mqtt.types import MqttDirection
from src.v2.utils.store import Store

if __name__ == '__main__':
    store = Store()
    dr = DomainRegistry()
    loader = YamlLoader(domain_registry=dr)
    loader.load()
    pprint(dr.get_tenants(),indent=1)
    pex = PolicyEngine()
    pex.allow(device_class=...,message_class=...,mqtt_direction=MqttDirection.PUB)
    TopicFactory(policy=pex)
    TopicBuilder()
