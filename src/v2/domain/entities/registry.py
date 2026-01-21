from typing import List

from src.v2.domain.entities.device import Device, DeviceClass
from src.v2.domain.entities.farm import Farm
from src.v2.domain.entities.mqtt_message_contract import MessageClass
from src.v2.domain.entities.tenant import Tenant
from src.v2.utils.singleton import Singleton

from typing import Dict

from src.v2.domain.entities.device import Device
from src.v2.domain.entities.farm import Farm
from src.v2.domain.entities.tenant import Tenant


class DomainRegistry:
    """
    DomainRegistry is a read-only coordinator for resolving aggregates
    and navigating across aggregate boundaries.

    It does NOT:
    - Own domain entities
    - Enforce invariants
    - Mutate aggregate internals
    """

    def __init__(self):
        # Aggregate roots ONLY
        self._tenants: Dict[str, Tenant] = {}

    # -------------------------
    # Aggregate root management
    # -------------------------
    def register_tenant(self, tenant: Tenant) -> None:
        if tenant.id in self._tenants:
            raise ValueError(f"Tenant '{tenant.id}' already registered")
        self._tenants[tenant.id] = tenant

    def get_tenant(self, tenant_id: str) -> Tenant:
        try:
            return self._tenants[tenant_id]
        except KeyError:
            raise KeyError(f"Tenant '{tenant_id}' not found")

    def get_tenants(self) -> List[Tenant]:
        return list(self._tenants.values())

    # -------------------------
    # Coordinated traversal
    # -------------------------

    def get_farm(
            self,
            tenant_id: str,
            farm_id: str
    ) -> Farm:
        tenant = self.get_tenant(tenant_id)
        return tenant.get_farm(farm_id)

    def get_device(
            self,
            tenant_id: str,
            farm_id: str,
            device_id: str
    ) -> Device:
        tenant = self.get_tenant(tenant_id)
        farm = tenant.get_farm(farm_id)
        return farm.get_device(device_id)

    def get_device_class(
            self,
            tenant_id: str,
            class_id: str
    ) -> DeviceClass:
        tenant = self.get_tenant(tenant_id)
        return tenant.get_device_class(class_id)

    def get_message_class(
            self,
            tenant_id: str,
            class_id: str
    ) -> MessageClass:
        tenant = self.get_tenant(tenant_id)
        return tenant.get_message_class(class_id)
