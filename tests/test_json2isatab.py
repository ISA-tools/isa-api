from unittest import TestCase
import os
import shutil
from isatools.convert import json2isatab
from isatools.isatab import assert_tab_content_equal


class JsonToTabTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)
        self._tmp = os.path.join(self._dir, './tmp/')
        if not os.path.exists(self._tmp):
            os.mkdir(self._tmp)

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_source_split_investigation(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-source-split.json')), self._tmp)
        try:
            fp = open(os.path.join(self._tmp, 'i_investigation.txt'))
        except IOError:
            self.fail("Could not open expected written file i_investigation.txt")
        if fp is not None:
            self.assertTrue(assert_tab_content_equal(fp, open(os.path.join(self._dir, 'data/TEST-ISA-source-split/i_investigation.txt'))))

    def test_source_split_study_table(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-source-split.json')), self._tmp)
        try:
            fp = open(os.path.join(self._tmp, 's_TEST-Template1-Splitting.txt'))
        except IOError:
            self.fail("Could not open expected written file s_TEST-Template1-Splitting.txt")
        if fp is not None:
            self.assertTrue(assert_tab_content_equal(fp, open(os.path.join(self._dir, 'data/TEST-ISA-source-split/s_TEST-Template1-Splitting.txt'))))

    def test_source_split_assay_table(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-source-split.json')), self._tmp)
        try:
            fp = open(os.path.join(self._tmp, 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt'))
        except IOError:
            self.fail("Could not open expected written file a_test-template1-splitting_transcription_profiling_DNA_microarray.txt")
        if fp is not None:
            self.assertTrue(assert_tab_content_equal(fp, open(os.path.join(self._dir, 'data/TEST-ISA-source-split/a_test-template1-splitting_transcription_profiling_DNA_microarray.txt'))))

    def test_sample_pool_investigation(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-sample-pool.json')), self._tmp)
        try:
            fp = open(os.path.join(self._tmp, 'i_investigation.txt'))
        except IOError:
            self.fail("Could not open expected written file i_investigation.txt")
        if fp is not None:
            self.assertTrue(assert_tab_content_equal(fp, open(os.path.join(self._dir, 'data/TEST-ISA-sample-pool/i_investigation.txt'))))

    def test_sample_pool_study_table(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-sample-pool.json')), self._tmp)
        try:
            fp = open(os.path.join(self._tmp, 's_TEST-Template3-Splitting.txt'))
        except IOError:
            self.fail("Could not open expected written file s_TEST-Template3-Splitting.txt")
        if fp is not None:
            self.assertTrue(assert_tab_content_equal(fp, open(os.path.join(self._dir, 'data/TEST-ISA-sample-pool/s_TEST-Template3-Splitting.txt'))))

    def test_sample_pool_assay_table(self):
        json2isatab.convert(open(os.path.join(self._dir, 'TEST-ISA-sample-pool.json')), self._tmp)
        try:
            fp = open(os.path.join(self._tmp, 'a_test-template3-splitting_transcription_profiling_DNA_microarray.txt'))
        except IOError:
            self.fail("Could not open expected written file a_test-template3-splitting_transcription_profiling_DNA_microarray.txt")
        if fp is not None:
            self.assertTrue(assert_tab_content_equal(fp, open(os.path.join(self._dir, 'data/TEST-ISA-sample-pool/a_test-template3-splitting_transcription_profiling_DNA_microarray.txt'))))

    def test_bii_s_3_investigation(self):
        try:
            fp = open(os.path.join(self._tmp, 'i_investigation.txt'))
            json2isatab.convert(open(os.path.join(self._dir, 'data/BII-S-3/BII-S-3.json')), self._tmp)
        except IOError:
            self.fail("Could not open expected written file i_investigation.txt")
        if fp is not None:
            self.assertTrue(assert_tab_content_equal(fp, open(os.path.join(self._dir, 'data/BII-S-3/i_gilbert.txt'))))

    def test_bii_s_3_study_table(self):
        json2isatab.convert(open(os.path.join(self._dir, 'data/BII-S-3/BII-S-3.json')), self._tmp)
        try:
            fp = open(os.path.join(self._tmp, 's_BII-S-3.txt'))
        except IOError:
            self.fail("Could not open expected written file s_BII-S-3.txt")
        if fp is not None:
            self.assertTrue(assert_tab_content_equal(fp, open(os.path.join(self._dir, 'data/BII-S-3/s_BII-S-3.txt'))))

    def test_bii_s_3_assay_table_Tx(self):
        json2isatab.convert(open(os.path.join(self._dir, 'data/BII-S-3/BII-S-3.json')), self._tmp)
        try:
            fp = open(os.path.join(self._tmp, 'a_gilbert-assay-Tx.txt'))
        except IOError:
            self.fail("Could not open expected written file a_gilbert-assay-Tx.txt")
        if fp is not None:
            self.assertTrue(assert_tab_content_equal(fp, open(os.path.join(self._dir, 'data/BII-S-3/a_gilbert-assay-Tx.txt'))))

    def test_bii_s_3_assay_table_Gx(self):
        json2isatab.convert(open(os.path.join(self._dir, 'data/BII-S-3/BII-S-3.json')), self._tmp)
        try:
            fp = open(os.path.join(self._tmp, 'a_gilbert-assay-Gx.txt'))
        except IOError:
            self.fail("Could not open expected written file a_gilbert-assay-Gx.txt")
        if fp is not None:
            self.assertTrue(assert_tab_content_equal(fp, open(os.path.join(self._dir, 'data/BII-S-3/a_gilbert-assay-Gx.txt'))))