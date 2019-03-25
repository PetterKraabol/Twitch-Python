from typing import Union, Generator

from twitch.api import API
from twitch.baseresource import BaseResource
from .models.comment import Comment


class Comments(BaseResource[Comment]):

    def __init__(self, video_id: Union[str, int], api: API):
        super().__init__(api=api, path='videos/{video_id}/comments')
        self._video_id: str = str(video_id)
        self._api = api

    def fragment(self, cursor: str = '') -> dict:
        return self._api.get(self._path.format(video_id=self._video_id), params={'cursor': cursor})

    def __iter__(self) -> Generator[Comment, None, None]:
        fragment: dict = {'_next': ''}

        while '_next' in fragment:
            fragment = self.fragment(fragment['_next'])
            for comment in fragment['comments']:
                yield Comment(api=self._api, data=comment)

    def __getitem__(self, item: int) -> Comment:
        for index, value in enumerate(self):
            if index == item:
                return value
