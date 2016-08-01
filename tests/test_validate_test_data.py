import unittest
import os
from isatools import isajson, isatab
from tests import utils
import logging


class TestIsaJsonTestData(unittest.TestCase):

    def setUp(self):
        self._reporting_level = logging.ERROR

    def test_validate_testdata_bii_i_1_json(self):
        test_case = 'BII-I-1'
        log_msg_stream = isajson.validate(fp=open(os.path.join(utils.JSON_DATA_DIR, test_case, test_case + '.json')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA JSON: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_bii_s_3_json(self):
        test_case = 'BII-S-3'
        log_msg_stream = isajson.validate(fp=open(os.path.join(utils.JSON_DATA_DIR, test_case, test_case + '.json')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA JSON: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_bii_s_7_json(self):
        test_case = 'BII-S-7'
        log_msg_stream = isajson.validate(fp=open(os.path.join(utils.JSON_DATA_DIR, test_case, test_case + '.json')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA JSON: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_charac_param_factor_json(self):
        test_case = 'TEST-ISA-charac-param-factor'
        log_msg_stream = isajson.validate(fp=open(os.path.join(utils.JSON_DATA_DIR, test_case + '.json')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA JSON: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_repeated_measure_json(self):
        test_case = 'TEST-ISA-repeated-measure'
        log_msg_stream = isajson.validate(fp=open(os.path.join(utils.JSON_DATA_DIR, test_case + '.json')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA JSON: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_sample_pool_json(self):
        test_case = 'TEST-ISA-sample-pool'
        log_msg_stream = isajson.validate(fp=open(os.path.join(utils.JSON_DATA_DIR, test_case + '.json')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA JSON: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_sample_pool_no_protocol_ref_json(self):
        test_case = 'TEST-ISA-sample-pool-no-protocolref'
        log_msg_stream = isajson.validate(fp=open(os.path.join(utils.JSON_DATA_DIR, test_case + '.json')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA JSON: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_sample_pool_with_error_json(self):
        test_case = 'TEST-ISA-sample-pool-with-error'
        log_msg_stream = isajson.validate(fp=open(os.path.join(utils.JSON_DATA_DIR, test_case + '.json')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA JSON: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_source_split_json(self):
        test_case = 'TEST-ISA-source-split'
        log_msg_stream = isajson.validate(fp=open(os.path.join(utils.JSON_DATA_DIR, test_case + '.json')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA JSON: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_source_split_with_error_json(self):
        test_case = 'TEST-ISA-source-split-with-error'
        log_msg_stream = isajson.validate(fp=open(os.path.join(utils.JSON_DATA_DIR, test_case + '.json')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA JSON: {}".format(log_msg_stream.getvalue()))


class TestIsaTabTestData(unittest.TestCase):

    def setUp(self):
        self._reporting_level = logging.ERROR

    def test_validate_testdata_bii_i_1_isatab(self):
        test_case = 'BII-I-1'
        log_msg_stream = isatab.validate2(fp=open(os.path.join(utils.TAB_DATA_DIR, test_case,
                                                               'i_investigation.txt')), log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA tab: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_bii_s_3_isatab(self):
        test_case = 'BII-S-3'
        log_msg_stream = isatab.validate2(fp=open(os.path.join(utils.TAB_DATA_DIR, test_case,
                                                               'i_gilbert.txt')), log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA tab: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_bii_s_7_isatab(self):
        test_case = 'BII-S-7'
        log_msg_stream = isatab.validate2(fp=open(os.path.join(utils.TAB_DATA_DIR, test_case,
                                                               'i_matteo.txt')), log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA tab: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_mtbls1_isatab(self):
        test_case = 'MTBLS1'
        log_msg_stream = isatab.validate2(fp=open(os.path.join(utils.TAB_DATA_DIR, test_case,
                                                               'i_investigation.txt')), log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA tab: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_mtbls2_isatab(self):
        test_case = 'MTBLS2'
        log_msg_stream = isatab.validate2(fp=open(os.path.join(utils.TAB_DATA_DIR, test_case,
                                                               'i_investigation.txt')), log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA tab: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_mtbls3_isatab(self):
        test_case = 'MTBLS3'
        log_msg_stream = isatab.validate2(fp=open(os.path.join(utils.TAB_DATA_DIR, test_case,
                                                               'i_investigation.txt')), log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA tab: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_charac_param_factor_isatab(self):
        test_case = 'TEST-ISA-charac-param-factor'
        log_msg_stream = isatab.validate2(fp=open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA tab: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_repeated_measure_isatab(self):
        test_case = 'TEST-ISA-repeated-measure'
        log_msg_stream = isatab.validate2(fp=open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA tab: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_sample_pool_isatab(self):
        test_case = 'TEST-ISA-sample-pool'
        log_msg_stream = isatab.validate2(fp=open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA tab: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_sample_pool_no_protocol_ref_isatab(self):
        test_case = 'TEST-ISA-sample-pool-no-protocolref'
        log_msg_stream = isatab.validate2(fp=open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA tab: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_sample_pool_with_error_isatab(self):
        test_case = 'TEST-ISA-sample-pool-with-error'
        log_msg_stream = isatab.validate2(fp=open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA tab: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_source_split_isatab(self):
        test_case = 'TEST-ISA-source-split'
        log_msg_stream = isatab.validate2(fp=open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA tab: {}".format(log_msg_stream.getvalue()))

    def test_validate_testdata_source_split_with_error_isatab(self):
        test_case = 'TEST-ISA-source-split-with-error'
        log_msg_stream = isatab.validate2(fp=open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')),
                                          log_level=self._reporting_level)
        if '(E)' in log_msg_stream.getvalue():
            self.fail("Error found when validating ISA tab: {}".format(log_msg_stream.getvalue()))
