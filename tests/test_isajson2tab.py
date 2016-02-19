from unittest import TestCase
import os
import shutil
from isatools.convert import json2isatab
from isatools.isatab import assert_tab_equal


class JsonToTabTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)
        self._tmp = os.path.join(self._dir, './tmp/')
        if not os.path.exists(self._tmp):
            os.mkdir(self._tmp)

    def tearDown(self):
        # shutil.rmtree(self._tmp, ignore_errors=True)
        pass

    # def test_source_split_investigation(self):
    #     json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-source-split.json')), self._tmp)
    #     self.assertTrue(assert_tab_equal(open(os.path.join(self._tmp, 'i_Investigation.txt')),
    #                                      open(os.path.join(self._dir, 'data/TEST-ISA-source-split/i_Investigation.txt'))))
    """
    FIXME: Check investigation parsing for above test
    """
    def test_source_split_study_table(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-source-split.json')), self._tmp)
        self.assertTrue(assert_tab_equal(open(os.path.join(self._tmp, 's_TEST-Template1-Splitting.txt')),
                                         open(os.path.join(self._dir, 'data/TEST-ISA-source-split/s_TEST-Template1-Splitting.txt'))))

    def test_source_split_assay_table(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-source-split.json')), self._tmp)
        self.assertTrue(assert_tab_equal(open(os.path.join(self._tmp, 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')),
                                         open(os.path.join(self._dir, 'data/TEST-ISA-source-split/a_test-template1-splitting_transcription_profiling_DNA_microarray.txt'))))

    def test_sample_pool_study_table(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-sample-pool.json')), self._tmp)
        self.assertTrue(assert_tab_equal(open(os.path.join(self._tmp, 's_TEST-Template3-Splitting.txt')),
                                         open(os.path.join(self._dir, 'data/TEST-ISA-sample-pool/s_TEST-Template3-Splitting.txt'))))

    def test_sample_pool_assay_table(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-sample-pool.json')), self._tmp)
        self.assertTrue(assert_tab_equal(open(os.path.join(self._tmp, 'a_test-template3-splitting_transcription_profiling_DNA_microarray.txt')),
                                         open(os.path.join(self._dir, 'data/TEST-ISA-sample-pool/a_test-template3-splitting_transcription_profiling_DNA_microarray.txt'))))

    def test_bii_s_3_study_table(self):
        json2isatab.convert(open('../isatools/sampledata/BII-S-3.json'), self._tmp)
        self.assertTrue(assert_tab_equal(open(os.path.join(self._tmp, 's_BII-S-3.txt')),
                                         open(os.path.join(self._dir, 'data/BII-S-3/s_BII-S-3.txt'))))

    def test_bii_s_3_assay_table_Tx(self):
        json2isatab.convert(open('../isatools/sampledata/BII-S-3.json'), self._tmp)
        self.assertTrue(assert_tab_equal(open(os.path.join(self._tmp, 'a_gilbert-assay-Tx.txt')),
                                         open(os.path.join(self._dir, 'data/BII-S-3/a_gilbert-assay-Tx.txt'))))

    # def test_bii_s_3_assay_table_Gx(self):
    #     json2isatab.convert(open('/Users/dj/PycharmProjects/isa-api/isatools/sampledata/BII-S-3.json'), self._tmp)
    #     self.assertTrue(assert_tab_equal(open(os.path.join(self._tmp, 'a_gilbert-assay-Gx.txt')),
    #                                      open(os.path.join(self._dir, '/Users/dj/PycharmProjects/isa-api/tests/data/BII-S-3/a_gilbert-assay-Gx.txt'))))
    # """
    #     FIXME: need Comment[] support
    # """
