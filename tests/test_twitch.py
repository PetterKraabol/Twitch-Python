import unittest
from datetime import timedelta

import twitch


class TestTwitchPython(unittest.TestCase):

    def test_cache(self):
        helix = twitch.Helix('client-id', use_cache=True)

        helix.api.SHARED_CACHE.set('key', {'data': 'value'})

        # Entry in shared cache
        self.assertTrue(helix.api.SHARED_CACHE.has('key'))

        # Not expired
        self.assertFalse(helix.api.SHARED_CACHE.expired('key'))

        # Expiration
        helix.api.SHARED_CACHE.set('key-with-expiration', {'data': 'value'}, duration=timedelta(seconds=-1))

        # Key is expired
        self.assertTrue(helix.api.SHARED_CACHE.expired('key-with-expiration'))

        # Unable to retrieve expired value
        self.assertFalse(helix.api.SHARED_CACHE.get('key-with-expiration'))

        # Has key, but expired
        self.assertTrue(helix.api.SHARED_CACHE.has('key-with-expiration'))

        # Clean expired keys
        helix.api.SHARED_CACHE.clean()
        self.assertFalse(helix.api.SHARED_CACHE.has('key-with-expiration'))

        # Flush cache
        helix.api.SHARED_CACHE.flush()
        self.assertFalse(helix.api.SHARED_CACHE.has('key'))
