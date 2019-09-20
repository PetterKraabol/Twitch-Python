from typing import Dict, Any

import twitch.helix as helix
import twitch.tmi as tmi
from twitch.api import API
from .model import Model


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

    def videos(self, **kwargs) -> 'helix.Videos':
        return helix.Videos(api=self._api, user_id=int(self.id), **kwargs)

    @property
    def stream(self) -> 'helix.Stream':
        return helix.Streams(api=self._api, user_id=int(self.id))[0]

    @property
    def is_live(self) -> bool:
        try:
            if self.stream:
                return True
        except helix.StreamNotFound:
            return False

    @property
    def chatters(self) -> 'tmi.Chatters':
        source = tmi.TMI('')
        source.api = self._api
        source.api.base_url = tmi.TMI.BASE_URL

        return source.chatters(self.login)

    def following(self, **kwargs) -> 'helix.Follows':
        kwargs['from_id'] = self.id
        return helix.Follows(api=self._api, follow_type='following', **kwargs)

    def followers(self, **kwargs) -> 'helix.Follows':
        kwargs['to_id'] = self.id
        return helix.Follows(api=self._api, follow_type='followers', **kwargs)
