from typing import Optional

import twitch.helix as helix
from twitch.api import API
from twitch.helix.models.model import Model


class User(Model):

    def __init__(self, api: API, data: dict):
        super().__init__(api, data)

        self.id: str = None
        self.login: str = None
        self.display_name: str = None
        self.type: str = None
        self.broadcaster_type: str = None
        self.description: str = None
        self.profile_image_url: str = None
        self.offline_image_url: str = None
        self.view_count: int = None
        self.email: Optional[str] = None

        self._populate()

    def __str__(self):
        return self.login

    def videos(self, **kwargs) -> 'helix.Videos':
        return helix.Videos(api=self._api, user_id=int(self.id), **kwargs)

    @property
    def stream(self) -> 'helix.Stream':
        return helix.Streams(api=self._api, user_id=int(self.id))[0]

    def following(self, **kwargs) -> 'helix.Follows':
        kwargs['from_id'] = self.id
        return helix.Follows(api=self._api, follow_type='following', **kwargs)

    def followers(self, **kwargs) -> 'helix.Follows':
        kwargs['to_id'] = self.id
        return helix.Follows(api=self._api, follow_type='followers', **kwargs)
