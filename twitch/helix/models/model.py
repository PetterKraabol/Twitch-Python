from abc import ABCMeta
from typing import Optional

from twitch.api import API


class Model(metaclass=ABCMeta):

    def __init__(self, api: API, data: dict):
        self._api: API = api
        self.data: dict = data

    def _populate(self, data: Optional[dict] = None):
        self.data = data or self.data

        for key, value in self.data.items():
            self.__dict__[key] = value
