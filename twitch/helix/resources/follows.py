from typing import List, Optional

import twitch.helix as helix
from twitch.api import API
from .resource import Resource


class Follows(Resource['helix.Follow']):
    FOLLOWING: int = 1
    FOLLOWED: int = 2

    def __init__(self, api: API, follow_type: 1, **kwargs: Optional):
        super().__init__(api=api, path='users/follows')
        self._kwargs = kwargs
        self.follow_type: int = follow_type

    def _can_paginate(self) -> bool:
        return True

    def _handle_pagination_response(self, response: dict) -> List['helix.Follow']:
        return [helix.Follow(api=self._api, data=follow) for follow in response.get('data', [])]

    @property
    def total(self) -> int:
        return self._api.get(self._path, params={**self._kwargs, **{'first': 100}}).get('total', -1)

    @property
    def users(self) -> 'helix.Users':
        user_ids: List[int] = []
        if self.follow_type == 'followers':
            user_ids = [int(follow.from_id) for follow in self]
        elif self.follow_type == 'followings':
            user_ids = [int(follow.to_id) for follow in self]

        return helix.Users(self._api, user_ids)
