import unittest
from unittest.mock import patch, MagicMock, mock_open
from isatools.net import ax as AX
from isatools.tests import utils as test_utils
from isatools.net.ax import get, get_isatab, getj
import shutil
import os
import tempfile
import ftplib
import logging


log = logging.getLogger('isatools')


class TestArrayExpressIO(unittest.TestCase):

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    # @patch('isatools.net.ax.ftplib.FTP')
    # def test_get_file_not_found(self, mock_ftp, mock_log=None):
    #     mock_ftp_instance = MagicMock()
    #     mock_ftp.return_value = mock_ftp_instance
    #     mock_ftp_instance.login.return_value = '230 Login successful'
    #     mock_ftp_instance.cwd.side_effect = ftplib.error_perm("550 File not found")
    #
    #     with self.assertLogs('isatools', level='CRITICAL') as tmp_log:
    #         target_dir = AX.get('E-AFMX-1')
    #         self.assertIn("Could not retrieve ArrayExpress study", tmp_log)
    #         # target_dir should be None because ftp.cwd failed
    #         self.assertIsNone(target_dir)
    #
    # @patch('isatools.net.ax.magetab2json.convert')
    # @patch('isatools.net.ax.get')
    # def test_getj_exception(self, mock_get, mock_convert):
    #     mock_get.return_value = tempfile.mkdtemp()
    #     mock_convert.side_effect = Exception("Conversion error")
    #
    #     with self.assertLogs('isatools', level='CRITICAL'):
    #         result = getj('E-GEOD-59671')
    #         self.assertIsNone(result)

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



    @patch('isatools.net.ax.ftplib.FTP')
    def test_get_successful(self, mock_ftp):
        mock_ftp_instance = MagicMock()
        mock_ftp.return_value = mock_ftp_instance
        mock_ftp_instance.login.return_value = '230 Login successful'
        mock_ftp_instance.cwd.return_value = None
        mock_ftp_instance.retrbinary.return_value = None

        with patch('isatools.net.ax.open', mock_open()) as mock_file:
            target_dir = get('E-GEOD-59671')

            self.assertTrue(os.path.exists(target_dir))
            mock_file.assert_called()

    @patch('isatools.net.ax.ftplib.FTP')
    def test_get_connection_error(self, mock_ftp):
        mock_ftp_instance = MagicMock()
        mock_ftp.return_value = mock_ftp_instance
        mock_ftp_instance.login.return_value = '500 Login failed'

        with self.assertRaises(ConnectionError):
            get('E-GEOD-59671')



    @patch('isatools.net.ax.magetab2isatab.convert')
    @patch('isatools.net.ax.get')
    def test_get_isatab_successful(self, mock_get, mock_convert):
        mock_get.return_value = tempfile.mkdtemp()
        target_dir = get_isatab('E-GEOD-59671')
        mock_convert.assert_called_once()
        self.assertTrue(tempfile.gettempdir() in target_dir)

    @patch('isatools.net.ax.ftplib.FTP')
    @patch('isatools.net.ax.magetab2json.convert')
    @patch('isatools.net.ax.get')
    def test_getj_successful(self, mock_get, mock_convert, mock_ftp):
        # this prevents logs being printed during test execution due to files not being found
        mock_ftp_instance = MagicMock()
        mock_ftp.return_value = mock_ftp_instance
        mock_ftp_instance.login.return_value = 'stuff'
        mock_get.return_value = tempfile.mkdtemp()
        mock_convert.return_value = {"test": "json"}
        result = getj('E-GEOD-59671')
        mock_convert.assert_called_once()
        self.assertEqual(result, {"test": "json"})

