from twitch.api import API

import twitch.helix.models
from twitch.helix.resources import Users


class Follow(twitch.helix.models.Model):

    def __init__(self, api: API, data: dict):
        super().__init__(api, data)

        self.from_id: str = self.data.get('from_id')
        self.from_name: str = self.data.get('from_name')
        self.to_id: str = self.data.get('to_id')
        self.to_name: str = self.data.get('to_name')
        self.followed_at: str = self.data.get('followed_at')

    @property
    def follower(self) -> 'twitch.helix.User':
        """
        This user follows the followed
        :return: User following the user
        """
        return Users(self._api, int(self.from_id))[0]

    @property
    def followed(self) -> 'twitch.helix.User':
        """
        This user is being followed by the follower
        :return: User being followed
        """
        return Users(self._api, int(self.to_id))[0]
