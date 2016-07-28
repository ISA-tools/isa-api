import os
import unittest
from isatools.convert import isatab2json, json2isatab
import shutil
import json
from tests import utils


class TestJsonIsaTabTwoWayConvert(unittest.TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)
        self._data_dir = os.path.join(self._dir, 'data')
        self._tmp = os.path.join(self._dir, 'tmp')
        if not os.path.exists(self._tmp):
            os.mkdir(self._tmp)

    def tearDown(self):
        shutil.rmtree(self._tmp)

    def test_json2isatab_isatab2json_2way_convert_sample_pool(self):
        test_case = 'TEST-ISA-sample-pool'
        test_json = open(os.path.join(self._dir, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp)
        isatab2json.convert(self._tmp, self._tmp)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_json2isatab_isatab2json_2way_convert_source_split(self):
        test_case = 'TEST-ISA-source-split'
        test_json = open(os.path.join(self._dir, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp)
        isatab2json.convert(self._tmp, self._tmp)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_json2isatab_isatab2json_2way_convert_repeated_measure(self):
        test_case = 'TEST-ISA-repeated-measure'
        test_json = open(os.path.join(self._dir, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp)
        isatab2json.convert(self._tmp, self._tmp)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_json2isatab_isatab2json_2way_convert_charac_param_factor(self):
        test_case = 'TEST-ISA-charac-param-factor'
        test_json = open(os.path.join(self._dir, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp)
        isatab2json.convert(self._tmp, self._tmp)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_json2isatab_isatab2json_2way_convert_bii_i_1(self):
        test_case = 'BII-I-1'
        test_json = open(os.path.join(self._data_dir, test_case, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp)
        isatab2json.convert(self._tmp, self._tmp)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_json2isatab_isatab2json_2way_convert_bii_s_3(self):
        test_case = 'BII-S-3'
        test_json = open(os.path.join(self._data_dir, test_case, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp)
        isatab2json.convert(self._tmp, self._tmp)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_json2isatab_isatab2json_2way_convert_bii_s_7(self):
        test_case = 'BII-S-7'
        test_json = open(os.path.join(self._data_dir, test_case, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp)
        isatab2json.convert(self._tmp, self._tmp)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))