import logging
from pathlib import Path

from src.v2.application.services.sensor_attachment_service import ModuleAttachmentService
from src.v2.application.services.tenant_assembler import TenantAssembler
from src.v2.application.services.tenant_config_service import TenantConfigService
from src.v2.application.services.topic_generation_service import TopicGenerationService

from src.v2.domain.entities.registry import DomainRegistry
from src.v2.edge_agent.device_runner import DeviceRunner
from src.v2.edge_agent.farm_runner import FarmRunner
from src.v2.edge_agent.mqtt_publisher import MqttPublisher
from src.v2.edge_agent.runtime import TenantRuntime
from src.v2.edge_agent.scheduler import SensorScheduler

from src.v2.infrastructure.filesystem.vfs import VirtualFS
from src.v2.infrastructure.loaders.schema_validator import SchemaValidator
from src.v2.infrastructure.loaders.yaml_loader import YamlLoader
from src.v2.infrastructure.mqtt.entity.client import MqttClient
from src.v2.edge_agent.imports import *  # noqa


def build_mqtt_client(tenant) -> MqttClient:
    broker = next(iter(tenant.mqtt_brokers.values()))

    client = MqttClient()
    client.create(broker, client_id="test")
    client.connect()

    return client


class BootstrapClient:
    @staticmethod
    async def bootstrap(tenant_id: str):
        service = TenantConfigService(
            fs=VirtualFS(Path(".")),
            tenant_assembler=TenantAssembler(DomainRegistry()),
            yaml_loader=YamlLoader(),
            schema_validator=SchemaValidator(),
        )
        logger = logging.getLogger(__name__)
        logger.debug("TenantConfigService instantiated")

        service.load()

        tenant = BootstrapClient.resolve_tenant(
            registry=service.tenant_assembler.registry,
            tenant_id=tenant_id
        )
        mas = ModuleAttachmentService()
        mas.attach_modules(tenant)

        mqtt_client = build_mqtt_client(tenant)
        print(mqtt_client)

        topic_service = TopicGenerationService(tenant)
        logger.debug(topic_service)
        publisher = MqttPublisher(mqtt_client, topic_service)

        scheduler = SensorScheduler(publisher)
        device_runner = DeviceRunner(scheduler)
        farm_runner = FarmRunner(device_runner)
        runtime = TenantRuntime(farm_runner)

        await runtime.run(tenant)

    @staticmethod
    def resolve_tenant(registry, tenant_id: str | None = None):
        tenants = list(registry.iter_tenants())

        if not tenants:
            raise RuntimeError("No tenants registered")

        if tenant_id is None:
            if len(tenants) != 1:
                raise RuntimeError(
                    f"Multiple tenants present ({len(tenants)}), but no tenant_id provided"
                )
            return tenants[0]

        for tenant in tenants:
            if tenant.id == tenant_id:
                return tenant

        raise KeyError(f"Tenant '{tenant_id}' not found")
