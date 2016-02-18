from unittest import TestCase
import os
import shutil
from isatools.convert import json2isatab
import pandas as pd
from pandas.util.testing import assert_frame_equal
import numpy as np


class JsonToTabTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)
        self._tmp = os.path.join(self._dir, './tmp/')
        if not os.path.exists(self._tmp):
            os.mkdir(self._tmp)

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)
        pass

    def _assert_study_tables_equal(self, df_x, df_y):
        try:
            # drop empty columns
            df_x = df_x.replace('', np.nan)
            df_x = df_x.dropna(axis=1, how='all')
            df_y = df_y.replace('', np.nan)
            df_y = df_y.dropna(axis=1, how='all')

            # Shuffles columns and sorts by source and sample names
            df_x = df_x.sort_index(axis=1).sort_values(by=['Source Name', 'Sample Name']).reset_index(drop=True)
            df_x_cols = list()
            i = 0
            for c in df_x.columns:
                df_x_cols.append(c.split('.')[0] + '.' + str(i))
                i += 1
            df_x.columns = df_x_cols

            df_y = df_y.sort_index(axis=1).sort_values(by=['Source Name', 'Sample Name']).reset_index(drop=True)
            df_y_cols = list()
            i = 0
            for c in df_y.columns:
                df_y_cols.append(c.split('.')[0] + '.' + str(i))
                i += 1
            df_y.columns = df_y_cols

            assert_frame_equal(df_x, df_y)
            return True
        except AssertionError as e:
            print(e)
            return False

    def _assert_assay_tables_equal(self, df_x, df_y):
        try:
            # Shuffles columns and sorts by sample name only
            df_x = df_x.replace('', np.nan)
            df_x = df_x.dropna(axis=1, how='all')
            df_y = df_y.replace('', np.nan)
            df_y = df_y.dropna(axis=1, how='all')

            df_x = df_x.sort_index(axis=1).sort_values(by=['Sample Name']).reset_index(drop=True)
            df_x_cols = list()
            for c in df_x.columns:
                df_x_cols.append(c.split('.')[0])
            df_x.columns = df_x_cols

            df_y = df_y.sort_index(axis=1).sort_values(by=['Sample Name']).reset_index(drop=True)
            df_y_cols = list()
            for c in df_y.columns:
                df_y_cols.append(c.split('.')[0])
            df_y.columns = df_y_cols

            assert_frame_equal(df_x, df_y)
            return True
        except AssertionError as e:
            print(e)
            return False

    def test_source_split_study_table(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-source-split.json')), self._tmp)
        test_study_df = pd.read_csv(open(os.path.join(self._tmp, 's_TEST-Template1-Splitting.txt')), sep='\t')
        ref_study_df = pd.read_csv(open(os.path.join(self._dir, 'data/TEST-ISA-source-split/s_TEST-Template1-Splitting.txt')), sep='\t')
        self.assertTrue(self._assert_study_tables_equal(test_study_df, ref_study_df))

    def test_source_split_assay_table(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-source-split.json')), self._tmp)
        test_study_df = pd.read_csv(open(os.path.join(self._tmp, 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')), sep='\t')
        ref_study_df = pd.read_csv(open(os.path.join(self._dir, 'data/TEST-ISA-source-split/a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')), sep='\t')
        self.assertTrue(self._assert_assay_tables_equal(test_study_df, ref_study_df))

    def test_sample_pool_study_table(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-sample-pool.json')), self._tmp)
        test_study_df = pd.read_csv(open(os.path.join(self._tmp, 's_TEST-Template3-Splitting.txt')), sep='\t')
        ref_study_df = pd.read_csv(open(os.path.join(self._dir, 'data/TEST-ISA-sample-pool/s_TEST-Template3-Splitting.txt')), sep='\t')
        self.assertTrue(self._assert_study_tables_equal(test_study_df, ref_study_df))

    def test_sample_pool_assay_table(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-sample-pool.json')), self._tmp)
        test_study_df = pd.read_csv(open(os.path.join(self._tmp, 'a_test-template3-splitting_transcription_profiling_DNA_microarray.txt')), sep='\t')
        ref_study_df = pd.read_csv(open(os.path.join(self._dir, 'data/TEST-ISA-sample-pool/a_test-template3-splitting_transcription_profiling_DNA_microarray.txt')), sep='\t')
        self.assertTrue(self._assert_assay_tables_equal(test_study_df, ref_study_df))
    #
    # def test_bii_s_3_study_table(self):
    #     json2isatab.convert(open('/Users/dj/PycharmProjects/isa-api/isatools/sampledata/BII-S-3.json'), self._tmp)
    #     test_study_df = pd.read_csv(open(os.path.join(self._tmp, 's_BII-S-3.txt')), sep='\t')
    #     ref_study_df = pd.read_csv(open(os.path.join(self._dir, '/Users/dj/PycharmProjects/isa-api/tests/data/BII-S-3/s_BII-S-3.txt')), sep='\t')
    #     self.assertTrue(self._assert_study_tables_equal(test_study_df, ref_study_df))

    # def test_bii_s_3_assay_table_Tx(self):
    #     json2isatab.convert(open('/Users/dj/PycharmProjects/isa-api/isatools/sampledata/BII-S-3.json'), self._tmp)
    #     test_study_df = pd.read_csv(open(os.path.join(self._tmp, 'a_gilbert-assay-Tx.txt')), sep='\t')
    #     ref_study_df = pd.read_csv(open(os.path.join(self._dir, '/Users/dj/PycharmProjects/isa-api/tests/data/BII-S-3/a_gilbert-assay-Tx.txt')), sep='\t')
    #     self.assertTrue(self._assert_assay_tables_equal(test_study_df, ref_study_df))
    #
    # def test_bii_s_3_assay_table_Gx(self):
    #     json2isatab.convert(open('/Users/dj/PycharmProjects/isa-api/isatools/sampledata/BII-S-3.json'), self._tmp)
    #     test_study_df = pd.read_csv(open(os.path.join(self._tmp, 'a_gilbert-assay-Gx.txt')), sep='\t')
    #     ref_study_df = pd.read_csv(open(os.path.join(self._dir, '/Users/dj/PycharmProjects/isa-api/tests/data/BII-S-3/a_gilbert-assay-Gx.txt')), sep='\t')
    #     self.assertTrue(self._assert_assay_tables_equal(test_study_df, ref_study_df))


    # Below tests don't work yet...

    # def test_charac_param_factor_study_table(self):
    #     json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-charac-param-factor.json')), self._tmp)
    #     test_study_df = pd.read_csv(open(os.path.join(self._tmp, 's_TEST-Template1-Splitting.txt')), sep='\t')
    #     ref_study_df = pd.read_csv(open(os.path.join(self._dir, 'data/TEST-ISA-charax-param-factor/s_TEST-Template1-Splitting.txt')), sep='\t')
    #     self.assertTrue(self._assert_study_tables_equal(test_study_df, ref_study_df))
    #
    # def test_charac_param_factor_study_table(self):
    #     json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-charac-param-factor.json')), self._tmp)
    #     test_study_df = pd.read_csv(open(os.path.join(self._tmp, 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')), sep='\t')
    #     ref_study_df = pd.read_csv(open(os.path.join(self._dir, 'data/TEST-ISA-charax-param-factor/a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')), sep='\t')
    #     self.assertTrue(self._assert_assay_tables_equal(test_study_df, ref_study_df))

    # def test_repeated_measure_study_table(self):
    #     json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-repeated-measure.json')), self._tmp)
    #     test_study_df = pd.read_csv(open(os.path.join(self._tmp, 's_TEST-Template5-repeatedmeasure.txt')), sep='\t')
    #     ref_study_df = pd.read_csv(open(os.path.join(self._dir, 'data/TEST-ISA-repeated-measure/s_TEST-Template5-repeatedmeasure.txt')), sep='\t')
    #     self.assertTrue(self._assert_study_tables_equal(test_study_df, ref_study_df))
    #     if not self._assert_study_tables_equal(test_study_df, ref_study_df):
    #         print(test_study_df)
    #
    # def test_repeated_measure_assay_table(self):
    #     json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-repeated-measure.json')), self._tmp)
    #     test_study_df = pd.read_csv(open(os.path.join(self._tmp, 'a_test-template5-repeatedmeasure_transcription_profiling_DNA_microarray.txt')), sep='\t')
    #     ref_study_df = pd.read_csv(open(os.path.join(self._dir, 'data/TEST-ISA-repeated-measure/a_test-template5-repeatedmeasure_transcription_profiling_DNA_microarray.txt')), sep='\t')
    #     self.assertTrue(self._assert_assay_tables_equal(test_study_df, ref_study_df))

    # def test_data_transformation_study_table(self):
    #     pass