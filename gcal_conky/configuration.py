from typing import Any
import yaml

from .helper import get_absolute_path

CONFIG_FILE_PATH = "configuration/configuration.yaml"


class Configuration:

    def __init__(self):
        self._config: dict = None
        # now is set here so we put all log/checkpoint files in the same folder
        self._config = self._load_yaml(get_absolute_path(CONFIG_FILE_PATH))

    def get(self, key: str) -> Any:
        if key in self._config:
            return self._config[key]
        else:
            return None

    @staticmethod
    def _load_yaml(path: str) -> dict:
        with open(path, 'r') as stream:
            return yaml.safe_load(stream)
