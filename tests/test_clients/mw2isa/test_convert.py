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
