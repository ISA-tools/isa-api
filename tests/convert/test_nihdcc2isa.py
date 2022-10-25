import unittest
import shutil
import os
import tempfile
from isatools.tests import utils
from isatools.tests.utils import assert_tab_content_equal
from isatools.convert.experimental import nih_dcc_flux as nihdcc


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self._nih_dcc_data_dir = utils.NIH_DCC_DATA_DIR
        self._tab_data_dir = os.path.join(utils.TAB_DATA_DIR, 'TEST-ISA-NIHDCC')
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_nihdcc2isa(self):

        nihdccjson = os.path.join(self._nih_dcc_data_dir, 'nih-dcc-metadata4.json')
        nihdcc.nihdcc2isa_convert(nihdccjson, output_path=self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 'i_investigation.txt')) as out_fp:
            with open(os.path.join(self._tab_data_dir, 'i_investigation.txt')) as reference_fp:
                self.assertTrue(assert_tab_content_equal(out_fp, reference_fp))
