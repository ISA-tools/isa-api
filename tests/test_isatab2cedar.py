import os
from isatools.convert.isatab2cedar import ISATab2CEDAR
import unittest
import shutil
from tests import utils
import json


class TestIsaTab2Cedar(unittest.TestCase):

    def setUp(self):
        self._tmp_dir = os.path.join(os.path.dirname(__file__), 'tmp')
        if not os.path.exists(self._tmp_dir):
            os.mkdir(self._tmp_dir)
        self._data_dir = os.path.join(os.path.dirname(__file__), 'data', 'tab')

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab2cedar_convert_bii_i_1(self):
        self.fail("Unfinished test code")
        test_case = 'BII-I-1'
        isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        isa2cedar.createCEDARjson(os.path.join(self._data_dir, test_case), self._tmp_dir, True)
        expected_json = json.load(open('path_to_reference_json'))  # TODO: Create reference output JSON
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case)))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2cedar_convert_bii_s_3(self):
        self.fail("Unfinished test code")
        test_case = 'BII-S-3'
        isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        isa2cedar.createCEDARjson(os.path.join(self._data_dir, test_case), self._tmp_dir, True)
        expected_json = json.load(open('path_to_reference_json'))  # TODO: Create reference output JSON
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case)))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2cedar_convert_bii_s_7(self):
        self.fail("Unfinished test code")
        test_case = 'BII-S-7'
        isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        isa2cedar.createCEDARjson(os.path.join(self._data_dir, test_case), self._tmp_dir, True)
        expected_json = json.load(open('path_to_reference_json'))  # TODO: Create reference output JSON
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case)))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2cedar_convert_charac_param_factor(self):
        self.fail("Unfinished test code")
        test_case = 'TEST-ISA-charac-param-factor'
        isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        isa2cedar.createCEDARjson(os.path.join(self._data_dir, test_case), self._tmp_dir, True)
        expected_json = json.load(open('path_to_reference_json'))  # TODO: Create reference output JSON
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case)))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2cedar_convert_mtbls1(self):
        self.fail("Unfinished test code")
        test_case = 'MTBLS1'
        isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        isa2cedar.createCEDARjson(os.path.join(self._data_dir, test_case), self._tmp_dir, True)
        expected_json = json.load(open('path_to_reference_json'))  # TODO: Create reference output JSON
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case)))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2cedar_convert_mtbls2(self):
        self.fail("Unfinished test code")
        test_case = 'MTBLS2'
        isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        isa2cedar.createCEDARjson(os.path.join(self._data_dir, test_case), self._tmp_dir, True)
        expected_json = json.load(open('path_to_reference_json'))  # TODO: Create reference output JSON
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case)))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2cedar_convert_mtbls3(self):
        self.fail("Unfinished test code")
        test_case = 'MTBLS3'
        isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        isa2cedar.createCEDARjson(os.path.join(self._data_dir, test_case), self._tmp_dir, True)
        expected_json = json.load(open('path_to_reference_json'))  # TODO: Create reference output JSON
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case)))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))


    # def test_isatab2cedar_convert_scidata(self):
    #     self.isa2cedar = ISATab2CEDAR("http://www.nature.com/sdata/")
    #     self.folder = os.path.join("/Users/agbeltran/work-dev/isa-explorer/", "data")
    #     self.path = os.path.abspath(self.folder)
    #
    #     # find all subdirectories in self.path directory
    #     self.directories = next(os.walk(self.path))[1]
    #
    #     for directory in self.directories:
    #         print("Converting ", directory, " ...")
    #         self.isa2cedar.createCEDARjson(os.path.join(self.path, directory),
    #                                        os.path.join(self._data_dir, "sdata"), False)
    #     print("\t... done")


