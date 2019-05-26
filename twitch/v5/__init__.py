from typing import List, Callable

from .models import Comment
from .resources import Comments
from .v5 import V5

__all__: List[Callable] = [
    V5,
    Comment, Comments
]
