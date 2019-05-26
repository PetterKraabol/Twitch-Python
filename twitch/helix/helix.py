from datetime import timedelta
from typing import List, Union, Optional

from twitch.api import API
from twitch.helix.models import User, Video, Stream, Game
from twitch.helix.resources import Users, Videos, Streams, Games


class Helix:
    BASE_URL: str = 'https://api.twitch.tv/helix/'

    def __init__(self,
                 client_id: str,
                 client_secret: str = None,
                 use_cache: bool = False,
                 cache_duration: Optional[timedelta] = None,
                 bearer_token: Optional[str] = None):
        """
        Helix API (New Twitch API)
        https://dev.twitch.tv/docs/api/

        :param client_id: Twitch client ID
        :param client_secret: Twitch client secret
        :param use_cache: Cache API requests (recommended)
        :param cache_duration: Cache duration
        :param bearer_token: API bearer token
        """
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.use_cache: bool = use_cache
        self.cache_duration: Optional[timedelta] = cache_duration
        self.bearer_token: Optional[str] = bearer_token

        # Format bearer token
        if self.bearer_token:
            self.bearer_token = 'Bearer ' + self.bearer_token.lower().lstrip('bearer').strip()

        self.api = API(Helix.BASE_URL, self.client_id, use_cache=self.use_cache, bearer_token=self.bearer_token)

    def users(self, *args) -> Users:
        return Users(self.api, *args)

    def user(self, user: Union[str, int]) -> User:
        return self.users(user)[0]

    def videos(self, video_ids: Union[str, int, List[Union[str, int]]] = None, **kwargs) -> Videos:
        if video_ids and type(video_ids) != list:
            video_ids = [int(video_ids)]
        return Videos(self.api, video_ids=video_ids, **kwargs)

    def video(self, video_id: Union[str, int] = None, **kwargs) -> Video:
        if video_id:
            kwargs['id'] = [video_id]
        return Videos(self.api, video_ids=None, **kwargs)[0]

    def streams(self, **kwargs) -> Streams:
        return Streams(self.api, **kwargs)

    def stream(self, **kwargs) -> Stream:
        return self.streams(**kwargs)[0]

    def games(self, **kwargs) -> Games:
        return Games(self.api, **kwargs)

    def game(self, **kwargs) -> Game:
        return self.games(**kwargs)[0]

    def top_games(self, **kwargs) -> List[Game]:
        return Games(self.api).top(**kwargs)

    def top_game(self) -> Game:
        return self.top_games()[0]
