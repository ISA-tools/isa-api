__author__ = 'dj'
import unittest, os
from api.io import isa_factory

class TestISATabReader(unittest.TestCase):

    def setUp(self):
        self._dir = os.path.join(os.path.dirname(__file__), "data")
        self._isa_tab_file = ""
        self._isa_json = ""

    def test_read_isa_tab(self):
        isa_object = isa_factory(self._isa_tab_file)

    def test_read_isa_json(self):
        isa_object = isa_factory(self._isa_json)



