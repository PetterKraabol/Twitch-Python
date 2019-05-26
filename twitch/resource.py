from typing import TypeVar, Generic, Generator, List, Optional

from twitch.api import API

T = TypeVar('T')


class Resource(Generic[T]):
    FIRST_API_LIMIT: int = 100

    def __init__(self, path: str, api: API, data: Optional[List[T]] = None):
        self._path: str = path
        self._api: API = api
        self._data: List[T] = data or []
        self._cursor: Optional[str] = None
        self._kwargs: dict = {}

    def __iter__(self) -> Generator[T, None, None]:
        # Yield available data
        if self._data:
            for entry in self._data:
                yield entry
            return

        # Stream data from API

        # Set start cursor
        self._cursor = self._kwargs or self._cursor or '0'

        # Set 'first' to limit
        self._kwargs['first'] = Resource.FIRST_API_LIMIT

        # Paginate
        while self._cursor:
            # API Response
            response: dict = self._api.get(self._path, params=self._kwargs)

            # Set pagination cursor
            self._cursor = response.get('pagination', {}).get('cursor', None)

    def __getitem__(self, item: int) -> T:
        return self._data[item]
