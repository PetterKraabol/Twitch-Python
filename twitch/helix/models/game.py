from typing import Dict, Any

import twitch.helix as helix
from twitch.api import API


class Game:

    def __init__(self, api: API, data: Dict[str, Any]):
        # Meta
        self._api: API = api
        self.data: Dict[str, Any] = data

        # Response fields
        self.id: str = self.data.get('id')
        self.name: str = self.data.get('name')
        self.box_art_url: str = self.data.get('box_art_url')

    def __str__(self):
        return self.name

    def videos(self, **kwargs) -> 'helix.Videos':
        return helix.Videos(self._api, game_id=self.id, **kwargs)
