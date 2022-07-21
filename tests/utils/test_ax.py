import unittest
from unittest.mock import patch, mock_open
from isatools.net import ax as AX
import shutil
import os
import tempfile


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

    """Tries to do actual call on ArrayExpress; uses E-AFMX-1
       Test is now idiotic I now by Massi 17/12/2019
    """
    @patch('isatools.net.ax.get')
    def test_get_experiment_as_magetab(self, mock_ax_get):
        src = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data', 'magetab', 'E-AFMX-1')
        )
        dest = tempfile.mkdtemp()
        target = shutil.copytree(src, os.path.abspath(os.path.join(dest, 'E-AFMX-1')))
        mock_ax_get.return_value = target
        tmp_dir = AX.get('E-AFMX-1')  # gets E-AFMX-1 MAGE-TAB files
        self.assertEqual(len(os.listdir(tmp_dir)), 2)
        self.assertSetEqual(set(os.listdir(tmp_dir)), {'E-AFMX-1.sdrf.txt', 'E-AFMX-1.idf.txt'})
        shutil.rmtree(tmp_dir)

    @patch('isatools.net.ax.get')
    def test_get_experiment_as_isatab(self, mock_ax_get):
        src = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data', 'magetab', 'E-AFMX-1')
        )
        dest = tempfile.mkdtemp()
        target = shutil.copytree(src, os.path.abspath(os.path.join(dest, 'E-AFMX-1')))
        mock_ax_get.return_value = target
        tmp_dir = AX.get_isatab('E-AFMX-1')  # gets E-AFMX-1 MAGE-TAB files
        self.assertEqual(len(os.listdir(tmp_dir)), 3)
        self.assertSetEqual(set(os.listdir(tmp_dir)), {'i_investigation.txt', 'a_E-AFMX-1_assay.txt',
                                                       's_E-AFMX-1_study.txt'})
        shutil.rmtree(tmp_dir)
