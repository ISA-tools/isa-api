import os
import unittest
from isatools import isatab2
from tests import utils


class TestIsaTab2JsonIdentifierName(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR

    def test_isatab2json_convert_charac_param_factor(self):
        test_case = 'TEST-ISA-charac-param-factor'
        df = isatab2.read_tfile(os.path.join(self._tab_data_dir, test_case, 'a_test-template1-splitting_transcription_profiling_DNA_microarray.txt'))
        sources, samples, other_material, data, processes, process_sequences = isatab2.ProcessSequenceFactory().create_from_df(df)
        print(sources, samples, other_material, data, processes, process_sequences)
        self.assertEqual(len(sources), 0)  # expecting no sources
        self.assertEqual(len(samples), 2)  # expecting 2 samples
        self.assertEqual(len(other_material), 4)  # expecting 2 extracts, 2 labeled extracts
        self.assertEqual(len(data), 4)  # expecting 3 array data files and 1 derived array data file
        self.assertEqual(len(processes), 21)  # expecting 18 processes (3 sets of 7)
        self.assertEqual(len(process_sequences), 3)  # expecting 3 process sequences