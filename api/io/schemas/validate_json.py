__author__ = 'agbeltran'

import json,os
from jsonschema import validate, FormatChecker, RefResolver, Draft4Validator
from os.path import join


path = os.path.abspath("cedar")


investigationSchema = json.load(open(join(path,"InvestigationSchema.json")))

resolver = RefResolver('file://'+path+'/'+"InvestigationSchema.json", investigationSchema)

validator = Draft4Validator(investigationSchema, resolver=resolver)

validator.validate(json.load(open(join(path,"ExampleInvestigationData.json"))), investigationSchema)


