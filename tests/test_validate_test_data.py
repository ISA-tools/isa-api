import unittest
import os
from isatools import isajson, isatab
from isatools.tests import utils
import logging


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestIsaJsonTestData(unittest.TestCase):

    def setUp(self):
        self._reporting_level = logging.ERROR

    def test_validate_testdata_bii_i_1_json(self):
        test_case = 'BII-I-1'
        with open(os.path.join(utils.JSON_DATA_DIR, test_case, test_case + '.json')) as test_case_fp:
            report = isajson.validate(fp=test_case_fp, log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA JSON: {}".format(report['errors']))

    def test_validate_testdata_bii_s_3_json(self):
        test_case = 'BII-S-3'
        with open(os.path.join(utils.JSON_DATA_DIR, test_case, test_case + '.json')) as test_case_fp:
            report = isajson.validate(fp=test_case_fp, log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA JSON: {}".format(report['errors']))

    def test_validate_testdata_bii_s_7_json(self):
        test_case = 'BII-S-7'
        with open(os.path.join(utils.JSON_DATA_DIR, test_case, test_case + '.json')) as test_case_fp:
            report = isajson.validate(fp=test_case_fp, log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA JSON: {}".format(report['errors']))

    def test_validate_testdata_charac_param_factor_json(self):
        test_case = 'TEST-ISA-charac-param-factor'
        with open(os.path.join(utils.JSON_DATA_DIR, test_case + '.json')) as test_case_fp:
            report = isajson.validate(fp=test_case_fp, log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA JSON: {}".format(report['errors']))

    def test_validate_testdata_repeated_measure_json(self):
        test_case = 'TEST-ISA-repeated-measure'
        with open(os.path.join(utils.JSON_DATA_DIR, test_case + '.json')) as test_case_fp:
            report = isajson.validate(fp=test_case_fp, log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA JSON: {}".format(report['errors']))

    def test_validate_testdata_sample_pool_json(self):
        test_case = 'TEST-ISA-sample-pool'
        with open(os.path.join(utils.JSON_DATA_DIR, test_case + '.json')) as test_case_fp:
            report = isajson.validate(fp=test_case_fp, log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA JSON: {}".format(report['errors']))

    def test_validate_testdata_sample_pool_no_protocol_ref_json(self):
        test_case = 'TEST-ISA-sample-pool-no-protocolref'
        with open(os.path.join(utils.JSON_DATA_DIR, test_case + '.json')) as test_case_fp:
            report = isajson.validate(fp=test_case_fp, log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA JSON: {}".format(report['errors']))

    def test_validate_testdata_sample_pool_with_error_json(self):
        test_case = 'TEST-ISA-sample-pool-with-error'
        with open(os.path.join(utils.JSON_DATA_DIR, test_case + '.json')) as test_case_fp:
            report = isajson.validate(fp=test_case_fp, log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA JSON: {}".format(report['errors']))

    def test_validate_testdata_source_split_json(self):
        test_case = 'TEST-ISA-source-split'
        with open(os.path.join(utils.JSON_DATA_DIR, test_case + '.json')) as test_case_fp:
            report = isajson.validate(fp=test_case_fp, log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA JSON: {}".format(report['errors']))

    def test_validate_testdata_source_split_with_error_json(self):
        test_case = 'TEST-ISA-source-split-with-error'
        with open(os.path.join(utils.JSON_DATA_DIR, test_case + '.json')) as test_case_fp:
            report = isajson.validate(fp=test_case_fp, log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA JSON: {}".format(report['errors']))


class TestIsaTabTestData(unittest.TestCase):

    def setUp(self):
        self._reporting_level = logging.ERROR

    def test_validate_testdata_bii_i_1_isatab(self):
        test_case = 'BII-I-1'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_bii_s_3_isatab(self):
        test_case = 'BII-S-3'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_gilbert.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_bii_s_7_isatab(self):
        test_case = 'BII-S-7'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_matteo.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_mtbls1_isatab(self):
        test_case = 'MTBLS1'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt'), encoding='utf-8') as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_mtbls2_isatab(self):
        test_case = 'MTBLS2'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt'), encoding='utf-8') as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_mtbls3_isatab(self):
        test_case = 'MTBLS3'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt'), encoding='utf-8') as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_charac_param_factor_isatab(self):
        test_case = 'TEST-ISA-charac-param-factor'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_repeated_measure_isatab(self):
        test_case = 'TEST-ISA-repeated-measure'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_sample_pool_isatab(self):
        test_case = 'TEST-ISA-sample-pool'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_sample_pool_no_protocol_ref_isatab(self):
        test_case = 'TEST-ISA-sample-pool-no-protocolref'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_sample_pool_with_error_isatab(self):
        test_case = 'TEST-ISA-sample-pool-with-error'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_source_split_isatab(self):
        test_case = 'TEST-ISA-source-split'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_source_split_with_error_isatab(self):
        test_case = 'TEST-ISA-source-split-with-error'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_protocol_chains_sparse_values_isatab(self):
        test_case = 'TEST-ISA-protocol-chains-sparse-values'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_data_transformation_isatab(self):
        test_case = 'TEST-ISA-data-transformation'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_investigation.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))


class TestIsaTabInvalidTestData(unittest.TestCase):

    def setUp(self):
        self._reporting_level = logging.ERROR

    def test_validate_testdata_invalid_data(self):
        test_case = 'i_invalid'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case, 'i_00.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.DEFAULT2015_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) == 0:
                self.fail("No errors found when validating invalid ISA tab: {}".format(
                    os.path.join(utils.TAB_DATA_DIR, test_case, 'i_00.txt')))


class TestIsaTabSraTestData(unittest.TestCase):

    def setUp(self):
        self._reporting_level = logging.ERROR

    def test_validate_testdata_sra_chromatin_mod_seq_isatab(self):
        test_case = 'TEST-ISA-SRA-chromatin-mod-seq'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case,  'i_TEST_SRA_chromatinmod_seq.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.SRA2016_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(len(report['errors'])))

    def test_validate_testdata_sra_env_gene_survey_isatab(self):
        test_case = 'TEST-ISA-SRA-env-gene-survey-seq'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case,  'i_matteo.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.SRA2016_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(len(report['errors'])))

    def test_validate_testdata_sra_exome_seq_isatab(self):
        test_case = 'TEST-ISA-SRA-exome-seq'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case,  'i_TEST_SRA_exome_seq.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.SRA2016_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(len(report['errors'])))

    def test_validate_testdata_sra_genome_seq_isatab(self):
        test_case = 'TEST-ISA-SRA-genome-seq'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case,  'i_TEST_SRA_wgs_seq.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.SRA2016_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(len(report['errors'])))

    def test_validate_testdata_sra_protein_dna_interaction_seq_isatab(self):
        test_case = 'TEST-ISA-SRA-protein-dna-interaction-seq'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case,  'i_TEST_SRA_protein_dna_intact_seq.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.SRA2016_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_sra_protein_rna_interaction_seq_isatab(self):
        test_case = 'TEST-ISA-SRA-protein-rna-interaction-seq'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case,  'i_TEST_SRA_protein_rna_intact_seq.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.SRA2016_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))

    def test_validate_testdata_sra_transcriptome_seq_isatab(self):
        test_case = 'TEST-ISA-SRA-transcriptome-seq'
        with open(os.path.join(utils.TAB_DATA_DIR, test_case,  'i_TEST_SRA_tx_seq.txt')) as test_case_fp:
            report = isatab.validate(fp=test_case_fp,config_dir=utils.SRA2016_XML_CONFIGS_DATA_DIR,
                                     log_level=self._reporting_level)
            if len(report['errors']) > 0:
                self.fail("Error found when validating ISA tab: {}".format(report['errors']))
