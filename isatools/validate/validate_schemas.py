__author__ = 'agbeltran'

import json
import os
import glob
from jsonschema import Draft4Validator

def validateSchemasInFolder(folder):
    path = os.path.abspath(folder)
    for schemaFile in glob.iglob(os.path.join(path, '*.json')):
        print("Validating schema ", os.path.basename(schemaFile), "...")
        schema = json.load(open(schemaFile))
        Draft4Validator.check_schema(schema)
        print("done.")
