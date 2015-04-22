
import json, os
from jsonschema import Draft4Validator, validate, FormatChecker
from api.io.writer import IsatabToJsonWriter

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

folder_name = "BII-I-1"
work_dir = os.path.join("../../tests/data", folder_name)
json_dir = os.path.join("../../tests/data", folder_name + "-json")

if not os.path.exists(json_dir):
    os.makedirs(json_dir)
# write out the json files for the isa-tab
writer = IsatabToJsonWriter()
writer.parsingIsatab(work_dir, json_dir)

validate(json.load(open(json_dir + "/i_Investigation.json")), investigationSchema, format_checker=FormatChecker())

validate(json.load(open(json_dir + "/s_BII-S-1.json")), studySchema, format_checker=FormatChecker())

validate(json.load(open(json_dir + "/s_BII-S-2.json")), studySchema, format_checker=FormatChecker())

validate(json.load(open(json_dir + "/a_metabolome.json")), assaySchema, format_checker=FormatChecker())

validate(json.load(open(json_dir + "/a_microarray.json")), assaySchema, format_checker=FormatChecker())

validate(json.load(open(json_dir + "/a_proteome.json")), assaySchema, format_checker=FormatChecker())

validate(json.load(open(json_dir + "/a_transcriptome.json")), assaySchema, format_checker=FormatChecker())