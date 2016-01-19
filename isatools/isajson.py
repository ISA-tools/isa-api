from isatools.model.v1 import *
import json
import logging
import networkx as nx

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
            ontologySourceReference = OntologySourceReference(
                name=ontologySourceReference_json['name'],
                file=ontologySourceReference_json['file'],
                version=ontologySourceReference_json['version'],
                description=ontologySourceReference_json['description']
            )
            investigation.ontology_source_references.append(ontologySourceReference)
        for publication_json in isajson['publications']:
            logger.debug('Build Investigation Publication object')
            publication = Publication(
                pubmed_id=publication_json['pubMedID'],
                doi=publication_json['doi'],
                author_list=publication_json['authorList'],
                title=publication_json['title'],
                status=OntologyAnnotation(
                    name=publication_json['status']['name'],
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
        for study_json in isajson['studies']:
            logger.debug('Start building Study object')
            study = Study(
                identifier=study_json['identifier'],
                title=study_json['title'],
                description=study_json['description'],
                submission_date=study_json['submissionDate'],
                public_release_date=study_json['publicReleaseDate'],
                file_name=study_json['filename']
            )
            for study_publication_json in study_json['publications']:
                logger.debug('Build Study Publication object')
                study_publication = Publication(
                    pubmed_id=study_publication_json['pubMedID'],
                    doi=study_publication_json['doi'],
                    author_list=study_publication_json['authorList'],
                    title=study_publication_json['title'],
                    status=OntologyAnnotation(
                        name=study_publication_json['status']['name'],
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
                    name=design_descriptor_json['name'],
                    term_accession=design_descriptor_json['termAccession'],
                    term_source=design_descriptor_json['termSource']
                )
                study.design_descriptors.append(design_descriptor)
            for protocol_json in study_json['protocols']:
                logger.debug('Build Study Protocol object')
                protocol = Protocol(
                    name=protocol_json['name'],
                    protocol_type=OntologyAnnotation(
                        name=protocol_json['protocolType']['name'],
                        term_accession=protocol_json['protocolType']['termAccession'],
                        term_source=protocol_json['protocolType']['termSource']
                    )
                )
                study.protocols.append(protocol)
            for assay_json in study_json['assays']:
                logger.debug('Build Study Assay object')
                assay = Assay(
                    measurement_type=OntologyAnnotation(
                        name=assay_json['measurementType']['name'],
                        term_accession=assay_json['measurementType']['termAccession'],
                        term_source=assay_json['measurementType']['termSource']
                    ),
                    technology_type=OntologyAnnotation(
                        name=assay_json['technologyType']['name'],
                        term_accession=assay_json['technologyType']['termAccession'],
                        term_source=assay_json['technologyType']['termSource']
                    ),
                    technology_platform=assay_json['technologyPlatform'],
                    file_name=assay_json['fileName']
                )
                study.assays.append(assay)
            for factor_json in study_json['factors']:
                logger.debug('Build Study Factor object')
                factor = StudyFactor(
                    name=factor_json['factorName'],
                    factor_type=OntologyAnnotation(
                        name=factor_json['factorType']['name'],
                        term_accession=factor_json['factorType']['termAccession'],
                        term_source=factor_json['factorType']['termSource']
                    )
                )
                study.factors.append(factor)
            sources_dict = dict()
            for source_json in study_json['sources']:
                logger.debug('Build Source object')
                source = Source(
                    name=source_json['name'],
                )
                for characteristic_json in source_json['characteristics']:
                    logger.debug('Build Ontology Annotation object (Source Characteristic)')
                    if isinstance(characteristic_json['value'], int or float):
                        characteristic = Characteristic(
                            category=characteristic_json['category'],
                            value=characteristic_json['value'],
                            unit=OntologyAnnotation(
                                name=characteristic_json['unit']['name'],
                                term_accession=characteristic_json['unit']['termAccession'],
                                term_source=characteristic_json['unit']['termSource'],
                            )
                        )
                    else:
                        characteristic = Characteristic(
                            category=characteristic_json['category'],
                            value=OntologyAnnotation(
                                name=characteristic_json['value']['name'],
                                term_accession=characteristic_json['value']['termAccession'],
                                term_source=characteristic_json['value']['termSource'],
                            )
                        )
                    source.characteristics.append(characteristic)
                sources_dict[source.name] = source
                study.sources.append(source)
            samples_dict = dict()
            for sample_json in study_json['samples']:
                logger.debug('Build Source object')
                sample = Sample(
                    name=sample_json['name'],
                    derives_from=sample_json['derivesFrom']
                )
                if isinstance(characteristic_json['value'], int or float):
                    characteristic = Characteristic(
                        category=characteristic_json['category'],
                        value=characteristic_json['value'],
                        unit=OntologyAnnotation(
                            name=characteristic_json['unit']['name'],
                            term_accession=characteristic_json['unit']['termAccession'],
                            term_source=characteristic_json['unit']['termSource'],
                        )
                    )
                else:
                    characteristic = Characteristic(
                        category=characteristic_json['category'],
                        value=OntologyAnnotation(
                            name=characteristic_json['value']['name'],
                            term_accession=characteristic_json['value']['termAccession'],
                            term_source=characteristic_json['value']['termSource'],
                        )
                    )
                sample.characteristics.append(characteristic)
                for factor_value_json in sample_json['factorValues']:
                    logger.debug('Build Ontology Annotation object (Sample Factor Value)')
                    factor_value = FactorValue(
                        value=OntologyAnnotation(
                            name=factor_value_json['value']['name'],
                            term_accession=factor_value_json['value']['termAccession'],
                            term_source=factor_value_json['value']['termSource'],
                        ),

                    )
                    sample.characteristics.append(factor_value)
                samples_dict[sample.name] = sample
                study.samples.append(sample)
            data_dict = dict()
            for data_json in study_json['data']:
                logger.debug('Build Data object')
                data = Data(
                    name=data_json['name'],
                    type_=data_json['type'],
                )
                data_dict[data.name] = data
                study.data.append(data)
            for process_json in study_json['processSequence']:
                logger.debug('Build Process object')
                process = Process(
                    executes_protocol=process_json['executesProtocol']['name'],
                    date_=process_json['date'],
                    performer=process_json['performer'],
                )
                for parameter_json in process_json['parameters']:
                    if isinstance(parameter_json['parameterValue'], int or float):
                        parameter = ParameterValue(
                            parameter_name=parameter_json['name'],
                            parameter_value=parameter_json['parameterValue'],
                            unit=OntologyAnnotation(
                                name=parameter_json['unit']['name'],
                                term_accession=parameter_json['unit']['termAccession'],
                                term_source=parameter_json['unit']['termSource'],
                            )
                        )
                    else:
                        parameter = ParameterValue(
                            parameter_name=parameter_json['name'],
                            parameter_value=OntologyAnnotation(
                                name=parameter_json['parameterValue']['name'],
                                term_accession=parameter_json['parameterValue']['termAccession'],
                                term_source=parameter_json['parameterValue']['termSource'],
                            )
                        )
                    process.parameters.append(parameter)
                study.process_sequence.append(process)
                inputs = list()
                for input_json in process_json['inputs']:
                    if input_json['name'].startswith('source-'):
                        input_ = sources_dict[input_json['name']]
                    elif input_json['name'].startswith('sample-'):
                        input_ = samples_dict[input_json['name']]
                    inputs.append(input_)
                    process.inputs = inputs
                outputs = list()
                for output_json in process_json['outputs']:
                    if output_json['name'].startswith('source-'):
                        output = sources_dict[output_json['name']]
                    elif output_json['name'].startswith('sample-'):
                        output = samples_dict[output_json['name']]
                    outputs.append(output)
                    process.outputs = outputs
                study.process_sequence.append(process)
            logger.debug('End building Study object')
            investigation.studies.append(study)
        logger.debug('End building Investigation object')
    return investigation
