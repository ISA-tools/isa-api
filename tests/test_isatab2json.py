__author__ = 'agbeltran'

import os
from isatools.convert.isatab2json import ISATab2ISAjson_v1
import unittest


class ISAtab2jsonTest(unittest.TestCase):

      def setUp(self):
        self._dir = os.path.dirname(__file__)
        print(self._dir)


      def test_bii_i_1_conversion(self):
        self.isatab2json = ISATab2ISAjson_v1()
        test_data_dir = os.path.join(self._dir, "./data/BII-I-1")
        self.sample_data_dir = os.path.join(self._dir, "../isatools/sampledata/")
        self.isatab2json.convert(test_data_dir, self.sample_data_dir, True)
