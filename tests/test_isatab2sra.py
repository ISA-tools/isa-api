from unittest import TestCase
import os
import shutil


class ISATabTest(TestCase):

    def setUp(self):
        """set up directories etc"""
        self._dir = os.path.join(os.path.dirname(__file__), "data")
        self._work_dir = os.path.join(self._dir, "BII-S-7")
        self._config_dir = os.path.join(self._dir, "Configurations/isaconfig-default_v2015-07-02")
        self._tmp = os.path.join(self._dir, './tmp/')
        if not os.path.exists(self._tmp):
            os.mkdir(self._tmp)

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_isatab_to_sra(self):
        from isatools.convert import isatab2sra
        isatab2sra.create_sra(self._work_dir, self._tmp, self._config_dir)
        self.assertTrue(os.path.exists(os.path.join(self._tmp, 'sra')))
