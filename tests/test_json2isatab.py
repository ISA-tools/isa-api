import unittest
import os
import shutil
from isatools.convert import json2isatab
from isatools.tests.utils import assert_tab_content_equal
from isatools.tests import utils
import tempfile


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestJson2IsaTab(unittest.TestCase):

    def setUp(self):
        self._json_data_dir = utils.JSON_DATA_DIR
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()
    #
    # def tearDown(self):
    #     shutil.rmtree(self._tmp_dir)

    def test_json2isatab_convert_source_split_study_table(self):
        with open(os.path.join(self._json_data_dir, 'TEST-ISA-source-split.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 's_TEST-Template1-Splitting.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'TEST-ISA-source-split', 's_TEST-Template1-Splitting.txt')) \
                    as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_source_split_assay_table(self):
        with open(os.path.join(self._json_data_dir, 'TEST-ISA-source-split.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'TEST-ISA-source-split', 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_sample_pool_study_table(self):
        with open(os.path.join(self._json_data_dir, 'TEST-ISA-sample-pool.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 's_TEST-Template3-Splitting.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'TEST-ISA-sample-pool', 's_TEST-Template3-Splitting.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_sample_pool_assay_table(self):
        with open(os.path.join(self._json_data_dir, 'TEST-ISA-sample-pool.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir, validate_first=False)
            with open(os.path.join(self._tmp_dir, 'a_test-template3-splitting_transcription_profiling_DNA_microarray.txt')) as out_fp:
                with open(os.path.join(self._tab_data_dir, 'TEST-ISA-sample-pool', 'a_test-template3-splitting_transcription_profiling_DNA_microarray.txt')) as reference_fp:
                    self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_bii_s_3_investigation(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir, i_file_name='i_gilbert.txt', validate_first=False)
        with open(os.path.join(self._tmp_dir, 'i_gilbert.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'BII-S-3', 'i_gilbert.txt'))as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_bii_s_3_study_table(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 's_BII-S-3.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'BII-S-3', 's_BII-S-3.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))
    #
    def test_json2isatab_convert_bii_s_3_assay_table_Tx(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 'a_gilbert-assay-Tx.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'BII-S-3', 'a_gilbert-assay-Tx.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_bii_s_3_assay_table_Gx(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 'a_gilbert-assay-Gx.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'BII-S-3_written_by_isatab', 'a_gilbert-assay-Gx.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_bii_s_7_investigation(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-7', 'BII-S-7.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir, i_file_name='i_matteo.txt', validate_first=False)
        with open(os.path.join(self._tmp_dir, 'i_matteo.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'BII-S-7', 'i_matteo.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_bii_s_7_study_table(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-7', 'BII-S-7.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 's_BII-S-7.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'BII-S-7', 's_BII-S-7.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_bii_s_7_assay_table_Gx(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-7', 'BII-S-7.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 'a_matteo-assay-Gx.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'BII-S-7', 'a_matteo-assay-Gx.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_validate_first(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-7', 'BII-S-7.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir, validate_first=True)
        
    def test_json2isatab_convert_bii_i_1_investigation(self):
        with open(os.path.join(self._json_data_dir, 'BII-I-1', 'BII-I-1.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'BII-I-1_written_by_isatab', 'i_investigation.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_bii_i_1_study_table(self):
        with open(os.path.join(self._json_data_dir, 'BII-I-1', 'BII-I-1.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 's_BII-S-1.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'BII-I-1_written_by_isatab', 's_BII-S-1.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_bii_i_1_study2_table(self):
        with open(os.path.join(self._json_data_dir, 'BII-I-1', 'BII-I-1.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 's_BII-S-2.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'BII-I-1', 's_BII-S-2.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_bii_i_1_assay_table_metabolome(self):
        with open(os.path.join(self._json_data_dir, 'BII-I-1', 'BII-I-1.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 'a_metabolome.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'BII-I-1_written_by_isatab', 'a_metabolome1.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_bii_i_1_assay_table_microarray(self):
        # FIXME: ArrayExpress comments come out twice (on Assay AND Derived Data File output from assay),
        #  missing Data Transformation Name and Factor Values
        with open(os.path.join(self._json_data_dir, 'BII-I-1', 'BII-I-1.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 'a_microarray.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'BII-I-1_written_by_isatab', 'a_microarray.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_bii_i_1_assay_table_proteome(self):
        # FIXME: Same duplication problem as above
        with open(os.path.join(self._json_data_dir, 'BII-I-1', 'BII-I-1.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 'a_proteome.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'BII-I-1_written_by_isatab', 'a_proteome.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))

    def test_json2isatab_convert_bii_i_1_assay_table_transcriptome(self):
        # FIXME: Has inserted Protocol REFs but Array Design REF, Scan Name, Factor Values
        with open(os.path.join(self._json_data_dir, 'BII-I-1', 'BII-I-1.json')) as json_fp:
            json2isatab.convert(json_fp, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 'a_transcriptome.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'BII-I-1_written_by_isatab', 'a_transcriptome.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))


