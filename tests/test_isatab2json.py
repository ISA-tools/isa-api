# coding: utf-8
import os
import unittest
import shutil
import json
import tempfile
import functools
import six

from isatools.convert import isatab2json
from tests import utils

# This will remove the "'U' flag is deprecated" DeprecationWarning in Python3
open = functools.partial(open, mode='r') if six.PY3 else functools.partial(open, mode='rbU')


class TestIsaTab2JsonIdentifierName(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._tab_data_dir = utils.TAB_DATA_DIR
        cls._json_data_dir = utils.JSON_DATA_DIR
        cls.identifier_type = isatab2json.IdentifierType.name

    def test_isatab2json_convert_charac_param_factor(self):
        test_case = 'TEST-ISA-charac-param-factor'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self.identifier_type)
        with open(os.path.join(self._json_data_dir, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_repeated_measure(self):
        test_case = 'TEST-ISA-repeated-measure'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self.identifier_type)
        with open(os.path.join(self._json_data_dir, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_sample_pool(self):
        test_case = 'TEST-ISA-sample-pool'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self.identifier_type)
        with open(os.path.join(self._json_data_dir, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_sample_pool_with_error(self):
        test_case = 'TEST-ISA-sample-pool-with-error'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self.identifier_type)
        with open(os.path.join(self._json_data_dir, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_source_split(self):
        test_case = 'TEST-ISA-source-split'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self.identifier_type)
        with open(os.path.join(self._json_data_dir, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_source_split_with_error(self):
        test_case = 'TEST-ISA-source-split-with-error'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self.identifier_type)
        with open(os.path.join(self._json_data_dir, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_s_3(self):
        test_case = 'BII-S-3'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self.identifier_type)
        with open(os.path.join(self._json_data_dir, test_case, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_s_7(self):
        test_case = 'BII-S-7'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self.identifier_type)
        with open(os.path.join(self._json_data_dir, test_case, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_i_1(self):
        test_case = 'BII-I-1'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self.identifier_type)
        with open(os.path.join(self._json_data_dir, test_case, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_mtbls1(self):
        test_case = 'MTBLS1'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self.identifier_type)
        with open(os.path.join(self._json_data_dir, test_case, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

"""

    The below tests are commented out as IdentifierType using uuid or counter is not stable.
    The issues with these modes are mainly to do with the typing information being embedded into
    the identifiers when using IdentifierType.name that cannot be picked up in other ID modes.
    Another issue will be on how to test effectively on uuid and counter IdentifierTypes as these
    may not provide canonical output.

class TestIsaTab2JsonIdentifierUuid(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._json_data_dir = utils.JSON_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

        self.identifier_type = isatab2json.IdentifierType.uuid

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab2json_convert_charac_param_factor(self):
        test_case = 'TEST-ISA-charac-param-factor'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_repeated_measure(self):
        test_case = 'TEST-ISA-repeated-measure'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_sample_pool(self):
        test_case = 'TEST-ISA-sample-pool'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_sample_pool_with_error(self):
        test_case = 'TEST-ISA-sample-pool-with-error'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_source_split(self):
        test_case = 'TEST-ISA-source-split'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_source_split_with_error(self):
        test_case = 'TEST-ISA-source-split-with-error'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_s_3(self):
        test_case = 'BII-S-3'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_s_7(self):
        test_case = 'BII-S-7'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_i_1(self):
        test_case = 'BII-I-1'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))


class TestIsaTab2JsonIdentifierCounter(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._json_data_dir = utils.JSON_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

        self.identifier_type = isatab2json.IdentifierType.counter

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab2json_convert_charac_param_factor(self):
        test_case = 'TEST-ISA-charac-param-factor'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_repeated_measure(self):
        test_case = 'TEST-ISA-repeated-measure'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_sample_pool(self):
        test_case = 'TEST-ISA-sample-pool'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_sample_pool_with_error(self):
        test_case = 'TEST-ISA-sample-pool-with-error'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_source_split(self):
        test_case = 'TEST-ISA-source-split'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_source_split_with_error(self):
        test_case = 'TEST-ISA-source-split-with-error'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_s_3(self):
        test_case = 'BII-S-3'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_s_7(self):
        test_case = 'BII-S-7'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_i_1(self):
        test_case = 'BII-I-1'
        isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self._tmp_dir, self.identifier_type)
        expected_json = json.load(open(os.path.join(self._json_data_dir, test_case, test_case + '.json')))
        actual_json = json.load(open(os.path.join(self._tmp_dir, test_case + '.json')))
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))
"""
