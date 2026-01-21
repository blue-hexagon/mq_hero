from src.v2.infrastructure.filesystem.vfs import VirtualFS


class SchemaResolver:
    def __init__(self, fs: VirtualFS):
        self.fs = fs

    def resolve(self, schema_name: str) -> str:
        candidates = [
            f"{schema_name}.yaml",
        ]

        for candidate in candidates:
            try:
                self.fs.read_text(candidate)
                return candidate
            except FileNotFoundError:
                continue

        raise FileNotFoundError(f"No schema found for {schema_name}")

