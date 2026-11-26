"""Utilities for mapping ISA Pydantic models to OBO JSON-LD contexts."""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry
from referencing.jsonschema import DRAFT202012

import isatools


def isatools_json_default(value):
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, datetime):
        return value.isoformat()
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def validate_with_isa_json_schema(json_dict: dict, schema: None | str | Path | dict = None) -> None:
    """Validate an ISA-JSON dictionary against a schema.

    ``schema`` may be an in-memory JSON Schema, a schema file, or a directory
    containing ``investigation_schema.json`` and its referenced schemas. When
    omitted, the bundled ISA model v1.0 core schemas are used.
    """
    if schema is None:
        schema = (
            Path(isatools.__file__).parent
            / "resources"
            / "schemas"
            / "isa_model_version_1_0_schemas"
            / "core"
        )

    if isinstance(schema, dict):
        schema_resource = DRAFT202012.create_resource(schema)
        schema_id = schema.get("$id")
        if schema_id:
            registry = Registry().with_resource(schema_id, schema_resource)
            validator = Draft202012Validator(
                {"$ref": schema_id},
                registry=registry,
                format_checker=FormatChecker(),
            )
        else:
            validator = Draft202012Validator(schema, format_checker=FormatChecker())
    else:
        if isinstance(schema, str):
            schema = Path(schema)
        if not isinstance(schema, Path):
            raise TypeError("schema must be a dict, string path, pathlib.Path, or None")

        schema = schema.expanduser().resolve()
        if not schema.exists():
            raise ValueError(f"schema file or folder does not exist: {schema}")

        if schema.is_dir():
            schema_directory = schema
            schema_path = schema_directory / "investigation_schema.json"
            if not schema_path.is_file():
                raise ValueError(
                    f"schema directory does not contain investigation_schema.json: {schema_directory}"
                )
        elif schema.is_file():
            schema_path = schema
            schema_directory = schema.parent
        else:
            raise ValueError(f"schema is not a file or folder: {schema}")

        root_schema = json.loads(schema_path.read_text(encoding="utf-8"))
        root_uri = root_schema.get("$id", schema_path.as_uri())
        schema_base_uri = root_uri.rsplit("/", 1)[0] + "/"
        resources_by_uri = {}
        for path in schema_directory.glob("*.json"):
            schema_dict = json.loads(path.read_text(encoding="utf-8"))
            resource = DRAFT202012.create_resource(schema_dict)
            resources_by_uri[path.resolve().as_uri()] = resource
            resources_by_uri[schema_base_uri + path.name] = resource
            if schema_dict.get("$id"):
                resources_by_uri[schema_dict["$id"]] = resource

        registry = Registry().with_resources(resources_by_uri.items())
        validator = Draft202012Validator(
            {"$ref": root_uri},
            registry=registry,
            format_checker=FormatChecker(),
        )

    validator.validate(json_dict)
