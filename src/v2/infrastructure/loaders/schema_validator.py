from jsonschema import Draft202012Validator
from ruamel.yaml.comments import CommentedMap, CommentedSeq

from src.v2.infrastructure.loaders.errors import ReferenceValidationError, SchemaValidationError, SchemaParsingError


class SchemaValidator:
    """
    Validates configuration against JSON Schema
    and performs cross-reference checks.
    """

    def validate_with_locations(
        self,
        config: dict,
        schema: dict,
        source_tree,
    ) -> None:
        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(config), key=lambda e: e.path)

        if not errors:
            return

        messages = []
        for err in errors:
            path = list(err.path)
            line, col = self.resolve_location(source_tree, path)

            loc = (
                f"line {line}, column {col}"
                if line is not None
                else "unknown location"
            )

            messages.append(
                f"- {loc} at {'/'.join(map(str, path))}: {err.message}"
            )

        raise SchemaValidationError(
            "Schema validation failed:\n" + "\n".join(messages)
        )

    @staticmethod
    def validate_references(tenants_cfg: dict) -> None:
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

    @staticmethod
    def resolve_location(root, path):
        node = root
        for p in path:
            try:
                if isinstance(node, CommentedMap):
                    node = node[p]
                elif isinstance(node, CommentedSeq):
                    node = node[p]
                else:
                    break
            except SchemaParsingError():
                break

        if hasattr(node, "lc") and node.lc.line is not None:
            return node.lc.line + 1, node.lc.col + 1

        return None, None
