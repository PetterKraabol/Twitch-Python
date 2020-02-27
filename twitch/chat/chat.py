import time
from typing import Optional

from rx.subject import Subject

import twitch
import twitch.chat as chat


class Chat(Subject):

    def __init__(self, channel: str, nickname: str, oauth: str, helix: Optional['twitch.Helix'] = None):
        """
        :param channel: Channel name
        :param nickname: User nickname
        :param oauth: Twitch OAuth
        :param helix: Optional Helix API
        """
        super().__init__()
        self.helix: Optional['twitch.Helix'] = helix

        self.irc = chat.IRC(nickname, password=oauth)
        self.irc.incoming.subscribe(self._message_handler)
        self.irc.start()

        self.channel = channel.lstrip('#')
        self.joined: bool = False

    def _message_handler(self, data: bytes) -> None:
        # First messages are server connection messages,
        # which should be handled by joining the chat room.
        if not self.joined:
            self.irc.join_channel(self.channel)
            self.joined = True

        text = data.decode("UTF-8").strip('\n\r')

        if text.find('PRIVMSG') >= 0:
            sender = text.split('!', 1)[0][1:]
            message = text.split('PRIVMSG', 1)[1].split(':', 1)[1]
            self.on_next(
                chat.Message(channel=self.channel, sender=sender, text=message, helix_api=self.helix, chat=self))

    def send(self, message: str) -> None:
        while not self.joined:
            time.sleep(0.01)
        self.irc.send_message(message=message, channel=self.channel)

    def __del__(self):
        self.irc.active = False
        self.dispose()
