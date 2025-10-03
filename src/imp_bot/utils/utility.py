import json
import httpx
from enum import Enum


CFG_FILENAME = "./src/imp_bot/config.json"

class Configurable:
    """
    Parent Configuration object used to store the config file
    """
    def __init__(self):
        self._file = self._get_config_file()

    def _get_config_file(self):
        with open(CFG_FILENAME) as cfg:
            configs = json.load(cfg)
        return configs