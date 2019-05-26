from typing import Dict, Any

from twitch.api import API
from twitch.helix.models import Model, Stream
from twitch.helix.resources import Videos, Streams, Follows


class User(Model):

    def __init__(self, api: API, data: Dict[str, Any]):
        super().__init__(api, data)

        self.broadcaster_type: str = self.data.get('broadcaster_type')
        self.description: str = self.data.get('description')
        self.display_name: str = self.data.get('display_name')
        self.email: str = self.data.get('email')
        self.id: str = self.data.get('id')
        self.login: str = self.data.get('login')
        self.offline_image_url: str = self.data.get('offline_image_url')
        self.profile_image_url: str = self.data.get('profile_image_url')
        self.type: str = self.data.get('type')
        self.view_count: int = self.data.get('view_count')

    def __str__(self):
        return self.login

    def videos(self, **kwargs) -> Videos:
        return Videos(api=self._api, user_id=int(self.id), **kwargs)

    @property
    def stream(self) -> Stream:
        return Streams(api=self._api, user_id=int(self.id))[0]

    def following(self, **kwargs) -> Follows:
        kwargs['from_id'] = self.id
        return Follows(api=self._api, follow_type='following', **kwargs)

    def followers(self, **kwargs) -> Follows:
        kwargs['to_id'] = self.id
        return Follows(api=self._api, follow_type='followers', **kwargs)
