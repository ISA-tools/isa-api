import os
from isatools.convert.isatab2cedar import ISATab2CEDAR
import unittest
import shutil
from isatools.tests import utils
import json
import tempfile


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestIsaTab2Cedar(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._json_data_dir = utils.JSON_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab2cedar_convert_bii_i_1(self):
        test_case = 'BII-I-1'
        isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        isa2cedar.createCEDARjson(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, True)
        with open(os.path.join(self._json_data_dir, 'cedar', test_case + '.json')) as expected_file, \
                open(os.path.join(self._tmp_dir, test_case + '.json')) as actual_file:
            expected_json = json.load(expected_file)
            actual_json = json.load(actual_file)
            utils.strip_ids(expected_json)
            utils.strip_ids(actual_json)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2cedar_convert_bii_s_3(self):
        test_case = 'BII-S-3'
        isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        isa2cedar.createCEDARjson(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, True)
        with open(os.path.join(self._json_data_dir, 'cedar', test_case + '.json')) as expected_file, \
                open(os.path.join(self._tmp_dir, test_case + '.json')) as actual_file:
            expected_json = json.load(expected_file)
            actual_json = json.load(actual_file)
            utils.strip_ids(expected_json)
            utils.strip_ids(actual_json)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2cedar_convert_bii_s_7(self):
        test_case = 'BII-S-7'
        isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        isa2cedar.createCEDARjson(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, True)
        with open(os.path.join(self._json_data_dir, 'cedar', test_case + '.json')) as expected_file, \
                open(os.path.join(self._tmp_dir, test_case + '.json')) as actual_file:
            expected_json = json.load(expected_file)
            actual_json = json.load(actual_file)
            utils.strip_ids(expected_json)
            utils.strip_ids(actual_json)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2cedar_convert_charac_param_factor(self):
        test_case = 'TEST-ISA-charac-param-factor'
        isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        isa2cedar.createCEDARjson(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, True)
        with open(os.path.join(self._json_data_dir, 'cedar', test_case + '.json')) as expected_file, \
                open(os.path.join(self._tmp_dir, test_case + '.json')) as actual_file:
            expected_json = json.load(expected_file)
            actual_json = json.load(actual_file)
            utils.strip_ids(expected_json)
            utils.strip_ids(actual_json)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2cedar_convert_mtbls1(self):
        test_case = 'MTBLS1'
        isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        isa2cedar.createCEDARjson(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, True)
        with open(os.path.join(self._json_data_dir, 'cedar', test_case + '.json')) as expected_file, \
                open(os.path.join(self._tmp_dir, '1425901783014' + '.json')) as actual_file:
            expected_json = json.load(expected_file)
            actual_json = json.load(actual_file)
            utils.strip_ids(expected_json)
            utils.strip_ids(actual_json)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2cedar_convert_mtbls2(self):
        test_case = 'MTBLS2'
        isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        isa2cedar.createCEDARjson(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, True)
        with open(os.path.join(self._json_data_dir, 'cedar', test_case + '.json')) as expected_file, \
                open(os.path.join(self._tmp_dir, test_case + '.json')) as actual_file:
            expected_json = json.load(expected_file)
            actual_json = json.load(actual_file)
            utils.strip_ids(expected_json)
            utils.strip_ids(actual_json)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2cedar_convert_mtbls3(self):
        test_case = 'MTBLS3'
        isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        isa2cedar.createCEDARjson(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, True)
        with open(os.path.join(self._json_data_dir, 'cedar', test_case + '.json')) as expected_file, \
                open(os.path.join(self._tmp_dir, test_case + '.json')) as actual_file:
            expected_json = json.load(expected_file)
            actual_json = json.load(actual_file)
            utils.strip_ids(expected_json)
            utils.strip_ids(actual_json)
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


