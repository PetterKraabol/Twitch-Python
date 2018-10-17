from typing import List

import twitch.helix as helix
from twitch.api import API


class Commenter:

    def __init__(self, data: dict = None):
        self.data: dict = data

        self.display_name: str = None
        self._id: str = None
        self.name: str = None
        self.type: str = None
        self.bio: str = None
        self.created_at: str = None
        self.updated_at: str = None
        self.logo: str = None

        for key, value in data.items():
            if key not in self.__dict__:
                return

            self.__dict__[key] = value


class Emoticon:

    def __init__(self, data: dict = None):
        self.data: dict = data

        self._id: str = None
        self.begin: int = None
        self.end: int = None
        self.emoticon_id: str = None
        self.emoticon_set_id: str = None

        for key, value in data.items():
            if key not in self.__dict__:
                return

            self.__dict__[key] = value


class Fragment:

    def __init__(self, data: dict = None):
        self.data: dict = data

        self.text: str = None
        self.emoticon: Emoticon = None

        for key, value in data.items():
            if key not in self.__dict__:
                return

            if key == 'emoticon':
                self.__dict__[key] = Emoticon(value)
            else:
                self.__dict__[key] = value


class UserBadge:

    def __init__(self, data: dict = None):
        self.data: dict = data

        self._id: str = None
        self.version: str = None

        for key, value in data.items():
            if key not in self.__dict__:
                return

            self.__dict__[key] = value


class Message:

    def __init__(self, data: dict = None):
        self.data: dict = data

        self.body: str = None
        self.emoticons: List[Emoticon] = []
        self.fragments: List[Fragment] = []
        self.is_action: bool = None
        self.user_badges: List[UserBadge] = []
        self.user_color: str = None

        for key, value in data.items():
            if key not in self.__dict__:
                return

            if key == 'emoticons':
                self.__dict__[key] = [Emoticon(data=data) for data in value]
            elif key == 'fragments':
                self.__dict__[key] = [Fragment(data=data) for data in value]
            elif key == 'user_badges':
                self.__dict__[key] = [UserBadge(data=data) for data in value]
            else:
                self.__dict__[key] = value


class Comment:

    def __init__(self, api: API, data: dict):
        self._api: API = api
        self.data: dict = data

        self.id: str = None
        self.created_at: str = None
        self.updated_at: str = None
        self.channel_id: str = None
        self.content_type: str = None
        self.content_id: str = None
        self.content_offset_seconds: float = None
        self.commenter: Commenter = None
        self.source: str = None
        self.state: str = None
        self.message: Message = None
        self.more_replies: bool = None

        for key, value in data.items():
            if key not in list(self.__dict__.keys()) + ['_id']:
                return

            if key == '_id':
                self.__dict__['id'] = value
            if key == 'commenter':
                self.__dict__[key] = Commenter(data=value)
            elif key == 'message':
                self.__dict__[key] = Message(data=value)
            else:
                self.__dict__[key] = value

    def user(self) -> 'helix.User':
        return helix.Helix(client_id=self._api.client_id).user(self.commenter.id)
