# coding: utf-8
import unittest
import os
import logging

from isatools import isajson
from tests import utils


class TestIsaJsonSampleData(unittest.TestCase):

    def test_validate_sampledata_bii_i_1_json(self):
        test_case = 'BII-I-1'
        with open(os.path.join(utils.SAMPLE_DATA_DIR, test_case + '.json')) as test_json:
            report = isajson.validate(fp=test_json, log_level=logging.ERROR)
        if report['errors']:
            self.fail("Errors found when validating ISA JSON: {}".format(report['errors']))

    def test_validate_sampledata_bii_s_3_json(self):
        test_case = 'BII-S-3'
        with open(os.path.join(utils.SAMPLE_DATA_DIR, test_case + '.json')) as test_json:
            report = isajson.validate(fp=test_json, log_level=logging.ERROR)
        if report['errors']:
            self.fail("Error found when validating ISA JSON: {}".format(report['errors']))

    def test_validate_sampledata_bii_s_7_json(self):
        test_case = 'BII-S-7'
        with open(os.path.join(utils.SAMPLE_DATA_DIR, test_case + '.json')) as test_json:
            report = isajson.validate(fp=test_json, log_level=logging.ERROR)
        if report['errors']:
            self.fail("Error found when validating ISA JSON: {}".format(report['errors']))
