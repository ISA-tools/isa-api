import unittest
from isatools import isatab
from isatools.convert.mw2isa import mw2isa_convert

__author__ = 'proccaserra@gmail.com'


class mw2ISATest(unittest.TestCase):

    def setUp(self):
        pass

    def test_conversion(self):
        success, study_id, validate = mw2isa_convert(studyid="ST000406", dl_option="no", validate_option="yes")
        # exit_code = sys.exit()

        if success and validate:
            print("conversion successful, invoking the validator for " + study_id)
            with open('temp/' + study_id + '/i_investigation.txt') as fp:
                report = isatab.validate2(fp)
                if len(report['errors']) > 0:
                    self.fail("conversion successful but validation failed")
        else:
            self.fail("conversion failed, validation was not invoked")