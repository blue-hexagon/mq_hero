from pathlib import PurePosixPath
from .asset_kind import AssetKind


class FilesystemPolicy:
    ALLOWED_ROOTS: dict[AssetKind, PurePosixPath] = {
        AssetKind.PLAYBOOK: PurePosixPath("src/v2/assets/playbooks"),
        AssetKind.SCHEMA: PurePosixPath("src/v2/assets/schemas"),
    }

    @classmethod
    def resolve_allowed_path(cls, kind: AssetKind, name: str) -> PurePosixPath:
        if kind not in cls.ALLOWED_ROOTS:
            # This should now be impossible, but stay defensive
            raise ValueError(f"Unsupported asset kind: {kind}")

        # Hard reject traversal attempts
        if ".." in name or name.startswith(("/", "\\")):
            raise PermissionError("Invalid asset name")

        # Normalize path safely
        rel = PurePosixPath(name)

        if rel.is_absolute():
            raise PermissionError("Absolute paths are forbidden")

        return cls.ALLOWED_ROOTS[kind] / rel
