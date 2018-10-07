from datetime import timedelta
from typing import List, Union

from .comments import Comments
from ..api import API


class V5:
    BASE_URL: str = 'https://api.twitch.tv/v5/'

    def __init__(self, client_id: str,
                 client_secret: str = None,
                 rate_limit: int = None,
                 use_cache: bool = False,
                 cache_duration: timedelta = timedelta(minutes=30)):
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.rate_limit: int = rate_limit
        self.use_cache: bool = use_cache
        self.cache_duration: timedelta = cache_duration
        self.scope: List[str] = []

    def api(self) -> API:
        return API(V5.BASE_URL, self.client_id, use_cache=self.use_cache, rate_limit=self.rate_limit)

    def comments(self, video_id: Union[str, int]) -> Comments:
        return Comments(api=self.api(), video_id=video_id)
