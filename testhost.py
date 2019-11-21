from unittest import TestCase
from musicplayer_host import *

class TestHostMethods(TestCase):
    def test_songPlay(self):
        self.assertTrue(listenForClient())

    def test_directoryChooser(self):
        self.assertTrue(directorychooser())

    def test_updatelabel(self):
        self.assertTrue(updatelabel())