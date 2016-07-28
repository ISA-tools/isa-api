import os
from unittest import TestCase
from isatools.convert import isatab2json
import json
import shutil
from tests import utils


class ISAtab2jsonTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)
        self._data_dir = os.path.join(self._dir, 'data')
        self._tmp = os.path.join(self._dir, 'tmp')
        if not os.path.exists(self._tmp):
            os.mkdir(self._tmp)

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_isa_charac_param_factor(self):
        test_case = 'TEST-ISA-charac-param-factor'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isa_repeated_measure_conversion(self):
        test_case = 'TEST-ISA-repeated-measure'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isa_sample_pool_conversion(self):
        test_case = 'TEST-ISA-sample-pool'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isa_sample_pool_with_error_conversion(self):
        test_case = 'TEST-ISA-sample-pool-with-error'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isa_source_split_conversion(self):
        test_case = 'TEST-ISA-source-split'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isa_source_split_with_error_conversion(self):
        test_case = 'TEST-ISA-source-split-with-error'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_bii_s_3_conversion(self):
        test_case = 'BII-S-3'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._data_dir, test_case, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_bii_s_7_conversion(self):
        test_case = 'BII-S-7'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._data_dir, test_case, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_bii_i_1_conversion(self):
        test_case = 'BII-I-1'
        isatab2json.convert(os.path.join(self._data_dir, test_case), self._tmp, isatab2json.IdentifierType.name)
        expected_json = json.load(open(os.path.join(self._data_dir, test_case, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

