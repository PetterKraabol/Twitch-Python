from typing import List, Union, Tuple, Generator

import twitch.helix as helix
import twitch.v5 as v5
from twitch.api import API
from .resource import Resource


class VideosAPIException(Exception):
    pass


class Videos(Resource['helix.Video']):
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
            self._download_video_ids()

    def _can_paginate(self) -> bool:
        """
        Kwargs must include user_id or game_id
        :return: If resource can paginate
        """
        # todo: maybe raise VideosAPIException('A user_id or a game_id must be specified.')
        return len([key for key in self._kwargs.keys() if key in ['user_id', 'game_id']]) == 1

    def _cache_videos(self, videos: List['helix.Video']) -> None:
        """
        Custom video cache
        Cache individual videos
        :param videos: Helix videos
        :return: None
        """
        if self._api.use_cache:
            for video in videos:
                API.SHARED_CACHE.set(f'{Videos.CACHE_PREFIX}{video.id}', video.data)

    def _handle_pagination_response(self, response: dict) -> List['helix.Video']:
        """
        Custom handling for video pagination
        :param response: API response data
        :return: Videos
        """
        videos: List['helix.Video'] = [helix.Video(api=self._api, data=video) for video in response['data']]
        self._cache_videos(videos)

        return videos

    def _next_videos_page(self, ignore_cache: bool = False) -> List['helix.Video']:
        """
        Video pagination
        :param ignore_cache: Ignore API cache
        :return: Videos
        """
        response: dict = self._next_page(ignore_cache=ignore_cache)

        return self._handle_pagination_response(response)

    def _cache_download(self, video_ids: List[int]) -> List[int]:
        """
        Fetch data from cache
        :param video_ids: Lookup the video ids
        :return: Cache hits (video ids)
        """
        cache_hits: list = []
        for video_id in video_ids:
            cache_data: dict = API.SHARED_CACHE.get(f'{Videos.CACHE_PREFIX}{video_id}')
            if cache_data:
                self._data.append(helix.Video(api=self._api, data=cache_data))
                cache_hits.append(video_id)

        return cache_hits

    def _download_video_ids(self) -> None:
        """
        Download videos by list of video IDs
        :return:
        """
        # Custom cache lookup
        if self._api.use_cache:
            cache_hits: List[int] = self._cache_download(self._kwargs['id'])

            # Removed cached ids from kwargs
            self._kwargs['id'] = [n for n in self._kwargs['id'] if n not in cache_hits]

        # Download uncached videos from API
        if len(self._kwargs['id']) > 0:

            # When the number of IDs exceeds API limitations, divide into multiple requests
            remaining_video_ids: list = self._kwargs['id']

            while remaining_video_ids:
                self._kwargs['id'] = remaining_video_ids[:Videos.ID_API_LIMIT]

                # Ignore default caching method, as we want to cache individual videos and not a collection of videos.
                videos: List[helix.Video] = self._next_videos_page(ignore_cache=True)

                # Save videos
                self._data.extend(videos)

                # Update remaining video ids
                remaining_video_ids = [] if len(videos) < len(remaining_video_ids) else remaining_video_ids[
                                                                                        Videos.ID_API_LIMIT:]

    @property
    def comments(self) -> Generator[Tuple['helix.Video', 'v5.Comments'], None, None]:
        for video in self:
            yield video, video.comments
