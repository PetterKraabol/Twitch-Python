from typing import List, Union, Tuple, Generator

import twitch.helix as helix
import twitch.v5 as v5
from twitch.api import API
from twitch.resource import Resource


class VideosAPIException(Exception):
    pass


class Videos(Resource[helix.Video]):
    DEFAULT_FIRST: int = 20
    FIRST_API_LIMIT: int = 100
    ID_API_LIMIT: int = 100
    CACHE_PREFIX: str = 'helix.video.'

    def __init__(self,
                 api: API,
                 video_ids: Union[int, List[int]] = None,
                 **kwargs):
        super().__init__(api=api, path='videos')

        # Store kwargs as class property for __iter__
        self._kwargs = kwargs

        # 'id' parameter can be a singular or a list
        # Create list of video ids by combining video_ids and kwargs['id']

        # Convert singular string to list
        if 'id' in self._kwargs and type(self._kwargs['id']) == str:
            self._kwargs['id'] = [self._kwargs['id']]

        self._kwargs['id'] = list(self._kwargs['id']) if 'id' in self._kwargs.keys() else []
        self._kwargs['id'] = self._kwargs['id'] + list(video_ids) if video_ids else self._kwargs['id']

        # Convert to integers
        self._kwargs['id'] = [int(x) for x in self._kwargs['id']]

        # Remove duplicates
        self._kwargs['id'] = list(set(self._kwargs['id'])) if self._kwargs['id'] else []

        # Download video ids
        if len(self._kwargs['id']) > 0:
            self._download_video_ids(**self._kwargs)

        # Download first n videos from a user or game
        elif 'first' in self._kwargs.keys():
            self._download_videos(**self._kwargs)

        # If neither statements are True, videos will be fetched continuously in __iter__

    def __iter__(self) -> Generator['helix.Video', None, None]:
        # If videos were downloaded in the constructor, yield only those
        if self._data:
            for video in self._data:
                yield video
            return

        # Yield a continuous stream of videos from a user id or game id
        if len([key for key in self._kwargs.keys() if key in ['user_id', 'game_id']]) != 1:
            raise VideosAPIException('A user_id or a game_id must be specified.')

        # Fetch the maximum amount of videos from
        # API to minimize the number of requests
        self._kwargs['first'] = Videos.FIRST_API_LIMIT

        while True:
            for video in self._videos_fragment(**self._kwargs):
                yield video

            # Break if no cursor
            if not self._cursor:
                break

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

        # Download videos
        videos: List['helix.Video'] = [helix.Video(api=self._api, data=video) for video in response['data']]

        # Cache individual videos
        if self._api.use_cache:
            for video in videos:
                API.SHARED_CACHE.set(f'{Videos.CACHE_PREFIX}{video.id}', video.data)

        # Return video data
        return videos

    def _download_video_ids(self, **kwargs):
        # Custom cache lookup
        if self._api.use_cache:
            cache_hits: list = []
            for video_id in list(kwargs['id']):
                cache_data: dict = API.SHARED_CACHE.get(f'{Videos.CACHE_PREFIX}{video_id}')
                if cache_data:
                    self._data.append(helix.Video(api=self._api, data=cache_data))
                    cache_hits.append(video_id)

            # Removed cached ids from kwargs
            kwargs['id'] = [n for n in kwargs['id'] if n not in cache_hits]

        # Download uncached videos from API
        if len(kwargs['id']) > 0:

            # When the number of IDs exceeds API limitations, divide into multiple requests
            remaining_video_ids: list = kwargs['id']

            while remaining_video_ids:
                kwargs['id'] = remaining_video_ids[:Videos.ID_API_LIMIT]

                # Ignore default caching method, as we want to cache individual videos and not a collection of videos.
                videos: List['helix.Video'] = self._videos_fragment(ignore_cache=True, **kwargs)
                self._data.extend(videos)

                # Update remaining video ids
                remaining_video_ids = [] if len(videos) < len(remaining_video_ids) else remaining_video_ids[
                                                                                        Videos.ID_API_LIMIT:]

    def _download_videos(self, **kwargs):
        # user_id or game_id must be provided
        if len([key for key in kwargs.keys() if key in ['user_id', 'game_id']]) != 1:
            raise VideosAPIException('A user_id or a game_id must be specified.')

        remaining_videos: int = kwargs['first']

        while remaining_videos:
            kwargs['first'] = min(Videos.FIRST_API_LIMIT, remaining_videos)

            # Use custom and API cache to cache individual and collections of videos
            videos: List['helix.Video'] = self._videos_fragment(ignore_cache=False, **kwargs)
            self._data.extend(videos)

            # Update remaining videos
            remaining_videos = 0 if len(videos) < remaining_videos else remaining_videos - kwargs['first']

    def comments(self) -> Generator[Tuple[helix.Video, v5.Comments], None, None]:
        for video in self:
            yield video, video.comments()
