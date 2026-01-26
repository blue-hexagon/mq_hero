# application/services/tenant_assembler.py
import logging

from src.v2.domain.entities.location import Location
from src.v2.domain.entities.tenant import Tenant
from src.v2.domain.entities.farm import Farm
from src.v2.domain.entities.device import Device, DeviceClass
from src.v2.domain.entities.message_class import MessageClass
from src.v2.domain.errors import LocationDontExists
from src.v2.domain.policies.policy import Policy
from src.v2.domain.entities.registry import DomainRegistry
from src.v2.infrastructure.mqtt.entity.broker import MqttBroker
from src.v2.infrastructure.mqtt.types import MqttDirection


class TenantAssembler:
    """
    Builds domain aggregates from validated tenant configuration.
    """

    def __init__(self, registry: DomainRegistry):
        self.registry = registry

    def assemble(self, tenants_cfg: dict) -> None:
        logger = logging.getLogger(__name__)
        for tenant_key, cfg in tenants_cfg.items():
            tenant = Tenant(
                id=tenant_key,
                short_name=cfg["meta"]["short_name"],
                full_name=cfg["meta"]["full_name"],
                api_version=cfg["meta"]["api_version"],
                description=cfg["meta"].get("description", ""),
            )
            logger.debug(tenant)
            for mqtt_cfg in cfg["meta"]["mqtt"]:
                mqtt_broker = MqttBroker(
                    tenant_id=tenant_key,
                    ref=mqtt_cfg["id"],
                    mqtt_username=mqtt_cfg["username"],
                    mqtt_password=mqtt_cfg["password"],
                    mqtt_host=mqtt_cfg["ipv4"],
                    mqtt_port=mqtt_cfg.get("port", 1883),
                    keepalive=mqtt_cfg["keepalive"]
                )
                logger.debug(mqtt_broker)
                tenant.register_mqtt_broker(mqtt_broker)

            # Device classes
            for dc_id in cfg["definitions"]["device_classes"]:
                dclass = DeviceClass(id=dc_id)
                logger.debug(dclass)
                tenant.register_device_class(dclass)

            # Message classes
            for mc in cfg["definitions"]["message_classes"]:
                msg_class = MessageClass(id=mc["id"], topic=mc["topic"])
                logger.debug(msg_class)
                tenant.register_message_class(msg_class)

            # Tenant Locations
            for loc in cfg["definitions"]["locations"]:
                loca = Location(name=loc['name'], latitude=loc['latitude'], longitude=loc['longitude'])
                logger.debug(loca)
                tenant.register_location(loca)

            self.registry.register_tenant(tenant)

            # Farms and devices
            for farm_cfg in cfg["topology"].get("farms", []):
                farm = Farm(
                    id=farm_cfg["id"],
                    name=farm_cfg["name"],
                    city=farm_cfg["city"],
                )
                logger.debug(farm)
                tenant.register_farm(farm)

                for dev_cfg in farm_cfg.get("devices", []):
                    device_class = tenant.get_device_class(dev_cfg["class"])
                    device_location = None
                    if dev_cfg.get("location"):
                        try:
                            device_location = self.registry.get_location(
                                tenant_id=tenant_key,
                                name=dev_cfg.get("location")
                            )
                        except LocationDontExists as e:
                            raise ReferenceError(e)

                    device = Device(
                        id=dev_cfg["id"],
                        device_class=device_class,
                        driver=dev_cfg.get("driver"),
                        location=device_location,
                        interval=dev_cfg.get("interval"),
                        _farm=farm,
                    )
                    tenant.register_device(farm.id, device)

            # Policies
            for policy_cfg in cfg["policies"]:
                self._expand_policies(tenant, policy_cfg)

    @staticmethod
    def _expand_policies(tenant: Tenant, policy_cfg: dict) -> None:
        policy_name = policy_cfg["name"]
        if policy_cfg["farms"] == ['*']:
            farms = (
                [tenant.get_farm(fid) for fid in tenant.farms]
                if policy_cfg.get("farms")
                else [None]
            )
        else:
            farms = (
                [tenant.get_farm(fid) for fid in policy_cfg["farms"]]
                if policy_cfg.get("farms")
                else [None]
            )

        device_classes = [
            tenant.get_device_class(dc_id)
            for dc_id in policy_cfg["device_classes"]
        ]

        message_classes = [
            tenant.get_message_class(mc_id)
            for mc_id in policy_cfg["message_classes"]
        ]

        direction = MqttDirection[policy_cfg["direction"]]

        for farm in farms:
            for dc in device_classes:
                for mc in message_classes:
                    tenant.register_policy(
                        Policy(
                            name=policy_name,
                            farm=farm,
                            device_class=dc,
                            message_class=mc,
                            direction=direction,
                        )
                    )
