from enum import Enum


class AssetKind(str, Enum):
    PLAYBOOK = "playbook"
    SCHEMA = "schema"
