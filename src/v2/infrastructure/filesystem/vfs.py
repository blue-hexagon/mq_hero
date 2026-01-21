from pathlib import Path
from typing import Optional

from src.v2.infrastructure.filesystem.errors import SecurityError


class VirtualFS:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def resolve(self, relative: str) -> Path:
        path = (self.root / relative).resolve()
        if not path.is_relative_to(self.root):
            raise SecurityError("Path escape attempt detected")
        return path

    def read_text(self, relative: str) -> str:
        path = self.resolve(relative)
        if not path.exists():
            raise FileNotFoundError(relative)
        return path.read_text(encoding="utf-8")
