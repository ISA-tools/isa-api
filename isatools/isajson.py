from isatools.model.v1 import *
import json
import logging
from networkx import DiGraph
from jsonschema import Draft4Validator, RefResolver
import os
from isatools.validate.utils import check_iso8601_date, check_encoding, ValidationReport, ValidationError

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def validates(isa_json, report):
    """Validate JSON"""

    def _check_isa_schemas(isa_json):
        investigation_schema_path = os.path.join(
            os.path.dirname(__file__) + '/schemas/isa_model_version_1_0_schemas/core/investigation_schema.json')
        investigation_schema = json.load(open(investigation_schema_path))
        resolver = RefResolver('file://' + investigation_schema_path, investigation_schema)
        validator = Draft4Validator(investigation_schema, resolver=resolver)
        validator.validate(isa_json)

    def _check_filenames(isa_json, report):
        for study in isa_json['studies']:
            if study['filename'] is '':
                report.warn("A study filename is missing")
            for assay in study['assays']:
                if assay['filename'] is '':
                    report.warn("An assay filename is missing")

    def _check_ontology_sources(isa_json, report):
        ontology_source_refs = ['']  # initalize with empty string as the default none ref
        for ontology_source in isa_json['ontologySourceReferences']:
            if ontology_source['name'] is '':
                report.warn("An Ontology Source Reference is missing Term Source Name, so can't be referenced")
            else:
                ontology_source_refs.append(ontology_source['name'])
        return ontology_source_refs

    def _check_date_formats(isa_json, report):
        check_iso8601_date(isa_json['publicReleaseDate'], report)
        check_iso8601_date(isa_json['submissionDate'], report)
        for study in isa_json['studies']:
            check_iso8601_date(study['publicReleaseDate'], report)
            check_iso8601_date(study['submissionDate'], report)
            for process in study['processSequence']:
                check_iso8601_date(process['date'], report)

    def _check_term_source_refs(isa_json, ontology_source_refs, report):
        # get all matching annotation patterns by traversing the whole json structure
        if isinstance(isa_json, dict):
            if set(isa_json.keys()) == {'annotationValue', 'termAccession', 'termSource'} or \
                            set(isa_json.keys()) == {'@id', 'annotationValue', 'termAccession', 'termSource'}:
                if isa_json['termSource'] not in ontology_source_refs:
                    report.warn("Annotation {0} references {1} term source that has not been declared"
                                .format(isa_json['annotationValue'], isa_json['termSource']))
            for i in isa_json.keys():
                _check_term_source_refs(isa_json[i], ontology_source_refs, report)
        elif isinstance(isa_json, list):
            for j in isa_json:
                _check_term_source_refs(j, ontology_source_refs, report)

    def _check_pubmed_ids(isa_json, report):
        from isatools.isatab import check_pubmed_id
        for ipub in isa_json['publications']:
            check_pubmed_id(ipub['pubMedID'], report)
        for study in isa_json['studies']:
            for spub in study['publications']:
                check_pubmed_id(spub['pubMedID'], report)

    def _check_protocol_names(isa_json, report):
        protocol_refs = ['']  # initalize with empty string as the default none ref
        for study in isa_json['studies']:
            for protocol in study['protocols']:
                if protocol['name'] is '':
                    report.warn("A Protocol is missing Protocol Name, so can't be referenced")
                else:
                    protocol_refs.append(protocol['name'])
        return protocol_refs

    def _check_protocol_parameter_names(isa_json, report):
        protocol_parameter_refs = ['']  # initalize with empty string as the default none ref
        for study in isa_json['studies']:
            for protocol in study['protocols']:
                for parameter in protocol['parameters']:
                    if parameter['parameterName'] is '':
                        report.warn("A Protocol Parameter is missing Name, so can't be referenced")
                    else:
                        protocol_parameter_refs.append(parameter['parameterName'])
        return protocol_parameter_refs

    def _check_study_factor_names(isa_json, report):
        study_factor_refs = ['']  # initalize with empty string as the default none ref
        for study in isa_json['studies']:
            for factor in study['factors']:
                    if factor['factorName'] is '':
                        report.warn("A Study Factor is missing Name, so can't be referenced")
                    else:
                        study_factor_refs.append(study_factor_refs)
        return study_factor_refs

    def _collect_object_refs(isa_json, object_refs):
        # get all matching annotation patterns by traversing the whole json structure
        if isinstance(isa_json, dict):
            if '@id' in set(isa_json.keys()) and len(set(isa_json.keys())) > 1:
                if isa_json['@id'] not in object_refs:
                    object_refs.append(isa_json['@id'])
            for i in isa_json.keys():
                _collect_object_refs(isa_json[i], object_refs)
        elif isinstance(isa_json, list):
            for j in isa_json:
                _collect_object_refs(j, object_refs)
        return object_refs

    def _collect_id_refs(isa_json, id_refs):
        # get all matching annotation patterns by traversing the whole json structure
        if isinstance(isa_json, dict):
            if '@id' in set(isa_json.keys()) and len(set(isa_json.keys())) == 1:
                if isa_json['@id'] not in id_refs:
                    id_refs.append(isa_json['@id'])
            for i in isa_json.keys():
                _collect_id_refs(isa_json[i], id_refs)
        elif isinstance(isa_json, list):
            for j in isa_json:
                _collect_id_refs(j, id_refs)
        return id_refs

    def _check_object_refs(isa_json, object_refs, report):
        # get all matching annotation patterns by traversing the whole json structure
        if isinstance(isa_json, dict):
            if '@id' in set(isa_json.keys()) and len(set(isa_json.keys())) == 1:
                if isa_json['@id'] not in object_refs and isa_json['@id'] != '#parameter/Array_Design_REF':
                    report.error("Object reference {} not declared anywhere".format(isa_json['@id']))
            for i in isa_json.keys():
                _check_object_refs(isa_json=isa_json[i], object_refs=object_refs, report=report)
        elif isinstance(isa_json, list):
            for j in isa_json:
                _check_object_refs(j, object_refs, report)
        return object_refs

    def _check_object_usage(section, objects_declared, id_refs, report):
        for obj_ref in objects_declared:
            if obj_ref not in id_refs:
                report.error("Object reference {0} not used anywhere in {1}".format(obj_ref, section))

    def _check_data_files(isa_json, report):
        isajson_dir = os.path.dirname(report.file_name)
        for study in isa_json['studies']:
            for assay in study['assays']:
                for data_file in assay['dataFiles']:
                    try:
                        filename = data_file['name']
                        with open(os.path.join(isajson_dir, filename)) as file:
                            pass
                    except IOError as e:
                        report.warn("Cannot open file {}".format(filename))

    try:  # if can load the JSON (if the JSON is well-formed already), validate the JSON against our schemas
        _check_isa_schemas(isa_json)
        # if the JSON is validated against ISA JSON, let's start checking content
        _check_filenames(isa_json=isa_json, report=report)  # check if tab filenames are present for converting back
        ontology_source_refs = _check_ontology_sources(isa_json=isa_json, report=report)  # check if ontology sources are declared with enough info
        _check_date_formats(isa_json=isa_json, report=report)  # check if dates are all ISO8601 compliant
        _check_term_source_refs(isa_json=isa_json, ontology_source_refs=ontology_source_refs, report=report)  # check if ontology refs refer to ontology source
        _check_pubmed_ids(isa_json=isa_json, report=report)
        # _check_dois(isa_json=isa_json, report=report)
        _check_protocol_names(isa_json=isa_json, report=report)
        _check_protocol_parameter_names(isa_json=isa_json, report=report)
        _check_study_factor_names(isa_json=isa_json, report=report)
        _check_object_refs(isa_json=isa_json, object_refs=_collect_object_refs(isa_json=isa_json, object_refs=list()), report=report)

        # check protocols declared are used
        for study in isa_json['studies']:
            prot_obj_ids = list()
            for protocol in study['protocols']:
                prot_obj_ids.append(protocol['@id'])
            _check_object_usage(section=study['identifier'], objects_declared=prot_obj_ids, id_refs=_collect_id_refs(isa_json=isa_json, id_refs=list()), report=report)

        # check study factors declared are used
        for study in isa_json['studies']:
            prot_obj_ids = list()
            for protocol in study['factors']:
                prot_obj_ids.append(protocol['@id'])
            _check_object_usage(section=study['identifier'], objects_declared=prot_obj_ids, id_refs=_collect_id_refs(isa_json=isa_json, id_refs=list()), report=report)

        _check_data_files(isa_json=isa_json, report=report)

        # if we got this far, let's load using isajson.load()
        i = load(open(report.file_name))
        for study in i.studies:
            G = study.graph
            report.warn("Experimental graphs in study: {}".format(study.identifier))
            from isatools.isatab import _get_start_end_nodes, _all_end_to_end_paths
            start_nodes, end_nodes = _get_start_end_nodes(G)
            for path in _all_end_to_end_paths(G, start_nodes, end_nodes):
                type_seq_str = ""
                node_seq_str = ""
                for node in path:
                    if isinstance(node, Source):
                        type_seq_str += "(Source:{})->".format(node.name)
                        node_seq_str += "(Source)->"
                    elif isinstance(node, Sample):
                        type_seq_str += "(Sample:{})->".format(node.name)
                        node_seq_str += "(Sample)->"
                    elif isinstance(node, Process):
                        type_seq_str += "(Process:{})->".format(node.executes_protocol)
                        node_seq_str += "(Process)->"
                report.warn(type_seq_str[:len(type_seq_str) - 2])

    except ValidationError as isa_schema_validation_error:
        raise isa_schema_validation_error
    print(report.print_report())


def validate_against_config(fp):
    study_config = json.load(open('/Users/dj/PycharmProjects/isa-api/isatools/schemas/isa_model_version_1_0_schemas/configurations/study_sample_config.json'))
    print("Validating against config: {}".format(study_config))
    isa_json = load(fp=fp)
    G = isa_json.studies[0].graph
    from isatools.isatab import _get_start_end_nodes, _all_end_to_end_paths
    start_nodes, end_nodes = _get_start_end_nodes(G)
    for path in _all_end_to_end_paths(G, start_nodes, end_nodes):
        chain_str = ""
        for node in path:
            if isinstance(node, Source):
                chain_str += "({})->".format(node.name)
            elif isinstance(node, Sample):
                chain_str += "({})->".format(node.name)
            elif isinstance(node, Process):
                chain_str += "({})->".format(node.executes_protocol.protocol_type.name)
        print(chain_str[:len(chain_str)-2])


def validate(fp):  # default reporting
    """Validate JSON file"""
    report = ValidationReport(fp.name)
    check_encoding(fp, report)
    try:  # first, try open the file as a JSON
        try:
            isa_json = json.load(fp=fp)
            validates(isa_json, report)
        except ValueError as json_load_error:
            report.fatal("There was an error when trying to parse the JSON")
            raise json_load_error
    except SystemError as system_error:
        report.fatal("There was a general system error")
        raise system_error


def load_ontology_source_reference(ontology_source_reference_json):
    ontology_source_reference = OntologySourceReference()
    keys = ontology_source_reference_json.keys()
    if 'name' in keys:
        ontology_source_reference.name = ontology_source_reference_json['name']
    if 'file' in keys:
        ontology_source_reference.file = ontology_source_reference_json['file']
    if 'version' in keys:
        ontology_source_reference.version = ontology_source_reference_json['version']
    if 'description' in keys:
        ontology_source_reference.description = ontology_source_reference_json['description']
    return ontology_source_reference


def load_ontology_source_references(ontology_source_references_json):
    for ontology_source_reference_json in ontology_source_references_json:
        yield load_ontology_source_reference(ontology_source_reference_json)


def load_comment(comment_json):
    keys = comment_json.keys()
    comment = Comment()
    if 'name' in keys:
        comment.name = comment_json['name']
    if 'value' in keys:
        comment.value = comment_json['value']
    return comment


def load_comments(comments_json):
    for comment_json in comments_json:
        yield load_comment(comment_json)


def load_person(person_json):
    person = Person()
    keys = person_json.keys()
    if 'lastName' in keys:
        person.last_name = person_json['lastName']
    if 'firstName' in keys:
        person.first_name = person_json['firstName']
    if 'midInitials' in keys:
        person.mid_initials = person_json['midInitials']
    if 'email' in keys:
        person.email = person_json['email']
    if 'phone' in keys:
        person.phone = person_json['phone']
    if 'fax' in keys:
        person.fax = person_json['fax']
    if 'address' in keys:
        person.address = person_json['address']
    if 'affiliation' in keys:
        person.affiliation = person_json['affiliation']
    if 'roles' in keys:
        for role_json in person_json['roles']:
            role = OntologyAnnotation(
                name=role_json['annotationValue'],
                term_accession=role_json['termAccession'],
                term_source=role_json['termSource']
            )
            person.roles.append(role)
    if 'comments' in keys:
        for comment in load_comments(person_json['comments']):
            person.comments.append(comment)
    return person


def load_people(people_json):
    for person_json in people_json:
        yield load_person(person_json)


def load_ontology_annotation(ontology_annotation_json):
    keys = ontology_annotation_json.keys()
    ontology_annotation = OntologyAnnotation()
    if '@id' in keys:
        ontology_annotation.id = ontology_annotation_json['@id']
    if 'annotationValue' in keys:
        ontology_annotation.name = ontology_annotation_json['annotationValue']
    if 'termAccession' in keys:
        ontology_annotation.term_accession = ontology_annotation_json['termAccession']
    if 'termSource' in keys:
        ontology_annotation.term_source = ontology_annotation_json['termSource']
    return ontology_annotation


def load_ontology_annotations(ontology_annotations_json):
    for ontology_annotation_json in ontology_annotations_json:
        yield load_ontology_annotation(ontology_annotation_json)


def load_publication(publication_json):
    keys = publication_json.keys()
    publication = Publication()
    if 'pubMedID' in keys:
        publication.pubmed_id = publication_json['pubMedID']
    if 'doi' in keys:
        publication.doi = publication_json['doi']
    if 'authorList' in keys:
        publication.author_list = publication_json['authorList']
    if 'status' in keys:
        if isinstance(publication_json['status'], dict):
            publication.status = load_ontology_annotation(publication_json['status'])
        else:
            publication.status = publication_json['status']
    if 'comments' in keys:
        for comment in load_comments(publication_json['comments']):
            publication.comments.append(comment)
    return publication


def load_publications(publications_json):
    for publication_json in publications_json:
        yield load_publication(publication_json)


def load_protocol(protocol_json):
    keys = protocol_json.keys()
    protocol = Protocol()
    if '@id' in keys:
        protocol.id = protocol_json['@id']
    if 'name' in keys:
        protocol.name = protocol_json['name']
    if 'uri' in keys:
        protocol.uri = protocol_json['uri']
    if 'description' in keys:
        protocol.description = protocol_json['description']
    if 'version' in keys:
        protocol.version = protocol_json['version']
    if 'protocolType' in keys:
        protocol.protocol_type = protocol_json['protocolType']
    if 'parameters' in keys:
        for parameter_json in protocol_json['parameters']:
            parameter = ProtocolParameter()
            if '@id' in parameter_json.keys():
                parameter.id = parameter_json['@id']
            if 'parameterName' in parameter_json.keys():
                parameter.parameter_name = load_ontology_annotation(parameter_json['parameterName'])
            protocol.parameters.append(parameter)
    if 'components' in keys:
        for component_json in protocol_json['components']:
            component_keys = component_json.keys()
            component = ProtocolComponent()
            if 'componentName' in component_keys:
                component.name = component_json['componentName']
            if 'componentType' in component_keys:
                component.component_type = component_json['componentType']
            protocol.components.append(component)
    return protocol


def load_protocols(protocols_json):
    for protocol_json in protocols_json:
        yield load_protocol(protocol_json)


def load_process(process_json):
    keys = process_json.keys()
    process = Process()
    if '@id' in keys:
        process.id = process_json['@id']
    if 'executesProtocol' in keys:
        process.executes_protocol = process_json['executesProtocol']['@id']
    if 'name' in keys:
        process.name = process_json['name']
    if 'comments' in keys:
        for comment in load_comments(process_json['comments']):
            process.comments.append(comment)
    if 'date' in keys:
        process.date = process_json['date']
    if 'performer' in keys:
        process.performer = process_json['performer']
    if 'previousProcess' in keys:
        process.prev_process = process_json['previousProcess']['@id']
    if 'nextProcess' in keys:
        process.next_process = process_json['nextProcess']['@id']
    return process


def load_parameter_value(parameter_value_json):
    keys = parameter_value_json.keys()
    pv = ParameterValue()
    if 'category' in keys:
        pv.category = parameter_value_json['category']['@id']
    if 'value' in keys:
        value = parameter_value_json['value']
        if isinstance(value, int) or isinstance(value, float):
            pv.value = value
            if 'unit' in keys:
                pv.unit = parameter_value_json['unit']['@id']
        elif isinstance(value, dict):
            pv.value = load_ontology_annotation(value)
        elif isinstance(value, str):
            pv.value = value
    return pv


def load_characteristic(characteristic_json):
    keys = characteristic_json.keys()
    characteristic = Characteristic()
    if 'category' in keys:
        characteristic.category = characteristic_json['category']['@id']
    if 'value' in keys:
        value = characteristic_json['value']
        if isinstance(value, int) or isinstance(value, float):
            characteristic.value = value
            if 'unit' in keys:
                characteristic.unit = characteristic_json['unit']['@id']
        elif isinstance(value, dict):
            characteristic.value = load_ontology_annotation(value)
        elif isinstance(value, str):
            characteristic.value = value
    return characteristic


def load_characteristics(characteristics_json):
    for characteristic_json in characteristics_json:
        yield load_characteristic(characteristic_json)


def load_factor_value(factor_value_json):
    keys = factor_value_json.keys()
    fv = FactorValue()
    if 'category' in keys:
        fv.category = factor_value_json['category']['@id']
    if 'value' in keys:
        value = factor_value_json['value']
        if isinstance(value, int) or isinstance(value, float):
            fv.value = value
            if 'unit' in keys:
                fv.unit = factor_value_json['unit']['@id']
        elif isinstance(value, dict):
            fv.value = load_ontology_annotation(value)
        elif isinstance(value, str):
            fv.value = value
    return fv


def load_factor_values(factor_values_json):
    for factor_value_json in factor_values_json:
        yield load_factor_value(factor_value_json)


def load_data_file(data_json):
    keys = data_json.keys()
    data_file = DataFile()
    if '@id' in keys:
        data_file.id = data_json['@id']
    if 'name' in keys:
        data_file.filename = data_json['name']
    if 'type' in keys:
        data_file.label = data_json['type']
    for comment in load_comments(data_json['comments']):
        data_file.comments.append(comment)
    return data_file


def load_data_files(data_files_json):
    for data_file_json in data_files_json:
        yield load_data_file(data_file_json)


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
        inv_keys = isajson.keys()
        investigation = Investigation()
        if 'identifier' in inv_keys:
            investigation.identifier = isajson['identifier']
        if 'title' in inv_keys:
            investigation.title = isajson['title']
        if 'description' in inv_keys:
            investigation.description = isajson['description']
        if 'submissionDate' in inv_keys:
            investigation.submission_date = isajson['submissionDate']
        if 'publicReleaseDate' in inv_keys:
            investigation.public_release_date = isajson['publicReleaseDate']
        if 'filename' in inv_keys:
            investigation.filename = isajson['filename']
        if 'comments' in inv_keys:
            for comment in load_comments(isajson['comments']):
                investigation.comments.append(comment)
        if 'ontologySourceReferences' in inv_keys:
            for ontology_source_reference in load_ontology_source_references(isajson['ontologySourceReferences']):
                logger.debug('Build Ontology Source Reference object')
                investigation.ontology_source_references.append(ontology_source_reference)
        if 'publications' in inv_keys:
            for publication in load_publications(isajson['publications']):
                logger.debug('Build Investigation Publication object')
                investigation.publications.append(publication)
        if 'people' in inv_keys:
            for person in load_people(isajson['people']):
                logger.debug('Build Investigation Person object')
                investigation.contacts.append(person)

        logger.debug('Start building Studies objects')
        for study_json in isajson['studies']:
            logger.debug('Start building Study object')
            study_keys = study_json.keys()
            study = Study()
            if 'identifier' in study_keys:
                study.identifier = study_json['identifier']
            if 'title' in study_keys:
                study.title = study_json['title']
            if 'description' in study_keys:
                study.description = study_json['description']
            if 'submissionDate' in study_keys:
                study.submission_date = study_json['submissionDate']
            if 'publicReleaseDate' in study_keys:
                study.public_release_date = study_json['publicReleaseDate']
            if 'filename' in study_keys:
                study.filename = study_json['filename']
            if 'comments' in study_keys:
                for comment in load_comments(study_json['comments']):
                    study.comments.append(comment)
            if 'publications' in study_keys:
                for study_publication in load_publications(study_json['publications']):
                    logger.debug('Build Study Publication object')
                    study.publications.append(study_publication)
            for study_person in load_people(study_json['people']):
                logger.debug('Build Study Person object')
                study.contacts.append(study_person)
            for study_characteristics_category_json in study_json['characteristicCategories']:
                study_characteristics_category_json['characteristicType']['@id'] = study_characteristics_category_json['@id']
                characteristic_category = load_ontology_annotation(study_characteristics_category_json['characteristicType'])
                study.characteristic_categories.append(characteristic_category)
                # print(characteristic_category.id)
            for study_unit_json in study_json['unitCategories']:
                unit = load_ontology_annotation(study_unit_json)
                study.units.append(unit)
            for design_descriptor in load_ontology_annotations(study_json['studyDesignDescriptors']):
                logger.debug('Build Ontology Annotation object (Study Design Descriptor)')
                study.design_descriptors.append(design_descriptor)
            for protocol in load_protocols(study_json['protocols']):
                logger.debug('Build Study Protocol object')
                study.protocols.append(protocol)
            for factor_json in study_json['factors']:
                logger.debug('Build Study Factor object')
                factor = StudyFactor(
                    id_=factor_json['@id'],
                    name=factor_json['factorName'],
                    factor_type=load_ontology_annotation(factor_json['factorType'])
                )
                study.factors.append(factor)
            for source_json in study_json['materials']['sources']:
                logger.debug('Build Source object')
                source = Source(
                    id_=source_json['@id'],
                    name=source_json['name'][7:],
                )
                for characteristic in load_characteristics(source_json['characteristics']):
                    source.characteristics.append(characteristic)
                study.materials['sources'].append(source)
            for sample_json in study_json['materials']['samples']:
                logger.debug('Build Sample object')
                sample = Sample(
                    id_=sample_json['@id'],
                    name=sample_json['name'][7:],
                    derives_from=sample_json['derivesFrom']
                )
                for characteristic in load_characteristics(sample_json['characteristics']):
                    sample.characteristics.append(characteristic)
                for factor_value in load_factor_values(sample_json['factorValues']):
                    sample.factor_values.append(factor_value)
                study.materials['samples'].append(sample)
            for study_process_json in study_json['processSequence']:
                logger.debug('Build Process object')
                process = load_process(study_process_json)
                for parameter_value_json in study_process_json['parameterValues']:
                    parameter_value = load_parameter_value(parameter_value_json)
                    process.parameter_values.append(parameter_value)
                for input_json in study_process_json['inputs']:
                    if '@id' in input_json.keys():
                        process.inputs.append(input_json['@id'])
                for output_json in study_process_json['outputs']:
                    if '@id' in output_json.keys():
                        process.outputs.append(output_json['@id'])
                study.process_sequence.append(process)
            study.graph = _build_assay_graph(study.process_sequence)
            for assay_json in study_json['assays']:
                logger.debug('Start building Assay object')
                logger.debug('Build Study Assay object')
                assay = Assay(
                    measurement_type=load_ontology_annotation(assay_json['measurementType']),
                    technology_type=load_ontology_annotation(assay_json['technologyType']),
                    technology_platform=assay_json['technologyPlatform'],
                    filename=assay_json['filename']
                )
                for assay_unit_json in assay_json['unitCategories']:
                    unit = load_ontology_annotation(assay_unit_json)
                    # assay.units.append(unit)
                for data_file in load_data_files(assay_json['dataFiles']):
                    assay.data_files.append(data_file)
                for sample_json in assay_json['materials']['samples']:
                    sample = sample_json['@id']
                    assay.materials['samples'].append(sample)
                for assay_characteristics_category_json in assay_json['characteristicCategories']:
                    characteristic_category = load_ontology_annotation(assay_characteristics_category_json)
                    study.characteristic_categories.append(characteristic_category)  # PUT AT STUDY LEVEL
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
                    for characteristic in load_characteristics(other_material_json['characteristics']):
                        material.characteristics.append(characteristic)
                    assay.materials['other_material'].append(material)
                for assay_process_json in assay_json['processSequence']:
                    process = load_process(assay_process_json)
                    for parameter_value_json in assay_process_json['parameterValues']:
                        parameter_value = load_parameter_value(parameter_value_json)
                        process.parameter_values.append(parameter_value)
                    for input_json in assay_process_json['inputs']:
                        if '@id' in input_json.keys():
                            process.inputs.append(input_json['@id'])
                    for output_json in assay_process_json['outputs']:
                        if '@id' in output_json.keys():
                            process.outputs.append(output_json['@id'])
                    assay.process_sequence.append(process)
                    assay.graph = _build_assay_graph(assay.process_sequence)
                study.assays.append(assay)
            logger.debug('End building Study object')
            investigation.studies.append(study)
        logger.debug('End building Studies objects')
        logger.debug('End building Investigation object')

        # now try and build links
        # link_objects(investigation)
    return investigation


def link_objects(investigation, report=None):

    def _link_chars_to_cats(chars, cats, units, report):
        for x, char in enumerate(chars):
            if char.category is not None:
                obj_list = [o for o in cats if o.id == char.category]
                if len(obj_list) > 1:
                    if report is not None:
                        report.error(
                            "Duplicate object identifier '{}' declared, impossible to resolve object links".format(
                                char.category))
                elif char.category != '' and len(obj_list) == 0:
                    if report is not None:
                        report.error(
                            "A characteristic category '{}' has been referenced that has not been declared at the Study level".format(
                                char.category))
                else:
                    obj = obj_list[0]
                    chars[x].category = obj
            if char.unit is not None:
                obj_list = [o for o in units if o.id == char.unit]
                if len(obj_list) > 1:
                    if report is not None:
                        report.error(
                            "Duplicate object identifier '{}' declared, impossible to resolve object links".format(
                                char.unit))
                elif char.unit != '' and len(obj_list) == 0:
                    if report is not None:
                        report.error(
                            "A unit '{}' has been referenced that has not been declared at the Study level".format(
                                char.unit))
                else:
                    obj = obj_list[0]
                    chars[x].unit = obj

    def _link_pvs_to_params(process, units, report):
        for x, parameter_value in enumerate(process.parameter_values):
            protocol = [o for o in study.protocols if o.id == process.executes_protocol.id][0]  # just assume it works
            if parameter_value.category is not None:
                obj_list = [o for o in protocol.parameters if o.id == parameter_value.category]
                if len(obj_list) > 1:
                    if report is not None:
                        report.error(
                            "Duplicate object identifier '{}' declared, impossible to resolve object links".format(
                                parameter_value.category))
                elif parameter_value.category != '' and len(obj_list) == 0:
                    if report is not None:
                        report.error(
                            "A parameter '{}' has been referenced that has not been declared at the Study level".format(
                                parameter_value.category))
                else:
                    obj = obj_list[0]
                    process.parameter_values[x].category = obj
            # link UNITS
            if parameter_value.unit is not None:
                obj_list = [o for o in units if o.id == parameter_value.unit]
                if len(obj_list) > 1:
                    if report is not None:
                        report.error(
                            "Duplicate object identifier '{}' declared, impossible to resolve object links".format(
                                parameter_value.unit))
                elif parameter_value.unit != '' and len(obj_list) == 0:
                    if report is not None:
                        report.error(
                            "A unit '{}' has been referenced that has not been declared at the Study level".format(
                                parameter_value.unit))
                else:
                    obj = obj_list[0]
                    process.parameter_values[x].unit = obj

    def _link_process_to_in_out_and_prots(process, node_list, prots, report):
        for x, input_ in enumerate(process.inputs):
            obj_list = [o for o in node_list if o.id == input_]
            if len(obj_list) > 1:
                if report is not None:
                    report.error(
                        "Duplicate object identifier '{}' declared, impossible to resolve object links".format(
                            input_))
            elif input_ != '' and len(obj_list) == 0:
                if report is not None:
                    report.error(
                        "A source '{}' has been referenced that has not been declared at the Study level".format(
                            input_))
            else:
                obj = obj_list[0]
                process.inputs[x] = obj
        # build study samples links
        for x, output in enumerate(process.outputs):
            obj_list = [o for o in node_list if o.id == output]
            if len(obj_list) > 1:
                if report is not None:
                    report.error(
                        "Duplicate object identifier '{}' declared, impossible to resolve object links".format(
                            output))
            elif output != '' and len(obj_list) == 0:
                if report is not None:
                    report.error(
                        "A sample '{}' has been referenced that has not been declared at the Study level".format(
                            output))
            else:
                obj = obj_list[0]
                process.outputs[x] = obj
        # build protocol link
        obj_list = [o for o in prots if o.id == process.executes_protocol]
        if len(obj_list) > 1:
            if report is not None:
                report.error(
                    "Duplicate object identifier '{}' declared, impossible to resolve object links".format(
                        process.executes_protocol))
        elif process.executes_protocol != '' and len(obj_list) == 0:
            if report is not None:
                report.error(
                    "A protocol '{}' has been referenced that has not been declared at the Study level".format(
                        process.executes_protocol))
        else:
            obj = obj_list[0]
            process.executes_protocol = obj

    for study in investigation.studies:
        # build links for SOURCES
        for source in study.materials['sources']:
            # link source and samples characteristics to categories
            _link_chars_to_cats(chars=source.characteristics, cats=study.characteristic_categories, units=study.units, report=report)
        # build links for SAMPLES
        for sample in study.materials['samples']:
            _link_chars_to_cats(chars=sample.characteristics, cats=study.characteristic_categories, units=study.units, report=report)
            # currently only samples have factor values
            for x, factor_value in enumerate(sample.factor_values):
                if factor_value.category is not None:
                    obj_list = [o for o in study.factors if o.id == factor_value.category]
                    if len(obj_list) > 1:
                        if report is not None:
                            report.error(
                                "Duplicate object identifier '{}' declared, impossible to resolve object links".format(
                                    factor_value.category))
                    elif factor_value.category != '' and len(obj_list) == 0:
                        if report is not None:
                            report.error(
                                "A factor '{}' has been referenced that has not been declared at the Study level".format(
                                    factor_value.category))
                    else:
                        obj = obj_list[0]
                        sample.factor_values[x].category = obj
                # link UNITS
                if factor_value.unit is not None:
                    obj_list = [o for o in study.units if o.id == factor_value.unit]
                    if len(obj_list) > 1:
                        if report is not None:
                            report.error(
                                "Duplicate object identifier '{}' declared, impossible to resolve object links".format(
                                    factor_value.unit))
                    elif factor_value.unit != '' and len(obj_list) == 0:
                        if report is not None:
                            report.error(
                                "A unit '{}' has been referenced in {} {} that has not been declared at the Study level".format(
                                    factor_value.unit, sample.id, factor_value.category.name))
                    else:
                        obj = obj_list[0]
                        sample.factor_values[x].unit = obj
        # build links in PROCESSES
        # build study sources links
        node_list = study.materials['sources'] + study.materials['samples']
        for process in study.process_sequence:
            _link_process_to_in_out_and_prots(process=process, node_list=node_list, prots=study.protocols, report=report)
            _link_pvs_to_params(process=process, units=study.units, report=report)
        # build prev-next process links
        for assay in study.assays:
            node_list = study.materials['samples'] + assay.materials['other_material'] + assay.data_files
            for material in assay.materials['other_material']:
                _link_chars_to_cats(chars=material.characteristics, cats=study.characteristic_categories,
                                    units=study.units, report=report)
            for x, process in enumerate(assay.process_sequence):
                _link_process_to_in_out_and_prots(process=process, node_list=node_list, prots=study.protocols,
                                                  report=report)
                # build pv links
                _link_pvs_to_params(process=process, units=study.units, report=report)
                # build prev link
                obj_list = [o for o in assay.process_sequence if o.id == process.prev_process]
                if len(obj_list) > 1:
                    if report is not None:
                        report.error(
                            "Duplicate object identifier '{}' declared, impossible to resolve object links".format(
                                process.prev_process))
                elif len(obj_list) == 1:
                    obj = obj_list[0]
                    assay.process_sequence[x].prev_process = obj
                # build next link
                obj_list = [o for o in assay.process_sequence if o.id == process.next_process]
                if len(obj_list) > 1:
                    if report is not None:
                        report.error(
                            "Duplicate object identifier '{}' declared, impossible to resolve object links".format(
                                process.next_process))
                elif len(obj_list) == 1:
                    obj = obj_list[0]
                    assay.process_sequence[x].next_process = obj


def collect_term_source_refs(obj):
    t_list = list()
    if isinstance(obj, list):
        for item in obj:
            t = collect_term_source_refs(item)
            t_list += t
    elif '__dict__' in dir(obj):
            for k in list(vars(obj).keys()):
                o = getattr(obj, k)
                t = collect_term_source_refs(o)
                t_list += t
    else:
        t_list.append(obj)
    return t_list


