from typing import Dict, Any, List

import twitch.helix as helix
from twitch.api import API
from .model import Model


class Chatter(Model):

    def __init__(self, api: API, name: str, chatter_type: str):
        super().__init__(api, {})
        self.name: str = name
        self.type: str = chatter_type

    @property
    def user(self) -> 'helix.User':
        source = helix.Helix('')
        source.api = self._api
        source.api.base_url = helix.Helix.BASE_URL
        return source.user(self.name)
