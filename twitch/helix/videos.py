from typing import List, Union, Tuple, Generator

import twitch.helix as helix
import twitch.v5 as v5
from twitch.api import API
from twitch.resource import Resource


class Videos(Resource[helix.Video]):
    DEFAULT_FIRST: int = 20
    MAX_FIRST: int = 100

    def __init__(self,
                 api: API,
                 video_ids: Union[str, int, List[Union[str, int]]] = None,
                 **kwargs):
        super().__init__(api=api, path='videos')

        self._kwargs = kwargs

        if video_ids:
            self._kwargs['id'] = list(set(video_ids))
            self._download_video_ids(**self._kwargs)
        else:
            # Limit videos if first parameter is specified.
            # If not limit is specified, the pagination cursor
            # is used to continuously fetch videos.

            # The Helix API has a maximum of 100 videos per API call.
            # To fetch >100, we split the request in chunks of =<100 videos
            first: int = kwargs['first'] if 'first' in kwargs else 0

            while first > 0:
                kwargs['first'] = min(Videos.MAX_FIRST, first)
                kwargs['after'] = self._cursor or None
                self._download_by_login(**kwargs)
                first -= kwargs['first']

    def __iter__(self) -> Generator['helix.Video', None, None]:
        # if first or ids are specified, yield data
        # that was downloader in the constructor
        if 'first' in self._kwargs or 'id' in self._kwargs:
            for video in self._data:
                yield video

        else:
            # Fetch the maximum amount of videos from
            # API to minimize the number of requests
            self._kwargs['first'] = Videos.MAX_FIRST

            while True:
                for video in self._videos_fragment(**self._kwargs):
                    yield video

    def __getitem__(self, item: int) -> 'helix.Video':
        for index, value in enumerate(self):
            if index == item:
                return value

    def _videos_fragment(self, ignore_cache: bool = False, **kwargs) -> List['helix.Video']:
        # Set potential cursor
        kwargs['after'] = self._cursor or None

        # API Response
        response: dict = self._api.get(self._path, params=kwargs, ignore_cache=ignore_cache)

        # Set pagination cursor
        self._cursor = response.get('pagination', {}).get('cursor', None)

        # Return video data
        return [helix.Video(api=self._api, data=video) for video in response['data']]

    def _download_video_ids(self, **kwargs):
        # Custom video caching
        if self._api.use_cache:
            cache_hits: list = []
            for video_id in list(kwargs['id']):
                cache_key: str = f'helix.video.{video_id}'
                cache_data: dict = API.SHARED_CACHE.get(cache_key)
                if cache_data:
                    self._data.append(helix.Video(api=self._api, data=cache_data))
                    cache_hits.append(video_id)

            kwargs['id'] = [n for n in kwargs['id'] if n not in cache_hits]

        # Download from API
        if len(kwargs['id']):
            # Video data
            # Ignore cache, as we want to cache individual videos and not a collection of videos.
            for video in self._videos_fragment(ignore_cache=True, **kwargs):
                self._data.append(video)

                # Save individual videos to cache
                if self._api.use_cache:
                    API.SHARED_CACHE.set(f'helix.videos.{video.id}', video.data)

    def _download_by_login(self, **kwargs):
        self._data.extend(self._videos_fragment(**kwargs))

    def comments(self) -> Generator[Tuple[helix.Video, v5.Comments], None, None]:
        for video in self:
            yield video, video.comments()
