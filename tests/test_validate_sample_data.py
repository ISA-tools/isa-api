import unittest
import os
from isatools import isajson
from tests import utils
import logging


class TestIsaJsonSampleData(unittest.TestCase):

    def test_validate_sampledata_bii_i_1_json(self):
        test_case = 'BII-I-1'
        report = isajson.validate(fp=open(os.path.join(utils.SAMPLE_DATA_DIR, test_case + '.json')),
                                  log_level=logging.ERROR)
        if len(report['errors']) > 0:
            self.fail("Errors found when validating ISA JSON: {}".format(report['errors']))

    def test_validate_sampledata_bii_s_3_json(self):
        test_case = 'BII-S-3'
        report = isajson.validate(fp=open(os.path.join(utils.SAMPLE_DATA_DIR, test_case + '.json')),
                                  log_level=logging.ERROR)
        if len(report['errors']) > 0:
            self.fail("Error found when validating ISA JSON: {}".format(report['errors']))

    def test_validate_sampledata_bii_s_7_json(self):
        test_case = 'BII-S-7'
        report = isajson.validate(fp=open(os.path.join(utils.SAMPLE_DATA_DIR, test_case + '.json')),
                                  log_level=logging.ERROR)
        if len(report['errors']) > 0:
            self.fail("Error found when validating ISA JSON: {}".format(report['errors']))