import os
import unittest
from isatools.convert import isatab2json
import json
from isatools.tests import utils
from isatools import isajson
from isatools import isatab
import tempfile
import shutil


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the "
                                "ISAdatasets repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestIsaTab2Json(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._json_data_dir = utils.JSON_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab2json_convert_bii_i_1(self):
        test_case = 'BII-I-1'
        actual_json = isatab2json.convert(
            os.path.join(self._tab_data_dir, test_case), validate_first=False,
            use_new_parser=True)
        with open(os.path.join(self._tmp_dir, 'isa.json'), 'w') as out_fp:
            json.dump(actual_json, out_fp)
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json)
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_bii_s_3(self):
        test_case = 'BII-S-3'
        actual_json = isatab2json.convert(
            os.path.join(self._tab_data_dir, test_case), validate_first=False,
            use_new_parser=True)
        with open(os.path.join(self._tmp_dir, 'isa.json'), 'w') as out_fp:
            json.dump(actual_json, out_fp)
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json)
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_bii_s_7(self):
        test_case = 'BII-S-7'
        actual_json = isatab2json.convert(
            os.path.join(self._tab_data_dir, test_case), validate_first=False,
            use_new_parser=True)
        with open(os.path.join(self._tmp_dir, 'isa.json'), 'w') as out_fp:
            json.dump(actual_json, out_fp)
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json)
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_mtbls1(self):
        test_case = 'MTBLS1'
        actual_json = isatab2json.convert(
            os.path.join(self._tab_data_dir, test_case), validate_first=False,
            use_new_parser=True)
        with open(os.path.join(self._tmp_dir, 'isa.json'), 'w') as out_fp:
            json.dump(actual_json, out_fp)
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json)
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_sample_pool(self):
        test_case = 'TEST-ISA-sample-pool'
        actual_json = isatab2json.convert(
            os.path.join(self._tab_data_dir, test_case), validate_first=False,
            use_new_parser=True)
        with open(os.path.join(self._tmp_dir, 'isa.json'), 'w') as out_fp:
            json.dump(actual_json, out_fp)
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json)
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_source_split(self):
        test_case = 'TEST-ISA-source-split'
        actual_json = isatab2json.convert(os.path.join(self._tab_data_dir, test_case),
                                          validate_first=False, use_new_parser=True)
        with open(os.path.join(self._tmp_dir, 'isa.json'), 'w') as out_fp:
            json.dump(actual_json, out_fp)
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json)

            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_charac_param_factor(self):
        test_case = 'TEST-ISA-charac-param-factor'
        actual_json = isatab2json.convert(
            os.path.join(self._tab_data_dir, test_case), validate_first=False,
            use_new_parser=True)
        with open(os.path.join(self._tmp_dir, 'isa.json'), 'w') as out_fp:
            json.dump(actual_json, out_fp)
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json)
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_repeated_measure(self):
        test_case = 'TEST-ISA-repeated-measure'
        actual_json = isatab2json.convert(
            os.path.join(self._tab_data_dir, test_case), validate_first=False,
            use_new_parser=True)
        with open(os.path.join(self._tmp_dir, 'isa.json'), 'w') as out_fp:
            json.dump(actual_json, out_fp)
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json)
            self.assertEqual(len(report['errors']), 0)

    def test_isatab2json_convert_comment(self):
        with open(os.path.join(self._tab_data_dir, 'issue200', 'i_Investigation.txt')) as fp:
            ISA = isatab.load(fp)
            self.assertEqual(ISA.studies[0].assays[0].comments[0].value, "ena")
            self.assertEqual(ISA.ontology_source_references[0].comments[0].name, "onto_comment")
            self.assertEqual(ISA.ontology_source_references[0].comments[0].value, "onto_stuff")
            self.assertEqual(ISA.studies[0].protocols[0].comments[0].value, "another protocol related comment")
            self.assertEqual(ISA.studies[0].protocols[2].comments[0].value, "protocol related comment")
            self.assertEqual(ISA.studies[0].protocols[3].comments[0].value, "")
            self.assertEqual(ISA.studies[0].contacts[0].comments[0].name, "person comment")
            self.assertEqual(ISA.studies[0].factors[0].comments[0].value, "stf_cmt")

        test_case = "issue200"
        actual_json = isatab2json.convert(
                os.path.join(self._tab_data_dir, test_case), validate_first=False,
                use_new_parser=True)
        with open(os.path.join(self._tmp_dir, 'isa.json'), 'w') as out_fp:
            json.dump(actual_json, out_fp)

        with open(os.path.join(self._tmp_dir, 'isa.json')) as isa_json:
            isajson_read = json.load(isa_json)
            self.assertEqual(isajson_read["studies"][0]["filename"], "s_Study id.txt")
            self.assertEqual(isajson_read["studies"][0]["assays"][0]["comments"][0]["value"], "ena")

