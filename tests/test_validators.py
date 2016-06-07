from unittest import TestCase
from isatools import isajson
import os


class ValidateIsaJsonTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def test_json_load(self):
        """Tests against 0001"""
        with open(os.path.join(self._dir, 'data', 'json', 'minimal_syntax.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "There was an error when trying to parse the JSON" in log_msg_stream.getvalue():
                self.fail("Error raised when trying to parse JSON, when it should have been fine!")
        with open(os.path.join(self._dir, 'data', 'json', 'invalid.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "There was an error when trying to parse the JSON" not in log_msg_stream.getvalue():
                self.fail("NO error raised when trying to parse invalid formed JSON!")

    def test_isajson_schemas(self):
        """Tests against 0002"""
        with open(os.path.join(self._dir, 'data', 'json', 'minimal_syntax.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "The JSON does not validate against the ISA-JSON schemas!" in log_msg_stream.getvalue():
                self.fail("Error raised when trying to parse valid ISA-JSON, when it should have been fine!")
        # log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'invalid_isajson.json')))
        # if "The JSON does not validate against the ISA-JSON schemas!" not in log_msg_stream.getvalue():
        #     self.fail("NO error raised when validating against some non-ISA-JSON conforming JSON!")

    def test_encoding_check(self):
        """Tests against 0010"""
        with open(os.path.join(self._dir, 'data', 'json', 'minimal_syntax.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "File should be UTF-8 encoding" in log_msg_stream.getvalue():
                self.fail("Validation warning present when testing against UTF-8 encoded file")
        with open(os.path.join(self._dir, 'data', 'json', 'non_utf8.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "File should be UTF-8 encoding" not in log_msg_stream.getvalue():
                self.fail("Validation warning missing when testing against UTF-16 encoded file (UTF-8 required)")

    def test_source_link(self):
        """Tests against 1002"""
        with open(os.path.join(self._dir, 'data', 'json', 'source_link.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#source/1'] not found" in log_msg_stream.getvalue():
                self.fail("Validation error present when should pass without error - source link reports broken when present in data")
        with open(os.path.join(self._dir, 'data', 'json', 'source_link_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#source/1'] not found" not in log_msg_stream.getvalue():
                self.fail("Validation error missing when should report error - data has broken source link but not reported in validation report")

    def test_sample_link(self):
        """Tests against 1003"""
        with open(os.path.join(self._dir, 'data', 'json', 'sample_link.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#sample/1'] not found" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error present when should pass without error - sample link reports broken when present in data")
        with open(os.path.join(self._dir, 'data', 'json', 'sample_link_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#sample/1'] not found" not in log_msg_stream.getvalue():
                self.fail(
                    "Validation error missing when should report error - data has broken sample link but not reported in validation report")

    def test_data_file_link(self):
        """Tests against 1004"""
        with open(os.path.join(self._dir, 'data', 'json', 'datafile_link.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#data/a_file.dat'] not found" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error present when should pass without error - data file link reports broken when present in data")
        with open(os.path.join(self._dir, 'data', 'json', 'datafile_link_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#data/a_file.dat'] not found" not in log_msg_stream.getvalue():
                self.fail(
                    "Validation error missing when should report error - data has broken data file link but not reported in validation report")

    def test_material_link(self):
        """Tests against 1005"""
        with open(os.path.join(self._dir, 'data', 'json', 'material_link.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#material/1'] not found" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error present when should pass without error -materiallink link reports broken when present in data")
        with open(os.path.join(self._dir, 'data', 'json', 'material_link_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#material/1'] not found" not in log_msg_stream.getvalue():
                self.fail(
            "Validation error missing when should report error - data has broken material link but not reported in validation report")

    def test_process_link(self):
        """Tests against 1006"""
        with open(os.path.join(self._dir, 'data', 'json', 'process_link.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "link #process/1 in process #process/2 does not refer to another process" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error present when should pass without error - process link reports broken when present in data")
        with open(os.path.join(self._dir, 'data', 'json', 'process_link_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "link #process/1 in process #process/2 does not refer to another process" not in log_msg_stream.getvalue():
                self.fail(
                    "Validation error missing when should report error - data has broken process link but not reported in validation report")

    def test_protocol_ref_link(self):
        """Tests against 1007"""
        with open(os.path.join(self._dir, 'data', 'json', 'protocol_ref_link.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#protocol/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error present when should pass without error - executesProtocol link reports broken when present in data")
        with open(os.path.join(self._dir, 'data', 'json', 'protocol_ref_link_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#protocol/1'] used in a study or assay process sequence not declared" not in log_msg_stream.getvalue():
                self.fail(
                    "Validation error missing when should report error - data has broken executesProtocol link but not reported in validation report")

    def test_factor_link(self):
        """Tests against 1008"""
        with open(os.path.join(self._dir, 'data', 'json', 'factor_link.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#factor/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error present when should pass without error - factor link in factorValue reports broken when present in data")
        with open(os.path.join(self._dir, 'data', 'json', 'factor_link_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#factor/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error missing when should report error - data has broken factor link in factorValue but not reported in validation report")

    def test_characteristic_link(self):
        """Tests against 1008"""
        with open(os.path.join(self._dir, 'data', 'json', 'characteristic_link.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#characteristic/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error present when should pass without error - characteristic link reports broken when present in data")
        with open(os.path.join(self._dir, 'data', 'json', 'characteristic_link_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#characteristic/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error missing when should report error - data has broken factor link in factorValue but not reported in validation report")


    # def test_unit_categories_link(self):
    #     """Tests against 1008"""
    #     log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'unit_link.json')))
    #     if "['#Unit/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
    #         self.fail(
    #             "Validation error present when should pass without error - unit link in factorValue reports broken when present in data")
    #
    #     log_msg_stream = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'unit_link.json')))
    #     if "['#Unit/1'] used in a study or assay process sequence not declared" not in log_msg_stream.getvalue():
    #         self.fail(
    #             "Validation error missing when should report error - data has broken factor link in factorValue but not reported in validation report")


    def test_protocol_parameter_link(self):
        """Tests against 1009"""
        with open(os.path.join(self._dir, 'data', 'json', 'protocol_parameter_link.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#parameter/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error present when should pass without error - parameter link in parameterValue reports broken when present in data")
        with open(os.path.join(self._dir, 'data', 'json', 'protocol_parameter_link_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#parameter/1'] used in a study or assay process sequence not declared" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error missing when should report error - data has broken parameter link in parameterValue but not reported in validation report")

    def test_iso8601(self):
        """Tests against 3001"""
        with open(os.path.join(self._dir, 'data', 'json', 'iso8601.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "does not conform to ISO8601 format" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error present when should pass without error - incorrectly formatted ISO8601 date in publicReleaseDate reports invalid when valid data")
        with open(os.path.join(self._dir, 'data', 'json', 'iso8601_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "does not conform to ISO8601 format" not in log_msg_stream.getvalue():
                self.fail(
                    "Validation error missing when should report error - data has incorrectly formatted ISO8601 date in publicReleaseDate but not reported in validation report")

    def test_doi(self):
        """Tests against 3002"""
        with open(os.path.join(self._dir, 'data', 'json', 'doi.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "does not conform to DOI format" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error present when should pass without error - incorrectly formatted DOI in publication reports invalid when valid data")
        with open(os.path.join(self._dir, 'data', 'json', 'doi_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "does not conform to DOI format" not in log_msg_stream.getvalue():
                self.fail(
                    "Validation error missing when should report error - data has incorrectly formatted DOI in publication but not reported in validation report")

    def test_pubmed(self):
        """Tests against 3003"""
        with open(os.path.join(self._dir, 'data', 'json', 'pubmed.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "is not valid format" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error present when should pass without error - incorrectly formatted Pubmed ID in publication reports invalid when valid data")
        with open(os.path.join(self._dir, 'data', 'json', 'pubmed_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "is not valid format" not in log_msg_stream.getvalue():
                self.fail(
                    "Validation error missing when should report error - data has incorrectly formatted Pubmed ID in publication but not reported in validation report")

    def test_protocol_used(self):
        """Tests against 1019"""
        with open(os.path.join(self._dir, 'data', 'json', 'protocol_used.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#protocol/1'] not used" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error present when should pass without error - incorrectly reports #protocol/1 not used when it has been used in #process/1")
        with open(os.path.join(self._dir, 'data', 'json', 'protocol_used_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "['#protocol/1'] not used" not in log_msg_stream.getvalue():
                self.fail(
                    "Validation error missing when should report error - data has incorrectly reported everything is OK but not reported #protocol/1 as being unused")

    def test_factor_used(self):
        """Tests against 1021"""
        with open(os.path.join(self._dir, 'data', 'json', 'factor_used.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "factors declared ['#factor/1'] that have not been used" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error present when should pass without error - incorrectly reports #factor/1 not used when it has been used in #sample/1")
        with open(os.path.join(self._dir, 'data', 'json', 'factor_used_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "factors declared ['#factor/1'] that have not been used" not in log_msg_stream.getvalue():
                self.fail(
                    "Validation error missing when should report error - data has incorrectly reported everything is OK but not reported #factor/1 as being unused")

    def test_term_source_used(self):
        """Tests against 3007"""
        with open(os.path.join(self._dir, 'data', 'json', 'term_source_used.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "ontology sources declared ['PATO'] that have not been used" in log_msg_stream.getvalue():
                self.fail(
                    "Validation error present when should pass without error - incorrectly reports PATO not used when it has been used in #factor/1")
        with open(os.path.join(self._dir, 'data', 'json', 'term_source_used_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "ontology sources declared ['PATO'] that have not been used" not in log_msg_stream.getvalue():
                self.fail(
                    "Validation error missing when should report error - data has incorrectly reported everything is OK but not reported PATO as being unused")

    def test_load_config(self):
        """Tests against 4001"""
        try:
            isajson.load_config(os.path.join(self._dir, 'data', 'json', 'configs'))
        except IOError as e:
            self.fail("Could not load config because... " + str(e))

    def test_get_config(self):
        """Tests against 4002"""
        try:
            configs = isajson.load_config(os.path.join(self._dir, 'data', 'json', 'configs'))
            if configs is None:
                self.fail("There was a problem and config is null")
            else:
                self.assertIsNotNone(configs[('metagenome sequencing', 'nucleotide sequencing')])
        except IOError as e:
            self.fail("Could not load config because... " + str(e))

    def test_study_config_validation(self):
        """Tests against 4004"""
        with open(os.path.join(self._dir, 'data', 'json', 'study_config.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "protocol sequence ['sample collection'] does not match study graph" in log_msg_stream.getvalue():
                self.fail("Validation failed against default study configuration, when it should have passed")
        with open(os.path.join(self._dir, 'data', 'json', 'study_config_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "protocol sequence ['sample collection'] does not match study graph" not in log_msg_stream.getvalue():
                self.fail("Validation passed against default study configuration, when it should have failed")

    def test_assay_config_validation(self):
        """Tests against 4004"""
        with open(os.path.join(self._dir, 'data', 'json', 'assay_config.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "protocol sequence ['nucleic acid extraction', 'library construction', 'nucleic acid sequencing', 'sequence analysis data transformation'] does not match study graph" in log_msg_stream.getvalue():
                self.fail("Validation failed against transcription_seq.json configuration, when it should have passed")
        with open(os.path.join(self._dir, 'data', 'json', 'assay_config_fail.json')) as fp:
            log_msg_stream = isajson.validate(fp)
            if "protocol sequence ['nucleic acid extraction', 'library construction', 'nucleic acid sequencing', 'sequence analysis data transformation'] does not match study graph" not in log_msg_stream.getvalue():
                self.fail("Validation passed against transcription_seq.json configuration, when it should have failed")

# class ValidateIsaTabTest(TestCase):
#
#     def setUp(self):
#         self._dir = os.path.dirname(__file__)
#         self.reporting_level = INFO
#
#     def tearDown(self):
#         pass
#
#     def test_i_no_content(self):
#         with self.assertRaises(ValidationError):
#             isatab.validate_i_file(i_fp=open(os.path.join(self._dir, 'data', 'tab', 'invalid_i', 'i_01.txt')))
#
#     def test_i_no_required_labels(self):
#         with self.assertRaises(ValidationError):
#             isatab.validate_i_file(i_fp=open(os.path.join(self._dir, 'data', 'tab', 'invalid_i', 'i_02.txt')))
#
#     def test_i_valid_labels(self):
#         isatab.validate_i_file(i_fp=open(os.path.join(self._dir, 'data', 'tab', 'valid_i', 'i_01.txt')))
#
#     def test_i_content(self):
#         isatab.validate_i_file(i_fp=open(os.path.join(self._dir, 'data', 'tab', 'invalid_i', 'i_03.txt')))
