from typing import Generator, Tuple, List

from twitch.api import API
from twitch.helix.models import Stream, User
from twitch.helix.resources import Resource


class StreamNotFound(Exception):
    pass


class Streams(Resource[Stream]):

    def __init__(self, api: API, **kwargs):
        super().__init__(api=api, path='streams')

        response: dict = self._api.get(self._path, params=kwargs)

        if response['data']:
            self._data = [Stream(api=self._api, data=video) for video in
                          self._api.get(self._path, params=kwargs)['data']]
        else:
            raise StreamNotFound('No stream was found')

    @property
    def users(self) -> Generator[Tuple[Stream, User], None, None]:
        for stream in self:
            yield stream, stream.user

    def _can_paginate(self) -> bool:
        return False

    def _handle_pagination_response(self, response: dict) -> List[Stream]:
        pass
