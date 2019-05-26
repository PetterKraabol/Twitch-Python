from typing import List, Optional

from twitch.api import API
from twitch.helix.models import Game
from twitch.helix.resources import Resource


class Games(Resource[Game]):

    def __init__(self, api: API, **kwargs: Optional):
        super().__init__(api=api, path='games')

        if len(kwargs) > 0:
            self._data = [Game(api=self._api, data=game) for game in
                          self._api.get(self._path, params=kwargs)['data']]

    def top(self, **kwargs) -> List[Game]:
        return [Game(api=self._api, data=game) for game in
                self._api.get(f'{self._path}/top', params=kwargs)['data']]

    def _can_paginate(self) -> bool:
        return False

    def _handle_pagination_response(self, response: dict) -> List[Game]:
        pass
