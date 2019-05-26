from typing import List, Callable

from .v5 import V5
from .models import Comment
from .resources import Comments

__all__: List[Callable] = [
    V5,
    Comment, Comments
]
