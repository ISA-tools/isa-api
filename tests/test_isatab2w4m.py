# Test conversion to W4M format
# To run this test, run the following command from root directory:
# coverage run --source isatools -m py.test tests/test_isatab2w4m.py

import os
import tempfile
import unittest
from isatools.convert import isatab2w4m
from isatools.tests import utils

# Test presence of data folder
def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))
 
# Test class
class TestIsaTab2W4m(unittest.TestCase):

    # Initialize instance resources
    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    # Destroy resources
    def tearDown(self):
        #shutil.rmtree(self._tmp_dir)
        pass
        
    # Test MTBLS30
    def test_isatab2w4m_convert_MTBLS30(self):
        test_case = 'MTBLS30-2'
        isatab2w4m.convert(input_dir = os.path.join(utils.TAB_DATA_DIR, test_case), output_dir = self._tmp_dir, sample_output = '%s-w4m-sample-metadata.tsv', variable_output = '%s-w4m-variable-metadata.tsv', matrix_output = '%s-w4m-sample-variable-matrix.tsv')
        raise RuntimeError('BLABLA ' + self._tmp_dir)
