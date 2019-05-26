from twitch.api import API
from twitch.helix.resources.users import Users
from .model import Model
from .user import User


class Follow(Model):

    def __init__(self, api: API, data: dict):
        super().__init__(api, data)

        self.from_id: str = data.get('from_id')
        self.from_name: str = data.get('from_name')
        self.to_id: str = data.get('to_id')
        self.to_name: str = data.get('to_name')
        self.followed_at: str = data.get('followed_at')

    @property
    def follower(self) -> User:
        """
        This user follows the followed
        :return: User following the user
        """
        return Users(self._api, int(self.from_id))[0]

    @property
    def followed(self) -> User:
        """
        This user is being followed by the follower
        :return: User being followed
        """
        return Users(self._api, int(self.to_id))[0]
