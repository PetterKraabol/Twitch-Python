import twitch.helix as helix
from twitch.api import API
from twitch.helix.models.model import Model


class Game(Model):

    def __init__(self, api: API, data: dict):
        super().__init__(api, data)

        self.id: str = None
        self.name: str = None
        self.box_art_url: str = None

        self._populate()

    def __str__(self):
        return self.name

    def videos(self, **kwargs) -> 'helix.Videos':
        return helix.Videos(self._api, game_id=self.id, **kwargs)
