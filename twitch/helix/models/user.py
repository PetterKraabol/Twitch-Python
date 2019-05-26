from typing import Dict, Any

from twitch.api import API
from twitch.helix.resources.follows import Follows
from twitch.helix.resources.streams import Streams
from twitch.helix.resources.videos import Videos
from .model import Model
from .stream import Stream


class User(Model):

    def __init__(self, api: API, data: Dict[str, Any]):
        super().__init__(api, data)

        self.broadcaster_type: str = data.get('broadcaster_type')
        self.description: str = data.get('description')
        self.display_name: str = data.get('display_name')
        self.email: str = data.get('email')
        self.id: str = data.get('id')
        self.login: str = data.get('login')
        self.offline_image_url: str = data.get('offline_image_url')
        self.profile_image_url: str = data.get('profile_image_url')
        self.type: str = data.get('type')
        self.view_count: int = data.get('view_count')

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
