import unittest
import os
from isatools.io import isa_v1_model
__author__ = 'dj'

from isatools.io import isa_v1_model

class TestISATabReader(unittest.TestCase):

    def setUp(self):
        self._dir = os.path.join(os.path.dirname(__file__), "data")
        self._work_dir = os.path.join(self._dir, "BII-I-1")

    def test_read_isa_tab(self):
        model = isa_v1_model.fromISArchive(self._work_dir)
