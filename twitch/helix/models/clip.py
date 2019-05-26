from typing import Dict, Any

from twitch.api import API
from .model import Model


class Clip(Model):

    def __init__(self, api: API, data: Dict[str, Any]):
        super().__init__(api, data)
