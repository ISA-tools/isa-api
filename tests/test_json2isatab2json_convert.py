import os
import unittest
from isatools.convert import isatab2json, json2isatab
import shutil
import json
from tests import utils
import tempfile


class TestJsonIsaTabTwoWayConvert(unittest.TestCase):

    def setUp(self):
        self._json_data_dir = utils.JSON_DATA_DIR
        self._unit_json_data_dir = utils.UNIT_JSON_DATA_DIR
        self._configs_json_data_dir = utils.JSON_DEFAULT_CONFIGS_DATA_DIR
        self._sra_data_dir = utils.SRA_DATA_DIR
        self._sra_configs_dir = utils.DEFAULT2015_XML_CONFIGS_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_json2isatab_isatab2json_2way_convert_sample_pool(self):
        test_case = 'TEST-ISA-sample-pool'
        test_json = open(os.path.join(self._json_data_dir, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp_dir)
        isatab2json.convert(self._tmp_dir, self._tmp_dir)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_json2isatab_isatab2json_2way_convert_source_split(self):
        test_case = 'TEST-ISA-source-split'
        test_json = open(os.path.join(self._json_data_dir, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp_dir)
        isatab2json.convert(self._tmp_dir, self._tmp_dir)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_json2isatab_isatab2json_2way_convert_repeated_measure(self):
        test_case = 'TEST-ISA-repeated-measure'
        test_json = open(os.path.join(self._json_data_dir, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp_dir)
        isatab2json.convert(self._tmp_dir, self._tmp_dir)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_json2isatab_isatab2json_2way_convert_charac_param_factor(self):
        test_case = 'TEST-ISA-charac-param-factor'
        test_json = open(os.path.join(self._json_data_dir, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp_dir)
        isatab2json.convert(self._tmp_dir, self._tmp_dir)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_json2isatab_isatab2json_2way_convert_bii_i_1(self):
        test_case = 'BII-I-1'
        test_json = open(os.path.join(self._json_data_dir, test_case, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp_dir)
        isatab2json.convert(self._tmp_dir, self._tmp_dir)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_json2isatab_isatab2json_2way_convert_bii_s_3(self):
        test_case = 'BII-S-3'
        test_json = open(os.path.join(self._json_data_dir, test_case, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp_dir)
        isatab2json.convert(self._tmp_dir, self._tmp_dir)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_json2isatab_isatab2json_2way_convert_bii_s_7(self):
        test_case = 'BII-S-7'
        test_json = open(os.path.join(self._json_data_dir, test_case, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp_dir)
        isatab2json.convert(self._tmp_dir, self._tmp_dir)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))