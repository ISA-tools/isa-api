import os
import unittest
from isatools import isatab2
from tests import utils
import shutil
import tempfile


class TestIsaTab2(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab2_investigation_load_bii_i_1(self):
        test_case = 'BII-I-1'
        with open(os.path.join(self._tab_data_dir, test_case, 'i_investigation.txt')) as test_fp:
            I = isatab2.StudyFactory().create_from_fp(test_fp)
            self.assertEqual(I.identifier, 'BII-I-1')
            self.assertEqual(I.title, 'Growth control of the eukaryote cell: a systems biology study in yeast')
            # self.assertEqual(I.submission_date, '30/04/2007')
            # self.assertEqual(I.public_release_date, '10/03/2009')
            
            self.assertEqual(len(I.ontology_source_references), 7)
            self.assertEqual(len(I.publications), 1)
            self.assertEqual(len(I.contacts), 3)
            self.assertEqual(len(I.studies), 2)

            self.assertEqual(len(I.studies[0].design_descriptors), 1)
            self.assertEqual(len(I.studies[0].publications), 1)
            self.assertEqual(len(I.studies[0].factors), 2)
            self.assertEqual(len(I.studies[0].protocols), 7)
            self.assertEqual(len(I.studies[0].contacts), 3)
            self.assertEqual(len(I.studies[0].assays), 3)
            # TODO: Check counts of processes
            self.assertEqual(len(I.studies[0].assays[0].process_sequence), 16)
            self.assertEqual(len(I.studies[0].assays[1].process_sequence), 92)
            self.assertEqual(len(I.studies[0].assays[2].process_sequence), 144)
            
            self.assertEqual(len(I.studies[1].design_descriptors), 1)
            self.assertEqual(len(I.studies[1].publications), 1)
            self.assertEqual(len(I.studies[1].factors), 3)
            self.assertEqual(len(I.studies[1].assays), 1)
            self.assertEqual(len(I.studies[1].protocols), 4)
            self.assertEqual(len(I.studies[1].contacts), 3)
            self.assertEqual(len(I.studies[1].assays), 1)
            # TODO: Check counts of processes
            self.assertEqual(len(I.studies[1].assays[0].process_sequence), 30)

    def test_isatab2_investigation_load_bii_s_3(self):
        test_case = 'BII-S-3'
        with open(os.path.join(self._tab_data_dir, test_case, 'i_gilbert.txt')) as test_fp:
            I = isatab2.StudyFactory().create_from_fp(test_fp)
            self.assertEqual(I.identifier, 'BII-S-3')
            self.assertEqual(I.title, '')
            # self.assertEqual(I.submission_date, '30/04/2007')
            # self.assertEqual(I.public_release_date, '10/03/2009')

            self.assertEqual(len(I.ontology_source_references), 5)
            self.assertEqual(len(I.publications), 0)
            self.assertEqual(len(I.contacts), 0)
            self.assertEqual(len(I.studies), 1)

            self.assertEqual(len(I.studies[0].design_descriptors), 1)
            self.assertEqual(len(I.studies[0].publications), 2)
            self.assertEqual(len(I.studies[0].factors), 3)
            self.assertEqual(len(I.studies[0].protocols), 8)
            self.assertEqual(len(I.studies[0].contacts), 7)
            self.assertEqual(len(I.studies[0].assays), 2)
            # TODO: Check counts of processes
            self.assertEqual(len(I.studies[0].assays[0].process_sequence), 18)
            self.assertEqual(len(I.studies[0].assays[1].process_sequence), 36)

    def test_isatab2_investigation_load_bii_s_7(self):
        test_case = 'BII-S-7'
        with open(os.path.join(self._tab_data_dir, test_case, 'i_matteo.txt')) as test_fp:
            I = isatab2.StudyFactory().create_from_fp(test_fp)
            self.assertEqual(I.identifier, 'BII-S-7')
            self.assertEqual(I.title, '')
            # self.assertEqual(I.submission_date, '30/04/2007')
            # self.assertEqual(I.public_release_date, '10/03/2009')

            self.assertEqual(len(I.ontology_source_references), 7)
            self.assertEqual(len(I.publications), 0)
            self.assertEqual(len(I.contacts), 0)
            self.assertEqual(len(I.studies), 1)

            self.assertEqual(len(I.studies[0].design_descriptors), 1)
            self.assertEqual(len(I.studies[0].publications), 1)
            self.assertEqual(len(I.studies[0].factors), 1)
            self.assertEqual(len(I.studies[0].protocols), 5)
            self.assertEqual(len(I.studies[0].contacts), 10)
            self.assertEqual(len(I.studies[0].assays), 1)
            # TODO: Check counts of processes
            self.assertEqual(len(I.studies[0].assays[0].process_sequence), 116)

    def test_isatab2_charac_param_factor(self):
        test_case = 'TEST-ISA-charac-param-factor'
        df = isatab2.read_tfile(os.path.join(self._tab_data_dir, test_case, 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt'))
        sources, samples, other_material, data, processes, process_sequences = isatab2.ProcessSequenceFactory().create_from_df(df)
        print(sources, samples, other_material, data, processes, process_sequences)
        self.assertEqual(len(sources), 0)  # expecting no sources
        self.assertEqual(len(samples), 2)  # expecting 2 samples
        self.assertEqual(len(other_material), 4)  # expecting 2 extracts, 2 labeled extracts
        self.assertEqual(len(data), 4)  # expecting 3 array data files and 1 derived array data file
        self.assertEqual(len(processes), 11)  # expecting 11 processes
        # self.assertEqual(len(process_sequences), 3)  # expecting 3 process sequences

    def test_isatab2_bii_s_7(self):
        test_case = 'BII-S-7'
        df = isatab2.read_tfile(os.path.join(self._tab_data_dir, test_case, 'a_matteo-assay-Gx.txt'))
        sources, samples, other_material, data, processes, process_sequences = isatab2.ProcessSequenceFactory().create_from_df(df)
        print(sources, samples, other_material, data, processes, process_sequences)
        self.assertEqual(len(sources), 0)  # expecting no sources
        self.assertEqual(len(samples), 29)  # expecting 29 samples
        self.assertEqual(len(other_material), 29)  # expecting 29 extracts
        self.assertEqual(len(data), 29)  # expecting 29 raw data files
        self.assertEqual(len(processes), 116)  # expecting 116 processes (29 sets of 4)
        # self.assertEqual(len(process_sequences), 29)  # expecting 29 process sequences
        #  TODO: Fix processes and sequences to combine repeated parts to build graph properly.

    def test_isatab2_bii_s_3_Gx(self):
        test_case = 'BII-S-3'
        df = isatab2.read_tfile(os.path.join(self._tab_data_dir, test_case, 'a_gilbert-assay-Gx.txt'))
        sources, samples, other_material, data, processes, process_sequences = isatab2.ProcessSequenceFactory().create_from_df(df)
        print(sources, samples, other_material, data, processes, process_sequences)
        self.assertEqual(len(sources), 0)  # expecting no sources
        self.assertEqual(len(samples), 4)  # expecting 4 samples
        self.assertEqual(len(other_material), 4)  # expecting 4 extracts
        self.assertEqual(len(data), 6)  # expecting 6 raw data files
        self.assertEqual(len(processes), 18)  # expecting 18 processes
        # self.assertEqual(len(process_sequences), 6)  # expecting 6 process sequences
        #  TODO: Fix processes and sequences to combine repeated parts to build graph properly
