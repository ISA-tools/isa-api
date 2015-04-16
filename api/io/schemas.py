
import json
from jsonschema import Draft4Validator
#from jsonschema import FormatChecker


#from jsonschema import validate
import validictory

investigationSchema = json.load(open("schemas/investigation_schema.json"))
Draft4Validator.check_schema(investigationSchema)

commonDefinitionsSchema = json.load(open("schemas/common_definitions_schema.json"))
Draft4Validator.check_schema(commonDefinitionsSchema)

studySchema = json.load(open("schemas/study_schema.json"))
Draft4Validator.check_schema(studySchema)

assaySchema = json.load(open("schemas/assay_schema.json"))
Draft4Validator.check_schema(assaySchema)


#assay_schema = json.load(open("schemas/isa_table_schema.json"))
#Draft4Validator.check_schema(assay_schema)

#assay_transcription_micro = json.load(open("schemas/assay_transcription_micro.json"))
#Draft4Validator.check_schema(assay_transcription_micro)


#validate(json.load(open("../../json/BII-I-1_json/i_Investigation.json")), investigationSchema, format_checker=FormatChecker())

validictory.validate(json.load(open("../../json/BII-I-1_json/i_Investigation.json")), investigationSchema)

