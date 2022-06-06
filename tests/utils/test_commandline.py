import unittest
from contextlib import contextmanager
from io import StringIO
import sys


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class TestCommandLineIsaTools(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_command_version(self):
        from isatools.__main__ import main
        with captured_output() as (out, err):
            with self.assertRaises(SystemExit):
                main(argv=["--version"])
                output = out.getvalue().strip()
                self.assertEqual(output, "isatools 0.7")

    def test_command_help(self):
        from isatools.__main__ import main
        with captured_output() as (out, err):
            with self.assertRaises(SystemExit):
                main(argv=["--version"])
                output = out.getvalue().strip()
                self.assertEqual(output, """usage: isatools -c COMMAND [options]

Create, convert, and manipulate ISA-formatted metadata

optional arguments:
  -h, --help            show this help message and exit
  -c {isatab2json,json2isatab,sampletab2isatab,sampletab2json}
                        isatools API command to run
  -i IN_PATH            in (files or directory will be read from here)
  -o OUT_PATH           out (file will be written out here or written to
                        directory if ISA-Tab archive out)
  --version             show program's version number and exit
  -v                    show more output""")
