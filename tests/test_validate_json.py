from unittest import TestCase
import os
from isatools.validate.validate_json import validateJsonAgainstSchemas
from jsonschema.exceptions import ValidationError


class ValidateJsonTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)
        self._test_json_dir = os.path.join(os.path.dirname(__file__), '..', 'isatools', 'sampledata',)
        self.investigation_schema_dir = os.path.join(self._dir, "..", "isatools", "schemas",
                                                     "isa_model_version_1_0_schemas", "core",
                                                     "investigation_schema.json")
        self.cedar_dir = os.path.join(self._dir, "..", "isatools", "schemas",
                                                     "cedar",
                                                     "investigation_template.json")
        self._mtbls_test_json_dir = os.path.join(os.path.dirname(__file__), "./data", "metabolights")

    def test_sampledata_bii_i_1(self):
        try:
            validateJsonAgainstSchemas(self.investigation_schema_dir, os.path.join(self._test_json_dir, "BII-I-1.json"))
        except ValidationError:
            self.fail('JSON Validation against schema failed')

    def test_sampledata_bii_s_3(self):
        try:
            validateJsonAgainstSchemas(self.investigation_schema_dir, os.path.join(self._test_json_dir, "BII-S-3.json"))
        except ValidationError:
            self.fail('JSON Validation against schema failed')

    def test_sampledata_bii_s_7(self):
        try:
            validateJsonAgainstSchemas(self.investigation_schema_dir, os.path.join(self._test_json_dir, "BII-S-7.json"))
        except ValidationError:
            self.fail('JSON Validation against schema failed')

    # def test_mtbls34(self):
    #     try:
    #         validateJsonAgainstSchemas(self.cedar_dir, os.path.join(self._mtbls_test_json_dir, "MTBLS34.json"))
    #     except ValidationError:
    #         print(ValidationError.message)
    #         self.fail('JSON Validation against schema failed')