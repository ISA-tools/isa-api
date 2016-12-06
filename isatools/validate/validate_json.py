__author__ = 'agbeltran'

import json,os
from jsonschema import RefResolver, Draft4Validator
from os.path import join


def validateJsonAgainstSchemas(schema_file, json_file):
    with open(join(schema_file)) as schema_fp:
        schema = json.load(schema_fp)
        resolver = RefResolver('file://'+schema_file, schema)
        validator = Draft4Validator(schema, resolver=resolver)
        return validator.validate(json.load(open(json_file)), schema)


