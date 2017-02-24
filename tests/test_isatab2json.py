import os
import unittest
from isatools.convert import isatab2json
import json
from tests import utils
from isatools import isajson
import tempfile
import shutil


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestIsaTab2JsonNewParser(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._json_data_dir = utils.JSON_DATA_DIR
        self.identifier_type = isatab2json.IdentifierType.name
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab2json_convert_bii_i_1(self):
        test_case = 'BII-I-1'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case),
                                          validate_first=False,
                                          use_new_parser=True)
        json.dump(actual_json, open(os.path.join(self._tmp_dir, 'isa.json'), 'w'))
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json,
                                      base_schemas_dir="isa_model_version_1_1_schemas")
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_bii_s_3(self):
        test_case = 'BII-S-3'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case),
                                          validate_first=False,
                                          use_new_parser=True)
        json.dump(actual_json, open(os.path.join(self._tmp_dir, 'isa.json'), 'w'))
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json,
                                      base_schemas_dir="isa_model_version_1_1_schemas")
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_bii_s_7(self):
        test_case = 'BII-S-7'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case),
                                          validate_first=False,
                                          use_new_parser=True)
        json.dump(actual_json, open(os.path.join(self._tmp_dir, 'isa.json'), 'w'))
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json,
                                      base_schemas_dir="isa_model_version_1_1_schemas")
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_mtbls1(self):
        test_case = 'MTBLS1'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case),
                                          validate_first=False,
                                          use_new_parser=True)
        json.dump(actual_json, open(os.path.join(self._tmp_dir, 'isa.json'), 'w'))
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json,
                                      base_schemas_dir="isa_model_version_1_1_schemas")
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_mtbls2(self):
        test_case = 'MTBLS2'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case),
                                          validate_first=False,
                                          use_new_parser=True)
        json.dump(actual_json, open(os.path.join(self._tmp_dir, 'isa.json'), 'w'))
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json,
                                      base_schemas_dir="isa_model_version_1_1_schemas")
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_mtbls3(self):
        test_case = 'MTBLS3'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case),
                                          validate_first=False,
                                          use_new_parser=True)
        json.dump(actual_json, open(os.path.join(self._tmp_dir, 'isa.json'), 'w'))
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json,
                                      base_schemas_dir="isa_model_version_1_1_schemas")
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_sample_pool(self):
        test_case = 'TEST-ISA-sample-pool'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case),
                                          validate_first=False,
                                          use_new_parser=True)
        json.dump(actual_json, open(os.path.join(self._tmp_dir, 'isa.json'), 'w'))
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json,
                                      base_schemas_dir="isa_model_version_1_1_schemas")
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_sample_pool_with_error(self):
        test_case = 'TEST-ISA-sample-pool-with-error'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case),
                                          validate_first=False,
                                          use_new_parser=True)
        json.dump(actual_json, open(os.path.join(self._tmp_dir, 'isa.json'), 'w'))
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json,
                                      base_schemas_dir="isa_model_version_1_1_schemas")
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_source_split(self):
        test_case = 'TEST-ISA-source-split'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case),
                                          validate_first=False,
                                          use_new_parser=True)
        json.dump(actual_json, open(os.path.join(self._tmp_dir, 'isa.json'), 'w'))
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json,
                                      base_schemas_dir="isa_model_version_1_1_schemas")
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_source_split_with_error(self):
        test_case = 'TEST-ISA-source-split-with-error'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case),
                                          validate_first=False,
                                          use_new_parser=True)
        json.dump(actual_json, open(os.path.join(self._tmp_dir, 'isa.json'), 'w'))
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json,
                                      base_schemas_dir="isa_model_version_1_1_schemas")
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_charac_param_factor(self):
        test_case = 'TEST-ISA-charac-param-factor'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case),
                                          validate_first=False,
                                          use_new_parser=True)
        json.dump(actual_json, open(os.path.join(self._tmp_dir, 'isa.json'), 'w'))
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json,
                                      base_schemas_dir="isa_model_version_1_1_schemas")
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_repeated_measure(self):
        test_case = 'TEST-ISA-repeated-measure'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case),
                                          validate_first=False,
                                          use_new_parser=True)
        json.dump(actual_json, open(os.path.join(self._tmp_dir, 'isa.json'), 'w'))
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json,
                                      base_schemas_dir="isa_model_version_1_1_schemas")
            self.assertEqual(len(report['errors']), 0)


class TestIsaTab2JsonIdentifierName(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._json_data_dir = utils.JSON_DATA_DIR

        self.identifier_type = isatab2json.IdentifierType.name

    def tearDown(self):
        pass

    def test_isatab2json_convert_charac_param_factor(self):
        test_case = 'TEST-ISA-charac-param-factor'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), validate_first=False)
        with open(os.path.join(self._json_data_dir, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_repeated_measure(self):
        test_case = 'TEST-ISA-repeated-measure'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), validate_first=False)
        with open(os.path.join(self._json_data_dir, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_sample_pool(self):
        test_case = 'TEST-ISA-sample-pool'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), validate_first=False)
        with open(os.path.join(self._json_data_dir, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_sample_pool_with_error(self):
        test_case = 'TEST-ISA-sample-pool-with-error'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), validate_first=False)
        with open(os.path.join(self._json_data_dir, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_source_split(self):
        test_case = 'TEST-ISA-source-split'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), validate_first=False)
        with open(os.path.join(self._json_data_dir, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_source_split_with_error(self):
        test_case = 'TEST-ISA-source-split-with-error'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), validate_first=False)
        with open(os.path.join(self._json_data_dir, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_s_3(self):
        test_case = 'BII-S-3'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), validate_first=False)
        with open(os.path.join(self._json_data_dir, test_case, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_s_7(self):
        test_case = 'BII-S-7'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), validate_first=False)
        with open(os.path.join(self._json_data_dir, test_case, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_bii_i_1(self):
        test_case = 'BII-I-1'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self.identifier_type, validate_first=False)
        with open(os.path.join(self._json_data_dir, test_case, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_isatab2json_convert_mtbls1(self):
        test_case = 'MTBLS1'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case), self.identifier_type, validate_first=False)
        with open(os.path.join(self._json_data_dir, test_case, test_case + '.json')) as expected_file:
            expected_json = json.load(expected_file)
            self.assertTrue(utils.assert_json_equal(expected_json, actual_json))
