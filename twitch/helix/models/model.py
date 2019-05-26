from abc import ABCMeta
from dataclasses import dataclass
from typing import Optional, Dict, Any

from twitch.api import API


@dataclass
class Model(metaclass=ABCMeta):
    _api: Optional[API]
    data: Dict[str, Any]
