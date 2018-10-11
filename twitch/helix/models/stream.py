from typing import List

import twitch.helix as helix
from twitch.api import API


class Stream:

    def __init__(self, api: API, data: dict):
        # Meta
        self._api: API = api
        self.data: dict = data

        # Response fields
        self.id: str = None
        self.user_id: str = None
        self.game_id: str = None
        self.community_ids: List[str] = []
        self.type: str = None
        self.title: str = None
        self.viewer_count: int = None
        self.started_at: str = None
        self.language: str = None
        self.thumbnail_url: str = None

        # Fill response fields
        for key, value in data.items():
            self.__dict__[key] = value

    def user(self) -> 'helix.User':
        return helix.Users(self._api, self.user_id)[0]

    def __str__(self):
        return self.title
