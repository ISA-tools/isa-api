import unittest
import os
import shutil
from isatools.convert import json2isatab
from tests.utils import assert_tab_content_equal
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)


class TestJson2IsaTab(unittest.TestCase):

    def setUp(self):
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self._json_data_dir = os.path.join(data_dir, 'json')
        self._tab_data_dir = os.path.join(data_dir, 'tab')
        self._tmp_dir = os.path.join(os.path.dirname(__file__), 'tmp')
        if not os.path.exists(self._tmp_dir):
            os.mkdir(self._tmp_dir)

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_json2isatab_convert_source_split_study_table(self):
        json2isatab.convert(open(os.path.join(self._json_data_dir, 'TEST-ISA-source-split.json')), self._tmp_dir)
        self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 's_TEST-Template1-Splitting.txt')),
                                                 open(os.path.join(self._tab_data_dir, 'TEST-ISA-source-split',
                                                                   's_TEST-Template1-Splitting.txt'))))

    def test_json2isatab_convert_source_split_assay_table(self):
        json2isatab.convert(open(os.path.join(self._json_data_dir, 'TEST-ISA-source-split.json')), self._tmp_dir)
        self.assertTrue(assert_tab_content_equal(
            open(os.path.join(self._tmp_dir, 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')),
            open(os.path.join(self._tab_data_dir, 'TEST-ISA-source-split',
                              'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt'))))

    def test_json2isatab_convert_sample_pool_study_table(self):
        json2isatab.convert(open(os.path.join(self._json_data_dir, 'TEST-ISA-sample-pool.json')), self._tmp_dir)
        self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 's_TEST-Template3-Splitting.txt')),
                                                 open(os.path.join(self._tab_data_dir, 'TEST-ISA-sample-pool',
                                                                   's_TEST-Template3-Splitting.txt'))))

    def test_json2isatab_convert_sample_pool_assay_table(self):
        json2isatab.convert(open(os.path.join(self._json_data_dir, 'TEST-ISA-sample-pool.json')), self._tmp_dir)
        self.assertTrue(assert_tab_content_equal(
            open(os.path.join(self._tmp_dir, 'a_test-template3-splitting_transcription_profiling_DNA_microarray.txt')),
            open(os.path.join(self._tab_data_dir, 'TEST-ISA-sample-pool',
                              'a_test-template3-splitting_transcription_profiling_DNA_microarray.txt'))))

    def test_json2isatab_convert_bii_s_3_investigation(self):
        json2isatab.convert(open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')), self._tmp_dir)
        self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 'i_investigation.txt')),
                                         open(os.path.join(self._tab_data_dir, 'BII-S-3', 'i_gilbert.txt'))))

    def test_json2isatab_convert_bii_s_3_study_table(self):
        json2isatab.convert(open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')), self._tmp_dir)
        self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 's_BII-S-3.txt')),
                                                 open(os.path.join(self._tab_data_dir, 'BII-S-3', 's_BII-S-3.txt'))))

    def test_json2isatab_convert_bii_s_3_assay_table_Tx(self):
        json2isatab.convert(open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')), self._tmp_dir)
        self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 'a_gilbert-assay-Tx.txt')),
                                                 open(os.path.join(self._tab_data_dir, 'BII-S-3',
                                                                   'a_gilbert-assay-Tx.txt'))))

    def test_json2isatab_convert_bii_s_3_assay_table_Gx(self):
        json2isatab.convert(open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')), self._tmp_dir)
        self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 'a_gilbert-assay-Gx.txt')),
                                                 open(os.path.join(self._tab_data_dir, 'BII-S-3',
                                                                   'a_gilbert-assay-Gx.txt'))))