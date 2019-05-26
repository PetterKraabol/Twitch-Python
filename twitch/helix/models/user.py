from typing import Dict, Any

import twitch.helix as helix
from twitch.api import API


class User:

    def __init__(self, api: API, data: Dict[str, Any]):
        # Meta
        self._api: API = api
        self.data: Dict[str, Any] = data

        # Response fields
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

    def videos(self, **kwargs) -> 'helix.Videos':
        return helix.Videos(api=self._api, user_id=int(self.id), **kwargs)

    def stream(self) -> 'helix.Stream':
        return helix.Streams(api=self._api, user_id=int(self.id))[0]
