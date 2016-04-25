from unittest import TestCase
from isatools import isajson
import os
from jsonschema import ValidationError


class ValidateIsaJsonTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def test_json_load(self):
        """Tests against 0001"""
        with self.assertRaises(ValueError):
            isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'invalid.json')))

        try:
            isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'minimal_syntax.json')))
        except ValueError:
            self.fail("isajson.validate() raised a ValueError where it shouldn't have!")

    def test_isajson_schemas(self):
        """Tests against 0002"""
        with self.assertRaises(ValidationError):
            isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'invalid_isajson.json')))

        try:
            isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'minimal_syntax.json')))
        except ValidationError:
            self.fail("isajson.validate() raised a ValidationError where it shouldn't have!")

    def test_encoding_check(self):
        """Tests against 0010"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'minimal_syntax.json')))
        validation_report = v.generate_report_json()
        encoding_warning = [m['message'] for m in validation_report['warnings'] if "File should be UTF-8 encoding" in m['message']]
        if len(encoding_warning) > 0:
            self.fail("Validation warning present when testing against UTF-8 encoded file")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'non_utf8.json')))
        validation_report = v.generate_report_json()
        encoding_warning = [m['message'] for m in validation_report['warnings'] if
                            "File should be UTF-8 encoding" in m['message']]
        if len(encoding_warning) == 0:
            self.fail("Validation warning missing when testing against UTF-16 encoded file (UTF-8 required)")

    def test_source_link(self):
        """Tests against 1002"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'source_link.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #source/1 not declared" in m['message']]
        if len(object_ref_error) > 0:
            self.fail("Validation error present when should pass without error - source link reports broken when present in data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'source_link_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #source/1 not declared" in m['message']]
        if len(object_ref_error) == 0:
            self.fail("Validation error missing when should report error - data has broken source link but not reported in validation report")


    def test_sample_link(self):
        """Tests against 1003"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'sample_link.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #sample/1 not declared" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - sample link reports broken when present in data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'sample_link_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #sample/1 not declared" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has broken sample link but not reported in validation report")

    def test_data_file_link(self):
        """Tests against 1004"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'datafile_link.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #data/a_file.dat not declared" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - data file link reports broken when present in data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'datafile_link_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #data/a_file.dat not declared" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has broken data file link but not reported in validation report")

    def test_material_link(self):
        """Tests against 1005"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'material_link.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #material/1 not declared" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - material link reports broken when present in data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'material_link_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #material/1 not declared" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has broken material link but not reported in validation report")

    def test_process_link(self):
        """Tests against 1006"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'process_link.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #process/1 not declared" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - process link reports broken when present in data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'process_link_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #process/1 not declared" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has broken process link but not reported in validation report")

    def test_protocol_ref_link(self):
        """Tests against 1007"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_ref_link.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #protocol/1 not declared" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - executesProtocol link reports broken when present in data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_ref_link_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #protocol/1 not declared" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has broken executesProtocol link but not reported in validation report")

    def test_factor_link(self):
        """Tests against 1008"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'factor_link.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #factor/1 not declared" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - factor link in factorValue reports broken when present in data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'factor_link_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #factor/1 not declared" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has broken factor link in factorValue but not reported in validation report")

    def test_protocol_parameter_link(self):
        """Tests against 1009"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_parameter_link.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #parameter/1 not declared" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - parameter link in parameterValue reports broken when present in data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'protocol_parameter_link_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['errors'] if
                            "Object reference #parameter/1 not declared" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has broken parameter link in parameterValue but not reported in validation report")

    def test_iso8601(self):
        """Tests against 3001"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'iso8601.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "Date 2008-08-15 does not conform to ISO8601 format" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - incorrectly formatted ISO8601 date in publicReleaseDate reports invalid when valid data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'iso8601_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "Date 15/08/2008 does not conform to ISO8601 format" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has incorrectly formatted ISO8601 date in publicReleaseDate but not reported in validation report")


    def test_doi(self):
        """Tests against 3002"""
        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'doi.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "DOI 10.1371/journal.pone.0003042 does not conform to DOI format" in m['message']]
        if len(object_ref_error) > 0:
            self.fail(
                "Validation error present when should pass without error - incorrectly formatted DOI in publication reports invalid when valid data")

        v = isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'doi_fail.json')))
        validation_report = v.generate_report_json()
        object_ref_error = [m['message'] for m in validation_report['warnings'] if
                            "DOI 1371/journal.pone.0003042 does not conform to DOI format" in m['message']]
        if len(object_ref_error) == 0:
            self.fail(
                "Validation error missing when should report error - data has incorrectly formatted DOI in publication but not reported in validation report")

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
