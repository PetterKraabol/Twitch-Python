from typing import Dict, Any

from twitch.api import API
from twitch.helix.models import Model
from twitch.helix.resources import Videos


class Game(Model):

    def __init__(self, api: API, data: Dict[str, Any]):
        super().__init__(api, data)

        self.id: str = self.data.get('id')
        self.name: str = self.data.get('name')
        self.box_art_url: str = self.data.get('box_art_url')

    def __str__(self):
        return self.name

    def videos(self, **kwargs) -> Videos:
        return Videos(self._api, game_id=self.id, **kwargs)
