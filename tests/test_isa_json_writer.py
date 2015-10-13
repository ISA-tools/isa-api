__author__ = 'dj'
import unittest, os
from isatools.io import isa_v1_model

class TestISATabWriter(unittest.TestCase):

    def setUp(self):
        self._dir = os.path.join(os.path.dirname(__file__), "data")
        self._work_dir = os.path.join(self._dir, "tmp")

    def test_read_isa_tab(self):
        model = isa_v1_model.create()
        #populate ISA model object with stuff
        #model.title = "Title of ISA"
        #model.writeISArchive(self._work_dir)
