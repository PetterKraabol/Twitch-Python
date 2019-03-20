from typing import Generator, Tuple

import twitch.helix as helix
from twitch.api import API
from twitch.resource import Resource


class StreamNotFound(Exception):
    pass


class Streams(Resource['Stream']):

    def __init__(self, api: API, **kwargs):
        super().__init__(api=api, path='streams')

        response: dict = self._api.get(self._path, params=kwargs)

        if response['data']:
            self._data = [helix.Stream(api=self._api, data=video) for video in
                          self._api.get(self._path, params=kwargs)['data']]
        else:
            raise StreamNotFound('No stream was found')

    def users(self) -> Generator[Tuple['helix.Stream', 'helix.User'], None, None]:
        for stream in self:
            yield stream, stream.user()
