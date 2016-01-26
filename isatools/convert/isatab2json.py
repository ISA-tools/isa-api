__author__ = 'agbeltran'

import json
import os
from os.path import join
from isatools.io.isatab_parser import parse
from jsonschema import RefResolver, Draft4Validator
from uuid import uuid4

SCHEMAS_PATH = join(os.path.dirname(os.path.realpath(__file__)), "../schemas/isa_model_version_1_0_schemas/core/")
INVESTIGATION_SCHEMA = "investigation_schema.json"


def convert(work_dir, json_dir):
    converter = ISATab2ISAjson_v1()
    converter.convert(work_dir, json_dir)


class ISATab2ISAjson_v1:

    def __init__(self):
        self.identifiers = list() #list of dictionaries
        self.counters = dict()

    def setIdentifier(self, type, name, identifier):
        self.identifiers.append(dict([("type", type), ("name", name), ("identifier", identifier)]))

    def getIdentifier(self, type, name):
        for subVal in self.identifiers:
            if subVal["type"]==type and subVal["name"]==name:
                return subVal["identifier"]

    def generateIdentifier(self, type):
        try:
            self.counters[type] += 1
        except KeyError:
            self.counters[type] = 1

        return "http://data.isa-tools.org/"+type+"/"+str(self.counters[type])

    #def generateIdentifier(self):
    #    return "http://data.isa-tools.org/UUID/"+str(uuid4())

    def convert(self, work_dir, json_dir):
        """Convert an ISA-Tab dataset (version 1) to JSON provided the ISA model v1.0 JSON Schemas
            :param work_dir: directory containing the ISA-tab dataset
            :param json_dir: output directory where the resulting json file will be saved
        """
        print("Converting ISAtab to ISAjson for ", work_dir)


        isa_tab = parse(work_dir)
        #print(isa_tab)

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
                        ("ontologySourceReferences", self.createOntologySourceReferences(isa_tab.ontology_refs)),
                        ("publications", self.createPublications(isa_tab.publications, "Investigation")),
                        ("people", self.createContacts(isa_tab.contacts, "Investigation")),
                        ("studies", self.createStudies(isa_tab.studies)),
                        ("comments", self.createInvestigationComments(isa_tab))
                    ])

                if (isa_tab.metadata['Investigation Identifier']):
                    file_name = os.path.join(json_dir,isa_tab.metadata['Investigation Identifier']+".json")
                else:
                    file_name = os.path.join(json_dir,isa_tab.studies[0].metadata['Study Identifier']+".json")

                #validate json
                schema = json.load(open(join(SCHEMAS_PATH, INVESTIGATION_SCHEMA)))
                resolver = RefResolver('file://'+join(SCHEMAS_PATH, INVESTIGATION_SCHEMA), schema)
                validator = Draft4Validator(schema, resolver=resolver)
                validator.validate(isa_json, schema)

                #TODO refactor saving the file into a separate method
                with open(file_name, "w") as outfile:
                    json.dump(isa_json, outfile, indent=4, sort_keys=True)
                    outfile.close()
                print("... conversion finished.")
                return isa_json

    def createInvestigationComments(self, isa_tab):
        comments = []
        comments.append(self.createComment('Created With Configuration',isa_tab.metadata['Comment[Created With Configuration]']))
        comments.append(self.createComment('Last Opened With Configuration', isa_tab.metadata['Comment[Last Opened With Configuration]']))
        return comments

    def createComment(self, name, value):
        comment_json = dict([
            ("name", name),
            ("value", value)
        ])
        return comment_json


    def createContacts(self, contacts, inv_or_study):
        people_json = []
        for contact in contacts:
            person_identifier = self.generateIdentifier("person")
            person_json = dict([
                ("@id", person_identifier),
                ("lastName", contact[inv_or_study+" Person Last Name"]),
                ("firstName", contact[inv_or_study+" Person First Name"]),
                ("midInitials", contact[inv_or_study+" Person Mid Initials"]),
                ("email", contact[inv_or_study+" Person Email"]),
                ("phone", contact[inv_or_study+" Person Phone"]),
                ("fax", contact[inv_or_study+" Person Fax"]),
                ("address", contact[inv_or_study+" Person Address"]),
                ("affiliation", contact[inv_or_study+" Person Affiliation"]),
                ("roles", self.createOntologyAnnotationsFromStringList(contact, inv_or_study, " Person Roles"))
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
            protocol_identifier = self.generateIdentifier("protocol")
            protocol_name = protocol['Study Protocol Name']
            self.setIdentifier("protocol", protocol_name, protocol_identifier)
            protocol_json = dict([
                ("@id", protocol_identifier),
                ("name", protocol_name),
                ("protocolType", self.createOntologyAnnotationForInvOrStudy(protocol, "Study", " Protocol Type")),
                ("description", protocol['Study Protocol Description']),
                ("uri", protocol['Study Protocol URI']),
                ("version", protocol['Study Protocol Version']),
                ("parameters", self.createProtocolParameterList(protocol)),
                ("components", self.createProtocolComponentList(protocol))
                ])
            protocols_json.append(protocol_json)
        return protocols_json


    def createProtocolParameterList(self, protocol):
        json_list = []
        parameters_json = self.createOntologyAnnotationsFromStringList(protocol, "Study", " Protocol Parameters Name")
        for parameter_json in parameters_json:
            parameter_identifier = self.generateIdentifier("parameter")
            self.setIdentifier("parameter", parameters_json[0]["annotationValue"], parameter_identifier)
            json_item = dict([
                ("@id", parameter_identifier),
                ("parameterName",  parameter_json)
            ])
            json_list.append(json_item)
        return json_list


    def createOntologyAnnotationForInvOrStudy(self, object, inv_or_study, type):
        onto_ann = dict([
                ("annotationValue", object[inv_or_study+type]),
                ("termSource", object[inv_or_study+type+" Term Source REF"]),
                ("termAccession", object[inv_or_study+type+" Term Accession Number"])
        ])
        return onto_ann


    def createOntologyAnnotation(self, name, termSource, termAccesssion):
        onto_ann = dict([
            ("annotationValue", name),
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
             onto_ann = self.createOntologyAnnotation(name_array[i],
                                                      term_source_array[i],
                                                      term_accession_array[i] )
             onto_annotations.append(onto_ann)
        return onto_annotations


    def createOntologyAnnotationListForInvOrStudy(self, array, inv_or_study, type):
        onto_annotations = []
        for object in array:
            onto_ann = self.createOntologyAnnotation(object[inv_or_study+type],
                                                     object[inv_or_study+type+" Term Source REF"],
                                                     object[inv_or_study+type+" Term Accession Number"])
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
            study_identifier = self.generateIdentifier("study")
            study_name = study.metadata['Study Identifier']
            self.setIdentifier("study", study_name, study_identifier)
            characteristics_categories_list = self.createCharacteristicsCategories(study.nodes)
            factors_list = self.createStudyFactorsList(study.factors)
            source_dict = self.createSourcesDictionary(study.nodes)
            sample_dict = self.createSampleDictionary(study.nodes)
            material_dict = self.createMaterialDictionary(study.nodes)
            #This data_dict should be empty on the studies - it is only used in the assays
            data_dict = self.createDataFiles(study.nodes)
            studyJson = dict([
                ("@id", study_identifier),
                ("identifier",study_name),
                ("title", study.metadata['Study Title']),
                ("description", study.metadata['Study Description']),
                ("submissionDate", study.metadata['Study Submission Date']),
                ("publicReleaseDate", study.metadata['Study Public Release Date']),
                ("studyDesignDescriptors",self.createOntologyAnnotationListForInvOrStudy(study.design_descriptors, "Study", " Design Type")),
                ("publications", self.createPublications(study.publications, "Study")),
                ("people", self.createContacts(study.contacts, "Study")),
                ("protocols", self.createProtocols(study.protocols)),
                ("factors", factors_list),
                ("characteristicCategories", characteristics_categories_list),
                ("materials", dict([
                        ("sources", list(source_dict.values())),
                        ("samples",list(sample_dict.values())),
                        ("otherMaterials",list(material_dict.values()))
                ])),
                ("processSequence", self.createProcessSequence(study.process_nodes, source_dict, sample_dict, material_dict, data_dict)),
                ("assays", self.createStudyAssaysList(study.assays, sample_dict)),
                ("filename", study.metadata['Study File Name']),
            ])
            study_array.append(studyJson)
        return study_array


    def createProtocolComponentList(self, protocol):
        json_list = []
        components_name = protocol['Study Protocol Components Name'].split(";")
        components_type_json = self.createOntologyAnnotationsFromStringList(protocol, "Study", " Protocol Components Type")
        index = 0
        for component_type_json in components_type_json:
            component_name = components_name[index]
            json_item = dict([
                ("componentName", component_name),
                ("componentType",  component_type_json)
            ])
            json_list.append(json_item)
            index += 1
        return json_list


    def createStudyFactorsList(self, factors):
        json_list = []
        for factor in factors:
             factor_identifier = self.generateIdentifier("factor")
             self.setIdentifier("factor", factor['Study Factor Name'], factor_identifier)
             json_item = dict([
                ("@id", factor_identifier),
                ("factorName", factor['Study Factor Name']),
                ("factorType", self.createOntologyAnnotation(factor['Study Factor Type'], factor['Study Factor Type Term Source REF'],factor['Study Factor Type Term Accession Number']))
            ])
             json_list.append(json_item)
        return json_list


    def createProcessSequence(self, process_nodes, source_dict, sample_dict, material_dict, data_dict):
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

            process_node = process_nodes[process_node_name]

            json_item = dict([
                    ("executesProtocol", self.createExecuteStudyProtocol(process_node_name, process_node)),
                    ("parameterValues", self.createValueList("Parameter Value", process_node_name, process_node)),
                    ("inputs", self.createInputList(process_node.inputs, source_dict, sample_dict, material_dict)),
                    ("outputs", self.createOutputList(process_node.outputs, sample_dict, material_dict) )
            ])
            json_list.append(json_item)
        return json_list

    def createInputList(self, inputs, source_dict, sample_dict, material_dict):
        json_list = []
        for argument in inputs:
            try:
                json_item = source_dict[argument]
                source_id = dict([("@id", json_item["@id"])])
                json_list.append(source_id)
            except KeyError:
                pass
            try:
                json_item = sample_dict[argument]
                sample_id = dict([("@id", json_item["@id"])])
                json_list.append(sample_id)
            except KeyError:
                pass
            try:
                json_item = material_dict[argument]
                material_id = dict([("@id", json_item["@id"])])
                json_list.append(material_id)
            except KeyError:
                pass
        return json_list

    def createOutputList(self, arguments, sample_dict, material_dict):
        json_list = []
        for argument in arguments:
            try:
                json_item = sample_dict[argument]
                sample_id = dict([("@id", json_item["@id"])])
                json_list.append(sample_id)
            except KeyError:
                pass

            try:
                json_item = material_dict[argument]
                material_id = dict([("@id", json_item["@id"])])
                json_list.append(material_id)
            except KeyError:
                pass
        return json_list

    def createExecuteStudyProtocol(self, process_node_name, process_node):
        json_item = dict([
                   ("@id", self.getIdentifier("protocol", process_node.protocol))
                ])
        return json_item


    def createStudyAssaysList(self, assays, sample_dict):
        json_list = []
        for assay in assays:
            source_dict = self.createSourcesDictionary(assay.nodes)
            sample_list = self.createSampleReferenceDict(assay.nodes)
            material_dict = self.createMaterialDictionary(assay.nodes)
            data_dict = self.createDataFiles(assay.nodes)
            assay_identifier = self.generateIdentifier("assay")
            assay_name = assay.metadata['Study Assay File Name']
            self.setIdentifier("assay", assay_name, assay_identifier)
            json_item = dict([
                ("@id", assay_identifier),
                ("filename", assay.metadata['Study Assay File Name']),
                ("measurementType", self.createOntologyAnnotation(assay.metadata['Study Assay Measurement Type'],
                                                                  assay.metadata['Study Assay Measurement Type Term Source REF'],
                                                                  assay.metadata['Study Assay Measurement Type Term Accession Number'])),
                ("technologyType", self.createOntologyAnnotation(assay.metadata['Study Assay Technology Type'],
                                                                 assay.metadata['Study Assay Technology Type Term Source REF'],
                                                                 assay.metadata['Study Assay Technology Type Term Accession Number'])),
                ("technologyPlatform", assay.metadata['Study Assay Technology Platform']),
                ("materials", dict([
                    ("samples", sample_list),
                    ("otherMaterials", list(material_dict.values()))
                ])),
                ("dataFiles", list(data_dict.values())),
                ("processSequence", self.createProcessSequence(assay.process_nodes, source_dict, sample_dict, material_dict, data_dict))
                ])
            json_list.append(json_item)
        return json_list

    def createDataFiles(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype.endswith("Data File") :
                data_identifier = self.generateIdentifier("data")
                self.setIdentifier("data", node_index, data_identifier)
                json_item = dict([
                    ("@id", data_identifier),
                    ("name", nodes[node_index].name),
                    ("type", nodes[node_index].ntype)
                ])
                json_dict.update({node_index: json_item})
        return json_dict


    def createSampleDictionary(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype == "Sample Name":
                sample_identifier = self.generateIdentifier("sample")
                self.setIdentifier("sample", node_index, sample_identifier)

                json_item = dict([
                        ("@id", sample_identifier),
                        ("name", node_index),
                        ("factorValues", self.createValueList("Factor Value", node_index, nodes[node_index])),
                        ("characteristics", self.createValueList("Characteristics",node_index, nodes[node_index]))
                    ])

                #derivesFrom source
                try:
                    source_name = nodes[node_index].metadata["Source Name"][0]
                    source_index = "source-"+source_name
                    source_identifier = self.getIdentifier("source", source_index)
                    json_item["derivesFrom"] = dict([ ("@id", source_identifier)])
                except KeyError:
                    print("There is no source declared for sample ", node_index)

                json_dict.update({node_index: json_item})

        return json_dict


    def createSampleReferenceDict(self, nodes):
        json_dict = []
        for node_index in nodes:
             if nodes[node_index].ntype == "Sample Name":
                sample_identifier = self.getIdentifier("sample", node_index)
                if sample_identifier:
                    json_dict.append(dict([("@id", sample_identifier)]))
                else:
                    print("Warning: sample identifier has not been defined before", node_index)
        return json_dict


    def createSourcesDictionary(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype == "Source Name":
                source_identifier = self.generateIdentifier("source")
                self.setIdentifier("source", node_index, source_identifier)
                json_item = dict([
                    ("@id", source_identifier),
                    ("name", node_index),
                    ("characteristics", self.createValueList("Characteristics", node_index, nodes[node_index])),
                ])
                json_dict.update({node_index: json_item})
        return json_dict

    def createMaterialDictionary(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype != "Source Name" and nodes[node_index].ntype != "Sample Name" and nodes[node_index].ntype.find("File")==-1:
                material_identifier = self.generateIdentifier("material")
                self.setIdentifier("material", node_index, material_identifier)
                json_item = dict([
                    ("@id", material_identifier),
                    ("name", node_index),
                    ("type", nodes[node_index].ntype),
                    ("characteristics", self.createValueList("Characteristics", node_index, nodes[node_index])),
                ])
                json_dict.update({node_index: json_item})
        return json_dict


    def createCharacteristicsCategories(self, nodes):
        json_list = []
        for node_index in nodes:
            node = nodes[node_index]
            for header in node.metadata:
                 if not header.startswith("Characteristics"):
                    continue
                 value_header = header.replace("]", "").split("[")[-1]
                 characteristic_category_identifier = self.getIdentifier("characteristics_category", value_header)
                 if characteristic_category_identifier:
                     continue

                 characteristic_category_identifier = self.generateIdentifier("charactersitic_category")
                 self.setIdentifier("characteristics_category", value_header, characteristic_category_identifier)

                 json_item = dict([])
                 #the header has an ontology annotation TODO - get a test dataset
                 if value_header.startswith("http"):
                    pass
                 else:
                    json_item = dict([
                        ("@id", characteristic_category_identifier),
                        ("characteristicType", self.createOntologyAnnotation(value_header, "", ""))
                    ])

                 json_list.append(json_item)
        return json_list

    def convert_num(self, s):
        try:
            return int(s)
        except ValueError:
            try:
               return float(s)
            except ValueError:
                return s



    def createValueList(self, column_name, node_name, node):
        """Method for the creation of factor, characteristics and parameter values"""
        json_list = []
        for header in node.metadata:
            if header.startswith(column_name):
                 value_header = header.replace("]", "").split("[")[-1]
                 value_attributes = node.metadata[header][0]
                 value  = self.convert_num(value_attributes[0])
                 header_type = None

                 if column_name.strip()=="Characteristics":
                     if header not in node.attributes:
                         continue
                     header_type = "characteristics_category"

                 if column_name.strip()=="Factor Value":
                     if header not in node.attributes:
                         continue
                     header_type = "factor"

                 if column_name.strip()=="Parameter Value":
                     if header not in node.parameters:
                         continue
                     header_type = "parameter"

                 category_identifier =  self.getIdentifier(header_type, value_header)

                 if value_header==None or category_identifier==None:
                    try:
                        value_json = dict([
                         ("value", value),
                         ("unit", self.createOntologyAnnotation(value_attributes.Unit, value_attributes.Term_Source_REF, value_attributes.Term_Accession_Number))
                        ])
                        json_list.append(value_json)
                        continue
                    except AttributeError:
                        try:
                            value_json = dict([
                                ("value", self.createOntologyAnnotation(value, value_attributes.Term_Source_REF, value_attributes.Term_Accession_Number))
                                ])
                            json_list.append(value_json)
                            continue
                        except AttributeError:
                            value_json = dict([
                                 ("value", value)
                                 ])
                            json_list.append(value_json)

                 else:
                    try:
                        value_json = dict([
                         ("category", dict([("@id", category_identifier)])),
                         ("value", value),
                         ("unit", self.createOntologyAnnotation(value_attributes.Unit, value_attributes.Term_Source_REF, value_attributes.Term_Accession_Number))
                        ])
                        json_list.append(value_json)
                        continue
                    except AttributeError:
                        try:
                            value_json = dict([
                                ("category", dict([("@id", category_identifier)])),
                                ("value", self.createOntologyAnnotation(value, value_attributes.Term_Source_REF, value_attributes.Term_Accession_Number))
                                ])
                            json_list.append(value_json)
                            continue
                        except AttributeError:
                            value_json = dict([
                                 ("category", dict([("@id", category_identifier)])),
                                 ("value", value)
                                 ])
                            json_list.append(value_json)
        return json_list
