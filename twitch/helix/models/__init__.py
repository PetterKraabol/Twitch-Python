from typing import List, Callable

from .follow import Follow
from .game import Game
from .model import Model
from .stream import Stream
from .user import User
from .video import Video

__all__: List[Callable] = [
    Follow,
    Game,
    Model,
    Stream,
    User,
    Video,
]
