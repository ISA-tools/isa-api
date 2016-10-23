import unittest
import json
from tests import utils
import os


class TestImportSampleData(unittest.TestCase):

    def setUp(self):
        self._json_data_dir = utils.JSON_DATA_DIR

    def test_import_bii_i_1(self):
        test_case = 'BII-I-1'
        with open(os.path.join(utils.JSON_DATA_DIR, test_case, test_case + '.json')) as json_file:
            json_expected = json.load(json_file)
        from isatools.sampledata import bii_i_1
        utils.assert_json_equal(json_expected, bii_i_1.json)


    def test_import_bii_s_3(self):
        test_case = 'BII-S-3'
        with open(os.path.join(utils.JSON_DATA_DIR, test_case, test_case + '.json')) as json_file:
            json_expected = json.load(json_file)
        from isatools.sampledata import bii_s_3
        utils.assert_json_equal(json_expected, bii_s_3.json)

    def test_import_bii_s_7(self):
        test_case = 'BII-S-7'
        with open(os.path.join(utils.JSON_DATA_DIR, test_case, test_case + '.json')) as json_file:
            json_expected = json.load(json_file)
        from isatools.sampledata import bii_s_7
        utils.assert_json_equal(json_expected, bii_s_7.json)
