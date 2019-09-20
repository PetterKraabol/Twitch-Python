from typing import Union, Generator

import twitch.v5 as v5
from twitch.api import API
from twitch.baseresource import BaseResource


class Comments(BaseResource['v5.Comment']):

    def __init__(self, api: API, video_id: Union[str, int]):
        super().__init__(api=api, path='videos/{video_id}/comments')
        self._video_id: str = str(video_id)
        self._api = api

    def fragment(self, cursor: str = '') -> dict:
        return self._api.get(self._path.format(video_id=self._video_id), params={'cursor': cursor})

    def __iter__(self) -> Generator['v5.Comment', None, None]:
        fragment: dict = {'_next': ''}

        while '_next' in fragment:
            fragment = self.fragment(fragment['_next'])
            for comment in fragment['comments']:
                yield v5.Comment(api=self._api, data=comment)

    def __getitem__(self, item: int) -> 'v5.Comment':
        for index, value in enumerate(self):
            if index == item:
                return value
