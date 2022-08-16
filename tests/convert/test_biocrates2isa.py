import unittest
import shutil
import tempfile
import os
import uuid

from isatools.tests import utils
from isatools.convert.experimental import biocrates2isatab as bc2isa
from isatools.convert.experimental.biocrates2isatab import DEFAULT_SAXON_EXECUTABLE, BIOCRATES_INPUT_XML, DESTINATION_DIR


class TestBiocrates2isatab(unittest.TestCase):

    def setUp(self):
        self._biocrates_data_dir = utils.BIOCRATES_DATA_DIR
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()
        test_case = 'TEST-ISA-BIOCRATES'
        input_path = os.path.join(self._tab_data_dir, test_case)

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_biocrates2isa(self):

        dir_name = "output/isatab"
        dest_path = os.path.join(DESTINATION_DIR, dir_name)
        bc2isa.biocrates_to_isatab_convert(BIOCRATES_INPUT_XML, dest_path, saxon_jar_path=DEFAULT_SAXON_EXECUTABLE)
