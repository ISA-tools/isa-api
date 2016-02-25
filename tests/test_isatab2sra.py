from unittest import TestCase
from io import BytesIO
from zipfile import ZipFile
import os
import shutil
from isatools.convert import isatab2sra


class ISATabTest(TestCase):

    def setUp(self):
        """set up directories etc"""
        self._dir = os.path.join(os.path.dirname(__file__), "data")
        self._config_dir = os.path.join(self._dir, "Configurations/isaconfig-default_v2015-07-02")
        self._tmp = os.path.join(self._dir, './tmp/')
        if not os.path.exists(self._tmp):
            os.mkdir(self._tmp)

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_isatab_to_sra_bii_s_3(self):
        work_dir = os.path.join(self._dir, "BII-S-3")
        res = isatab2sra.create_sra(work_dir, self._tmp, self._config_dir)
        self.assertIsInstance(res, BytesIO)

        # check that content was effectively written to response
        with ZipFile(res) as zip_file:
            self.assertGreater(len(zip_file.namelist()), 0)
        self.assertTrue(os.path.exists(os.path.join(self._tmp, 'sra')))

    def test_isatab_to_sra_bii_s_7(self):
        work_dir = os.path.join(self._dir, "BII-S-7")
        res = isatab2sra.create_sra(work_dir, self._tmp, self._config_dir)
        self.assertIsInstance(res, BytesIO)

        # check that content was effectively written to response
        with ZipFile(res) as zip_file:
            self.assertGreater(len(zip_file.namelist()), 0)
        self.assertTrue(os.path.exists(os.path.join(self._tmp, 'sra')))
