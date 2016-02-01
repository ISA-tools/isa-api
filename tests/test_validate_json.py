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

    # def test_cedar_example(self):
    #   validateJsonAgainstSchemas("../isatools/schemas/cedar/InvestigationSchema.json","../isatools/schemas/cedar/InvestigationExampleInstances.json")
    #
    # def test_cedar_bii_i_1(self):
    #   validateJsonAgainstSchemas("../isatools/schemas/cedar/InvestigationSchema.json","./data/BII-I-1.json")

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

    def test_ideally_canonical(self):
        try:
            validateJsonAgainstSchemas(self.investigation_schema_dir, os.path.join(self._test_json_dir,
                                                                                   "ideally-canonical.json"))
        except ValidationError:
            self.fail('JSON Validation against schema failed')
