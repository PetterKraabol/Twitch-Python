from typing import Dict, Any

from twitch.api import API
from twitch.helix.models import Model, User
from twitch.helix.resources import Users
from twitch.v5 import V5
from twitch.v5.resources import Comments


class Video(Model):

    def __init__(self, api: API, data: Dict[str, Any]):
        super().__init__(api, data)

        self.id: str = self.data.get('id')
        self.user_id: str = self.data.get('user_id')
        self.title: str = self.data.get('title')
        self.description: str = self.data.get('description')
        self.created_at: str = self.data.get('created_at')
        self.published_at: str = self.data.get('published_at')
        self.url: str = self.data.get('url')
        self.thumbnail_url: str = self.data.get('thumbnail_url')
        self.viewable: str = self.data.get('viewable')
        self.view_count: int = self.data.get('view_count')
        self.language: str = self.data.get('language')
        self.type: str = self.data.get('type')
        self.duration: str = self.data.get('duration')

    def __str__(self):
        return self.title

    @property
    def comments(self) -> Comments:
        return V5(client_id=self._api.client_id,
                  use_cache=self._api.use_cache,
                  cache_duration=self._api.cache_duration).comments(self.id)

    @property
    def user(self) -> User:
        return Users(self._api, int(self.user_id))[0]
