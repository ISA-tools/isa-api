import unittest
import os
import shutil
from isatools.convert import isatab2magetab
from tests import utils
import tempfile


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestIsaTab2MageTab(unittest.TestCase):

    def setUp(self):
        self._json_data_dir = utils.JSON_DATA_DIR
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._magetab_data_dir = utils.MAGETAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab2magetab_convert_bii_i_1(self):
        with open(os.path.join(self._tab_data_dir, 'BII-I-1', 'i_investigation.txt')) as inv_fp:
            isatab2magetab.convert(inv_fp, self._tmp_dir)
            self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'BII-I-1.idf.txt')))
            self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'BII-S-1.transcriptome.sdrf.txt.sdrf.txt')))
            self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'BII-S-2.microarray.sdrf.txt.sdrf.txt')))

    def test_isatab2magetab_convert_bii_s_3(self):
        with open(os.path.join(self._tab_data_dir, 'BII-S-3', 'i_gilbert.txt')) as inv_fp:
            with self.assertRaises(IOError):
                isatab2magetab.convert(inv_fp, self._tmp_dir)

    def test_isatab2magetab_convert_bii_s_7(self):
        with open(os.path.join(self._tab_data_dir, 'BII-S-7', 'i_matteo.txt')) as inv_fp:
            with self.assertRaises(IOError):
                isatab2magetab.convert(inv_fp, self._tmp_dir)
