# coding: utf-8
import unittest
import os
import re
import logging
import functools
import six

from isatools import isajson, isatab
from tests import utils

# This will remove the "'U' flag is deprecated" DeprecationWarning in Python3
open = functools.partial(open, mode='r') if six.PY3 else functools.partial(open, mode='rU')


class TestValidateIsaJson(unittest.TestCase):

    def setUp(self):
        self._unit_json_data_dir = utils.UNIT_JSON_DATA_DIR
        self._configs_json_data_dir = utils.JSON_DEFAULT_CONFIGS_DATA_DIR

    def tearDown(self):
        pass

    def test_validate_isajson_json_load(self):
        """Tests against 0001"""
        with open(os.path.join(self._unit_json_data_dir, 'minimal_syntax.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "There was an error when trying to parse the JSON" in log_msg_stream.getvalue():
            self.fail("Error raised when trying to parse JSON, when it should have been fine!")
        with open(os.path.join(self._unit_json_data_dir, 'invalid.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "There was an error when trying to parse the JSON" not in log_msg_stream.getvalue():
            self.fail("NO error raised when trying to parse invalid formed JSON!")

    def test_validate_isajson_isajson_schemas(self):
        """Tests against 0002"""
        with open(os.path.join(self._unit_json_data_dir, 'minimal_syntax.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "The JSON does not validate against the provided ISA-JSON schemas!" in log_msg_stream.getvalue():
            self.fail("Error raised when trying to parse valid ISA-JSON, when it should have been fine!")
        with open(os.path.join(self._unit_json_data_dir, 'invalid_isajson.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "The JSON does not validate against the provided ISA-JSON schemas!" not in log_msg_stream.getvalue():
            self.fail("NO error raised when validating against some non-ISA-JSON conforming JSON!")

    def test_validate_isajson_utf8_encoding_check(self):
        """Tests against 0010"""
        with open(os.path.join(self._unit_json_data_dir, 'minimal_syntax.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "File should be UTF-8 encoding" in log_msg_stream.getvalue():
            self.fail("Validation warning present when testing against UTF-8 encoded file")
        with open(os.path.join(self._unit_json_data_dir, 'non_utf8.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "File should be UTF-8 encoding" not in log_msg_stream.getvalue():
            self.fail("Validation warning missing when testing against UTF-16 encoded file (UTF-8 required)")

    def test_validate_isajson_source_link(self):
        """Tests against 1002"""
        err = re.compile("\[u?'#source/1'\] not found")
        with open(os.path.join(self._unit_json_data_dir, 'source_link.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is not None:#"['#source/1'] not found" in log_msg_stream.getvalue():
            self.fail("Validation error present when should pass without error - source link reports broken when "
                      "present in data")
        with open(os.path.join(self._unit_json_data_dir, 'source_link_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is None:#"['#source/1'] not found" not in log_msg_stream.getvalue():
            self.fail("Validation error missing when should report error - data has broken source link but not "
                      "reported in validation report")

    def test_validate_isajson_sample_link(self):
        """Tests against 1003"""
        err = re.compile("\[u?'#sample/1'\] not found")
        with open(os.path.join(self._unit_json_data_dir, 'sample_link.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is not None: #"['#sample/1'] not found" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - sample link reports broken when present in "
                "data")
        with open(os.path.join(self._unit_json_data_dir, 'sample_link_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is None: #"['#sample/1'] not found" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken sample link but not reported in "
                "validation report")

    def test_validate_isajson_data_file_link(self):
        """Tests against 1004"""
        err = re.compile("\[u?'#data/a_file.dat'\] not found")
        with open(os.path.join(self._unit_json_data_dir, 'datafile_link.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is not None:#"[u'#data/a_file.dat'] not found" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - data file link reports broken when present "
                "in data")
        with open(os.path.join(self._unit_json_data_dir, 'datafile_link_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is None:#"[u'#data/a_file.dat'] not found" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken data file link but not reported "
                "in validation report")

    def test_validate_isajson_material_link(self):
        """Tests against 1005"""
        err = re.compile("\[u?'#material/1'\] not found")
        with open(os.path.join(self._unit_json_data_dir, 'material_link.json')) as json_file
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is not None:#"['#material/1'] not found" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error -materiallink link reports broken when "
                "present in data")
        with open(os.path.join(self._unit_json_data_dir, 'material_link_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is None:#"['#material/1'] not found" not in log_msg_stream.getvalue():
            self.fail(
        "Validation error missing when should report error - data has broken material link but not reported in "
        "validation report")

    def test_validate_isajson_process_link(self):
        """Tests against 1006"""
        with open(os.path.join(self._unit_json_data_dir, 'process_link.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "link #process/1 in process #process/2 does not refer to another process" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - process link reports broken when present "
                "in data")
        with open(os.path.join(self._unit_json_data_dir, 'process_link_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "link #process/1 in process #process/2 does not refer to another process" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken process link but not reported in "
                "validation report")

    def test_validate_isajson_protocol_ref_link(self):
        """Tests against 1007"""
        err = re.compile("\[u?'#protocol/1'\] used in a study or assay process sequence not declared")
        with open(os.path.join(self._unit_json_data_dir, 'protocol_ref_link.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is not None:#"['#protocol/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - executesProtocol link reports broken when "
                "present in data")
        with open(os.path.join(self._unit_json_data_dir, 'protocol_ref_link_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is None:#"['#protocol/1'] used in a study or assay process sequence not declared" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken executesProtocol link but not "
                "reported in validation report")

    def test_validate_isajson_factor_link(self):
        """Tests against 1008"""
        with open(os.path.join(self._unit_json_data_dir, 'factor_link.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "['#factor/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - factor link in factorValue reports broken "
                "when present in data")
        with open(os.path.join(self._unit_json_data_dir, 'factor_link_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "['#factor/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken factor link in factorValue but "
                "not reported in validation report")

    def test_validate_isajson_protocol_parameter_link(self):
        """Tests against 1009"""
        with open(os.path.join(self._unit_json_data_dir, 'protocol_parameter_link.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "['#parameter/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - parameter link in parameterValue reports "
                "broken when present in data")
        with open(os.path.join(self._unit_json_data_dir, 'protocol_parameter_link_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "['#parameter/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken parameter link in parameterValue "
                "but not reported in validation report")

    def test_validate_isajson_iso8601(self):
        """Tests against 3001"""
        with open(os.path.join(self._unit_json_data_dir, 'iso8601.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "does not conform to ISO8601 format" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - incorrectly formatted ISO8601 date in "
                "publicReleaseDate reports invalid when valid data")
        with open(os.path.join(self._unit_json_data_dir, 'iso8601_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "does not conform to ISO8601 format" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has incorrectly formatted ISO8601 date in "
                "publicReleaseDate but not reported in validation report")

    def test_validate_isajson_doi(self):
        """Tests against 3002"""
        with open(os.path.join(self._unit_json_data_dir, 'doi.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "does not conform to DOI format" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - incorrectly formatted DOI in publication "
                "reports invalid when valid data")
        with open(os.path.join(self._unit_json_data_dir, 'doi_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "does not conform to DOI format" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has incorrectly formatted DOI in publication "
                "but not reported in validation report")

    def test_validate_isajson_pubmed(self):
        """Tests against 3003"""
        with open(os.path.join(self._unit_json_data_dir, 'pubmed.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "is not valid format" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - incorrectly formatted Pubmed ID in "
                "publication reports invalid when valid data")
        with open(os.path.join(self._unit_json_data_dir, 'pubmed_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if "is not valid format" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has incorrectly formatted Pubmed ID in "
                "publication but not reported in validation report")

    def test_validate_isajson_protocol_used(self):
        """Tests against 3005"""
        err = re.compile("\[u?'#protocol/1'\] not used")
        with open(os.path.join(self._unit_json_data_dir, 'protocol_used.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is not None:#"['#protocol/1'] not used" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - incorrectly reports #protocol/1 not used "
                "when it has been used in #process/1")
        with open(os.path.join(self._unit_json_data_dir, 'protocol_used_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is None:#"['#protocol/1'] not used" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has incorrectly reported everything is OK "
                "but not reported #protocol/1 as being unused")

    def test_validate_isajson_factor_used(self):
        """Tests against 3006"""
        err = re.compile("factors declared \[u?'#factor/1'\] that have not been used")
        with open(os.path.join(self._unit_json_data_dir, 'factor_used.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is not None:#"factors declared ['#factor/1'] that have not been used" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - incorrectly reports #factor/1 not used when "
                "it has been used in #sample/1")
        with open(os.path.join(self._unit_json_data_dir, 'factor_used_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is None:#"factors declared ['#factor/1'] that have not been used" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has incorrectly reported everything is OK "
                "but not reported #factor/1 as being unused")

    def test_validate_isajson_term_source_used(self):
        """Tests against 3007"""
        err = re.compile("ontology sources declared [\[a-zA-Z\' ,\]]* that have not been used")
        with open(os.path.join(self._unit_json_data_dir, 'term_source_used.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is not None:
            self.fail(
                "Validation error present when should pass without error - incorrectly reports PATO not used when it "
                "has been used in #factor/1")
        with open(os.path.join(self._unit_json_data_dir, 'term_source_used_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is None:
            self.fail(
                "Validation error missing when should report error - data has incorrectly reported everything is OK "
                "but not reported PATO as being unused")

    def test_validate_isajson_load_config(self):
        """Tests against 4001"""
        try:
            isajson.load_config(self._configs_json_data_dir)#os.path.join(self._configs_json_data_dir))
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
        err = re.compile("Configuration protocol sequence [\[a-zA-Z' ,\]]* does not match study graph found in [\[a-zA-Z' ,\]]*")
        with open(os.path.join(self._unit_json_data_dir, 'study_config.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is not None:
            self.fail("Validation failed against default study configuration, when it should have passed")
        with open(os.path.join(self._unit_json_data_dir, 'study_config_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is None:
            self.fail("Validation passed against default study configuration, when it should have failed")

    def test_validate_isajson_assay_config_validation(self):
        """Tests against 4004"""
        err = re.compile("Configuration protocol sequence [\[a-zA-Z' ,\]]* does not match study graph found in [\[a-zA-Z' ,\]]*")
        with open(os.path.join(self._unit_json_data_dir, 'assay_config.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is not None:
            self.fail("Validation failed against transcription_seq.json configuration, when it should have passed")
        with open(os.path.join(self._unit_json_data_dir, 'assay_config_fail.json')) as json_file:
            log_msg_stream = isajson.validate(json_file)
        if err.search(log_msg_stream.getvalue()) is None:
            self.fail("Validation passed against transcription_seq.json configuration, when it should have failed")


class TestValidateIsaTab(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = os.path.join(os.path.dirname(__file__), 'data', 'tab')

    def tearDown(self):
        pass

    def test_validate_isatab_bii_i_1(self):
        with open(os.path.join(self._tab_data_dir, 'BII-I-1', 'i_investigation.txt')) as tab_file:
            log_msg_stream = isatab.validate2(tab_file)
        log = log_msg_stream.getvalue()
        if "Finished validation..." not in log:
            self.fail("Validation did not complete successfully when it should have!")
        if '(W)' not in log:
            self.fail("Validation error and warnings are missing when should report some with BII-I-1")

    def test_validate_isatab_bii_s_3(self):
        with open(os.path.join(self._tab_data_dir, 'BII-S-3', 'i_gilbert.txt')) as tab_file:
            log_msg_stream = isatab.validate2(tab_file)
        log = log_msg_stream.getvalue()
        if "Finished validation..." not in log:
            self.fail("Validation did not complete successfully when it should have!")
        elif '(W)' not in log:
            self.fail("Validation error and warnings are missing when should report some with BII-S-3")

    def test_validate_isatab_bii_s_7(self):
        with open(os.path.join(self._tab_data_dir, 'BII-S-7', 'i_matteo.txt')) as tab_file:
            log_msg_stream = isatab.validate2(tab_file)
        log = log_msg_stream.getvalue()
        if "Finished validation..." not in log:
            self.fail("Validation did not complete successfully when it should have!")
        elif '(W)' not in log:
            self.fail("Validation error and warnings are missing when should report some with BII-S-7")
