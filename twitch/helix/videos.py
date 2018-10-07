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

        if type(video_ids) == list:
            query = '?' + ''.join(f'id={video_id}&' for video_id in set([str(n) for n in video_ids]))

            self._data = [helix.Video(api=self._api, data=data) for data in
                          self._api.get(self._path + query.rstrip('&'))['data']]
        else:
            self._data = [helix.Video(api=self._api, data=video) for video in
                          self._api.get(self._path, params=kwargs)['data']]

    def comments(self) -> Generator[Tuple[helix.Video, v5.Comments], None, None]:
        for video in self:
            yield video, video.comments()
