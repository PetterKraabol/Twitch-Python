from typing import List, Dict, Any

import twitch.helix as helix
from twitch.api import API
from .model import Model


class Stream(Model):

    def __init__(self, api: API, data: Dict[str, Any]):
        """
        [reference](https://dev.twitch.tv/docs/api/reference#get-streams)
        """
        super().__init__(api, data)

        self.id: str = data.get('id')
        self.user_id: str = data.get('user_id')
        self.user_login: str = data.get('user_login')
        self.user_name: str = data.get('user_name')
        self.game_id: str = data.get('game_id')
        self.game_name: str = data.get('game_name')
        self.community_ids: List[str] = data.get('community_ids', [])
        self.type: str = data.get('type')
        self.title: str = data.get('title')
        self.viewer_count: int = data.get('viewer_count')
        self.started_at: str = data.get('started_at')
        self.language: str = data.get('language')
        self.thumbnail_url: str = data.get('thumbnail_url')
        self.tag_ids: list = data.get('tag_ids', [])
        self.is_mature: bool = data.get('is_mature', False)

    def __str__(self):
        return self.title

    @property
    def user(self) -> 'helix.User':
        return helix.Users(self._api, int(self.user_id))[0]
