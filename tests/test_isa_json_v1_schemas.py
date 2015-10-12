
import json, os, unittest
from jsonschema import Draft4Validator, validate, FormatChecker
from isatools.convert.isatab_to_json import IsatabToJsonWriter

class ISASchemasTest(unittest.TestCase):

    def setUp(self):
        self._dir = os.path.join(os.path.dirname(__file__), "data")
        self._schema_dir = os.path.join(os.path.dirname(__file__) + "/../isatools", "schemas/isa_model_version_1_0_schemas")
        self._work_dir = os.path.join(self._dir, "BII-I-1")
        self._json_dir = self._work_dir + "-json"

    def tearDown(self):
        """Remove temporary directory (generated JSON)?"""
        #shutil.rmtree(self._json_dir, ignore_errors=True)
        pass

    def test_ontology_source_reference_schema(self):
        schema = json.load(open(self._schema_dir + "/ontology_source_reference_schema.json"))
        Draft4Validator.check_schema(schema)

    def test_factor_schema(self):
        schema = json.load(open(self._schema_dir + "/factor_schema.json"))
        Draft4Validator.check_schema(schema)

    def test_factor_value_schema(self):
        schema = json.load(open(self._schema_dir + "/factor_value_schema.json"))
        Draft4Validator.check_schema(schema)

    def test_material_attribute_schema(self):
        schema = json.load(open(self._schema_dir + "/material_attribute_schema.json"))
        Draft4Validator.check_schema(schema)

    def test_sample_schema(self):
        schema = json.load(open(self._schema_dir + "/sample_schema.json"))
        Draft4Validator.check_schema(schema)

    def test_assay_table_schema(self):
        schema = json.load(open(self._schema_dir + "/assay_table_schema.json"))
        Draft4Validator.check_schema(schema)

    def test_assay_schema(self):
        schema = json.load(open(self._schema_dir + "/assay_schema.json"))
        Draft4Validator.check_schema(schema)

    def test_publication_schema(self):
        schema = json.load(open(self._schema_dir + "/publication_schema.json"))
        Draft4Validator.check_schema(schema)

    def test_organization_schema(self):
        schema = json.load(open(self._schema_dir + "/organization_schema.json"))
        Draft4Validator.check_schema(schema)

    def test_person_schema(self):
        schema = json.load(open(self._schema_dir + "/person_schema.json"))
        Draft4Validator.check_schema(schema)

    def test_source_schema(self):
        schema = json.load(open(self._schema_dir + "/source_schema.json"))
        Draft4Validator.check_schema(schema)

    def test_study_sample_table_schema(self):
        schema = json.load(open(self._schema_dir + "/study_sample_table_schema.json"))
        Draft4Validator.check_schema(schema)

    def test_protocol_schema(self):
        schema = json.load(open(self._schema_dir + "/protocol_schema.json"))
        Draft4Validator.check_schema(schema)

    def test_study_schema(self):
        schema = json.load(open(self._schema_dir + "/study_schema.json"))
        Draft4Validator.check_schema(schema)

    def test_investigation_schema(self):
        schema = json.load(open(self._schema_dir + "/investigation_schema.json"))
        Draft4Validator.check_schema(schema)


    """
    def test_json_schemas(self):
        pass

        #common_definitions_schema = json.load(open("/isa_model_version_1_0_schemas/common_definitions_schema.json"))
        #Draft4Validator.check_schema(common_definitions_schema)
        #assay_schema = json.load(open("schemas/isa_table_schema.json"))
        #Draft4Validator.check_schema(assay_schema)
        #assay_transcription_micro = json.load(open("schemas/assay_transcription_micro.json"))
        #Draft4Validator.check_schema(assay_transcription_micro)

        #validate(json.load(open("../../json/BII-I-1_json/i_Investigation.json")), investigationSchema, format_checker=FormatChecker())

        # What does this bit do? Is it validating schemas against test data? <DJ>

        if not os.path.exists(self._json_dir):
            os.makedirs(self._json_dir)
        # write out the json files for the isa-tab
        writer = IsatabToJsonWriter()
        writer.parsingIsatab(self._work_dir, self._json_dir)

        validate(json.load(open(self._json_dir + "/i_Investigation.json")), investigation_schema, format_checker=FormatChecker())
        validate(json.load(open(self._json_dir + "/s_BII-S-1.json")), study_schema, format_checker=FormatChecker())
        validate(json.load(open(self._json_dir + "/s_BII-S-2.json")), study_schema, format_checker=FormatChecker())
        validate(json.load(open(self._json_dir + "/a_metabolome.json")), assay_schema, format_checker=FormatChecker())
        validate(json.load(open(self._json_dir + "/a_microarray.json")), assay_schema, format_checker=FormatChecker())
        validate(json.load(open(self._json_dir + "/a_proteome.json")), assay_schema, format_checker=FormatChecker())
        validate(json.load(open(self._json_dir + "/a_transcriptome.json")), assay_schema, format_checker=FormatChecker())
    """