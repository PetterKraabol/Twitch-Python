from typing import TypeVar, Generic, List, Optional

from .api import API

T = TypeVar('T')


class BaseResource(Generic[T]):
    FIRST_API_LIMIT: int = 100

    def __init__(self, path: str, api: API, data: Optional[List[T]] = None, **kwargs):
        self._path: str = path
        self._api: Optional[API] = api
        self._data: List[T] = data or []
        self._kwargs: dict = kwargs

    def __iter__(self):
        for item in self._data:
            yield item

    def __getitem__(self, index: int) -> T:
        return self._data[index]
