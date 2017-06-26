import unittest
import os
import shutil
from isatools.convert import magetab2isatab
from tests import utils
import tempfile
from isatools.io import ax as AX
from isatools import isatab


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestMageTab2IsaTab(unittest.TestCase):

    def setUp(self):
        self._json_data_dir = utils.JSON_DATA_DIR
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._magetab_data_dir = utils.MAGETAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_magetab2isatab_convert_e_mexp_31(self):
        magetab2isatab.convert(os.path.join(self._magetab_data_dir, 'E-MEXP-31.idf.txt'), self._tmp_dir, 'protein microarray', 'protein expression profiling')
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'i_investigation.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 's_E-MEXP-31.sdrf.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'a_E-MEXP-31.sdrf.txt')))
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_magetab2isatab_convert_e_geod_59671(self):
        magetab2isatab.convert(os.path.join(self._magetab_data_dir, 'E-GEOD-59671.idf.txt'), self._tmp_dir)
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'i_investigation.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 's_E-GEOD-59671.sdrf.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'a_E-GEOD-59671.sdrf.txt')))
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_afmx_1(self):
        AX.get_isatab('E-AFMX-1', self._tmp_dir)  # gets E-AFMX-1 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_afmx_2(self):  # FIXME -> output ISA-Tab has many missing cells! See #222
        AX.get_isatab('E-AFMX-2', self._tmp_dir)  # gets E-AFMX-2 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_afmx_3(self):
        AX.get_isatab('E-AFMX-3', self._tmp_dir)  # gets E-AFMX-3 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_afmx_5(self):
        AX.get_isatab('E-AFMX-5', self._tmp_dir)  # gets E-AFMX-5 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    """Tests on datasets suggest from prs"""

    def test_get_experiment_as_isatab_mtab_584(self):
        AX.get_isatab('E-MTAB-584', "/Users/dj/PycharmProjects/isa-api/tests/data/tmp")  # gets E-MTAB-584 MAGE-TAB files
        with open(os.path.join("/Users/dj/PycharmProjects/isa-api/tests/data/tmp", 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_mtab_1073(self):  # FIXME: Fails because is ISO-8859-2 (Latin 2) encoding, not utf-8
        AX.get_isatab('E-MTAB-1073', self._tmp_dir)  # gets E-MTAB-1073 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_mtab_4649(self):
        AX.get_isatab('E-MTAB-4649', self._tmp_dir)  # gets E-MTAB-4649 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_mtab_1936(self):  # check transcription profiling list
        AX.get_isatab('E-MTAB-1936', self._tmp_dir)  # gets E-MTAB-1936 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_mtab_621(self):
        AX.get_isatab('E-MTAB-621', self._tmp_dir)  # gets E-MTAB-621 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_mtab_3624(self):
        AX.get_isatab('E-MTAB-3624', self._tmp_dir)  # gets E-MTAB-3624 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_mtab_20(self):
        AX.get_isatab('E-MTAB-20', self._tmp_dir)  # gets E-MTAB-20 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_mtab_1443(self):  # FIXME: Fails because of wrong pointer to dl SDRFs
        AX.get_isatab('E-MTAB-1443', self._tmp_dir)  # gets E-MTAB-1443 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_mtab_3336(self):
        AX.get_isatab('E-MTAB-3336', self._tmp_dir)  # gets E-MTAB-3336 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_mtab_1677(self):
        AX.get_isatab('E-MTAB-1677', self._tmp_dir)  # gets E-MTAB-1677 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_mtab_1653(self):
        AX.get_isatab('E-MTAB-1653', self._tmp_dir)  # gets E-MTAB-1653 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_mtab_2143(self):
        AX.get_isatab('E-MTAB-2143', self._tmp_dir)  # gets E-MTAB-2143 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)

    def test_get_experiment_as_isatab_mtab_5171(self):
        AX.get_isatab('E-MTAB-5171', self._tmp_dir)  # gets E-MTAB-5171 MAGE-TAB files
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as i_fp:
            isatab.validate(i_fp)
