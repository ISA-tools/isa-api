from unittest import TestCase
from isatools import isajson, isatab
import os


class ValidateIsaJsonTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def test_json_load(self):
        """Tests against 0001"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'minimal_syntax.json')))
        if "There was an error when trying to parse the JSON" in log_msg_stream.getvalue():
            self.fail("Error raised when trying to parse JSON, when it should have been fine!")
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'invalid.json')))
        if "There was an error when trying to parse the JSON" not in log_msg_stream.getvalue():
            self.fail("NO error raised when trying to parse invalid formed JSON!")

    def test_isajson_schemas(self):
        """Tests against 0002"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'minimal_syntax.json')))
        if "The JSON does not validate against the ISA-JSON schemas!" in log_msg_stream.getvalue():
            self.fail("Error raised when trying to parse valid ISA-JSON, when it should have been fine!")
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'invalid_isajson.json')))
        if "The JSON does not validate against the ISA-JSON schemas!" not in log_msg_stream.getvalue():
            self.fail("NO error raised when validating against some non-ISA-JSON conforming JSON!")

    def test_encoding_check(self):
        """Tests against 0010"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'minimal_syntax.json')))
        if "File should be UTF-8 encoding" in log_msg_stream.getvalue():
            self.fail("Validation warning present when testing against UTF-8 encoded file")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'non_utf8.json')))
        if "File should be UTF-8 encoding" not in log_msg_stream.getvalue():
            self.fail("Validation warning missing when testing against UTF-16 encoded file (UTF-8 required)")

    def test_source_link(self):
        """Tests against 1002"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'source_link.json')))
        if "['#source/1'] not found" in log_msg_stream.getvalue():
            self.fail("Validation error present when should pass without error - source link reports broken when "
                      "present in data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'source_link_fail.json')))
        if "['#source/1'] not found" not in log_msg_stream.getvalue():
            self.fail("Validation error missing when should report error - data has broken source link but not "
                      "reported in validation report")

    def test_sample_link(self):
        """Tests against 1003"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'sample_link.json')))
        if "['#sample/1'] not found" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - sample link reports broken when present in "
                "data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'sample_link_fail.json')))
        if "['#sample/1'] not found" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken sample link but not reported in "
                "validation report")

    def test_data_file_link(self):
        """Tests against 1004"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'datafile_link.json')))
        if "['#data/a_file.dat'] not found" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - data file link reports broken when present "
                "in data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'datafile_link_fail.json')))
        if "['#data/a_file.dat'] not found" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken data file link but not reported "
                "in validation report")

    def test_material_link(self):
        """Tests against 1005"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'material_link.json')))
        if "['#material/1'] not found" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error -materiallink link reports broken when "
                "present in data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'material_link_fail.json')))
        if "['#material/1'] not found" not in log_msg_stream.getvalue():
            self.fail(
        "Validation error missing when should report error - data has broken material link but not reported in "
        "validation report")

    def test_process_link(self):
        """Tests against 1006"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'process_link.json')))
        if "link #process/1 in process #process/2 does not refer to another process" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - process link reports broken when present "
                "in data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'process_link_fail.json')))
        if "link #process/1 in process #process/2 does not refer to another process" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken process link but not reported in "
                "validation report")

    def test_protocol_ref_link(self):
        """Tests against 1007"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_ref_link.json')))
        if "['#protocol/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - executesProtocol link reports broken when "
                "present in data")
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_ref_link_fail.json')))
        if "['#protocol/1'] used in a study or assay process sequence not declared" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken executesProtocol link but not "
                "reported in validation report")

    def test_factor_link(self):
        """Tests against 1008"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'factor_link.json')))
        if "['#factor/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - factor link in factorValue reports broken "
                "when present in data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'factor_link_fail.json')))
        if "['#factor/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken factor link in factorValue but "
                "not reported in validation report")

    def test_protocol_parameter_link(self):
        """Tests against 1009"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_parameter_link.json')))
        if "['#parameter/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - parameter link in parameterValue reports "
                "broken when present in data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_'
                                                                                       'parameter_link_fail.json')))
        if "['#parameter/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has broken parameter link in parameterValue "
                "but not reported in validation report")

    def test_iso8601(self):
        """Tests against 3001"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'iso8601.json')))
        if "does not conform to ISO8601 format" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - incorrectly formatted ISO8601 date in "
                "publicReleaseDate reports invalid when valid data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'iso8601_fail.json')))
        if "does not conform to ISO8601 format" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has incorrectly formatted ISO8601 date in "
                "publicReleaseDate but not reported in validation report")

    def test_doi(self):
        """Tests against 3002"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'doi.json')))
        if "does not conform to DOI format" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - incorrectly formatted DOI in publication "
                "reports invalid when valid data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'doi_fail.json')))
        if "does not conform to DOI format" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has incorrectly formatted DOI in publication "
                "but not reported in validation report")

    def test_pubmed(self):
        """Tests against 3003"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'pubmed.json')))
        if "is not valid format" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - incorrectly formatted Pubmed ID in "
                "publication reports invalid when valid data")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'pubmed_fail.json')))
        if "is not valid format" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has incorrectly formatted Pubmed ID in "
                "publication but not reported in validation report")

    def test_protocol_used(self):
        """Tests against 3005"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_used.json')))
        if "['#protocol/1'] not used" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - incorrectly reports #protocol/1 not used "
                "when it has been used in #process/1")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_used_fail.json')))
        if "['#protocol/1'] not used" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has incorrectly reported everything is OK "
                "but not reported #protocol/1 as being unused")

    def test_factor_used(self):
        """Tests against 3006"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'factor_used.json')))
        if "factors declared ['#factor/1'] that have not been used" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - incorrectly reports #factor/1 not used when "
                "it has been used in #sample/1")
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'factor_used_fail.json')))
        if "factors declared ['#factor/1'] that have not been used" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has incorrectly reported everything is OK "
                "but not reported #factor/1 as being unused")

    def test_term_source_used(self):
        """Tests against 3007"""
        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'term_source_used.json')))
        if "ontology sources declared ['PATO'] that have not been used" in log_msg_stream.getvalue():
            self.fail(
                "Validation error present when should pass without error - incorrectly reports PATO not used when it "
                "has been used in #factor/1")

        log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'term_source_used_fail.json')))
        if "ontology sources declared ['PATO'] that have not been used" not in log_msg_stream.getvalue():
            self.fail(
                "Validation error missing when should report error - data has incorrectly reported everything is OK "
                "but not reported PATO as being unused")


class ValidateIsaTabTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def test_validate_bii_i_1(self):
        log_msg_stream = isatab.validate2(open(os.path.join(self._dir, 'data', 'BII-I-1', 'i_investigation.txt')))
        if '(W)' not in log_msg_stream.getvalue() and '(E)' not in log_msg_stream.getvalue():
            self.fail("Validation error and warnings are missing when should report some with BII-I-1")

    def test_validate_bii_s_3(self):
        log_msg_stream = isatab.validate2(open(os.path.join(self._dir, 'data', 'BII-S-3', 'i_gilbert.txt')))
        if '(W)' not in log_msg_stream.getvalue() and '(E)' not in log_msg_stream.getvalue():
            self.fail("Validation error and warnings are missing when should report some with BII-S-3")

    def test_validate_bii_s_7(self):
        log_msg_stream = isatab.validate2(open(os.path.join(self._dir, 'data', 'BII-S-7', 'i_matteo.txt')))
        if '(W)' not in log_msg_stream.getvalue() and '(E)' not in log_msg_stream.getvalue():
            self.fail("Validation error and warnings are missing when should report some with BII-S-7")
