import os
from unittest import TestCase
from isatools.convert import isatab2json, json2isatab
from isatools import isatab
import shutil


class TwoWayConvertTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)
        self._tmp = os.path.join(self._dir, './tmp/')
        if not os.path.exists(self._tmp):
            os.mkdir(self._tmp)

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_isa_sample_pool(self):
        source_dir = os.path.join(self._dir, 'data/TEST-ISA-sample-pool/')
        isatab2json.convert(source_dir, self._tmp)
        json2isatab.convert(open(os.path.join(self._tmp, 'TEST-ISA-sample-pool.json')), self._tmp)
        self.assertTrue(isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'i_investigation.txt')),
                                                open(os.path.join(self._tmp, 'i_investigation.txt'))))
        self.assertTrue(isatab.assert_tab_content_equal(open(os.path.join(source_dir, 's_TEST-Template3-Splitting.txt')),
                                                open(os.path.join(self._tmp, 's_TEST-Template3-Splitting.txt'))))
        self.assertTrue(isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'a_test-template3-splitting_transcription_profiling_DNA_microarray.txt')),
                                                open(os.path.join(self._tmp, 'a_test-template3-splitting_transcription_profiling_DNA_microarray.txt'))))

    def test_isa_source_split(self):
        source_dir = os.path.join(self._dir, 'data/TEST-ISA-source-split/')
        isatab2json.convert(source_dir, self._tmp)
        json2isatab.convert(open(os.path.join(self._tmp, 'TEST-ISA-source-split.json')), self._tmp)
        self.assertTrue(isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'i_investigation.txt')),
                                                open(os.path.join(self._tmp, 'i_investigation.txt'))))
        self.assertTrue(isatab.assert_tab_content_equal(open(os.path.join(source_dir, 's_TEST-Template1-Splitting.txt')),
                                                open(os.path.join(self._tmp, 's_TEST-Template1-Splitting.txt'))))
        self.assertTrue(isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')),
                                                open(os.path.join(self._tmp, 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt'))))

    # def test_isa_repeated_measure(self):
    #     source_dir = os.path.join(self._dir, 'data/TEST-ISA-repeated-measure/')
    #     isatab2json.convert(source_dir, self._tmp)
    #     json2isatab.convert(open(os.path.join(self._tmp, 'TEST-ISA-repeated-measure.json')), self._tmp)
    #     isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'i_investigation.txt')),
    #                             open(os.path.join(self._tmp, 'i_investigation.txt')))
    #     isatab.assert_tab_content_equal(open(os.path.join(source_dir, 's_TEST-Template5-repeatedmeasure.txt')),
    #                             open(os.path.join(self._tmp, 's_TEST-Template5-repeatedmeasure.txt')))
    #     isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'a_test-template5-repeatedmeasure_transcription_profiling_DNA_microarray.txt')),
    #                             open(os.path.join(self._tmp, 'a_test-template5-repeatedmeasure_transcription_profiling_DNA_microarray.txt')))
    """ Repeated measure test produces too many study table rows """


    # def test_isa_charac_param_factor(self):
    #     source_dir = os.path.join(self._dir, 'data/TEST-ISA-charac-param-factor/')
    #     isatab2json.convert(source_dir, self._tmp)
    #     json2isatab.convert(open(os.path.join(self._tmp, 'TEST-ISA-charac-param-factor.json')), self._tmp)
    #     isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'i_investigation.txt')),
    #                             open(os.path.join(self._tmp, 'i_investigation.txt')))
    #     isatab.assert_tab_content_equal(open(os.path.join(source_dir, 's_TEST-Template1-Splitting.txt')),
    #                             open(os.path.join(self._tmp, 's_TEST-Template1-Splitting.txt')))
    #     isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')),
    #                             open(os.path.join(self._tmp, 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt')))
    """Problem with intermediate json"""

    # def test_isa_bii_i_1(self):
    #     source_dir = os.path.join(self._dir, 'data/BII-I-1/')
    #     isatab2json.convert(source_dir, self._tmp)
    #     json2isatab.convert(open(os.path.join(self._tmp, 'BII-I-1.json')), self._tmp)
    #     isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'i_investigation.txt')),
    #                             open(os.path.join(self._tmp, 'i_investigation.txt')))
    #     isatab.assert_tab_content_equal(open(os.path.join(source_dir, 's_BII-S-1.txt')),
    #                             open(os.path.join(self._tmp, 's_BII-S-2.txt')))
    #     isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'a_metabolome.txt')),
    #                             open(os.path.join(self._tmp, 'a_metabolome.txt')))
    #     isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'a_microarray.txt')),
    #                             open(os.path.join(self._tmp, 'a_microarray.txt')))
    #     isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'a_transcriptome.txt')),
    #                             open(os.path.join(self._tmp, 'a_transcriptome.txt')))
    """Problem with intermediate json"""

    def test_isa_bii_s_3(self):
        source_dir = os.path.join(self._dir, 'data/BII-S-3/')
        isatab2json.convert(source_dir, self._tmp)
        json2isatab.convert(open(os.path.join(self._tmp, 'BII-S-3.json')), self._tmp)
        self.assertTrue(isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'i_gilbert.txt')),
                                                open(os.path.join(self._tmp, 'i_investigation.txt'))))
        self.assertTrue(isatab.assert_tab_content_equal(open(os.path.join(source_dir, 's_BII-S-3.txt')),
                                                open(os.path.join(self._tmp, 's_BII-S-3.txt'))))
        self.assertTrue(isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'a_gilbert-assay-Gx.txt')),
                                                open(os.path.join(self._tmp, 'a_gilbert-assay-Gx.txt'))))
        self.assertTrue(isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'a_gilbert-assay-Tx.txt')),
                                                open(os.path.join(self._tmp, 'a_gilbert-assay-Tx.txt'))))

    def test_isa_bii_s_7(self):
        source_dir = os.path.join(self._dir, 'data/BII-S-7/')
        isatab2json.convert(source_dir, self._tmp)
        json2isatab.convert(open(os.path.join(self._tmp, 'BII-S-7.json')), self._tmp)
        isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'i_matteo.txt')),
                                open(os.path.join(self._tmp, 'i_investigation.txt')))
        isatab.assert_tab_content_equal(open(os.path.join(source_dir, 's_BII-S-7.txt')),
                                open(os.path.join(self._tmp, 's_BII-S-7.txt')))
        isatab.assert_tab_content_equal(open(os.path.join(source_dir, 'a_matteo-assay-Gx.txt')),
                                open(os.path.join(self._tmp, 'a_matteo-assay-Gx.txt')))