import unittest
import shutil
from isatools.convert import mzml2isa
from tests.utils import assert_tab_content_equal
from tests import utils
import tempfile
import os


class TestMzml2IsaTab(unittest.TestCase):

    def setUp(self):
        self._mzml_data_dir = utils.MZML_DATA_DIR
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_mzml2isa_convert_investigation(self):
        study_id = 'MTBLS267'
        report = mzml2isatab.convert(os.path.join(self._mzml_data_dir, study_id + '-partial'), self._tmp_dir, study_id,
                                  validate_output=True)
        self.assertTrue(report['validation_finished'])
        self.assertEqual(len(report['errors']), 0)
        self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, study_id, 'i_Investigation.txt')),
                                                 open(os.path.join(self._tab_data_dir, study_id + '-partial',
                                                                   'i_Investigation.txt'))))

    def test_mzml2isa_convert_study_table(self):
        study_id = 'MTBLS267'
        report = mzml2isatab.convert(os.path.join(self._mzml_data_dir, study_id + '-partial'), self._tmp_dir, study_id,
                                  validate_output=True)
        self.assertTrue(report['validation_finished'])
        self.assertEqual(len(report['errors']), 0)
        self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, study_id,
                                                                   's_{}.txt'.format(study_id))),
                                                 open(os.path.join(self._tab_data_dir, study_id + '-partial',
                                                                   's_{}.txt'.format(study_id)))))

    def test_mzml2isa_convert_assay_table(self):
        study_id = 'MTBLS267'
        report = mzml2isatab.convert(os.path.join(self._mzml_data_dir, study_id + '-partial'), self._tmp_dir, study_id,
                                  validate_output=True)
        self.assertTrue(report['validation_finished'])
        self.assertEqual(len(report['errors']), 0)
        self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, study_id,
                                                                   'a_{}_metabolite_profiling_mass_spectrometry.txt'
                                                                   .format(study_id))),
                                                 open(os.path.join(self._tab_data_dir, study_id + '-partial',
                                                                   'a_{}_metabolite_profiling_mass_spectrometry.txt'
                                                                   .format(study_id)))))
