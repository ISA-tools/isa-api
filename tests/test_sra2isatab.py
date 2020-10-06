"""Tests for importing from SRA XML 1.5 to ISA-Tab"""
import unittest
import os
import shutil
import tempfile
import zipfile

from isatools.tests import utils
from isatools.net import sra2isatab


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError(
            "Could not fine test data directory in {0}. Ensure you have cloned "
            "the ISAdatasets repository using "
            "git clone -b tests --single-branch "
            "git@github.com:ISA-tools/ISAdatasets {0}".format(utils.DATA_DIR))


class TestSraImport(unittest.TestCase):

    # TODO: Use local data to test
    def setUp(self):

        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    # def tearDown(self):
    #     shutil.rmtree(self._tmp_dir)

   # https://www.ebi.ac.uk/ena/data/view/SRA108974&amp;display=xml

    def test_sra_import(self):
        zipped_bytes = sra2isatab.sra_to_isatab_batch_convert('SRA108974')
        with open(os.path.join(self._tmp_dir, 'o.zip'), 'wb') as zip_fp:
            shutil.copyfileobj(zipped_bytes, zip_fp, length=131072)

        with zipfile.ZipFile(
                os.path.join(self._tmp_dir, 'o.zip'), 'r') as zip_fp:
            self.assertListEqual(
                sorted([os.path.basename(x) for x in zip_fp.namelist()]),
                ['a_wgs-genomic.txt', 'i_SRA108974.txt', 's_SRA108974.txt']
            )
