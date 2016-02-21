import os
from unittest import TestCase
from isatools.convert import isatab2json, json2isatab
from isatools import isatab
import shutil


class TwoWayConvertTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)
        self._tmp = os.path.join(self._dir, './tmp/')
        if not os.path.exists(self._tmp):
            os.mkdir(self._tmp)

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_isa_bii_s_3(self):
        source_dir = os.path.join(self._dir, 'data/BII-S-3/')
        isatab2json.convert(source_dir, self._tmp)
        json2isatab.convert(open(os.path.join(self._tmp, 'BII-S-3.json')), self._tmp)
        isatab.assert_tab_equal(open(os.path.join(source_dir, 'i_gilbert.txt')),
                                open(os.path.join(self._tmp, 'i_investigation.txt')))
        isatab.assert_tab_equal(open(os.path.join(source_dir, 's_BII-S-3.txt')),
                                open(os.path.join(self._tmp, 's_BII-S-3.txt')))
        isatab.assert_tab_equal(open(os.path.join(source_dir, 'a_gilbert-assay-Gx.txt')),
                                open(os.path.join(self._tmp, 'a_gilbert-assay-Gx.txt')))
        isatab.assert_tab_equal(open(os.path.join(source_dir, 'a_gilbert-assay-Tx.txt')),
                                open(os.path.join(self._tmp, 'a_gilbert-assay-Tx.txt')))
