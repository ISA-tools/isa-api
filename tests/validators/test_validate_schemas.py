import unittest
import os
import json
import glob
from jsonschema import Draft4Validator


class TestIsaJsonSchemas(unittest.TestCase):

    @staticmethod
    def validateSchemasInFolder(folder):
        path = os.path.abspath(folder)
        for schemaFile in glob.iglob(os.path.join(path, '*.json')):
            print("Validating schema ", os.path.basename(schemaFile), "...")
            with open(schemaFile) as schema_fp:
                schema = json.load(schema_fp)
                Draft4Validator.check_schema(schema)
                print("done.")

    def setUp(self):
        self._schemas_dir = os.path.join(os.path.dirname(__file__), '..', 'isatools', 'schemas')

    # validating schemas for isa v1 model
    def test_isa_model_v1_schemas(self):
        folder = os.path.join(self._schemas_dir, "isa_model_version_1_0_schemas", "core")
        self.validateSchemasInFolder(folder)

    # validating schemas for isa v2 core model and extensions
    def test_isa_model_v2_schemas(self):
        folder = os.path.join(self._schemas_dir, "isa_model_version_2_0_schemas", "core")
        # self.folder = "../isatools/schemas/isa_model_version_2_0_schemas/core"
        self.validateSchemasInFolder(folder)
        folder = os.path.join(self._schemas_dir, "isa_model_version_2_0_schemas", "create")
        self.validateSchemasInFolder(folder)

    def test_cedar_schemas(self):
        folder = os.path.join(self._schemas_dir, "cedar")
        self.validateSchemasInFolder(folder)
