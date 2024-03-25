import unittest
import tempfile
import shutil
import os
import logging


from isatools import isatab
from isatools.net.mw2isa import mw2isa_convert


log = logging.getLogger('isatools')

__author__ = 'proccaserra@gmail.com'


class mw2ISATest(unittest.TestCase):

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_conversion_ms(self):
        success, study_id, validate = mw2isa_convert(studyid="ST000367",
                                                     outputdir=self._tmp_dir,
                                                     dl_option="no",
                                                     validate_option=True)
        if success and validate:
            log.info("conversion successful, invoking the validator for " + study_id)
            with open(os.path.join(self._tmp_dir, study_id, 'i_investigation.txt')) as fp:
                report = isatab.validate(fp)
                # print(report)
                # for error in report['errors']:
                    # print("ERROR:", error)
                    # self.assertEqual(error['code'], 4014)
                    # self.assertIn(error['code'], [4003, 4014])
                self.assertTrue(len(report['errors']) > 0)
        else:
            self.fail("conversion failed, validation was not invoked")

    def test_conversion_nmr(self):
        report = {}
        success, study_id, validate = mw2isa_convert(studyid="ST000102",
                                                     outputdir=self._tmp_dir,
                                                     dl_option="no",
                                                     validate_option=True)
        if success and validate:
            log.info("conversion successful, invoking the validator for " + study_id)
            with open(os.path.join(self._tmp_dir, study_id, 'i_investigation.txt')) as fp:
                report = isatab.validate(fp)
                self.assertEqual(report['errors'][0]['code'], 1007)
        else:
            self.assertFalse(success)

    def test_conversion_invalid_id(self):
        success, study_id, validate = mw2isa_convert(studyid="TOTO",
                                                     outputdir=self._tmp_dir,
                                                     dl_option="no",
                                                     validate_option=True)
        self.assertFalse(success)

    def test_conversion_invalid_dloption(self):

        with self.assertRaises(Exception) as context:
            success, study_id, validate = mw2isa_convert(studyid="ST000102",
                                                         outputdir=self._tmp_dir,
                                                         dl_option="TOTO",
                                                         validate_option=False)
            self.assertFalse(success)
            self.assertTrue('invalid input, option not recognized' in context.exception)
