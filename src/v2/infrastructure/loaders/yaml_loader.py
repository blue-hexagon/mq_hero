from pathlib import Path

import yaml
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from jsonschema import Draft202012Validator

from src.v2.domain.entities.message_class import MessageClass
from src.v2.domain.entities.registry import DomainRegistry
from src.v2.domain.entities.tenant import Tenant
from src.v2.domain.entities.device import Device, DeviceClass
from src.v2.domain.entities.farm import Farm
from src.v2.domain.policies.policy import Policy
from src.v2.infrastructure.mqtt.types import MqttDirection


class YamlLoader:
    """
    Boundary adapter:
    YAML → validated structure → domain aggregates
    """

    def __init__(
            self,
            domain_registry: DomainRegistry,
            config_path: Path = Path(Store().settings.PROJECT_ROOT + r"/src/v2/playbooks/tenants.yml"),
            schema_path: Path = Path(Store().settings.PROJECT_ROOT + r"/src/v2/schemas/tenant.schema.yaml"),
    ):
        self.config_path = Path(config_path)
        self.schema_path = Path(schema_path)
        self.registry = domain_registry

    # -------------------------
    # Public API
    # -------------------------
    def load(self) -> None:
        # Load twice: once for structure, once for locations
        source_tree = self._load_yaml_with_locations(self.config_path)
        config = self._load_yaml_plain(self.config_path)
        schema = self._load_yaml_plain(self.schema_path)

        self.validate_schema_with_locations(config, schema, source_tree)
        self._validate_references(config["tenants"])
        self._parse_tenants(config["tenants"])

    # -------------------------
    # YAML loading
    # -------------------------
    def _load_yaml_with_locations(self, path: Path):
        if not path.exists():
            raise FileNotFoundError(path)

        yaml_rt = YAML()
        yaml_rt.preserve_quotes = True

        with open(path, "r") as f:
            return yaml_rt.load(f)

    def _load_yaml_plain(self, path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(path)

        with open(path, "r") as f:
            return yaml.safe_load(f)

    # -------------------------
    # Validation
    # -------------------------

    @classmethod
    def validate_schema_with_locations(cls, config, schema, source_tree):
        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(config), key=lambda e: e.path)

        if not errors:
            return

        messages = []

        for err in errors:
            path = list(err.path)
            line, col = cls.resolve_location(source_tree, path)

            loc = (
                f"line {line}, column {col}"
                if line is not None
                else "unknown location")

            messages.append(f"- {loc} at {'/'.join(map(str, path))}: {err.message}")

        raise SchemaValidationError(
            "Schema validation failed:\n" + "\n".join(messages)
        )

    def _validate_references(self, tenants_cfg: dict) -> None:
        for tenant_id, cfg in tenants_cfg.items():
            device_classes = set(cfg["definitions"]["device_classes"].keys())

            for farm in cfg["topology"].get("farms", []):
                for device in farm.get("devices", []):
                    if device["class"] not in device_classes:
                        raise ReferenceValidationError(
                            f"Tenant '{tenant_id}': "
                            f"device '{device['id']}' "
                            f"uses unknown device_class '{device['class']}'"
                        )

    # -------------------------
    # Domain construction
    # -------------------------

    def _parse_tenants(self, tenants_cfg: dict) -> None:
        # TENANTS
        for tenant_key, cfg in tenants_cfg.items():
            tenant = Tenant(
                id=tenant_key,
                short_name=cfg["meta"]["short_name"],
                full_name=cfg["meta"]["full_name"],
                api_version=cfg["meta"]["api_version"],
                description=cfg["meta"].get("description", ""),
            )
            # DEVICE_CLASSES
            for dc_id in cfg["definitions"]["device_classes"].keys():
                tenant.register_device_class(DeviceClass(id=dc_id))

            # MESSAGE_CLASSES
            for mc in cfg["definitions"]["message_classes"]:
                tenant.register_message_class(
                    MessageClass(
                        id=mc["id"],
                        topic=mc["topic"]
                    )
                )
            self.registry.register_tenant(tenant)

            # FARMS
            for farm_cfg in cfg["topology"].get("farms", []):
                farm = Farm(
                    id=farm_cfg["id"],
                    name=farm_cfg["name"],
                    city=farm_cfg["city"],
                )
                tenant.register_farm(farm)

                # DEVICES
                for dev_cfg in farm_cfg.get("devices", []):
                    try:
                        device_class = tenant.get_device_class(dev_cfg["class"])

                        device = Device(
                            id=dev_cfg["id"],
                            device_class=device_class,
                            model=dev_cfg.get("model"),
                            location=dev_cfg.get("location"),
                        )
                    except Exception as e:
                        raise DomainConstructionError(
                            f"Tenant '{tenant.id}', farm '{farm.id}', "
                            f"device '{dev_cfg.get('id')}': {e}"
                        ) from e
                    tenant.register_device(farm.id, device)

            # POLICIES
            for policy_cfg in cfg["policies"]:
                policy_name = policy_cfg["name"]

                # Resolve farms (None = global)
                if "farms" in policy_cfg and policy_cfg["farms"]:
                    farms: list[Farm | None] = [
                        tenant.get_farm(farm_id)
                        for farm_id in policy_cfg["farms"]
                    ]
                else:
                    farms = [None]

                # Resolve device classes
                device_classes: list[DeviceClass] = [
                    tenant.get_device_class(dc_id)
                    for dc_id in policy_cfg["device_classes"]
                ]

                # Resolve message classes
                message_classes: list[MessageClass] = [
                    tenant.get_message_class(mc_id)
                    for mc_id in policy_cfg["message_classes"]
                ]

                # Resolve direction (if needed)
                direction = MqttDirection[policy_cfg["direction"]]

                # Expand into atomic policies
                for farm in farms:
                    for device_class in device_classes:
                        for message_class in message_classes:
                            atomic_policy = Policy(
                                name=policy_name,
                                farm=farm,
                                device_class=device_class,
                                message_class=message_class,
                                direction=direction,
                            )

                            tenant.register_policy(atomic_policy)

    # -------------------------
    # Location resolution
    # -------------------------

    @staticmethod
    def resolve_location(root, path):
        """
        Resolve a jsonschema error.path into (line, column).
        Falls back gracefully if exact node is unavailable.
        """
        node = root

        for p in path:
            try:
                if isinstance(node, CommentedMap):
                    node = node[p]
                elif isinstance(node, CommentedSeq):
                    node = node[p]
                else:
                    break
            except Exception:
                break

        if hasattr(node, "lc") and node.lc.line is not None:
            return node.lc.line + 1, node.lc.col + 1

        return None, None
