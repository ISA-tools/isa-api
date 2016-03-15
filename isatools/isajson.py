from isatools.model.v1 import *
import json
import logging
from networkx import DiGraph
from jsonschema import Draft4Validator, RefResolver, ValidationError
import os

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def validates(isa_json, reporting_level=logging.INFO):
    """Validate JSON"""
    logging.basicConfig(level=reporting_level)
    logger = logging.getLogger(__name__)
    try:  # if can load the JSON (if the JSON is well-formed already), validate the JSON against our schemas
        investigation_schema_path = os.path.join(os.path.dirname(__file__) + '/schemas/isa_model_version_1_0_schemas/core/investigation_schema.json')
        investigation_schema = json.load(open(investigation_schema_path))
        resolver = RefResolver('file://' + investigation_schema_path, investigation_schema)
        validator = Draft4Validator(investigation_schema, resolver=resolver)
        validator.validate(isa_json)
        # if the JSON is validated against ISA JSON, let's start checking content
    except ValidationError as isa_schema_validation_error:
        logger.fatal("There was an error when validating the JSON against the ISA schemas")
        raise isa_schema_validation_error


def validate(fp, reporting_level=logging.INFO):  # default reporting
    """Validate JSON file"""
    logging.basicConfig(level=reporting_level)
    logger = logging.getLogger(__name__)
    try:  # first, try open the file as a JSON
        try:
            isa_json = json.load(fp=fp)
            validates(isa_json, reporting_level)
        except ValueError as json_load_error:
            logger.fatal("There was an error when trying to parse the JSON")
            raise json_load_error
    except SystemError as system_error:
        logger.fatal("There was a general system error")
        raise system_error

def load(fp):

    def _build_assay_graph(process_sequence=list()):
        G = DiGraph()
        for process in process_sequence:
            if process.next_process is not None or len(process.outputs) > 0:  # first check if there's some valid outputs to connect
                if len(process.outputs) > 0:
                    for output in [n for n in process.outputs if not isinstance(n, DataFile)]:
                        G.add_edge(process, output)
                else:  # otherwise just connect the process to the next one
                    G.add_edge(process, process.next_process)
            if process.prev_process is not None or len(process.inputs) > 0:
                if len(process.inputs) > 0:
                    for input_ in process.inputs:
                        G.add_edge(input_, process)
                else:
                    G.add_edge(process.prev_process, process)
        return G

    investigation = None
    logger.info('Opening file %s', fp)
    isajson = json.load(fp)
    if isajson is None:
        logger.error('There was a problem opening the JSON file')
    else:
        logger.debug('Start building the Investigation object')
        investigation = Investigation(
            identifier=isajson['identifier'],
            title=isajson['title'],
            description=isajson['description'],
            submission_date=isajson['submissionDate'],
            public_release_date=isajson['publicReleaseDate']
        )
        for comment_json in isajson['comments']:
            comment = Comment(
                name=comment_json['name'],
                value=comment_json['value'],
            )
            investigation.comments.append(comment)
        logger.debug('Populate the ontology source references')
        term_source_dict = {'': None}
        for ontologySourceReference_json in isajson['ontologySourceReferences']:
            logger.debug('Build Ontology Source Reference object')
            ontology_source_reference = OntologySourceReference(
                name=ontologySourceReference_json['name'],
                file=ontologySourceReference_json['file'],
                version=ontologySourceReference_json['version'],
                description=ontologySourceReference_json['description']
            )
            term_source_dict[ontology_source_reference.name] = ontology_source_reference
            investigation.ontology_source_references.append(ontology_source_reference)
        for publication_json in isajson['publications']:
            logger.debug('Build Investigation Publication object')
            publication = Publication(
                pubmed_id=publication_json['pubMedID'],
                doi=publication_json['doi'],
                author_list=publication_json['authorList'],
                title=publication_json['title'],
                status=OntologyAnnotation(
                    name=publication_json['status']['annotationValue'],
                    term_accession=publication_json['status']['termAccession'],
                    term_source=term_source_dict[publication_json['status']['termSource']]
                )
            )
            try:
                for comment_json in publication_json['comments']:
                    comment = Comment(
                        name=comment_json['name'],
                        value=comment_json['value']
                    )
                    publication.comments.append(comment)
            except KeyError:
                pass
            investigation.publications.append(publication)
        for person_json in isajson['people']:
            logger.debug('Build Investigation Person object')
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
                    name=role_json['annotationValue'],
                    term_accession=role_json['termAccession'],
                    term_source=term_source_dict[role_json['termSource']]
                )
                person.roles.append(role)
            for comment_json in person_json['comments']:
                comment = Comment(
                    name=comment_json['name'],
                    value=comment_json['value'],
                )
                person.comments.append(comment)
            investigation.contacts.append(person)
        logger.debug('Start building Studies objects')
        samples_dict = dict()
        sources_dict = dict()
        categories_dict = dict()
        protocols_dict = dict()
        factors_dict = dict()
        parameters_dict = dict()
        units_dict = dict()
        process_dict = dict()

        # populate assay characteristicCategories first
        for study_json in isajson['studies']:
            for assay_json in study_json['assays']:
                for assay_characteristics_category_json in assay_json['characteristicCategories']:
                    characteristic_category = OntologyAnnotation(
                        id_=assay_characteristics_category_json['@id'],
                        name=assay_characteristics_category_json['characteristicType']['annotationValue'],
                        term_source=term_source_dict[assay_characteristics_category_json['characteristicType']['termSource']],
                        term_accession=assay_characteristics_category_json['characteristicType']['termAccession'],
                    )
                    # study.characteristic_categories.append(characteristic_category)
                    categories_dict[characteristic_category.id] = characteristic_category
        for study_json in isajson['studies']:
            logger.debug('Start building Study object')
            study = Study(
                identifier=study_json['identifier'],
                title=study_json['title'],
                description=study_json['description'],
                submission_date=study_json['submissionDate'],
                public_release_date=study_json['publicReleaseDate'],
                filename=study_json['filename']
            )
            try:
                for comment_json in study_json['comments']:
                    comment = Comment(
                        name=comment_json['name'],
                        value=comment_json['value'],
                    )
                    study.comments.append(comment)
            except KeyError:
                pass
            for study_characteristics_category_json in study_json['characteristicCategories']:
                characteristic_category = OntologyAnnotation(
                    id_=study_characteristics_category_json['@id'],
                    name=study_characteristics_category_json['characteristicType']['annotationValue'],
                    term_source=term_source_dict[study_characteristics_category_json['characteristicType']['termSource']],
                    term_accession=study_characteristics_category_json['characteristicType']['termAccession'],
                )
                study.characteristic_categories.append(characteristic_category)
                categories_dict[characteristic_category.id] = characteristic_category
            for study_unit_json in study_json['unitCategories']:
                unit = OntologyAnnotation(id_=study_unit_json['@id'],
                                          name=study_unit_json['annotationValue'],
                                          term_source=term_source_dict[study_unit_json['termSource']],
                                          term_accession=study_unit_json['termAccession'])
                units_dict[unit.id] = unit
            for study_publication_json in study_json['publications']:
                logger.debug('Build Study Publication object')
                study_publication = Publication(
                    pubmed_id=study_publication_json['pubMedID'],
                    doi=study_publication_json['doi'],
                    author_list=study_publication_json['authorList'],
                    title=study_publication_json['title'],
                    status=OntologyAnnotation(
                        name=study_publication_json['status']['annotationValue'],
                        term_source=term_source_dict[study_publication_json['status']['termSource']],
                        term_accession=study_publication_json['status']['termAccession'],
                    )
                )
                try:
                    for comment_json in study_publication_json['comments']:
                        comment = Comment(
                            name=comment_json['name'],
                            value=comment_json['value']
                        )
                        study_publication.comments.append(comment)
                except KeyError:
                    pass
                study.publications.append(study_publication)
            for study_person_json in study_json['people']:
                logger.debug('Build Study Person object')
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
                for role_json in study_person_json['roles']:
                    role = OntologyAnnotation(
                        name=role_json['annotationValue'],
                        term_accession=role_json['termAccession'],
                        term_source=term_source_dict[role_json['termSource']]
                    )
                    study_person.roles.append(role)
                try:
                    for comment_json in study_person_json['comments']:
                        comment = Comment(
                            name=comment_json['name'],
                            value=comment_json['value'],
                        )
                        study_person.comments.append(comment)
                except KeyError:
                    pass
                study.contacts.append(study_person)
            for design_descriptor_json in study_json['studyDesignDescriptors']:
                logger.debug('Build Ontology Annotation object (Study Design Descriptor)')
                design_descriptor = OntologyAnnotation(
                    name=design_descriptor_json['annotationValue'],
                    term_accession=design_descriptor_json['termAccession'],
                    term_source=term_source_dict[design_descriptor_json['termSource']]
                )
                study.design_descriptors.append(design_descriptor)
            for protocol_json in study_json['protocols']:
                logger.debug('Build Study Protocol object')
                protocol = Protocol(
                    id_=protocol_json['@id'],
                    name=protocol_json['name'],
                    uri=protocol_json['uri'],
                    description=protocol_json['description'],
                    version=protocol_json['version'],
                    protocol_type=OntologyAnnotation(
                        name=protocol_json['protocolType']['annotationValue'],
                        term_accession=protocol_json['protocolType']['termAccession'],
                        term_source=term_source_dict[protocol_json['protocolType']['termSource']]
                    )
                )
                for parameter_json in protocol_json['parameters']:
                    parameter = ProtocolParameter(
                        id_=parameter_json['@id'],
                        parameter_name=OntologyAnnotation(
                            name=parameter_json['parameterName']['annotationValue'],
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
                            name=component_json['componentType']['annotationValue'],
                            term_source=term_source_dict[component_json['componentType']['termSource']],
                            term_accession=component_json['componentType']['termAccession']
                        )
                    )
                    protocol.components.append(component)
                study.protocols.append(protocol)
                protocols_dict[protocol.id] = protocol
            for factor_json in study_json['factors']:
                logger.debug('Build Study Factor object')
                factor = StudyFactor(
                    id_=factor_json['@id'],
                    name=factor_json['factorName'],
                    factor_type=OntologyAnnotation(
                        name=factor_json['factorType']['annotationValue'],
                        term_accession=factor_json['factorType']['termAccession'],
                        term_source=term_source_dict[factor_json['factorType']['termSource']]
                    )
                )
                study.factors.append(factor)
                factors_dict[factor.id] = factor
            for source_json in study_json['materials']['sources']:
                logger.debug('Build Source object')
                source = Source(
                    id_=source_json['@id'],
                    name=source_json['name'][7:],
                )
                for characteristic_json in source_json['characteristics']:
                    logger.debug('Build Ontology Annotation object (Characteristic)')
                    value = characteristic_json['value']
                    unit = None
                    characteristic = Characteristic(category=categories_dict[characteristic_json['category']['@id']],)
                    if isinstance(value, dict):
                        try:
                            value = OntologyAnnotation(
                                name=characteristic_json['value']['annotationValue'],
                                term_source=term_source_dict[characteristic_json['value']['termSource']],
                                term_accession=characteristic_json['value']['termAccession'])
                        except KeyError:
                            raise IOError("Can't create value as annotation")
                    elif isinstance(value, int) or isinstance(value, float):
                        try:
                            unit = units_dict[characteristic_json['unit']['@id']]
                        except KeyError:
                            raise IOError("Can't create unit annotation")
                    elif not isinstance(value, str):
                        raise IOError("Unexpected type in characteristic value")
                    characteristic.value = value
                    characteristic.unit = unit
                    source.characteristics.append(characteristic)
                sources_dict[source.id] = source
                study.materials['sources'].append(source)
            for sample_json in study_json['materials']['samples']:
                logger.debug('Build Sample object')
                sample = Sample(
                    id_=sample_json['@id'],
                    name=sample_json['name'][7:],
                    derives_from=sample_json['derivesFrom']
                )
                for characteristic_json in sample_json['characteristics']:
                    logger.debug('Build Ontology Annotation object (Characteristic)')
                    value = characteristic_json['value']
                    unit = None
                    characteristic = Characteristic(
                            category=categories_dict[characteristic_json['category']['@id']])
                    if isinstance(value, dict):
                        try:
                            value = OntologyAnnotation(
                                name=characteristic_json['value']['annotationValue'],
                                term_source=term_source_dict[characteristic_json['value']['termSource']],
                                term_accession=characteristic_json['value']['termAccession'])
                        except KeyError:
                            raise IOError("Can't create value as annotation")
                    elif isinstance(value, int) or isinstance(value, float):
                        try:
                            unit = units_dict[characteristic_json['unit']['@id']]
                        except KeyError:
                            raise IOError("Can't create unit annotation")
                    elif not isinstance(value, str):
                        raise IOError("Unexpected type in characteristic value")
                    characteristic.value = value
                    characteristic.unit = unit
                    sample.characteristics.append(characteristic)
                for factor_value_json in sample_json['factorValues']:
                    logger.debug('Build Ontology Annotation object (Sample Factor Value)')
                    try:
                        factor_value = FactorValue(
                            factor_name=factors_dict[factor_value_json['category']['@id']],
                            value=OntologyAnnotation(
                                name=factor_value_json['value']['annotationValue'],
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
                logger.debug('Build Process object')
                process = Process(
                    id_=study_process_json['@id'],
                    executes_protocol=protocols_dict[study_process_json['executesProtocol']['@id']],
                )
                try:
                    for comment_json in study_process_json['comments']:
                        comment = Comment(
                            name=comment_json['name'],
                            value=comment_json['value'],
                        )
                        process.comments.append(comment)
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
                    if isinstance(parameter_value_json['value'], int) or isinstance(parameter_value_json['value'], float):
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
                                name=parameter_value_json['value']['annotationValue'],
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
            study.graph = _build_assay_graph(study.process_sequence)
            for assay_json in study_json['assays']:
                logger.debug('Start building Assay object')
                logger.debug('Build Study Assay object')
                assay = Assay(
                    measurement_type=OntologyAnnotation(
                        name=assay_json['measurementType']['annotationValue'],
                        term_accession=assay_json['measurementType']['termAccession'],
                        term_source=term_source_dict[assay_json['measurementType']['termSource']]
                    ),
                    technology_type=OntologyAnnotation(
                        name=assay_json['technologyType']['annotationValue'],
                        term_accession=assay_json['technologyType']['termAccession'],
                        term_source=term_source_dict[assay_json['technologyType']['termSource']]
                    ),
                    technology_platform=assay_json['technologyPlatform'],
                    filename=assay_json['filename']
                )
                for assay_unit_json in assay_json['unitCategories']:
                    unit = OntologyAnnotation(id_=assay_unit_json['@id'],
                                              name=assay_unit_json['annotationValue'],
                                              term_source=term_source_dict[assay_unit_json['termSource']],
                                              term_accession=assay_unit_json['termAccession'])
                    units_dict[unit.id] = unit
                data_dict = dict()
                for data_json in assay_json['dataFiles']:
                    logger.debug('Build Data object')
                    data_file = DataFile(
                        id_=data_json['@id'],
                        filename=data_json['name'],
                        label=data_json['type'],
                    )
                    try:
                        for comment_json in data_json['comments']:
                            comment = Comment(
                                name=comment_json['name'],
                                value=comment_json['value'],
                            )
                            data_file.comments.append(comment)
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
                        name=assay_characteristics_category_json['characteristicType']['annotationValue'],
                        term_source=term_source_dict[assay_characteristics_category_json['characteristicType']['termSource']],
                        term_accession=assay_characteristics_category_json['characteristicType']['termAccession'],
                    )
                    study.characteristic_categories.append(characteristic_category)
                    categories_dict[characteristic_category.id] = characteristic_category
                other_materials_dict = dict()
                for other_material_json in assay_json['materials']['otherMaterials']:
                    logger.debug('Build Material object')  # need to detect material types
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
                                name=characteristic_json['value']['annotationValue'],
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
                        for comment_json in assay_process_json['comments']:
                            comment = Comment(
                                name=comment_json['name'],
                                value=comment_json['value'],
                            )
                            process.comments.append(comment)
                    except KeyError:
                        pass
                    # additional properties, currently hard-coded special cases
                    if process.executes_protocol.protocol_type.name == 'data collection' and assay.technology_type.name == 'DNA microarray':
                        process.additional_properties['Scan Name'] = assay_process_json['name']
                    elif process.executes_protocol.protocol_type.name == 'nucleic acid sequencing':
                        process.additional_properties['Assay Name'] = assay_process_json['name']
                    elif process.executes_protocol.protocol_type.name == 'nucleic acid hybridization':
                        process.additional_properties['Hybridization Assay Name'] = assay_process_json['name']
                    elif process.executes_protocol.protocol_type.name == 'data transformation':
                        process.additional_properties['Data Transformation Name'] = assay_process_json['name']
                    elif process.executes_protocol.protocol_type.name == 'data normalization':
                        process.additional_properties['Normalization Name'] = assay_process_json['name']
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
                            process.additional_properties['Array Design REF'] = parameter_value_json['value']
                        elif isinstance(parameter_value_json['value'], int) or \
                                isinstance(parameter_value_json['value'], float):
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
                                    name=parameter_value_json['value']['annotationValue'],
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
                    assay.graph = _build_assay_graph(assay.process_sequence)
                study.assays.append(assay)
            logger.debug('End building Study object')
            investigation.studies.append(study)
        logger.debug('End building Studies objects')
        logger.debug('End building Investigation object')
    return investigation
