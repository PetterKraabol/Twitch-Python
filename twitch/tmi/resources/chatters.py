from typing import Generator, List

import twitch.tmi as tmi
from twitch.api import API
from twitch.baseresource import BaseResource


class Chatters(BaseResource['tmi.Chatter']):

    def __init__(self, api: API, user: str):
        super().__init__(api=api, path='group/user/{user}/chatters')
        self._api = api

        # API return data
        self._data = self._api.get(self._path.format(user=user))

        # API Data
        self.count: int = self._data.get('chatter_count', -1)

        self.types: List[str] = list(self._data.get('chatters', {}).keys())

        self.broadcaster: List[tmi.Chatter] = [tmi.Chatter(self._api, name, 'broadcaster') for name in
                                               self._data.get('chatters', {}).get('broadcaster', [])]

        self.vips: List[tmi.Chatter] = [tmi.Chatter(self._api, name, 'vip') for name in
                                        self._data.get('chatters', {}).get('vips', [])]

        self.moderators: List[tmi.Chatter] = [tmi.Chatter(self._api, name, 'moderator') for name in
                                              self._data.get('chatters', {}).get('moderators', [])]

        self.staff: List[tmi.Chatter] = [tmi.Chatter(self._api, name, 'staff') for name in
                                         self._data.get('chatters', {}).get('staff', [])]

        self.admins: List[tmi.Chatter] = [tmi.Chatter(self._api, name, 'admin') for name in
                                          self._data.get('chatters', {}).get('admins', [])]

        self.global_mods: List[tmi.Chatter] = [tmi.Chatter(self._api, name, 'global_mod') for name in
                                               self._data.get('chatters', {}).get('global_mods', [])]

        self.viewers: List[tmi.Chatter] = [tmi.Chatter(self._api, name, 'viewer') for name in
                                           self._data.get('chatters', {}).get('viewers', [])]

    def all(self) -> List[tmi.Chatter]:
        """
        Get all chatters from all groups
        :return: List of all chatters
        """
        return self.broadcaster + self.vips + self.moderators + self.staff + self.admins + self.global_mods + self.viewers

    def __iter__(self) -> Generator['tmi.Chatter', None, None]:
        """
        Iterate over all chatters
        :return: Yield chatter
        """
        for chatter in self.all():
            yield chatter

    def __getitem__(self, index: int) -> 'tmi.Chatter':
        """
        Get chatter by index
        :param index: Index
        :return: Chatter
        """
        return self.all()[index]
