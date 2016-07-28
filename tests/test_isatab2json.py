import os
import unittest
from isatools.convert import isatab2json
import json
import shutil
from tests import utils


class TestIsaTab2Json(unittest.TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)
        self._data_dir = os.path.join(self._dir, 'data')
        self._tmp = os.path.join(self._dir, 'tmp')
        if not os.path.exists(self._tmp):
            os.mkdir(self._tmp)

    def tearDown(self):
        shutil.rmtree(self._tmp)

    def test_isatab2json_convert_charac_param_factor(self):
        test_case = 'TEST-ISA-charac-param-factor'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_repeated_measure(self):
        test_case = 'TEST-ISA-repeated-measure'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_sample_pool(self):
        test_case = 'TEST-ISA-sample-pool'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_sample_pool_with_error(self):
        test_case = 'TEST-ISA-sample-pool-with-error'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_source_split(self):
        test_case = 'TEST-ISA-source-split'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_source_split_with_error(self):
        test_case = 'TEST-ISA-source-split-with-error'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_s_3(self):
        test_case = 'BII-S-3'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._data_dir, test_case, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_s_7(self):
        test_case = 'BII-S-7'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._data_dir, test_case, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_i_1(self):
        test_case = 'BII-I-1'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._data_dir, test_case, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

