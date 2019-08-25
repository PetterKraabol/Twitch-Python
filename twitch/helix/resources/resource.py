from abc import abstractmethod
from typing import Optional, List, Generator, Generic, TypeVar

import requests

from twitch.api import API
from twitch.baseresource import BaseResource

T = TypeVar('T')


class Resource(BaseResource, Generic[T]):

    def __init__(self, path: str, api: API, data: Optional[List[T]] = None, **kwargs):
        super().__init__(path=path, api=api, data=data, **kwargs)
        self._cursor: Optional[str] = None

    def __iter__(self) -> Generator[T, None, None]:
        # Yield available data
        if self._data:
            for entry in self._data:
                yield entry
            return

        # Check if iterator should paginate from api
        if self._can_paginate() is False:
            return

        # Remaining elements. Download all if set to None
        remaining: Optional[int] = self._kwargs.get('first', None)

        # When downloading add data, set first to maximum to minimize api calls
        if remaining is None:
            self._kwargs['first'] = BaseResource.FIRST_API_LIMIT

        # Paginate
        while remaining is None or remaining > 0:
            # Update remaining
            if remaining:
                self._kwargs['first'] = min(Resource.FIRST_API_LIMIT, remaining)

            # API Response
            try:
                response: dict = self._next_page()
            except requests.exceptions.HTTPError:
                return

            # Let resource handle pagination response and return elements
            elements: List[T] = self._handle_pagination_response(response)
            for element in elements:
                yield element

            # Decrement remaining if not None
            if remaining is not None:
                remaining = 0 if len(elements) > remaining else remaining - self._kwargs['first']

            # If no next cursor, stop
            if not self._cursor:
                break

    def __getitem__(self, index: int) -> T:
        if len(self._data) > index:
            return self._data[index]

        for i, value in enumerate(self._data):
            if i == index:
                return value

    @abstractmethod
    def _can_paginate(self) -> bool:
        """
        Check if resource can be paginated
        :return: Can paginate
        """
        return True

    @abstractmethod
    def _handle_pagination_response(self, response: dict) -> List[T]:
        """
        Pagination hook for every iteration
        :param response: Response from pagination
        :return: None
        """
        elements: List[T] = [T(api=self._api, data=data) for data in response['data']]

        return elements

    def _next_page(self, ignore_cache: bool = False) -> dict:
        """
        API Pagination
        Get next page from API
        :param ignore_cache: Whether to ignore API cache.
        :return: Response
        """
        # API Response
        self._kwargs['after'] = self._cursor

        response: dict = self._api.get(self._path, params=self._kwargs, ignore_cache=ignore_cache)

        # Set pagination cursor
        self._cursor = response.get('pagination', {}).get('cursor', None)

        return response
