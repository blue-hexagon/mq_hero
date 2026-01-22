# infrastructure/loaders/yaml_loader.py

import yaml
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq


class YamlLoader:
    """
    Pure YAML parser.
    Converts YAML text into Python structures.
    """

    def load_plain(self, text: str) -> dict:
        return yaml.safe_load(text)

    def load_with_locations(self, text: str):
        yaml_rt = YAML()
        yaml_rt.preserve_quotes = True
        return yaml_rt.load(text)
