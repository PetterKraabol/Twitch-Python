from datetime import timedelta
from typing import List, Union

import twitch.v5 as v5
from twitch.api import API


class V5:
    BASE_URL: str = 'https://api.twitch.tv/v5/'

    def __init__(self, client_id: str,
                 client_secret: str = None,
                 request_rate: int = None,
                 use_cache: bool = False,
                 cache_duration: timedelta = timedelta(minutes=30)):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.request_rate: int = request_rate
        self.use_cache: bool = use_cache
        self.cache_duration: timedelta = cache_duration
        self.scope: List[str] = []

        self.api = API(V5.BASE_URL, self.client_id, use_cache=self.use_cache, request_rate=self.request_rate)

    def comments(self, video_id: Union[str, int]) -> 'v5.Comments':
        return v5.Comments(api=self.api, video_id=video_id)
