from rx.subjects import Subject

import twitch
import twitch.chat as chat


class Chat(Subject):

    def __init__(self, channel: str, nickname: str, oauth: str, helix: 'twitch.Helix' = None):
        super().__init__()
        self.helix: 'twitch.Helix' = helix

        self.irc = chat.IRC(nickname, password=oauth)
        self.irc.incoming.subscribe(self._message_handler)
        self.irc.start()

        self.channel = channel
        self.irc.incoming.subscribe()
        self.joined: bool = False

    def _message_handler(self, data: bytes) -> None:
        if not self.joined:
            self.irc.join_channel(self.channel)
            self.joined = True

        message = data.decode("UTF-8").strip('\n\r')

        if message.find('PRIVMSG') >= 0:
            name = message.split('!', 1)[0][1:]
            message = message.split('PRIVMSG', 1)[1].split(':', 1)[1]

            self.on_next(chat.Message(channel=self.channel, sender=name, text=message, helix_api=self.helix))

    def __del__(self):
        self.dispose()
