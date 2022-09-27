import os
import unittest
from isatools.convert import isatab2sampletab
from isatools.tests import utils
import tempfile
import shutil


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestIsaTab2SampleTab(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._sampletab_dir = utils.SAMPLETAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab2sampletab_bii_i_1(self):
        with open(os.path.join(self._tab_data_dir, "BII-I-1", "i_investigation.txt")) as i_fp:
            with open(os.path.join(self._tmp_dir, "samples.txt"), "w") as out_fp:
                isatab2sampletab.convert(source_inv_fp=i_fp, target_fp=out_fp)

    def test_isatab2sampletab_bii_s_3(self):
        with open(os.path.join(self._tab_data_dir, "BII-S-3", "i_gilbert.txt")) as i_fp:
            with open(os.path.join(self._tmp_dir, "samples.txt"), "w") as out_fp:
                isatab2sampletab.convert(source_inv_fp=i_fp, target_fp=out_fp)

    def test_isatab2sampletab_bii_s_7(self):
        with open(os.path.join(self._tab_data_dir, "BII-S-7", "i_matteo.txt")) as i_fp:
            with open(os.path.join(self._tmp_dir, "samples.txt"), "w") as out_fp:
                isatab2sampletab.convert(source_inv_fp=i_fp, target_fp=out_fp)
