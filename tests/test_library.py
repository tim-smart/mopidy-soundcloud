from __future__ import unicode_literals

import unittest
from mopidy.models import Ref
import pykka
from mopidy_soundcloud import actor, SoundCloudExtension
from mopidy_soundcloud.library import SoundCloudLibraryProvider


class ApiTest(unittest.TestCase):

    def setUp(self):
        config = SoundCloudExtension().get_config_schema()
        config['auth_token'] = '1-35204-61921957-55796ebef403996'
        # using this user http://maildrop.cc/inbox/mopidytestuser
        self.backend = actor.SoundCloudBackend.start(
            config={'soundcloud': config},
            audio=None
        ).proxy()
        self.library = SoundCloudLibraryProvider(backend=self.backend)

    def tearDown(self):
        pykka.ActorRegistry.stop_all()

    def test_add_folder(self):
        self.assertEquals(
            self.library.new_folder('Test', ['test']),
            Ref(name='Test', type='directory',
                uri='soundcloud:directory:test')
        )

    def test_only_resolves_soundcloud_uris(self):
        self.assertIsNone(self.library.search(
            {'uri': 'http://www.youtube.com/watch?v=wD6H6Yhluo8'}))

    def test_default_folders(self):
        self.assertEquals(
            self.library.browse('soundcloud:directory'),
            [
                Ref(name='Explore', type='directory',
                    uri='soundcloud:directory:explore'),
                Ref(name='Following', type='directory',
                    uri='soundcloud:directory:following'),
                Ref(name='Liked', type='directory',
                    uri='soundcloud:directory:liked'),
                Ref(name='Sets', type='directory',
                    uri='soundcloud:directory:sets'),
                Ref(name='Stream', type='directory',
                    uri='soundcloud:directory:stream')
            ]
        )
