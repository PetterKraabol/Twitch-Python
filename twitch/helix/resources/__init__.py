from typing import List, Callable

from .clips import Clips
from .follows import Follows
from .games import Games
from .resource import Resource
from .streams import Streams, StreamNotFound
from .users import Users
from .videos import Videos

__all__: List[Callable] = [
    Follows,
    Games,
    Resource,
    Streams,
    StreamNotFound,
    Users,
    Videos,
]
