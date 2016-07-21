import unittest
from unittest.mock import patch
from isatools.io import mtbls as MTBLS


class TestMtblsIO(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    """Mock-only test on MTBLS3 as problem with MTBLS1 in isatab2json (see issue #130); also problem with MTBLS2"""
    @patch('ftplib.FTP', autospec=True)
    def test_get_study(self, mock_ftp_constructor):
        mock_ftp = mock_ftp_constructor.return_value
        mock_ftp.login.return_value = '230' # means login OK

        MTBLS.get_study('MTBLS3')  # only retrieves ISA files from MTBLS

        self.assertTrue(mock_ftp.login.called)
        mock_ftp_constructor.assert_called_with('ftp.ebi.ac.uk')
        mock_ftp.cwd.assert_called_with('/pub/databases/metabolights/studies/public/MTBLS3')
        mock_ftp.retrbinary.assert_called_with('RETR i_Investigation.txt', print)
        mock_ftp.retrbinary.assert_called_with('RETR s_MTBLS3.txt', print)
        mock_ftp.retrbinary.assert_called_with('RETR a_live_mtbl3_metabolite profiling_mass spectrometry.txt', print)

    """Tries to do actual call on MetaboLights"""
    def test_load_study(self):
        isa_json = MTBLS.load('MTBLS3')  # loads MTBLS study into ISA JSON
        self.assertIsInstance(isa_json, dict)
        self.assertEqual(isa_json['identifier'], 'MTBLS3')
        self.assertEqual(isa_json['studies'][0]['people'][0]['email'], 'rms72@cam.ac.uk')