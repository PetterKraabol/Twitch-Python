import twitch.helix as helix
import twitch.v5 as v5
from twitch.api import API


class Video:

    def __init__(self, data: dict = None, api: API = None):
        # Meta
        self._api: API = api
        self.data: dict = data

        # Response fields
        self.id: str = None
        self.user_id: str = None
        self.title: str = None
        self.description: str = None
        self.created_at: str = None
        self.published_at: str = None
        self.url: str = None
        self.thumbnail_url: str = None
        self.viewable: str = None
        self.view_count: int = None
        self.language: str = None
        self.type: str = None
        self.duration: str = None

        # Fill response fields
        for key, value in data.items():
            self.__dict__[key] = value

    def comments(self) -> 'v5.Comments':
        return v5.V5(client_id=self._api.client_id,
                     use_cache=self._api.use_cache,
                     cache_duration=self._api.cache_duration).comments(self.id)

    def user(self) -> 'helix.Users':
        return helix.Users(self._api, self.user_id)

    def __str__(self):
        return self.title
