# coding: utf-8
import unittest
from isatools.validate.validate_schemas import validateSchemasInFolder
import os


class TestIsaJsonSchemas(unittest.TestCase):

    def setUp(self):
        self._schemas_dir = os.path.join(os.path.dirname(__file__), '..', 'isatools', 'schemas')

    # validating schemas for isa v1 model
    def test_isa_model_v1_schemas(self):
        folder = os.path.join(self._schemas_dir, "isa_model_version_1_0_schemas", "core")
        validateSchemasInFolder(folder)

    # validating schemas for isa v2 core model and extensions
    def test_isa_model_v2_schemas(self):
        folder = os.path.join(self._schemas_dir, "isa_model_version_2_0_schemas", "core")
        # self.folder = "../isatools/schemas/isa_model_version_2_0_schemas/core"
        validateSchemasInFolder(folder)
        folder = os.path.join(self._schemas_dir, "isa_model_version_2_0_schemas", "DFT")
        validateSchemasInFolder(folder)

    def test_cedar_schemas(self):
        folder = os.path.join(self._schemas_dir, "cedar")
        validateSchemasInFolder(folder)
