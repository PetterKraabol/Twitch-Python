from typing import Optional

import twitch
import twitch.helix as helix


class Message:

    def __init__(self,
                 channel: str,
                 sender: str,
                 text: str,
                 helix_api: 'twitch.Helix' = None,
                 chat: 'twitch.Chat' = None):
        self.channel: str = channel
        self.sender: str = sender
        self.text: str = text
        self.helix: 'twitch.Helix' = helix_api
        self.chat: 'twitch.Chat' = chat

    def user(self) -> Optional['helix.User']:
        return self.helix.user(self.sender) if self.helix else None
