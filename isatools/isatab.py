from .model.v1 import *
from isatools.io import isatab_parser
import os
import sys


def validate(isatab_dir, config_dir):
    """ Validate an ISA-Tab archive using the Java validator
    :param isatab_dir: Path to ISA-Tab files
    :param config_dir: Path to configuration XML files
    """
    if not os.path.exists(isatab_dir):
        raise IOError("isatab_dir " + isatab_dir + " does not exist")
    print("Using source ISA Tab folder: " + isatab_dir)
    print("ISA configuration XML folder: " + config_dir)
    convert_command = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "convert/isa_line_commands/bin/validate.sh -c " + config_dir + " " + isatab_dir)
    from subprocess import call
    try:
        return_code = call([convert_command], shell=True)
        if return_code < 0:
            print(sys.stderr, "Terminated by signal", -return_code)
        else:
            print(sys.stderr, "Returned", return_code)
    except OSError as e:
        print(sys.stderr, "Execution failed:", e)


def load(isatab_dir):

    def _createOntologySourceReferences(ontology_refs):
        ontologies = []
        for ontology_ref in ontology_refs:
            ontology = OntologySourceReference(
                description=ontology_ref['Term Source Description'],
                file=ontology_ref['Term Source File'],
                name=ontology_ref['Term Source Name'],
                version=ontology_ref['Term Source Version'],
            )
            ontologies.append(ontology)
        return ontologies

    def _createPublications(publications, inv_or_study):
        publications = []
        for pub in publications:
            publication= Publication(
                pubmed_id=pub[inv_or_study+' PubMed ID'],
                doi=pub[inv_or_study+' Publication DOI'],
                author_list=pub[inv_or_study+' Publication Author List'],
                title=pub[inv_or_study+' Publication Title'],
                status=_createOntologyAnnotationForInvOrStudy(pub, inv_or_study, ' Publication Status')
            )
            publications.append(publication)
        return publications

    def _createOntologyAnnotationForInvOrStudy(object_, inv_or_study, type_):
        onto_ann = OntologyAnnotation(
                name=object_[inv_or_study+type_],
                term_source=object_[inv_or_study+type_+" Term Source REF"],
                term_accession=object_[inv_or_study+type_+" Term Accession Number"],
        )
        return onto_ann

    def _createContacts(self, contacts, inv_or_study):
        people_json = []
        for contact in contacts:
            person_json = Contact(
                last_name=contact[inv_or_study+" Person Last Name"],
                first_name=contact[inv_or_study+" Person First Name"],
                mid_initials=contact[inv_or_study+" Person Mid Initials"],
                email=contact[inv_or_study+" Person Email"],
                phone=contact[inv_or_study+" Person Phone"],
                fax=contact[inv_or_study+" Person Fax"],
                address=contact[inv_or_study+" Person Address"],
                affiliation=contact[inv_or_study+" Person Affiliation"],
                roles=[]
            )
            people_json.append(person_json)
        return people_json


    def _createSampleDictionary(self, nodes):
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

    def _createSourcesDictionary(self, nodes):
        json_dict = dict([])
        for node_name in nodes:
            if nodes[node_name].ntype == "Source Name":
                json_item = dict([
                    ("name", node_name),
                    ("characteristics", self.createCharacteristicList(node_name, nodes[node_name])),
                ])
                json_dict.update({node_name: json_item})
        return json_dict

    def _createOntologyAnnotationListForInvOrStudy(array, inv_or_study, type_):
        onto_annotations = []
        for object_ in array:
            onto_ann = OntologyAnnotation(
                name=object_[inv_or_study+type_],
                term_source=object_[inv_or_study+type_+" Term Source REF"],
                term_accession=object_[inv_or_study+type_+" Term Accession Number"],
            )
            onto_annotations.append(onto_ann)
        return onto_annotations

    def _createProtocols(self, protocols):
        protocols_list = []
        for prot in protocols:
            protocol = Protocol(
                name=prot['Study Protocol Name'],
                protocol_type=self.createOntologyAnnotationForInvOrStudy(prot, "Study", " Protocol Type"),
                description=prot['Study Protocol Description'],
                uri=prot['Study Protocol URI'],
                version=prot['Study Protocol Version'],
                parameters=_createProtocolParameterList(prot),
            )
            protocols_list.append(protocol)
        return protocols_list

    def _createProtocolParameterList(protocol):
        parameters_list = []
        parameters_annotations = _createOntologyAnnotationsFromStringList(protocol, "Study", " Protocol Parameters Name")
        for parameter_annotation in parameters_annotations:
            parameter = ProtocolParameter(
                name=parameter_annotation
            )
            # TODO Units?
            parameters_list.append(parameter)
        return parameters_list

    def _createOntologyAnnotationsFromStringList(object_, inv_or_study, type_):
        name_array = object_[inv_or_study+type_].split(";")
        term_source_array = object_[inv_or_study+type_+" Term Source REF"].split(";")
        term_accession_array = object_[inv_or_study+type_+" Term Accession Number"].split(";")
        onto_annotations = []
        for i in range(0, len(name_array)):
             onto_ann = OntologyAnnotation(
                 name=name_array[i],
                 term_source=term_source_array[i],
                 term_accession=term_accession_array[i],
             )
             onto_annotations.append(onto_ann)
        return onto_annotations

    #TODO Finish how to process nodes etc.
    def _createDataFiles(nodes):
        json_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype.endswith("Data File"):
                json_item = Data(
                    name=nodes[node_index].name,
                    type_=nodes[node_index].ntype
                )
                json_dict.update({node_index: json_item})
        return json_dict

    def _createProcessSequence(process_nodes, source_dict, sample_dict, data_dict):
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
                    ("executesProtocol", _createExecuteStudyProtocol(process_node_name, process_nodes[process_node_name])),
                    ("parameters", []),
                    ("inputs", _createInputList(process_nodes[process_node_name].inputs, source_dict, sample_dict)),
                    ("outputs", _createOutputList(process_nodes[process_node_name].outputs, sample_dict) )
            ])
            json_list.append(json_item)
        return json_list

    def _createExecuteStudyProtocol(self, process_node_name, process_node):
        json_item = dict([
                   # ("name", dict([("value", process_node_name)])),
                   # ("description", dict([("value", process_node_name)])),
                   # ("version", dict([("value", process_node_name)])),
                   # ("uri", dict([("value", process_node_name)])),
                   # ("parameters", self.createProcessParameterList(process_node_name, process_node))
                ])
        return json_item

    def _createInputList(self, inputs, source_dict, sample_dict):
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


    def _createOutputList(self, arguments, sample_dict):
        json_list = []
        for argument in arguments:
            try:
                json_item = sample_dict[argument]
                json_list.append(json_item)
            except KeyError:
                pass
        return json_list

    def _createStudyAssaysList(self, assays):
        json_list = []
        for assay in assays:
            source_dict = self.createSourcesDictionary(assay.nodes)
            sample_dict = self.createSampleDictionary(assay.nodes)
            data_dict = self.createDataFiles(assay.nodes)
            json_item = Assay(
                file_name=assay.metadata['Study Assay File Name'],
                measurement_type=OntologyAnnotation(
                    name=assay.metadata['Study Assay Measurement Type'],
                    term_source=assay.metadata['Study Assay Measurement Type Term Source REF'],
                    term_accession=assay.metadata['Study Assay Measurement Type Term Accession Number']),
                technology_type=OntologyAnnotation(
                    name=assay.metadata['Study Assay Technology Type'],
                    term_source=assay.metadata['Study Assay Technology Type Term Source REF'],
                    term_accession=assay.metadata['Study Assay Technology Type Term Accession Number']),
                technology_platform=assay.metadata['Study Assay Technology Platform'],
                process_sequence=_createProcessSequence(assay.process_nodes, source_dict, sample_dict, data_dict),
            )
            json_list.append(json_item)
        return json_list

    def _createStudies(studies):
        study_array = []
        for study in studies:
            source_dict = _createSourcesDictionary(study.nodes)
            sample_dict = _createSampleDictionary(study.nodes)
            data_dict = _createDataFiles(study.nodes)
            studyJson = Study(
                identifier=study.metadata['Study Identifier'],
                title=study.metadata['Study Title'],
                description=study.metadata['Study Description'],
                submission_date=study.metadata['Study Submission Date'],
                public_release_date=study.metadata['Study Public Release Date'],
                design_descriptors=_createOntologyAnnotationListForInvOrStudy(study.design_descriptors, "Study", " Design Type"),
                publications=_createPublications(study.publications, "Study"),
                contacts=_createContacts(study.contacts, "Study"),
                protocols=_createProtocols(study.protocols),
                sources=list(source_dict.values()),
                samples=list(sample_dict.values()),
                process_sequence=_createProcessSequence(study.process_nodes, source_dict, sample_dict, data_dict),
                assays=_createStudyAssaysList(study.assays),
            )
            study_array.append(studyJson)
        return study_array


    isa_tab = isatab_parser.parse(isatab_dir)

    if isa_tab is None:
        raise IOError("There was problem parsing the ISA Tab")
    else:
        if isa_tab.metadata != {}:
            #print("isa_tab.metadata->",isa_tab.metadata)
            investigation = Investigation(
                identifier=isa_tab.metadata['Investigation Identifier'],
                title=isa_tab.metadata['Investigation Title'],
                description=isa_tab.metadata['Investigation Description'],
                submission_date=isa_tab.metadata['Investigation Submission Date'],
                public_release_date=isa_tab.metadata['Investigation Public Release Date'],
                ontology_source_references=_createOntologySourceReferences(isa_tab.ontology_refs),
                publications=_createPublications(isa_tab.publications, "Investigation"),
                contacts=_createContacts(isa_tab.contacts, "Investigation"),
                studies=_createStudies(isa_tab.studies),
            )
    return investigation


def dumpj(isa_obj, fp):
    s = isa_obj.to_json()
    return s


def loads(s):
    isa_obj = Investigation()
    return isa_obj


def dumps(isa_obj):
    s = isa_obj.to_json()
    return s
