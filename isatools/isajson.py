from isatools.model.v1 import *
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def load(fp):
    # ontologySourceReference_REFs = dict()  # For term source REF pointers
    # file_REFs = dict()  # For fileName REF pointers
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
        logger.debug('Populate the ontology source references')
        for ontologySourceReference_json in isajson['ontologySourceReferences']:
            logger.debug('Build Ontology Source Reference object')
            ontology_source_reference = OntologySourceReference(
                name=ontologySourceReference_json['name'],
                file=ontologySourceReference_json['file'],
                version=ontologySourceReference_json['version'],
                description=ontologySourceReference_json['description']
            )
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
                    term_source=publication_json['status']['termSource']
                )
            )
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
                affiliation=person_json['affiliation']
            )
            # TODO: Implement support for roles
            investigation.contacts.append(person)
        logger.debug('Start building Studies objects')
        samples_dict = dict()
        sources_dict = dict()
        categories_dict = dict()
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
            for study_characteristics_category_json in study_json['characteristicCategories']:
                characteristic_category = CharacteristicCategory(
                    id_=study_characteristics_category_json['@id'],
                    characteristic_type=OntologyAnnotation(
                        name=study_characteristics_category_json['characteristicType']['annotationValue'],
                        term_source=study_characteristics_category_json['characteristicType']['termSource'],
                        term_accession=study_characteristics_category_json['characteristicType']['termAccession'],
                    )
                )
                study.characteristic_categories.append(characteristic_category)
                categories_dict[characteristic_category.id] = characteristic_category
            for study_publication_json in study_json['publications']:
                logger.debug('Build Study Publication object')
                study_publication = Publication(
                    pubmed_id=study_publication_json['pubMedID'],
                    doi=study_publication_json['doi'],
                    author_list=study_publication_json['authorList'],
                    title=study_publication_json['title'],
                    status=OntologyAnnotation(
                        name=study_publication_json['status']['annotationValue'],
                        term_accession=study_publication_json['status']['termAccession'],
                    )
                )
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
                )
                study.contacts.append(study_person)
            for design_descriptor_json in study_json['studyDesignDescriptors']:
                logger.debug('Build Ontology Annotation object (Study Design Descriptor)')
                design_descriptor = OntologyAnnotation(
                    name=design_descriptor_json['annotationValue'],
                    term_accession=design_descriptor_json['termAccession'],
                    term_source=design_descriptor_json['termSource']
                )
                study.design_descriptors.append(design_descriptor)
            for protocol_json in study_json['protocols']:
                logger.debug('Build Study Protocol object')
                protocol = Protocol(
                    id_=protocol_json['@id'],
                    name=protocol_json['name'],
                    protocol_type=OntologyAnnotation(
                        name=protocol_json['protocolType']['annotationValue'],
                        term_accession=protocol_json['protocolType']['termAccession'],
                        term_source=protocol_json['protocolType']['termSource']
                    )
                )
                study.protocols.append(protocol)
            for factor_json in study_json['factors']:
                logger.debug('Build Study Factor object')
                factor = StudyFactor(
                    name=factor_json['factorName'],
                    factor_type=OntologyAnnotation(
                        name=factor_json['factorType']['annotationValue'],
                        term_accession=factor_json['factorType']['termAccession'],
                        term_source=factor_json['factorType']['termSource']
                    )
                )
                study.factors.append(factor)
            for source_json in study_json['materials']['sources']:
                logger.debug('Build Source object')
                source = Source(
                    id_=source_json['@id'],
                    name=source_json['name'],
                )
                for characteristic_json in source_json['characteristics']:
                    logger.debug('Build Ontology Annotation object (Source Characteristic)')
                    characteristic = Characteristic(
                        characteristic_type=categories_dict[characteristic_json['category']['@id']],
                        # value=''
                    )
                    source.characteristics.append(characteristic)
                sources_dict[source.id] = source
                study.materials['sources'].append(source)
            for sample_json in study_json['materials']['samples']:
                logger.debug('Build Source object')
                sample = Sample(
                    id_=sample_json['@id'],
                    name=sample_json['name'],
                    derives_from=sample_json['derivesFrom']
                )
                for characteristic_json in sample_json['characteristics']:
                    logger.debug('Build Ontology Annotation object (Source Characteristic)')
                    characteristic = Characteristic(
                        characteristic_type=categories_dict[characteristic_json['category']['@id']],
                        # value=''
                    )
                    sample.characteristics.append(characteristic)
                for factor_value_json in sample_json['factorValues']:
                    logger.debug('Build Ontology Annotation object (Sample Factor Value)')
                    try:
                        factor_value = FactorValue(
                            value=OntologyAnnotation(
                                name=factor_value_json['value']['annotationValue'],
                                term_accession=factor_value_json['value']['termAccession'],
                                term_source=factor_value_json['value']['termSource'],
                            ),

                        )
                    except TypeError:
                        factor_value = FactorValue(
                            value=factor_value_json['value'],
                            unit=OntologyAnnotation(
                                name=factor_value_json['unit']['annotationValue'],
                                term_accession=factor_value_json['unit']['termAccession'],
                                term_source=factor_value_json['unit']['termSource'],
                            ),
                        )
                    sample.characteristics.append(factor_value)
                samples_dict[sample.id] = sample
                study.materials['samples'].append(sample)
            for study_process_json in study_json['processSequence']:
                logger.debug('Build Process object')
                process = Process(
                    executes_protocol=study_process_json['executesProtocol']['@id'],
                )
                try:
                    process.date = study_process_json['date']
                except KeyError:
                    pass
                try:
                    process.performer = study_process_json['performer']
                except KeyError:
                    pass
                for parameter_json in study_process_json['parameterValues']:
                    if isinstance(parameter_json['parameterValue'], int or float):
                        parameter_value = ParameterValue(
                            category=parameter_json['name'],
                            parameter_value=parameter_json['parameterValue'],
                            unit=OntologyAnnotation(
                                name=parameter_json['unit']['name'],
                                term_accession=parameter_json['unit']['termAccession'],
                                term_source=parameter_json['unit']['termSource'],
                            )
                        )
                    else:
                        parameter_value = ParameterValue(
                            category=parameter_json['name'],
                            parameter_value=OntologyAnnotation(
                                name=parameter_json['parameterValue']['name'],
                                term_accession=parameter_json['parameterValue']['termAccession'],
                                term_source=parameter_json['parameterValue']['termSource'],
                            )
                        )
                    process.parameter_values.append(parameter_value)
                study.process_sequence.append(process)
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
                for assay_json in study_json['assays']:
                    logger.debug('Start building Assay object')
                    logger.debug('Build Study Assay object')
                    assay = Assay(
                        measurement_type=OntologyAnnotation(
                            name=assay_json['measurementType']['annotationValue'],
                            term_accession=assay_json['measurementType']['termAccession'],
                            term_source=assay_json['measurementType']['termSource']
                        ),
                        technology_type=OntologyAnnotation(
                            name=assay_json['technologyType']['annotationValue'],
                            term_accession=assay_json['technologyType']['termAccession'],
                            term_source=assay_json['technologyType']['termSource']
                        ),
                        technology_platform=assay_json['technologyPlatform'],
                        filename=assay_json['filename']
                    )
                    data_dict = dict()
                    for data_json in assay_json['dataFiles']:
                        logger.debug('Build Data object')
                        data = Data(
                            name=data_json['name'],
                            type_=data_json['type'],
                        )
                        data_dict[data.name] = data
                        assay.data_files.append(data)
                    other_materials_dict = dict()
                    for other_material_json in assay_json['materials']['otherMaterials']:
                        logger.debug('Build Material object')
                        material = Material(
                            id_=other_material_json['@id'],
                            name=other_material_json['name'],
                            type_=other_material_json['type'],
                        )
                        for characteristic_json in other_material_json['characteristics']:
                            characteristic = Characteristic(
                                id_=characteristic_json['@id'],
                                characteristic_type=OntologyAnnotation(
                                    name=characteristic_json['characteristicType']['annotationValue'],
                                    term_source=characteristic_json['characteristicType']['termSource'],
                                    term_accession=characteristic_json['characteristicType']['termAccession'],
                                )
                            )
                            material.characteristics.append(characteristic)
                        assay.materials['other_material'].append(material)
                        other_materials_dict[material.id] = material
                    for assay_process_json in assay_json['processSequence']:
                        process = Process(
                            executes_protocol=assay_process_json['executesProtocol']['@id']
                        )
                        for input_json in assay_process_json['inputs']:
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
                                raise IOError("Could not find input node in sources or samples dicts: " +
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
                                        output = other_materials_dict[output_json['@id']]
                                    except KeyError:
                                        pass
                            if output is None:
                                raise IOError("Could not find output node in samples or other materials dicts: " +
                                              output_json['@id'])
                            process.outputs.append(output)
                        assay.process_sequence.append(process)
                study.assays.append(assay)
            logger.debug('End building Study object')
            investigation.studies.append(study)
        logger.debug('End building Studies objects')
        logger.debug('End building Investigation object')
    return investigation
