import unittest
from mock import patch, mock_open
from isatools.io import mtbls as MTBLS
import shutil


class TestMtblsIO(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    """Mock-only test on MTBLS1"""
    @patch('ftplib.FTP', autospec=True)
    def test_get_study(self, mock_ftp_constructor):  # FIXME: mock_open was working, but now doesn't (with no change to code...)
        mock_ftp = mock_ftp_constructor.return_value
        mock_ftp.login.return_value = '230'  # means login OK
        tmp_dir = MTBLS.get_study('MTBLS1')  # only retrieves ISA files from MTBLS
        self.assertTrue(mock_ftp.login.called)
        mock_ftp_constructor.assert_called_with('ftp.ebi.ac.uk')
        mock_ftp.cwd.assert_called_with('/pub/databases/metabolights/studies/public/MTBLS1')
        shutil.rmtree(tmp_dir)

    """Tries to do actual call on MetaboLights"""
    def test_load_study(self):
        isa_json = MTBLS.load('MTBLS1')  # loads MTBLS study into ISA JSON
        self.assertIsInstance(isa_json, dict)
        self.assertEqual(isa_json['identifier'], 'MTBLS1')
        self.assertEqual(isa_json['studies'][0]['people'][0]['email'], 'rms72@cam.ac.uk')
