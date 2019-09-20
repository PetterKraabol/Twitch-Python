import time
from datetime import timedelta
from typing import Dict, Any, Optional

import requests

from .cache import Cache


class API:
    SHARED_CACHE: Cache = Cache()

    def __init__(self,
                 base_url: Optional[str] = None,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 use_cache: Optional[bool] = False,
                 request_rate: Optional[int] = None,
                 bearer_token: Optional[str] = None,
                 handle_rate_limit: bool = True,
                 cache_duration: Optional[timedelta] = None):
        """
        Twitch API
        :param base_url: API URL
        :param client_id: Twitch Client ID
        :param use_cache: Use local API cache
        :param bearer_token: Twitch bearer token
        :param handle_rate_limit: Handle rate limits by sleeping
        :param cache_duration: Local cache duration
        """
        self.base_url: Optional[str] = base_url
        self.client_id: Optional[str] = client_id
        self.client_secret: Optional[str] = client_secret
        self.use_cache: bool = use_cache
        self.request_rate: Optional[int] = request_rate
        self.bearer_token: Optional[str] = bearer_token
        self.handle_rate_limit: bool = handle_rate_limit
        self.cache_duration: Optional[timedelta] = cache_duration

        # Rate limit
        self.rate_limit_points: int = 800 if self.bearer_token else 30
        self.rate_limit_remaining: int = self.rate_limit_points
        self.rate_limit_reset: int = 0

    def _headers(self, custom: Dict[str, str] = None) -> Dict[str, str]:
        default: Dict[str, str] = {}

        if self.client_id:
            default['Client-ID'] = self.client_id

        if self.bearer_token:
            default['Authorization'] = self.bearer_token

        return {**default, **custom} if custom else default.copy()

    def _url(self, path: str = '') -> str:
        return self.base_url.rstrip('/') + '/' + path.lstrip('/')

    @staticmethod
    def flush_cache():
        API.SHARED_CACHE.flush()

    def _handle_rate_limit(self) -> None:
        if self.handle_rate_limit and self.rate_limit_remaining == 0:
            time_to_sleep: float = min((self.rate_limit_reset - time.time()), 10)
            time_to_sleep = max(time_to_sleep, 1)

            time.sleep(time_to_sleep)

    def _set_rate_limit(self, response: requests.Response) -> None:
        # Update rate limit fields
        if 'Ratelimit-Limit' in response.headers.keys():
            self.rate_limit_points: int = int(response.headers.get('Ratelimit-Limit'))
            self.rate_limit_remaining: int = int(response.headers.get('Ratelimit-Remaining'))
            self.rate_limit_reset: int = int(response.headers.get('Ratelimit-Reset'))

    def request(self, method, path: str = '', ignore_cache: bool = False, **kwargs) -> dict:
        url: str = self._url(path=path)
        request = requests.Request(method, url, **kwargs).prepare()
        cache_key: str = f'{method}:{request.url}'

        # Cache lookup
        if self.use_cache and not ignore_cache and API.SHARED_CACHE.get(cache_key):
            return API.SHARED_CACHE.get(cache_key)

        # Check rate limit
        self._handle_rate_limit()

        while True:
            response = requests.Session().send(request)
            self._set_rate_limit(response)

            # Too many requests status
            if response.status_code == 429 and self.handle_rate_limit:
                self._handle_rate_limit()
            else:
                break

        # Raise exception if status code is not 200
        response.raise_for_status()

        # Cache response
        if self.use_cache and not ignore_cache:
            API.SHARED_CACHE.set(key=cache_key, value=response.json(), duration=self.cache_duration)

        return response.json()

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, Any]] = None,
            ignore_cache: bool = False,
            **kwargs) -> dict:
        return self.request('GET', path, ignore_cache, params=params, headers=self._headers(headers), **kwargs)

    def post(self):
        pass

    def put(self):
        pass
