__author__ = 'agbeltran'

import json
import os
from uuid import uuid4
from os import listdir
from os.path import isdir, join
from jsonschema import RefResolver, Draft4Validator

#from bcbio.isatab.parser import InvestigationParser
from isatools.io.isatab_parser import parse
#from isatab_parser_orig import parse

CEDAR_SCHEMA_PATH = join(os.path.dirname(os.path.realpath(__file__)), "../schemas/cedar")

class ISATab2CEDAR():

    def __init__(self, primary_source):
        self.primary_source = primary_source

    def createCEDARjson_folder(self, work_dir, json_dir, inv_identifier):
        print("Convert ISA datasets in folder ", work_dir)
        path = os.path.abspath(work_dir)
        folders = [ f for f in listdir(path) if isdir(join(path,f))]

        for folder in folders:
            self.createCEDARjson(CEDAR_SCHEMA_PATH, join(path,folder), json_dir, inv_identifier)


    def createCEDARjson(self, work_dir, json_dir, inv_identifier):
        print("Converting ISA to CEDAR model for ", work_dir)
        schema_file = "investigation_template.json"
        schema = json.load(open(join(CEDAR_SCHEMA_PATH,schema_file)))
        resolver = RefResolver('file://'+join(CEDAR_SCHEMA_PATH, schema_file), schema)
        validator = Draft4Validator(schema, resolver=resolver)

        isa_tab = parse(work_dir)
        #print(isa_tab)

        if isa_tab is None:
            print("No ISAtab dataset found")
        else:
                if isa_tab.metadata != {}:
                    investigationObject = dict([
                        ("schemaID", "https://repo.metadatacenter.org/UUID"),
                        ("@id", "https://repo.metadatacenter.org/UUID/"+str(uuid4())),
                        ("@type", "https://repo.metadatacenter.org/model/Investigation"),
                        ("@context", dict(
                            [
                                ("model", "https://repo.metadatacenter.org/model/"),
                                ("xsd", "http://www.w3.org/2001/XMLSchema"),
                                ("schema", "https://schema.org/"),
                                ("title", "https://repo.metadatacenter.org/model/title"),
                                ("description", "https://repo.metadatacenter.org/model/description")
                            ]
                        )),
                        ("title", dict([ ("_value", isa_tab.metadata['Investigation Title'])])),
                        ("description", dict([ ("_value", isa_tab.metadata['Investigation Description'])])),
                        ("identifier", dict([ ("_value", isa_tab.metadata['Investigation Identifier'])])),
                        ("submissionDate", dict([ ("_value", isa_tab.metadata['Investigation Submission Date'])])),
                        ("publicReleaseDate", dict([ ("_value", isa_tab.metadata['Investigation Public Release Date'])])),
                        ("study", self.createStudiesList(isa_tab.studies)),
                        ("contact", self.createInvestigationContactsList(isa_tab.contacts)),
                        ("publication", self.createInvestigationPublicationsList(isa_tab.publications)),
                        ("provenance", dict([
                            ("wasGeneratedBy", "http://www.isa-tools.org"),
                            ("hadPrimarySource", self.primary_source)
                        ]))
                    ])
                else:
                    investigationObject = dict([
                        ("schemaID", "https://repo.metadatacenter.org/UUID"),
                        ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                        ("@type", "https://repo.metadatacenter.org/model/Investigation"),
                        ("@context", dict(
                            [
                                ("model", "https://repo.metadatacenter.org/model/"),
                                ("xsd", "http://www.w3.org/2001/XMLSchema"),
                                ("schema", "https://schema.org/"),
                                ("title", "https://repo.metadatacenter.org/model/title"),
                                ("description", "https://repo.metadatacenter.org/model/description")
                            ]
                        )),
                        ("title", dict([ ("_value", "")])),
                        ("description", dict([ ("_value", "")])),
                        ("identifier", dict([ ("_value", "")])),
                        ("submissionDate", dict([ ("_value", "")])),
                        ("publicReleaseDate", dict([ ("_value", "")])),
                        ("study", self.createStudiesList(isa_tab.studies)),
                        ("contact", self.createInvestigationContactsList(isa_tab.contacts)),
                        ("publication", self.createInvestigationPublicationsList(isa_tab.publications))
                    ])

                cedar_json = dict([
                    ("investigation",investigationObject)
                ])

                validator.validate(cedar_json, schema)

                #save output json
                if (inv_identifier):
                    file_name = os.path.join(json_dir,isa_tab.metadata['Investigation Identifier']+".json")
                else:
                    #print isa_tab.studies[0]
                    file_name = os.path.join(json_dir,isa_tab.studies[0].metadata['Study Identifier']+".json")
                with open(file_name, "w") as outfile:
                    json.dump(cedar_json, outfile, indent=4, sort_keys=True)
                    outfile.close()
                print("... conversion finished.")

    def createStudiesList(self, studies):
        json_list = []
        for study in studies:
            source_dict = self.createSources(study.nodes)
            sample_dict = self.createSamples(study.nodes)
            data_dict = self.createDataFiles(study.nodes)
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://repo.metadatacenter.org/model/Study"),
                ("title", dict([("_value", study.metadata['Study Title'])])),
                ("description", dict([("_value", study.metadata['Study Description'])])),
                ("identifier", dict([("_value", study.metadata['Study Identifier'])])),
                ("submissionDate", dict([("_value", study.metadata['Study Submission Date'])])),
                ("publicReleaseDate", dict([("_value", study.metadata['Study Public Release Date'])])),
                ("studyDesignType", dict([("_value", "")])),  #dict([("value", study.metadata['Study Public Design Type Accession Number'])]))
                ("publication", self.createStudyPublicationsList(study.publications)),
                ("contact", self.createStudyContactsList(study.contacts)),
                ("studyFactor", self.createStudyFactorsList(study.factors)),
                ("studyAssay", self.createStudyAssaysList(study.assays)),
                ("studyGroupPopulation", self.createStudyGroupList(source_dict)),
                ("studyProtocol", self.createStudyProtocolList(study.protocols)),
                ("process", self.createProcessList(study.process_nodes, source_dict, sample_dict, data_dict))
            ])
            json_list.append(json_item)
        return json_list

    def createStudyGroupList(self, source_dict):
         json_list = []
         json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/StudyGroupPopulation"),
                    ("name", dict([("_value", "population name")])),
                    ("type", dict([("_value", "http://bioportal.bioontology.org/ontologies/EFO/3232")])),
                    ("selectionRule",  dict([("_value", "selection rule")])),
                    ("studySubject", list(source_dict.values()))
                ])
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

            json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/Process"),
                    ("type", dict([("_value", process_node_name)])),
                    ("executeStudyProtocol", self.createExecuteStudyProtocol(process_node_name, process_nodes[process_node_name])),
                    ("studyAssay", { "@type": "https://repo.metadatacenter.org/model/StudyAssay",
                                        "@id": "https://repo.metadatacenter.org/UUID",
                                        "measurementType": { "_value": measurement_type },
                                        "platform": { "_value": platform },
                                        "technology": { "_value": technology } }),
                    ("input", self.createInputList(process_nodes[process_node_name].inputs, source_dict, sample_dict)),
                    ("output", self.createOutputList(process_nodes[process_node_name].outputs, sample_dict) )
            ])
            json_list.append(json_item)
        return json_list


    def createInputList(self, inputs, source_dict, sample_dict):
        json_list = []
        for argument in inputs:
            try:
                json_item = source_dict[argument]
                json_list.append(json_item)
            except KeyError:
                pass
            try:
                json_item = sample_dict[argument]
                json_list.append(json_item)
            except KeyError:
                pass
        return json_list


    def createOutputList(self, arguments, sample_dict):
        json_list = []
        for argument in arguments:
            try:
                json_item = sample_dict[argument]
                json_list.append(json_item)
            except KeyError:
                pass
        return json_list


    def createExecuteStudyProtocol(self, process_node_name, process_node):
        json_item = dict([
                    ("name", dict([("_value", process_node_name)])),
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "http://purl.obolibrary.org/obo/OBI_0000272"),
                    ("type", dict([("_value", "http://purl.obolibrary.org/obo/OBI_0000272")])),
                    ("description", dict([("_value", process_node_name)])),
                    ("version", dict([("_value", process_node_name)])),
                    ("uri", dict([("_value", process_node_name)])),
                    ("protocolParameter", self.createProcessParameterList(process_node_name, process_node))
                ])

        return json_item


    def createProcessParameterList(self, process_node_name, process_node):
        json_list = []
        json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/ProtocolParameter"),
                    ("name", dict([("_value", process_node_name )])),
                    ("description", dict([("_value", "")])),
                ])
        json_list.append(json_item)
        return json_list


    def createDataFiles(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype.endswith("Data File") :
                json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/DataFile"),
                    ("name", dict([("_value", node_index)])),
                    ("type", dict([("_value", "http://purl.obolibrary.org/obo/OBI_0000747")])),
                    ("description", dict([("_value", "")]))
                ])
                json_dict.update({node_index: json_item})
        return json_dict

    def createSamples(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype == "Sample Name":
                json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/Sample"),
                    ("name", dict([("_value", node_index)])),
                    ("type", dict([("_value", "http://purl.obolibrary.org/obo/OBI_0000747")])),
                    ("description", dict([("_value", "")])),
                    ("source", dict([("_value", "")])),
                    ("hasFactorValue", []),
                    ("hasCollectionStudyTime", self.createStudyTimeCollection()),
                    ("hasCharacteristic", self.createCharacteristicList(node_index, nodes[node_index])),
                ])
                json_dict.update({node_index: json_item})
        return json_dict

    def createSources(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype == "Source Name":
                json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/StudySubject"),
                    ("name", dict([("_value", node_index)])),
                    ("type", dict([("_value", "http://purl.obolibrary.org/obo/OBI_0000925")])),
                    ("hasCharacteristic", self.createCharacteristicList(node_index, nodes[node_index])),
                ])
                json_dict.update({node_index: json_item})
        return json_dict


    def createStudyTimeCollection(self):
        json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/StudyTime"),
                    ("durationValue", dict([("_value", 0)])),
                    ("isBeforeEvent", dict([("_value", False)])),
                    ("studyEvent", dict([("_value", "")])),
                    ("unit", dict([("_value", "")]))
                  ])
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
                ("affiliation", self.createAffiliationsList(contact['Investigation Person Affiliation']))
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
                ("affiliation", self.createAffiliationsList(contact['Study Person Affiliation']))
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
                ("doi", dict([("_value", publication['Investigation Publication DOI'])])),
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
                ("doi", dict([("_value", publication['Study Publication DOI'])])),
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
                ("@type", "https://repo.metadatacenter.org/model/Organization"),
                ("name", dict([("_value", affiliations)])),
                ("department", dict([("_value", "")]))
                ])
        json_list.append(json_item)
        return json_list

    def createStudyAssaysList(self, assays):
        json_list = []
        for assay in assays:
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://repo.metadatacenter.org/model/StudyAssay"),
                ("measurementType", dict([("_value", assay.metadata['Study Assay Measurement Type Term Accession Number'])])),
                ("platform", dict([("_value", assay.metadata['Study Assay Technology Platform'])])),
                ("technology", dict([("_value", assay.metadata['Study Assay Technology Type'])]))
                ])
            json_list.append(json_item)
        return json_list

    def createStudyProtocolList(self, protocols):
        json_list = []
        for protocol in protocols:
            #print protocol
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://repo.metadatacenter.org/model/StudyProtocol"),
                ("name", dict([("_value", protocol['Study Protocol Name'])])),
                ("description", dict([("_value", protocol['Study Protocol Description'])])),
                ("type", dict([("_value", protocol['Study Protocol Type'])])),
                ("version", dict([("_value", protocol['Study Protocol Version'])])),
                ("uri", dict([("_value", protocol['Study Protocol URI'])])),
                ("protocolParameter", self.createProtocolParametersList(protocol)),
                ])
            json_list.append(json_item)
        return json_list

    def createProtocolParametersList(self, protocol):
        json_list = []
        parameters = protocol['Study Protocol Parameters Name']
        parametersURIs = protocol['Study Protocol Parameters Name Term Accession Number']
        index = 0
        if len(parameters) > 0:
            for parameter in parameters.split(';'):
                json_item = dict([
                      ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/ProtocolParameter"),
                    ("name", dict([("_value", parameter)])),
                    ("description", (dict([("_value", parametersURIs[index] if (len(parametersURIs) == len(parameters)) else "")]))),
                ])
                index=index+1
                json_list.append(json_item)
        return json_list

    def createStudyFactorsList(self, factors):
        #print factors
        json_list = []
        for factor in factors:
             json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@context", ""),
                ("@type", "https://repo.metadatacenter.org/model/StudyFactor"),
                ("name", dict([("_value", factor['Study Factor Name'])])),
                ("description", dict([("_value", factor['Study Factor Type'])]))
                #("description", "")

            ])
             json_list.append(json_item)
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



#local tests
#isa2cedar = ISATab2CEDAR("Metabolights")
#isa2cedar.createCEDARjson("../../tests/data/BII-I-1", "./schemas/cedar", True)
#isa2cedar.createCEDARjson("../../tests/datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS114", "../../tests/datasets/metabolights", False)
#isa2cedar.createCEDARjson("../../tests/datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS1", "../../tests/datasets/metabolights", False)
#isa2cedar.createCEDARjson("../../tests/datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS10", "../../tests/datasets/metabolights", False)
#isa2cedar.createCEDARjson("../../tests/datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS161", "../../tests/datasets/metabolights", False)
#isa2cedar.createCEDARjson_folder("../../tests/datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/", "../../tests/datasets/metabolights", False)

