from typing import List, Union, Tuple, Generator

import twitch.helix as helix
import twitch.v5 as v5
from twitch.api import API
from twitch.resource import Resource


class Videos(Resource[helix.Video]):

    def __init__(self,
                 api: API,
                 video_ids: Union[str, int, List[Union[str, int]]] = None,
                 **kwargs):
        super().__init__(api=api, path='videos')

        if video_ids:
            kwargs['id'] = list(set(video_ids))

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
                for data in self._api.get(self._path, params=kwargs, ignore_cache=True)['data']:

                    # Create and append user
                    video = helix.Video(api=self._api, data=data)
                    self._data.append(video)

                    # Save to cache
                    if self._api.use_cache:
                        API.SHARED_CACHE.set(f'helix.videos.{video.id}', data)
        else:
            self._data = [helix.Video(api=self._api, data=video) for video in
                          self._api.get(self._path, params=kwargs)['data']]

    def comments(self) -> Generator[Tuple[helix.Video, v5.Comments], None, None]:
        for video in self:
            yield video, video.comments()
