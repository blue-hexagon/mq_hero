from src.v2.infrastructure.filesystem.policies import FilesystemPolicy
from src.v2.infrastructure.filesystem.asset_kind import AssetKind
from src.v2.infrastructure.filesystem.vfs import VirtualFS

from src.v2.infrastructure.loaders.yaml_loader import YamlLoader
from src.v2.infrastructure.loaders.schema_validator import SchemaValidator
from src.v2.application.services.tenant_assembler import TenantAssembler


class TenantConfigService:
    """
    Application use-case:
    Load tenant configuration assets and populate the domain registry.
    """

    def __init__(
            self,
            fs: VirtualFS,
            tenant_assembler: TenantAssembler,
            yaml_loader: YamlLoader,
            schema_validator: SchemaValidator,
    ):
        self.fs = fs
        self.tenant_assembler = tenant_assembler
        self.yaml_loader = yaml_loader
        self.schema_validator = schema_validator

    def load(self) -> None:
        # Resolve assets
        config_path = FilesystemPolicy.resolve_allowed_path(
            AssetKind.PLAYBOOK, "main.yaml"
        )
        schema_path = FilesystemPolicy.resolve_allowed_path(
            AssetKind.SCHEMA, "tenant.schema.yaml"
        )

        # Read files
        config_text = self.fs.read_text(config_path)
        schema_text = self.fs.read_text(schema_path)

        # Parse
        source_tree = self.yaml_loader.load_with_locations(config_text)
        config = self.yaml_loader.load_plain(config_text)
        schema = self.yaml_loader.load_plain(schema_text)

        # Validate
        self.schema_validator.validate_with_locations(
            config, schema, source_tree
        )
        self.schema_validator.validate_references(config["tenants"])

        # Assemble domain
        self.tenant_assembler.assemble(config["tenants"])
