from datetime import timedelta
from typing import List, Union

import twitch.helix as helix
from twitch.api import API


class Helix:
    BASE_URL: str = 'https://api.twitch.tv/helix/'

    def __init__(self, client_id: str, client_secret: str = None, use_cache: bool = False,
                 cache_duration: timedelta = timedelta(minutes=30), rate_limit: int = 30):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.use_cache: bool = use_cache
        self.cache_duration: timedelta = cache_duration
        self.rate_limit: int = rate_limit

    def api(self) -> API:
        return API(Helix.BASE_URL, self.client_id, use_cache=self.use_cache, rate_limit=self.rate_limit)

    def users(self, *args) -> 'helix.Users':
        return helix.Users(self.api(), *args)

    def user(self, user: Union[str, int]) -> 'helix.User':
        return self.users(user)[0]

    def videos(self, video_ids: Union[str, int, List[Union[str, int]]], **kwargs) -> 'helix.Videos':
        if type(video_ids) != list:
            video_ids = [video_ids]
        return helix.Videos(self.api(), video_ids=video_ids, **kwargs)

    def video(self, video_id: Union[str, int] = None, **kwargs) -> 'helix.Video':
        if video_id:
            kwargs['id'] = video_id
        return helix.Videos(self.api(), video_ids=None, **kwargs)[0]

    def streams(self, **kwargs) -> 'helix.Streams':
        return helix.Streams(self.api(), **kwargs)

    def stream(self, **kwargs) -> 'helix.Stream':
        return self.streams(**kwargs)[0]
