from datetime import timedelta
from typing import List, Union, Optional

import twitch.helix as helix
from twitch.api import API


class Helix:
    BASE_URL: str = 'https://api.twitch.tv/helix/'

    def __init__(self,
                 client_id: str,
                 client_secret: str = None,
                 use_cache: bool = False,
                 cache_duration: Optional[timedelta] = None,
                 handle_rate_limit: bool = True,
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
        self.client_secret: str = client_secret

        # Format bearer token
        if bearer_token:
            bearer_token = 'Bearer ' + bearer_token.lower().lstrip('bearer').strip()

        self.api = API(Helix.BASE_URL,
                       client_id=client_id,
                       client_secret=client_secret,
                       use_cache=use_cache,
                       cache_duration=cache_duration,
                       handle_rate_limit=handle_rate_limit,
                       bearer_token=bearer_token)

    def users(self, *args) -> 'helix.Users':
        return helix.Users(self.api, *args)

    def user(self, user: Union[str, int]) -> 'helix.User':
        return self.users(user)[0]

    def videos(self, video_ids: Union[str, int, List[Union[str, int]]] = None, **kwargs) -> 'helix.Videos':
        if video_ids and type(video_ids) != list:
            video_ids = [int(video_ids)]
        return helix.Videos(self.api, video_ids=video_ids, **kwargs)

    def video(self, video_id: Union[str, int] = None, **kwargs) -> 'helix.Video':
        if video_id:
            kwargs['id'] = [video_id]
        return helix.Videos(self.api, video_ids=None, **kwargs)[0]

    def streams(self, **kwargs) -> 'helix.Streams':
        return helix.Streams(self.api, **kwargs)

    def stream(self, **kwargs) -> 'helix.Stream':
        return self.streams(**kwargs)[0]

    def games(self, **kwargs) -> 'helix.Games':
        return helix.Games(self.api, **kwargs)

    def game(self, **kwargs) -> 'helix.Game':
        return self.games(**kwargs)[0]

    def top_games(self, **kwargs) -> List['helix.Game']:
        return helix.Games(self.api).top(**kwargs)

    def top_game(self) -> 'helix.Game':
        return self.top_games()[0]
