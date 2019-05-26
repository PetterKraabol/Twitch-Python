from typing import Dict, Any

import twitch.helix as helix
from twitch.api import API
from .model import Model


class Follow(Model):

    def __init__(self, api: API, data: Dict[str, Any]):
        super().__init__(api, data)

        self.from_id: str = data.get('from_id')
        self.from_name: str = data.get('from_name')
        self.to_id: str = data.get('to_id')
        self.to_name: str = data.get('to_name')
        self.followed_at: str = data.get('followed_at')

    @property
    def follower(self) -> 'helix.User':
        """
        This user follows the followed
        :return: User following the user
        """
        return helix.Users(self._api, int(self.from_id))[0]

    @property
    def followed(self) -> 'helix.User':
        """
        This user is being followed by the follower
        :return: User being followed
        """
        return helix.Users(self._api, int(self.to_id))[0]
