import unittest
from tests import utils
from isatools import sampletab
from isatools import isatab


class UnitSampleTabLoad(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR

    def tearDown(self):
        pass

    def test_sampletab_load_test1(self):
        with open('/Users/dj/PycharmProjects/isa-api/tests/data/sampletab/test1.txt') as fp:
            ISA = sampletab.load(fp)
            self.assertEqual(len(ISA.studies), 1)
            self.assertEqual(len(ISA.studies[0].materials['sources']), 1)
            self.assertEqual(len(ISA.studies[0].materials['samples']), 1)
            # print(isatab.dumps(ISA))