import re
import iso8601
import chardet
import os
from isatools.model.v1 import *
import json
from networkx import DiGraph


class ValidationError(Exception):
    pass


class ValidationReport:

    def __init__(self, file_name):
        self.report = dict()
        self.report['warnings'] = list()
        self.report['errors'] = list()
        self.report['fatal'] = list()
        self.file_name = file_name

    def fatal(self, msg):
        self.report['fatal'].append({
            'message': msg,
        })

    def warn(self, msg):
        self.report['warnings'].append({
            'message': msg,
        })

    def error(self, msg):
        self.report['errors'].append({
            'message': msg,
        })

    def generate_report_json(self, reporting_level=3):
        if reporting_level == 0:
            return {
                'warnings': self.report['warnings']
            }
        if reporting_level == 1:
            return {
                'errors': self.report['errors']
            }
        if reporting_level == 2:
            return {
                'warnings': self.report['fatal']
            }
        if reporting_level == 3:
            return self.report

    def print_report(self, reporting_level=3):
        report_json = self.generate_report_json(reporting_level)
        if len(self.report['fatal']) > 0: print(self.file_name + ' ::: Fatal errors:')
        for message in report_json['fatal']:
            print(message['message'])
        if len(self.report['errors']) > 0: print(self.file_name + ' ::: Errors:')
        for message in report_json['errors']:
            print(message['message'])
        if len(self.report['warnings']) > 0: print(self.file_name + ' ::: Warnings:')
        for message in report_json['warnings']:
            print(message['message'])


def check_pubmed_id(pubmed_id_str, report):
    if pubmed_id_str is not '':
        pmid_regex = re.compile('[0-9]{8}')
        pmcid_regex = re.compile('PMC[0-9]{8}')
        if (pmid_regex.match(pubmed_id_str) is None) and (pmcid_regex.match(pubmed_id_str) is None):
            report.warn("PubMed ID {} is not valid format".format(pubmed_id_str))
    # TODO: Check if publication exists and consistency with other metadata in section; needs network connection


def date_is_iso8601(string):
    r"""Dates must be ISO8601 formatted, e.g. YYYY-MM-DD, YYYY-MM, YYYYMMDD

    Okay: 2016-04-07
    Okay: 2016-04
    Okay: 20160407
    Exxx: 201604
    """
    if string is not '':
        try:
            iso8601.parse_date(string)
        except iso8601.ParseError:
            return string, "Date is not ISO8601 format"


def check_iso8601_date(date_str, report):
    if date_str is not '':
        try:
            iso8601.parse_date(date_str)
        except iso8601.ParseError:
            report.warn("Date {} does not conform to ISO8601 format".format(date_str))


def is_iso8601_date(date_str):
    if date_str is not '':
        try:
            iso8601.parse_date(date_str)
        except iso8601.ParseError:
            return False
        return True
    return False


def check_doi(doi_str, report):
    if doi_str is not '':
        regexDOI = re.compile('(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![%"#? ])\\S)+)')
        if not regexDOI.match(doi_str):
            report.warn("DOI {} does not conform to DOI format".format(doi_str))


def check_encoding(fp, report):
    charset = chardet.detect(open(fp.name, 'rb').read())
    if charset['encoding'] is not 'UTF-8' and charset['encoding'] is not 'ascii':
        report.warn("File should be UTF-8 encoding but found it is '{0}' encoding with {1} confidence"
                    .format(charset['encoding'], charset['confidence']))


def is_utf8(fp):
    charset = chardet.detect(open(fp.name, 'rb').read())
    if charset['encoding'] is not 'UTF-8' and charset['encoding'] is not 'ascii':
        return False
    else:
        return True


def check_data_files(data_files, dir_context, report):
    for data_file in data_files:
        try:
            filename = data_file['name']
            with open(os.path.join(dir_context, filename)) as file:
                pass
        except IOError as e:
            report.warn("Cannot open file {}".format(filename))

# Alternative loading functions that do what isajson.load() does but in stages to determine linking

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
        protocol.protocol_type = load_ontology_annotation(protocol_json['protocolType'])
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
                component.component_type = load_ontology_annotation(component_json['componentType'])
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


def isajson_load(fp):
    def _build_assay_graph(process_sequence=list()):
        G = DiGraph()
        for process in process_sequence:
            if process.next_process is not None or len(
                    process.outputs) > 0:  # first check if there's some valid outputs to connect
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
    isajson = json.load(fp)
    if isajson is None:
        raise IOError("There was a problem opening the JSON file")
    else:
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
                investigation.ontology_source_references.append(ontology_source_reference)
        if 'publications' in inv_keys:
            for publication in load_publications(isajson['publications']):
                investigation.publications.append(publication)
        if 'people' in inv_keys:
            for person in load_people(isajson['people']):
                investigation.contacts.append(person)
        for study_json in isajson['studies']:
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
                    study.publications.append(study_publication)
            for study_person in load_people(study_json['people']):
                study.contacts.append(study_person)
            for study_characteristics_category_json in study_json['characteristicCategories']:
                study_characteristics_category_json['characteristicType']['@id'] = study_characteristics_category_json[
                    '@id']
                characteristic_category = load_ontology_annotation(
                    study_characteristics_category_json['characteristicType'])
                study.characteristic_categories.append(characteristic_category)
                # print(characteristic_category.id)
            for study_unit_json in study_json['unitCategories']:
                unit = load_ontology_annotation(study_unit_json)
                study.units.append(unit)
            for design_descriptor in load_ontology_annotations(study_json['studyDesignDescriptors']):
                study.design_descriptors.append(design_descriptor)
            for protocol in load_protocols(study_json['protocols']):
                study.protocols.append(protocol)
            for factor_json in study_json['factors']:
                factor = StudyFactor(
                    id_=factor_json['@id'],
                    name=factor_json['factorName'],
                    factor_type=load_ontology_annotation(factor_json['factorType'])
                )
                study.factors.append(factor)
            for source_json in study_json['materials']['sources']:
                source = Source(
                    id_=source_json['@id'],
                    name=source_json['name'][7:],
                )
                for characteristic in load_characteristics(source_json['characteristics']):
                    source.characteristics.append(characteristic)
                study.materials['sources'].append(source)
            for sample_json in study_json['materials']['samples']:
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
            for assay_json in study_json['assays']:
                assay = Assay(
                    measurement_type=load_ontology_annotation(assay_json['measurementType']),
                    technology_type=load_ontology_annotation(assay_json['technologyType']),
                    technology_platform=assay_json['technologyPlatform'],
                    filename=assay_json['filename']
                )
                # for assay_unit_json in assay_json['unitCategories']:
                #     unit = load_ontology_annotation(assay_unit_json)
                #     assay.units.append(unit)
                for data_file in load_data_files(assay_json['dataFiles']):
                    assay.data_files.append(data_file)
                for sample_json in assay_json['materials']['samples']:
                    sample = sample_json['@id']
                    assay.materials['samples'].append(sample)
                for assay_characteristics_category_json in assay_json['characteristicCategories']:
                    assay_characteristics_category_json['characteristicType']['@id'] = \
                    assay_characteristics_category_json['@id']
                    characteristic_category = load_ontology_annotation(
                        assay_characteristics_category_json['characteristicType'])
                    study.characteristic_categories.append(characteristic_category)
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
                study.assays.append(assay)
            investigation.studies.append(study)
        # now try and build links
        # isajson_link_objects(investigation=investigation)
        # one more pass to build graphs
        for study in investigation.studies:
            study.build_graph()
            for assay in study.assays:
                assay.build_graph()
    return investigation


def isajson_link_objects(investigation, report=None):
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
                if parameter_value.category == '#parameter/Array_Design_REF' and len(obj_list) == 0:
                    pv = ProtocolParameter(id_='#parameter/Array_Design_REF',
                                           parameter_name=OntologyAnnotation(name="Array Design REF"))
                    protocol.parameters.append(pv)
                    obj_list.append(pv)
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
        elif process.executes_protocol == '' and len(obj_list) == 0:
            if report is not None:
                report.error(
                    "A protocol has a blank reference, impossible to resolve object link".format(
                        process.executes_protocol))
        else:
            obj = obj_list[0]
            process.executes_protocol = obj

    for study in investigation.studies:
        # build links for SOURCES
        for source_or_sample in study.materials['sources'] + study.materials['samples']:
            # link source and samples characteristics to categories
            _link_chars_to_cats(chars=source_or_sample.characteristics, cats=study.characteristic_categories,
                                units=study.units, report=report)
        # build links for SAMPLES
        for sample in study.materials['samples']:
            _link_chars_to_cats(chars=sample.characteristics, cats=study.characteristic_categories, units=study.units,
                                report=report)
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
            _link_process_to_in_out_and_prots(process=process, node_list=node_list, prots=study.protocols,
                                              report=report)
            _link_pvs_to_params(process=process, units=study.units, report=report)
        # build prev-next process links
        for assay in study.assays:
            # first link assay-level samples back to study-level samples
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
