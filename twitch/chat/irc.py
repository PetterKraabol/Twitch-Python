import socket
import threading
from typing import List

from rx.subjects import Subject


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
                self.incoming.on_next(self._read_line())
            except IOError:
                break

    def send_raw(self, message: str) -> None:
        self.socket.send((message.lstrip('\n') + '\n').encode('utf-8'))

    def send_message(self, message: str) -> None:
        self.send_raw(f'MESSAGE {message}')

    def connect(self):
        self.socket.connect((self.address, self.port))

    def authenticate(self):
        self.send_raw(f'PASS {self.password}')
        self.send_raw(f'NICK {self.nickname}')

    def join_channel(self, channel: str):
        self.send_raw(f'JOIN {channel}')

    def ping(self):
        self.send_raw('PONG')

    def _read_line(self) -> bytes:
        data: bytes = b''
        while True:
            next_byte: bytes = self.socket.recv(1)
            if next_byte == b'\n':
                break
            data += next_byte

        return data
