import unittest
from unittest.mock import patch, mock_open
from isatools.io import mtbls as MTBLS
import shutil


class TestMtblsIO(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    """Mock-only test on MTBLS1"""
    @patch('ftplib.FTP', autospec=True)
    def test_get_study(self, mock_ftp_constructor, mock_open):
        mock_ftp = mock_ftp_constructor.return_value
        mock_ftp.login.return_value = '230' # means login OK
        fp = mock_open()
        tmp_dir = MTBLS.get_study('MTBLS1')  # only retrieves ISA files from MTBLS
        self.assertTrue(mock_ftp.login.called)
        mock_ftp_constructor.assert_called_with('ftp.ebi.ac.uk')
        mock_ftp.cwd.assert_called_with('/pub/databases/metabolights/studies/public/MTBLS1')
        mock_ftp.retrbinary.assert_called_with('RETR i_Investigation.txt', fp.write)
        mock_ftp.retrbinary.assert_called_with('RETR s_MTBLS1.txt', fp.write)
        mock_ftp.retrbinary.assert_called_with('RETR a_mtbls1_metabolite_profiling_NMR_spectroscopy.txt', fp.write)
        shutil.rmtree(tmp_dir)

    """Tries to do actual call on MetaboLights"""
    def test_load_study(self):
        isa_json = MTBLS.load('MTBLS1')  # loads MTBLS study into ISA JSON
        self.assertIsInstance(isa_json, dict)
        self.assertEqual(isa_json['identifier'], 'MTBLS1')
        self.assertEqual(isa_json['studies'][0]['people'][0]['email'], 'rms72@cam.ac.uk')


    """Test getting data urls for files from a study, given a filter of factor selection"""
    def test_get_data_urls(self):
        data_files_urls = MTBLS.get_data_files_urls('MTBLS1', factor_selection={"gender": "male"})
