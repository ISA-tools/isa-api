"""Tests for importing from SRA XML 1.5 to ISA-Tab"""
import unittest
import os
import shutil
import tempfile
import zipfile
import warnings

from os import path, walk, listdir, remove
from unittest.mock import patch, MagicMock
from io import BytesIO
from isatools.net import sra2isatab
from isatools.tests import utils


SLOW_TESTS = int(os.getenv('SLOW_TESTS', '0'))


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError(
            "Could not fine test data directory in {0}. Ensure you have cloned "
            "the ISAdatasets repository using "
            "git clone -b tests --single-branch "
            "git@github.com:ISA-tools/ISAdatasets {0}".format(utils.DATA_DIR))


class TestZipDir(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file1 = os.path.join(self.test_dir.name, "file1.txt")
        self.test_file2 = os.path.join(self.test_dir.name, "file2.txt")

        # Create some dummy files
        with open(self.test_file1, 'w') as f:
            f.write("Hello from file 1")
        with open(self.test_file2, 'w') as f:
            f.write("Hello from file 2")

        # Temp file for zip
        self.zip_path = os.path.join(self.test_dir.name, "test.zip")
        self.zip_file = zipfile.ZipFile(self.zip_path, 'w')

    def tearDown(self):
        self.zip_file.close()
        self.test_dir.cleanup()

    def test_zipdir_adds_all_files(self):
        sra2isatab.zipdir(self.test_dir.name, self.zip_file)
        self.zip_file.close()

        # Open the zip and verify contents
        with zipfile.ZipFile(self.zip_path, 'r') as z:
            names = z.namelist()

            # Only the files should be in the zip, not the zip itself
            self.assertIn("file1.txt", [os.path.basename(n) for n in names])
            self.assertIn("file2.txt", [os.path.basename(n) for n in names])


class TestSraImport(unittest.TestCase):

    # TODO: Use local data to test
    def setUp(self):

        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    # https://www.ebi.ac.uk/ena/data/view/SRA108974&amp;display=xml

    @unittest.skipIf(not SLOW_TESTS, "slow")
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

    @patch("subprocess.call")
    def test_sra_import_mocked(self, mock_call):
        with self.assertRaises(FileNotFoundError, msg='as subprocess.call is mocked files are nor generated'):
            sra2isatab.sra_to_isatab_batch_convert('SRA108974')
            mock_call.assert_called_with('java', '-jar')


