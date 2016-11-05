import unittest
from isatools import isajson, isatab
import os
from tests import utils
import tempfile
import shutil


class TestValidateIsaJson(unittest.TestCase):

    def setUp(self):
        self._unit_json_data_dir = utils.UNIT_JSON_DATA_DIR
        self._configs_json_data_dir = utils.JSON_DEFAULT_CONFIGS_DATA_DIR

    def tearDown(self):
        pass

    def test_validate_isajson_json_load(self):
        """Tests against 0002"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'minimal_syntax.json')))
        if 2 in [e['code'] for e in errors['errors']]:
            self.fail("Error raised when trying to parse JSON, when it should have been fine!")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'invalid.json')))
        if 2 not in [e['code'] for e in errors['errors']]:
            self.fail("NO error raised when trying to parse invalid formed JSON!")

    def test_validate_isajson_isajson_schemas(self):
        """Tests against 0003"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'minimal_syntax.json')))
        if 3 in [e['code'] for e in errors['errors']]:
            self.fail("Error raised when trying to parse valid ISA-JSON, when it should have been fine!")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'invalid_isajson.json')))
        if 3 not in [e['code'] for e in errors['errors']]:
            self.fail("NO error raised when validating against some non-ISA-JSON conforming JSON!")

    def test_validate_isajson_utf8_encoding_check(self):
        """Tests against 0010"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'minimal_syntax.json')))
        if 10 in [e['code'] for e in errors['errors']]:
            self.fail("Validation warning present when testing against UTF-8 encoded file")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'non_utf8.json')))
        if 10 not in [e['code'] for e in errors['errors']]:
            self.fail("Validation warning missing when testing against UTF-16 encoded file (UTF-8 required)")

    def test_validate_isajson_source_link(self):
        """Tests against 1002, but reports 1005 error (more general case)"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'source_link.json')))
        if 1005 in [e['code'] for e in errors['errors']]:
            self.fail("Validation error present when should pass without error - source link reports broken when "
                      "present in data")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'source_link_fail.json')))
        if 1005 not in [e['code'] for e in errors['errors']]:
            self.fail("Validation error missing when should report error - data has broken source link but not "
                      "reported in validation report")

    def test_validate_isajson_sample_link(self):
        """Tests against 1003 but reports 1005 error (more general case)"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'sample_link.json')))
        if 1005 in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error present when should pass without error - sample link reports broken when present in "
                "data")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'sample_link_fail.json')))
        if 1005 not in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error missing when should report error - data has broken sample link but not reported in "
                "validation report")

    def test_validate_isajson_data_file_link(self):
        """Tests against 1004 but reports 1005 error (more general case)"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'datafile_link.json')))
        if 1005 in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error present when should pass without error - data file link reports broken when present "
                "in data")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'datafile_link_fail.json')))
        if 1005 not in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error missing when should report error - data has broken data file link but not reported "
                "in validation report")

    def test_validate_isajson_material_link(self):
        """Tests against 1005"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'material_link.json')))
        if 1005 in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error present when should pass without error -material link link reports broken when "
                "present in data")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'material_link_fail.json')))
        if 1005 not in [e['code'] for e in errors['errors']]:
            self.fail("Validation error missing when should report error - data has broken material link but not "
                      "reported in validation report")

    def test_validate_isajson_process_link(self):
        """Tests against 1006"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'process_link.json')))
        if 1006 in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error present when should pass without error - process link reports broken when present "
                "in data")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'process_link_fail.json')))
        if 1006 not in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error missing when should report error - data has broken process link but not reported in "
                "validation report")

    def test_validate_isajson_protocol_ref_link(self):
        """Tests against 1007"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'protocol_ref_link.json')))
        if 1007 in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error present when should pass without error - executesProtocol link reports broken when "
                "present in data")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'protocol_ref_link_fail.json')))
        if 1007 not in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error missing when should report error - data has broken executesProtocol link but not "
                "reported in validation report")

    def test_validate_isajson_factor_link(self):
        """Tests against 1008"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'factor_link.json')))
        if 1008 in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error present when should pass without error - factor link in factorValue reports broken "
                "when present in data")

        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'factor_link_fail.json')))
        if 1008 not in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error missing when should report error - data has broken factor link in factorValue but "
                "not reported in validation report")

    def test_validate_isajson_protocol_parameter_link(self):
        """Tests against 1009"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'protocol_parameter_link.json')))
        if 1009 in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error present when should pass without error - parameter link in parameterValue reports "
                "broken when present in data")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'protocol_parameter_link_fail.json')))
        if 1009 not in [e['code'] for e in errors['errors']]:
            self.fail("Validation error missing when should report error - data has broken parameter link in "
                      "parameterValue but not reported in validation report")

    def test_validate_isajson_iso8601(self):
        """Tests against 3001"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'iso8601.json')))
        if 3001 in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error present when should pass without error - incorrectly formatted ISO8601 date in "
                "publicReleaseDate reports invalid when valid data")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'iso8601_fail.json')))
        if 3001 not in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error missing when should report error - data has incorrectly formatted ISO8601 date in "
                "publicReleaseDate but not reported in validation report")

    def test_validate_isajson_doi(self):
        """Tests against 3002"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'doi.json')))
        if 3002 in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error present when should pass without error - incorrectly formatted DOI in publication "
                "reports invalid when valid data")

        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'doi_fail.json')))
        if 3002 not in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error missing when should report error - data has incorrectly formatted DOI in publication "
                "but not reported in validation report")

    def test_validate_isajson_pubmed(self):
        """Tests against 3003"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'pubmed.json')))
        if 3003 in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error present when should pass without error - incorrectly formatted Pubmed ID in "
                "publication reports invalid when valid data")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'pubmed_fail.json')))
        if 3003 not in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error missing when should report error - data has incorrectly formatted Pubmed ID in "
                "publication but not reported in validation report")

    def test_validate_isajson_protocol_used(self):
        """Tests against 1019"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'protocol_used.json')))
        if 1019 in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error present when should pass without error - incorrectly reports #protocol/1 not used "
                "when it has been used in #process/1")

        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'protocol_used_fail.json')))
        if 1019 not in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error missing when should report error - data has incorrectly reported everything is OK "
                "but not reported #protocol/1 as being unused")

    def test_validate_isajson_factor_used(self):
        """Tests against 1021"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'factor_used.json')))
        if 1021 in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error present when should pass without error - incorrectly reports #factor/1 not used when "
                "it has been used in #sample/1")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'factor_used_fail.json')))
        if 1021 not in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error missing when should report error - data has incorrectly reported everything is OK "
                "but not reported #factor/1 as being unused")

    def test_validate_isajson_term_source_used(self):
        """Tests against 3007"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'term_source_used.json')))
        if 3007 in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error present when should pass without error - incorrectly reports PATO not used when it "
                "has been used in #factor/1")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'term_source_used_fail.json')))
        if 3007 not in [e['code'] for e in errors['errors']]:
            self.fail(
                "Validation error missing when should report error - data has incorrectly reported everything is OK "
                "but not reported PATO as being unused")

    def test_validate_isajson_load_config(self):
        """Tests against 4001"""
        try:
            isajson.load_config(os.path.join(self._configs_json_data_dir))
        except IOError as e:
            self.fail("Could not load config because... " + str(e))

    def test_validate_isajson_get_config(self):
        """Tests against 4002"""
        try:
            configs = isajson.load_config(os.path.join(self._configs_json_data_dir))
            if configs is None:
                self.fail("There was a problem and config is null")
            else:
                self.assertIsNotNone(configs[('metagenome sequencing', 'nucleotide sequencing')])
        except IOError as e:
            self.fail("Could not load config because... " + str(e))

    def test_validate_isajson_study_config_validation(self):
        """Tests against 4004"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'study_config.json')))
        if 4004 in [e['code'] for e in errors['errors']]:
            self.fail("Validation failed against default study configuration, when it should have passed")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'study_config_fail.json')))
        if 4004 not in [e['code'] for e in errors['errors']]:
            self.fail("Validation passed against default study configuration, when it should have failed")

    def test_validate_isajson_assay_config_validation(self):
        """Tests against 4004"""
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'assay_config.json')))
        if 4004 in [e['code'] for e in errors['errors']]:
            self.fail("Validation failed against transcription_seq.json configuration, when it should have passed")
        errors = isajson.validate(open(os.path.join(self._unit_json_data_dir, 'assay_config_fail.json')))
        if 4004 not in [e['code'] for e in errors['errors']]:
            self.fail("Validation passed against transcription_seq.json configuration, when it should have failed")


class TestValidateIsaTab(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR

    def tearDown(self):
        pass

    def test_validate_isatab_bii_i_1(self):
        log_msg_stream = isatab.validate2(open(os.path.join(self._tab_data_dir, 'BII-I-1', 'i_investigation.txt')))
        log = log_msg_stream.getvalue()
        if "Finished validation..." not in log:
            self.fail("Validation did not complete successfully when it should have!")
        if '(W)' not in log:
            self.fail("Validation error and warnings are missing when should report some with BII-I-1")

    def test_validate_isatab_bii_s_3(self):
        log_msg_stream = isatab.validate2(open(os.path.join(self._tab_data_dir, 'BII-S-3', 'i_gilbert.txt')))
        log = log_msg_stream.getvalue()
        if "Finished validation..." not in log:
            self.fail("Validation did not complete successfully when it should have!")
        elif '(W)' not in log:
            self.fail("Validation error and warnings are missing when should report some with BII-S-3")

    def test_validate_isatab_bii_s_7(self):
        log_msg_stream = isatab.validate2(open(os.path.join(self._tab_data_dir, 'BII-S-7', 'i_matteo.txt')))
        log = log_msg_stream.getvalue()
        if "Finished validation..." not in log:
            self.fail("Validation did not complete successfully when it should have!")
        elif '(W)' not in log:
            self.fail("Validation error and warnings are missing when should report some with BII-S-7")


class TestBatchValidateIsaTab(unittest.TestCase):

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._bii_tab_dir_list = [
            os.path.join(self._tab_data_dir, 'BII-I-1'),
            os.path.join(self._tab_data_dir, 'BII-S-3'),
            os.path.join(self._tab_data_dir, 'BII-S-7')
        ]

    def tearDown(self):
        shutil.rmtree(os.path.join(self._tmp_dir))

    def test_batch_validate_bii(self):
        isatab.batch_validate(self._bii_tab_dir_list, os.path.join(self._tmp_dir, 'isatab_report.txt'))
        self.assertTrue(os.path.isfile(os.path.join(self._tmp_dir, 'isatab_report.txt')))


class TestBatchValidateIsaJson(unittest.TestCase):

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()
        self._json_dir = utils.JSON_DATA_DIR
        self._bii_json_files = [
            os.path.join(self._json_dir, 'BII-I-1', 'BII-I-1.json'),
            os.path.join(self._json_dir, 'BII-S-3', 'BII-S-3.json'),
            os.path.join(self._json_dir, 'BII-S-7', 'BII-S-7.json')
        ]

    def tearDown(self):
        shutil.rmtree(os.path.join(self._tmp_dir))

    def test_batch_validate_bii(self):
        batch_report = isajson.batch_validate(self._bii_json_files)
        self.assertListEqual([f['filename'] for f in batch_report['batch_report']], self._bii_json_files)
