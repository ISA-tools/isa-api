import unittest
from isatools import isatab
from mw2isa import mw2isa_convert

__author__ = 'proccaserra@gmail.com'


class ms2ISATest(unittest.TestCase):

    def setUp(self):
        pass

    def test_conversion(self):
        success, study_id, validate = mw2isa_convert(studyid="ST000367", outputdir='output', dl_option="no", validate_option="yes")
        # exit_code = sys.exit()

        if success and validate:
            print("conversion successfull, invoking the validator for " + study_id)
            try:
                isatab.validate2(open('temp/' + study_id + '/i_investigation.txt'), './isaconfig-default_v2015-07-02/')
            except:
                print("conversion successful but validation failed")
        else:
            print("conversion failed, validation was not invoked")