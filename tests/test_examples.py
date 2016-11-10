import unittest
import sys
from io import StringIO


class TestSimpleExamples(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_simple_ISA(self):
        from isatools.examples import createSimpleISA as eg
        sys.stdout = StringIO()
        out = eg.create_descriptor()
        self.assertIn("i_investigation.txt", out)
        self.assertIn("s_study.txt", out)
        self.assertIn("a_assay.txt", out)
        self.assertIn("Investigation Title	My Simple ISA Investigation", out)
        self.assertIn("Study Protocol Name	sample collection	extraction	sequencing", out)
        self.assertIn("Study Protocol Type	sample collection	material extraction	material sequencing", out)
        self.assertIn("Source Name	Protocol REF	Sample Name", out)
        self.assertIn("source_material	sample collection	sample_material-0", out)
        self.assertIn("Sample Name	Protocol REF	Material Name	Protocol REF", out)
        self.assertIn("sample_material-0	extraction	extract-0	sequencing	sequenced-data-0", out)
