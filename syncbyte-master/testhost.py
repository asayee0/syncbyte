from unittest import TestCase
import musicplayer_host

class TestHostMethods(TestCase):
    def test_listenForClient(self):
        self.assertEqual(True, musicplayer_host.listenForClient())

    def test_directoryChooser(self):
        self.assertEqual(True, musicplayer_host.directorychooser())

    def test_updatelabel(self):
        self.assertEqual(True, musicplayer_host.updatelabel())