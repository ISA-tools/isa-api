import unittest
import os
import shutil


class ISATabTest(unittest.TestCase):

    def setUp(self):
        """set up directories etc"""
        self._dir = os.path.join(os.path.dirname(__file__), "data")
        self._work_dir = os.path.join(self._dir, "BII-S-3")
        self._sra_dir = self._work_dir + "-sra"
        if not os.path.exists(self._sra_dir):
            os.makedirs(self._sra_dir)

    def tearDown(self):
        shutil.rmtree(self._sra_dir, ignore_errors=True)
        pass

    def test_isatab_to_sra(self):
        from isatools.convert import isatab2sra
        isatab2sra.create_sra(self._work_dir, self._sra_dir)