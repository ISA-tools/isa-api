
import json
from jsonschema import Draft4Validator
from jsonschema import validate


investigationSchema = json.load(open("schemas/investigation.json"))
Draft4Validator.check_schema(investigationSchema)

#assay_schema = json.load(open("schemas/assay_schema.json"))
#Draft4Validator.check_schema(assay_schema)

#assay_transcription_micro = json.load(open("schemas/assay_transcription_micro.json"))
#Draft4Validator.check_schema(assay_transcription_micro)


validate( json.load(open("../../json/BII-I-1_json/i_Investigation.json")), investigationSchema)

