import re
from dataclasses import dataclass
from typing import Dict, Any, Optional

import twitch.helix as helix
import twitch.v5 as v5
from twitch.api import API
from .model import Model


@dataclass
class Duration:
    h: int = 0
    m: int = 0
    s: int = 0

    def __str__(self):
        return f'{self.h}h{self.m}m{self.s}s'


class Video(Model):

    def __init__(self, api: API, data: Dict[str, Any]):
        """
        [reference](https://dev.twitch.tv/docs/api/reference#get-videos)
        """
        super().__init__(api, data)

        self.id: str = data.get('id')
        self.stream_id: Optional[str] = data.get('stream_id', None)
        self.user_id: str = data.get('user_id')
        self.user_login: str = data.get('user_login')
        self.user_name: str = data.get('user_name')
        self.title: str = data.get('title')
        self.description: str = data.get('description')
        self.created_at: str = data.get('created_at')
        self.published_at: str = data.get('published_at')
        self.url: str = data.get('url')
        self.thumbnail_url: str = data.get('thumbnail_url')
        self.viewable: str = data.get('viewable')
        self.view_count: int = data.get('view_count')
        self.language: str = data.get('language')
        self.type: str = data.get('type')
        self.duration: str = data.get('duration')

    def __str__(self):
        return self.title

    @property
    def comments(self) -> 'v5.Comments':
        return v5.V5(client_id=self._api.client_id,
                     use_cache=self._api.use_cache,
                     cache_duration=self._api.cache_duration).comments(self.id)

    @property
    def user(self) -> 'helix.User':
        return helix.Users(self._api, int(self.user_id))[0]

    @property
    def duration_fmt(self) -> Duration:
        _ = [0, 0, 0]
        if self.duration:
            if "h" in self.duration:
                regex = r"([\d]+)h([\d]+)m([\d]+)s$"
                matches = re.finditer(regex, self.duration, re.MULTILINE)
                for matchNum, match in enumerate(matches, start=1):
                    if len(match.groups()) == 3:
                        _ = [int(x) for x in match.groups()]
            elif "m" in self.duration:
                regex = r"([\d]+)m([\d]+)s$"
                matches = re.finditer(regex, self.duration, re.MULTILINE)
                for matchNum, match in enumerate(matches, start=1):
                    if len(match.groups()) == 2:
                        _[1] = int(match.groups()[0])
                        _[2] = int(match.groups()[1])
            elif "s" in self.duration:
                regex = r"([\d]+)s$"
                matches = re.finditer(regex, self.duration, re.MULTILINE)
                for matchNum, match in enumerate(matches, start=1):
                    if len(match.groups()) == 1:
                        _[2] = int(match.groups()[0])
        return Duration(**{"h": _[0], "m": _[1], "s": _[2]})
