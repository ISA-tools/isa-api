import json
import os
from os.path import join
from isatools.io.isatab_parser import parse
from jsonschema import RefResolver, Draft4Validator
from uuid import uuid4
from enum import Enum
import re
import glob
import logging


from isatools import isatab
from isatools.isajson import ISAJSONEncoder


log = logging.getLogger('isatools')

SCHEMAS_PATH = join(os.path.dirname(os.path.realpath(__file__)), "../resources/schemas/isa_model_version_1_0_schemas/core/")
INVESTIGATION_SCHEMA = "investigation_schema.json"

# REGEXES
_RX_COMMENTS = re.compile('Comment\[(.*?)\]')


class IdentifierType(Enum):
    counter = 1
    uuid = 2
    name = 3

def convert(work_dir, identifier_type=IdentifierType.name,
                validate_first=True, config_dir=isatab.default_config_dir,
                use_new_parser=False):
    i_files = glob.glob(os.path.join(work_dir, 'i_*.txt'))
    if validate_first:
        log.info("Validating input ISA tab before conversion")
        if len(i_files) != 1:
            log.fatal("Could not resolve input investigation file, please check input ISA tab directory")
            return
        with open(i_files[0], 'r', encoding='utf-8') as validate_fp:
            report = isatab.validate(fp=validate_fp, config_dir=config_dir,
                                     log_level=logging.ERROR)
            if len(report['errors']) > 0:
                log.fatal("Could not proceed with conversion as there are some fatal validation errors. Check log")
                return
    if use_new_parser:
        log.info("Using new ISA-Tab parser")
        log.info("Loading ISA-Tab: %s", i_files[0])
        with open(i_files[0], 'r', encoding='utf-8') as fp:
            ISA = isatab.load(fp)
            log.info("Dumping ISA-JSON")
            return json.loads(json.dumps(ISA, cls=ISAJSONEncoder))
    else:
        converter = ISATab2ISAjson_v1(identifier_type)
        log.info("Using old parser")
        return converter.convert(work_dir)


class ISATab2ISAjson_v1:

    MATERIAL_TYPE = "Material Type"
    LABEL = "Label"
    CHARACTERISTICS = "Characteristics"
    CHARACTERISTIC_CATEGORY = "characteristic_category"
    FACTOR_VALUE = "Factor Value"
    UNIT = "Unit"
    PARAMETER_VALUE = "Parameter Value"
    ARRAY_DESIGN_REF = "Array Design REF"

    def __init__(self, identifier_type):
        self.identifiers = list() #list of dictionaries
        self.counters = dict()
        self.identifier_type = identifier_type

    def setIdentifier(self, type, name, identifier):
        self.identifiers.append(dict([("type", type), ("name", name), ("identifier", identifier)]))

    def getIdentifier(self, type, name):
        for subVal in self.identifiers:
            if subVal["type"]==type and subVal["name"]==name:
                return subVal["identifier"]

    def generateIdentifier(self, type, name):
        try:
            self.counters[type] += 1
        except KeyError:
            self.counters[type] = 1

        identifier = ""

        if self.identifier_type==IdentifierType.counter:
            identifier = "http://data.isa-tools.org/"+type+"/"+str(self.counters[type])
        elif self.identifier_type == IdentifierType.uuid:
            identifier = "http://data.isa-tools.org/UUID/"+str(uuid4())
        elif self.identifier_type == IdentifierType.name:
            identifier = "#"+type+"/"+name.replace (" ", "_")

        self.setIdentifier(type, name, identifier)
        return identifier

    #def generateIdentifier(self):
    #    return "http://data.isa-tools.org/UUID/"+str(uuid4())

    def convert(self, work_dir):
        """Convert an ISA-Tab dataset (version 1) to JSON provided the ISA model v1.0 JSON Schemas
            :param work_dir: directory containing the ISA-tab dataset
        """
        log.info("Converting ISA-Tab to ISA-JSON for %s", work_dir)


        isa_tab = parse(work_dir)
        #print(isa_tab)

        if isa_tab is None:
            log.fatal("No ISA-Tab dataset found")
        else:
                isa_json = dict([])
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
                        ("comments", self.createComments(isa_tab.metadata))
                    ])

                # validate json
                with open(join(SCHEMAS_PATH, INVESTIGATION_SCHEMA)) as json_fp:
                    schema = json.load(json_fp)
                    resolver = RefResolver('file://'+join(SCHEMAS_PATH, INVESTIGATION_SCHEMA), schema)
                    validator = Draft4Validator(schema, resolver=resolver)
                    validator.validate(isa_json, schema)

                    log.info("Conversion finished")
                    return isa_json

    def createComments(self, isadict):
        comments = []
        for k in [k for k in isadict.keys() if _RX_COMMENTS.match(k)]:
            comments.append(self.createComment(_RX_COMMENTS.findall(k)[0], isadict[k]))
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
            person_last_name = contact[inv_or_study+" Person Last Name"]
            if not person_last_name:
                continue
            person_identifier = self.generateIdentifier("person", person_last_name)
            person_json = dict([
                ("@id", person_identifier),
                ("lastName", person_last_name),
                ("firstName", contact[inv_or_study+" Person First Name"]),
                ("midInitials", contact[inv_or_study+" Person Mid Initials"]),
                ("email", contact[inv_or_study+" Person Email"]),
                ("phone", contact[inv_or_study+" Person Phone"]),
                ("fax", contact[inv_or_study+" Person Fax"]),
                ("address", contact[inv_or_study+" Person Address"]),
                ("affiliation", contact[inv_or_study+" Person Affiliation"]),
                ("roles", self.createOntologyAnnotationsFromStringList(contact, inv_or_study, " Person Roles")),
                ("comments", self.createComments(contact))
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

    def createProtocols(self, protocols, assays):
        protocols_json = []

        protocols_to_attach_parameter = []
        #keep protocols that should have ArrayDesignREF as a parameter
        for assay in assays:
            for process_node in assay.process_nodes.values():
                if self.ARRAY_DESIGN_REF in process_node.parameters:
                        protocols_to_attach_parameter.append(process_node.protocol)
        protocol_identifier = self.generateIdentifier("protocol", "unknown")
        protocol_json = dict([
                                 ("@id", protocol_identifier),
                                 ("name", "unknown"),
                                 ("protocolType", dict([
                                     ("annotationValue", "")
                                 ])),
                                 ("description", ""),
                                 ("uri", ""),
                                 ("version", ""),
                                 ("parameters", []),
                                 ("components", [])
                             ])
        protocols_json.append(protocol_json)
        for protocol in protocols:
            protocol_name = protocol['Study Protocol Name']
            if not protocol_name:
                continue
            protocol_identifier = self.generateIdentifier("protocol", protocol_name)
            parameters = self.createProtocolParameterList(protocol)

            if protocol_name in protocols_to_attach_parameter:
                #add parameter for ArrayDesignREF if it is used in any assay
                parameter_identifier = self.generateIdentifier("parameter", self.ARRAY_DESIGN_REF)
                json_item = dict([
                    ("@id", parameter_identifier),
                    ("parameterName",  self.createOntologyAnnotation(self.ARRAY_DESIGN_REF, "", ""))
                ])

            protocol_json = dict([
                ("@id", protocol_identifier),
                ("name", protocol_name),
                ("protocolType", self.createOntologyAnnotationForInvOrStudy(protocol, "Study", " Protocol Type")),
                ("description", protocol['Study Protocol Description']),
                ("uri", protocol['Study Protocol URI']),
                ("version", protocol['Study Protocol Version']),
                ("parameters", parameters),
                ("components", self.createProtocolComponentList(protocol))
                ])
            protocols_json.append(protocol_json)

        return protocols_json


    def createProtocolParameterList(self, protocol):
        json_list = []
        parameters_json = self.createOntologyAnnotationsFromStringList(protocol, "Study", " Protocol Parameters Name")
        i = 0
        for parameter_json in parameters_json:
            parameter_identifier = self.generateIdentifier("parameter", parameters_json[i]["annotationValue"])
            json_item = dict([
                ("@id", parameter_identifier),
                ("parameterName",  parameter_json)
            ])
            json_list.append(json_item)
            i += 1
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
             if (not name_array[i]):
                 continue
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
            study_name = study.metadata['Study Identifier']
            study_identifier = self.generateIdentifier("study", study_name)
            characteristics_categories_list = self.createCharacteristicsCategories(study.nodes)
            unit_categories_list = self.createUnitsCategories(study.nodes)
            factors_list = self.createStudyFactorsList(study.factors)
            source_dict = self.createSourcesDictionary(study.nodes)
            sample_dict = self.createSampleDictionary(study.nodes)
            material_dict = self.createMaterialDictionary(study.nodes)
            protocol_list = self.createProtocols(study.protocols, study.assays)
            assay_list = self.createStudyAssaysList(study.assays, sample_dict)
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
                ("protocols", protocol_list),
                ("factors", factors_list),
                ("characteristicCategories", characteristics_categories_list),
                ("unitCategories", unit_categories_list),
                ("materials", dict([
                        ("sources", list(source_dict.values())),
                        ("samples",list(sample_dict.values())),
                        ("otherMaterials",list(material_dict.values()))
                ])),
                ("processSequence", self.createProcessSequence(study.process_nodes, source_dict, sample_dict, material_dict, data_dict)),
                ("assays", assay_list),
                ("filename", study.metadata['Study File Name']),
                ("comments", self.createComments(study.metadata)),
            ])
            # clean up unknown process if it's not used in process sequence
            unknown_used = False
            for assay in assay_list:
                for process in assay['processSequence']:
                    if process['executesProtocol']['@id'] == '#protocol/unknown':
                        unknown_used = True
                        break
            if not unknown_used:
                try:
                    unknown_prot_index = protocol_list.index(dict([
                                     ("@id", "#protocol/unknown"),
                                     ("name", "unknown"),
                                     ("protocolType", dict([
                                         ("annotationValue", "")
                                     ])),
                                     ("description", ""),
                                     ("uri", ""),
                                     ("version", ""),
                                     ("parameters", []),
                                     ("components", [])
                                 ]))
                    del studyJson['protocols'][unknown_prot_index]
                except ValueError:
                    pass  # if something went wrong earlier and the unknown protocol was never generated
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
             factor_identifier = self.generateIdentifier("factor", factor['Study Factor Name'])
             json_item = dict([
                ("@id", factor_identifier),
                ("factorName", factor['Study Factor Name']),
                ("factorType", self.createOntologyAnnotation(factor['Study Factor Type'], factor['Study Factor Type Term Source REF'],factor['Study Factor Type Term Accession Number']))
            ])
             json_list.append(json_item)
        return json_list

    def createProcessSequence(self, process_nodes, source_dict, sample_dict, material_dict, data_dict):
        json_list = []
        #generate all the identifiers
        for process_node_name in process_nodes:
            self.generateIdentifier("process", process_node_name)

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

            process_identifier = self.getIdentifier("process", process_node_name)
            protocol_executed =  self.createExecuteStudyProtocol(process_node_name, process_node)
            previous_process_identifier = self.getIdentifier("process", process_node.previous_process.name) if process_node.previous_process else ""
            next_process_identifier = self.getIdentifier("process", process_node.next_process.name) if process_node.next_process else ""
            if (process_node.assay_name):
                json_item = dict([
                    ("@id", process_identifier),
                    ("name", process_node.assay_name),
                    ("executesProtocol", protocol_executed),
                    ("performer", process_node.performer),
                    ("date", process_node.date),
                    ("parameterValues", self.createValueList(self.PARAMETER_VALUE, process_node_name, process_node)),
                    ("inputs", self.createInputList(process_node.inputs, source_dict, sample_dict, material_dict, data_dict)),
                    ("outputs", self.createOutputList(process_node.outputs, sample_dict, material_dict, data_dict)),
                    ("comments", self.createFromNodeComments(process_node)),
                ])
            else:
                json_item = dict([
                    ("@id", process_identifier),
                    ("executesProtocol", protocol_executed),
                    ("performer", process_node.performer),
                    ("date", process_node.date),
                    ("parameterValues", self.createValueList(self.PARAMETER_VALUE, process_node_name, process_node)),
                    ("inputs", self.createInputList(process_node.inputs, source_dict, sample_dict, material_dict, data_dict)),
                    ("outputs", self.createOutputList(process_node.outputs, sample_dict, material_dict, data_dict)),
                    ("comments", self.createFromNodeComments(process_node)),
            ])

            if previous_process_identifier:
                json_item.update({  "previousProcess" : dict([("@id", previous_process_identifier)]) })
            if next_process_identifier:
                json_item.update({ "nextProcess" :  dict([("@id", next_process_identifier)]) })
            json_list.append(json_item)
        return json_list

    def createInputList(self, inputs, source_dict, sample_dict, material_dict, data_dict):
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

            try:
                json_item = data_dict[argument]
                data_id = dict([("@id", json_item["@id"])])
                json_list.append(data_id)
            except KeyError:
                pass
        return json_list

    def createOutputList(self, arguments, sample_dict, material_dict, data_dict):
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

            try:
                json_item = data_dict[argument]
                data_id = dict([("@id", json_item["@id"])])
                json_list.append(data_id)
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
            characteristics_categories_list = self.createCharacteristicsCategories(assay.nodes)
            unit_categories_list = self.createUnitsCategories(assay.nodes)
            source_dict = self.createSourcesDictionary(assay.nodes)
            sample_list = self.createSampleReferenceDict(assay.nodes, sample_dict)
            material_dict = self.createMaterialDictionary(assay.nodes)
            data_dict = self.createDataFiles(assay.nodes)
            assay_name = assay.metadata['Study Assay File Name']
            assay_identifier = self.generateIdentifier("assay", assay_name)
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
                ("characteristicCategories", characteristics_categories_list),
                ("unitCategories", unit_categories_list),
                ("materials", dict([
                    ("samples", sample_list),
                    ("otherMaterials", list(material_dict.values()))
                ])),
                ("dataFiles", list(data_dict.values())),
                ("processSequence", self.createProcessSequence(assay.process_nodes, source_dict, sample_dict, material_dict, data_dict))
                ])
            json_list.append(json_item)
        return json_list

    def createFromNodeComments(self, node):
        comments = []
        for key in [key for key in node.metadata.keys() if _RX_COMMENTS.match(key)]:
            comments.append(self.createComment(_RX_COMMENTS.findall(key)[0], getattr(
                node.metadata[key][0], _RX_COMMENTS.findall(key)[0].replace(' ', '_'))))
        return comments

    def createDataFiles(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype.endswith(" File") :
                data_identifier = self.generateIdentifier("data", node_index)
                json_item = dict([
                    ("@id", data_identifier),
                    ("name", nodes[node_index].name),
                    ("type", nodes[node_index].ntype),
                    ("comments", self.createFromNodeComments(nodes[node_index]))
                ])
                json_dict.update({node_index: json_item})
        return json_dict

    def createSampleDictionary(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype == "Sample Name":
                sample_identifier = self.generateIdentifier("sample", node_index)

                json_item = dict([
                        ("@id", sample_identifier),
                        ("name", node_index),
                        ("factorValues", self.createValueList(self.FACTOR_VALUE, node_index, nodes[node_index])),
                        ("characteristics", self.createValueList(self.CHARACTERISTICS,node_index, nodes[node_index]))
                    ])

                #derivesFrom sources
                try:
                     json_list = []
                     for source_name in nodes[node_index].derivesFrom:
                        source_index = "source-"+source_name
                        source_identifier = self.getIdentifier("source", source_index)
                        json_list.append(dict([ ("@id", source_identifier)]))

                     json_item["derivesFrom"] = json_list
                except KeyError:
                     log.error("There is no source declared for sample %s", node_index)

                json_dict.update({node_index: json_item})

        return json_dict

    def createSampleReferenceDict(self, nodes, sample_dict):
        json_dict = []
        for node_index in nodes:
             node = nodes[node_index]
             if node.ntype == "Sample Name":
                sample_identifier = self.getIdentifier("sample", node_index)
                if sample_identifier:
                    json_dict.append(dict([("@id", sample_identifier)]))
                else:
                    log.warning("Warning: sample identifier has not been defined before %s", node_index)
                #  adding sample attributes that may have been defined at the assay level
                try:
                    sample_json = sample_dict[node_index]
                    new_characteristics = self.createValueList(self.CHARACTERISTICS,node_index, node)
                    sample_json["characteristics"] = sample_json["characteristics"] + new_characteristics
                    sample_dict[node_index] = sample_json
                except KeyError:
                    log.warning("Warning: the sample %s has not been defined at the study level", node_index)

        return json_dict

    def createSourcesDictionary(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype == "Source Name":
                source_identifier = self.generateIdentifier("source", node_index)
                json_item = dict([
                    ("@id", source_identifier),
                    ("name", node_index),
                    ("characteristics", self.createValueList(self.CHARACTERISTICS, node_index, nodes[node_index])),
                ])
                json_dict.update({node_index: json_item})
        return json_dict

    def createMaterialDictionary(self, nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype != "Source Name" and nodes[node_index].ntype != "Sample Name" and nodes[node_index].ntype.find("File")==-1:
                material_identifier = self.generateIdentifier("material", node_index)
                json_item = dict([
                    ("@id", material_identifier),
                    ("name", node_index),
                    ("type", nodes[node_index].ntype),
                    ("characteristics", self.createValueList(self.CHARACTERISTICS, node_index, nodes[node_index])),
                ])
                json_dict.update({node_index: json_item})
        return json_dict

    def createCharacteristicsCategories(self, nodes):
        json_list = []
        for node_index in nodes:
            node = nodes[node_index]
            for header in node.metadata:
                 if (not header.startswith(self.CHARACTERISTICS)) and (not header==self.MATERIAL_TYPE) and (not header==self.LABEL):
                    continue
                 value_header = header.replace("]", "").split("[")[-1]
                 if header == self.MATERIAL_TYPE:
                     value_header = self.MATERIAL_TYPE
                 if header == self.LABEL:
                     value_header = self.LABEL

                 characteristic_category_identifier = self.getIdentifier(self.CHARACTERISTIC_CATEGORY, value_header)
                 if characteristic_category_identifier:
                     continue

                 characteristic_category_identifier = self.generateIdentifier(self.CHARACTERISTIC_CATEGORY, value_header)

                 json_item = dict([])
                 if value_header.startswith("http"):
                    #the header has an ontology annotation TODO - get a test dataset
                    pass
                 else:
                    json_item = dict([
                        ("@id", characteristic_category_identifier),
                        ("characteristicType", self.createOntologyAnnotation(value_header, "", ""))
                    ])

                 json_list.append(json_item)
        return json_list

    def createUnitsCategories(self, nodes):
        json_list = []
        for node_index in nodes:
            node = nodes[node_index]
            for header in node.metadata:
                 if not header.startswith(self.CHARACTERISTICS) and not header.startswith(self.FACTOR_VALUE) and not header.startswith(self.PARAMETER_VALUE):
                    continue
                 value_attributes = node.metadata[header][0]
                 try:
                    unit = value_attributes.Unit
                 except AttributeError:
                     continue

                 unit_category_identifier = self.getIdentifier(self.UNIT, unit)
                 if unit_category_identifier:
                    continue

                 unit_category_identifier = self.generateIdentifier(self.UNIT, value_attributes.Unit)
                 json_item = dict([
                         ("@id", unit_category_identifier),
                     ])
                 json_item.update(self.createOntologyAnnotation(value_attributes.Unit, value_attributes.Term_Source_REF, value_attributes.Term_Accession_Number))
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
            if header.startswith(column_name) or header == self.MATERIAL_TYPE or header == self.LABEL or header==self.ARRAY_DESIGN_REF:
                 value_header = header.replace("]", "").split("[")[-1]

                 value_attributes = node.metadata[header][0]
                 value  = self.convert_num(value_attributes[0])
                 header_type = None

                 if column_name.strip()==self.CHARACTERISTICS:
                     if header not in node.attributes:
                         continue
                     if header == self.MATERIAL_TYPE:
                        value_header = self.MATERIAL_TYPE
                     elif header == self.LABEL:
                        value_header = self.LABEL
                     header_type = self.CHARACTERISTIC_CATEGORY
                 elif column_name.strip()==self.FACTOR_VALUE:
                     if header not in node.attributes:
                         continue
                     header_type = "factor"
                 elif column_name.strip()==self.PARAMETER_VALUE:
                     if header not in node.parameters:
                         continue
                     if header == self.ARRAY_DESIGN_REF:
                         value_header = self.ARRAY_DESIGN_REF
                     header_type = "parameter"

                 category_identifier =  self.getIdentifier(header_type, value_header)

                 if value_header==None or category_identifier==None:
                    try:
                        unit_identifier = self.getIdentifier(self.UNIT, value_attributes.Unit)
                        value_json = dict([
                         ("value", value),
                         ("unit", dict([("@id", unit_identifier)]))
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
                        unit_identifier = self.getIdentifier(self.UNIT, value_attributes.Unit)
                        value_json = dict([
                         ("category", dict([("@id", category_identifier)])),
                         ("value", value),
                         ("unit", dict([("@id", unit_identifier)]))
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