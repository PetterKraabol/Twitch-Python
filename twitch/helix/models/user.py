import twitch.helix as helix
from twitch.api import API


class User:

    def __init__(self, data: dict = None, api: API = None):
        # Meta
        self._api: API = api
        self.data: dict = data

        # Response fields
        self.broadcaster_type: str = None
        self.description: str = None
        self.display_name: str = None
        self.email: str = None
        self.id: str = None
        self.login: str = None
        self.offline_image_url: str = None
        self.profile_image_url: str = None
        self.type: str = None
        self.view_count: int = None

        # Fill response fields
        for key, value in data.items():
            self.__dict__[key] = value

    def __str__(self):
        return self.login

    def videos(self, **kwargs) -> 'helix.Videos':
        return helix.Videos(api=self._api, user_id=self.id, **kwargs)

    def stream(self) -> 'helix.Stream':
        return helix.Streams(api=self._api, user_id=self.id)[0]
