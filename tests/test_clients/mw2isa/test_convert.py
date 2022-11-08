import unittest
import logging
from unittest.mock import patch

from isatools.net.mw2isa.convert import MW2ISA
from mw2isa_mocks import (
    mock_analysis_get_response_error,
    MockAnalysisGetResponseSingle,
    MockAnalysisGetResponseMultiple,
    MockGetResponseHTMLTable,
    MOCK_BS4_SUCCESS,
    MOCK_BS4_ERROR_NOTABLE,
    MOCK_BS4_ERROR_NOID,
)


log = logging.getLogger('isatools')
log.level = logging.CRITICAL


class TestConvert(unittest.TestCase):

    def test_constructor_errors(self):
        with self.assertRaises(ValueError) as context:
            investigation = MW2ISA('MTBLS1')
        self.assertTrue('Invalid MetaboLights ID: MTBLS1' in str(context.exception))

    @patch('isatools.net.mw2isa.convert.requests.get', return_value=MockAnalysisGetResponseSingle)
    def test_get_analysis_type_single(self, mock_get):
        investigation = MW2ISA('ST000367')
        investigation.get_analysis_type()
        self.assertEqual(investigation.analysis_type, 'test')

        # Hit the cache
        investigation.analysis_type = 'test2'
        investigation.get_analysis_type()
        self.assertEqual(investigation.analysis_type, 'test2')

    @patch('isatools.net.mw2isa.convert.requests.get', return_value=MockAnalysisGetResponseMultiple)
    def test_get_analysis_type_multiple(self, mock_get):
        investigation = MW2ISA('ST000367')
        investigation.get_analysis_type()
        self.assertEqual(investigation.analysis_type, 'test2')

    @patch('isatools.net.mw2isa.convert.requests.get', autospec=True)
    def test_get_analysis_type_error(self, mock_get):
        mock_get.return_value = mock_analysis_get_response_error
        investigation = MW2ISA('ST000367')
        with self.assertRaises(Exception) as context:
            investigation.get_analysis_type()
        self.assertEqual(str(context.exception),
                         "There was a problem when trying to download the analysis for ST000367: "
                         "'function' object has no attribute 'text'")

    @patch('isatools.net.mw2isa.convert.requests.get', return_value=MockGetResponseHTMLTable)
    def test_get_html_table(self, mock_get):
        investigation = MW2ISA('ST000367')
        investigation.analysis_type = 'MS'
        investigation.get_html_table()
        mock_get.assert_called_with(
            "http://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&DataMode=MSData&StudyID=ST000367"
            "&StudyType=MS&ResultType=1#DataTabs"
        )

    def test_parse_table_errors(self):
        investigation = MW2ISA('ST000367')
        investigation.analysis_type = 'MS'

        # Testing no table
        with self.assertRaises(KeyError) as context:
            investigation.parse_table(MOCK_BS4_ERROR_NOTABLE)
        self.assertEqual(str(context.exception), str(KeyError("No table found for ST000367")))

        # Testing no ID
        with self.assertRaises(KeyError) as context:
            investigation.parse_table(MOCK_BS4_ERROR_NOID)
        self.assertEqual(str(context.exception), str(KeyError("No analysis ID found for ST000367")))

    def test_parse_table_success(self):
        investigation = MW2ISA('ST000367')
        investigation.analysis_type = 'MS'
        study_assa_dict = investigation.parse_table(MOCK_BS4_SUCCESS)
        self.assertEqual(study_assa_dict['assays'], [
            {'techtype': 'mass spectrometry', 'analysis_id': 'AN000600'},
            {'techtype': 'nmr spectrometry', 'analysis_id': 'AN000601'}
        ])

    def test_get_download_url(self):
        assay_dict = {'assays': [{'analysis_id': 'AN000600'}]}
        investigation = MW2ISA('ST000367')
        investigation.analysis_type = 'MS'
        url = investigation.get_download_url(assay_dict)
        self.assertEqual(url, "http://www.metabolomicsworkbench.org/data/study_textformat_view.php"
                              "?STUDY_ID=ST000367&ANALYSIS_ID=AN000600&MODE=d")
