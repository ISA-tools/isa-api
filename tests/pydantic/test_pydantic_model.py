from __future__ import annotations

import json
import unittest
from pathlib import Path

import isatools
from isatools.pydantic.models import JSONLD_ENABLED, PYDANTIC_ENABLED
from isatools.pydantic.utils import validate_with_isa_json_schema

if PYDANTIC_ENABLED:
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry
    from referencing.jsonschema import DRAFT202012

    from isatools.model import Investigation as ISAToolsInvestigation
    from isatools.pydantic.models import (
        WIKIDATA_CONTEXT_DIR,
        WIKIDATA_CONTEXT_FILENAME_MATCH_PATTERN,
        WIKIDATA_CONTEXT_ID_FILE_PREFIX,
        Investigation,
        JsonLdConfiguration,
        LoadOptions,
        SerializationOptions,
    )

    class TestPydanticModel(unittest.TestCase):
        def setUp(self):
            self.test_data = Path(__file__).resolve().parent / "fixtures" / "i_investigation.json"
            self.jsonld_config = JsonLdConfiguration(
                jsonld_dir=WIKIDATA_CONTEXT_DIR,
                filename_match_pattern=WIKIDATA_CONTEXT_FILENAME_MATCH_PATTERN,
                context_id_prefix=WIKIDATA_CONTEXT_ID_FILE_PREFIX,
            )

        def test_load_from_file(self):
            investigation = Investigation.from_file(
                self.test_data, options=LoadOptions(jsonld_config=self.jsonld_config)
            )
            assert len(investigation.studies) == 1

        def test_to_dict(self):
            investigation = Investigation.from_file(self.test_data)
            inv_dict = investigation.to_dict(
                options=SerializationOptions(ignore_empty_fields=True),
            )
            assert len(inv_dict.get("studies")) == 1

        def test_to_dict_jsonld_compact(self):
            investigation = Investigation.from_file(
                self.test_data,
                options=LoadOptions(jsonld_config=self.jsonld_config, generate_ids=True),
            )
            inv_dict = investigation.to_dict(
                options=SerializationOptions(ignore_empty_fields=True),
            )
            assert len(inv_dict.get("studies")) == 1

        def test_from_isatools_model(self):
            isatools_investigation = ISAToolsInvestigation()
            isatools_investigation.from_dict(json.loads(self.test_data.read_text()))

            investigation = Investigation.from_isatools_model(isatools_investigation)

            self.assertEqual(investigation.title, isatools_investigation.title)
            self.assertEqual(len(investigation.studies), len(isatools_investigation.studies))
            self.assertEqual(len(investigation.people), len(isatools_investigation.contacts))
            self.assertEqual(
                investigation.studies[0].identifier,
                isatools_investigation.studies[0].identifier,
            )
            self.assertEqual(
                len(investigation.studies[0].assays),
                len(isatools_investigation.studies[0].assays),
            )

        def test_to_isatools_model(self):
            investigation = Investigation.from_file(self.test_data)

            isatools_investigation = investigation.to_isatools_model()

            self.assertIsInstance(isatools_investigation, ISAToolsInvestigation)
            self.assertEqual(isatools_investigation.title, investigation.title)
            self.assertEqual(len(isatools_investigation.studies), len(investigation.studies))
            self.assertEqual(
                isatools_investigation.studies[0].identifier,
                investigation.studies[0].identifier,
            )
            self.assertEqual(
                len(isatools_investigation.studies[0].assays),
                len(investigation.studies[0].assays),
            )

        @staticmethod
        def _remove_empty_values(value):
            """Remove empty values recursively so both model outputs can be compared."""
            if isinstance(value, dict):
                return {
                    key: cleaned
                    for key, item in value.items()
                    if (cleaned := TestPydanticModel._remove_empty_values(item)) not in (None, "", [])
                }
            if isinstance(value, list):
                return [
                    cleaned
                    for item in value
                    if (cleaned := TestPydanticModel._remove_empty_values(item)) not in (None, "", [])
                ]
            return value

        def test_pydantic_and_isatools_models_and_validate(self):
            source_data = json.loads(self.test_data.read_text())

            pydantic_investigation = Investigation.from_file(self.test_data)

            isatools_investigation = ISAToolsInvestigation()
            isatools_investigation.from_dict(source_data)

            pydantic_dict = pydantic_investigation.to_dict()
            isatools_dict = isatools_investigation.to_dict()
            schema = Path(isatools.__file__).parent / "resources" / "schemas" / "isa_model_version_1_0_schemas" / "core"
            validate_with_isa_json_schema(pydantic_dict, schema=schema)
            validate_with_isa_json_schema(isatools_dict, schema=schema)


if PYDANTIC_ENABLED and JSONLD_ENABLED:
    import rdflib
    from pyld import FileDocumentLoader

    class TestJsonLdModel(unittest.TestCase):
        def setUp(self):
            self.test_data = Path(__file__).resolve().parent / "fixtures" / "i_investigation.json"
            self.jsonld_config = JsonLdConfiguration(
                jsonld_dir=WIKIDATA_CONTEXT_DIR,
                filename_match_pattern=WIKIDATA_CONTEXT_FILENAME_MATCH_PATTERN,
                context_id_prefix=WIKIDATA_CONTEXT_ID_FILE_PREFIX,
            )

        def test_to_dict_jsonld_expanded(self):
            jsonld_expand_options = {
                "documentLoader": FileDocumentLoader(),
                "base": "https://raw.githubusercontent.com/ISA-tools/isa-api",
            }
            investigation = Investigation.from_file(
                self.test_data,
                options=LoadOptions(jsonld_config=self.jsonld_config, generate_ids=True),
            )
            serialization_options = SerializationOptions(jsonld_config=self.jsonld_config, ignore_empty_fields=True)
            jsonld_document = investigation.to_jsonld_expanded(
                serialization_options=serialization_options, jsonld_expand_options=jsonld_expand_options
            )
            assert jsonld_document

        def test_to_rdf(self):

            jsonld_expand_options = {
                "documentLoader": FileDocumentLoader(),
                "base": "https://raw.githubusercontent.com/ISA-tools/isa-api",
            }
            rdf_options = {
                "base": "https://raw.githubusercontent.com/ISA-tools/isa-api",
            }
            investigation = Investigation.from_file(
                self.test_data,
                options=LoadOptions(jsonld_config=self.jsonld_config, generate_ids=True),
            )
            serialization_options = SerializationOptions(jsonld_config=self.jsonld_config, ignore_empty_fields=True)

            rdf_dataset: rdflib.Dataset = investigation.to_rdf_dataset(
                serialization_options=serialization_options,
                jsonld_expand_options=jsonld_expand_options,
                rdf_options=rdf_options,
            )
            wd_namespace = rdflib.Namespace(WIKIDATA_CONTEXT_ID_FILE_PREFIX)
            isa_namespace = rdflib.Namespace("https://raw.githubusercontent.com/ISA-tools/isa-api")
            rdf_dataset.bind("wd", wd_namespace)
            rdf_dataset.bind("isa", isa_namespace)

            serialized = rdf_dataset.serialize(format="turtle", encoding="utf-8")
            rdf_str = serialized.decode("utf-8") if isinstance(serialized, bytes) else serialized
            assert rdf_str
