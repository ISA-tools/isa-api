import os
import unittest
from isatools.convert import json2sampletab
from isatools.tests import utils
import tempfile
import shutil


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestJson2SampleTab(unittest.TestCase):

    def setUp(self):
        self._json_dir = utils.JSON_DATA_DIR
        self._sampletab_dir = utils.SAMPLETAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_json2sampletab_bii_i_1(self):
        with open(os.path.join(self._json_dir, "BII-I-1", "BII-I-1.json")) as json_fp:
            with open(os.path.join(self._tmp_dir, "samples.txt"), "w") as out_fp:
                json2sampletab.convert(source_json_fp=json_fp, target_fp=out_fp)

    def test_json2sampletab_bii_s_3(self):
        with open(os.path.join(self._json_dir, "BII-S-3", "BII-S-3.json")) as json_fp:
            with open(os.path.join(self._tmp_dir, "samples.txt"), "w") as out_fp:
                json2sampletab.convert(source_json_fp=json_fp, target_fp=out_fp)

    def test_json2sampletab_bii_s_7(self):
        with open(os.path.join(self._json_dir, "BII-S-7", "BII-S-7.json")) as json_fp:
            with open(os.path.join(self._tmp_dir, "samples.txt"), "w") as out_fp:
                json2sampletab.convert(source_json_fp=json_fp, target_fp=out_fp)
