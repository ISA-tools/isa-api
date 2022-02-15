import unittest
import os
import shutil
from unittest.mock import patch
from isatools.convert import magetab2isatab
from isatools.tests import utils
import tempfile
from isatools.net import ax as AX
from isatools import isatab
from ddt import ddt, data


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


@ddt
class TestMageTab2IsaTab(unittest.TestCase):

    def setUp(self):
        self._json_data_dir = utils.JSON_DATA_DIR
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._magetab_data_dir = utils.MAGETAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_magetab2isatab_convert_e_mexp_31(self):
        magetab2isatab.convert(os.path.join(self._magetab_data_dir, 'E-MEXP-31.idf.txt'), self._tmp_dir)
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'i_investigation.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 's_E-MEXP-31_study.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir,
                                                    'a_E-MEXP-31_assay-transcription profiling by array.txt')))
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_magetab2isatab_convert_e_geod_59671(self):
        magetab2isatab.convert(os.path.join(self._magetab_data_dir, 'E-GEOD-59671.idf.txt'), self._tmp_dir)
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'i_investigation.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 's_E-GEOD-59671_study.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'a_E-GEOD-59671_assay-RNA-Seq.txt')))
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    """Tests on datasets suggest from prs"""
    @patch('isatools.net.ax.get')
    @data('E-MTAB-20', 'E-MTAB-584', 'E-MTAB-621', 'E-MTAB-1073', 'E-MTAB-1443', 'E-MTAB-1653', 'E-MTAB-1677',
          'E-MTAB-1963', 'E-MTAB-2143', 'E-MTAB-3336', 'E-MTAB-3624', 'E-MTAB-4649', 'E-MTAB-5171')
    def test_get_experiment_as_isatab_mtab(self, value, mock_ax_get):
        src = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'magetab', value)
        )
        dest = tempfile.mkdtemp()
        target = shutil.copytree(src, os.path.abspath(os.path.join(dest, value)))
        mock_ax_get.return_value = target
        AX.get_isatab(value, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    @patch('isatools.net.ax.get')
    def test_get_experiment_as_isatab_mtab_3954(self, mock_ax_get):  # Tests assay splitting
        value = 'E-MTAB-3954'
        src = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'magetab', value)
        )
        dest = tempfile.mkdtemp()
        target = shutil.copytree(src, os.path.abspath(os.path.join(dest, value)))
        mock_ax_get.return_value = target
        AX.get_isatab(value, self._tmp_dir)
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'i_investigation.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 's_E-MTAB-3954_study.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'a_E-MTAB-3954_assay-ChIP-Seq.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'a_E-MTAB-3954_assay-Chromatin-Seq.txt')))