from typing import List, Callable

from .game import Game
from .stream import Stream
from .user import User
from .video import Video

__all__: List[Callable] = [Stream, User, Video, Game]
