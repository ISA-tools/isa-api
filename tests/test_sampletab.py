import unittest
from tests import utils
from isatools import sampletab
from isatools import isatab
import os


class UnitSampleTabLoad(unittest.TestCase):

    def setUp(self):
        self._sampletab_data_dir = utils.SAMPLETAB_DATA_DIR

    def tearDown(self):
        pass

    def test_sampletab_load_test1(self):
        with open(os.path.join(self._sampletab_data_dir, 'test1.txt')) as fp:
            ISA = sampletab.load(fp)
            self.assertEqual(len(ISA.studies), 1)
            self.assertEqual(len(ISA.studies[0].materials['sources']), 1)
            self.assertEqual(len(ISA.studies[0].materials['samples']), 1)
            print(isatab.dumps(ISA))

    # def test_sampletab_load_gsb_718(self):
    #     with open(os.path.join(self._sampletab_data_dir, 'GSB-718.txt')) as fp:
    #         ISA = sampletab.load(fp)
    #         self.assertEqual(len(ISA.studies), 1)
    #         self.assertEqual(len(ISA.studies[0].materials['sources']), 51)
    #         self.assertEqual(len(ISA.studies[0].materials['samples']), 2409)
    #         print(isatab.dumps(ISA))