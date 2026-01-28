from typing import Iterable, Optional

from src.v2.domain.entities.device import Device
from src.v2.domain.entities.farm import Farm
from src.v2.domain.entities.message_class import MessageClass
from src.v2.domain.policies.policy import Policy
from src.v2.infrastructure.mqtt.types import MqttDirection


class PolicyEngine:
    """Evaluates whether a concrete action is allowed
    based on atomic policies owned by a tenant.
    """

    def __init__(self, policies: Iterable[Policy]):
        # Snapshot — engine is immutable
        self._rules: tuple[Policy, ...] = tuple(policies)

    def is_allowed(
            self,
            *,
            farm: Optional[Farm],
            device: Device,
            msg_class: MessageClass,
            direction: MqttDirection,
    ) -> bool:

        for rule in self._rules:

            # Device class must match
            if rule.device_class != device.device_class:
                continue

            # Message class must match
            if rule.message_class != msg_class:
                continue

            # Direction must match
            if not (
                    rule.direction == MqttDirection.BOTH
                    or rule.direction == direction
            ):
                continue

            # Farm scoping (None = global)
            if rule.farm is not None and rule.farm != farm:
                continue

            return True

        return False

    def iter_rules(self):
        yield from self._rules
