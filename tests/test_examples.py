import unittest
import sys
import six
from tests import utils
import os


class TestSimpleExamples(unittest.TestCase):

    def test_create_simple_ISAtab_example(self):
        from isatools.examples import createSimpleISAtab
        sys.stdout = six.StringIO()
        out = createSimpleISAtab.create_descriptor()
        self.assertIn("i_investigation.txt", out)
        self.assertIn("s_study.txt", out)
        self.assertIn("a_assay.txt", out)
        self.assertIn("Investigation Title	My Simple ISA Investigation", out)
        self.assertIn("Study Protocol Name	sample collection	extraction	sequencing", out)
        self.assertIn("Study Protocol Type	sample collection	material extraction	material sequencing", out)
        self.assertIn("Source Name	Protocol REF	Sample Name", out)
        self.assertIn("source_material	sample collection	sample_material-0", out)
        self.assertIn("Sample Name	Protocol REF	Extract Name	Protocol REF", out)
        self.assertIn("sample_material-0	extraction	extract-0	sequencing	sequenced-data-0", out)

    def test_validate_ISAtab_example_wrong_args(self):
        from isatools.examples import validateISAtab
        with self.assertRaises(SystemExit) as cm:
            validateISAtab.main([])
            self.assertEqual(cm.exception.code, 1)

    def test_validate_ISAtab_example_skip_file(self):
        from isatools.examples import validateISAtab
        old_stdout = sys.stdout
        sys.stdout = mystdout = six.StringIO()
        args = ['validateISAtab.py', os.path.join(utils.TAB_DATA_DIR, 'BII-I-1', 'i_investigation.tx')]
        validateISAtab.main(args)
        sys.stdout = old_stdout
        self.assertIn("Validated 0 ISA-Tab archives, 0 valid ISA-Tab archives, 0 invalid ISA-Tab archives",
                      mystdout.getvalue())

    def test_validate_ISAtab_example_invalid(self):
        from isatools.examples import validateISAtab
        with self.assertRaises(SystemExit):
            old_stdout = sys.stdout
            sys.stdout = mystdout = six.StringIO()
            args = ['validateISAtab.py', os.path.join(utils.TAB_DATA_DIR, 'i_invalid', 'i_01.txt')]
            validateISAtab.main(args)
            sys.stdout = old_stdout
            self.assertIn("Validated 1 ISA-Tab archives, 0 valid ISA-Tab archives, 1 invalid ISA-Tab archives",
                          mystdout.getvalue())

    def test_validate_ISAtab_example(self):
        from isatools.examples import validateISAtab
        old_stdout = sys.stdout
        sys.stdout = mystdout = six.StringIO()
        args = ['validateISAtab.py', os.path.join(utils.TAB_DATA_DIR, 'BII-I-1', 'i_investigation.txt')]
        validateISAtab.main(args)
        sys.stdout = old_stdout
        self.assertIn("Validated 1 ISA-Tab archives, 1 valid ISA-Tab archives, 0 invalid ISA-Tab archives", mystdout.getvalue())
        self.assertIn("Found 0 errors and 45 warnings in across all ISA-Tab archives", mystdout.getvalue())

    def test_validate_ISAjson_example_wrong_args(self):
        from isatools.examples import validateISAjson
        with self.assertRaises(SystemExit) as cm:
            validateISAjson.main([])
            self.assertEqual(cm.exception.code, 1)

    def test_validate_ISAjson_example_skip_file(self):
        from isatools.examples import validateISAjson
        old_stdout = sys.stdout
        sys.stdout = mystdout = six.StringIO()
        args = ['validateISAjson.py', os.path.join(utils.JSON_DATA_DIR, 'BII-I-1', 'BII-I-1.jso')]
        validateISAjson.main(args)
        sys.stdout = old_stdout
        self.assertIn("Validated 0 ISA-JSONs, 0 valid ISA-JSONs, 0 invalid ISA-JSONs", mystdout.getvalue())

    def test_validate_ISAjson_example_invalid(self):
        from isatools.examples import validateISAjson
        with self.assertRaises(SystemExit):
            old_stdout = sys.stdout
            sys.stdout = mystdout = six.StringIO()
            args = ['validateISAjson.py', os.path.join(utils.JSON_DATA_DIR, 'unit', 'invalid_isajson.json')]
            validateISAjson.main(args)
            sys.stdout = old_stdout
            self.assertIn("Validated 1 ISA-JSONs, 0 valid ISA-JSONs, 1 invalid ISA-JSONs", mystdout.getvalue())

    def test_validate_ISAjson_example(self):
        from isatools.examples import validateISAjson
        old_stdout = sys.stdout
        sys.stdout = mystdout = six.StringIO()
        args = ['validateISAjson.py', os.path.join(utils.JSON_DATA_DIR, 'BII-I-1', 'BII-I-1.json')]
        validateISAjson.main(args)
        sys.stdout = old_stdout
        self.assertIn("Validated 1 ISA-JSONs, 1 valid ISA-JSONs, 0 invalid ISA-JSONs", mystdout.getvalue())
        #self.assertIn("Found 0 errors and 187 warnings in across all ISA-JSONs", mystdout.getvalue())
        self.assertIn("Found 0 errors and 25 warnings in across all ISA-JSONs", mystdout.getvalue())

