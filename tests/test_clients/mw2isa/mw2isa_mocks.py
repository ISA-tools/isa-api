from bs4 import BeautifulSoup


MOCK_ANALYSIS_TYPE = '{"analysis_type": "test"}'
MOCK_HTML_TABLE = '''
<table class="datatable2">
    <tr class="even"><td align=left><b>MS ID:</b></td><td>MS000533</td></tr>
    <tr class="odd"><td align=left><b>Analysis ID:</b></td><td>AN000600</td></tr>
</table>
<table class="datatable2">
    <tr class="even"><td align=left><b>NMR ID:</b></td><td>MS000531</td></tr>
    <tr class="odd"><td align=left><b>Analysis ID:</b></td><td>AN000601</td></tr>
</table>
'''
MOCK_BS4_SUCCESS = BeautifulSoup(MOCK_HTML_TABLE, 'html.parser')
MOCK_BS4_ERROR_NOTABLE = BeautifulSoup('<table></table>', 'html.parser')
MOCK_BS4_ERROR_NOID = BeautifulSoup('<table class="datatable2"></table>', 'html.parser')


def mock_analysis_get_response_error():
    pass


class MockAnalysisGetResponseSingle(object):
    text = '%s' % MOCK_ANALYSIS_TYPE


class MockAnalysisGetResponseMultiple(object):
    text = '{"1": %s, "2": {"analysis_type": "test2"}}' % MOCK_ANALYSIS_TYPE


class MockGetResponseHTMLTable(object):
    text = '<html>%s %s</html>' % (MOCK_HTML_TABLE, MOCK_HTML_TABLE)


