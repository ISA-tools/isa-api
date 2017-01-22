import os
import unittest
from isatools.convert import isatab2json, json2isatab
import shutil
import json
from tests import utils
import tempfile


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have clone the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestJsonIsaTabTwoWayConvert(unittest.TestCase):

    def setUp(self):
        self._json_data_dir = utils.JSON_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_json2isatab_isatab2json_2way_convert_sample_pool(self):
        test_case = 'TEST-ISA-sample-pool'
        test_json = open(os.path.join(self._json_data_dir, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp_dir, validate_first=False)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = isatab2json.convert(self._tmp_dir, validate_first=False)
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    def test_json2isatab_isatab2json_2way_convert_source_split(self):
        test_case = 'TEST-ISA-source-split'
        test_json = open(os.path.join(self._json_data_dir, test_case + '.json'))
        json2isatab.convert(test_json, self._tmp_dir, validate_first=False)
        test_json.seek(0)  # reset pointer
        expected_json = json.load(test_json)
        actual_json = isatab2json.convert(self._tmp_dir, validate_first=False)
        self.assertTrue(utils.assert_json_equal(expected_json, actual_json))

    # def test_json2isatab_isatab2json_2way_convert_bii_i_1(self):
    #     #  FIXME: Get error in isatab2json.createUnitsCategories
    #     #  json_item.update(self.createOntologyAnnotation(value_attributes.Unit, value_attributes.Term_Source_REF, value_attributes.Term_Accession_Number))
    #     #  AttributeError: 'Attrs' object has no attribute 'Term_Source_REF'
    #     #  Are Units always OntologyAnnotations? (i.e. Unit column alway accompanied by Term Accession and
    #     #  Term Source REF?
    #     test_case = 'BII-I-1'
    #     test_json = open(os.path.join(self._json_data_dir, test_case, test_case + '.json'))
    #     json2isatab.convert(test_json, self._tmp_dir)
    #     test_json.seek(0)  # reset pointer
    #     expected_json = json.load(test_json)
    #     actual_json = isatab2json.convert(self._tmp_dir)
    #     self.assertTrue(utils.assert_json_equal(expected_json, actual_json))
    #
    # def test_json2isatab_isatab2json_2way_convert_bii_s_3(self):
    #     #  FIXME: Get error in isatab2json.createUnitsCategories
    #     #  json_item.update(self.createOntologyAnnotation(value_attributes.Unit, value_attributes.Term_Source_REF, value_attributes.Term_Accession_Number))
    #     #  AttributeError: 'Attrs' object has no attribute 'Term_Source_REF'
    #     #  Are Units always OntologyAnnotations? (i.e. Unit column alway accompanied by Term Accession and
    #     #  Term Source REF? If so, related to below bii_s_7 error
    #     test_case = 'BII-S-3'
    #     test_json = open(os.path.join(self._json_data_dir, test_case, test_case + '.json'))
    #     json2isatab.convert(test_json, self._tmp_dir)
    #     test_json.seek(0)  # reset pointer
    #     expected_json = json.load(test_json)
    #     actual_json = isatab2json.convert(self._tmp_dir)
    #     self.assertTrue(utils.assert_json_equal(expected_json, actual_json))
    #
    # def test_json2isatab_isatab2json_2way_convert_bii_s_7(self):
    #     #  FIXME: It reports a big diff because when doing json2isatab, if Term Accession and Term Source REF columns
    #     #  are empty it strips them out. When going back from isatab2json, it converts as string and not
    #     #  OntologyAnnotation since there is no extra info to be able to cast back to original
    #     test_case = 'BII-S-7'
    #     test_json = open(os.path.join(self._json_data_dir, test_case, test_case + '.json'))
    #     json2isatab.convert(test_json, self._tmp_dir)
    #     test_json.seek(0)  # reset pointer
    #     expected_json = json.load(test_json)
    #     actual_json = isatab2json.convert(self._tmp_dir)
    #     self.assertTrue(utils.assert_json_equal(expected_json, actual_json))