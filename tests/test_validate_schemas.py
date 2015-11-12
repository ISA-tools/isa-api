__author__ = 'agbeltran'

import unittest
from isatools.validate.validate_schemas import validateSchemasInFolder

class ValidateSchemasTest(unittest.TestCase):

      #validating schemas for isa v1 model
      def test_isa_model_v1_schemas(self):
        self.folder = "../isatools/schemas/isa_model_version_1_0_schemas/core"
        validateSchemasInFolder(self.folder)

      #validating schemas for isa v2 core model and extensions
      def test_isa_model_v2_schemas(self):
        self.folder = "../isatools/schemas/isa_model_version_2_0_schemas/core"
        validateSchemasInFolder(self.folder)
        self.folder = "../isatools/schemas/isa_model_version_2_0_schemas/DFT"
        validateSchemasInFolder(self.folder)

      def test_cedar_schemas(self):
        self.folder = "../isatools/schemas/cedar"
        validateSchemasInFolder(self.folder)

