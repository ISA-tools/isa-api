from os import path
import unittest
from unittest.mock import patch
from logging import getLogger, CRITICAL
from ftplib import error_perm

from isatools.net.metabolights.core import MTBLSInvestigationBase, MTBLSInvestigation
from isatools.model import DataFile

log = getLogger('isatools')
log.level = CRITICAL

HERE = path.dirname(path.abspath(__file__))
DATA_PATH = path.join(HERE, '..', '..', 'data')
MTBLS_1_PATH = path.join(DATA_PATH, 'mtbls', 'MTBLS1')
MTBLS_mock = path.join(DATA_PATH, 'mtbls', 'test')

with open(path.join(MTBLS_1_PATH, 'i_Investigation.txt')) as mock_file:
    MTBLS_i = mock_file.read()
with open(path.join(MTBLS_1_PATH, 's_MTBLS1.txt')) as mock_file:
    MTBLS_s = mock_file.read()
with open(path.join(MTBLS_1_PATH, 'a_mtbls1_metabolite_profiling_NMR_spectroscopy.txt')) as mock_file:
    MTBLS_a = mock_file.read()


class TextIO:
    def __init__(self):
        self.name = "test"

    def write(self, s):
        pass


class MockFTP:
    def __init__(self, *args, **kwargs):
        pass

    def login(*args, **kwargs):
        pass

    def cwd(*args, **kwargs):
        pass

    @staticmethod
    def nlst(*args):
        return ['i_Investigation.txt', 's_study.txt', 'a_assay1.txt', 'a_assay2.txt']

    @staticmethod
    def retrbinary(filename, output_file):
        if filename.startswith('RETR i_'):
            output_file(MTBLS_i.encode('utf-8'))
        elif filename.startswith('RETR s_'):
            output_file(MTBLS_s.encode('utf-8'))
        elif filename.startswith('RETR a_'):
            output_file(MTBLS_a.encode('utf-8'))

    def close(self):
        pass


class MockMTBLSDownloader:
    pass


class TestMTBLSInvestigationBase(unittest.TestCase):

    @patch('isatools.net.metabolights.core.MTBLSDownloader', returned_value=MockMTBLSDownloader)
    def test_properties(self, mock_mtbls):
        with self.assertRaises(TypeError) as context:
            MTBLSInvestigationBase(mtbls_id=12)
        self.assertEqual(str(context.exception), "The MTBLS instance ID must be an string but got int")
        with self.assertRaises(ValueError) as context:
            MTBLSInvestigationBase(mtbls_id="MTBLS1", output_format="blah")
        self.assertEqual(str(context.exception), "The output format must be one of the following: json, json-ld, tab")

        investigation = MTBLSInvestigationBase(mtbls_id="MTBLS12", output_format="json")
        self.assertEqual(investigation.mtbls_id, "MTBLS12")
        self.assertEqual(investigation.format, "json")
        self.assertIsNotNone(investigation.output_dir)
        self.assertEqual(investigation.temp, True)

    @patch('isatools.net.metabolights.core.MTBLSDownloader', autospec=True)
    def test_get_investigation_success(self, mock_mtbls):
        mock = mock_mtbls.return_value
        mock.ftp = MockFTP
        investigation = MTBLSInvestigationBase(mtbls_id="MTBLS12", output_format="tab")
        investigation.get_investigation()

    @patch('isatools.net.metabolights.utils.FTP')
    def test_get_investigations_failure(self, mock_ftp):
        def mock_retrbinary(filename, output_file):
            raise error_perm('Mock FTP Failure')

        def mock_login_(*args, **kwargs):
            return "230 !!!"

        mock = mock_ftp.return_value
        mock.login = mock_login_
        mock.nlst.return_value = ['i_Investigation.txt', 's_study.txt']
        mock.retrbinary = mock_retrbinary

        investigation = MTBLSInvestigationBase(mtbls_id="MTBLS12", output_format="tab")
        self.assertIsNotNone(investigation.output_dir)

        with self.assertRaises(Exception) as context:
            investigation.get_investigation()
        self.assertEqual(str(context.exception), "Could not download a file: Mock FTP Failure for MTBLS12")

        mock.nlst.return_value = ['a.txt', 'b.txt']
        with self.assertRaises(Exception) as context:
            investigation.get_investigation()
        self.assertEqual(str(context.exception), "Could not find an investigation file for this study")


class TestMTBLSInvestigation(unittest.TestCase):
    investigation = MTBLSInvestigation(mtbls_id="MTBLS1", output_format="tab", ftp_server=MockFTP)

    @patch('isatools.net.metabolights.core.MTBLSDownloader', autospec=True)
    def test_constructor(self, mock_mtbls):
        mock = mock_mtbls.return_value
        mock.ftp = MockFTP
        investigation = MTBLSInvestigation(mtbls_id="MTBLS12", output_format="tab")
        self.assertIsInstance(investigation, MTBLSInvestigationBase)
        self.assertIsInstance(investigation, MTBLSInvestigation)

    def test_load_dataframes(self):
        self.investigation.load_dataframes()
        self.assertEqual(len(self.investigation.dataframes.keys()), 3)
        self.investigation.get()
        self.assertEqual(len(self.investigation.dataframes.keys()), 3)

    def test_load_json(self):
        self.investigation.load_json()
        self.assertEqual(self.investigation.investigation.identifier, "MTBLS1")

        # hitting cache
        self.investigation.get()
        self.assertEqual(self.investigation.investigation.identifier, "MTBLS1")

    def test_get_factor_names(self):
        self.assertEqual(self.investigation.get_factor_names(), {'Gender', 'Metabolic syndrome'})

    def test_get_factor_values(self):
        self.assertEqual(self.investigation.get_factor_values('Gender'), {'Male', 'Female'})

    def test_get_data_files(self):
        factor_selection = {"Gender": "Male", "Metabolic syndrome": "Control Group"}
        data_files = self.investigation.get_data_files(factor_selection=factor_selection)
        self.assertEqual(len(data_files), 56)
        self.assertEqual(len(data_files[0]['data_files']), 1)
        self.assertEqual(len(self.investigation.get_data_files({"Gender": "Male"})), 78)

    def test_get_factors_summary(self):
        self.assertEqual(len(self.investigation.get_factors_summary()), 132)

    def test_get_study_groups(self):
        study_groups = self.investigation.get_study_groups()
        self.assertEqual(len(study_groups), 4)

    def test_get_study_groups_samples_sizes(self):
        study_groups = self.investigation.get_study_groups_samples_sizes()
        self.assertEqual(study_groups[0][1], 22)
        self.assertEqual(study_groups[1][1], 26)
        self.assertEqual(study_groups[2][1], 56)
        self.assertEqual(study_groups[3][1], 28)

    def test_get_sources_for_sample(self):
        sources_for_sample = self.investigation.get_sources_for_sample("ADG10003u_066")
        self.assertEqual(sources_for_sample, ['ADG10003u'])

    def test_get_data_for_sample(self):
        data_for_sample = self.investigation.get_data_for_sample("ADG10003u_066")
        for data in data_for_sample:
            self.assertIsInstance(data, DataFile)

    def test_get_study_groups_data_sizes(self):
        study_groups_data_sizes = self.investigation.get_study_groups_data_sizes()
        self.assertEqual(study_groups_data_sizes[0][1], 22)
        self.assertEqual(study_groups_data_sizes[1][1], 26)
        self.assertEqual(study_groups_data_sizes[2][1], 56)
        self.assertEqual(study_groups_data_sizes[3][1], 28)

    def test_get_characteristics_summary(self):
        characteristics_summary = self.investigation.get_characteristics_summary()
        self.assertEqual(len(characteristics_summary), 132)

    def test_get_study_variable_summary(self):
        study_variable_summary = self.investigation.get_study_variable_summary()
        self.assertEqual(len(study_variable_summary), 132)

    def test_get_study_group_factors(self):
        study_group_factors = self.investigation.get_study_group_factors()
        self.assertEqual(len(study_group_factors), 4)

    @unittest.skip("get_filtered_df_on_factors_list is not working")
    def test_get_filtered_df_on_factors_list(self):
        from isatools.net.mtbls import get_filtered_df_on_factors_list
        t = get_filtered_df_on_factors_list('MTBLS1')
        filtered_df = self.investigation.get_filtered_df_on_factors_list()
        self.assertEqual(t, filtered_df)

    def test_get_factors_command(self):
        output_file = TextIO()
        factors = self.investigation.get_factors_command(output_file)
        for factor in factors:
            self.assertIn(factor, ['Metabolic syndrome', 'Gender'])

    def test_get_factor_values_command(self):
        output_file = TextIO()
        factor_values = self.investigation.get_factor_values_command('Gender', output_file)
        for fv in factor_values:
            self.assertIn(fv, ['Male', 'Female'])

