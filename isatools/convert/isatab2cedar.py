# coding: utf-8
from __future__ import unicode_literals

__author__ = 'agbeltran'

import json
import os
from uuid import uuid4
from os import listdir
from os.path import isdir, join
from jsonschema import RefResolver, Draft4Validator
from jsonschema.exceptions import ValidationError

#from bcbio.isatab.parser import InvestigationParser
from isatools.io.isatab_parser import parse

CEDAR_SCHEMA_PATH = join(os.path.dirname(os.path.realpath(__file__)), "../schemas/cedar")

class ISATab2CEDAR():

    def __init__(self, primary_source):
        self.primary_source = primary_source

    def createCEDARjson_folder(self, work_dir, json_dir, inv_identifier):
        print("Convert ISA datasets in folder {}".format(work_dir))
        path = os.path.abspath(work_dir)
        folders = [ f for f in listdir(path) if isdir(join(path,f))]

        for folder in folders:
            self.createCEDARjson(CEDAR_SCHEMA_PATH, join(path,folder), json_dir, inv_identifier)


    def createCEDARjson(self, work_dir, json_dir, inv_identifier):
        print("Converting ISA to CEDAR model for {}".format(work_dir))
        schema_file = "investigation_template.json"
        with open(join(CEDAR_SCHEMA_PATH,schema_file)) as schema_handler:
            schema = json.load(schema_handler)
        resolver = RefResolver('file://'+join(CEDAR_SCHEMA_PATH, schema_file), schema)
        validator = Draft4Validator(schema, resolver=resolver)

        isa_tab = parse(work_dir)
        # parser_file_name = os.path.join(json_dir, "parser.log")
        # with open(parser_file_name, "w") as parserfile:
        #                 parserfile.write(str(isa_tab))
        #                 parserfile.close()

        if isa_tab is None:
            print("No ISAtab dataset found")
        else:
                if isa_tab.metadata:
                    investigationObject = {
                        "@id": "https://repo.metadatacenter.org/UUID/{}".format(uuid4()),
                        "_templateId": "http://example.org",
                        "@type": "https://repo.metadatacenter.org/model/Investigation",
                        "@context": {
                                "description": "https://metadatacenter.org/schemas/description",
                                "title": "https://metadatacenter.org/schemas/title",
                                "study": "https://metadatacenter.org/schemas/study",
                                "submissionDate": "https://metadatacenter.org/schemas/submissionDate",
                                "_value": "https://schema.org/value",
                                "publicReleaseDate": "https://metadatacenter.org/schemas/publicReleaseDate",
                                "identifier": "https://metadatacenter.org/schemas/identifier",
                        },
                        "title": {"_value": isa_tab.metadata['Investigation Title']},
                        "description": {"_value": isa_tab.metadata['Investigation Description']},
                        "identifier": {"_value": isa_tab.metadata['Investigation Identifier']},
                        "submissionDate": {"_value": isa_tab.metadata['Investigation Submission Date']},
                        "publicReleaseDate": {"_value": isa_tab.metadata['Investigation Public Release Date']},
                        "study": self.createStudiesList(isa_tab.studies),
                    }
                else:
                    investigationObject = {
                        "@id": "https://repo.metadatacenter.org/UUID{}".format(uuid4()),
                        "_templateId": "http://example.org",
                        "@type": "https://repo.metadatacenter.org/model/Investigation",
                        "@context": {
                                "description": "https://metadatacenter.org/schemas/description",
                                "title": "https://metadatacenter.org/schemas/title",
                                "study": "https://metadatacenter.org/schemas/study",
                                "submissionDate": "https://metadatacenter.org/schemas/submissionDate",
                                "_value": "https://schema.org/value",
                                "publicReleaseDate": "https://metadatacenter.org/schemas/publicReleaseDate",
                                "identifier": "https://metadatacenter.org/schemas/identifier",
                        },
                        "title": {"_value": ""},
                        "description": {"_value": ""},
                        "identifier": {"_value": ""},
                        "submissionDate": {"_value": ""},
                        "publicReleaseDate": {"_value": ""},
                        "study": self.createStudiesList(isa_tab.studies),
                    }

                cedar_json = investigationObject
                try:
                    investigation_identifier = isa_tab.metadata['Investigation Identifier']
                except KeyError:
                    investigation_identifier = ""

                try:
                    study_identifier = isa_tab.studies[0].metadata['Study Identifier']
                    #study_identifier = study_identifier[study_identifier.find("/")+1:]
                except KeyError:
                    study_identifier = ""

                try:
                    validator.validate(cedar_json, schema)
                except ValidationError as e:
                    error_file_name = os.path.join(json_dir, "error.log")
                    with open(error_file_name, "w") as errorfile:
                        errorfile.write(e.message)
                        errorfile.write(e.cause)

                #save output json
                if (inv_identifier):
                    file_name = os.path.join(json_dir,investigation_identifier+".json")
                else:
                    #print isa_tab.studies[0]
                    file_name = os.path.join(json_dir,study_identifier+".json")
                with open(file_name, "w") as outfile:
                    json.dump(cedar_json, outfile, indent=4, sort_keys=True)

                print("... conversion finished.")

    def createStudiesList(self, studies):
        json_list = []
        for study in studies:
            source_dict = self.createSources(study.nodes)
            sample_dict = self.createSamples(study.nodes)
            data_dict = self.createDataFiles(study.nodes)
            json_item = {
                "@id": "https://repo.metadatacenter.org/UUID{}".format(uuid4()),
                "@type": "https://repo.metadatacenter.org/model/Study",
                "title": {"_value": study.metadata['Study Title']},
                "description": {"_value": study.metadata['Study Description']},
                "identifier": {"_value": study.metadata['Study Identifier']},
                "submissionDate": {"_value": study.metadata['Study Submission Date']},
                "publicReleaseDate": {"_value": study.metadata['Study Public Release Date']},
                "studyDesignType": {"_value": ""},  #dict([("value", study.metadata['Study Public Design Type Accession Number'])]))
                "publication": self.createStudyPublicationsList(study.publications),
                "contact": self.createStudyContactsList(study.contacts),
                "studyFactor": self.createStudyFactorsList(study.factors),
                "studyAssay": self.createStudyAssaysList(study.assays),
                "studyGroupPopulation": self.createStudyGroupList(source_dict),
                "studyProtocol": self.createStudyProtocolList(study.protocols),
                "process": self.createProcessList(study.process_nodes, source_dict, sample_dict, data_dict)
            }
            json_list.append(json_item)
        return json_list

    def createStudyGroupList(self, source_dict):
         json_list = []
         json_item = {
                    "@id": "https://repo.metadatacenter.org/UUID{}".format(uuid4()),
                    "@type": "http://purl.obolibrary.org/obo/STATO_0000193",
                    "name": {"_value": "population name"},
                    "type": {"_value": "http://bioportal.bioontology.org/ontologies/EFO/3232"},
                    "selectionRule":  {"_value": "selection rule"},
                    "studySubject": list(source_dict.values())
                }
         json_list.append(json_item)
         return json_list


    def createProcessList(self, process_nodes, source_dict, sample_dict, data_dict):
        json_list = []
        for process_node_name in process_nodes:
            try:
                measurement_type = process_nodes[process_node_name].study_assay.metadata["Study Assay Measurement Type"]
            except:
                measurement_type = ""

            try:
                platform = process_nodes[process_node_name].study_assay.metadata["Study Assay Technology Platform"]
            except:
                platform = ""

            try:
                technology = process_nodes[process_node_name].study_assay.metadata["Study Assay Technology Type"]
            except:
                technology = ""

            process_node =  process_nodes[process_node_name]

            json_item = {
                    "@id": "https://repo.metadatacenter.org/UUID{}".format(uuid4()),
                    "@type": "https://repo.metadatacenter.org/model/Process",
                    "type": {"_value": process_node_name},
                    "studyProtocol": self.createExecuteStudyProtocol(process_node_name, process_node),
                    "studyAssay": [{ "@type": "http://purl.obolibrary.org/obo/BFO_0000055",
                                        "@id": "https://repo.metadatacenter.org/UUID",
                                        "measurementType": { "_value": measurement_type },
                                        "platform": { "_value": platform },
                                        "technology": { "_value": technology } }],
                    "input": self.createInputList(process_node.inputs, source_dict, sample_dict),
                    "output": self.createOutputList(process_node.outputs, sample_dict),
                    "parameterValue": self.createParameterValueList(process_node_name, process_node),
            }
            json_list.append(json_item)
        return json_list


    def createInputList(self, inputs, source_dict, sample_dict):
        json_dict = dict([])
        sample_list = []
        studySubject_list = []
        for argument in inputs:
            try:
                json_item = source_dict[argument]
                studySubject_list.append(json_item)
            except KeyError:
                pass
            try:
                json_item = sample_dict[argument]
                sample_list.append(json_item)
            except KeyError:
                pass
        json_dict["sample"] = sample_list
        json_dict["studySubject"] = studySubject_list
        return json_dict


    def createOutputList(self, arguments, sample_dict):
        json_dict = dict([])
        sample_list = []
        for argument in arguments:
            try:
                json_item = sample_dict[argument]
                sample_list.append(json_item)
            except KeyError:
                pass
        json_dict["sample"] = sample_list
        return json_dict


    def createExecuteStudyProtocol(self, process_node_name, process_node):
        json_item = {
                    "@context": {
                                "name": "https://metadatacenter.org/schemas/name",
                                "uRI": "https://metadatacenter.org/schemas/uRI",
                                "_value": "https://schema.org/value",
                                "version":  "https://metadatacenter.org/schemas/version",
                                "protocolParameter": "https://metadatacenter.org/schemas/protocolParameter",
                                "type":  "https://metadatacenter.org/schemas/type",
                                "description": "https://metadatacenter.org/schemas/description"
                    },
                    "name": {"_value": process_node_name},
                    "@id": "https://repo.metadatacenter.org/UUID{}".format(uuid4()),
                    "@type": "http://purl.obolibrary.org/obo/OBI_0000272",
                    "type": {"_value": "http://purl.obolibrary.org/obo/OBI_0000272"},
                    "description": {"_value": process_node_name},
                    "version": {"_value": process_node_name},
                    "uRI": {"_value": process_node_name},
                    "protocolParameter": self.createProtocolParameterFromNode(process_node)
                }

        return [ json_item ]


    def createProtocolParametersList(self, protocol):
        json_list = []
        parameters = protocol['Study Protocol Parameters Name']
        parametersURIs = protocol['Study Protocol Parameters Name Term Accession Number']
        index = 0
        if parameters:
            for parameter in parameters.split(';'):
                json_item = {
                    "name": {"_value": parameter},
                    "description": ( {"_value": parametersURIs[index] if len(parametersURIs)==len(parameters) else ""}),
                }
                index=index+1
                json_list.append(json_item)
        return json_list


    def createProtocolParameterFromNode(self, process_node):
        json_list = []
        json_item = {
            "description": {"_value": process_node.protocol},
            "name": {"_value": process_node.protocol},
        }
        json_list.append(json_item)
        return json_list

    def createParameterValueList(self, process_node_name, process_node):
        json_list = []
        for header in process_node.metadata:
            value_header = header.replace("]", "").split("[")[-1]
            value_attributes = process_node.metadata[header][0]
            value = value_attributes[0]
            if header.startswith("Parameter Value"):
                json_item = {
                    "@id": "https://repo.metadatacenter.org/UUID{}".format(uuid4()),
                    "@type": "https://repo.metadatacenter.org/model/ProtocolParameter",
                    "value": {"_value": value},
                    "protocolParameter": self.createProtocolParameterFromNode(process_node),
                    "type": {"_value": value_header},
                    "unit": {"_value": value_header},
                }
                json_list.append(json_item)
        return json_list


    def createDataFiles(self, nodes):
        json_dict = {}
        for node_index in nodes:
            if nodes[node_index].ntype.endswith("Data File") :
                json_item = {
                    "@id": "https://repo.metadatacenter.org/UUID{}".format(uuid4()),
                    "@type": "https://repo.metadatacenter.org/model/DataFile",
                    "name": {"_value": node_index},
                    "type": {"_value": "http://purl.obolibrary.org/obo/OBI_0000747"},
                    "description": {"_value": ""},
                }
                json_dict[node_index] = json_item
        return json_dict

    def createSamples(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype == "Sample Name":
                json_item = {
                    "@id": "https://repo.metadatacenter.org/UUID{}".format(uuid4()),
                    "@type": "https://repo.metadatacenter.org/model/Sample",
                    "name": {"_value": node_index},
                    "type": {"_value": "http://purl.obolibrary.org/obo/OBI_0000747"},
                    "description": {"_value": ""},
                    "source": {"_value": ""},
                    "factorValue": self.createFactorValueList(nodes[node_index]),
                    "studyTime": self.createStudyTimeCollection(),
                    "characteristic": self.createCharacteristicList(node_index, nodes[node_index]),
                }
                json_dict[node_index] = json_item
        return json_dict

    def createSources(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype == "Source Name":
                json_item = {
                    "name": {"_value": node_index},
                    "type": {"_value": "http://purl.obolibrary.org/obo/OBI_0000925"},
                    "characteristic": self.createCharacteristicList(node_index, nodes[node_index]),
                }
                json_dict[node_index] = json_item
        return json_dict


    def createStudyTimeCollection(self):
        json_item = {
                    "@id": "https://repo.metadatacenter.org/UUID{}".format(uuid4()),
                    "@type": "http://purl.obolibrary.org/obo/OBI_0001619",
                    "durationValue": {"_value": ""},
                    "isBeforeEvent": {"_value": ""},
                    "studyEvent": {"_value": ""},
                    "unit": {"_value": ""}
                  }
        return json_item


    def createCharacteristicList(self, node_name, node):
        json_list = []
        for header in node.metadata:
            if header.startswith("Characteristics"):
                 characteristic = header.replace("]", "").split("[")[-1]
                 json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/Characteristic"),
                    ("name", dict([("_value", characteristic)])),
                    ("description", dict([("_value", "")])),
                    ("characteristicValue", self.createCharacteristicValueList(node.metadata[header][0]))
                    ])
                 json_list.append(json_item)
        return json_list

    def createCharacteristicValueList(self, value_attributes):

        value  = value_attributes[0]
        try:
            typeValue = value_attributes.Term_Accession_Number
        except AttributeError:
            typeValue = ""

        try:
            unitValue = value_attributes.Unit
        except AttributeError:
            unitValue = ""

        if unitValue:
            characteristicValue = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://repo.metadatacenter.org/model/CharacteristicValue"),
                ("type", dict([("_value", "")])),
                ("unit", dict([("_value", unitValue), ("@type", typeValue)])),
                ("value", dict([("_value", value)]))
                ])
        else:
            characteristicValue = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://repo.metadatacenter.org/model/CharacteristicValue"),
                ("type", dict([("_value", typeValue)])),
                ("unit", dict([("_value", unitValue)])),
                ("value", dict([("_value", value)]))
                ])

        return characteristicValue


    def createFactorValueList(self, node):
        factor_list = []
        for header in node.metadata:
            if header.startswith("Factor Value"):
                 value_header = header.replace("]", "").split("[")[-1]
                 value_attributes = node.metadata[header][0]
                 value  = value_attributes[0]
                 try:
                    unit = value_attributes.Unit
                 except AttributeError:
                     unit = ""
                 factorValue = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/CharacteristicValue"),
                    ("type", dict([("_value", value_header)])),
                    ("unit", dict([("_value", unit), ("@type", "")])),
                    ("value", dict([("_value", value)])),
                    ("studyFactor", [ self.createStudyFactor("", "") ] )
                    ])
                 factor_list.append(factorValue)
        return factor_list


    def createInvestigationContactsList(self, contacts):
        json_list = []
        for contact in contacts:
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://repo.metadatacenter.org/model/Contact"),
                ("lastName", dict([("_value", contact['Investigation Person Last Name'])])),
                ("firstName", dict([("_value", contact['Investigation Person First Name'])])),
                ("middleInitial", dict([("_value", contact['Investigation Person Mid Initials'])])),
                ("email", dict([("_value", contact['Investigation Person Email'])])),
                ("phone", dict([("_value", contact['Investigation Person Phone'])])),
                ("fax", dict([("_value", contact['Investigation Person Fax'])])),
                ("address", dict([("_value", contact['Investigation Person Address'])])),
                ("role", dict([("_value", contact['Investigation Person Roles Term Accession Number'])])),
                ("organization", self.createAffiliationsList(contact['Investigation Person Affiliation']))
                ])
            json_list.append(json_item)
        return json_list

    def createStudyContactsList(self, contacts):
        json_list = []
        for contact in contacts:
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://repo.metadatacenter.org/model/Contact"),
                ("lastName", dict([("_value", contact['Study Person Last Name'])])),
                ("firstName", dict([("_value", contact['Study Person First Name'])])),
                ("middleInitial", dict([("_value", contact['Study Person Mid Initials'])])),
                ("email", dict([("_value", contact['Study Person Email'])])),
                ("phone", dict([("_value", contact['Study Person Phone'])])),
                ("fax", dict([("_value", contact['Study Person Fax'])])),
                ("address", dict([("_value", contact['Study Person Address'])])),
                ("role", dict([("_value", contact['Study Person Roles Term Accession Number'])])),
                ("organization", self.createAffiliationsList(contact['Study Person Affiliation']))
                ])
            json_list.append(json_item)
        return json_list

    def createInvestigationPublicationsList(self, publications):
        json_list = []
        for publication in publications:
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://repo.metadatacenter.org/model/Publication"),
                ("title", dict([("_value", publication['Investigation Publication Title'])])),
                ("pubMedID", dict([("_value", publication['Investigation PubMed ID'])])),
                ("dOI", dict([("_value", publication['Investigation Publication DOI'])])),
                ("authorList", self.createAuthorList(publication['Investigation Publication Author List'])),
                ("status", dict([("_value", publication['Investigation Publication Status'])])),
                ])
            json_list.append(json_item)
        return json_list

    def createStudyPublicationsList(self, publications):
        json_list = []
        for publication in publications:
            #print publication
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://repo.metadatacenter.org/model/Publication"),
                ("title", dict([("_value", publication['Study Publication Title'])])),
                ("pubMedID", dict([("_value", publication['Study PubMed ID'])])),
                ("dOI", dict([("_value", publication['Study Publication DOI'])])),
                ("authorList", self.createAuthorList(publication['Study Publication Author List'])),
                ("status", dict([("_value", publication['Study Publication Status'])])),
                ])
            json_list.append(json_item)
        return json_list

    def createAffiliationsList(self, affiliations):
        json_list = []
        json_item = dict([
                ("@context", ""),
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://metadatacenter.org/model/Organization"),
                ("name", dict([("_value", affiliations)])),
                ("department", dict([("_value", "")]))
                ])
        json_list.append(json_item)
        return json_list

    def createStudyAssaysList(self, assays):
        json_list = []
        for assay in assays:
            json_item = {
                "@id": "https://repo.metadatacenter.org/UUID{}".format(uuid4()),
                "@type": "http://purl.obolibrary.org/obo/BFO_0000055",
                "measurementType": {"_value": assay.metadata['Study Assay Measurement Type Term Accession Number']},
                "platform": {"_value": assay.metadata['Study Assay Technology Platform']},
                "technology": {"_value": assay.metadata['Study Assay Technology Type']},
                }
            json_list.append(json_item)
        return json_list

    def createStudyProtocolList(self, protocols):
        json_list = []
        for protocol in protocols:
            #print protocol
            json_item = {
                "@id": "https://repo.metadatacenter.org/UUID{}".format(uuid4()),
                "@type": "https://repo.metadatacenter.org/model/StudyProtocol",
                "name": {"_value": protocol['Study Protocol Name']},
                "description": {"_value": protocol['Study Protocol Description']},
                "type": {"_value": protocol['Study Protocol Type']},
                "version": {"_value": protocol['Study Protocol Version']},
                "uRI": {"_value": protocol['Study Protocol URI']},
                "protocolParameter": self.createProtocolParametersList(protocol),
                }
            json_list.append(json_item)
        return json_list

    def createStudyFactor(self, factor_name, factor_desc):
         json_item = {
                "@id": "https://repo.metadatacenter.org/UUID{}".format(uuid4()),
                "@context": "",
                "@type": "http://www.ebi.ac.uk/efo/EFO_0000001",
                "name": {"_value": factor_name},
                "description": {"_value": factor_desc}
                #"description": ""
            }
         return json_item

    def createStudyFactorsList(self, factors):
        #print factors
        json_list = []
        for factor in factors:
             json_item = self.createStudyFactor(factor['Study Factor Name'], factor['Study Factor Type'])
             json_list.append(json_item)
        return json_list

    def createAuthorList(self, authorListString):
        json_list = []
        elements = authorListString.split(',')
        for element in elements:
            json_item = dict([
                ("_value", element)
            ])
            json_list.append(json_item)
        return json_list
