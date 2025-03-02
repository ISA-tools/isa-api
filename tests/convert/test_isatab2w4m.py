# Test conversion to W4M format

import os
import shutil
import tempfile
import unittest
from isatools.convert import isatab2w4m
from isatools.tests import utils


def universal_filecmp(f1, f2):
    with open(f1, 'r') as fp1, open(f2, 'r') as fp2:
        while True:
            b1 = fp1.readline()
            b2 = fp2.readline()
            if b1 != b2:
                return False
            if not b1:
                return True

# Test presence of data folder
def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError(
            'Could not fine test data directory in {0}. Ensure you have cloned '
            'the ISAdatasets repository using git clone -b tests '
            '--single-branch git@github.com:ISA-tools/ISAdatasets {0}'.format(
                utils.DATA_DIR))
 
 
# Test class
class TestIsatab2w4m(unittest.TestCase):

    # Initialize instance resources
    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    # Destroy resources
    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def plain_test(self, study, test_dir):
        # Convert
        isatab2w4m.convert(
            input_dir=os.path.join(utils.TAB_DATA_DIR, test_dir), 
            output_dir=self._tmp_dir, 
            sample_output='%s-w4m-sample-metadata.tsv', 
            variable_output='%s-w4m-variable-metadata.tsv', 
            matrix_output='%s-w4m-sample-variable-matrix.tsv')
        # Check files
        for x in [
                'sample-metadata', 'variable-metadata', 'sample-variable-matrix']:
            ref_file = os.path.join(utils.TAB_DATA_DIR, test_dir, '.'.join(
                ['-'.join([study, 'w4m', x]), 'tsv']))
            output_file = os.path.join(self._tmp_dir, '.'.join(
                ['-'.join([study, 'w4m', x]), 'tsv']))
            self.assertTrue(os.path.exists(output_file))
            self.assertTrue(universal_filecmp(output_file, ref_file),
                            'Output file "{0}" differs from reference file "{1}".'.format(output_file, ref_file))

    # Test MTBLS30
    def test_MTBLS30(self):
        self.plain_test('MTBLS30', 'MTBLS30-w4m')

    # Test MTBLS404
    def test_MTBLS404(self):
        self.plain_test('MTBLS404', 'MTBLS404-w4m')

    # Test MTBLS338
    def test_MTBLS338(self):
        self.plain_test('MTBLS338', 'MTBLS338-w4m')

    # Test NA filtering
    def na_filtering_test(self, study, test_dir, samp_na_filtering=None, 
                          var_na_filtering=None):
        var_filtering = ','.join(var_na_filtering)

        # Set file names
        output_files = dict()
        ref_files = dict()
        for x in [
                'sample-metadata', 'variable-metadata', 'sample-variable-matrix']:
            filename = '.'.join(
                ['-'.join([study, 'w4m', var_filtering, x, 'na-filtering']), 
                 'tsv'])
            output_files[x] = os.path.join(self._tmp_dir, filename)
            ref_files[x] = os.path.join(utils.TAB_DATA_DIR, test_dir, filename)
        # Convert
        isatab2w4m.convert(input_dir=os.path.join(utils.TAB_DATA_DIR, test_dir),
                           output_dir=self._tmp_dir,
                           sample_output=output_files['sample-metadata'],
                           variable_output=output_files['variable-metadata'],
                           matrix_output=output_files['sample-variable-matrix'],
                           samp_na_filtering=samp_na_filtering,
                           var_na_filtering=var_na_filtering)
        # Check files
        for x in [
                'sample-metadata', 'variable-metadata', 'sample-variable-matrix']:
            self.assertTrue(os.path.exists(output_files[x]))
        self.assertTrue(
            universal_filecmp(output_files[x], ref_files[x]),
            'Output file "{0}" differs from reference file "{1}".'.format(
                output_files[x], ref_files[x]))

    # Test MTBLS404 NA filtering
    def test_MTBLS404_na_filtering(self):
        self.na_filtering_test('MTBLS404', 'MTBLS404-w4m',
                               samp_na_filtering=['Characteristics[gender]'],
                               var_na_filtering=['mass_to_charge'])
        self.na_filtering_test('MTBLS404', 'MTBLS404-w4m',
                               samp_na_filtering=['Characteristics[gender]'],
                               var_na_filtering=['mass_to_charge',
                                                 'mass_to_charge'])
        self.na_filtering_test('MTBLS404', 'MTBLS404-w4m',
                               samp_na_filtering=['Characteristics[gender]'],
                               var_na_filtering=['charge'])
        self.na_filtering_test('MTBLS404', 'MTBLS404-w4m',
                               samp_na_filtering=['Characteristics[gender]'],
                               var_na_filtering=['database'])
        self.na_filtering_test('MTBLS404', 'MTBLS404-w4m',
                               samp_na_filtering=['Characteristics[gender]'],
                               var_na_filtering=['charge', 'database'])

    # Test assay selection
    def test_assay_selection(self):

        study = 'MTBLS30'
        test_dir = 'MTBLS30-w4m'

        for assay in ['a_york_src_GC_mass_spectrometry.txt',
                      'a_york_src_FIA_mass_spectrometry.txt']:

            # Convert
            isatab2w4m.convert(
                input_dir=os.path.join(utils.TAB_DATA_DIR, test_dir),
                output_dir=self._tmp_dir,
                sample_output='%s-w4m-sample-metadata-{0}.tsv'.format(assay),
                variable_output='%s-w4m-variable-metadata-{0}.tsv'.format(
                    assay),
                matrix_output='%s-w4m-sample-variable-matrix-{0}.tsv'.format(
                    assay), assay_filename=assay)

            # Check files
            for x in ['sample-metadata', 'variable-metadata',
                      'sample-variable-matrix']:
                ref_file = os.path.join(utils.TAB_DATA_DIR, test_dir, '.'.join(
                    ['-'.join([study, 'w4m', x, assay]), 'tsv']))
                output_file = os.path.join(self._tmp_dir, '.'.join(
                    ['-'.join([study, 'w4m', x, assay]), 'tsv']))
                self.assertTrue(os.path.exists(output_file))
                self.assertTrue(
                    universal_filecmp(output_file, ref_file),
                    'Output file "{0}" differs from reference file "{1}".'.format(output_file, ref_file))
