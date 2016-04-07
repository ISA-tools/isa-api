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
        for study in isa_json['studies']:
            for assay in study['assays']:
                for data_file in assay['dataFiles']:
                    try:
                        filename = data_file['name']
                        with open(filename) as file:
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
        #i = load(open(investigation_schema_path))

    except ValidationError as isa_schema_validation_error:
        raise isa_schema_validation_error
    print(report.generate_report())


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
    report = ValidationReport()
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
    if 'annotationValue' in keys:
        ontology_annotation.name = ontology_annotation_json['annotationValue']
    if 'termAccession' in keys:
        ontology_annotation.term_accession = ontology_annotation_json['termAccession']
    if 'termSource' in keys:
        ontology_annotation.term_accession = ontology_annotation_json['termSource']
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
            term_source_dict = {'': None}
            for ontology_source_reference in load_ontology_source_references(isajson['ontologySourceReferences']):
                logger.debug('Build Ontology Source Reference object')
                term_source_dict[ontology_source_reference.name] = ontology_source_reference
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
        samples_dict = dict()
        sources_dict = dict()
        categories_dict = dict()
        protocols_dict = dict()
        factors_dict = dict()
        parameters_dict = dict()
        units_dict = dict()
        process_dict = dict()

        object_refs_by_id = dict()  # we can store anything with an @id in one dict rather than split them out?

        # populate ASSAY characteristicCategories first
        for study_json in isajson['studies']:
            for assay_json in study_json['assays']:
                for assay_characteristics_category_json in assay_json['characteristicCategories']:
                    characteristic_category = OntologyAnnotation(
                        id_=assay_characteristics_category_json['@id'],
                        name=assay_characteristics_category_json['characteristicType']['annotationValue'],
                        term_source=assay_characteristics_category_json['characteristicType']['termSource'],
                        term_accession=assay_characteristics_category_json['characteristicType']['termAccession'],
                    )
                    # study.characteristic_categories.append(characteristic_category)
                    categories_dict[characteristic_category.id] = characteristic_category

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
                characteristic_category = load_ontology_annotation(study_characteristics_category_json['characteristicType'])
                characteristic_category.id = study_characteristics_category_json['@id']
                study.characteristic_categories.append(characteristic_category)
                categories_dict[characteristic_category.id] = characteristic_category
            for study_unit_json in study_json['unitCategories']:
                unit = load_ontology_annotation(study_unit_json)
                unit.id = study_unit_json['@id']
                units_dict[unit.id] = unit
            for design_descriptor in load_ontology_annotations(study_json['studyDesignDescriptors']):
                logger.debug('Build Ontology Annotation object (Study Design Descriptor)')
                study.design_descriptors.append(design_descriptor)
            for protocol_json in study_json['protocols']:
                logger.debug('Build Study Protocol object')
                protocol = Protocol(
                    id_=protocol_json['@id'],
                    name=protocol_json['name'],
                    uri=protocol_json['uri'],
                    description=protocol_json['description'],
                    version=protocol_json['version'],
                    protocol_type=load_ontology_annotation(protocol_json['protocolType'])
                )
                for parameter_json in protocol_json['parameters']:
                    parameter = ProtocolParameter(
                        id_=parameter_json['@id'],
                        parameter_name=load_ontology_annotation(parameter_json['parameterName'])
                    )
                    protocol.parameters.append(parameter)
                    parameters_dict[parameter.id] = parameter
                for component_json in protocol_json['components']:
                    component = ProtocolComponent(
                        name=component_json['componentName'],
                        component_type=load_ontology_annotation(component_json['componentType'])
                    )
                    protocol.components.append(component)
                study.protocols.append(protocol)
                protocols_dict[protocol.id] = protocol
            for factor_json in study_json['factors']:
                logger.debug('Build Study Factor object')
                factor = StudyFactor(
                    id_=factor_json['@id'],
                    name=factor_json['factorName'],
                    factor_type=load_ontology_annotation(factor_json['factorType'])
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
                            value = load_ontology_annotation(characteristic_json['value'])
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
                            value = load_ontology_annotation(characteristic_json['value'])
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
                            value=load_ontology_annotation(factor_value_json['value'])

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
                    measurement_type=load_ontology_annotation(assay_json['measurementType']),
                    technology_type=load_ontology_annotation(assay_json['technologyType']),
                    technology_platform=assay_json['technologyPlatform'],
                    filename=assay_json['filename']
                )
                for assay_unit_json in assay_json['unitCategories']:
                    unit = load_ontology_annotation(assay_unit_json)
                    unit.id = assay_unit_json['@id']
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
                        for comment in load_comments(data_json['comments']):
                            data_file.comments.append(comment)
                    except KeyError:
                        pass
                    data_dict[data_file.id] = data_file
                    assay.data_files.append(data_file)
                for sample_json in assay_json['materials']['samples']:
                    sample = samples_dict[sample_json['@id']]
                    assay.materials['samples'].append(sample)
                for assay_characteristics_category_json in assay_json['characteristicCategories']:
                    characteristic_category = load_ontology_annotation(assay_characteristics_category_json)
                    characteristic_category.id = assay_characteristics_category_json['@id']
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
                            value=load_ontology_annotation(characteristic_json['value'])
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
                        for comment in load_comments(assay_process_json['comments']):
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
                                if isinstance(parameter_value_json['value'], dict):
                                    parameter_value.value = load_ontology_annotation(parameter_value_json['value'])
                                else:
                                    parameter_value.value = parameter_value_json['value']
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
