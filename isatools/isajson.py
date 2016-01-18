from isatools.model.v1 import *
import json

def load(fp):
    investigation = None
    isajson = json.load(fp)
    if isajson is None:
        raise IOError("There was problem parsing the ISA JSON")
    else:
        investigation = Investigation(
            identifier=isajson['identifier'],
            title=isajson['title'],
            description=isajson['description'],
            submission_date=isajson['submissionDate'],
            public_release_date=isajson['publicReleaseDate']
        )
        for ontologySourceReference_json in isajson['ontologySourceReferences']:
            ontologySourceReference = OntologySourceReference(
                name=ontologySourceReference_json['name'],
                file=ontologySourceReference_json['file'],
                version=ontologySourceReference_json['version'],
                description=ontologySourceReference_json['description']
            )
            investigation.ontology_source_references.append(ontologySourceReference)
        for publication_json in isajson['publications']:
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
            # TODO: Impement support for roles
            investigation.contacts.append(person)
        for study_json in isajson['studies']:
            study = Study(
                identifier=study_json['identifier'],
                title=study_json['title'],
                description=study_json['description'],
                submission_date=study_json['submissionDate'],
                public_release_date=study_json['publicReleaseDate'],
                file_name=study_json['filename']
            )
            for study_publication_json in study_json['publications']:
                study_publication = Publication(
                    pubmed_id=study_publication_json['pubMedID'],
                    doi=study_publication_json['doi'],
                    author_list=study_publication_json['authorList'],
                    title=study_publication_json['title'],
                    status=OntologyAnnotation(
                        name=study_publication_json['status']['name'],
                        term_accession=study_publication_json['status']['termAccession'],
                        term_source=study_publication_json['status']['termSource']
                    )
                )
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
                )
                study.contacts.append(study_person)
            for design_descriptor_json in study_json['studyDesignDescriptors']:
                design_descriptor = OntologyAnnotation(
                    name=design_descriptor_json['name'],
                    term_accession=design_descriptor_json['termAccession'],
                    term_source=design_descriptor_json['termSource']
                )
                study.design_descriptors.append(design_descriptor)
            for protocol_json in study_json['protocols']:
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
                    file_name=assay_json['filename']
                )
                study.assays.append(assay)
            for factor_json in study_json['factors']:
                factor = StudyFactor(
                    name=factor_json['factorName'],
                    factor_type=OntologyAnnotation(
                        name=factor_json['factorType']['name'],
                        term_accession=factor_json['factorType']['termAccession'],
                        term_source=factor_json['factorType']['termSource'],
                    )
                )
                study.factors.append(factor)
            investigation.studies.append(study)
    return investigation
