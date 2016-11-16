# coding: utf-8
__author__ = 'agbeltran'

import json
import os
from jsonschema import RefResolver, Draft4Validator


def validateJsonAgainstSchemas(schema_file, json_file):
    with open(os.path.join(schema_file)) as fp:
        schema = json.load(fp)
    resolver = RefResolver('file://{}'.format(schema_file), schema)
    validator = Draft4Validator(schema, resolver=resolver)
    with open(json_file) as fp
        validation_result = validator.validate(json.load(fp), schema)
    return validation_result


