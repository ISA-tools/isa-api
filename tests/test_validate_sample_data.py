import unittest
import os
from isatools import isajson
from tests import utils
import logging


class TestIsaJsonSampleData(unittest.TestCase):

    def test_validate_sampledata_bii_i_1_json(self):
        test_case = 'BII-I-1'
        log_msg_stream = isajson.validate(fp=open(os.path.join(utils.SAMPLE_DATA_DIR, test_case + '.json')),
                                          log_level=logging.ERROR)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA JSON: {}".format(log_msg_stream.getvalue()))

    def test_validate_sampledata_bii_s_3_json(self):
        test_case = 'BII-S-3'
        log_msg_stream = isajson.validate(fp=open(os.path.join(utils.SAMPLE_DATA_DIR, test_case + '.json')),
                                          log_level=logging.ERROR)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA JSON: {}".format(log_msg_stream.getvalue()))

    def test_validate_sampledata_bii_s_7_json(self):
        test_case = 'BII-S-7'
        log_msg_stream = isajson.validate(fp=open(os.path.join(utils.SAMPLE_DATA_DIR, test_case + '.json')),
                                          log_level=logging.ERROR)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA JSON: {}".format(log_msg_stream.getvalue()))