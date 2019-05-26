from typing import List, Dict, Any

import twitch.helix as helix
from twitch.api import API
from .model import Model


class Stream(Model):

    def __init__(self, api: API, data: Dict[str, Any]):
        super().__init__(api, data)

        self.id: str = data.get('id')
        self.user_id: str = data.get('user_id')
        self.game_id: str = data.get('game_id')
        self.community_ids: List[str] = data.get('community_ids', [])
        self.type: str = data.get('type')
        self.title: str = data.get('title')
        self.viewer_count: int = data.get('viewer_count')
        self.started_at: str = data.get('started_at')
        self.language: str = data.get('language')
        self.thumbnail_url: str = data.get('thumbnail_url')

    def __str__(self):
        return self.title

    @property
    def user(self) -> 'helix.User':
        return helix.Users(self._api, int(self.user_id))[0]
