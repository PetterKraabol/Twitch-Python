import tracemalloc
import unittest

import responses

import twitch

tracemalloc.start()


class TestHelixVideo(unittest.TestCase):

    @responses.activate
    def test_video(self):
        responses.add(responses.GET, 'https://api.twitch.tv/helix/videos?id=471855782',
                      match_querystring=True,
                      json={
                          'data': [{
                              'id': '471855782',
                              'user_id': '26301881',
                              'user_name': 'sodapoppin',
                              'title': '2 days til Classic, passing the time til then. ',
                              'description': '',
                              'created_at': '2019-08-24T21:34:03Z',
                              'published_at': '2019-08-24T21:34:03Z',
                              'url': 'https://www.twitch.tv/videos/471855782',
                              'thumbnail_url': '',
                              'viewable': 'public',
                              'view_count': 329,
                              'language': 'en',
                              'type': 'archive',
                              'duration': '2h14m55s'}],
                          'pagination': {'cursor': 'eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MX19'}
                      })

        helix = twitch.Helix('client-id', use_cache=True)

        # Get display name to display name
        self.assertEqual(helix.video('471855782').user_name, 'sodapoppin')

    @responses.activate
    def test_first_videos(self):
        responses.add(responses.GET, 'https://api.twitch.tv/helix/users?login=sodapoppin',
                      match_querystring=True,
                      json={
                          'data': [
                              {
                                  'id': '26301881', 'login': 'sodapoppin', 'display_name': 'sodapoppin', 'type': '',
                                  'broadcaster_type': 'partner',
                                  'description': 'Wtf do i write here? Click my stream, or i scream.',
                                  'profile_image_url': 'https://static-cdn.jtvnw.net/jtv_user_pictures/sodapoppin-profile_image-10049b6200f90c14-300x300.png',
                                  'offline_image_url': 'https://static-cdn.jtvnw.net/jtv_user_pictures/7ed72b04-897e-4a85-a3c9-2a8ba74aeaa7-channel_offline_image-1920x1080.jpg',
                                  'view_count': 287171213
                              }]
                      })

        responses.add(responses.GET, 'https://api.twitch.tv/helix/videos?user_id=26301881&first=2',
                      match_querystring=True,
                      json={
                          'data': [
                              {
                                  'id': '471855782', 'user_id': '26301881', 'user_name': 'sodapoppin',
                                  'title': '2 days til Classic, passing the time til then. ', 'description': '',
                                  'created_at': '2019-08-24T21:34:03Z', 'published_at': '2019-08-24T21:34:03Z',
                                  'url': 'https://www.twitch.tv/videos/471855782', 'thumbnail_url': '',
                                  'viewable': 'public', 'view_count': 453, 'language': 'en', 'type': 'archive',
                                  'duration': '2h21m43s'
                              },
                              {
                                  'id': '471295896', 'user_id': '26301881', 'user_name': 'sodapoppin',
                                  'title': '3 days til Classic, passing the time til then. ', 'description': '',
                                  'created_at': '2019-08-23T18:40:05Z', 'published_at': '2019-08-23T18:40:05Z',
                                  'url': 'https://www.twitch.tv/videos/471295896',
                                  'thumbnail_url': 'https://static-cdn.jtvnw.net/s3_vods/7d5ae2c2918cf4ca8579_sodapoppin_35403289856_1281380185/thumb/thumb0-%{width}x%{height}.jpg',
                                  'viewable': 'public', 'view_count': 5892, 'language': 'en', 'type': 'archive',
                                  'duration': '6h4m13s'}],
                          'pagination': {'cursor': 'eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6Mn19'}
                      })

        # Should returned cached data from above
        helix = twitch.Helix('client-id', use_cache=True)

        for video, user_name in zip(helix.user('sodapoppin').videos(first=2), ['sodapoppin', 'sodapoppin']):
            self.assertEqual(video.user_name, user_name)

    @responses.activate
    def test_custom_video_cache(self):
        responses.add(responses.GET, 'https://api.twitch.tv/helix/videos?id=471855782',
                      match_querystring=True,
                      json={
                          'data': [
                              {'id': '471855782',
                               'user_id': '26301881',
                               'user_name': 'sodapoppin',
                               'title': '2 days til Classic, passing the time til then. ',
                               'description': '',
                               'created_at': '2019-08-24T21:34:03Z',
                               'published_at': '2019-08-24T21:34:03Z',
                               'url': 'https://www.twitch.tv/videos/471855782',
                               'thumbnail_url': '',
                               'viewable': 'public',
                               'view_count': 329,
                               'language': 'en',
                               'type': 'archive',
                               'duration': '2h14m55s'}],
                          'pagination': {'cursor': 'eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MX19'}})

        helix = twitch.Helix('client-id', use_cache=True)
        helix.video(471855782)

        # Videos have custom caching, such that url should not be cached
        self.assertFalse(helix.api.SHARED_CACHE.has('GET:https://api.twitch.tv/helix/videos?id=471855782'))

        # Cache entries by video id
        self.assertTrue(helix.api.SHARED_CACHE.has('helix.video.471855782'))

        # Flush cache to remove
        helix.api.flush_cache()

        # Check cache flush (cache should be empty)
        self.assertFalse(helix.api.SHARED_CACHE.has('helix.video.471855782'))
