import tracemalloc
import unittest
from typing import Dict, Any

import responses

import twitch

tracemalloc.start()


class TestHelixUser(unittest.TestCase):
    user: Dict[str, Dict[str, Any]] = {
        'zarlach': {
            'id': '24250859',
            'login': 'zarlach',
            'display_name': 'Zarlach',
            'type': '',
            'broadcaster_type': '',
            'description': '',
            'profile_image_url': 'https://static-cdn.jtvnw.net/jtv_user_pictures/zarlach-profile_image-1cb98e7eadb5918a-300x300.png',
            'offline_image_url': 'https://static-cdn.jtvnw.net/jtv_user_pictures/zarlach-channel_offline_image-f2d036ac9582d793-1920x1080.png',
            'view_count': 1664
        },
        'sodapoppin': {
            'id': '26301881',
            'login': 'sodapoppin',
            'display_name': 'sodapoppin',
            'type': '',
            'broadcaster_type': 'partner',
            'description': 'Wtf do i write here? Click my stream, or i scream.',
            'profile_image_url': 'https://static-cdn.jtvnw.net/jtv_user_pictures/sodapoppin-profile_image-10049b6200f90c14-300x300.png',
            'offline_image_url': 'https://static-cdn.jtvnw.net/jtv_user_pictures/7ed72b04-897e-4a85-a3c9-2a8ba74aeaa7-channel_offline_image-1920x1080.jpg',
            'view_count': 276164750
        }
    }

    def setUp(self) -> None:
        responses.add(responses.GET, 'https://api.twitch.tv/helix/users?login=zarlach',
                      match_querystring=True,
                      json={'data': [TestHelixUser.user['zarlach']]})
        responses.add(responses.GET, 'https://api.twitch.tv/helix/users?login=sodapoppin',
                      match_querystring=True,
                      json={'data': [TestHelixUser.user['sodapoppin']]})

        responses.add(responses.GET, 'https://api.twitch.tv/helix/users?id=24250859&login=sodapoppin',
                      match_querystring=True,
                      json={'data': [TestHelixUser.user['zarlach'], TestHelixUser.user['sodapoppin']]})

        responses.add(responses.GET, 'https://api.twitch.tv/helix/users?login=sodapoppin&login=zarlach',
                      match_querystring=True,
                      json={'data': [TestHelixUser.user['zarlach'], TestHelixUser.user['sodapoppin']]})

    @responses.activate
    def test_user(self):
        helix = twitch.Helix('client-id', use_cache=True)

        # Get display name to display name
        self.assertEqual(helix.user('zarlach').display_name, 'Zarlach')

    @responses.activate
    def test_users(self):
        # Should returned cached data from above
        helix = twitch.Helix('client-id', use_cache=True)

        for user, display_name in zip(helix.users([24250859, 'sodapoppin']), ['Zarlach', 'sodapoppin']):
            self.assertEqual(user.display_name, display_name)

    @responses.activate
    def test_custom_user_cache(self):
        helix = twitch.Helix('client-id', use_cache=True)
        helix.users(['zarlach', 'sodapoppin'])

        # Users have custom caching, such that url should not be cached
        self.assertFalse(helix.api.SHARED_CACHE.has('GET:https://api.twitch.tv/helix/users?login=zarlach'))

        # Cache entries by login name and id number
        self.assertTrue(helix.api.SHARED_CACHE.has('helix.users.login.zarlach'))
        self.assertTrue(helix.api.SHARED_CACHE.has('helix.users.id.24250859'))

        self.assertTrue(helix.api.SHARED_CACHE.has('helix.users.login.sodapoppin'))
        self.assertTrue(helix.api.SHARED_CACHE.has('helix.users.id.26301881'))

        # Flush cache to remove
        helix.api.flush_cache()

        # Check cache flush
        self.assertFalse(helix.api.SHARED_CACHE.has('helix.users.login.zarlach'))
        self.assertFalse(helix.api.SHARED_CACHE.has('helix.users.id.24250859'))

        self.assertFalse(helix.api.SHARED_CACHE.has('helix.users.login.sodapoppin'))
        self.assertFalse(helix.api.SHARED_CACHE.has('helix.users.id.26301881'))
