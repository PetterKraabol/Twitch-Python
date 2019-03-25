from typing import List

import twitch.helix as helix
from twitch.api import API
from twitch.helix.models.model import Model


class Stream(Model):

    def __init__(self, api: API, data: dict):
        super().__init__(api, data)

        self.id: str = None
        self.user_id: str = None
        self.game_id: str = None
        self.community_ids: List[str] = []
        self.type: str = None
        self.title: str = None
        self.viewer_count: int = None
        self.started_at: str = None
        self.language: str = None
        self.thumbnail_url: str = None

        self._populate()

    def __str__(self):
        return self.title

    @property
    def user(self) -> 'helix.User':
        return helix.Users(self._api, int(self.user_id))[0]
