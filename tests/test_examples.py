import unittest
import sys
from io import StringIO
from tests import utils
import os


class TestSimpleExamples(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_simple_ISAtab_example(self):
        from isatools.examples import createSimpleISAtab
        sys.stdout = StringIO()
        out = createSimpleISAtab.create_descriptor()
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

    def test_validate_ISAtab_example(self):
        from isatools.examples import validateISAtab
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        args = ['validateISAtab.py', os.path.join(utils.TAB_DATA_DIR, 'BII-I-1', 'i_investigation.txt')]
        validateISAtab.main(args)
        sys.stdout = old_stdout
        self.assertIn("Validated 1 ISA-Tab archives, 1 valid ISA-Tab archives, 0 invalid ISA-Tab archives", mystdout.getvalue())
        self.assertIn("Found 0 errors and 45 warnings in across all ISA-Tab archives", mystdout.getvalue())

    def test_validate_ISAjson_example(self):
        from isatools.examples import validateISAjson
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        args = ['validateISAjson.py', os.path.join(utils.JSON_DATA_DIR, 'BII-I-1', 'BII-I-1.json')]
        validateISAjson.main(args)
        sys.stdout = old_stdout
        self.assertIn("Validated 1 ISA-JSONs, 1 valid ISA-JSONs, 0 invalid ISA-JSONs", mystdout.getvalue())
        self.assertIn("Found 0 errors and 187 warnings in across all ISA-JSONs", mystdout.getvalue())