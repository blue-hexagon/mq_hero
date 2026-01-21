from src.v2.infrastructure.filesystem.asset_kind import AssetKind
from src.v2.infrastructure.filesystem.policies import FilesystemPolicy
from src.v2.infrastructure.filesystem.vfs import VirtualFS


class PlaybookLoader:
    def __init__(self, fs: VirtualFS, resolver: FilesystemPolicy):
        self.fs = fs
        self.policy = resolver

    def load(self, name: str) -> str:
        path = self.policy.resolve_allowed_path(AssetKind.PLAYBOOK, name)
        return self.fs.read_text(str(path))
