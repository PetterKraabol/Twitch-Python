from twitch.api import API


class Game:

    def __init__(self, api: API, data: dict):
        # Meta
        self._api: API = api
        self.data: dict = data

        # Response fields
        self.id: str = None
        self.name: str = None
        self.box_art_url: str = None

        # Fill response fields
        for key, value in data.items():
            self.__dict__[key] = value

    def __str__(self):
        return self.name
