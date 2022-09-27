from __future__ import absolute_import

from unittest.mock import patch
from isatools.net import mtbls as MTBLS

import unittest
import os

import shutil
import tempfile
from isatools.tests import utils


class TestMtblsIO(unittest.TestCase):

    def setUp(self):
        # pass  # detect if MTBLS is reachable. If so, run test of real server, otherwise run Mocks only?
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        pass

    """Mock-only test on MTBLS1"""
    @patch('ftplib.FTP', autospec=True)
    def test_get_study(self, mock_ftp_constructor):
        mock_ftp = mock_ftp_constructor.return_value
        mock_ftp.login.return_value = '230'  # means login OK
        tmp_dir = MTBLS.get('MTBLS1')  # only retrieves ISA files from MTBLS
        self.assertTrue(mock_ftp.login.called)
        mock_ftp_constructor.assert_called_with('ftp.ebi.ac.uk')
        mock_ftp.cwd.assert_called_with('/pub/databases/metabolights/studies/public/MTBLS1')
        shutil.rmtree(tmp_dir)

    """Tries to do actual call on MetaboLights; uses MTBLS2 as not so big"""
    # def test_get_study_as_tab(self):
    #     tmp_dir = MTBLS.getj('MTBLS2')  # gets MTBLS ISA-Tab files
    #     self.assertEqual(len(os.listdir(tmp_dir)), 3)
    #     self.assertSetEqual(set(os.listdir(tmp_dir)), {'a_mtbl2_metabolite profiling_mass spectrometry.txt',
    #                                                'i_Investigation.txt', 's_MTBL2.txt'})
    #     shutil.rmtree(tmp_dir)

    # def test_get_study_as_json(self):
    #     isa_json = MTBLS.get('MTBLS2')  # loads MTBLS study into ISA JSON
    #     self.assertIsInstance(isa_json, dict)
    #     self.assertEqual(isa_json['identifier'], 'MTBLS2')
    #     self.assertEqual(isa_json['studies'][0]['people'][0]['email'], 'boettch@ipb-halle.de')

    # def test_get_factor_names(self):
    #     factors = MTBLS.get_factor_names('MTBLS2')
    #     self.assertIsInstance(factors, set)
    #     self.assertEqual(len(factors), 2)
    #     self.assertSetEqual(factors, {'genotype', 'replicate'})

    # def test_get_factor_values(self):
    #     fvs = MTBLS.get_factor_values('MTBLS2', 'genotype')
    #     self.assertIsInstance(fvs, set)
    #     self.assertEqual(len(fvs), 2)
    #     self.assertSetEqual(fvs, {'Col-0', 'cyp79'})

    # def test_get_datafiles(self):
    #     datafiles = MTBLS.get_data_files('MTBLS2')
    #     self.assertIsInstance(datafiles, list)
    #     self.assertEqual(len(datafiles), 16)
    #     factor_selection = {"genotype": "Col-0"}
    #     results = MTBLS.get_data_files('MTBLS2', factor_selection)
    #     self.assertEqual(len(results), 8)
    #     self.assertEqual(len(results[0]['data_files']), 1)

    @patch('isatools.net.mtbls.get')
    def test_get_datafiles_multiple_factors(self, mock_mtbls_get):
        value = 'MTBLS1'
        src = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'mtbls', value)
        )
        targets = []
        for i in range(3):
            dest = tempfile.mkdtemp()
            targets.append(shutil.copytree(src, os.path.abspath(os.path.join(dest, value))))
        it = iter(targets)
        mock_mtbls_get.return_value = next(it)
        factor_selection = {"Gender": "Male",
                            "Metabolic syndrome": "Control Group"}
        results = MTBLS.get_data_files(value, factor_selection)
        self.assertEqual(len(results), 56)
        self.assertEqual(len(results[0]['data_files']), 1)
        mock_mtbls_get.return_value = next(it)
        results_0 = MTBLS.get_data_files(value, {
            "Gender": "Male",
            "Metabolic syndrome": "Control Group"
        })
        mock_mtbls_get.return_value = next(it)
        results_1 = MTBLS.get_data_files(value, {
            "Gender": "Male"
        })
        self.assertLess(len(results_0), len(results_1))

    @patch('isatools.net.mtbls.get')
    def test_get_factors_summary(self, mock_mtbls_get):  # Test for issue #221
        value = 'MTBLS26'
        src = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'mtbls', value)
        )
        dest = tempfile.mkdtemp()
        target = shutil.copytree(src, os.path.abspath(os.path.join(dest, value)))
        mock_mtbls_get.return_value = target
        factors_summary = MTBLS.get_factors_summary(value)
        self.assertIsInstance(factors_summary, list)
        self.assertEqual(len(factors_summary), 18)

    @patch('isatools.net.mtbls.get')
    def test_get_data_for_sample(self, mock_mtbls_get):
        value = 'MTBLS108'
        src = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'mtbls', value)
        )
        dest = tempfile.mkdtemp()
        target = shutil.copytree(src, os.path.abspath(os.path.join(dest, value)))
        mock_mtbls_get.return_value = target
        hits = MTBLS.get_data_for_sample(
            value, sample_name='Lut_C_223h')
        self.assertEqual(len(hits), 2)
        self.assertIn(
            'm_study_p_c_metabolite_profiling_mass_spectrometry_v2_maf.tsv',
            [x.filename for x in hits])
        self.assertIn('Lut_C_223h.raw', [x.filename for x in hits])
