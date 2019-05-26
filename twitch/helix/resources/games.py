from typing import List, Optional

import twitch.helix as helix
from twitch.api import API
from .resource import Resource


class Games(Resource['helix.Game']):

    def __init__(self, api: API, **kwargs: Optional):
        super().__init__(api=api, path='games')

        if len(kwargs) > 0:
            self._data = [helix.Game(api=self._api, data=game) for game in
                          self._api.get(self._path, params=kwargs)['data']]

    def top(self, **kwargs) -> List['helix.Game']:
        return [helix.Game(api=self._api, data=game) for game in
                self._api.get(f'{self._path}/top', params=kwargs)['data']]

    def _can_paginate(self) -> bool:
        return False

    def _handle_pagination_response(self, response: dict) -> List['helix.Game']:
        pass
