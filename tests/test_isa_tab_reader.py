__author__ = 'dj'
import unittest, os
class TestISATabReader(unittest.TestCase):

    def setUp(self):
        self._dir = os.path.join(os.path.dirname(__file__), "data")

