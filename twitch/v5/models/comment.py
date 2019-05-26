from typing import List, Optional, Dict, Any

import twitch.helix as helix
from twitch.api import API


class Commenter:

    def __init__(self, data: Dict[str, Any]):
        self.data: Dict[str, Any] = data

        self.display_name: str = self.data.get('display_name')
        self.id: str = self.data.get('_id')
        self.name: str = self.data.get('name')
        self.type: str = self.data.get('type')
        self.bio: str = self.data.get('bio')
        self.created_at: str = self.data.get('created_at')
        self.updated_at: str = self.data.get('updated_at')
        self.logo: str = self.data.get('logo')


class Emoticon:

    def __init__(self, data: Dict[str, Any]):
        self.data: Dict[str, Any] = data

        self.id: str = self.data.get('id')
        self.begin: int = self.data.get('begin')
        self.end: int = self.data.get('end')
        self.emoticon_id: str = self.data.get('emoticon_id')
        self.emoticon_set_id: str = self.data.get('emoticon_set_id')


class Fragment:

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self.data: dict = data

        self.text: Optional[str] = self.data.get('text')
        self.emoticon: Optional[Emoticon] = Emoticon(self.data.get('emoticon'))


class UserBadge:

    def __init__(self, data: Dict[str, Any]):
        self.data: Dict[str, Any] = data

        self.id: str = self.data.get('_id')
        self.version: str = self.data.get('version')


class Message:

    def __init__(self, data: Dict[str, Any]):
        self.data: Dict[str, Any] = data

        self.body: str = self.data.get('body')
        self.emoticons: List[Emoticon] = [Emoticon(data) for data in self.data.get('emoticons', [])]
        self.fragments: List[Fragment] = [Fragment(data) for data in self.data.get('fragments', [])]
        self.is_action: bool = self.data.get('is_action')
        self.user_badges: List[UserBadge] = [UserBadge(data) for data in self.data.get('user_badges', [])]
        self.user_color: str = self.data.get('user_color')


class Comment:

    def __init__(self, api: API, data: dict):
        self._api: API = api
        self.data: dict = data

        self.id: str = self.data.get('_id')
        self.created_at: str = self.data.get('created_at')
        self.updated_at: str = self.data.get('updated_at')
        self.channel_id: str = self.data.get('channel_id')
        self.content_type: str = self.data.get('content_type')
        self.content_id: str = self.data.get('content_id')
        self.content_offset_seconds: float = self.data.get('content_offset_seconds')
        self.commenter: Commenter = Commenter(self.data.get('commenter'))
        self.source: str = self.data.get('source')
        self.state: str = self.data.get('state')
        self.message: Message = Message(self.data.get('message'))
        self.more_replies: bool = self.data.get('more_replies')

    def user(self) -> 'helix.User':
        return helix.Helix(client_id=self._api.client_id).user(int(self.commenter.id))
