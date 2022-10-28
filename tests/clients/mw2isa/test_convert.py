import unittest
import logging
from unittest.mock import patch

from isatools.net.mw2isa.convert import MW2ISA


log = logging.getLogger('isatools')
log.level = logging.CRITICAL
mock_analysis_type = '"1": {"analysis_type": "test"}'
mock_html_table = '''
<table class="datatable2">
    <thead></thead>
    <tbody>
        <tr> Hello </tr> <td> World </td>
    </tbody>
</table>
'''


class MockGetResponse(object):
    text = '{%s}' % mock_analysis_type


class MockGetResponseMultiple(object):
    text = '{%s, "2": {"analysis_type": "test2"}}' % mock_analysis_type


class MockGetResponseHTML(object):
    text = '<html>%s %s</html>' % (mock_html_table, mock_html_table)


class TestConvert(unittest.TestCase):

    def test_constructor_errors(self):
        with self.assertRaises(ValueError) as context:
            investigation = MW2ISA('MTBLS1')
        self.assertTrue('Invalid MetaboLights ID: MTBLS1' in str(context.exception))

    @patch('isatools.net.mw2isa.convert.requests.get', return_value=MockGetResponse)
    def test_get_analysis_type(self, mock_get):
        investigation = MW2ISA('ST000367')
        investigation.get_analysis_type()
        self.assertEqual(investigation.analysis_type, 'test')

        # Hit the cache
        investigation.analysis_type = 'test2'
        investigation.get_analysis_type()
        self.assertEqual(investigation.analysis_type, 'test2')

    @patch('isatools.net.mw2isa.convert.requests.get', return_value=MockGetResponseMultiple)
    def test_get_analysis_type_multiple(self, mock_get):
        investigation = MW2ISA('ST000367')
        investigation.get_analysis_type()
        self.assertEqual(investigation.analysis_type, 'test2')

    @patch('isatools.net.mw2isa.convert.requests.get', return_value=MockGetResponseHTML)
    def test_get_html_table(self, mock_get):
        investigation = MW2ISA('ST000367')
        investigation.analysis_type = 'MS'
        tables = investigation.get_html_table()
        mock_get.assert_called_with(
            "http://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&DataMode=MSData&StudyID=ST000367"
            "&StudyType=MS&ResultType=1#DataTabs"
        )
        self.assertEqual(len(tables), 2)
