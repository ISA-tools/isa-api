import unittest
from unittest.mock import patch
from isatools.io import mtbls as MTBLS
import os
import shutil


class TestMtblsIO(unittest.TestCase):

    def setUp(self):
        self._tmp = os.path.join(os.path.dirname(__file__), './tmp/')
        if not os.path.exists(self._tmp):
            os.mkdir(self._tmp)

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    @patch('ftplib.FTP', autospec=True)
    def test_get_study(self, mock_ftp_constructor):
        mock_ftp = mock_ftp_constructor.return_value
        mock_ftp.login.return_value = '230' # means login OK

        MTBLS.get_study('MTBLS1', self._tmp)  # only retrieves ISA files from MTBLS

        self.assertTrue(mock_ftp.login.called)
        mock_ftp_constructor.assert_called_with('ftp.ebi.ac.uk')
        mock_ftp.cwd.assert_called_with('/pub/databases/metabolights/studies/public/MTBLS1')
        mock_ftp.retrbinary.assert_called_with('RETR i_Investigation.txt', print)
        mock_ftp.retrbinary.assert_called_with('RETR s_MTBLS1.txt', print)
        mock_ftp.retrbinary.assert_called_with('RETR a_mtbls1_metabolite_profiling_NMR_spectroscopy.txt', print)

    def test_load_study(self):
        isa_json = MTBLS.load_study('MTBLS1', self._tmp)  # loads MTBLS study into ISA JSON
