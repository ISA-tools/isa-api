__author__ = 'agbeltran'

import unittest
from isatools.validate.validate_schemas import validateSchemasInFolder

class ValidateSchemasTest(unittest.TestCase):

      def test_cedar_schemas(self):
        self.folder = "../isatools/schemas/cedar"
        validateSchemasInFolder(self.folder)

      def test_cedar_schemas(self):
        self.folder = "../isatools/schemas/isa_model_version_1_0_schemas"
        validateSchemasInFolder(self.folder)
