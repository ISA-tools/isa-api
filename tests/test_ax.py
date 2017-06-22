import unittest
from unittest.mock import patch, mock_open
from isatools.io import ax as AX
import shutil
import os


class TestArrayExpressIO(unittest.TestCase):

    def setUp(self):
        pass  # detect if MTBLS is reachable. If so, run test of real server, otherwise run Mocks only?

    def tearDown(self):
        pass

    """Mock-only test on E-AFMX1"""
    @patch('ftplib.FTP', autospec=True)
    def test_get_experiment(self, mock_ftp_constructor):
        mock_ftp = mock_ftp_constructor.return_value
        mock_ftp.login.return_value = '230'  # means login OK
        tmp_dir = AX.get('E-AFMX-1')  # only retrieves ISA files from MTBLS
        self.assertTrue(mock_ftp.login.called)
        mock_ftp_constructor.assert_called_with('ftp.ebi.ac.uk')
        mock_ftp.cwd.assert_called_with('/pub/databases/arrayexpress/data/experiment/AFMX/E-AFMX-1')
        shutil.rmtree(tmp_dir)

    """Tries to do actual call on ArrayExpress; uses E-AFMX-1 as not so big"""
    def test_get_experiment_as_magetab(self):
        tmp_dir = AX.get('E-AFMX-1')  # gets E-AFMX-1 MAGE-TAB files
        self.assertEqual(len(os.listdir(tmp_dir)), 2)
        self.assertSetEqual(set(os.listdir(tmp_dir)), {'E-AFMX-1.sdrf.txt', 'E-AFMX-1.idf.txt'})
        shutil.rmtree(tmp_dir)

    def test_get_experiment_as_isatab(self):
        tmp_dir = AX.get_isatab('E-AFMX-1')  # gets E-AFMX-1 MAGE-TAB files
        self.assertEqual(len(os.listdir(tmp_dir)), 3)
        self.assertSetEqual(set(os.listdir(tmp_dir)), {'i_investigation.txt', 'a_E-AFMX-1.sdrf.txt',
                                                       's_E-AFMX-1.sdrf.txt'})
        shutil.rmtree(tmp_dir)

    def test_get_experiment_as_json(self):
        isa_json = AX.getj('E-AFMX-1')  # loads E-AFMX-1 study into ISA-JSON
        self.assertIsInstance(isa_json, dict)
        self.assertEqual(isa_json['identifier'], 'E-AFMX-1')
        self.assertEqual(isa_json['studies'][0]['people'][0]['email'], 'khaitovich@eva.mpg.de')
