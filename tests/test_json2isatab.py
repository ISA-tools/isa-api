# coding: utf-8
import os
import unittest
import shutil
import json
import tempfile
import functools
import contextlib
import six

from isatools.convert import json2isatab
from tests.utils import assert_tab_content_equal
from tests import utils

# This will remove the "'U' flag is deprecated" DeprecationWarning in Python3
open = functools.partial(open, mode='r') if six.PY3 else functools.partial(open, mode='rU')


class TestJson2IsaTab(unittest.TestCase):

    def setUp(self):
        self._json_data_dir = utils.JSON_DATA_DIR
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_json2isatab_convert_source_split_study_table(self):
        with open(os.path.join(self._json_data_dir, 'TEST-ISA-source-split.json')) as test_file:
            json2isatab.convert(test_file, self._tmp_dir)

        with open(os.path.join(self._tab_data_dir, 'TEST-ISA-source-split',
                               's_TEST-Template1-Splitting.txt')) as expected_file:
            with open(os.path.join(self._tmp_dir, 's_TEST-Template1-Splitting.txt')) as dumped_file:
                self.assertTrue(assert_tab_content_equal(expected_file, dumped_file))


    def test_json2isatab_convert_source_split_assay_table(self):
        with open(os.path.join(self._json_data_dir, 'TEST-ISA-source-split.json')) as test_file:
            json2isatab.convert(test_file, self._tmp_dir)

        with open(os.path.join(self._tab_data_dir, 'TEST-ISA-source-split',
                              'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')) as expected_file:
            with open(os.path.join(self._tmp_dir, 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')) as dumped_file:
                self.assertTrue(assert_tab_content_equal(expected_file, dumped_file))


    def test_json2isatab_convert_sample_pool_study_table(self):
        with open(os.path.join(self._json_data_dir, 'TEST-ISA-sample-pool.json')) as test_file:
            json2isatab.convert(test_file, self._tmp_dir)
        with open(os.path.join(self._tab_data_dir, 'TEST-ISA-sample-pool', 's_TEST-Template3-Splitting.txt')) as expected_file:
            with open(os.path.join(self._tmp_dir, 's_TEST-Template3-Splitting.txt')) as dumped_file:
                self.assertTrue(assert_tab_content_equal(expected_file, dumped_file))


    def test_json2isatab_convert_sample_pool_assay_table(self):
        with open(os.path.join(self._json_data_dir, 'TEST-ISA-sample-pool.json')) as test_file:
            json2isatab.convert(test_file, self._tmp_dir)
        with open(os.path.join(self._tab_data_dir, 'TEST-ISA-sample-pool',
                              'a_test-template3-splitting_transcription_profiling_DNA_microarray.txt')) as expected_file:
            with open(os.path.join(self._tmp_dir, 'a_test-template3-splitting_transcription_profiling_DNA_microarray.txt')) as dumped_file:
                self.assertTrue(assert_tab_content_equal(expected_file, dumped_file))

    def test_json2isatab_convert_bii_s_3_investigation(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')) as test_file:
            json2isatab.convert(test_file, self._tmp_dir, i_file_name='i_gilbert.txt')
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as dumped_file:
            with open(os.path.join(self._tab_data_dir, 'BII-S-3', 'i_gilbert.txt')) as expected_file:
                self.assertTrue(assert_tab_content_equal(dumped_file, expected_file))

    def test_json2isatab_convert_bii_s_3_study_table(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')) as test_file:
            json2isatab.convert(test_file, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 's_BII-S-3.txt')) as dumped_file:
            with open(os.path.join(self._tab_data_dir, 'BII-S-3', 's_BII-S-3.txt')) as expected_file:
                self.assertTrue(assert_tab_content_equal(dumped_file, expected_file))

    def test_json2isatab_convert_bii_s_3_assay_table_Tx(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')) as test_file:
            json2isatab.convert(test_file, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 'a_gilbert-assay-Tx.txt')) as dumped_file:
            with open(os.path.join(self._tab_data_dir, 'BII-S-3', 'a_gilbert-assay-Tx.txt')) as expected_file:
                self.assertTrue(assert_tab_content_equal(dumped_file, expected_file))

    def test_json2isatab_convert_bii_s_3_assay_table_Gx(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')) as test_file:
            json2isatab.convert(test_file, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 'a_gilbert-assay-Gx.txt')) as dumped_file:
            with open(os.path.join(self._tab_data_dir, 'BII-S-3','a_gilbert-assay-Gx.txt')) as expected_file:
                self.assertTrue(assert_tab_content_equal(dumped_file, expected_file))

    def test_json2isatab_convert_bii_s_7_investigation(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-7', 'BII-S-7.json')) as test_file:
            json2isatab.convert(test_file, self._tmp_dir, i_file_name='i_matteo.txt')
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as dumped_file:
            with open(os.path.join(self._tab_data_dir, 'BII-S-7', 'i_matteo.txt')) as expected_file:
                self.assertTrue(assert_tab_content_equal(dumped_file, expected_file))

    def test_json2isatab_convert_bii_s_7_study_table(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-7', 'BII-S-7.json')) as test_file:
            json2isatab.convert(test_file, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 's_BII-S-7.txt')) as dumped_file:
            with open(os.path.join(self._tab_data_dir, 'BII-S-7', 's_BII-S-7.txt')) as expected_file:
                self.assertTrue(assert_tab_content_equal(dumped_file, expected_file))

    def test_json2isatab_convert_bii_s_7_assay_table_Gx(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-7', 'BII-S-7.json')) as test_file:
            json2isatab.convert(test_file, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 'a_matteo-assay-Gx.txt')) as dumped_file:
            with open(os.path.join(self._tab_data_dir, 'BII-S-7','a_matteo-assay-Gx.txt')) as expected_file:
                self.assertTrue(assert_tab_content_equal(dumped_file,expected_file))

    # def test_json2isatab_convert_bii_i_1_investigation(self):
    #     json2isatab.convert(open(os.path.join(self._json_data_dir, 'BII-I-1', 'BII-I-1.json')), self._tmp_dir)
    #     self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 'i_investigation.txt')),
    #                                              open(os.path.join(self._tab_data_dir, 'BII-I-1', 'i_investigation.txt'))))
    #
    # def test_json2isatab_convert_bii_i_1_study_table(self):
    #     json2isatab.convert(open(os.path.join(self._json_data_dir, 'BII-I-1', 'BII-I-1.json')), self._tmp_dir)
    #     self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 's_BII-S-1.txt')),
    #                                              open(os.path.join(self._tab_data_dir, 'BII-I-1', 's_BII-S-1.txt'))))
    #
    # def test_json2isatab_convert_bii_i_1_study2_table(self):
    #     json2isatab.convert(open(os.path.join(self._json_data_dir, 'BII-I-1', 'BII-I-1.json')), self._tmp_dir)
    #     self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 's_BII-S-2.txt')),
    #                                              open(os.path.join(self._tab_data_dir, 'BII-I-1', 's_BII-S-2.txt'))))
    #
    # def test_json2isatab_convert_bii_i_1_assay_table_metabolome(self):
    #     json2isatab.convert(open(os.path.join(self._json_data_dir, 'BII-I-1', 'BII-I-1.json')), self._tmp_dir)
    #     self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 'a_metabolome.txt')),
    #                                              open(os.path.join(self._tab_data_dir, 'BII-I-1',
    #                                                                'a_metabolome.txt'))))
    #
    # def test_json2isatab_convert_bii_i_1_assay_table_microarray(self):
    #     json2isatab.convert(open(os.path.join(self._json_data_dir, 'BII-I-1', 'BII-I-1.json')), self._tmp_dir)
    #     self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 'a_microarray.txt')),
    #                                              open(os.path.join(self._tab_data_dir, 'BII-I-1',
    #                                                                'a_microarray.txt'))))
    #
    # def test_json2isatab_convert_bii_i_1_assay_table_proteome(self):
    #     json2isatab.convert(open(os.path.join(self._json_data_dir, 'BII-I-1', 'BII-I-1.json')), self._tmp_dir)
    #     self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 'a_proteome.txt')),
    #                                              open(os.path.join(self._tab_data_dir, 'BII-I-1',
    #                                                                'a_proteome.txt'))))
    #
    # def test_json2isatab_convert_bii_i_1_assay_table_transcriptome(self):
    #     json2isatab.convert(open(os.path.join(self._json_data_dir, 'BII-I-1', 'BII-I-1.json')), self._tmp_dir)
    #     self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 'a_transcriptome.txt')),
    #                                              open(os.path.join(self._tab_data_dir, 'BII-I-1',
    #                                                                'a_transcriptome.txt'))))
