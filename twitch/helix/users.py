from typing import List, Union, Generator, Tuple

import twitch.helix as helix
from twitch.api import API
from twitch.resource import Resource


class Users(Resource['User']):

    def __init__(self, api: API, *args):
        super().__init__(api=api, path='users')

        # Load data
        users: List[Union[str, int]] = []
        for user in args:
            users += [user] if type(user) in [str, int] else list(user)

        params: dict = dict()
        params['id'], params['login'] = [list(set(n)) for n in
                                         [[str(user) for user in users if type(user) == x] for x in [int, str]]]

        query: str = '?'
        for param, user_list in params.items():
            for user in user_list:
                query += f'{param}={user}&'

        self._data = [helix.User(api=self._api, data=data) for data in
                      self._api.get(self._path + query.rstrip('&'))['data']]

    def videos(self, **kwargs) -> Generator[Tuple['helix.User', 'helix.Videos'], None, None]:
        for user in self:
            yield user, user.videos(**kwargs)
