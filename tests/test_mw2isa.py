import unittest
from isatools import isatab
from isatools.convert.mw2isa import mw2isa_convert
import tempfile
import shutil
import os

__author__ = 'proccaserra@gmail.com'


class mw2ISATest(unittest.TestCase):

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_conversion(self):
        success, study_id, validate = mw2isa_convert(studyid="ST000367", outputdir=self._tmp_dir, dl_option="no",
                                                     validate_option="yes")
        # exit_code = sys.exit()

        if success and validate:
            print("conversion successful, invoking the validator for " + study_id)
            with open(os.path.join(self._tmp_dir, study_id, 'i_investigation.txt')) as fp:
                report = isatab.validate(fp)
                if len(report['errors']) > 0:
                    self.fail("conversion successful but validation failed")
        else:
            self.fail("conversion failed, validation was not invoked")