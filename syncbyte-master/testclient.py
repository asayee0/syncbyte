from unittest import TestCase
from musicplayer_client import *
from threading import Thread

class TestHostMethods(TestCase):
    def test_playSong(self):
        self.assertTrue(directorychooser())

    def test_updatelabel(self):
        self.assertTrue(updatelabel())