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
            # print(isatab.dumps(ISA))

    def test_sampletab_load_test2(self):
        with open(os.path.join(self._sampletab_data_dir, 'test2.txt')) as fp:
            ISA = sampletab.load(fp)
            self.assertEqual(len(ISA.studies), 1)
            self.assertEqual(len(ISA.studies[0].materials['sources']), 1)
            self.assertEqual(len(ISA.studies[0].materials['samples']), 2)
            self.assertEqual(len(ISA.studies[0].process_sequence), 1)
            # print(isatab.dumps(ISA))

    def test_sampletab_load_gsb_718(self):
        with open(os.path.join(self._sampletab_data_dir, 'GSB-718.txt')) as fp:
            ISA = sampletab.load(fp)
            self.assertEqual(len(ISA.studies), 1)
            self.assertEqual(len(ISA.studies[0].materials['sources']), 51)  # 51 organism
            self.assertEqual(len(ISA.studies[0].materials['samples']), 2409) # 2337 specimen from org + 72 cell specimen
            self.assertEqual(len(ISA.studies[0].process_sequence), 109)
            # print(isatab.dumps(ISA))  # looking for 2351 paths
            # isatab.dump(ISA, "/Users/dj/PycharmProjects/isa-api/tests/data/tmp")


class UnitSampleTabDump(unittest.TestCase):

    def setUp(self):
        self._sampletab_data_dir = utils.SAMPLETAB_DATA_DIR

    def tearDown(self):
        pass

    def test_sampletab_dump_test1(self):
        pass

    def test_sampletab_dump_test2(self):
        pass

    def test_sampletab_dump_gsb_718(self):
        pass
