__author__ = 'agbeltran'

import json
import os
from uuid import uuid4
from os import listdir
from os.path import isdir, join

import warlock

#from bcbio.isatab.parser import InvestigationParser
from isatools.io.isatab_parser import parse
#from isatab_parser_orig import parse

CEDAR_SCHEMA_PATH = join(os.path.dirname(os.path.realpath(__file__)), "../schemas/cedar")

class ISATab2CEDAR():

    def createCEDARjson_folder(self, work_dir, json_dir, inv_identifier):
        print "Convert ISA datasets in folder ", work_dir
        path = os.path.abspath(work_dir)
        folders = [ f for f in listdir(path) if isdir(join(path,f))]

        for folder in folders:
            self.createCEDARjson(CEDAR_SCHEMA_PATH, join(path,folder), json_dir, inv_identifier)


    def createCEDARjson(self, work_dir, json_dir, inv_identifier):
        print "Converting ISA to CEDAR model for ", work_dir
        schema_file = "InvestigationSchema.json"
        schema = json.load(open(join(CEDAR_SCHEMA_PATH,schema_file)))
        CEDARSchema = warlock.model_factory(schema)

        isa_tab = parse(work_dir)
        #print isa_tab

        if isa_tab is None:
            print "No ISAtab dataset found"
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
                        ("title", dict([ ("value", isa_tab.metadata['Investigation Title'])])),
                        ("description", dict([ ("value", isa_tab.metadata['Investigation Description'])])),
                        ("identifier", dict([ ("value", isa_tab.metadata['Investigation Identifier'])])),
                        ("submissionDate", dict([ ("value", isa_tab.metadata['Investigation Submission Date'])])),
                        ("publicReleaseDate", dict([ ("value", isa_tab.metadata['Investigation Public Release Date'])])),
                        ("hasStudy", self.createStudiesList(isa_tab.studies)),
                        ("hasContact", self.createInvestigationContactsList(isa_tab.contacts)),
                        ("hasPublication", self.createInvestigationPublicationsList(isa_tab.publications))
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
                        ("title", dict([ ("value", "")])),
                        ("description", dict([ ("value", "")])),
                        ("identifier", dict([ ("value", "")])),
                        ("submissionDate", dict([ ("value", "")])),
                        ("publicReleaseDate", dict([ ("value", "")])),
                        ("hasStudy", self.createStudiesList(isa_tab.studies)),
                        ("hasContact", self.createInvestigationContactsList(isa_tab.contacts)),
                        ("hasPublication", self.createInvestigationPublicationsList(isa_tab.publications))
                    ])

                cedar_json = CEDARSchema(
                    investigation=investigationObject
                )

                #save output json
                if (inv_identifier):
                    file_name = os.path.join(json_dir,isa_tab.metadata['Investigation Identifier']+".json")
                else:
                    #print isa_tab.studies[0]
                    file_name = os.path.join(json_dir,isa_tab.studies[0].metadata['Study Identifier']+".json")
                with open(file_name, "w") as outfile:
                    json.dump(cedar_json, outfile, indent=4, sort_keys=True)
                    outfile.close()
                print "... conversion finished."

    def createStudiesList(self, studies):
        json_list = []
        for study in studies:
            source_dict = self.createStudySubjectDictionary(study.nodes)
            sample_dict = self.createSampleDictionary(study.nodes)
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://repo.metadatacenter.org/model/Study"),
                ("title", dict([("value", study.metadata['Study Title'])])),
                ("description", dict([("value", study.metadata['Study Description'])])),
                ("identifier", dict([("value", study.metadata['Study Identifier'])])),
                ("submissionDate", dict([("value", study.metadata['Study Submission Date'])])),
                ("publicReleaseDate", dict([("value", study.metadata['Study Public Release Date'])])),
                ("studyDesignType", dict([("value", "")])),  #dict([("value", study.metadata['Study Public Design Type Accession Number'])]))
                ("hasPublication", self.createStudyPublicationsList(study.publications)),
                ("hasContact", self.createStudyContactsList(study.contacts)),
                ("hasStudyFactor", self.createStudyFactorsList(study.factors)),
                ("hasStudyAssay", self.createStudyAssaysList(study.assays)),
                ("hasStudyGroupPopulation", self.createStudyGroupList(source_dict)),
                #REMOVED FROM SCHEMA, ONLY AVAILABLE IN STUDY GROUP POPULATION NOW - ("hasStudySubject", source_dict.values()),
                ("hasStudyProtocol", self.createStudyProtocolList(study.protocols)),
                ("hasProcess", self.createProcessList(study.process_nodes, source_dict, sample_dict))
            ])
            json_list.append(json_item)
        return json_list

    def createStudyGroupList(self, source_dict):
         json_list = []
         json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/StudyGroupPopulation"),
                    ("name", dict([("value", "population name")])),
                    ("type", dict([("value", "http://bioportal.bioontology.org/ontologies/EFO/3232")])),
                    ("selectionRule",  dict([("value", "selection rule")])),
                    ("hasStudySubject", source_dict.values())
                ])
         json_list.append(json_item)
         return json_list


    def createProcessList(self, process_nodes, source_dict, sample_dict):
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
                    ("type", dict([("value", process_node_name)])),
                    ("executeStudyProtocol", self.createExecuteStudyProtocol(process_node_name, process_nodes[process_node_name])),
                    ("hasStudyAssay", { "@type": "https://repo.metadatacenter.org/model/StudyAssay",
                                        "@id": "https://repo.metadatacenter.org/UUID",
                                        "measurementType": { "value": measurement_type },
                                        "platform": { "value": platform },
                                        "technology": { "value": technology } }),
                    ("hasInput", self.createInputOutputList(process_nodes[process_node_name].inputs, source_dict, sample_dict)),
                    ("hasOutput", self.createInputOutputList(process_nodes[process_node_name].outputs, source_dict, sample_dict) )
            ])
            json_list.append(json_item)
        return json_list

    def createInputOutputList(self, arguments, source_dict, sample_dict):
        json_list = []
        for argument in arguments:
            try:
                json_item = source_dict[argument]
                json_list.append(json_item)
            except KeyError:
                json_item = sample_dict[argument]
                json_list.append(json_item)
        return json_list


    def createExecuteStudyProtocol(self, process_node_name, process_node):
        json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/StudyProtocol"),
                    ("name", dict([("value", process_node_name)])),
                    ("type", dict([("value", "http://purl.obolibrary.org/obo/OBI_0000715")])),
                    ("description", dict([("value", process_node_name)])),
                    ("version", dict([("value", process_node_name)])),
                    ("uri", dict([("value", process_node_name)])),
                    ("hasProtocolParameter", self.createProcessParameterList(process_node_name, process_node))
                ])

        return json_item


    def createProcessParameterList(self, process_node_name, process_node):
        json_list = []
        json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/ProtocolParameter"),
                    ("name", dict([("value", process_node_name )])),
                    ("description", dict([("value", "")])),
                ])
        json_list.append(json_item)
        return json_list


    def createSampleDictionary(self, nodes):
        json_dict = dict([])
        #print "nodes ", nodes
        for node_name in nodes:
            #print "node_name ", node_name
            #print "node ", nodes[node_name]
            if nodes[node_name].ntype == "Sample Name":
                json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/Sample"),
                    ("name", dict([("value", node_name)])),
                    ("type", dict([("value", "http://purl.obolibrary.org/obo/OBI_0000747")])),
                    ("description", dict([("value", "")])),
                    ("source", dict([("value", "")])),
                    ("hasFactorValue", []),
                    ("hasCollectionStudyTime", self.createStudyTimeCollection()),
                    ("hasCharacteristic", self.createCharacteristicList(node_name, nodes[node_name])),
                ])
                json_dict.update({node_name: json_item})
        return json_dict


    def createStudyTimeCollection(self):
        json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/StudyTime"),
                    ("durationValue", dict([("value", 0)])),
                    ("isBeforeEvent", dict([("value", False)])),
                    ("studyEvent", dict([("value", "")])),
                    ("unit", dict([("value", "")]))
                  ])
        return json_item


    def createStudySubjectDictionary(self, nodes):
        json_dict = dict([])
        for node_name in nodes:
            if nodes[node_name].ntype == "Source Name":
                json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/StudySubject"),
                    ("name", dict([("value", node_name)])),
                    ("type", dict([("value", "http://purl.obolibrary.org/obo/OBI_0000925")])),
                    ("hasCharacteristic", self.createCharacteristicList(node_name, nodes[node_name])),
                ])
                json_dict.update({node_name: json_item})
        return json_dict

    def createCharacteristicList(self, node_name, node):
        json_list = []
        for header in node.metadata:
            if header.startswith("Characteristics"):
                 characteristic = header.replace("]", "").split("[")[-1]
                 json_item = dict([
                    ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                    ("@type", "https://repo.metadatacenter.org/model/Characteristic"),
                    ("name", dict([("value", characteristic)])),
                    ("description", dict([("value", "")])),
                    ("hasCharacteristicValue", self.createCharacteristicValueList(node.metadata[header]))
                    ])
                 json_list.append(json_item)
        return json_list

    def createCharacteristicValueList(self, characteristicValues):
        #TODO - check how to represent more than one characteristics value
        characteristicValue = dict([
                                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                                ("@type", "https://repo.metadatacenter.org/model/CharacteristicValue"),
                                ("type", dict([("value", characteristicValues[0][2])])),
                                ("unit", dict([("value", "")])),
                                ("value", dict([("value", characteristicValues[0][0])]))
                    ])
        return characteristicValue


    def createInvestigationContactsList(self, contacts):
        json_list = []
        for contact in contacts:
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
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

    def createStudyContactsList(self, contacts):
        json_list = []
        for contact in contacts:
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://repo.metadatacenter.org/model/Contact"),
                ("lastName", dict([("value", contact['Study Person Last Name'])])),
                ("firstName", dict([("value", contact['Study Person First Name'])])),
                ("middleInitial", dict([("value", contact['Study Person Mid Initials'])])),
                ("email", dict([("value", contact['Study Person Email'])])),
                ("phone", dict([("value", contact['Study Person Phone'])])),
                ("fax", dict([("value", contact['Study Person Fax'])])),
                ("address", dict([("value", contact['Study Person Address'])])),
                ("role", dict([("value", contact['Study Person Roles Term Accession Number'])])),
                ("hasAffiliation", self.createAffiliationsList(contact['Study Person Affiliation']))
                ])
            json_list.append(json_item)
        return json_list

    def createInvestigationPublicationsList(self, publications):
        json_list = []
        for publication in publications:
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://repo.metadatacenter.org/model/Publication"),
                ("title", dict([("value", publication['Investigation Publication Title'])])),
                ("pubMedID", dict([("value", publication['Investigation PubMed ID'])])),
                ("doi", dict([("value", publication['Investigation Publication DOI'])])),
                ("authorList", self.createAuthorList(publication['Investigation Publication Author List'])),
                ("status", dict([("value", publication['Investigation Publication Status'])])),
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
                ("title", dict([("value", publication['Study Publication Title'])])),
                ("pubMedID", dict([("value", publication['Study PubMed ID'])])),
                ("doi", dict([("value", publication['Study Publication DOI'])])),
                ("authorList", self.createAuthorList(publication['Study Publication Author List'])),
                ("status", dict([("value", publication['Study Publication Status'])])),
                ])
            json_list.append(json_item)
        return json_list

    def createAffiliationsList(self, affiliations):
        json_list = []
        json_item = dict([
                ("@context", ""),
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://repo.metadatacenter.org/model/Organization"),
                ("name", dict([("value", affiliations)])),
                ("department", dict([("value", "")]))
                ])
        json_list.append(json_item)
        return json_list

    def createStudyAssaysList(self, assays):
        json_list = []
        for assay in assays:
            json_item = dict([
                ("@id", "https://repo.metadatacenter.org/UUID"+str(uuid4())),
                ("@type", "https://repo.metadatacenter.org/model/StudyAssay"),
                ("measurementType", dict([("value", assay.metadata['Study Assay Measurement Type Term Accession Number'])])),
                ("platform", dict([("value", assay.metadata['Study Assay Technology Platform'])])),
                ("technology", dict([("value", assay.metadata['Study Assay Technology Type'])]))
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
                ("name", dict([("value", protocol['Study Protocol Name'])])),
                ("description", dict([("value", protocol['Study Protocol Description'])])),
                ("type", dict([("value", protocol['Study Protocol Type'])])),
                ("version", dict([("value", protocol['Study Protocol Version'])])),
                ("uri", dict([("value", protocol['Study Protocol URI'])])),
                ("hasProtocolParameter", self.createProtocolParametersList(protocol)),
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
                    ("name", dict([("value", parameter)])),
                    ("description", (dict([("value", parametersURIs[index] if (len(parametersURIs) == len(parameters)) else "")]))),
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
                ("name", dict([("value", factor['Study Factor Name'])])),
                ("description", dict([("value", factor['Study Factor Type'])]))
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
#isa2cedar = ISATab2CEDAR()
#isa2cedar.createCEDARjson("../../tests/data/BII-I-1", "./schemas/cedar", True)
#isa2cedar.createCEDARjson("../../tests/datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS1", "../../tests/datasets/metabolights", False)
#isa2cedar.createCEDARjson("../../tests/datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS161", "../../tests/datasets/metabolights", False)
#isa2cedar.createCEDARjson_folder("../../tests/datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/", "../../tests/datasets/metabolights", False)

