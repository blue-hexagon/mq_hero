from src.v2.domain.entities.device import Device, DeviceClass
from src.v2.domain.entities.message_class import MessageClass

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

    """ Add an iterator only if all of these are true:
        The traversal is structural, not semantic
        It would otherwise be duplicated in multiple places
        It reflects a stable domain relationship
        Its name contains no business language """

    def iter_tenants(self):
        yield from self._tenants.values()

    def iter_policies(self, tenant_id: str):
        yield self.get_tenant(tenant_id)._policies.values()

    def iter_farms(self, tenant_id: str | None = None):
        if tenant_id:
            tenant = self.get_tenant(tenant_id)
            yield from tenant.farms.values()
        else:
            for tenant in self._tenants.values():
                yield from tenant.farms.values()

    def iter_devices(
            self,
            tenant_id: str | None = None,
            farm_id: str | None = None,
    ):
        # Case 1: no filters → all devices
        if tenant_id is None and farm_id is None:
            for tenant in self._tenants.values():
                for farm in tenant.farms.values():
                    yield from farm.devices.values()
            return

        # Case 2: tenant only → all devices in tenant
        if tenant_id is not None and farm_id is None:
            tenant = self.get_tenant(tenant_id)
            for farm in tenant.farms.values():
                yield from farm.devices.values()
            return

        # Case 3: tenant + farm → devices in farm
        if tenant_id is not None and farm_id is not None:
            farm = self.get_farm(tenant_id, farm_id)
            yield from farm.devices.values()
            return

        # Case 4: farm without tenant → invalid
        raise ValueError(
            "farm_id cannot be used without tenant_id "
            "(farm IDs are tenant-scoped)"
        )

    def iter_device_classes(self, tenant_id: str):
        tenant = self.get_tenant(tenant_id)
        yield from tenant.device_classes.values()

    def iter_message_classes(self, tenant_id: str):
        tenant = self.get_tenant(tenant_id)
        yield from tenant.message_classes.values()
