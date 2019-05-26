from typing import Optional, List

from twitch.api import API
from twitch.helix.resources.resource import T
from .resource import Resource


class Clips(Resource['helix.Clip']):

    def __init__(self, api: API, **kwargs: Optional):
        super().__init__(api=api, path='users/follows')
        self._kwargs = kwargs

    def _can_paginate(self) -> bool:
        return False

    def _handle_pagination_response(self, response: dict) -> List[T]:
        pass
