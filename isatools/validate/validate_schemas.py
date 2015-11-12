__author__ = 'agbeltran'

import json, os
from os import listdir
from os.path import isfile, join
from jsonschema import Draft4Validator

def validateSchemasInFolder(folder):
    path = os.path.abspath(folder)
    files = [ f for f in listdir(path) if isfile(join(path,f)) ]

    for schemaFile in files:
        if (schemaFile.endswith('.json')):
            print("Validating schema ", schemaFile, "...")
            schema = json.load(open(join(path,schemaFile)))
            Draft4Validator.check_schema(schema)
            print("done.")
