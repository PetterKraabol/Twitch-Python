from typing import Optional

from twitch.helix import User, Helix
from .chat import Chat


class Message:

    def __init__(self,
                 channel: str,
                 sender: str,
                 text: str,
                 helix_api: Optional[Helix] = None,
                 chat: Optional[Chat] = None):
        self.channel: str = channel
        self.sender: str = sender
        self.text: str = text
        self.helix: Optional[Helix] = helix_api
        self.chat: Optional[Chat] = chat

    @property
    def user(self) -> Optional[User]:
        return self.helix.user(self.sender) if self.helix else None
