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

        #print isatab

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
            ("title", dict([ ("value", isatab.metadata['Investigation Title'])])),
            ("description", dict([ ("value", isatab.metadata['Investigation Description'])])),
            ("identifier", dict([ ("value", isatab.metadata['Investigation Identifier'])])),
            ("submissionDate", dict([ ("value", isatab.metadata['Investigation Submission Date'])])),
            ("publicReleaseDate", dict([ ("value", isatab.metadata['Investigation Public Release Date'])])),
            ("hasStudy", self.createStudiesArray(isatab.studies)),
            ("hasContact", self.createInvestigationContactsArray(isatab.contacts)),
            ("hasPublication", self.createPublicationsArray(isatab.publications))
        ])

        cedar_json = CEDARSchema(
            investigation=investigationObject
        )

        #save output json
        file_name = os.path.join(json_dir,isatab.metadata['Investigation Identifier']+".json")
        with open(file_name, "w") as outfile:
            json.dump(cedar_json, outfile, indent=4, sort_keys=True)
            outfile.close()

    def createStudiesArray(self, studies):
        json_list = []
        for study in studies:
            #print study
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"),
                ("@type", "https://repo.metadatacenter.org/model/Study"),
                ("title", dict([("value", study.metadata['Study Title'])])),
                ("description", dict([("value", study.metadata['Study Description'])])),
                ("identifier", dict([("value", study.metadata['Study Identifier'])])),
                ("submissionDate", dict([("value", study.metadata['Study Submission Date'])])),
                ("publicReleaseDate", dict([("value", study.metadata['Study Public Release Date'])])),
                ("studyDesignType", dict([("value", "")])),  #dict([("value", study.metadata['Study Public Design Type Accession Number'])]))
                ("hasPublication", []),
                ("hasContact", []),
                ("hasStudyFactor", []),
                ("hasExperiment", []),
                ("hasStudyAssay", []),
                ("hasStudyGroupPopulation", []),
                ("hasStudySubject", [])
            ])
            json_list.append(json_item)
        return json_list

    def createInvestigationContactsArray(self, contacts):
        json_list = []
        for contact in contacts:
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"),
                ("@type", "https://repo.metadatacenter.org/model/Contact"),
                ("lastName", dict([("value", contact['Investigation Person Last Name'])])),
                ("firstName", dict([("value", contact['Investigation Person First Name'])])),
                ("middleInitial", dict([("value", contact['Investigation Person Mid Initials'])])),
                ("email", dict([("value", contact['Investigation Person Email'])])),
                ("phone", dict([("value", contact['Investigation Person Phone'])])),
                ("fax", dict([("value", contact['Investigation Person Fax'])])),
                ("address", dict([("value", contact['Investigation Person Address'])])),
                ("role", dict([("value", contact['Investigation Person Roles Term Accession Number'])])),
                ("hasAffiliation", self.createAffiliationsArray(contact['Investigation Person Affiliation']))
                ])
            json_list.append(json_item)
        return json_list

    def createPublicationsArray(self, publications):
        array = []
        return array

    def createAffiliationsArray(self, affiliations):
        array = []
        return array




isa2cedar = ISATab2CEDAR()
isa2cedar.createCEDARjson("../../tests/data/BII-I-1", "./schemas/cedar")
