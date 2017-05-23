import unittest
import os
import shutil
from isatools.convert import magetab2isatab
from tests import utils
import tempfile


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
        with open(os.path.join(self._magetab_data_dir, 'E-MEXP-31.idf.txt')) as idf_fp:
            magetab2isatab.convert(idf_fp, self._tmp_dir)
            self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'i_investigation.txt')))
            self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 's_E-MEXP-31.txt')))
            self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'a_E-MEXP-31.txt')))

