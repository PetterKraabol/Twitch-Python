import twitch.helix as helix
from twitch.api import API
from twitch.helix.models.model import Model


class Follow(Model):

    def __init__(self, api: API, data: dict):
        super().__init__(api, data)

        self.from_id: str = None
        self.from_name: str = None
        self.to_id: str = None
        self.to_name: str = None
        self.followed_at: str = None

        # Fill response fields
        self._populate()

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
