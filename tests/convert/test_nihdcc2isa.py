import unittest
import shutil
import os
import tempfile
from isatools.tests import utils
from isatools.convert.experimental import nih_dcc_flux as nihdcc


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self._nih_dcc_data_dir = utils.NIH_DCC_DATA_DIR
        self._tab_data_dir = os.path.join(utils.TAB_DATA_DIR, 'TEST-ISA-NIHDCC')
        self._tmp_dir = tempfile.mkdtemp()

    # def tearDown(self):
    #     shutil.rmtree(self._tmp_dir)

    def test_nihdcc2isa(self):
        nihdccjson = os.path.join(self._nih_dcc_data_dir, 'nih-dcc-metadata4.json')
        result = nihdcc.nihdcc2isa_convert(nihdccjson, output_path=self._tab_data_dir)
        # self.assertEqual(result, stored)
        # self.assertEqual(True, False)  # add assertion here
