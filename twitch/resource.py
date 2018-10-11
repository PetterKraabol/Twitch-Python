from typing import TypeVar, Generic, Generator, List

from twitch.api import API

T = TypeVar('T')


class Resource(Generic[T]):

    def __init__(self, path: str, api: API, data: List[T] = None):
        self._path: str = path
        self._api: API = api
        self._data: List[T] = data or []

    def __iter__(self) -> Generator[T, None, None]:
        for entry in self._data:
            yield entry

    def __getitem__(self, item: int) -> T:
        return self._data[item]
