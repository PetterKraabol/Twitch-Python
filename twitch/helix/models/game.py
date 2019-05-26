from typing import Dict, Any

import twitch.helix as helix
from twitch.api import API
from .model import Model


class Game(Model):

    def __init__(self, api: API, data: Dict[str, Any]):
        super().__init__(api, data)

        self.id: str = data.get('id')
        self.name: str = data.get('name')
        self.box_art_url: str = data.get('box_art_url')

    def __str__(self):
        return self.name

    def videos(self, **kwargs) -> 'helix.Videos':
        return helix.Videos(self._api, game_id=self.id, **kwargs)
