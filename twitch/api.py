from datetime import datetime, timedelta
from typing import Dict

import requests


class API:
    SHARED_CACHE: Dict[str, dict] = {}

    def __init__(self, base_url: str = None,
                 client_id: str = None,
                 rate_limit: int = None,
                 use_cache: bool = False,
                 cache_duration: timedelta = timedelta(minutes=30)):
        self.base_url: str = base_url
        self.rate_limit: int = rate_limit
        self.client_id: str = client_id
        self.use_cache: str = use_cache
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
        cache_key: str = f'{method}:{path}'

        if self.use_cache and not ignore_cache and cache_key in API.SHARED_CACHE and API.SHARED_CACHE[cache_key][
            'cache_expiration'] > datetime.now():
            return API.SHARED_CACHE[cache_key]
        else:
            response: requests.api = requests.request(method=method, url=url, **kwargs)

            if self.use_cache and not ignore_cache:
                API.SHARED_CACHE[cache_key] = response.json()
                API.SHARED_CACHE[cache_key]['cache_expiration'] = datetime.now() + self.cache_duration

            return response.json()

    def get(self, path: str, params: Dict[str, str] = None, headers: Dict[str, str] = None, ignore_cache: bool = False,
            **kwargs) -> dict:
        return self.request('GET', path, ignore_cache, params=params, headers=self._headers(headers), **kwargs)

    def post(self):
        pass

    def put(self):
        pass
