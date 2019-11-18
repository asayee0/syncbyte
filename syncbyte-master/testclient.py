from unittest import TestCase
from musicplayer_client import *

class TestHostMethods(TestCase):
    def test_clientConnect(self):
        self.assertRaises(Exception, clientConnect())