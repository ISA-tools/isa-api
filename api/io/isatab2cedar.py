__author__ = 'agbeltran'

import json, glob, os, ntpath, warlock

from os.path import join
from api.io import parser
from api.io.common_functions import CommonFunctions


class ISATab2CEDAR():
    def createCEDARjson(self, work_dir, json_dir):
        path = "./schemas/cedar/"
        schema_file = "InvestigationSchema.json"
        schema = json.load(open(join(path,schema_file)))
        CEDARSchema = warlock.model_factory(schema)

        #parse ISA tab
        isatab = parser.parse(work_dir)

        # process the investigation file
        fileNames = glob.glob(os.path.join(work_dir, "i_*.txt")) + \
                    glob.glob(os.path.join(work_dir, "*.idf.txt"))
        investigationFilename = ntpath.basename(str(fileNames[0])).split(".")
        #self.convert_investigation(rec, os.path.join(json_dir, investigationFilename[0] + ".json"),
        #                           os.path.join(json_dir, os.path.basename(work_dir) + ".json"), work_dir, json_dir)

        investigationObject = dict([
            ("schemaID", "https://repo.metadatacenter.org/UUID"),
            ("@id", "https://repo.metadatacenter.org/UUID"),
            ("@type", "https://repo.metadatacenter.org/model/Investigation"),
            ("@context", dict(
                [
                    ("model", "https://repo.metadatacenter.org/model/"),
                    ("xsd", "http://www.w3.org/2001/XMLSchema"),
                    ("schema", "https://schema.org/"),
                    ("title", "schema:title"),
                    ("description", "schema:description")
                ]
            )),
            ("title", dict([ ("value", isatab.metadata['Investigation Title'])]))
        ])

        cedar_json = CEDARSchema(
            investigation=investigationObject
        )

        #save output json
        with open(investigationFilename, "w") as outfile:
            json.dump(cedar_json, outfile, indent=4, sort_keys=True)
            outfile.close()


    # def convert_investigation(self, rec, i_file, single_file, work_dir, json_dir):
    #     json_structures = {}
    #     self.create_investigation_node(json_structures, rec)
    #     # self.studies(json_structures, rec.studies, work_dir, json_dir, False)
    #     with open(i_file, "w") as outfile:
    #         json.dump(json_structures, outfile, indent=4, sort_keys=True)
    #     outfile.close()
    #
    # def create_investigation_node(self, json_structures, rec):
    #     # commonFunctions = CommonFunctions()
    #     json_structures = {}
    #     for meta in rec.metadata:
    #         json_structures["investigation"] = self.create_list_of_attributes_array(rec.metadata, 'Investigation')
    #         #json_structures[commonFunctions.getAttributeName(meta)] = rec.metadata[meta]
    #         #json_structures["publications"] = self.createListOfAttributesArray(rec.publications, 'Investigation Publication')
    #         #json_structures["people"] = self.createListOfAttributesArray(rec.contacts, 'Investigation Person')
    #     return json_structures
    #
    #
    # def create_list_of_attributes_array(self, properties, toBeRemovedTag):
    #     json_list = []
    #     for onto in properties:
    #         json_item = {}
    #         for item in onto:
    #             json_item[self.commonFunctions.makeAttributeName(item, toBeRemovedTag)] = onto[item]
    #         json_list.append(json_item)
    #     return json_list
    #
    #
    # def create_list_of_attributes(self, json_structure, properties, tagName):
    #     json_list = []
    #     for onto in properties:
    #         json_item = {}
    #         for item in onto:
    #             json_item[self.commonFunctions.makeAttributeName(item, 'Term Source')] = onto[item]
    #             json_list.append(json_item)
    #         json_structure[tagName] = json_list
    #     return json_structure

isa2cedar = ISATab2CEDAR()
isa2cedar.createCEDARjson("../../tests/data/BII-I-1", "./schemas/cedar")
