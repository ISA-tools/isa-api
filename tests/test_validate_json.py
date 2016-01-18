from unittest import TestCase
import os
from isatools.validate.validate_json import validateJsonAgainstSchemas


class ValidateJsonTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)
        self.investigation_schema_dir = os.path.join(self._dir, "../isatools/schemas/isa_model_version_1_0_"
                                                                "schemas/core/investigation_schema.json")

    # def test_cedar_example(self):
    #   validateJsonAgainstSchemas("../isatools/schemas/cedar/InvestigationSchema.json","../isatools/schemas/cedar/InvestigationExampleInstances.json")
    #
    # def test_cedar_bii_i_1(self):
    #   validateJsonAgainstSchemas("../isatools/schemas/cedar/InvestigationSchema.json","./data/BII-I-1.json")

    def test_sampledata_bii_i_1(self):
        validateJsonAgainstSchemas(self.investigation_schema_dir, "../isatools/sampledata/BII-I-1.json")

    def test_sampledata_bii_s_3(self):
        validateJsonAgainstSchemas(self.investigation_schema_dir, "../isatools/sampledata/BII-S-3.json")

    def test_sampledata_bii_s_7(self):
        validateJsonAgainstSchemas(self.investigation_schema_dir, "../isatools/sampledata/BII-S-7.json")
