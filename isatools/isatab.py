from _hashlib import new
from .model.v1 import *
from isatools.io import isatab_parser
import os
import sys
import pandas as pd
import io
import networkx as nx


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

    def _createPublications(isapubs, inv_or_study):
        publications = []
        for pub in isapubs:
            publication = Publication(
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

    def _createContacts(contacts, inv_or_study):
        people_json = []
        for contact in contacts:
            person_json = Person(
                last_name=contact[inv_or_study+" Person Last Name"],
                first_name=contact[inv_or_study+" Person First Name"],
                mid_initials=contact[inv_or_study+" Person Mid Initials"],
                email=contact[inv_or_study+" Person Email"],
                phone=contact[inv_or_study+" Person Phone"],
                fax=contact[inv_or_study+" Person Fax"],
                address=contact[inv_or_study+" Person Address"],
                affiliation=contact[inv_or_study+" Person Affiliation"],
                # FIXME Parsing roles?
                roles=[]
            )
            people_json.append(person_json)
        return people_json


    def _createCharacteristicList(node_name, node):
        obj_list = []
        for header in node.metadata:
            if header.startswith("Characteristics"):
                characteristic = header.replace("]", "").split("[")[-1]
                characteristic_obj = Characteristic(
                    value=OntologyAnnotation(name=characteristic)
                )
                obj_item = dict([
                    ("characteristic", characteristic_obj)
                ])
                obj_list.append(obj_item)
        return obj_list

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

    def _createProtocols(protocols):
        protocols_list = []
        for prot in protocols:
            protocol = Protocol(
                name=prot['Study Protocol Name'],
                protocol_type=_createOntologyAnnotationForInvOrStudy(prot, "Study", " Protocol Type"),
                description=prot['Study Protocol Description'],
                uri=prot['Study Protocol URI'],
                version=prot['Study Protocol Version'],
                parameters=_createProtocolParameterList(prot),
            )
            protocols_list.append(protocol)
        return protocols_list

    def _createProtocolParameterList(protocol):
        parameters_list = []
        parameters_annotations = _createOntologyAnnotationsFromStringList(protocol, "Study",
                                                                          " Protocol Parameters Name")
        for parameter_annotation in parameters_annotations:
            parameter = ProtocolParameter(
                # parameterName=parameter_annotation
            )
            parameters_list.append(parameter)
        return parameters_list

    def _createOntologyAnnotationsFromStringList(object_, inv_or_study, type_):
        #FIXME If empty string, it returns 1?
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

    def _createDataFiles(nodes):
        obj_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype.endswith("Data File"):
                obj_item = Data(
                    name=nodes[node_index].name,
                    type_=nodes[node_index].ntype
                )
                obj_dict.update({node_index: obj_item})
        return obj_dict

    def _createProcessSequence(process_nodes, source_dict, sample_dict, data_dict):
        obj_list = []
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

            obj_item = Process(
                executes_protocol=_createExecuteStudyProtocol(process_node_name, process_nodes[process_node_name]),
                parameters=list(),
                inputs=_createInputList(process_nodes[process_node_name].inputs, source_dict, sample_dict),
                outputs=_createOutputList(process_nodes[process_node_name].outputs, sample_dict)
            )
            obj_list.append(obj_item)
        return obj_list

    def _createExecuteStudyProtocol(process_node_name, process_node):
        json_item = dict([
                   # ("name", dict([("value", process_node_name)])),
                   # ("description", dict([("value", process_node_name)])),
                   # ("version", dict([("value", process_node_name)])),
                   # ("uri", dict([("value", process_node_name)])),
                   # ("parameters", self.createProcessParameterList(process_node_name, process_node))
                ])
        return json_item

    def _createInputList(inputs, source_dict, sample_dict):
        obj_list = list()
        for argument in inputs:
            try:
                obj_item = source_dict[argument]
                obj_list.append(obj_item)
            except KeyError:
                pass
            try:
                obj_item = sample_dict[argument]
                obj_list.append(obj_item)
            except KeyError:
                pass
        return obj_list

    def _createOutputList(arguments, sample_dict):
        obj_list = []
        for argument in arguments:
            try:
                obj_item = sample_dict[argument]
                obj_list.append(obj_item)
            except KeyError:
                pass
        return obj_list

    def _createStudyAssaysList(assays):
        json_list = list()
        for assay in assays:
            source_dict = _createSourceDictionary(assay.nodes)
            sample_dict = _createSampleDictionary(assay.nodes)
            data_dict = _createDataFiles(assay.nodes)
            json_item = Assay(
                filename=assay.metadata['Study Assay File Name'],
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

    def _createValueList(column_name, node_name, node):
        obj_list = list()
        for header in node.metadata:
            if header.startswith(column_name):
                value_header = header.replace("]", "").split("[")[-1]
                value_attributes = node.metadata[header][0]
                value = value_attributes[0]  # In tab2json uses convert_num to recast string to int or float
                try:
                    if column_name == 'Characteristics':
                        value_obj = Characteristic(
                            category=value_header,
                            value=value,
                            unit=OntologyAnnotation(
                                name=value_attributes.Unit,
                                term_accession=value_attributes.Term_Accession_Number,
                                term_source=value_attributes.Term_Source_REF,
                            )
                        )
                    elif column_name == 'Factor Value':
                        value_obj = FactorValue(
                            # factorName=value_header,
                            value=value,
                            unit=OntologyAnnotation(
                                name=value_attributes.Unit,
                                term_accession=value_attributes.Term_Accession_Number,
                                term_source=value_attributes.Term_Source_REF,
                            )
                        )
                    obj_list.append(value_obj)
                    continue
                except AttributeError:
                    try:
                        if column_name == 'Characteristics':
                            value_obj = Characteristic(
                                category=value_header,
                                value=OntologyAnnotation(
                                    name=value,
                                    term_accession=value_attributes.Term_Accession_Number,
                                    term_source=value_attributes.Term_Source_REF,
                                )
                            )
                            obj_list.append(value_obj)
                        elif column_name == 'Factor Value':
                            value_obj = FactorValue(
                                # factorName=value_header,
                                value=OntologyAnnotation(
                                    name=value,
                                    term_accession=value_attributes.Term_Accession_Number,
                                    term_source=value_attributes.Term_Source_REF,
                                )
                            )
                        continue
                    except AttributeError:
                        if column_name == 'Characteristics':
                            value_obj = Characteristic(
                                category=value_header,
                                value=OntologyAnnotation(
                                    name=value
                                )
                            )
                        elif column_name == 'Factor Value':
                            value_obj = FactorValue(
                                # factorName=value_header,
                                value=OntologyAnnotation(
                                    name=value
                                )
                            )
                        obj_list.append(value_obj)
        return obj_list

    def _createSourceDictionary(nodes):
        obj_dict = dict([])
        for node_name in nodes:
            if nodes[node_name].ntype == "Source Name":
                reformatted_node_name = node_name[7:]  # Strip out the source- bit
                source_item = Source(
                    name=reformatted_node_name,
                    characteristics=_createValueList("Characteristics", node_name, nodes[node_name]),
                )
                obj_dict.update({node_name: source_item})
        return obj_dict

    def _createSampleDictionary(nodes):
        obj_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype == "Sample Name":
                reformatted_node_name = node_index[7:]  # Strip out the sample- bit
                try:
                    obj_item = Sample(
                        name=reformatted_node_name,
                        factor_values=_createValueList("Factor Value", node_index, nodes[node_index]),
                        characteristics=_createValueList("Characteristics", node_index, nodes[node_index]),
                        derives_from=nodes[node_index].metadata["Source Name"][0],
                    )
                    obj_dict.update({node_index: obj_item})
                except KeyError:
                    pass
        return obj_dict

    def _createStudies(studies):
        study_array = []
        for study in studies:
            sources = _createSourceDictionary(study.nodes)
            samples = _createSampleDictionary(study.nodes)
            data_dict = _createDataFiles(study.nodes)
            study_obj = Study(
                identifier=study.metadata['Study Identifier'],
                title=study.metadata['Study Title'],
                description=study.metadata['Study Description'],
                submission_date=study.metadata['Study Submission Date'],
                public_release_date=study.metadata['Study Public Release Date'],
                factors=None,
                filename=study.metadata['Study File Name'],
                design_descriptors=_createOntologyAnnotationListForInvOrStudy(study.design_descriptors, "Study",
                                                                              " Design Type"),
                publications=_createPublications(study.publications, "Study"),
                contacts=_createContacts(study.contacts, "Study"),
                protocols=_createProtocols(study.protocols),
                sources=list(sources.values()),
                samples=list(samples.values()),
                process_sequence=_createProcessSequence(study.process_nodes, sources, samples, data_dict),
                # assays=_createStudyAssaysList(study.assays),
            )
            study_array.append(study_obj)
        return study_array

    investigation = None
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


def dump(isa_obj, output_path):
    if os.path.exists(output_path):
        fp = open(os.path.join(output_path, 'i_investigation.txt'), 'w')
    else:
        raise FileNotFoundError("Can't find " + output_path)
    if isinstance(isa_obj, Investigation):
        # Process Investigation object first to write the investigation file
        investigation = isa_obj

        # Write ONTOLOGY SOURCE REFERENCE section
        ontology_source_references_df = pd.DataFrame(columns=('Term Source Name',
                                                              'Term Source File',
                                                              'Term Source Version',
                                                              'Term Source Description'
                                                              )
                                                     )
        i = 0
        for ontology_source_reference in investigation.ontology_source_references:
            ontology_source_references_df.loc[i] = [
                ontology_source_reference.name,
                ontology_source_reference.file,
                ontology_source_reference.version,
                ontology_source_reference.description
            ]
            i += 1
        ontology_source_references_df = ontology_source_references_df.set_index('Term Source Name').T
        fp.write('ONTOLOGY SOURCE REFERENCE\n')
        ontology_source_references_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                             index_label='Term Source Name')  # Need to set index_label as top left cell

        # Write INVESTIGATION section
        investigation_df = pd.DataFrame(columns=('Investigation Identifier',
                                                 'Investigation Title',
                                                 'Investigation Description',
                                                 'Investigation Submission Date',
                                                 'Investigation Public Release Date'
                                                 )
                                        )
        investigation_df.loc[0] = [
            investigation.identifier,
            investigation.title,
            investigation.description,
            investigation.submission_date,
            investigation.public_release_date
        ]
        investigation_df = investigation_df.set_index('Investigation Identifier').T
        fp.write('INVESTIGATION\n')
        investigation_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                index_label='Investigation Identifier')  # Need to set index_label as top left cell

        # Write INVESTIGATION PUBLICATIONS section
        investigation_publications_df = pd.DataFrame(columns=('Investigation PubMed ID',
                                                              'Investigation Publication DOI',
                                                              'Investigation Publication Author List',
                                                              'Investigation Publication Status',
                                                              'Investigation Publication Status Term Accession '
                                                              'Number',
                                                              'Investigation Publication Status Term Source REF'
                                                              )
                                                     )
        i = 0
        for investigation_publication in investigation.publications:
            investigation_publications_df.loc[i] = [
                investigation_publication.pubmed_id,
                investigation_publication.doi,
                investigation_publication.author_list,
                investigation_publication.status.name,
                investigation_publication.status.term_source,
                investigation_publication.status.term_accession,
            ]
            i += 1
        investigation_publications_df = investigation_publications_df.set_index('Investigation PubMed ID').T
        fp.write('INVESTIGATION PUBLICATIONS\n')
        investigation_publications_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                             index_label='Investigation PubMed ID')

        # Write INVESTIGATION CONTACTS section
        investigation_contacts_df = pd.DataFrame(columns=('Investigation Person Last Name',
                                                          'Investigation Person First Name',
                                                          'Investigation Person Mid Initials',
                                                          'Investigation Person Email',
                                                          'Investigation Person Phone',
                                                          'Investigation Person Fax',
                                                          'Investigation Person Address',
                                                          'Investigation Person Affiliation',
                                                          'Investigation Person Roles',
                                                          'Investigation Person Roles Term Accession Number',
                                                          'Investigation Person Roles Term Source REF'
                                                          )
                                                 )
        i = 0
        for investigation_contact in investigation.contacts:
            roles = ''
            roles_accession_numbers = ''
            roles_source_refs = ''
            for role in investigation_contact.roles:
                roles += role.name + ';'
                roles_accession_numbers += role.term_accession + ';'
                roles_source_refs += role.term_source.name + ';'
            investigation_contacts_df.loc[i] = [
                investigation_contact.last_name,
                investigation_contact.first_name,
                investigation_contact.mid_initials,
                investigation_contact.email,
                investigation_contact.phone,
                investigation_contact.fax,
                investigation_contact.address,
                investigation_contact.affiliation,
                roles,
                roles_accession_numbers,
                roles_source_refs
            ]
            i += 1
        investigation_contacts_df = investigation_contacts_df.set_index('Investigation Person Last Name').T
        fp.write('INVESTIGATION CONTACTS\n')
        investigation_contacts_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                         index_label='Investigation PubMed ID')

        # Write STUDY sections
        i = 0
        for study in investigation.studies:
            study_df = pd.DataFrame(columns=('Study Identifier',
                                             'Study Title',
                                             'Study Description',
                                             'Study Submission Date',
                                             'Study Public Release Date',
                                             'Study File Name'
                                             )
                                    )
            study_df.loc[i] = [
                study.identifier,
                study.title,
                study.description,
                study.submission_date,
                study.public_release_date,
                study.filename
            ]
            study_df = study_df.set_index('Study Identifier').T
            fp.write('STUDY\n')
            study_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8', index_label='Study Identifier')

            # Write STUDY DESIGN DESCRIPTORS section
            study_design_descriptors_df = pd.DataFrame(columns=('Study Design Type',
                                                                'Study Design Type Term Accession Number',
                                                                'Study Design Type Term Source REF'
                                                                )
                                                       )
            j = 0
            for design_descriptor in study.design_descriptors:
                study_design_descriptors_df.loc[j] = [
                    design_descriptor.name,
                    design_descriptor.term_accession,
                    design_descriptor.term_source
                ]
                study_design_descriptors_df = study_design_descriptors_df.set_index('Study Design Type').T
                fp.write('STUDY DESIGN DESCRIPTORS\n')
                study_design_descriptors_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                                   index_label='Study Design Type')

            # Write STUDY PUBLICATIONS section
            study_publications_df = pd.DataFrame(columns=('Study PubMed ID',
                                                          'Study Publication DOI',
                                                          'Study Publication Author List',
                                                          'Study Publication Status',
                                                          'Study Publication Status Term Accession Number',
                                                          'Study Publication Status Term Source REF'
                                                          )
                                                 )
            j = 0
            for study_publication in study.publications:
                study_publications_df.loc[j] = [
                    study_publication.pubmed_id,
                    study_publication.doi,
                    study_publication.author_list,
                    study_publication.status.name,
                    study_publication.status.term_source,
                    study_publication.status.term_accession,
                ]
                j += 1
            study_publications_df = study_publications_df.set_index('Study PubMed ID').T
            fp.write('STUDY PUBLICATIONS\n')
            study_publications_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                                 index_label='Study PubMed ID')

            # Write STUDY FACTORS section
            study_factors_df = pd.DataFrame(columns=('Study Factor Name',
                                                     'Study Factor Type',
                                                     'Study Factor Type Term Accession Number',
                                                     'Study Factor Type Term Source REF'
                                                     )
                                            )
            j = 0
            for factor in study.factors:
                study_factors_df.loc[j] = [
                    factor.name,
                    factor.factor_type.name,
                    factor.factor_type.term_accession,
                    factor.factor_type.term_source
                ]
                j += 1
            study_factors_df = study_factors_df.set_index('Study Factor Name').T
            fp.write('STUDY FACTORS\n')
            study_factors_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                    index_label='Study Factor Name')

            # Write STUDY ASSAYS section
            study_assays_df = pd.DataFrame(columns=('Study Assay Measurement Type',
                                                    'Study Assay Measurement Type Term Accession Number',
                                                    'Study Assay Measurement Type Term Source REF',
                                                    'Study Assay Technology Type',
                                                    'Study Assay Technology Type Term Accession Number',
                                                    'Study Assay Technology Type Term Source REF',
                                                    'Study Assay Technology Platform',
                                                    'Study Assay File Name'
                                                    )
                                           )
            j = 0
            for assay in study.assays:
                study_assays_df.loc[j] = [
                    assay.measurement_type.name,
                    assay.measurement_type.term_accession,
                    assay.measurement_type.term_source,
                    assay.technology_type.name,
                    assay.technology_type.term_accession,
                    assay.technology_type.term_source,
                    assay.technology_platform,
                    assay.filename
                ]
                j += 1
            study_assays_df = study_assays_df.set_index('Study Assay Measurement Type').T
            fp.write('STUDY ASSAYS\n')
            study_assays_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                   index_label='Study Assay Measurement Type')

            # Write STUDY PROTOCOLS section
            study_protocols_df = pd.DataFrame(columns=('Study Protocol Name',
                                                       'Study Protocol Type',
                                                       'Study Protocol Type  Accession Number',
                                                       'Study Protocol Type Source REF',
                                                       'Study Protocol Description',
                                                       'Study Protocol URI',
                                                       'Study Protocol Version',
                                                       'Study Protocol Parameters Name',
                                                       'Study Protocol Parameters Name Term Accession Number',
                                                       'Study Protocol Parameters Name Term Source REF',
                                                       'Study Protocol Components Name',
                                                       'Study Protocol Components Type',
                                                       'Study Protocol Components Type Term Accession Number',
                                                       'Study Protocol Components Type Term Source REF',
                                                       )
                                              )
            j = 0
            for protocol in study.protocols:
                parameters_names = ''
                parameters_accession_numbers = ''
                parameters_source_refs = ''
                for parameter in protocol.parameters:
                    parameters_names += parameter.parameter_name.name + ';'
                    parameters_accession_numbers += parameter.parameter_name.term_accession + ';'
                    parameters_source_refs += parameter.parameter_name.term_source.name + ';'
                component_names = ''
                component_types = ''
                component_types_accession_numbers = ''
                component_types_source_refs = ''
                for component in protocol.components:
                    component_names += component.name + ';'
                    component_types += component.component_type + ';'
                    component_types_accession_numbers += component.component_type.term_accession + ';'
                    component_types_source_refs += component.component_type.term_source.name + ';'
                study_protocols_df.loc[j] = [
                    protocol.name,
                    protocol.protocol_type.name,
                    protocol.protocol_type.term_accession,
                    protocol.protocol_type.term_source,
                    protocol.description,
                    protocol.uri,
                    protocol.version,
                    parameters_names,
                    parameters_accession_numbers,
                    parameters_source_refs,
                    component_names,
                    component_types,
                    component_types_accession_numbers,
                    component_types_source_refs
                ]
                j += 1
            study_protocols_df = study_protocols_df.set_index('Study Protocol Name').T
            fp.write('STUDY PROTOCOLS\n')
            study_protocols_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                      index_label='Study Protocol Name')

            # Write STUDY CONTACTS section
            study_contacts_df = pd.DataFrame(columns=('Study Person Last Name',
                                                      'Study Person First Name',
                                                      'Study Person Mid Initials',
                                                      'Study Person Email',
                                                      'Study Person Phone',
                                                      'Study Person Fax',
                                                      'Study Person Address',
                                                      'Study Person Affiliation',
                                                      'Study Person Roles',
                                                      'Study Person Roles Term Accession Number',
                                                      'Study Person Roles Term Source REF'
                                                      )
                                             )
            j = 0
            for study_contact in study.contacts:
                # roles = ''
                # roles_accession_numbers = ''
                # roles_source_refs = ''
                # for role in study_contact.roles:
                #     roles += role.name + ';'
                #     roles_accession_numbers += role.term_accession + ';'
                #     roles_source_refs += role.term_source.name + ';'
                study_contacts_df.loc[j] = [
                    study_contact.last_name,
                    study_contact.first_name,
                    study_contact.mid_initials,
                    study_contact.email,
                    study_contact.phone,
                    study_contact.fax,
                    study_contact.address,
                    study_contact.affiliation,
                    '',  # roles,
                    '',  # roles_accession_numbers,
                    '',  # roles_source_refs
                ]
                j += 1
            study_contacts_df = study_contacts_df.set_index('Study Person Last Name').T
            fp.write('STUDY CONTACTS\n')
            study_contacts_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                     index_label='Study Person Last Name')
        write_study_table_files(investigation, output_path)
        write_assay_table_files(investigation, output_path)

        fp.close()
    else:
        raise NotImplementedError("Dumping this ISA object to ISA Tab is not yet supported")
    return investigation


def _longest_path(G):
    """
    Wrote this myself... woooo, get me!
    """
    start_nodes = list()
    end_nodes = list()
    for node in G.nodes():
        if len(G.in_edges(node)) == 0:
            start_nodes.append(node)
        if len(G.out_edges(node)) == 0:
            end_nodes.append(node)
    from networkx.algorithms import all_simple_paths
    longest = (0, None)
    for start_node in start_nodes:
        for end_node in end_nodes:
            for path in all_simple_paths(G, start_node, end_node):
                if len(path) > longest[0]:
                    longest = (len(path), path)
    return longest[1]

prev = ''  # used in rolling_group(val) in write_assay_table_files(inv_obj, output_dir)


def write_assay_table_files(inv_obj, output_dir):
    """
        Writes out assay table files according to pattern defined by

        Sample Name,
        Protocol Ref: 'sample collection', [ ParameterValue[], ... ],
        Material Name, [ Characteristics[], ... ]
        [ FactorValue[], ... ]


    """
    if isinstance(inv_obj, Investigation):
        for study_obj in inv_obj.studies:
            for assay_obj in study_obj.assays:
                graph = assay_obj.graph
                cols = list()
                mcount = 0
                protrefcount = 0
                prottypes = dict()
                col_map = dict()
                for node in _longest_path(graph):
                    if isinstance(node, Sample):
                        cols.append('sample')
                        col_map['sample'] = 'Sample Name'
                    elif isinstance(node, Material):
                        if node.type == 'Labeled Extract Name':
                            cols.append('lextract')
                            cols.append('lextract_label')
                            cols.append('lextract_label_termsource')
                            cols.append('lextract_label_termaccession')
                            col_map['lextract'] = 'Labeled Extract Name'
                            col_map['lextract_label'] = 'Label'
                            col_map['lextract_label_termsource'] = 'Term Source REF'
                            col_map['lextract_label_termaccession'] = 'Term Accession Number'
                        elif node.type == 'Extract Name':
                            cols.append('extract')
                            col_map['extract'] = 'Extract Name'
                            for c in sorted(node.characteristics, key=lambda x: id(x.category)):
                                if isinstance(c.value, int) or isinstance(c.value, float):
                                    cols.extend(('extract_char[' + c.category.characteristic_type.name + ']',
                                                 'extract_char[' + c.category.characteristic_type.name + ']_unit',
                                                 'extract_char[' + c.category.characteristic_type.name + ']_unit_termsource',
                                                 'extract_char[' + c.category.characteristic_type.name + ']_unit_termaccession',))
                                    col_map['extract_char[' + c.category.characteristic_type.name + ']'] = 'Characteristics[' + c.category.characteristic_type.name + ']'
                                    col_map['extract_char[' + c.category.characteristic_type.name + ']_unit'] = 'Unit'
                                    col_map['extract_char[' + c.category.characteristic_type.name + ']_unit_termsource'] = 'Term Source REF'
                                    col_map['extract_char[' + c.category.characteristic_type.name + ']_unit_termaccession'] = 'Term Accession Number'
                                elif isinstance(c.value, OntologyAnnotation):
                                    cols.extend(('extract_char[' + c.category.characteristic_type.name + ']',
                                                 'extract_char[' + c.category.characteristic_type.name + ']_termsource',
                                                 'extract_char[' + c.category.characteristic_type.name + ']_termaccession',))
                                    col_map['extract_char[' + c.category.characteristic_type.name + ']'] = 'Characteristics[' + c.category.characteristic_type.name + ']'
                                    col_map['extract_char[' + c.category.characteristic_type.name + ']_termsource'] = 'Term Source REF'
                                    col_map['extract_char[' + c.category.characteristic_type.name + ']_termaccession'] = 'Term Accession Number'
                                else:
                                    cols.append('extract_char[' + c.category.characteristic_type.name + ']')
                                    col_map['extract_char[' + c.category.characteristic_type.name + ']'] = 'Characteristics[' + c.category.characteristic_type.name + ']'
                        else:
                            cols.append('material[' + str(mcount) + ']')
                            col_map['material[' + str(mcount) + ']'] = 'Material Name'
                            for c in sorted(node.characteristics, key=lambda x: id(x.category)):
                                if isinstance(c.value, int) or isinstance(c.value, float):
                                    cols.extend(('material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']',
                                                 'material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_unit',
                                                 'material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_unit_termsource',
                                                 'material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_unit_termaccession',))
                                    col_map['material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']'] = 'Characteristics[' + c.category.characteristic_type.name + ']'
                                    col_map['material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_unit'] = 'Unit'
                                    col_map['material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_unit_termsource'] = 'Term Source REF'
                                    col_map['material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_unit_termaccession'] = 'Term Accession Number'
                                elif isinstance(c.value, OntologyAnnotation):
                                    cols.extend(('material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']',
                                                 'material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_termsource',
                                                 'material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_termaccession',))
                                    col_map['material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']'] = 'Characteristics[' + c.category.characteristic_type.name + ']'
                                    col_map['material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_termsource'] = 'Term Source REF'
                                    col_map['material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_termaccession'] = 'Term Accession Number'
                                else:
                                    cols.append('material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']')
                                    col_map['material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']'] = 'Characteristics[' + c.category.characteristic_type.name + ']'
                            mcount += 1
                    elif isinstance(node, Process):
                        cols.append('protocol[' + str(protrefcount) + ']')
                        col_map['protocol[' + str(protrefcount) + ']'] = 'Protocol REF'
                        if node.date is not None:
                            cols.append('protocol[' + str(protrefcount) + ']_date')
                            col_map['protocol[' + str(protrefcount) + ']_date'] = 'Date'
                        if node.performer is not None:
                            cols.append('protocol[' + str(protrefcount) + ']_performer')
                            col_map['protocol[' + str(protrefcount) + ']_performer'] = 'Performer'
                        for prop in reversed(sorted(node.additional_properties.keys())):
                            cols.append('protocol[' + str(protrefcount) + ']_prop[' + prop + ']')
                            col_map['protocol[' + str(protrefcount) + ']_prop[' + prop + ']'] = prop
                        for pv in sorted(node.parameter_values, key=lambda x: id(x.category)):
                            if isinstance(pv.value, int) or isinstance(pv.value, float):
                                cols.extend(('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termsource',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termaccession'))
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = 'Parameter Value[' + pv.category.parameter_name.name + ']'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit'] = 'Unit'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termsource'] = 'Term Source REF'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termaccession'] = 'Term Accession Number'
                            elif isinstance(pv.value, OntologyAnnotation):
                                cols.extend(('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termsource',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termaccession',))
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = 'Parameter Value[' + pv.category.parameter_name.name + ']'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termsource'] = 'Term Source REF'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termaccession'] = 'Term Accession Number'
                            else:
                                cols.append('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']',)
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = 'Parameter Value[' + pv.category.parameter_name.name + ']'
                        for output in [x for x in node.outputs if isinstance(x, DataFile)]:
                            cols.append('data[' + output.label + ']')
                            col_map['data[' + output.label + ']'] = output.label
                        if node.executes_protocol.protocol_type.name not in prottypes.keys():
                            prottypes[node.executes_protocol.protocol_type.name] = protrefcount
                            protrefcount += 1
                    elif isinstance(node, DataFile):
                        pass  # we process DataFile above inside Process
                start_nodes = list()
                end_nodes = list()
                for node in graph.nodes():
                    if len(graph.in_edges(node)) == 0:
                        start_nodes.append(node)
                    if len(graph.out_edges(node)) == 0:
                        end_nodes.append(node)
                import pandas as pd
                df = pd.DataFrame(columns=cols)
                i = 0
                assay_obj.paths = list()
                for start_node in start_nodes:
                    for end_node in end_nodes:
                        for path in list(nx.algorithms.all_simple_paths(graph, start_node, end_node)):
                            mcount = 0
                            compound_key = str()
                            for node in path:
                                if isinstance(node, Sample):
                                    df.loc[i, 'sample'] = node.name
                                    compound_key += node.name + '/'
                                elif isinstance(node, Material):
                                    if node.type == 'Labeled Extract Name':
                                        df.loc[i, 'lextract'] = node.name
                                        compound_key += node.name + '/'
                                        df.loc[i, 'lextract_label'] = node.characteristics[0].value.name
                                        df.loc[i, 'lextract_label_termsource'] =  node.characteristics[0].value.term_source.name
                                        df.loc[i, 'lextract_label_termaccession'] =  node.characteristics[0].value.term_accession
                                    elif node.type == 'Extract Name':
                                        df.loc[i, 'extract'] = node.name
                                        compound_key += node.name + '/'
                                        for c in sorted(node.characteristics, key=lambda x: id(x.category)):
                                            if isinstance(c.value, int) or isinstance(c.value, float):
                                                df.loc[i, 'extract_char[' + c.category.characteristic_type.name + ']'] = c.value
                                                df.loc[i, 'extract_char[' + c.category.characteristic_type.name + ']_unit'] = c.unit.name
                                                df.loc[i, 'extract_char[' + c.category.characteristic_type.name + ']_unit_termsource'] = c.unit.term_source.name
                                                df.loc[i, 'extract_char[' + c.category.characteristic_type.name + ']_unit_termaccession'] = c.unit.term_accession
                                            elif isinstance(c.value, OntologyAnnotation):
                                                df.loc[i, 'extract_char[' + c.category.characteristic_type.name + ']'] = c.value.name
                                                df.loc[i, 'extract_char[' + c.category.characteristic_type.name + ']_termsource'] = c.value.term_source.name
                                                df.loc[i, 'extract_char[' + c.category.characteristic_type.name + ']_termaccession'] = c.value.term_accession
                                            else:
                                                df.loc[i, 'extract_char[' + c.category.characteristic_type.name + ']'] = c.value
                                    else:
                                        df.loc[i, 'material[' + str(mcount) + ']'] = node.name
                                        compound_key += node.name + '/'
                                        for c in sorted(node.characteristics, key=lambda x: id(x.category)):
                                            if isinstance(c.value, int) or isinstance(c.value, float):
                                                df.loc[i, 'material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']'] = c.value
                                                df.loc[i, 'material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_unit'] = c.unit.name
                                                df.loc[i, 'material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_unit_termsource'] = c.unit.term_source.name
                                                df.loc[i, 'material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_unit_termaccession'] = c.unit.term_accession
                                            elif isinstance(c.value, OntologyAnnotation):
                                                df.loc[i, 'material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']'] = c.value.name
                                                df.loc[i, 'material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_termsource'] = c.value.term_source.name
                                                df.loc[i, 'material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']_termaccession'] = c.value.term_accession
                                            else:
                                                df.loc[i, 'material[' + str(mcount) + ']_char[' + c.category.characteristic_type.name + ']'] = c.value
                                        mcount += 1
                                elif isinstance(node, Process):
                                    protrefcount = prottypes[node.executes_protocol.protocol_type.name]
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']'] = node.executes_protocol.name
                                    compound_key += str(protrefcount) + '/' + node.name + '/'
                                    if node.date is not None:
                                        df.loc[i, 'protocol[' + str(protrefcount) + ']_date'] = node.date
                                    if node.performer is not None:
                                        df.loc[i, 'protocol[' + str(protrefcount) + ']_performer'] = node.performer
                                    for prop in reversed(sorted(node.additional_properties.keys())):
                                        df.loc[i, 'protocol[' + str(protrefcount) + ']_prop[' + prop + ']'] = node.additional_properties[prop]
                                        compound_key += str(protrefcount) + '/' + prop + '/' + node.additional_properties[prop]
                                    for pv in sorted(node.parameter_values, key=lambda x: id(x.category)):
                                        if isinstance(pv.value, int) or isinstance(pv.value, float):
                                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = pv.value
                                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit'] = pv.unit.name
                                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termsource'] = pv.unit.term_source.name
                                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termaccession'] = pv.unit.term_accession
                                        elif isinstance(pv.value, OntologyAnnotation):
                                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = pv.value.name
                                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termsource'] = pv.value.term_source.name
                                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termaccession'] = pv.value.term_accession
                                        else:
                                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = pv.value
                                    for output in [x for x in node.outputs if isinstance(x, DataFile)]:
                                        df.loc[i, 'data[' + output.label + ']'] = output.filename
                            df.loc[i, 'compound_key'] = compound_key
                            i += 1

                # reduce rows of data on separate lines

                # can we group by matching all columns minus the data columns?
                import re
                data_regex = re.compile('data\[(.*?)\]')
                # cols_no_data = [col for col in cols if not data_regex.match(col)]  # column list without data cols

                # calculate groupings
                def rolling_group(val):
                    global prev
                    if val != prev:
                        rolling_group.group += 1  # val != prev is signal to switch group; rows sorted by cols_no_data
                    prev = val
                    return rolling_group.group
                rolling_group.group = 0  # static variable
                groups = df.groupby(df['compound_key'].apply(rolling_group), as_index=True)  # groups by column 1 only

                # merge items in column groups
                def reduce(group, column):
                    col = group[column]
                    s = [str(each) for each in col if pd.notnull(each)]
                    if len(s) > 0:
                        return s[0]
                    else:
                        return ''
                df = groups.apply(lambda g: pd.Series([reduce(g, col) for col in g.columns], index=g.columns))

                #  cleanup column headers before writing out df
                # WARNING: don't just dump out col_map.values() as we need to put columns back in order
                df = df.sort_values(by=df.columns[0], ascending=True)  # arbitrary sort on column 0 (Sample name)
                del df['compound_key']  # release compound_key as we don't write it out
                for i, col in enumerate(df.columns):
                    cols[i] = col_map[col]
                    if col_map[col] == 'Characteristics[Material Type]':
                        cols[i] = 'Material Type'
                    if data_regex.match(col) is not None:
                        if data_regex.findall(col)[0] == 'Raw Data File':
                            if assay_obj.technology_type.name == 'DNA microarray':
                                cols[i] = 'Array Data File'
                df.columns = cols  # reset column headers
                # drop completely empty columns
                import numpy as np
                df = df.replace('', np.nan)
                df = df.dropna(axis=1, how='all')
                assay_obj.df = df
                df.to_csv(path_or_buf=open(os.path.join(output_dir, assay_obj.filename), 'w'), index=False, sep='\t', encoding='utf-8',)


def write_study_table_files(inv_obj, output_dir):
    """
        Writes out study table files according to pattern defined by

        Source Name, [ Characteristics[], ... ],
        Protocol Ref*: 'sample collection', [ ParameterValue[], ... ],
        Sample Name, [ Characteristics[], ... ]
        [ FactorValue[], ... ]

        which should be equivalent to studySample.xml in default config

    """
    if isinstance(inv_obj, Investigation):
        for study_obj in inv_obj.studies:
            graph = study_obj.graph
            cols = list()
            protrefcount = 0
            prottypes = dict()
            col_map = dict()
            for node in _longest_path(graph):
                if isinstance(node, Source):
                    cols.append('source')
                    col_map['source'] = 'Source Name'
                    for c in sorted(node.characteristics, key=lambda x: id(x.category)):
                        if isinstance(c.value, int) or isinstance(c.value, float):
                            cols.extend(('source_char[' + c.category.characteristic_type.name + ']',
                                         'source_char[' + c.category.characteristic_type.name + ']_unit',
                                         'source_char[' + c.category.characteristic_type.name + ']_unit_termsource',
                                         'source_char[' + c.category.characteristic_type.name + ']_unit_termaccession',))
                            col_map['source_char[' + c.category.characteristic_type.name + ']'] = 'Characteristics[' + c.category.characteristic_type.name + ']'
                            col_map['source_char[' + c.category.characteristic_type.name + ']_unit'] = 'Unit'
                            col_map['source_char[' + c.category.characteristic_type.name + ']_unit_termsource'] = 'Term Source REF'
                            col_map['source_char[' + c.category.characteristic_type.name + ']_unit_termaccession'] = 'Term Accession Number'
                        elif isinstance(c.value, OntologyAnnotation):
                            cols.extend(('source_char[' + c.category.characteristic_type.name + ']',
                                         'source_char[' + c.category.characteristic_type.name + ']_termsource',
                                         'source_char[' + c.category.characteristic_type.name + ']_termaccession',))
                            col_map['source_char[' + c.category.characteristic_type.name + ']'] = 'Characteristics[' + c.category.characteristic_type.name + ']'
                            col_map['source_char[' + c.category.characteristic_type.name + ']_termsource'] = 'Term Source REF'
                            col_map['source_char[' + c.category.characteristic_type.name + ']_termaccession'] = 'Term Accession Number'
                        else:
                            cols.append('source_char[' + c.category.characteristic_type.name + ']',)
                            col_map['source_char[' + c.category.characteristic_type.name + ']'] = 'Characteristics[' + c.category.characteristic_type.name + ']'
                elif isinstance(node, Process):
                    cols.append('protocol[' + str(protrefcount) + ']')
                    col_map['protocol[' + str(protrefcount) + ']'] = 'Protocol REF'
                    if node.date is not None:
                        cols.append('protocol[' + str(protrefcount) + ']_date')
                        col_map['protocol[' + str(protrefcount) + ']_date'] = 'Date'
                    if node.performer is not None:
                        cols.append('protocol[' + str(protrefcount) + ']_performer')
                        col_map['protocol[' + str(protrefcount) + ']_performer'] = 'Performer'
                    for pv in sorted(node.parameter_values, key=lambda x: id(x.category)):
                        if isinstance(pv.value, int) or isinstance(pv.value, float):
                            cols.extend(('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']',
                                         'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit',
                                         'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termsource',
                                         'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termaccession'))
                            col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = 'Parameter Value[' + pv.category.parameter_name.name + ']'
                            col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit'] = 'Unit'
                            col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termsource'] = 'Term Source REF'
                            col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termaccession'] = 'Term Accession Number'
                        elif isinstance(pv.value, OntologyAnnotation):
                            cols.extend(('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']',
                                         'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termsource',
                                         'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termaccession',))
                            col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = 'Parameter Value[' + pv.category.parameter_name.name + ']'
                            col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termsource'] = 'Term Source REF'
                            col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termaccession'] = 'Term Accession Number'
                        else:
                            cols.append('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']')
                            col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = 'Parameter Value[' + pv.category.parameter_name.name + ']'
                    if node.executes_protocol.protocol_type.name not in prottypes.values():
                        prottypes[protrefcount] = node.executes_protocol.protocol_type.name
                        protrefcount += 1
                elif isinstance(node, Sample):
                    cols.append('sample')
                    col_map['sample'] = 'Sample Name'
                    for c in sorted(node.characteristics, key=lambda x: id(x.category)):
                        if isinstance(c.value, int) or isinstance(c.value, float):
                            cols.extend(('sample_char[' + c.category.characteristic_type.name + ']',
                                         'sample_char[' + c.category.characteristic_type.name + ']_unit',
                                         'sample_char[' + c.category.characteristic_type.name + ']_unit_termsource',
                                         'sample_char[' + c.category.characteristic_type.name + ']_unit_termaccession',))
                            col_map['sample_char[' + c.category.characteristic_type.name + ']'] = 'Characteristics[' + c.category.characteristic_type.name + ']'
                            col_map['sample_char[' + c.category.characteristic_type.name + ']_unit'] = 'Unit'
                            col_map['sample_char[' + c.category.characteristic_type.name + ']_unit_termsource'] = 'Term Source REF'
                            col_map['sample_char[' + c.category.characteristic_type.name + ']_unit_termaccession'] = 'Term Accession Number'
                        elif isinstance(c.value, OntologyAnnotation):
                            cols.extend(('sample_char[' + c.category.characteristic_type.name + ']',
                                         'sample_char[' + c.category.characteristic_type.name + ']_termsource',
                                         'sample_char[' + c.category.characteristic_type.name + ']_termaccession',))
                            col_map['sample_char[' + c.category.characteristic_type.name + ']'] = 'Characteristics[' + c.category.characteristic_type.name + ']'
                            col_map['sample_char[' + c.category.characteristic_type.name + ']_termsource'] = 'Term Source REF'
                            col_map['sample_char[' + c.category.characteristic_type.name + ']_termaccession'] = 'Term Accession Number'
                        else:
                            cols.append('sample_char[' + c.category.characteristic_type.name + ']')
                            col_map['sample_char[' + c.category.characteristic_type.name + ']'] = 'Characteristics[' + c.category.characteristic_type.name + ']'
                    for fv in sorted(node.factor_values, key=lambda x: id(x.factor_name)):
                        if isinstance(fv.value, int) or isinstance(fv.value, float):
                            cols.extend(('sample_fv[' + fv.factor_name.name + ']',
                                         'sample_fv[' + fv.factor_name.name + ']_unit',
                                         'sample_fv[' + fv.factor_name.name + ']_unit_termsource',
                                         'sample_fv[' + fv.factor_name.name + ']_unit_termaccession',))
                            col_map['sample_fv[' + fv.factor_name.name + ']'] = 'Factor Value[' + fv.factor_name.name + ']'
                            col_map['sample_fv[' + fv.factor_name.name + ']_unit'] = 'Unit'
                            col_map['sample_fv[' + fv.factor_name.name + ']_unit_termsource'] = 'Term Source REF'
                            col_map['sample_fv[' + fv.factor_name.name + ']_unit_termaccession'] = 'Term Accession Number'
                        elif isinstance(fv.value, OntologyAnnotation):
                            cols.extend(('sample_fv[' + fv.factor_name.name + ']',
                                         'sample_fv[' + fv.factor_name.name + ']_termsource',
                                         'sample_fv[' + fv.factor_name.name + ']_termaccession',))
                            col_map['sample_fv[' + fv.factor_name.name + ']'] = 'Factor Value[' + fv.factor_name.name + ']'
                            col_map['sample_fv[' + fv.factor_name.name + ']_termsource'] = 'Term Source REF'
                            col_map['sample_fv[' + fv.factor_name.name + ']_termaccession'] = 'Term Accession Number'
                        else:
                            cols.append('sample_fv[' + fv.factor_name.name + ']')
                            col_map['sample_fv[' + fv.factor_name.name + ']'] = 'Factor Value[' + fv.factor_name.name + ']'
            start_nodes = list()
            end_nodes = list()
            for node in graph.nodes():
                if len(graph.in_edges(node)) == 0:
                    start_nodes.append(node)
                if len(graph.out_edges(node)) == 0:
                    end_nodes.append(node)
            import pandas as pd
            df = pd.DataFrame(columns=cols)
            i = 0
            for start_node in start_nodes:
                for end_node in end_nodes:
                    paths = list(nx.algorithms.all_simple_paths(graph, start_node, end_node))
                    for path in paths:
                        for node in path:
                            if isinstance(node, Source):
                                df.loc[i, 'source'] = node.name
                                for c in sorted(node.characteristics, key=lambda x: id(x.category)):
                                    if isinstance(c.value, int) or isinstance(c.value, float):
                                        df.loc[i, 'source_char[' + c.category.characteristic_type.name + ']'] = c.value
                                        df.loc[i, 'source_char[' + c.category.characteristic_type.name + ']_unit'] = c.unit.name
                                        df.loc[i, 'source_char[' + c.category.characteristic_type.name + ']_unit_termsource'] = c.unit.term_source.name
                                        df.loc[i, 'source_char[' + c.category.characteristic_type.name + ']_unit_termaccession'] = c.unit.term_accession
                                    elif isinstance(c.value, OntologyAnnotation):
                                        df.loc[i, 'source_char[' + c.category.characteristic_type.name + ']'] = c.value.name
                                        df.loc[i, 'source_char[' + c.category.characteristic_type.name + ']_termsource'] = c.value.term_source.name
                                        df.loc[i, 'source_char[' + c.category.characteristic_type.name + ']_termaccession'] = c.value.term_accession
                                    else:
                                        df.loc[i, 'source_char[' + c.category.characteristic_type.name + ']'] = c.value
                            elif isinstance(node, Process):
                                def find(n):
                                    k = 0
                                    for k, v in prottypes.items():
                                        if v == n.executes_protocol.protocol_type.name:
                                            return k
                                    return k
                                protrefcount = find(node)
                                df.loc[i, 'protocol[' + str(protrefcount) + ']'] = node.executes_protocol.name
                                if node.date is not None:
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_date'] = node.date
                                if node.performer is not None:
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_performer'] = node.performer
                                for pv in sorted(node.parameter_values, key=lambda x: id(x.category)):
                                    if isinstance(pv.value, int) or isinstance(pv.value, float):
                                        df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = pv.value
                                        df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit'] = pv.unit.name
                                        df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termsource'] = pv.unit.term_source.name
                                        df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termaccession'] = pv.unit.term_accession
                                    elif isinstance(pv.value, OntologyAnnotation):
                                        df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = pv.value.name
                                        df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termsource'] = pv.value.term_source
                                        df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termaccession'] = pv.value.term_accession
                                    else:
                                        df.loc[i, i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.characteristic_type.name + ']'] = pv.value
                            elif isinstance(node, Sample):
                                df.loc[i, 'sample'] = node.name
                                for c in sorted(node.characteristics, key=lambda x: id(x.category)):
                                    if isinstance(c.value, int) or isinstance(c.value, float):
                                        df.loc[i, 'sample_char[' + c.category.characteristic_type.name + ']'] = c.value
                                        df.loc[i, 'sample_char[' + c.category.characteristic_type.name + ']_unit'] = c.unit.name
                                        df.loc[i, 'sample_char[' + c.category.characteristic_type.name + ']_unit_termsource'] = c.unit.term_source.name
                                        df.loc[i, 'sample_char[' + c.category.characteristic_type.name + ']_unit_termaccession'] = c.unit.term_accession
                                    elif isinstance(c.value, OntologyAnnotation):
                                        df.loc[i, 'sample_char[' + c.category.characteristic_type.name + ']'] = c.value.name
                                        df.loc[i, 'sample_char[' + c.category.characteristic_type.name + ']_termsource'] = c.value.term_source.name
                                        df.loc[i, 'sample_char[' + c.category.characteristic_type.name + ']_termaccession'] = c.value.term_accession
                                    else:
                                        df.loc[i, 'sample_char[' + c.category.characteristic_type.name + ']'] = c.value
                                for fv in sorted(node.factor_values, key=lambda x: id(x.factor_name)):
                                    if isinstance(fv.value, int) or isinstance(fv.value, float):
                                        df.loc[i, 'sample_fv[' + fv.factor_name.name + ']'] = fv.value
                                        df.loc[i, 'sample_fv[' + fv.factor_name.name + ']_unit'] = fv.unit.name
                                        df.loc[i, 'sample_fv[' + fv.factor_name.name + ']_unit_termsource'] = fv.unit.term_source.name
                                        df.loc[i, 'sample_fv[' + fv.factor_name.name + ']_unit_termaccession'] = fv.unit.term_accession
                                    elif isinstance(fv.value, OntologyAnnotation):
                                        df.loc[i, 'sample_fv[' + fv.factor_name.name + ']'] = fv.value.name
                                        df.loc[i, 'sample_fv[' + fv.factor_name.name + ']_termsource'] = fv.value.term_source.name
                                        df.loc[i, 'sample_fv[' + fv.factor_name.name + ']_termaccession'] = fv.value.term_accession
                                    else:
                                        df.loc[i, 'sample_fv[' + fv.factor_name.name + ']'] = fv.value
                        i += 1
            #  cleanup column headers before writing out df
            import re
            char_regex = re.compile('.*_char\[(.*?)\]')
            pv_regex = re.compile('.*_pv\[(.*?)\]')
            fv_regex = re.compile('.*_fv\[(.*?)\]')
            # WARNING: don't just dump out col_map.values() as we need to put columns back in order
            for i, col in enumerate(cols):
                cols[i] = col_map[col]
                if char_regex.match(col) is not None:
                    if char_regex.findall(col)[0] == 'Material Type':
                        cols[i] = 'Material Type'
            df.columns = cols  # reset column headers
            import numpy as np
            df = df.replace('', np.nan)
            df = df.dropna(axis=1, how='all')
            df = df.sort_values(by=df.columns[0], ascending=True)  # arbitrary sort on column 0
            df.to_csv(path_or_buf=open(os.path.join(output_dir, study_obj.filename), 'w'), index=False, sep='\t', encoding='utf-8',)
    else:
        raise IOError("Input object is not a valid Investigation object")


def assertTabEqual(fp_x, fp_y):
    def diff(a, b):
        b = set(b)
        return [aa for aa in a if aa not in b]
    """
    Test for equality of tab files, only down to level of content - should not be taken as canonical equality, but
    rather that all the expected content matches to both input files
    :param fp_x: File descriptor of a ISAtab file
    :param fp_y: File descriptor of another  ISAtab file
    :return: True or False plus any AssertionErrors
    """
    import numpy as np
    df_x = pd.read_csv(fp_x, sep='\t', encoding='utf-8')
    df_y = pd.read_csv(fp_y, sep='\t', encoding='utf-8')
    try:
        # drop empty columns
        df_x = df_x.replace('', np.nan)
        df_x = df_x.dropna(axis=1, how='all')
        df_y = df_y.replace('', np.nan)
        df_y = df_y.dropna(axis=1, how='all')

        is_cols_equal = set([x.split('.', 1)[0] for x in df_x.columns]) == set([x.split('.', 1)[0] for x in df_y.columns])
        if not is_cols_equal:
            print('x: ' + df_x.columns)
            print('y: ' + df_y.columns)
            print(diff(df_x.columns, df_y.columns))
            raise AssertionError("Columns in x do not match those in y")

        # reindex to add contexts for duplicate named columns (i.e. Term Accession Number, Unit, etc.)
        import re
        char_regex = re.compile('Characteristics\[(.*?)\]')
        pv_regex = re.compile('Parameter Value\[(.*?)\]')
        fv_regex = re.compile('Factor Value\[(.*?)\]')
        newcolsx = list()
        for col in df_x.columns:
            newcolsx.append(col)
        for i, col in enumerate(df_x.columns):
            if char_regex.match(col) or pv_regex.match(col) or fv_regex.match(col):
                try:
                    if 'Unit' in df_x.columns[i+1]:
                        newcolsx[i+1] = col + '/Unit'
                        if 'Term Source REF' in df_x.columns[i+2]:
                            newcolsx[i+2] = col + '/Unit/Term Source REF'
                        if 'Term Accession Number' in df_x.columns[i+3]:
                            newcolsx[i+3] = col + '/Unit/Term Accession Number'
                    elif 'Term Source REF' in df_x.columns[i+1]:
                        newcolsx[i+1] = col + '/Term Source REF'
                        if 'Term Accession Number' in df_x.columns[i+2]:
                            newcolsx[i+2] = col + '/Term Accession Number'
                except IndexError:
                    pass
        df_x.columns = newcolsx
        newcolsy = list()
        for col in df_y.columns:
            newcolsy.append(col)
        for i, col in enumerate(df_y.columns):
            if char_regex.match(col) or pv_regex.match(col) or fv_regex.match(col):
                try:
                    if 'Unit' in df_y.columns[i+1]:
                        newcolsy[i+1] = col + '/Unit'
                        if 'Term Source REF' in df_y.columns[i+2]:
                            newcolsy[i+2] = col + '/Unit/Term Source REF'
                        if 'Term Accession Number' in df_y.columns[i+3]:
                            newcolsy[i+3] = col + '/Unit/Term Accession Number'
                    elif 'Term Source REF' in df_y.columns[i+1]:
                        newcolsy[i+1] = col + '/Term Source REF'
                        if 'Term Accession Number' in df_y.columns[i+2]:
                            newcolsy[i+2] = col + '/Term Accession Number'
                except IndexError:
                    pass
        df_y.columns = newcolsy
        for colx in df_x.columns:
            for eachx, eachy in zip(df_x[colx], df_y[colx]):
                if eachx != eachy:
                    print(df_x[colx])
                    print(df_y[colx])
                    raise AssertionError("Value: " + str(eachx) + ", does not match: " + str(eachy))
        print("Well, you got here so the files must be same-ish... well done, you!")
        return True
    except AssertionError as e:
        print(str(e))
        return False


def read_investigation_file(fp):

    def _peek(f):
        position = f.tell()
        l = f.readline()
        f.seek(position)
        return l

    def _read_tab_section(f, sec_key, next_sec_key=None):

        line = f.readline()
        if not line.rstrip() == sec_key:
            raise IOError("Expected: " + sec_key + " section, but got: " + line)
        memf = io.StringIO()
        while not _peek(f=f).rstrip() == next_sec_key:
            line = f.readline()
            if not line:
                break
            memf.write(line)
        memf.seek(0)
        return memf

    def _build_section_df(f):
        import numpy as np
        df = pd.read_csv(f, sep='\t').T  # Load and transpose ISA file section
        df.replace(np.nan, '', regex=True, inplace=True)  # Strip out the nan entries
        df.reset_index(inplace=True)  # Reset index so it is accessible as column
        df.columns = df.iloc[0]  # If all was OK, promote this row to the column headers
        df = df.reindex(df.index.drop(0))  # Reindex the DataFrame
        return df

    # Read in investigation file into DataFrames first
    ontology_sources_df = _build_section_df(_read_tab_section(
        f=fp,
        sec_key='ONTOLOGY SOURCE REFERENCE',
        next_sec_key='INVESTIGATION'
    ))
    # assert({'Term Source Name', 'Term Source File', 'Term Source Version', 'Term Source Description'}
    #        .issubset(set(ontology_sources_df.columns.values)))  # Check required labels are present
    investigation_df = _build_section_df(_read_tab_section(
        f=fp,
        sec_key='INVESTIGATION',
        next_sec_key='INVESTIGATION PUBLICATIONS'
    ))
    investigation_publications_df = _build_section_df(_read_tab_section(
        f=fp,
        sec_key='INVESTIGATION PUBLICATIONS',
        next_sec_key='INVESTIGATION CONTACTS'
    ))
    investigation_contacts_df = _build_section_df(_read_tab_section(
        f=fp,
        sec_key='INVESTIGATION CONTACTS',
        next_sec_key='STUDY'
    ))
    study_df_list = list()
    study_design_descriptors_df_list = list()
    study_publications_df_list = list()
    study_factors_df_list = list()
    study_assays_df_list = list()
    study_protocols_df_list = list()
    study_contacts_df_list = list()
    while _peek(fp):  # Iterate through STUDY blocks until end of file
        study_df_list.append(_build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY',
            next_sec_key='STUDY DESIGN DESCRIPTORS'
        )))
        study_design_descriptors_df_list.append(_build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY DESIGN DESCRIPTORS',
            next_sec_key='STUDY PUBLICATIONS'
        )))
        study_publications_df_list.append(_build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY PUBLICATIONS',
            next_sec_key='STUDY FACTORS'
        )))
        study_factors_df_list.append(_build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY FACTORS',
            next_sec_key='STUDY ASSAYS'
        )))
        study_assays_df_list.append(_build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY ASSAYS',
            next_sec_key='STUDY PROTOCOLS'
        )))
        study_protocols_df_list.append(_build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY PROTOCOLS',
            next_sec_key='STUDY CONTACTS'
        )))
        study_contacts_df_list.append(_build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY CONTACTS',
            next_sec_key='STUDY'
        )))

    # # Start building the object model
    # ontology_source_references = list()
    # for x in ontology_sources_df.iterrows():  # Iterate over the rows to build our OntologySourceReference objs
    #     ontology_source_data = x[1]  # Get data out of df row
    #     ontology_source = OntologySourceReference(
    #         name=ontology_source_data['Term Source Name'],
    #         file=ontology_source_data['Term Source File'],
    #         version=ontology_source_data['Term Source Version'],
    #         description=ontology_source_data['Term Source Description']
    #     )
    #     print(ontology_source.to_json())
    #     ontology_source_references.append(ontology_source)
    # investigation_data = investigation_df.loc[1]
    # investigation = Investigation(
    #     identifier=investigation_data['Investigation Identifier'],
    #     title=investigation_data['Investigation Title'],
    #     description=investigation_data['Investigation Description'],
    #     submission_date=investigation_data['Investigation Submission Date'],
    #     public_release_date=investigation_data['Investigation Public Release Date'],
    # )
    # for x in investigation_publications_df.iterrows():
    #     investigation_publication_data = x[1]
    #     investigation_publication = Publication(
    #         pubmed_id=investigation_publication_data['Investigation PubMed ID'],
    #         doi=investigation_publication_data['Investigation Publication DOI'],
    #         author_list=investigation_publication_data['Investigation Publication Author List'],
    #         title=investigation_publication_data['Investigation Publication Title'],
    #         status=OntologyAnnotation(
    #             name=investigation_publication_data['Investigation Publication Status'],
    #             term_accession=investigation_publication_data['Investigation Publication Status Term Accession'],
    #             term_source=investigation_publication_data['Investigation Publication Status Term Source REF'],
    #         )
    #     )
    #     investigation.publications.append(investigation_publication)
    return investigation_df


def read_study_file(fp):
    import re

    def _read_study_record_line(column_names, row_):
        characteristics_regex = re.compile('Characteristics\[(.*?)\]')
        factor_value_regex = re.compile('Factor Value\[(.*?)\]')
        if len(column_names) != len(row_):
            raise IOError
        source_ = Source()
        sample_ = Sample()
        for index, value in enumerate(column_names):
            if value == 'Source Name':
                source_.name = row_[index]
            if value == 'Sample Name':
                sample_.name = row_[index]
            if value == 'Material Type':
                pass
            if value == 'Protocol REF':
                processing_event_ = Process(
                    executes_protocol=row_[index],
                )
                try:
                    peek_column = column_names[index+1]
                    if peek_column == 'Date':
                        processing_event_.date_ = row_[index+1]
                        peek_column = column_names[index+2]
                        if peek_column == 'Performer':
                            processing_event_.performer = row_[index+2]
                    if peek_column == 'Performer':
                        processing_event_.performer = row_[index+1]
                        if peek_column == 'Date':
                            processing_event_.date = row_[index+2]
                except IndexError:
                    pass
            if characteristics_regex.match(value):
                characteristic = Characteristic()
                characteristic.category = characteristics_regex.findall(value)[0]
                try:
                    peek_column = column_names[index+1]
                    if peek_column == 'Term Source REF':
                        characteristic.value = OntologyAnnotation(
                            name=row_[index],
                            term_source=row_[index+1],
                            term_accession=row_[index+2],
                        )
                    else:
                        characteristic.value = row_[index]
                except IndexError:
                    pass
                finally:
                    if sample_.name == '':
                        source_.characteristics.append(characteristic)
                    else:
                        sample_.characteristics.append(characteristic)
            if factor_value_regex.match(value):
                factor_value = FactorValue()
                factor_value.factor_name = factor_value_regex.findall(value)[0]
                try:
                    peek_column = column_names[index+1]
                    if peek_column == 'Term Source REF':
                        factor_value.value = OntologyAnnotation(
                            name=row_[index],
                            term_source=row_[index+1],
                            term_accession=row_[index+2],
                        )
                    elif peek_column == 'Unit':
                        factor_value.value = row_[index]
                        factor_value.unit = OntologyAnnotation(
                            name=row_[index+1],
                            term_source=row_[index+2],
                            term_accession=row_[index+3],
                        )
                except IndexError:
                    pass
                finally:
                    sample_.factor_values.append(factor_value)
        return source_, sample_, processing_event_

    import csv
    study_reader = csv.reader(fp, delimiter='\t')
    fieldnames = next(study_reader)
    experimental_graph = dict()
    for row in study_reader:
        source, sample, processing_event = _read_study_record_line(column_names=fieldnames, row_=row)
        try:
            experimental_graph[source].append(processing_event)
        except KeyError:
            experimental_graph[source] = list()
            experimental_graph[source].append(processing_event)
        try:
            experimental_graph[processing_event].append(sample)
        except KeyError:
            experimental_graph[processing_event] = list()
            experimental_graph[processing_event].append(sample)
    return experimental_graph
