from typing import Optional

import twitch
import twitch.helix as helix


class Message:

    def __init__(self, channel: str, name: str, message: str, helix: twitch.Helix = None):
        self.channel: str = channel
        self.sender: str = name
        self.text: str = message
        self.helix = helix

    def user(self) -> Optional[helix.User]:
        return self.helix.user(self.sender) if self.helix else None
