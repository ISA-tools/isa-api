__author__ = 'agbeltran'

import json
import os
from uuid import uuid4
from os import listdir
from os.path import isdir, join
import warlock

from isatools.io.isatab_parser import parse
from jsonschema import RefResolver, Draft4Validator

SCHEMAS_PATH = join(os.path.dirname(os.path.realpath(__file__)), "../schemas/isa_model_version_1_0_schemas/core/")
INVESTIGATION_SCHEMA = "investigation_schema.json"

class ISATab2ISAjson_v1():

    def __init__(self):
        pass

    def convert(self, work_dir, json_dir, inv_identifier):
        """Convert an ISA-Tab dataset (version 1) to JSON provided the ISA model v1.0 JSON Schemas
            :param work_dir: directory containing the ISA-tab dataset
            :param json_dir: output directory where the resulting json file will be saved
        """
        print("Converting ISAtab to ISAjson for ", work_dir)

        isa_tab = parse(work_dir)

        if isa_tab is None:
            print("No ISAtab dataset found")
        else:
                if isa_tab.metadata != {}:
                    #print("isa_tab.metadata->",isa_tab.metadata)
                    isa_json = dict([
                        ("identifier",isa_tab.metadata['Investigation Identifier']),
                        ("title", isa_tab.metadata['Investigation Title']),
                        ("description",isa_tab.metadata['Investigation Description']),
                        ("submissionDate", isa_tab.metadata['Investigation Submission Date']),
                        ("publicReleaseDate", isa_tab.metadata['Investigation Public Release Date']),
                        ("commentCreatedWithConfiguration", self.createComment('Created With Configuration',isa_tab.metadata['Comment[Created With Configuration]'])),
                        ("commentLastOpenedWithConfiguration", self.createComment('Last Opened With Configuration', isa_tab.metadata['Comment[Last Opened With Configuration]'])),
                        ("ontologySourceReferences", self.createOntologySourceReferences(isa_tab.ontology_refs)),
                        ("publications", self.createPublications(isa_tab.publications, "Investigation")),
                        ("people", self.createContacts(isa_tab.contacts, "Investigation")),
                        ("studies", self.createStudies(isa_tab.studies))
                    ])

                if (inv_identifier):
                    file_name = os.path.join(json_dir,isa_tab.metadata['Investigation Identifier']+".json")
                else:
                    file_name = os.path.join(json_dir,isa_tab.studies[0].metadata['Study Identifier']+".json")

                #validate json
                schema = json.load(open(join(SCHEMAS_PATH, INVESTIGATION_SCHEMA)))
                resolver = RefResolver('file://'+join(SCHEMAS_PATH, INVESTIGATION_SCHEMA), schema)
                validator = Draft4Validator(schema, resolver=resolver)
                validator.validate(isa_json, schema)

                with open(file_name, "w") as outfile:
                    json.dump(isa_json, outfile, indent=4, sort_keys=True)
                    outfile.close()
                print("... conversion finished.")


    def createComment(self, name, value):
        comment_json = dict([
            ("name", name),
            ("value", value)
        ])
        return comment_json

    def createContacts(self, contacts, inv_or_study):
        people_json = []
        for contact in contacts:
            person_json = dict([
                ("lastName", contact[inv_or_study+" Person Last Name"]),
                ("firstName", contact[inv_or_study+" Person First Name"]),
                ("midInitials", contact[inv_or_study+" Person Mid Initials"]),
                ("email", contact[inv_or_study+" Person Email"]),
                ("phone", contact[inv_or_study+" Person Phone"]),
                ("fax", contact[inv_or_study+" Person Fax"]),
                ("address", contact[inv_or_study+" Person Address"]),
                ("affiliation", contact[inv_or_study+" Person Affiliation"]),
                ("roles", [])
            ])
            people_json.append(person_json)
        return people_json


    def createPublications(self, publications, inv_or_study):
        publications_json = []
        for pub in publications:
            publication_json = dict([
                ("pubMedID", pub[inv_or_study+' PubMed ID']),
                ("doi", pub[inv_or_study+' Publication DOI']),
                ("authorList", pub[inv_or_study+' Publication Author List']),
                ("title", pub[inv_or_study+' Publication Title']),
                ("status", self.createOntologyAnnotationForInvOrStudy(pub, inv_or_study, " Publication Status"))
            ]
            )
            publications_json.append(publication_json)
        return publications_json

    def createProtocols(self, protocols):
        protocols_json = []
        for protocol in protocols:
            protocol_json = dict([
                ("name", protocol['Study Protocol Name']),
                ("protocolType", self.createOntologyAnnotationForInvOrStudy(protocol, "Study", " Protocol Type")),
                ("description", protocol['Study Protocol Description']),
                ("uri", protocol['Study Protocol URI']),
                ("version", protocol['Study Protocol Version']),
                ("parameters", self.createProtocolParameterList(protocol))
                ]
                )
            protocols_json.append(protocol_json)
        return protocols_json


    def createProtocolParameterList(self, protocol):
        json_list = []
        parameters_json = self.createOntologyAnnotationsFromStringList(protocol, "Study", " Protocol Parameters Name")
        for parameter_json in parameters_json:
            json_item = dict([
                ("parameterName",  parameter_json)
            ])
            json_list.append(json_item)
        return json_list


    def createOntologyAnnotationForInvOrStudy(self, object, inv_or_study, type):
        onto_ann = dict([
                ("name", object[inv_or_study+type]),
                ("termSource", object[inv_or_study+type+" Term Source REF"]),
                ("termAccession", object[inv_or_study+type+" Term Accession Number"])
        ])
        return onto_ann

    def createOntologyAnnotation(self, name, termSource, termAccesssion):
        onto_ann = dict([
            ("name", name),
            ("termSource", termSource),
            ("termAccession", termAccesssion)
        ])
        return onto_ann

    def createOntologyAnnotationsFromStringList(self, object, inv_or_study, type):
        name_array = object[inv_or_study+type].split(";")
        term_source_array = object[inv_or_study+type+" Term Source REF"].split(";")
        term_accession_array = object[inv_or_study+type+" Term Accession Number"].split(";")
        onto_annotations = []
        for i in range(0,len(name_array)):
             onto_ann = dict([
                 ("name", name_array[i]),
                 ("termSource", term_source_array[i]),
                 ("termAccession", term_accession_array[i])
             ])
             onto_annotations.append(onto_ann)
        return onto_annotations


    def createOntologyAnnotationListForInvOrStudy(self, array, inv_or_study, type):
        onto_annotations = []
        for object in array:
            onto_ann = dict([
                ("name", object[inv_or_study+type]),
                ("termSource", object[inv_or_study+type+" Term Source REF"]),
                ("termAccession", object[inv_or_study+type+" Term Accession Number"])
            ])
            onto_annotations.append(onto_ann)
        return onto_annotations



    def createOntologySourceReferences(self, ontology_refs):
        ontologies = []
        for ontology_ref in ontology_refs:
            ontology = dict([
                ("description", ontology_ref["Term Source Description"]),
                ("file",ontology_ref["Term Source File"]),
                ("name", ontology_ref["Term Source Name"]),
                ("version", ontology_ref["Term Source Version"])
            ])
            ontologies.append(ontology)
        return ontologies

    def createStudies(self, studies):
        study_array = []
        for study in studies:
            source_dict = self.createSourcesDictionary(study.nodes)
            sample_dict = self.createSampleDictionary(study.nodes)
            data_dict = self.createDataFiles(study.nodes)
            studyJson = dict([
                ("identifier",study.metadata['Study Identifier']),
                ("title", study.metadata['Study Title']),
                ("description", study.metadata['Study Description']),
                ("submissionDate", study.metadata['Study Submission Date']),
                ("publicReleaseDate", study.metadata['Study Public Release Date']),
                ("studyDesignDescriptors",self.createOntologyAnnotationListForInvOrStudy(study.design_descriptors, "Study", " Design Type")),
                ("publications", self.createPublications(study.publications, "Study")),
                ("people", self.createContacts(study.contacts, "Study")),
                #TODO
                ("studyDesignDescriptors", []),
                ("protocols", self.createProtocols(study.protocols)),
                ("sources", list(source_dict.values())),
                ("samples",list(sample_dict.values())),
                ("processSequence", self.createProcessSequence(study.process_nodes, source_dict, sample_dict, data_dict)),
                ("assays", self.createStudyAssaysList(study.assays))
            ])
            study_array.append(studyJson)

        return study_array

    def createProcessSequence(self, process_nodes, source_dict, sample_dict, data_dict):
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
                    ("executesProtocol", self.createExecuteStudyProtocol(process_node_name, process_nodes[process_node_name])),
                    ("parameters", []),
                    ("inputs", self.createInputList(process_nodes[process_node_name].inputs, source_dict, sample_dict)),
                    ("outputs", self.createOutputList(process_nodes[process_node_name].outputs, sample_dict) )
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
                   # ("name", dict([("value", process_node_name)])),
                   # ("description", dict([("value", process_node_name)])),
                   # ("version", dict([("value", process_node_name)])),
                   # ("uri", dict([("value", process_node_name)])),
                   # ("parameters", self.createProcessParameterList(process_node_name, process_node))
                ])
        return json_item


    def createProcessParameterList(self, process_node_name, process_node):
        #self.createOntologyAnnotationsFromStringList(protocol,"Study", " Protocol Parameters Name")
        json_list = []
        json_item = dict([
                    ("parameterType", dict([("value", process_node_name )])),
                    ("description", dict([("value", "")])),
                ])
        json_list.append(json_item)
        return json_list


    def createStudyAssaysList(self, assays):
        json_list = []
        for assay in assays:
            source_dict = self.createSourcesDictionary(assay.nodes)
            sample_dict = self.createSampleDictionary(assay.nodes)
            data_dict = self.createDataFiles(assay.nodes)
            json_item = dict([
                ("fileName", assay.metadata['Study Assay File Name']),
                ("measurementType", self.createOntologyAnnotation(assay.metadata['Study Assay Measurement Type'],
                                                                  assay.metadata['Study Assay Measurement Type Term Source REF'],
                                                                  assay.metadata['Study Assay Measurement Type Term Accession Number'])),
                ("technologyType", self.createOntologyAnnotation(assay.metadata['Study Assay Technology Type'],
                                                                 assay.metadata['Study Assay Technology Type Term Source REF'],
                                                                 assay.metadata['Study Assay Technology Type Term Accession Number'])),
                ("technologyPlatform", assay.metadata['Study Assay Technology Platform']),
                ("processSequence", self.createProcessSequence(assay.process_nodes, source_dict, sample_dict, data_dict))
                ])
            json_list.append(json_item)
        return json_list


    def createDataFiles(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype.endswith("Data File") :
                json_item = dict([
                    ("name", nodes[node_index].name),
                    ("type", nodes[node_index].ntype)
                ])
                json_dict.update({node_index: json_item})
        return json_dict


    def createSampleDictionary(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype == "Sample Name":
                json_item = dict([
                    ("name", node_index),
                    ("factors", []),
                    ("characteristics", self.createCharacteristicList(node_index, nodes[node_index])),
                ])
                json_dict.update({node_index: json_item})
        return json_dict

    def createSourcesDictionary(self, nodes):
        json_dict = dict([])
        for node_name in nodes:
            if nodes[node_name].ntype == "Source Name":
                json_item = dict([
                    ("name", node_name),
                    ("characteristics", self.createCharacteristicList(node_name, nodes[node_name])),
                ])
                json_dict.update({node_name: json_item})
        return json_dict


    def createCharacteristicList(self, node_name, node):
        json_list = []
        for header in node.metadata:
            if header.startswith("Characteristics"):
                 characteristic = header.replace("]", "").split("[")[-1]
                 characteristic_json = self.createOntologyAnnotation(characteristic, "", "")
                 json_item = dict([
                     ("characteristic", characteristic_json)
                 ])
                 json_list.append(json_item)
        return json_list



#isatab2isajson = ISATab2ISAjson_v1()
#isatab2isajson.convert("../../tests/datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS1","../../tests/datasets/metabolights", False)
#isatab2isajson.convert("../../tests/data/BII-I-1","../../tests/data", True)
#isatab2isajson.convert("../../tests/data/BII-S-7","../../tests/data", True)