from typing import List, Union, Generator, Tuple, Dict

import twitch.helix as helix
from twitch.api import API
from .resource import Resource


class Users(Resource['helix.User']):

    def __init__(self, api: API, *args):
        super().__init__(api=api, path='users')

        # Load data
        users: List[Union[str, int]] = []
        for user in args:
            users += [user] if type(user) in [str, int] else list(user)

        params: Dict[str, list] = dict()

        # Split user id and login (based on type t)
        params['id'], params['login'] = [
            list(set(n)) for n in [
                [str(user) for user in users if type(user) == t] for t in [int, str]
            ]
        ]

        # todo: Authenticated user if bearer token is provided
        if not len(params['id'] + params['login']):
            pass

        # Custom user caching
        if self._api.use_cache:
            cache_hits: Dict[str, list] = {'id': [], 'login': []}
            for key, users in tuple(params.items()):
                for user in users:
                    cache_key: str = f'helix.users.{key}.{user}'
                    cache_data: dict = API.SHARED_CACHE.get(cache_key)
                    if cache_data:
                        self._data.append(helix.User(api=self._api, data=cache_data))
                        cache_hits[key].append(user)

            # Remove cached users from params
            params['id'], params['login'] = [
                [n for n in params[key] if n not in cache_hits[key]] for key in ['id', 'login']
            ]

        # Fetch non-cached users from API
        if len(params['id'] + params['login']):
            for data in self._api.get(self._path, params=params, ignore_cache=True)['data']:

                # Create and append user)
                user = helix.User(api=self._api, data=data)
                self._data.append(user)

                # Save to cache
                if self._api.use_cache:
                    API.SHARED_CACHE.set(f'helix.users.login.{user.login}', data)
                    API.SHARED_CACHE.set(f'helix.users.id.{user.id}', data)


    def _can_paginate(self) -> bool:
        return False

    def _handle_pagination_response(self, response: dict) -> None:
        pass

    def _pagination_stream_done(self) -> None:
        pass

    def videos(self, **kwargs) -> Generator[Tuple['helix.User', 'helix.Videos'], None, None]:
        for user in self:
            yield user, user.videos(**kwargs)

    @property
    def streams(self) -> Generator[Tuple['helix.User', 'helix.Stream'], None, None]:
        for user in self:
            yield user, user.stream
