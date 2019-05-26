from typing import List, Dict, Any

import twitch.helix as helix
from twitch.api import API


class Stream:

    def __init__(self, api: API, data: Dict[str, Any]):
        # Meta
        self._api: API = api
        self.data: Dict[str, Any] = data

        # Response fields
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

    def user(self) -> 'helix.User':
        return helix.Users(self._api, int(self.user_id))[0]

    def __str__(self):
        return self.title
