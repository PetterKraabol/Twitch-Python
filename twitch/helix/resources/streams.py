from typing import Generator, Tuple, List

import twitch.helix as helix
from twitch.api import API
from .resource import Resource


class StreamNotFound(Exception):
    pass


class Streams(Resource['helix.Stream']):

    def __init__(self, api: API, **kwargs):
        super().__init__(api=api, path='streams')

        response: dict = self._api.get(self._path, params=kwargs)

        if response['data']:
            self._data = [helix.Stream(api=self._api, data=video) for video in
                          self._api.get(self._path, params=kwargs)['data']]
        else:
            raise StreamNotFound('No stream was found')

    @property
    def users(self) -> Generator[Tuple['helix.Stream', 'helix.User'], None, None]:
        for stream in self:
            yield stream, stream.user

    def _can_paginate(self) -> bool:
        return False

    def _handle_pagination_response(self, response: dict) -> List['helix.Stream']:
        pass
