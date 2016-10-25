# coding: utf-8
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
            print("Validating schema {} ...".format(schemaFile))
            with open(join(path,schemaFile)) as fp:
                schema = json.load(fp)
            Draft4Validator.check_schema(schema)
            print("done.")
