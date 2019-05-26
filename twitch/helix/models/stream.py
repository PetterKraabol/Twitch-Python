from typing import List, Dict, Any

from twitch.api import API
from twitch.helix.models import Model, User
from twitch.helix.resources import Users


class Stream(Model):

    def __init__(self, api: API, data: Dict[str, Any]):
        super().__init__(api, data)

        self.id: str = self.data.get('id')
        self.user_id: str = self.data.get('user_id')
        self.game_id: str = self.data.get('game_id')
        self.community_ids: List[str] = self.data.get('community_ids', [])
        self.type: str = self.data.get('type')
        self.title: str = self.data.get('title')
        self.viewer_count: int = self.data.get('viewer_count')
        self.started_at: str = self.data.get('started_at')
        self.language: str = self.data.get('language')
        self.thumbnail_url: str = self.data.get('thumbnail_url')

    def __str__(self):
        return self.title

    @property
    def user(self) -> User:
        return Users(self._api, int(self.user_id))[0]
