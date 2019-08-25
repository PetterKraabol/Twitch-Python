from typing import Dict, Any

import twitch.helix as helix
import twitch.v5 as v5
from twitch.api import API
from .model import Model


class Video(Model):

    def __init__(self, api: API, data: Dict[str, Any]):
        super().__init__(api, data)

        self.id: str = data.get('id')
        self.user_id: str = data.get('user_id')
        self.user_name: str = data.get('user_name')
        self.title: str = data.get('title')
        self.description: str = data.get('description')
        self.created_at: str = data.get('created_at')
        self.published_at: str = data.get('published_at')
        self.url: str = data.get('url')
        self.thumbnail_url: str = data.get('thumbnail_url')
        self.viewable: str = data.get('viewable')
        self.view_count: int = data.get('view_count')
        self.language: str = data.get('language')
        self.type: str = data.get('type')
        self.duration: str = data.get('duration')

    def __str__(self):
        return self.title

    @property
    def comments(self) -> 'v5.Comments':
        return v5.V5(client_id=self._api.client_id,
                     use_cache=self._api.use_cache,
                     cache_duration=self._api.cache_duration).comments(self.id)

    @property
    def user(self) -> 'helix.User':
        return helix.Users(self._api, int(self.user_id))[0]
