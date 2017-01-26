from isatools.model.v1 import *


def read_investigation(J):

    I = Investigation()

    try:
        I.identifier = J["identifier"]
    except KeyError:
        pass

    try:
        I.title = J["title"]
    except KeyError:
        pass

    try:
        I.description = J["description"]
    except KeyError:
        pass

    try:
        I.submission_date = J["submissionDate"]
    except KeyError:
        pass

    try:
        I.public_release_date = J["publicReleaseDate"]
    except KeyError:
        pass

    try:
        I.ontology_source_references = read_list(J["ontologySourceReferences"], read_ontology_source)
    except KeyError:
        pass

    try:
        I.publications = read_list(J["publications"], read_publication)
    except KeyError:
        pass

    try:
        I.contacts = read_list(J["people"], read_person)
    except KeyError:
        pass

    try:
        I.contacts = read_list(J["studies"], read_study)
    except KeyError:
        pass

    try:
        I.filename = J["filename"]
    except KeyError:
        pass

    return I


def read_comment(comment_json):

    comment = Comment()

    try:
        comment.name = comment_json["name"]
    except KeyError:
        pass

    try:
        comment.value = comment_json["value"]
    except KeyError:
        pass

    return comment


def read_ontology_source(ontology_source_json):

    ontology_source = OntologySource()

    try:
        ontology_source.name = ontology_source_json["name"]
    except KeyError:
        pass

    try:
        ontology_source.file = ontology_source_json["file"]
    except KeyError:
        pass

    try:
        ontology_source.version = ontology_source_json["version"]
    except KeyError:
        pass

    try:
        ontology_source.description = ontology_source_json["description"]
    except KeyError:
        pass

    return ontology_source


def read_publication(publication_json):

    publication = Publication()

    try:
        publication.pubmed_id = publication_json["pubMedID"]
    except KeyError:
        pass

    try:
        publication.doi = publication_json["doi"]
    except KeyError:
        pass

    try:
        publication.author_list = publication_json["authorList"]
    except KeyError:
        pass

    try:
        publication.title = publication_json["title"]
    except KeyError:
        pass

    try:
        publication.status = publication_json["status"]
    except KeyError:
        pass

    try:
        publication.comments = read_list(publication_json["comments"], read_comment)
    except KeyError:
        pass

    return publication


def read_person(person_json):

    person = Person()

    try:
        person.last_name = person_json["lastName"]
    except KeyError:
        pass

    try:
        person.first_name = person_json["firstName"]
    except KeyError:
        pass

    try:
        person.mid_initials = person_json["midInitials"]
    except KeyError:
        pass

    try:
        person.email = person_json["email"]
    except KeyError:
        pass

    try:
        person.phone = person_json["phone"]
    except KeyError:
        pass

    try:
        person.fax = person_json["fax"]
    except KeyError:
        pass

    try:
        person.address = person_json["address"]
    except KeyError:
        pass

    try:
        person.affiliation = person_json["affiliation"]
    except KeyError:
        pass

    try:
        person.roles = read_list(person_json["roles"], read_annotation)
    except KeyError:
        pass

    try:
        person.comments = read_list(person_json["comments"], read_comment)
    except KeyError:
        pass

    return person


def read_list(list_json, read_func, ontology_sources_dict=None):

    if ontology_sources_dict is not None:
        return list(map(lambda x: read_func(x, ontology_sources_dict), list_json))

    else:
        return list(map(lambda x: read_func(x), list_json))


def read_annotation(annotation_json, ontology_sources_dict=None):

    annotation = OntologyAnnotation()

    try:
        annotation.term = annotation_json["annotationValue"]
    except KeyError:
        pass

    try:
        annotation.term_accession = annotation_json["termAccession"]
    except KeyError:
        pass

    try:
        annotation.term_source = annotation_json["termSource"]
    except KeyError:
        pass

    if ontology_sources_dict is not None:
        annotation.term_source = ontology_sources_dict[annotation.term_source]

    return annotation


def read_study_factor(factor_json, ontology_sources_dict=None):

    factor = StudyFactor()

    try:
        factor.name = factor_json["factorName"]
    except KeyError:
        pass

    try:
        factor.factor_type = read_annotation(factor_json["factorType"], ontology_sources_dict)
    except KeyError:
        pass

    try:
        factor.comments = read_list(factor_json["comments"], read_comment)
    except KeyError:
        pass

    return factor


def read_protocol_parameter(parameter_json, ontology_sources_dict=None):

    parameter = ProtocolParameter()

    try:
        parameter.parameter_name = read_annotation(parameter_json["parameterName"], ontology_sources_dict)
    except KeyError:
        pass

    return parameter


def read_protocol_component(component_json, ontology_sources_dict=None):

    component = ProtocolComponent()

    try:
        component.name = component_json["componentName"]
    except KeyError:
        pass

    try:
        component.component_type = read_annotation(component_json["componentType"], ontology_sources_dict)
    except KeyError:
        pass

    return component


def read_protocol(protocol_json, ontology_sources_dict=None):

    protocol = Protocol()

    try:
        protocol.name = protocol_json["name"]
    except KeyError:
        pass

    try:
        protocol.uri = protocol_json["uri"]
    except KeyError:
        pass

    try:
        protocol.version = protocol_json["version"]
    except KeyError:
        pass

    try:
        protocol.description = protocol_json["description"]
    except KeyError:
        pass

    try:
        protocol.protocol_type = read_annotation(protocol_json["protocolType"], ontology_sources_dict)
    except KeyError:
        pass

    try:
        protocol.parameters = read_list(protocol_json["parameters"], read_protocol_parameter, ontology_sources_dict)
    except KeyError:
        pass

    try:
        protocol.components = read_list(protocol_json["components"], read_protocol_component, ontology_sources_dict)
    except KeyError:
        pass

    return protocol


def read_process(J):

    process = Process()

    return process


def read_study(J):

    S = Study()

    try:
        S.identifier = J["identifier"]
    except KeyError:
        pass

    try:
        S.title = J["title"]
    except KeyError:
        pass

    try:
        S.description = J["description"]
    except KeyError:
        pass

    try:
        S.submission_date = J["submissionDate"]
    except KeyError:
        pass

    try:
        S.public_release_date = J["publicReleaseDate"]
    except KeyError:
        pass

    try:
        S.factors = read_list(J["factors"], read_study_factor)
    except KeyError:
        pass

    try:
        S.filename = J["filename"]
    except KeyError:
        pass

    try:
        S.process_sequence = read_list(J["processSequence"], read_process)
    except KeyError:
        pass

    try:
        S.protocols = read_list(J["protocols"], read_protocol)
    except KeyError:
        pass

    try:
        S.design_descriptors = read_list(J["studyDesignDescriptors"], read_annotation)
    except KeyError:
        pass

    try:
        S.assays = read_list(J["assays"], read_assay)
    except KeyError:
        pass

    return S
