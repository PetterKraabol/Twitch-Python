from datetime import timedelta
from typing import Dict, Any

import requests

from twitch.cache import Cache


class API:
    SHARED_CACHE: Cache = Cache()

    def __init__(self, base_url: str = None,
                 client_id: str = None,
                 rate_limit: int = None,
                 use_cache: bool = False,
                 cache_duration: timedelta = None):
        self.base_url: str = base_url
        self.rate_limit: int = rate_limit
        self.client_id: str = client_id
        self.use_cache: bool = use_cache
        self.cache_duration: timedelta = cache_duration

    def _headers(self, custom: Dict[str, str] = None) -> Dict[str, str]:
        default: Dict[str, str] = {
            'Client-ID': self.client_id
        }
        return {**default, **custom} if custom else default.copy()

    def _url(self, path: str = '') -> str:
        return self.base_url.rstrip('/') + '/' + path.lstrip('/')

    @staticmethod
    def flush_cache():
        API.SHARED_CACHE = {}

    def request(self, method, path: str = '', ignore_cache: bool = False, **kwargs) -> dict:
        url: str = self._url(path=path)
        request = requests.Request(method, url, **kwargs).prepare()
        cache_key: str = f'{method}:{request.url}'

        if self.use_cache and not ignore_cache and API.SHARED_CACHE.get(cache_key):
            return API.SHARED_CACHE.get(cache_key)
        else:
            response: requests.Response = requests.Session().send(request)

            if self.use_cache and not ignore_cache:
                API.SHARED_CACHE.set(key=cache_key, value=response.json(), duration=self.cache_duration)
            return response.json()

    def get(self, path: str, params: Dict[str, Any] = None, headers: Dict[str, Any] = None, ignore_cache: bool = False,
            **kwargs) -> dict:
        return self.request('GET', path, ignore_cache, params=params, headers=self._headers(headers), **kwargs)

    def post(self):
        pass

    def put(self):
        pass
