import logging
import socket
import threading
from typing import List

from rx.subject import Subject


class IRC(threading.Thread):

    def __init__(self, nickname: str, password: str, address: str = 'irc.chat.twitch.tv', port: int = 6667):
        super().__init__()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address: str = address
        self.port: int = port
        self.channels: List[str] = []
        self.nickname: str = nickname
        self.password: str = 'oauth:' + password.lstrip('oauth:')
        self.active: bool = True
        self.incoming: Subject = Subject()

    def run(self):
        self.connect()
        self.authenticate()

        while self.active:
            try:
                data = self._read_line()
                text = data.decode("UTF-8").strip('\n\r')

                if text.find('PING') >= 0:
                    self.send_raw('PONG ' + text.split()[1])

                if text.find('Login authentication failed') > 0:
                    logging.fatal('IRC authentication error: ' + text or '')
                    return

                # Publish data to subscribers
                self.incoming.on_next(data)

            except IOError:
                break

    def send_raw(self, message: str) -> None:
        data = (message.lstrip('\n') + '\n').encode('utf-8')
        self.socket.send(data)

    def send_message(self, message: str, channel: str) -> None:
        channel = channel.lstrip('#')
        self.send_raw(f'PRIVMSG #{channel} :{message}')

    def connect(self) -> None:
        self.socket.connect((self.address, self.port))

    def authenticate(self) -> None:
        self.send_raw(f'PASS {self.password}')
        self.send_raw(f'NICK {self.nickname}')

    def join_channel(self, channel: str) -> None:
        channel = channel.lstrip('#')
        self.channels.append(channel)
        self.send_raw(f'JOIN #{channel}')

    def leave_channel(self, channel: str) -> None:
        channel = channel.lstrip('#')
        self.channels.remove(channel)
        self.send_raw(f'PART #{channel}')

    def leave_channels(self, channels: List[str]) -> None:
        channels = [channel.lstrip('#') for channel in channels]
        [self.channels.remove(channel) for channel in channels]
        self.send_raw('PART #' + '#'.join(channels))

    def _read_line(self) -> bytes:
        data: bytes = b''
        while True:
            next_byte: bytes = self.socket.recv(1)
            if next_byte == b'\n':
                break
            data += next_byte

        return data
