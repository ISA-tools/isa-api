__author__ = 'agbeltran'

import json, glob, os, ntpath, warlock, string

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
            ("hasStudy", self.createStudiesList(isatab.studies)),
            ("hasContact", self.createInvestigationContactsList(isatab.contacts)),
            ("hasPublication", self.createPublicationsList(isatab.publications))
        ])

        cedar_json = CEDARSchema(
            investigation=investigationObject
        )

        #save output json
        file_name = os.path.join(json_dir,isatab.metadata['Investigation Identifier']+".json")
        with open(file_name, "w") as outfile:
            json.dump(cedar_json, outfile, indent=4, sort_keys=True)
            outfile.close()

    def createStudiesList(self, studies):
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
                ("hasStudyAssay", self.createStudyAssaysList(study.assays)),
                ("hasStudyGroupPopulation", []),
                ("hasStudySubject", []),
                ("hasStudyProtocol", [])
            ])
            json_list.append(json_item)
        return json_list

    def createInvestigationContactsList(self, contacts):
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
                ("hasAffiliation", self.createAffiliationsList(contact['Investigation Person Affiliation']))
                ])
            json_list.append(json_item)
        return json_list

    def createPublicationsList(self, publications):
        json_list = []
        for publication in publications:
            print publication
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"),
                ("@type", "https://repo.metadatacenter.org/model/Publication"),
                ("title", dict([("value", publication['Investigation Publication Title'])])),
                ("pubMedID", dict([("value", publication['Investigation PubMed ID'])])),
                ("doi", dict([("value", publication['Investigation Publication DOI'])])),
                ("authorList", self.createAuthorList(publication['Investigation Publication Author List'])),
                ("status", dict([("value", publication['Investigation Publication Status'])])),
                ])
            json_list.append(json_item)
        return json_list

    def createAffiliationsList(self, affiliations):
        array = []
        return array

    def createStudyAssaysList(self, assays):
        json_list = []
        # for assay in assays:
        #     json_item = {}
        #     json_list.append(json_item)
        return json_list

    def createAuthorList(self, authorListString):
        json_list = []
        elements = authorListString.split(',')
        for element in elements:
            json_item = dict([
                ("value", element)
            ])
            json_list.append(json_item)
        return json_list



isa2cedar = ISATab2CEDAR()
isa2cedar.createCEDARjson("../../tests/data/BII-I-1", "./schemas/cedar")
