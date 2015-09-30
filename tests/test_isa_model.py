__author__ = 'dj'
import unittest
from api.io.isa_v1_model import *

class TestISAModel(unittest.TestCase):

    def setUp(self):
        """Create an empty ISAModel object"""
        isa_model = Investigation()
        isa_model.title = "Growth control of the eukaryote cell: a systems biology study in yeast"
        isa_model.description = ""
        pass

