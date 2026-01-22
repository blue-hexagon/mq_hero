import yaml
from ruamel.yaml import YAML


class YamlLoader:
    """
    Pure YAML parser.
    Converts YAML text into Python structures.
    """

    @staticmethod
    def load_plain(text: str) -> dict:
        return yaml.safe_load(text)

    @staticmethod
    def load_with_locations(text: str):
        yaml_rt = YAML()
        yaml_rt.preserve_quotes = True
        return yaml_rt.load(text)
