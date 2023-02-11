from unittest import TestCase

from isatools.net.mtbls.html import build_html_summary, build_html_data_files_list


class TestHtml(TestCase):

    def test_build_html_summary(self):
        expected_html = """
<html>
<head>
<title>ISA-Tab Factors Summary</title>
</head>
<body>
<table><tr><th>Study group</th><th>Number of samples</th></tr><tr><td>factor1: A, factor2: B</td><td>2</td></table>
</body>
</html>
"""
        summary = [
            {'sample_name': 'S1', 'factor1': 'A', 'factor2': 'B'},
            {'sample_name': 'S2', 'factor1': 'A', 'factor2': 'B'},
        ]
        self.assertEqual(build_html_summary(summary), expected_html)

    def test_build_html_data_files_list(self):
        expected_html = """
<html>
<head> <title>ISA-Tab Factors Summary</title> </head>
<body> <table><tr><th>Sample Name</th><th>Data File Names</th></tr><tr><td>S1</td><td>file1.txt, file2.txt</td></table> </body>
</html>
"""
        data_files_list = [
            {'sample': 'S1', 'data_files': ['file1.txt', 'file2.txt']},
        ]
        self.assertEqual(build_html_data_files_list(data_files_list).strip(), expected_html.strip())
