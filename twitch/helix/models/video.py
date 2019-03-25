import twitch.helix as helix
import twitch.v5 as v5
from twitch.api import API
from twitch.helix.models.model import Model


class Video(Model):

    def __init__(self, api: API, data: dict):
        super().__init__(api, data)

        # Response fields
        self.id: str = None
        self.user_id: str = None
        self.user_name: str = None
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

        self._populate()

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
