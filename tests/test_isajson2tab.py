from unittest import TestCase
import os
import shutil
from isatools.convert import json2isatab

class JsonToTabTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)
        self._tmp = os.path.join(self._dir, './tmp/')
        if not os.path.exists(self._tmp):
            os.mkdir(self._tmp)

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _assert_study_tables_equal(self, df_x, df_y):
        from pandas.util.testing import assert_frame_equal
        try:
            # Shuffles columns and sorts by source and sample names
            assert_frame_equal(df_x.sort(axis=1).sort_index(by=['Source Name', 'Sample Name']).reset_index(drop=True),  # Shuffles columns and sorts by material names
                               df_y.sort(axis=1).sort_index(by=['Source Name', 'Sample Name']).reset_index(drop=True))
            return True
        except AssertionError as e:
            print(e)
            return False

    def _assert_assay_tables_equal(self, df_x, df_y):
        from pandas.util.testing import assert_frame_equal
        try:
            # Shuffles columns and sorts by sample name only
            assert_frame_equal(df_x.sort(axis=1).sort_index(by=['Sample Name']).reset_index(drop=True),
                               df_y.sort(axis=1).sort_index(by=['Sample Name']).reset_index(drop=True))
            return True
        except AssertionError as e:
            print(e)
            return False

    def test_study_table_source_split(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-source-split.json')), self._tmp)
        import pandas as pd
        test_study_df = pd.read_csv(open(os.path.join(self._tmp, 's_TEST-Template1-Splitting.txt')), sep='\t')  # open written out study file for comparison
        ref_study_df = pd.read_csv(open(os.path.join(self._dir, 'data/TEST-ISA-source-split/s_TEST-Template1-Splitting.txt')), sep='\t')  # open original study file for comparison
        self.assertTrue(self._assert_study_tables_equal(test_study_df, ref_study_df))

    def test_assay_table_source_split(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-source-split.json')), self._tmp)
        import pandas as pd
        test_study_df = pd.read_csv(open(os.path.join(self._tmp, 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')), sep='\t')  # open written out study file for comparison
        ref_study_df = pd.read_csv(open(os.path.join(self._dir, 'data/TEST-ISA-source-split/a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')), sep='\t')  # open original study file for comparison
        self.assertTrue(self._assert_assay_tables_equal(test_study_df, ref_study_df))
        # FIXME: Assay tables currently do not match because of Raw Data File vs Array Data File naming conflict

    def test_sample_pool(self):
        pass

    def test_repeated_measure(self):
        pass

    def test_data_transformation(self):
        pass

    def test_charac_param_factor(self):
        pass