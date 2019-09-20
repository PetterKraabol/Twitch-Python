from datetime import timedelta
from typing import Optional

import twitch.tmi as tmi
from twitch.api import API


class TMI:
    BASE_URL: str = 'https://tmi.twitch.tv/'

    def __init__(self,
                 client_id: str,
                 client_secret: str = None,
                 use_cache: bool = False,
                 cache_duration: Optional[timedelta] = None,
                 handle_rate_limit: bool = True,
                 bearer_token: Optional[str] = None):
        # Format bearer token
        if bearer_token:
            bearer_token = 'Bearer ' + bearer_token.lower().lstrip('bearer').strip()

        self.api = API(TMI.BASE_URL,
                       client_id=client_id,
                       client_secret=client_secret,
                       use_cache=use_cache,
                       cache_duration=cache_duration,
                       handle_rate_limit=handle_rate_limit,
                       bearer_token=bearer_token)

    def chatters(self, user: str) -> 'tmi.Chatters':
        return tmi.Chatters(api=self.api, user=user)
