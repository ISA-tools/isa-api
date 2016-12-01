# coding: utf-8
from __future__ import print_function

__author__ = 'agbeltran'

import json
import os
import functools
import six
import glob
from jsonschema import Draft4Validator

# This will remove the "'U' flag is deprecated" DeprecationWarning in Python3
open = functools.partial(open, mode='r') if six.PY3 else functools.partial(open, mode='rbU')

def validateSchemasInFolder(folder):
    path = os.path.abspath(folder)
    files = (f for f in glob.iglob(os.path.join(path, '*')) if os.path.isfile(f))

    for schemaFile in files:
        if schemaFile.endswith('.json'):
            try:
                print("Validating schema {} ...".format(schemaFile))
            except TypeError:
                print("Validating schema {} ...".format(schemaFile.encode('utf-8')))
            with open(schemaFile) as fp:
                schema = json.load(fp)
            Draft4Validator.check_schema(schema)
            print("done.")
