# coding: utf-8
from __future__ import absolute_import, unicode_literals

import json
import logging
import itertools
import networkx as nx
from jsonschema import Draft4Validator, RefResolver, ValidationError
import os
import glob
import six
import functools

from .model.v1 import *

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# This will remove the "'U' flag is deprecated" DeprecationWarning in Python3
open = functools.partial(open, mode='r') if six.PY3 else functools.partial(open, mode='rbU')

errors = list()
warnings = list()



def load(fp):

    def get_comments(j):
        comments = None
        if 'comments' in j.keys():
            comments = list()
            for comment_json in j['comments']:
                name = comment_json['name']
                value = comment_json['value']
                comment = Comment(name, value)
                comments.append(comment)
        return comments

    def get_roles(j):
        roles = None
        if 'roles' in j.keys():
            roles = list()
            for role_json in j['roles']:
                term = role_json['annotationValue']
                term_accession = role_json['termAccession']
                term_source = term_source_dict[role_json['termSource']]
                role = OntologyAnnotation(term, term_source, term_accession)
                roles.append(role)
        return roles

    def _build_assay_graph(process_sequence=list()):
        G = nx.DiGraph()
        for process in process_sequence:
            if process.next_process is not None or process.outputs:  # first check if there's some valid outputs to connect
                if process.outputs:
                    for output in (n for n in process.outputs if not isinstance(n, DataFile)):
                        G.add_edge(process, output)
                else:  # otherwise just connect the process to the next one
                    G.add_edge(process, process.next_process)
            if process.prev_process is not None or process.inputs:
                if process.inputs:
                    for input_ in process.inputs:
                        G.add_edge(input_, process)
                else:
                    G.add_edge(process.prev_process, process)
        return G

    def get_jvalue(d, key):
        try:
            return d[key]
        except KeyError:
            return None

    investigation_json = json.load(fp)
    investigation = Investigation(
        identifier=investigation_json['identifier'],
        title=investigation_json['title'],
        description=investigation_json['description'],
        submission_date=investigation_json['submissionDate'],
        public_release_date=investigation_json['publicReleaseDate']
    )
    investigation.comments = get_comments(investigation_json)
    term_source_dict = {'': None}
    for ontologySourceReference_json in investigation_json['ontologySourceReferences']:
        ontology_source_reference = OntologySource(
            name=ontologySourceReference_json['name'],
            file=ontologySourceReference_json['file'],
            version=ontologySourceReference_json['version'],
            description=ontologySourceReference_json['description']
        )
        term_source_dict[ontology_source_reference.name] = ontology_source_reference
        investigation.ontology_source_references.append(ontology_source_reference)
    for publication_json in investigation_json['publications']:
        publication = Publication(
            pubmed_id=publication_json['pubMedID'],
            doi=publication_json['doi'],
            author_list=publication_json['authorList'],
            title=publication_json['title'],
            status=OntologyAnnotation(
                term=publication_json['status']['annotationValue'],
                term_accession=publication_json['status']['termAccession'],
                term_source=term_source_dict[publication_json['status']['termSource']]
            )
        )
        try:
            publication.comments = get_comments(publication_json)
        except KeyError:
            pass
        investigation.publications.append(publication)
    for person_json in investigation_json['people']:
        person = Person(
            last_name=person_json['lastName'],
            first_name=person_json['firstName'],
            mid_initials=person_json['midInitials'],
            email=person_json['email'],
            phone=person_json['phone'],
            fax=person_json['fax'],
            address=person_json['address'],
            affiliation=person_json['affiliation'],
        )
        for role_json in person_json['roles']:
            role = OntologyAnnotation(
                term=role_json['annotationValue'],
                term_accession=role_json['termAccession'],
                term_source=term_source_dict[role_json['termSource']]
            )
            person.roles.append(role)
        person.comments = get_comments(person_json)
        investigation.contacts.append(person)
    samples_dict = {}
    sources_dict = {}
    categories_dict = {}
    protocols_dict = {}
    factors_dict = {}
    parameters_dict = {}
    units_dict = {}
    process_dict = {}

    # populate assay characteristicCategories first
    for study_json in investigation_json['studies']:
        for assay_json in study_json['assays']:
            for assay_characteristics_category_json in assay_json['characteristicCategories']:
                characteristic_category = OntologyAnnotation(
                    id_=assay_characteristics_category_json['@id'],
                    term=assay_characteristics_category_json['characteristicType']['annotationValue'],
                    term_source=term_source_dict[assay_characteristics_category_json['characteristicType']['termSource']],
                    term_accession=assay_characteristics_category_json['characteristicType']['termAccession'],
                )
                # study.characteristic_categories.append(characteristic_category)
                categories_dict[characteristic_category.id] = characteristic_category
    for study_json in investigation_json['studies']:
        process_dict = dict()
        study = Study(
            identifier=study_json['identifier'],
            title=study_json['title'],
            description=study_json['description'],
            submission_date=study_json['submissionDate'],
            public_release_date=study_json['publicReleaseDate'],
            filename=study_json['filename']
        )
        try:
            study.comments = get_comments(study_json)
        except KeyError:
            pass
        for study_characteristics_category_json in study_json['characteristicCategories']:
            characteristic_category = OntologyAnnotation(
                id_=study_characteristics_category_json['@id'],
                term=study_characteristics_category_json['characteristicType']['annotationValue'],
                term_source=term_source_dict[study_characteristics_category_json['characteristicType']['termSource']],
                term_accession=study_characteristics_category_json['characteristicType']['termAccession'],
            )
            study.characteristic_categories.append(characteristic_category)
            categories_dict[characteristic_category.id] = characteristic_category
        for study_unit_json in study_json['unitCategories']:
            unit = OntologyAnnotation(id_=study_unit_json['@id'],
                                      term=study_unit_json['annotationValue'],
                                      term_source=term_source_dict[study_unit_json['termSource']],
                                      term_accession=study_unit_json['termAccession'])
            units_dict[unit.id] = unit
        for study_publication_json in study_json['publications']:
            study_publication = Publication(
                pubmed_id=study_publication_json['pubMedID'],
                doi=study_publication_json['doi'],
                author_list=study_publication_json['authorList'],
                title=study_publication_json['title'],
                status=OntologyAnnotation(
                    term=study_publication_json['status']['annotationValue'],
                    term_source=term_source_dict[study_publication_json['status']['termSource']],
                    term_accession=study_publication_json['status']['termAccession'],
                )
            )
            try:
                study_publication.comments = get_comments(study_publication_json)
            except KeyError:
                pass
            study.publications.append(study_publication)
        for study_person_json in study_json['people']:
            study_person = Person(
                last_name=study_person_json['lastName'],
                first_name=study_person_json['firstName'],
                mid_initials=study_person_json['midInitials'],
                email=study_person_json['email'],
                phone=study_person_json['phone'],
                fax=study_person_json['fax'],
                address=study_person_json['address'],
                affiliation=study_person_json['affiliation'],
            )
            study_person.roles = get_roles(study_person_json)
            try:
                study_person.comments = get_comments(study_person_json)
            except KeyError:
                pass
            study.contacts.append(study_person)
        for design_descriptor_json in study_json['studyDesignDescriptors']:
            design_descriptor = OntologyAnnotation(
                term=design_descriptor_json['annotationValue'],
                term_accession=design_descriptor_json['termAccession'],
                term_source=term_source_dict[design_descriptor_json['termSource']]
            )
            study.design_descriptors.append(design_descriptor)
        for protocol_json in study_json['protocols']:
            protocol = Protocol(
                id_=protocol_json['@id'],
                name=protocol_json['name'],
                uri=protocol_json['uri'],
                description=protocol_json['description'],
                version=protocol_json['version'],
                protocol_type=OntologyAnnotation(
                    term=protocol_json['protocolType']['annotationValue'],
                    term_accession=protocol_json['protocolType']['termAccession'],
                    term_source=term_source_dict[protocol_json['protocolType']['termSource']]
                )
            )
            for parameter_json in protocol_json['parameters']:
                parameter = ProtocolParameter(
                    id_=parameter_json['@id'],
                    parameter_name=OntologyAnnotation(
                        term=parameter_json['parameterName']['annotationValue'],
                        term_source=term_source_dict[parameter_json['parameterName']['termSource']],
                        term_accession=parameter_json['parameterName']['termAccession']
                    )
                )
                protocol.parameters.append(parameter)
                parameters_dict[parameter.id] = parameter
            for component_json in protocol_json['components']:
                component = ProtocolComponent(
                    name=component_json['componentName'],
                    component_type=OntologyAnnotation(
                        term=component_json['componentType']['annotationValue'],
                        term_source=term_source_dict[component_json['componentType']['termSource']],
                        term_accession=component_json['componentType']['termAccession']
                    )
                )
                protocol.components.append(component)
            study.protocols.append(protocol)
            protocols_dict[protocol.id] = protocol
        for factor_json in study_json['factors']:
            factor = StudyFactor(
                id_=factor_json['@id'],
                name=factor_json['factorName'],
                factor_type=OntologyAnnotation(
                    term=factor_json['factorType']['annotationValue'],
                    term_accession=factor_json['factorType']['termAccession'],
                    term_source=term_source_dict[factor_json['factorType']['termSource']]
                )
            )
            study.factors.append(factor)
            factors_dict[factor.id] = factor
        for source_json in study_json['materials']['sources']:
            source = Source(
                id_=source_json['@id'],
                name=source_json['name'][7:],
            )
            for characteristic_json in source_json['characteristics']:
                value = characteristic_json['value']
                unit = None
                characteristic = Characteristic(category=categories_dict[characteristic_json['category']['@id']],)
                if isinstance(value, dict):
                    try:
                        term = characteristic_json['value']['annotationValue']
                        if isinstance(term, (int, float)):
                            term = str(term)
                        value = OntologyAnnotation(
                            term=term,
                            term_source=term_source_dict[characteristic_json['value']['termSource']],
                            term_accession=characteristic_json['value']['termAccession'])
                    except KeyError:
                        raise IOError("Can't create value as annotation")
                elif isinstance(value, (int, float)):
                    try:
                        unit = units_dict[characteristic_json['unit']['@id']]
                    except KeyError:
                    	unit = None
                        #raise IOError("Can't create unit annotation")
                elif not isinstance(value, six.text_type):
                    raise IOError("Unexpected type in characteristic value")
                characteristic.value = value
                characteristic.unit = unit
                source.characteristics.append(characteristic)
            sources_dict[source.id] = source
            study.materials['sources'].append(source)
        for sample_json in study_json['materials']['samples']:
            sample = Sample(
                id_=sample_json['@id'],
                name=sample_json['name'][7:],
                derives_from=sample_json['derivesFrom']
            )
            for characteristic_json in sample_json['characteristics']:
                value = characteristic_json['value']
                unit = None
                characteristic = Characteristic(
                        category=categories_dict[characteristic_json['category']['@id']])
                if isinstance(value, dict):
                    try:
                        value = OntologyAnnotation(
                            term=characteristic_json['value']['annotationValue'],
                            term_source=term_source_dict[characteristic_json['value']['termSource']],
                            term_accession=characteristic_json['value']['termAccession'])
                    except KeyError:
                        raise IOError("Can't create value as annotation")
                elif isinstance(value, (int, float)):
                    try:
                        unit = units_dict[characteristic_json['unit']['@id']]
                    except KeyError:
                        raise IOError("Can't create unit annotation")
                elif not isinstance(value, six.text_type):
                    raise IOError("Unexpected type in characteristic value")
                characteristic.value = value
                characteristic.unit = unit
                sample.characteristics.append(characteristic)
            for factor_value_json in sample_json['factorValues']:
                try:
                    factor_value = FactorValue(
                        factor_name=factors_dict[factor_value_json['category']['@id']],
                        value=OntologyAnnotation(
                            term=factor_value_json['value']['annotationValue'],
                            term_accession=factor_value_json['value']['termAccession'],
                            term_source=term_source_dict[factor_value_json['value']['termSource']],
                        ),

                    )
                except TypeError:
                    factor_value = FactorValue(
                        factor_name=factors_dict[factor_value_json['category']['@id']],
                        value=factor_value_json['value'],
                        unit=units_dict[factor_value_json['unit']['@id']],
                    )
                sample.factor_values.append(factor_value)
            samples_dict[sample.id] = sample
            study.materials['samples'].append(sample)
        for study_process_json in study_json['processSequence']:
            process = Process(
                id_=study_process_json['@id'],
                executes_protocol=protocols_dict[study_process_json['executesProtocol']['@id']],
            )
            try:
                process.comments = get_comments(study_process_json)
            except KeyError:
                pass
            try:
                process.date = study_process_json['date']
            except KeyError:
                pass
            try:
                process.performer = study_process_json['performer']
            except KeyError:
                pass
            for parameter_value_json in study_process_json['parameterValues']:
                if isinstance(parameter_value_json['value'], (int, float)):
                    parameter_value = ParameterValue(
                        category=parameters_dict[parameter_value_json['category']['@id']],
                        value=parameter_value_json['value'],
                        unit=units_dict[parameter_value_json['unit']['@id']],
                    )
                    process.parameter_values.append(parameter_value)
                else:
                    parameter_value = ParameterValue(
                        category=parameters_dict[parameter_value_json['category']['@id']],
                        )
                    try:
                        parameter_value.value = OntologyAnnotation(
                            term=parameter_value_json['value']['annotationValue'],
                            term_accession=parameter_value_json['value']['termAccession'],
                            term_source=term_source_dict[parameter_value_json['value']['termSource']],)
                    except TypeError:
                        parameter_value.value = parameter_value_json['value']
                    process.parameter_values.append(parameter_value)
            for input_json in study_process_json['inputs']:
                input_ = None
                try:
                    input_ = sources_dict[input_json['@id']]
                except KeyError:
                    pass
                finally:
                    try:
                        input_ = samples_dict[input_json['@id']]
                    except KeyError:
                        pass
                if input_ is None:
                    raise IOError("Could not find input node in sources or samples dicts: " + input_json['@id'])
                process.inputs.append(input_)
            for output_json in study_process_json['outputs']:
                output = None
                try:
                    output = sources_dict[output_json['@id']]
                except KeyError:
                    pass
                finally:
                    try:
                        output = samples_dict[output_json['@id']]
                    except KeyError:
                        pass
                if output is None:
                    raise IOError("Could not find output node in sources or samples dicts: " + output_json['@id'])
                process.outputs.append(output)
            study.process_sequence.append(process)
            process_dict[process.id] = process
        for study_process_json in study_json['processSequence']:  # 2nd pass
            try:
                prev_proc = study_process_json['previousProcess']['@id']
                process_dict[study_process_json['@id']].prev_process = process_dict[prev_proc]
            except KeyError:
                pass
            try:
                next_proc = study_process_json['nextProcess']['@id']
                process_dict[study_process_json['@id']].next_process = process_dict[next_proc]
            except KeyError:
                pass
        # study.graph = _build_assay_graph(study.process_sequence)
        for assay_json in study_json['assays']:
            process_dict = dict()
            assay = Assay(
                measurement_type=OntologyAnnotation(
                    term=assay_json['measurementType']['annotationValue'],
                    term_accession=assay_json['measurementType']['termAccession'],
                    term_source=term_source_dict[assay_json['measurementType']['termSource']]
                ),
                technology_type=OntologyAnnotation(
                    term=assay_json['technologyType']['annotationValue'],
                    term_accession=assay_json['technologyType']['termAccession'],
                    term_source=term_source_dict[assay_json['technologyType']['termSource']]
                ),
                technology_platform=assay_json['technologyPlatform'],
                filename=assay_json['filename']
            )
            for assay_unit_json in assay_json['unitCategories']:
                unit = OntologyAnnotation(id_=assay_unit_json['@id'],
                                          term=assay_unit_json['annotationValue'],
                                          term_source=term_source_dict[assay_unit_json['termSource']],
                                          term_accession=assay_unit_json['termAccession'])
                units_dict[unit.id] = unit
            data_dict = {}
            for data_json in assay_json['dataFiles']:
                data_file = DataFile(
                    id_=data_json['@id'],
                    filename=data_json['name'],
                    label=data_json['type'],
                )
                try:
                    data_file.comments = get_comments(data_json)
                except KeyError:
                    pass
                data_dict[data_file.id] = data_file
                assay.data_files.append(data_file)
            for sample_json in assay_json['materials']['samples']:
                sample = samples_dict[sample_json['@id']]
                assay.materials['samples'].append(sample)
            for assay_characteristics_category_json in assay_json['characteristicCategories']:
                characteristic_category =OntologyAnnotation(
                    id_=assay_characteristics_category_json['@id'],
                    term=assay_characteristics_category_json['characteristicType']['annotationValue'],
                    term_source=term_source_dict[assay_characteristics_category_json['characteristicType']['termSource']],
                    term_accession=assay_characteristics_category_json['characteristicType']['termAccession'],
                )
                study.characteristic_categories.append(characteristic_category)
                categories_dict[characteristic_category.id] = characteristic_category
            other_materials_dict = {}
            for other_material_json in assay_json['materials']['otherMaterials']:
                material_name = other_material_json['name']
                if material_name.startswith('labeledextract-'):
                    material_name = material_name[15:]
                else:
                    material_name = material_name[8:]
                material = Material(
                    id_=other_material_json['@id'],
                    name=material_name,
                    type_=other_material_json['type'],
                )
                for characteristic_json in other_material_json['characteristics']:
                    characteristic = Characteristic(
                        category=categories_dict[characteristic_json['category']['@id']],
                        value=OntologyAnnotation(
                            term=characteristic_json['value']['annotationValue'],
                            term_source=term_source_dict[characteristic_json['value']['termSource']],
                            term_accession=characteristic_json['value']['termAccession'],
                        )
                    )
                    material.characteristics.append(characteristic)
                assay.materials['other_material'].append(material)
                other_materials_dict[material.id] = material
            for assay_process_json in assay_json['processSequence']:
                process = Process(
                    id_=assay_process_json['@id'],
                    executes_protocol=protocols_dict[assay_process_json['executesProtocol']['@id']]
                )
                try:
                    process.comments = get_comments(assay_process_json)
                except KeyError:
                    pass
                # additional properties, currently hard-coded special cases
                if process.executes_protocol.protocol_type.term == 'data collection' and assay.technology_type.term == 'DNA microarray':
                    process.name = assay_process_json['name']
                elif process.executes_protocol.protocol_type.term == 'nucleic acid sequencing':
                    process.name = assay_process_json['name']
                elif process.executes_protocol.protocol_type.term == 'nucleic acid hybridization':
                    process.name = assay_process_json['name']
                elif process.executes_protocol.protocol_type.term == 'data transformation':
                    process.name = assay_process_json['name']
                elif process.executes_protocol.protocol_type.term == 'data normalization':
                    process.name = assay_process_json['name']
                for input_json in assay_process_json['inputs']:
                    input_ = None
                    try:
                        input_ = samples_dict[input_json['@id']]
                    except KeyError:
                        pass
                    finally:
                        try:
                            input_ = other_materials_dict[input_json['@id']]
                        except KeyError:
                            pass
                        finally:
                            try:
                                input_ = data_dict[input_json['@id']]
                            except KeyError:
                                pass
                    if input_ is None:
                        raise IOError("Could not find input node in samples or materials or data dicts: " +
                                      input_json['@id'])
                    process.inputs.append(input_)
                for output_json in assay_process_json['outputs']:
                    output = None
                    try:
                        output = samples_dict[output_json['@id']]
                    except KeyError:
                        pass
                    finally:
                        try:
                            output = other_materials_dict[output_json['@id']]
                        except KeyError:
                            pass
                        finally:
                                try:
                                    output = data_dict[output_json['@id']]
                                except KeyError:
                                    pass
                    if output is None:
                        raise IOError("Could not find output node in samples or materials or data dicts: " +
                                      output_json['@id'])
                    process.outputs.append(output)
                for parameter_value_json in assay_process_json['parameterValues']:
                    if parameter_value_json['category']['@id'] == '#parameter/Array_Design_REF':  # Special case
                        process.array_design_ref = parameter_value_json['value']
                    elif isinstance(parameter_value_json['value'], (int, float)):
                        parameter_value = ParameterValue(
                            category=parameters_dict[parameter_value_json['category']['@id']],
                            value=parameter_value_json['value'],
                            unit=units_dict[parameter_value_json['unit']['@id']]
                        )
                        process.parameter_values.append(parameter_value)
                    else:
                        parameter_value = ParameterValue(
                            category=parameters_dict[parameter_value_json['category']['@id']],
                            )
                        try:
                            parameter_value.value = OntologyAnnotation(
                                term=parameter_value_json['value']['annotationValue'],
                                term_accession=parameter_value_json['value']['termAccession'],
                                term_source=term_source_dict[parameter_value_json['value']['termSource']],)
                        except TypeError:
                            parameter_value.value = parameter_value_json['value']
                        process.parameter_values.append(parameter_value)
                assay.process_sequence.append(process)
                process_dict[process.id] = process
                for assay_process_json in assay_json['processSequence']:  # 2nd pass
                    try:
                        prev_proc = assay_process_json['previousProcess']['@id']
                        process_dict[assay_process_json['@id']].prev_process = process_dict[prev_proc]
                    except KeyError:
                        pass
                    try:
                        next_proc = assay_process_json['nextProcess']['@id']
                        process_dict[assay_process_json['@id']].next_process = process_dict[next_proc]
                    except KeyError:
                        pass
            study.assays.append(assay)
        investigation.studies.append(study)
    return investigation


"""Everything below here is for the validator"""


def get_source_ids(study_json):
    """Used for rule 1002"""
    return [source['@id'] for source in study_json['materials']['sources']]


def get_sample_ids(study_json):
    """Used for rule 1003"""
    return [sample['@id'] for sample in study_json['materials']['samples']]


def get_material_ids(study_json):
    """Used for rule 1005"""
    material_ids = list()
    for assay_json in study_json['assays']:
        material_ids.extend([material['@id'] for material in assay_json['materials']['otherMaterials']])
    return material_ids


def get_data_file_ids(study_json):
    """Used for rule 1004"""
    data_file_ids = list()
    for assay_json in study_json['assays']:
        data_file_ids.extend([data_file['@id'] for data_file in assay_json['dataFiles']])
    return data_file_ids


def get_io_ids_in_process_sequence(study_json):
    """Used for rules 1001-1005"""
    all_process_sequences = list(study_json['processSequence'])
    for assay_json in study_json['assays']:
        all_process_sequences.extend(assay_json['processSequence'])
    # return [elem for iterabl in [[i['@id'] for i in process['inputs']] + [o['@id'] for o in process['outputs']] for process in
    #                              all_process_sequences] for elem in iterabl]

    return [
            io['@id']
                for process in all_process_sequences
                    for io in itertools.chain(process['inputs'], process['outputs'])
           ]



def check_material_ids_declared_used(study_json, id_collector_func):
    """Used for rules 1015-1018"""
    node_ids = id_collector_func(study_json)
    io_ids_in_process_sequence = get_io_ids_in_process_sequence(study_json)
    is_node_ids_used = set(node_ids).issubset(set(io_ids_in_process_sequence))
    if not is_node_ids_used:
        warnings.append({
            "message": "Material declared but not used",
            "supplemental": "{} not used in any inputs/outputs in {}".format(node_ids, io_ids_in_process_sequence),
            "code": 1017
        })
        logger.warning("(W) Not all node IDs in {} used by inputs/outputs {}".format(node_ids,
                                                                                     io_ids_in_process_sequence))


def check_material_ids_not_declared_used(study_json):
    """Used for rules 1002-1005"""
    node_ids = get_source_ids(study_json) + get_sample_ids(study_json) + get_material_ids(study_json) + \
               get_data_file_ids(study_json)
    io_ids_in_process_sequence = get_io_ids_in_process_sequence(study_json)
    diff = set(io_ids_in_process_sequence) - set(node_ids)
    if diff: #len(set(io_ids_in_process_sequence)) - len(set(node_ids)) > 0:
        #diff = set(io_ids_in_process_sequence) - set(node_ids)
        errors.append({
            "message": "Missing Material",
            "supplemental": "Inputs/outputs in {}  not found in sources, samples, materials or datafiles "
                            "declarations".format(list(diff)),
            "code": 1005
        })
        logger.error("(E) There are some inputs/outputs IDs {} not found in sources, samples, materials or data files declared"
              .format(list(diff)))


def check_process_sequence_links(process_sequence_json):
    """Used for rule 1006"""
    process_ids = [process['@id'] for process in process_sequence_json]
    for process in process_sequence_json:
        try:
            if process['previousProcess']['@id'] not in process_ids:
                errors.append({
                    "message": "Missing Process link",
                    "supplemental": "previousProcess {} in process {} does not refer to another process in "
                                    "sequence".format(process['previousProcess']['@id'], process['@id']),
                    "code": 1006
                })
                logger.error("(E) previousProcess link {} in process {} does not refer to another process in "
                             "sequence".format(process['previousProcess']['@id'], process['@id']))
        except KeyError:
            pass
        try:
            if process['nextProcess']['@id'] not in process_ids:
                errors.append({
                    "message": "Missing Process link",
                    "supplemental": "nextProcess {} in process {} does not refer to another process in "
                                    "sequence".format(process['nextProcess']['@id'], process['@id']),
                    "code": 1006
                })
                logger.error("(E) nextProcess {} in process {} does not refer to another process in sequence".format(
                    process['nextProcess']['@id'], process['@id']))
        except KeyError:
            pass


def get_study_protocol_ids(study_json):
    """Used for rule 1007"""
    return [protocol['@id'] for protocol in study_json['protocols']]


def check_process_protocol_ids_usage(study_json):
    """Used for rules 1007 and 1019"""
    protocol_ids_declared = get_study_protocol_ids(study_json)
    process_sequence = study_json['processSequence']
    protocol_ids_used = list()
    for process in process_sequence:
        try:
            protocol_ids_used.append(process['executesProtocol']['@id'])
        except KeyError:
            pass
    for assay in study_json['assays']:
        process_sequence = assay['processSequence']
        for process in process_sequence:
            try:
                protocol_ids_used.append(process['executesProtocol']['@id'])
            except KeyError:
                pass
    diff = set(protocol_ids_used) - set(protocol_ids_declared)
    if diff:
        errors.append({
            "message": "Missing Protocol declaration",
            "supplemental": "protocol IDs {} not declared".format(list(diff)),
            "code": 1007
        })
        logger.error("(E) There are protocol IDs {} used in a study or assay process sequence not declared"
              .format(list(diff)))

    diff = set(protocol_ids_declared) - set(protocol_ids_used)
    if diff:
        warnings.append({
            "message": "Protocol declared but not used",
            "supplemental": "protocol IDs declared {} not used".format(list(diff)),
            "code": 1019
        })
        logger.warning("(W) There are some protocol IDs declared {} not used in any study or assay process "
                       "sequence".format(list(diff)))


def get_study_protocols_parameter_ids(study_json):
    """Used for rule 1009"""
    # return [elem for iterabl in [[param['@id'] for param in protocol['parameters']] for protocol in
    #                              study_json['protocols']] for elem in iterabl]
    return [ param['@id'] for protocol in study_json['protocols'] for param in protocol['parameters'] ]


def get_parameter_value_parameter_ids(study_json):
    """Used for rule 1009"""
    # study_pv_parameter_ids = [elem for iterabl in
    #                           [[parameter_value['category']['@id'] for parameter_value in process['parameterValues']]
    #                               for process in study_json['processSequence']] for elem in iterabl]
    study_pv_parameter_ids = [
        parameter_value['category']['@id']
            for process in study_json['processSequence']
                for parameter_value in process['parameterValues']

    ]

    # for assay in study_json['assays']:
    #     # study_pv_parameter_ids.extend([elem for iterabl in
    #     #                                [[parameter_value['category']['@id'] for parameter_value in
    #     #                                  process['parameterValues']]
    #     #                                 for process in assay['processSequence']] for elem in iterabl]
    #     #                               )
    study_pv_parameter_ids.extend([
        parameter_value['category']['@id']
            for assay in study_json['assays']
                for process in assay['processSequence']
                    for parameter_value in process['parameterValues']
    ])
    return study_pv_parameter_ids


def check_protocol_parameter_ids_usage(study_json):
    """Used for rule 1009 and 1020"""
    protocols_declared = get_study_protocols_parameter_ids(study_json) + ['#parameter/Array_Design_REF'] # + special case
    protocols_used = get_parameter_value_parameter_ids(study_json)

    diff = set(protocols_used) - set(protocols_declared)
    if diff:
        errors.append({
            "message": "Missing Protocol Parameter declaration",
            "supplemental": "protocol parameters {} used".format(list(diff)),
            "code": 1009
        })
        logger.error("(E) There are protocol parameters {} used in a study or assay process not declared in any protocol"
              .format(list(diff)))
    diff = set(protocols_declared) - set(protocols_used)
    if diff:
        warnings.append({
            "message": "Protocol parameter declared in a protocol but never used",
            "supplemental": "protocol declared {} are not used".format(list(diff)),
            "code": 1020
        })
        logger.warning("(W) There are some protocol parameters declared {} not used in any study or assay process"
                       .format(list(diff)))


def get_characteristic_category_ids(study_or_assay_json):
    """Used for rule 1013"""
    return [category['@id'] for category in study_or_assay_json['characteristicCategories']]


def get_characteristic_category_ids_in_study_materials(study_json):
    """Used for rule 1013"""

    return [
            characteristic['category']['@id']
                for material in itertools.chain(study_json['materials']['sources'], study_json['materials']['samples'])
                    for characteristic in material['characteristics']
            ]

    # return [elem for iterabl in
    #         [[characteristic['category']['@id'] for characteristic in material['characteristics']] for material in
    #          study_json['materials']['sources'] + study_json['materials']['samples']] for elem in iterabl]


def get_characteristic_category_ids_in_assay_materials(assay_json):
    """Used for rule 1013"""
    # return [elem for iterabl in [[characteristic['category']['@id']  for characteristic in material['characteristics']]
    #                              if 'characteristics' in material else [] for material in
    #           assay_json['materials']['samples'] + assay_json['materials']['otherMaterials']] for elem in iterabl]
    return [
             characteristic['category']['@id']
                for material in itertools.chain(assay_json['materials']['samples'], assay_json['materials']['otherMaterials'])
                    if 'characteristics' in material
                        for characteristic in material['characteristics']
           ]



def check_characteristic_category_ids_usage(studies_json):
    """Used for rule 1013"""
    characteristic_categories_declared = list()
    characteristic_categories_used = list()
    for study_json in studies_json:
        characteristic_categories_declared += get_characteristic_category_ids(study_json)
        for assay in study_json['assays']:
            characteristic_categories_declared_in_assay = get_characteristic_category_ids(assay)
            characteristic_categories_declared += characteristic_categories_declared_in_assay
        characteristic_categories_used += get_characteristic_category_ids_in_study_materials(study_json)
        for assay in study_json['assays']:
            characteristic_categories_used_in_assay = get_characteristic_category_ids_in_assay_materials(assay)
            characteristic_categories_used += characteristic_categories_used_in_assay

    diff = set(characteristic_categories_used) - set(characteristic_categories_declared)
    if diff:
        errors.append({
                "message": "Missing Characteristic Category declaration",
                "supplemental": "Characteristic Categories {} used not declared".format(list(diff)),
                "code": 1013
            })
        logger.error("(E) There are characteristic categories {} used in a source or sample characteristic that have "
                     "not been not declared".format(list(diff)))
    diff = set(characteristic_categories_declared) - set(characteristic_categories_used)
    if diff:
        warnings.append({
            "message": "Characteristic Category not used",
            "supplemental": "Characteristic Categories {} declared".format(list(diff)),
            "code": 1022
        })
        logger.warning("(W) There are characteristic categories declared {} that have not been used in any source or "
                       "sample characteristic".format(list(diff)))


def get_study_factor_ids(study_json):
    """Used for rule 1008 and 1021"""
    return [factor['@id'] for factor in study_json['factors']]


def get_study_factor_ids_in_sample_factor_values(study_json):
    """Used for rule 1008 and 1021"""
    # return [elem for iterabl in [[factor['category']['@id'] for factor in sample['factorValues']] for sample in
    #                              study_json['materials']['samples']] for elem in iterabl]
    return [ factor['category']['@id']
                for sample in study_json['materials']['samples']
                    for factor in sample['factorValues']
           ]


def check_study_factor_usage(study_json):
    """Used for rules 1008 and 1021"""
    factors_declared = get_study_factor_ids(study_json)
    factors_used = get_study_factor_ids_in_sample_factor_values(study_json)
    if set(factors_used) - set(factors_declared):
        diff = set(factors_used) - set(factors_declared)
        errors.append({
            "message": "Missing Study Factor declaration",
            "supplemental": "Study Factors {} used".format(list(diff)),
            "code": 1008
        })
        logger.error("(E) There are study factors {} used in a sample factor value that have not been not declared"
              .format(list(diff)))
    elif set(factors_declared) - set(factors_used):
        diff = set(factors_declared) - set(factors_used)
        warnings.append({
            "message": "Study Factor is not used",
            "supplemental": "Study Factors {} are not used".format(list(diff)),
            "code": 1021
        })
        logger.warning("(W) There are some study factors declared {} that have not been used in any sample factor value"
              .format(list(diff)))


def get_unit_category_ids(study_or_assay_json):
    """Used for rule 1014"""
    return [category['@id'] for category in study_or_assay_json['unitCategories']]


def get_study_unit_category_ids_in_materials_and_processes(study_json):
    """Used for rule 1014"""
    # study_characteristics_units_used = [elem for iterabl in
    #                                     [[characteristic['unit']['@id'] if 'unit' in characteristic else None for
    #                                       characteristic in material['characteristics']] for material in
    #                                      study_json['materials']['sources'] + study_json['materials']['samples']] for
    #                                     elem in iterabl]
    study_characteristics_units_used = [characteristic['unit']['@id']
                                            for material in itertools.chain(study_json['materials']['sources'],study_json['materials']['samples'])
                                                for characteristic in material['characteristics']
                                                    if 'unit' in characteristic
                                        ]

    # study_factor_value_units_used = [elem for iterabl in
    #                                  [[factor_value['unit']['@id'] if 'unit' in factor_value else None for
    #                                    factor_value in material['factorValues']] for material in
    #                                   study_json['materials']['samples']] for
    #                                  elem in iterabl]
    study_factor_value_units_used = [factor_value['unit']['@id']
                                        for material in study_json['materials']['samples']
                                            for factor_value in material['factorValues']
                                                if 'unit' in factor_value
                                    ]



    # parameter_value_units_used = [elem for iterabl in[[parameter_value['unit']['@id']
    #                                                    if 'unit' in parameter_value else None for
    #                                parameter_value in process['parameterValues']] for process in
    #                               study_json['processSequence']] for
    #                               elem in iterabl]
    parameter_value_units_used = [parameter_value['unit']['@id']
                                    for process in study_json['processSequence']
                                        for parameter_value in process['parameterValues']
                                            if 'unit' in parameter_value
                                 ]

    # return [x for x in study_characteristics_units_used + study_factor_value_units_used + parameter_value_units_used
    #         if x is not None]
    return study_characteristics_units_used + study_factor_value_units_used + parameter_value_units_used



def get_assay_unit_category_ids_in_materials_and_processes(assay_json):
    """Used for rule 1014"""
    # assay_characteristics_units_used = [elem for iterabl in [[characteristic['unit']['@id'] if 'unit' in
    #                                     characteristic else None
    #                                                           for characteristic in material['characteristics']]
    #                                                          if 'characteristics' in material else None for
    #                                  material in assay_json['materials']['otherMaterials']] for elem in iterabl]
    assay_characteristics_units_used = [
        characteristic['unit']['@id']
            for material in assay_json['materials']['otherMaterials']
                if 'characteristics' in material
                    for characteristic in material
                        if 'unit' in characteristic
    ]


    # parameter_value_units_used = [elem for iterabl in[[parameter_value['unit']['@id']
    #                                                    if 'unit' in parameter_value else None
    #                                                    for parameter_value in process['parameterValues']] for process in
    #                                                   assay_json['processSequence']] for
    #                               elem in iterabl]

    parameter_value_units_used = [
        parameter_value['unit']['@id']
            for process in assay_json['processSequence']
                for parameter_value in process['parameterValues']
                    if 'unit' in parameter_value
    ]

    return parameter_value_units_used + assay_characteristics_units_used



def check_unit_category_ids_usage(study_json):
    """Used for rules 1014 and 1022"""
    logger.info("Getting units declared...")
    units_declared = get_unit_category_ids(study_json)
    for assay in study_json['assays']:
        units_declared.extend(get_unit_category_ids(assay))
    logger.info("Getting units used (study)...")
    units_used = get_study_unit_category_ids_in_materials_and_processes(study_json)
    logger.info("Getting units used (assay)...")
    for assay in study_json['assays']:
        units_used.extend(get_assay_unit_category_ids_in_materials_and_processes(assay))
    logger.info("Comparing units declared vs units used...")
    if set(units_used) - set(units_declared):
        diff = set(units_used) - set(units_declared)
        logger.error("(E) There are units {} used in a material or parameter value that have not been not declared"
              .format(list(diff)))
    elif set(units_declared) - set(units_used):
        diff = set(units_declared) - set(units_used)
        warnings.append({
            "message": "Unit declared but not used",
            "supplemental": "Units declared {} not used".format(list(diff)),
            "code": 1022
        })
        logger.warning("(W) There are some units declared {} that have not been used in any material or parameter value"
                       .format(list(diff)))


def check_utf8(fp):
    """Used for rule 0010"""
    import chardet
    with open(fp.name, mode='rb') as binary_fp:
        charset = chardet.detect(binary_fp.read())
    if charset['encoding'] not in {'UTF-8', 'ascii'}:
        #print(type(charset['encoding']), type('ascii'))
        warnings.append({
            "message": "File should be UTF8 encoding",
            "supplemental": "Encoding is '{0}' with confidence {1}".format(charset['encoding'], charset['confidence']),
            "code": 10
        })
        logger.warning("(W) File should be UTF-8 encoding but found it is '{0}' encoding with {1} confidence"
                       .format(charset['encoding'], charset['confidence']))
        raise SystemError



def check_isa_schemas(isa_json, investigation_schema_path):
    """Used for rule 0003 and 4003"""
    try:
        with open(investigation_schema_path) as schema_json:
            investigation_schema = json.load(schema_json)
        #investigation_schema_path = os.path.abspath(investigation_schema_path)
        resolver = RefResolver('file://' + investigation_schema_path, investigation_schema)
        validator = Draft4Validator(investigation_schema, resolver=resolver)
        validator.validate(isa_json)
    except ValidationError as ve:
        errors.append({
            "message": "Invalid JSON against ISA-JSON schemas",
            "supplemental": str(ve),
            "code": 3
        })
        logger.fatal("(F) The JSON does not validate against the provided ISA-JSON schemas!")
        logger.fatal("Fatal error: " + str(ve))
        raise SystemError("(F) The JSON does not validate against the provided ISA-JSON schemas!")
    except BaseException as be:
        logger.error("{}: {}".format(type(be).__name__, be))


def check_date_formats(isa_json):
    """Used for rule 3001"""
    def check_iso8601_date(date_str):
        if date_str:
            try:
                iso8601.parse_date(date_str)
            except iso8601.ParseError:
                warnings.append({
                    "message": "Date is not ISO8601 formatted",
                    "supplemental": "Found {} in date field".format(date_str),
                    "code": 3001
                })
                logger.warning("(W) Date {} does not conform to ISO8601 format".format(date_str))
    import iso8601
    check_iso8601_date(isa_json['publicReleaseDate'])
    check_iso8601_date(isa_json['submissionDate'])
    for study in isa_json['studies']:
        check_iso8601_date(study['publicReleaseDate'])
        check_iso8601_date(study['submissionDate'])
        for process in study['processSequence']:
            check_iso8601_date(process['date'])


def check_dois(isa_json):
    """Used for rule 3002"""
    def check_doi(doi_str):
        if doi_str:
            regexDOI = re.compile('(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![%"#? ])\\S)+)')
            if not regexDOI.match(doi_str):
                warnings.append({
                    "message": "DOI is not valid format",
                    "supplemental": "Found {} in DOI field".format(doi_str),
                    "code": 3002
                })
                logger.warning("(W) DOI {} does not conform to DOI format".format(doi_str))
    import re
    for ipub in isa_json['publications']:
        check_doi(ipub['doi'])
    for study in isa_json['studies']:
        for spub in study['publications']:
            check_doi(spub['doi'])


def check_filenames_present(isa_json):
    """Used for rule 3005"""
    for s_pos, study in enumerate(isa_json['studies']):
        if not study['filename']:
            warnings.append({
                "message": "Missing study file name",
                "supplemental": "At study position {}".format(s_pos),
                "code": 3005
            })
            logger.warning("(W) A study filename is missing")
        for a_pos, assay in enumerate(study['assays']):
            if not assay['filename']:
                warnings.append({
                    "message": "Missing assay file name",
                    "supplemental": "At study position {}, assay position {}".format(s_pos, a_pos),
                    "code": 3005
                })
                logger.warning("(W) An assay filename is missing")


def check_pubmed_ids_format(isa_json):
    """Used for rule 3003"""
    def check_pubmed_id(pubmed_id_str):
        if pubmed_id_str:
            pmid_regex = re.compile('[0-9]{8}')
            pmcid_regex = re.compile('PMC[0-9]{8}')
            if pmid_regex.match(pubmed_id_str) is None and pmcid_regex.match(pubmed_id_str) is None:
                warnings.append({
                    "message": "PubMed ID is not valid format",
                    "supplemental": "Found PubMedID {}".format(pubmed_id_str),
                    "code": 3003
                })
                logger.warning("(W) PubMed ID {} is not valid format".format(pubmed_id_str))
    import re
    for ipub in isa_json['publications']:
        check_pubmed_id(ipub['pubMedID'])
    for study in isa_json['studies']:
        for spub in study['publications']:
            check_pubmed_id(spub['pubMedID'])


def check_protocol_names(isa_json):
    """Used for rule 1010"""
    for study in isa_json['studies']:
        for protocol in study['protocols']:
            if not protocol['name']:
                warnings.append({
                    "message": "Protocol missing name",
                    "supplemental": "Protocol @id={}".format(protocol['@id']),
                    "code": 1010
                })
                logger.warning("(W) A Protocol {} is missing Protocol Name, so can't be referenced in ISA-tab"
                               .format(protocol['@id']))


def check_protocol_parameter_names(isa_json):
    """Used for rule 1011"""
    for study in isa_json['studies']:
        for protocol in study['protocols']:
            for parameter in protocol['parameters']:
                if not parameter['parameterName']:
                    warnings.append({
                        "message": "Protocol Parameter missing name",
                        "supplemental": "Protocol Parameter @id={}".format(parameter['@id']),
                        "code": 1011
                    })
                    logger.warning("(W) A Protocol Parameter {} is missing name, so can't be referenced in ISA-tab"
                                   .format(parameter['@id']))


def check_study_factor_names(isa_json):
    """Used for rule 1012"""
    for study in isa_json['studies']:
        for factor in study['factors']:
            if not factor['factorName']:
                warnings.append({
                    "message": "Study Factor missing name",
                    "supplemental": "Study Factor @id={}".format(factor['@id']),
                    "code": 1012
                })
                logger.warning("(W) A Study Factor is missing name, so can't be referenced in ISA-tab"
                               .format(factor['@id']))


def check_ontology_sources(isa_json):
    """Used for rule 3008"""
    for ontology_source in isa_json['ontologySourceReferences']:
        if not ontology_source['name']:
            warnings.append({
                "message": "Ontology Source missing name ref",
                "supplemental": "name={}".format(ontology_source['name']),
                "code": 3008
            })
            logger.warning("(W) An Ontology Source Reference is missing Term Source Name, so can't be referenced")


def get_ontology_source_refs(isa_json):
    """Used for rules 3007 and 3009"""
    return [ontology_source_ref['name'] for ontology_source_ref in isa_json['ontologySourceReferences']]


def walk_and_get_annotations(isa_json, collector):
    """Used for rules 3007 and 3009

    Usage:
      collector = list()
      walk_and_get_annotations(isa_json, collector)
      # and then like magic all your annotations from the JSON should be in the collector list
    """
    #  Walk JSON tree looking for ontology annotation structures in the JSON
    if isinstance(isa_json, dict):
        if set(isa_json.keys()) == {'annotationValue', 'termAccession', 'termSource'} or \
                        set(isa_json.keys()) == {'@id', 'annotationValue', 'termAccession', 'termSource'}:
            collector.append(isa_json)
        for i in six.iterkeys(isa_json):
            walk_and_get_annotations(isa_json[i], collector)
    elif isinstance(isa_json, list):
        for j in isa_json:
            walk_and_get_annotations(j, collector)


def check_term_source_refs(isa_json):
    """Used for rules 3007 and 3009"""
    term_sources_declared = get_ontology_source_refs(isa_json)
    collector = list()
    walk_and_get_annotations(isa_json, collector)
    term_sources_used = [annotation['termSource'] for annotation in collector if annotation['termSource']]
    diff = set(term_sources_used) - set(term_sources_declared)
    if diff:
        errors.append({
            "message": "Missing Term Source",
            "supplemental": "Ontology sources missing {}".format(list(diff)),
            "code": 3009
        })
        logger.error("(E) There are ontology sources {} referenced in an annotation that have not been not declared"
              .format(list(diff)))
    diff = set(term_sources_declared) - set(term_sources_used)
    if diff:
        warnings.append({
            "message": "Ontology Source Reference is not used",
            "supplemental": "Ontology sources not used {}".format(list(diff)),
            "code": 3007
        })
        logger.warning("(W) There are some ontology sources declared {} that have not been used in any annotation"
                       .format(list(diff)))


def check_term_accession_used_no_source_ref(isa_json):
    """Used for rule 3010"""
    collector = list()
    walk_and_get_annotations(isa_json, collector)
    terms_using_accession_no_source_ref = [annotation for annotation in collector if annotation['termAccession']
                                           and not annotation['termSource']]
    if terms_using_accession_no_source_ref:
        warnings.append({
            "message": "Missing Term Source REF in annotation",
            "supplemental": "Terms with accession but no source reference {}".format(terms_using_accession_no_source_ref),
            "code": 3010
        })
        logger.warning("(W) There are ontology annotations with termAccession set but no termSource referenced: {}"
                       .format(terms_using_accession_no_source_ref))


def print_graph(study_or_assay):
    print(study_or_assay.filename)
    G = study_or_assay.graph
    from isatools.isatab import _get_start_end_nodes, _all_end_to_end_paths
    start_nodes, end_nodes = _get_start_end_nodes(G)
    for path in _all_end_to_end_paths(G, start_nodes, end_nodes):
        #type_seq_str = ""
        type_seq = []
        for node in path:
            if isinstance(node, Source):
                #type_seq_str += '(' + node.name + ":Source)->"
                type_seq.append('({}:Source'.format(node.name))
            elif isinstance(node, Sample):
                #type_seq_str += '(' + node.name + ":Sample)->"
                type_seq.append('({}:Sample'.format(node.name))
            elif isinstance(node, Material):
                if '#material/extract' in node.id:
                    #type_seq_str += '(' + node.name + ":Extract)->"
                    type_seq.append('({}:Extract'.format(node.name))
                else:
                    #type_seq_str += '(' + node.name + ":Material)->"
                    type_seq.append('({}:Material'.format(node.name))
            elif isinstance(node, Process):
                protocol_type = node.executes_protocol.protocol_type.name
                #type_seq_str += "({})->".format(protocol_type)
                type_seq.append("({})".format(protocol_type))
                type_seq.extend([ "({})".format(node.filename) for node in node.outputs if isinstance(node, DataFile) ])
                #for data in [node for node in node.outputs if isinstance(node, DataFile)]:
                #    #type_seq_str += '(' + data.filename + ":DataFile)->"

            else:
                #type_seq_str += "({})->".format(type(node))
                type_seq.append("({})".format(type(node)))
        #if type_seq_str.endswith('->'):
        #    type_seq_str = type_seq_str[:len(type_seq_str) - 2]
        #print(type_seq_str)
        print("->".join(type_seq))


def load_config(config_dir):
    import json
    configs = dict()
    for file in glob.iglob(os.path.join(config_dir, "*.json")): # ignore non json files
        try:
            with open(os.path.join(config_dir, file)) as fp:
                config_dict = json.load(fp)
            if os.path.basename(file) == 'protocol_definitions.json':
                configs['protocol_definitions'] = config_dict
            elif os.path.basename(file) == 'study_config.json':
                configs['study'] = config_dict
            else:
                configs[(config_dict['measurementType'], config_dict['technologyType'])] = config_dict
        except ValidationError:
            errors.append({
                    "message": "Configurations could not be loaded",
                    "supplemental": "On loading {}".format(os.path.join(config_dir, file)),
                    "code": 4001
                })
            logger.error("(E) Could not load configuration file {}".format(str(file)))
    return configs


def check_measurement_technology_types(assay_json, configs):
    try:
        measurement_type = assay_json['measurementType']['annotationValue']
        technology_type = assay_json['technologyType']['annotationValue']
        config = configs[(measurement_type, technology_type)]
        if config is None:
            raise KeyError
    except KeyError:
        errors.append({
            "message": "Measurement/technology type invalid",
            "supplemental": "Measurement {}/technology {}".format(measurement_type, technology_type),
            "code": 4002
        })
        logger.error("(E) Could not load configuration for measurement type '{}' and technology type '{}'"
                     .format(measurement_type, technology_type))


def list_process_sequences(process_sequence_json):
    list_of_last_processes_in_sequence = (i for i in process_sequence_json if 'nextProcess' not in i)
    for process in list_of_last_processes_in_sequence:  # build graphs backwards
        assay_graph = list()
        try:
            while True:
                process_graph = list()
                if 'outputs' in process:
                    #outputs = process['outputs']
                    #if len(outputs) > 0:
                    for output in process['outputs']: #outputs:
                        output_id = output['@id']
                        process_graph.append(output_id)
                protocol_id = process['executesProtocol']['@id']
                process_graph.append(protocol_id)
                if 'inputs' in process:
                    #inputs = process['inputs']
                    #if len(inputs) > 0:
                    for input_ in process['inputs']:
                        input_id = input_['@id']
                        process_graph.append(input_id)
                process_graph.reverse()
                assay_graph.append(process_graph)
                process = [i for i in process_sequence_json if i['@id'] == process['previousProcess']['@id']][0]
        except KeyError:
            pass
        assay_graph.reverse()
        yield assay_graph


def check_study_and_assay_graphs(study_json, configs):

    def check_assay_graph(process_sequence_json, config):
        list_of_last_processes_in_sequence = (i for i in process_sequence_json if 'nextProcess' not in i)
        logger.info("Checking against assay protocol sequence configuration {}".format(config['description']))
        config_protocol_sequence = [i['protocol'] for i in config['protocols']]
        for process in list_of_last_processes_in_sequence:  # build graphs backwards
            assay_graph = list()
            try:
                while True:
                    process_graph = list()
                    if 'outputs' in process:
                        outputs = process['outputs']
                        #if outputs:
                        for output in outputs:
                            output_id = output['@id']
                            process_graph.append(output_id)
                    protocol_id = protocols_and_types[process['executesProtocol']['@id']]
                    process_graph.append(protocol_id)
                    if 'inputs' in process:
                        inputs = process['inputs']
                        #if len(inputs) > 0:
                        for input_ in inputs:
                            input_id = input_['@id']
                            process_graph.append(input_id)
                    process_graph.reverse()
                    assay_graph.append(process_graph)
                    process = next(i for i in process_sequence_json if i['@id'] == process['previousProcess']['@id'])
            except KeyError:  # this happens when we can't find a previousProcess
                pass
            assay_graph.reverse()
            assay_protocol_sequence = [j for i in assay_graph for j in i if not j.startswith('#') ]
            assay_protocol_sequence_of_interest = [i for i in assay_protocol_sequence if i in config_protocol_sequence]
            #  filter out protocols in sequence that are not of interest (additional ones to required by config)
            if config_protocol_sequence != assay_protocol_sequence_of_interest:
                warnings.append({
                    "message": "Process sequence is not valid against configuration",
                    "supplemental": "Protocol sequence {} does not in {}".format(config_protocol_sequence,
                                                                                 assay_protocol_sequence),
                    "code": 4004
                })
                logger.warning("Configuration protocol sequence {} does not match study graph found in {}"
                            .format(config_protocol_sequence, assay_protocol_sequence))

    protocols_and_types = {i['@id']: i['protocolType']['annotationValue'] for i in study_json['protocols']}
    # first check study graph
    logger.info("Loading configuration (study)")
    config = configs['study']
    check_assay_graph(study_json['processSequence'], config)
    for assay_json in study_json['assays']:
        m = assay_json['measurementType']['annotationValue']
        t = assay_json['technologyType']['annotationValue']
        logger.info("Loading configuration ({}, {})".format(m, t))
        config = configs[(m, t)]
        check_assay_graph(assay_json['processSequence'], config)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
default_config_dir = os.path.join(BASE_DIR, 'config', 'json', 'default')


def validate(fp, config_dir=default_config_dir, log_level=logging.INFO):
    if config_dir is None:
        config_dir = default_config_dir
    logger.setLevel(log_level)
    logger.info("ISA JSON Validator from ISA tools API v0.3")
    stream = six.StringIO()
    handler = logging.StreamHandler(stream)
    logger.addHandler(handler)
    try:
        global errors
        errors = list()
        global warnings
        warnings = list()
        logger.info("Checking if encoding is UTF8")
        check_utf8(fp=fp)  # Rule 0010
        logger.info("Loading json from " + fp.name)
        isa_json = json.load(fp=fp)  # Rule 0002
        logger.info("Validating JSON against schemas using Draft4Validator")
        check_isa_schemas(isa_json=isa_json,
                          investigation_schema_path=os.path.join(BASE_DIR, 'schemas', 'isa_model_version_1_0_schemas',
                                                                 'core', 'investigation_schema.json'))  # Rule 0003
        logger.info("Checking if material IDs used are declared...")
        for study_json in isa_json['studies']:
            check_material_ids_not_declared_used(study_json)  # Rules 1002-1005
        for study_json in isa_json['studies']:
            check_material_ids_declared_used(study_json, get_source_ids)  # Rule 1015
            check_material_ids_declared_used(study_json, get_sample_ids)  # Rule 1016
            check_material_ids_declared_used(study_json, get_material_ids)  # Rule 1017
            check_material_ids_declared_used(study_json, get_data_file_ids)  # Rule 1018
        logger.info("Checking characteristic categories usage...")
        check_characteristic_category_ids_usage(isa_json['studies'])  # Rules 1013 and 1022
        logger.info("Checking study factor usage...")
        for study_json in isa_json['studies']:
            check_study_factor_usage(study_json)  # Rules 1008 and 1021
        logger.info("Checking protocol parameter usage...")
        for study_json in isa_json['studies']:
            check_protocol_parameter_ids_usage(study_json)  # Rules 1009 and 1020
        logger.info("Checking unit category usage...")
        for study_json in isa_json['studies']:
            check_unit_category_ids_usage(study_json)  # Rules 1014 and 1022
        logger.info("Checking process sequences (study)...")
        for study_json in isa_json['studies']:
            check_process_sequence_links(study_json['processSequence'])  # Rule 1006
            logger.info("Checking process sequences (assay)...")
            for assay_json in study_json['assays']:
                check_process_sequence_links(assay_json['processSequence'])  # Rule 1006
        logger.info("Checking process protocol usage...")
        for study_json in isa_json['studies']:
            check_process_protocol_ids_usage(study_json)  # Rules 1007 and 1019
        logger.info("Checking date formats...")
        check_date_formats(isa_json)  # Rule 3001
        logger.info("Checking DOI formats...")
        check_dois(isa_json)  # Rule 3002
        logger.info("Checking Pubmed ID formats...")
        check_pubmed_ids_format(isa_json)  # Rule 3003
        logger.info("Checking filenames are present...")
        check_filenames_present(isa_json)  # Rule 3005
        logger.info("Checking protocol names...")
        check_protocol_names(isa_json)  # Rule 1010
        logger.info("Checking protocol parameter names...")
        check_protocol_parameter_names(isa_json)  # Rule 1011
        logger.info("Checking study factor names...")
        check_study_factor_names(isa_json)  # Rule 1012
        logger.info("Checking ontology sources...")
        check_ontology_sources(isa_json)  # Rule 3008
        logger.info("Checking term source REFs...")
        check_term_source_refs(isa_json)  # Rules 3007 and 3009
        logger.info("Checking missing term source REFs...")
        check_term_accession_used_no_source_ref(isa_json)  # Rule 3010
        logger.info("Loading configurations from " + config_dir)
        configs = load_config(config_dir)  # Rule 4001
        logger.info("Checking measurement and technology types...")
        for study_json in isa_json['studies']:
            for assay_json in study_json['assays']:
                check_measurement_technology_types(assay_json, configs)  # Rule 4002
        logger.info("Checking against configuration schemas...")
        check_isa_schemas(isa_json=isa_json,
                          investigation_schema_path=os.path.join(config_dir, 'schemas',
                                                                 'investigation_schema.json'))  # Rule 4003
        # if all ERRORS are resolved, then try and validate against configuration
        handler.flush()
        if "(E)" in stream.getvalue():
            logger.fatal("(F) There are some errors that mean validation against configurations cannot proceed.")
            return stream
        fp.seek(0)  # reset file pointer
        logger.info("Checking study and assay graphs...")
        for study_json in isa_json['studies']:
            check_study_and_assay_graphs(study_json, configs)  # Rule 4004
        logger.info("Finished validation...")
    except KeyError as k:
        errors.append({
            "message": "JSON Error",
            "supplemental": "Error when reading JSON; key: {}".format(str(k)),
            "code": 2
        })
        logger.fatal("(F) There was an error when trying to read the JSON")
        logger.fatal("Key: " + str(k))
    except ValueError as v:
        errors.append({
            "message": "JSON Error",
            "supplemental": "Error when parsing JSON; key: {}".format(str(v)),
            "code": 2
        })
        logger.fatal("(F) There was an error when trying to parse the JSON")
        logger.fatal("Value: " + str(v))
    except SystemError as e:
        errors.append({
            "message": "Unknown/System Error",
            "supplemental": str(e),
            "code": 0
        })
        logger.fatal("(F) Something went very very wrong! :(")
    except BaseException as b:
        logger.fatal("(F) An {} was raised!".format(type(b).__name__))
        logger.fatal("Value: {}".format(b))
    finally:
        handler.flush()
        return {
            "errors": errors,
            "warnings": warnings,
            "validation_finished": True
        }


def batch_validate(json_file_list):
    """ Validate a batch of ISA-JSON files
        :param json_file_list: List of file paths to the ISA-JSON files to validate
        :return: Dict of reports

        Example:
            from isatools import isajson
            my_jsons = [
                '/path/to/study1.json',
                '/path/to/study2.json'
            ]
            my_reports = isajson.batch_validate(my_jsons)
    """
    batch_report = {
        "batch_report": []
    }
    for json_file in json_file_list:
        logger.info("***Validating {}***\n".format(json_file))
        if not os.path.isfile(json_file):
            logger.warning("Could not find ISA-JSON file, skipping {}".format(json_file))
        else:
            with open(json_file) as fp:
                batch_report['batch_report'].append(
                    {
                        "filename": fp.name,
                        "report": validate(fp)
                    }
                )
    return batch_report
