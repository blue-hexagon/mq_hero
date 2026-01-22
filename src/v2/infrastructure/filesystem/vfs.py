import os
from pathlib import Path, PurePath
from typing import Union

PathLike = Union[str, os.PathLike[str], PurePath]


class VirtualFS:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def resolve(self, relative: PathLike) -> Path:
        rel = Path(relative)
        path = (self.root / rel).resolve()

        if not path.is_relative_to(self.root):
            raise PermissionError(f"Path escape attempt: {relative}")

        return path

    def read_text(self, relative: PathLike) -> str:
        path = self.resolve(relative)

        if not path.exists():
            raise FileNotFoundError(path)

        return path.read_text(encoding="utf-8")
