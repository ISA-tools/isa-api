import unittest
import os
from isatools.convert import magetab2json
from isatools.tests import utils
import json
from isatools import isajson
import tempfile
import shutil


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestMageTab2IsaJson(unittest.TestCase):

    def setUp(self):
        self._json_data_dir = utils.JSON_DATA_DIR
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._magetab_data_dir = utils.MAGETAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_magetab2json_convert_e_mexp_31(self):
        actual_json = magetab2json.convert(os.path.join(self._magetab_data_dir, 'E-MEXP-31.idf.txt'),)
        with open(os.path.join(self._tmp_dir, 'isa.json'), 'w') as out_fp:
            json.dump(actual_json, out_fp)
        with open(os.path.join(self._tmp_dir, 'isa.json')) as actual_json:
            report = isajson.validate(actual_json)
            self.assertEqual(len(report['errors']), 0)
