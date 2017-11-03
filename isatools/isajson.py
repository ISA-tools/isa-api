"""Functions for reading, writing and validating ISA-JSON.

Don't forget to read the ISA-JSON spec:
http://isa-specs.readthedocs.io/en/latest/isajson.html
"""
from __future__ import absolute_import

import json
import logging
import re
from json import JSONEncoder

from isatools.model import *

__author__ = 'djcomlab@gmail.com (David Johnson)'

logging.basicConfig(level=logging.ERROR)
log = logging.getLogger(__name__)

errors = []
warnings = []

# REGEXES
_RX_DOI = re.compile("(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![%'#? ])\\S)+)")
_RX_PMID = re.compile("[0-9]{8}")
_RX_PMCID = re.compile("PMC[0-9]{8}")


def load(fp):

    def get_comments(j):
        comments = []
        if "comments" in j.keys():
            for comment_json in j["comments"]:
                name = comment_json["name"]
                value = comment_json["value"]
                comment = Comment(name, value)
                comments.append(comment)
        return comments

    def get_roles(j):
        roles = None
        if "roles" in j.keys():
            roles = list()
            for role_json in j["roles"]:
                term = role_json["annotationValue"]
                term_accession = role_json["termAccession"]
                term_source = term_source_dict[role_json["termSource"]]
                role = OntologyAnnotation(term, term_source, term_accession)
                roles.append(role)
        return roles

    def get_jvalue(dict, key):
        if key in dict.keys():
            return dict[key]
        else:
            return None

    investigation_json = json.load(fp)
    investigation = Investigation(
        identifier=investigation_json["identifier"],
        title=investigation_json["title"],
        description=investigation_json["description"],
        submission_date=investigation_json["submissionDate"],
        public_release_date=investigation_json["publicReleaseDate"]
    )
    investigation.comments = get_comments(investigation_json)
    term_source_dict = {"": None}
    for ontologySourceReference_json in investigation_json["ontologySourceReferences"]:
        ontology_source_reference = OntologySource(
            name=ontologySourceReference_json["name"],
            file=ontologySourceReference_json["file"],
            version=ontologySourceReference_json["version"],
            description=ontologySourceReference_json["description"]
        )
        term_source_dict[ontology_source_reference.name] = ontology_source_reference
        investigation.ontology_source_references.append(ontology_source_reference)
    for publication_json in investigation_json["publications"]:
        publication = Publication(
            pubmed_id=publication_json["pubMedID"],
            doi=publication_json["doi"],
            author_list=publication_json["authorList"],
            title=publication_json["title"],
            status=OntologyAnnotation(
                term=publication_json["status"]["annotationValue"],
                term_accession=publication_json["status"]["termAccession"],
                term_source=term_source_dict[publication_json["status"]["termSource"]]
            )
        )
        try:
            publication.comments = get_comments(publication_json)
        except KeyError:
            pass
        investigation.publications.append(publication)
    for person_json in investigation_json["people"]:
        person = Person(
            last_name=person_json["lastName"],
            first_name=person_json["firstName"],
            mid_initials=person_json["midInitials"],
            email=person_json["email"],
            phone=person_json["phone"],
            fax=person_json["fax"],
            address=person_json["address"],
            affiliation=person_json["affiliation"],
            roles=[]
        )
        for role_json in person_json["roles"]:
            role = OntologyAnnotation(
                term=role_json["annotationValue"],
                term_accession=role_json["termAccession"],
                term_source=term_source_dict[role_json["termSource"]]
            )
            person.roles.append(role)
        person.comments = get_comments(person_json)
        investigation.contacts.append(person)
    samples_dict = dict()
    sources_dict = dict()
    categories_dict = dict()
    protocols_dict = dict()
    factors_dict = dict()
    parameters_dict = dict()
    units_dict = dict()

    # populate assay characteristicCategories first
    for study_json in investigation_json["studies"]:
        for assay_json in study_json["assays"]:
            for assay_characteristics_category_json in assay_json["characteristicCategories"]:
                characteristic_category = OntologyAnnotation(
                    id_=assay_characteristics_category_json["@id"],
                    term=assay_characteristics_category_json["characteristicType"]["annotationValue"],
                    term_source=term_source_dict[assay_characteristics_category_json["characteristicType"]["termSource"]],
                    term_accession=assay_characteristics_category_json["characteristicType"]["termAccession"],
                )
                # study.characteristic_categories.append(characteristic_category)
                categories_dict[characteristic_category.id] = characteristic_category
    for study_json in investigation_json["studies"]:
        process_dict = dict()
        study = Study(
            identifier=study_json["identifier"],
            title=study_json["title"],
            description=study_json["description"],
            submission_date=study_json["submissionDate"],
            public_release_date=study_json["publicReleaseDate"],
            filename=study_json["filename"]
        )
        try:
            study.comments = get_comments(study_json)
        except KeyError:
            pass
        for study_characteristics_category_json in study_json["characteristicCategories"]:
            characteristic_category = OntologyAnnotation(
                id_=study_characteristics_category_json["@id"],
                term=study_characteristics_category_json["characteristicType"]["annotationValue"],
                term_source=term_source_dict[study_characteristics_category_json["characteristicType"]["termSource"]],
                term_accession=study_characteristics_category_json["characteristicType"]["termAccession"],
            )
            study.characteristic_categories.append(characteristic_category)
            categories_dict[characteristic_category.id] = characteristic_category
        for study_unit_json in study_json["unitCategories"]:
            unit = OntologyAnnotation(id_=study_unit_json["@id"],
                                      term=study_unit_json["annotationValue"],
                                      term_source=term_source_dict[study_unit_json["termSource"]],
                                      term_accession=study_unit_json["termAccession"])
            units_dict[unit.id] = unit
            study.units.append(unit)
        for study_publication_json in study_json["publications"]:
            study_publication = Publication(
                pubmed_id=study_publication_json["pubMedID"],
                doi=study_publication_json["doi"],
                author_list=study_publication_json["authorList"],
                title=study_publication_json["title"],
                status=OntologyAnnotation(
                    term=study_publication_json["status"]["annotationValue"],
                    term_source=term_source_dict[study_publication_json["status"]["termSource"]],
                    term_accession=study_publication_json["status"]["termAccession"],
                )
            )
            try:
                study_publication.comments = get_comments(study_publication_json)
            except KeyError:
                pass
            study.publications.append(study_publication)
        for study_person_json in study_json["people"]:
            study_person = Person(
                last_name=study_person_json["lastName"],
                first_name=study_person_json["firstName"],
                mid_initials=study_person_json["midInitials"],
                email=study_person_json["email"],
                phone=study_person_json["phone"],
                fax=study_person_json["fax"],
                address=study_person_json["address"],
                affiliation=study_person_json["affiliation"],
            )
            study_person.roles = get_roles(study_person_json)
            try:
                study_person.comments = get_comments(study_person_json)
            except KeyError:
                pass
            study.contacts.append(study_person)
        for design_descriptor_json in study_json["studyDesignDescriptors"]:
            design_descriptor = OntologyAnnotation(
                term=design_descriptor_json["annotationValue"],
                term_accession=design_descriptor_json["termAccession"],
                term_source=term_source_dict[design_descriptor_json["termSource"]]
            )
            study.design_descriptors.append(design_descriptor)
        for protocol_json in study_json["protocols"]:
            protocol = Protocol(
                id_=protocol_json["@id"],
                name=protocol_json["name"],
                uri=protocol_json["uri"],
                description=protocol_json["description"],
                version=protocol_json["version"],
                protocol_type=OntologyAnnotation(
                    term=protocol_json["protocolType"]["annotationValue"],
                    term_accession=protocol_json["protocolType"]["termAccession"] if "termAccession" in protocol_json["protocolType"].keys() else "",
                    term_source=term_source_dict[protocol_json["protocolType"]["termSource"]] if "termSource" in protocol_json["protocolType"].keys() else None,
                )
            )
            for parameter_json in protocol_json["parameters"]:
                parameter = ProtocolParameter(
                    id_=parameter_json["@id"],
                    parameter_name=OntologyAnnotation(
                        term=parameter_json["parameterName"]["annotationValue"],
                        term_source=term_source_dict[parameter_json["parameterName"]["termSource"]],
                        term_accession=parameter_json["parameterName"]["termAccession"]
                    )
                )
                protocol.parameters.append(parameter)
                parameters_dict[parameter.id] = parameter
            for component_json in protocol_json["components"]:
                component = ProtocolComponent(
                    name=component_json["componentName"],
                    component_type=OntologyAnnotation(
                        term=component_json["componentType"]["annotationValue"],
                        term_source=term_source_dict[component_json["componentType"]["termSource"]],
                        term_accession=component_json["componentType"]["termAccession"]
                    )
                )
                protocol.components.append(component)
            study.protocols.append(protocol)
            protocols_dict[protocol.id] = protocol
        for factor_json in study_json["factors"]:
            factor = StudyFactor(
                id_=factor_json["@id"],
                name=factor_json["factorName"],
                factor_type=OntologyAnnotation(
                    term=factor_json["factorType"]["annotationValue"],
                    term_accession=factor_json["factorType"]["termAccession"],
                    term_source=term_source_dict[factor_json["factorType"]["termSource"]]
                )
            )
            study.factors.append(factor)
            factors_dict[factor.id] = factor
        for source_json in study_json["materials"]["sources"]:
            source = Source(
                id_=source_json["@id"],
                name=source_json["name"][7:],
            )
            for characteristic_json in source_json["characteristics"]:
                value = characteristic_json["value"]
                unit = None
                characteristic = Characteristic(category=categories_dict[characteristic_json["category"]["@id"]])
                if isinstance(value, dict):
                    try:
                        term = characteristic_json["value"]["annotationValue"]
                        if isinstance(term, (int, float)):
                            term = str(term)
                        value = OntologyAnnotation(
                            term=term,
                            term_source=term_source_dict[characteristic_json["value"]["termSource"]],
                            term_accession=characteristic_json["value"]["termAccession"])
                    except KeyError:
                        raise IOError("Can't create value as annotation")
                elif isinstance(value, (int, float)):
                    try:
                        unit = units_dict[characteristic_json["unit"]["@id"]]
                    except KeyError:
                        unit = None
                elif not isinstance(value, str):
                    raise IOError("Unexpected type in characteristic value")
                characteristic.value = value
                characteristic.unit = unit
                source.characteristics.append(characteristic)
            sources_dict[source.id] = source
            study.sources.append(source)
        for sample_json in study_json["materials"]["samples"]:
            sample = Sample(
                id_=sample_json["@id"],
                name=sample_json["name"][7:]
            )
            for characteristic_json in sample_json["characteristics"]:
                value = characteristic_json["value"]
                unit = None
                characteristic = Characteristic(
                        category=categories_dict[characteristic_json["category"]["@id"]])
                if isinstance(value, dict):
                    try:
                        value = OntologyAnnotation(
                            term=characteristic_json["value"]["annotationValue"],
                            term_source=term_source_dict[characteristic_json["value"]["termSource"]],
                            term_accession=characteristic_json["value"]["termAccession"])
                    except KeyError:
                        raise IOError("Can't create value as annotation")
                elif isinstance(value, int) or isinstance(value, float):
                    try:
                        unit = units_dict[characteristic_json["unit"]["@id"]]
                    except KeyError:
                        raise IOError("Can't create unit annotation")
                elif not isinstance(value, str):
                    raise IOError("Unexpected type in characteristic value")
                characteristic.value = value
                characteristic.unit = unit
                sample.characteristics.append(characteristic)
            for factor_value_json in sample_json["factorValues"]:
                try:
                    factor_value = FactorValue(
                        factor_name=factors_dict[factor_value_json["category"]["@id"]],
                        value=OntologyAnnotation(
                            term=factor_value_json["value"]["annotationValue"],
                            term_accession=factor_value_json["value"]["termAccession"],
                            term_source=term_source_dict[factor_value_json["value"]["termSource"]],
                        ),

                    )
                except TypeError:
                    factor_value = FactorValue(
                        factor_name=factors_dict[factor_value_json["category"]["@id"]],
                        value=factor_value_json["value"],
                        unit=units_dict[factor_value_json["unit"]["@id"]],
                    )
                sample.factor_values.append(factor_value)
            samples_dict[sample.id] = sample
            study.samples.append(sample)
            try:
                for source_id_ref_json in sample_json["derivesFrom"]:
                    sample.derives_from.append(sources_dict[source_id_ref_json["@id"]])
            except KeyError:
                sample.derives_from = []
        for study_process_json in study_json["processSequence"]:
            process = Process(
                id_=study_process_json["@id"],
                executes_protocol=protocols_dict[study_process_json["executesProtocol"]["@id"]],
            )
            try:
                process.comments = get_comments(study_process_json)
            except KeyError:
                pass
            try:
                process.date = study_process_json["date"]
            except KeyError:
                pass
            try:
                process.performer = study_process_json["performer"]
            except KeyError:
                pass
            for parameter_value_json in study_process_json["parameterValues"]:
                if isinstance(parameter_value_json["value"], int) or isinstance(parameter_value_json["value"], float):
                    parameter_value = ParameterValue(
                        category=parameters_dict[parameter_value_json["category"]["@id"]],
                        value=parameter_value_json["value"],
                        unit=units_dict[parameter_value_json["unit"]["@id"]],
                    )
                    process.parameter_values.append(parameter_value)
                else:
                    parameter_value = ParameterValue(
                        category=parameters_dict[parameter_value_json["category"]["@id"]],
                        )
                    try:
                        parameter_value.value = OntologyAnnotation(
                            term=parameter_value_json["value"]["annotationValue"],
                            term_accession=parameter_value_json["value"]["termAccession"],
                            term_source=term_source_dict[parameter_value_json["value"]["termSource"]],)
                    except TypeError:
                        parameter_value.value = parameter_value_json["value"]
                    process.parameter_values.append(parameter_value)
            for input_json in study_process_json["inputs"]:
                input_ = None
                try:
                    input_ = sources_dict[input_json["@id"]]
                except KeyError:
                    pass
                finally:
                    try:
                        input_ = samples_dict[input_json["@id"]]
                    except KeyError:
                        pass
                if input_ is None:
                    raise IOError("Could not find input node in sources or samples dicts: " + input_json["@id"])
                process.inputs.append(input_)
            for output_json in study_process_json["outputs"]:
                output = None
                try:
                    output = sources_dict[output_json["@id"]]
                except KeyError:
                    pass
                finally:
                    try:
                        output = samples_dict[output_json["@id"]]
                    except KeyError:
                        pass
                if output is None:
                    raise IOError("Could not find output node in sources or samples dicts: " + output_json["@id"])
                process.outputs.append(output)
            study.process_sequence.append(process)
            process_dict[process.id] = process
        for study_process_json in study_json["processSequence"]:  # 2nd pass
            try:
                prev_proc = study_process_json["previousProcess"]["@id"]
                process_dict[study_process_json["@id"]].prev_process = process_dict[prev_proc]
            except KeyError:
                pass

            try:
                next_proc = study_process_json["nextProcess"]["@id"]
                process_dict[study_process_json["@id"]].next_process = process_dict[next_proc]
            except KeyError:
                pass

        for assay_json in study_json["assays"]:
            process_dict = dict()
            assay = Assay(
                measurement_type=OntologyAnnotation(
                    term=assay_json["measurementType"]["annotationValue"],
                    term_accession=assay_json["measurementType"]["termAccession"],
                    term_source=term_source_dict[assay_json["measurementType"]["termSource"]]
                ),
                technology_type=OntologyAnnotation(
                    term=assay_json["technologyType"]["annotationValue"],
                    term_accession=assay_json["technologyType"]["termAccession"],
                    term_source=term_source_dict[assay_json["technologyType"]["termSource"]]
                ),
                technology_platform=assay_json["technologyPlatform"],
                filename=assay_json["filename"]
            )
            for assay_unit_json in assay_json["unitCategories"]:
                unit = OntologyAnnotation(id_=assay_unit_json["@id"],
                                          term=assay_unit_json["annotationValue"],
                                          term_source=term_source_dict[assay_unit_json["termSource"]],
                                          term_accession=assay_unit_json["termAccession"])
                units_dict[unit.id] = unit
                assay.units.append(unit)
            data_dict = dict()
            for data_json in assay_json["dataFiles"]:
                data_file = DataFile(
                    id_=data_json["@id"],
                    filename=data_json["name"],
                    label=data_json["type"],
                )
                try:
                    data_file.comments = get_comments(data_json)
                except KeyError:
                    pass
                data_dict[data_file.id] = data_file
                try:
                    data_file.derives_from = samples_dict[data_json["derivesFrom"][0]["@id"]]
                except KeyError:
                    data_file.derives_from = None
                assay.data_files.append(data_file)
            for sample_json in assay_json["materials"]["samples"]:
                sample = samples_dict[sample_json["@id"]]
                assay.samples.append(sample)
            for assay_characteristics_category_json in assay_json["characteristicCategories"]:
                characteristic_category =OntologyAnnotation(
                    id_=assay_characteristics_category_json["@id"],
                    term=assay_characteristics_category_json["characteristicType"]["annotationValue"],
                    term_source=term_source_dict[assay_characteristics_category_json["characteristicType"]["termSource"]],
                    term_accession=assay_characteristics_category_json["characteristicType"]["termAccession"],
                )
                study.characteristic_categories.append(characteristic_category)
                categories_dict[characteristic_category.id] = characteristic_category
            other_materials_dict = dict()
            for other_material_json in assay_json["materials"]["otherMaterials"]:
                material_name = other_material_json["name"]
                if material_name.startswith("labeledextract-"):
                    material_name = material_name[15:]
                else:
                    material_name = material_name[8:]
                material = Material(
                    id_=other_material_json["@id"],
                    name=material_name,
                    type_=other_material_json["type"],
                )
                for characteristic_json in other_material_json["characteristics"]:
                    characteristic = Characteristic(
                        category=categories_dict[characteristic_json["category"]["@id"]],
                        value=OntologyAnnotation(
                            term=characteristic_json["value"]["annotationValue"],
                            term_source=term_source_dict[characteristic_json["value"]["termSource"]],
                            term_accession=characteristic_json["value"]["termAccession"],
                        )
                    )
                    material.characteristics.append(characteristic)
                assay.other_material.append(material)
                other_materials_dict[material.id] = material
            for assay_process_json in assay_json["processSequence"]:
                process = Process(
                    id_=assay_process_json["@id"],
                    executes_protocol=protocols_dict[assay_process_json["executesProtocol"]["@id"]]
                )
                try:
                    process.comments = get_comments(assay_process_json)
                except KeyError:
                    pass
                # additional properties, currently hard-coded special cases
                if process.executes_protocol.protocol_type.term == "data collection" and assay.technology_type.term == "DNA microarray":
                    process.name = assay_process_json["name"]
                elif process.executes_protocol.protocol_type.term == "nucleic acid sequencing":
                    process.name = assay_process_json["name"]
                elif process.executes_protocol.protocol_type.term == "nucleic acid hybridization":
                    process.name = assay_process_json["name"]
                elif process.executes_protocol.protocol_type.term == "data transformation":
                    process.name = assay_process_json["name"]
                elif process.executes_protocol.protocol_type.term == "data normalization":
                    process.name = assay_process_json["name"]
                for input_json in assay_process_json["inputs"]:
                    input_ = None
                    try:
                        input_ = samples_dict[input_json["@id"]]
                    except KeyError:
                        pass
                    finally:
                        try:
                            input_ = other_materials_dict[input_json["@id"]]
                        except KeyError:
                            pass
                        finally:
                            try:
                                input_ = data_dict[input_json["@id"]]
                            except KeyError:
                                pass
                    if input_ is None:
                        raise IOError("Could not find input node in samples or materials or data dicts: " +
                                      input_json["@id"])
                    process.inputs.append(input_)
                for output_json in assay_process_json["outputs"]:
                    output = None
                    try:
                        output = samples_dict[output_json["@id"]]
                    except KeyError:
                        pass
                    finally:
                        try:
                            output = other_materials_dict[output_json["@id"]]
                        except KeyError:
                            pass
                        finally:
                                try:
                                    output = data_dict[output_json["@id"]]
                                except KeyError:
                                    pass
                    if output is None:
                        raise IOError("Could not find output node in samples or materials or data dicts: " +
                                      output_json["@id"])
                    process.outputs.append(output)
                for parameter_value_json in assay_process_json["parameterValues"]:
                    if "category" in parameter_value_json.keys():
                        if parameter_value_json["category"]["@id"] == "#parameter/Array_Design_REF":  # Special case
                            process.array_design_ref = parameter_value_json["value"]
                        elif isinstance(parameter_value_json["value"], int) or \
                                isinstance(parameter_value_json["value"], float):
                            parameter_value = ParameterValue(
                                category=parameters_dict[parameter_value_json["category"]["@id"]],
                                value=parameter_value_json["value"],
                            )
                            if "unit" in parameter_value_json.keys():
                                parameter_value.unit = units_dict[parameter_value_json["unit"]["@id"]]
                            process.parameter_values.append(parameter_value)
                        else:
                            parameter_value = ParameterValue(
                                category=parameters_dict[parameter_value_json["category"]["@id"]],
                                )
                            try:
                                parameter_value.value = OntologyAnnotation(
                                    term=parameter_value_json["value"]["annotationValue"],
                                    term_accession=parameter_value_json["value"]["termAccession"],
                                    term_source=term_source_dict[parameter_value_json["value"]["termSource"]],)
                            except TypeError:
                                parameter_value.value = parameter_value_json["value"]
                            process.parameter_values.append(parameter_value)
                    else:
                        log.warn("warning: parameter category not found for instance {}".format(parameter_json))
                assay.process_sequence.append(process)
                process_dict[process.id] = process

                for assay_process_json in assay_json["processSequence"]:  # 2nd pass
                    try:
                        prev_proc = assay_process_json["previousProcess"]["@id"]
                        process_dict[assay_process_json["@id"]].prev_process = process_dict[prev_proc]
                    except KeyError:
                        pass

                    try:
                        next_proc = assay_process_json["nextProcess"]["@id"]
                        process_dict[assay_process_json["@id"]].next_process = process_dict[next_proc]
                    except KeyError:
                        pass

            study.assays.append(assay)
        investigation.studies.append(study)
    return investigation


class ISAJSONEncoder(JSONEncoder):

    def default(self, o):

        def remove_nulls(d):
            return {k: v for k, v in d.items() if v or isinstance(v, list) or v == ''}

        def nulls_to_str(d):
            to_del = []
            for k, v in d.items():
                if not isinstance(v, list) and v is None:
                    d[k] = ''
                if (k == "unit" or k == "previousProcess" or k == "nextProcess") and (v is None or v == ''):
                    to_del.append(k)
            for k in to_del:
                del d[k]
            return d

        # TODO: deal with non-verbose mode parsing; currently will break because of missing k-v's
        clean_nulls = nulls_to_str  # creates verbose JSON if using nulls to str
        # clean_nulls = remove_nulls  # optimises by removing k-v's that are null or empty strings but breaks reader

        def get_comment(o):
            return clean_nulls(
                {
                    "name": o.name,
                    "value": o.value
                }
            )

        def get_comments(o):
            return list(map(lambda x: get_comment(x), o if o else []))

        def get_ontology_source(o):
            return clean_nulls(
                {
                    "name": o.name,
                    "description": o.description,
                    "file": o.file,
                    "version": o.version
                }
            )

        def get_ontology_annotation(o):
            return clean_nulls(
                {
                    "@id": id_gen(o),
                    "annotationValue": o.term,
                    "termAccession": o.term_accession,
                    "termSource": o.term_source.name if o.term_source else None
                }
            )

        def get_ontology_annotations(o):
            return list(map(lambda x: get_ontology_annotation(x), o))

        def get_person(o):
            return clean_nulls(
                {
                    "address": o.address,
                    "affiliation": o.affiliation,
                    "comments": get_comments(o.comments),
                    "email": o.email,
                    "fax": o.fax,
                    "firstName": o.first_name,
                    "lastName": o.last_name,
                    "midInitials": o.mid_initials if o.mid_initials else '',
                    "phone": o.phone,
                    "roles": get_ontology_annotations(o.roles)
                }
            )

        def get_people(o):
            return list(map(lambda x: get_person(x), o))

        def get_publication(o):
            return clean_nulls(
                {
                    "authorList": o.author_list,
                    "doi": o.doi,
                    "pubMedID": o.pubmed_id,
                    "status": get_ontology_annotation(o.status) if o.status else {"@id": ''},
                    "title": o.title
                }
            )

        def get_publications(o):
            return list(map(lambda x: get_publication(x), o))

        def get_protocol(o):
            return clean_nulls(
                {
                    "@id": id_gen(o),
                    "description": o.description,
                    "parameters": list(map(lambda x: {
                        "@id": id_gen(x),
                        "parameterName": get_ontology_annotation(x.parameter_name)
                    }, o.parameters)),  # TODO: Deal with Array Design REF
                    "name": o.name,
                    "protocolType": get_ontology_annotation(o.protocol_type),
                    "uri": o.uri,
                    "comments": get_comments(o.comments) if o.comments else [],
                    "components": [],  # TODO: Output components
                    "version": o.version
                }
            )

        def get_source(o):
            return clean_nulls(
                {
                    "@id": id_gen(o),
                    "name": o.name,
                    "characteristics": get_characteristics(o.characteristics)
                }
            )

        def get_characteristic(o):
            return clean_nulls(
                {
                    "category": {"@id": id_gen(o.category)} if o.category else None,
                    "value": get_value(o.value),
                    "unit": {"@id": id_gen(o.unit)} if o.unit else None
                }
            )

        def get_characteristics(o):
            return list(map(lambda x: get_characteristic(x), o))

        def get_value(o):
            if isinstance(o, OntologyAnnotation):
                return get_ontology_annotation(o)
            elif isinstance(o, (string_types, int, float)):
                return o
            else:
                raise ValueError("Unexpected value type found: %s", type(o))

        def get_characteristic_category(o):  # TODO: Deal with Material Type
            return clean_nulls(
                {
                    "@id": id_gen(o),
                    "characteristicType": get_ontology_annotation(o)
                }
            )

        def get_sample(o):
            return clean_nulls(
                {
                    "@id": id_gen(o),
                    "name": o.name,
                    "characteristics": get_characteristics(o.characteristics),
                    "factorValues": list(map(lambda x: clean_nulls(
                        {
                            "category": {"@id": id_gen(x.factor_name)} if x.factor_name else None,
                            "value": get_value(x.value),
                            "unit": {"@id": id_gen(x.unit)} if x.unit else None
                        }
                    ), o.factor_values))
            })

        def get_factor(o):
            return clean_nulls(
                {
                    "@id": id_gen(o),
                    "factorName": o.name,
                    "factorType": get_ontology_annotation(o.factor_type)
                }
            )

        def get_other_material(o):
            return clean_nulls(
                {
                    "@id": id_gen(o),
                    "name": o.name,
                    "type": o.type,
                    "characteristics": get_characteristics(o.characteristics)
                }
            )

        def sqeezstr(s):
            return s.replace(' ', '').lower()

        def id_gen(o):
            if o is not None:
                o_id = str(id(o))
                if isinstance(o, Source):
                    return '#source/' + o_id
                elif isinstance(o, Sample):
                    return '#sample/' + o_id
                elif isinstance(o, Material):
                    if o.type == 'Extract Name':
                        return '#material/extract-' + o_id
                    elif o.type == 'Labeled Extract Name':
                        return '#material/labledextract-' + o_id
                    else:
                        raise TypeError("Could not resolve data type labeled: " + o.type)
                elif isinstance(o, DataFile):
                        return '#data/{}-'.format(sqeezstr(o.label)) + o_id
                elif isinstance(o, Process):
                    return '#process/' + o_id  # TODO: Implement ID gen on different kinds of processes?
                else:
                    return '#' + o_id
            else:
                return None

        def get_process(o):
            return clean_nulls(
                {
                    "@id": id_gen(o),
                    "name": o.name,
                    "executesProtocol": {"@id": id_gen(o.executes_protocol)},
                    "parameterValues": list(map(lambda x: get_parameter_value(x), o.parameter_values)),
                    "performer": o.performer,
                    "date": o.date,
                    "previousProcess": {"@id": id_gen(o.prev_process)} if o.prev_process else None,
                    "nextProcess": {"@id": id_gen(o.next_process)} if o.next_process else None,
                    "inputs": list(map(lambda x: {"@id": id_gen(x)}, o.inputs)),
                    "outputs": list(map(lambda x: {"@id": id_gen(x)}, o.outputs)),
                    "comments": get_comments(o.comments)
                }
            )

        def get_parameter_value(o):
            return clean_nulls(
                {
                    "category": {"@id": id_gen(o.category)} if o.category else None,
                    "value": get_value(o.value),
                    "unit": {"@id": id_gen(o.unit)} if o.unit else None
                }
            )

        def get_study(o): return clean_nulls(
            {
                "filename": o.filename,
                "identifier": o.identifier,
                "title": o.title,
                "description": o.description,
                "submissionDate": o.submission_date,
                "publicReleaseDate": o.public_release_date,
                "publications": get_publications(o.publications),
                "people": get_people(o.contacts),
                "studyDesignDescriptors": get_ontology_annotations(o.design_descriptors),
                "protocols": list(map(lambda x: get_protocol(x), o.protocols)),
                "materials": {
                    "sources": list(map(lambda x: get_source(x), o.sources)),
                    "samples": get_samples(o.samples),
                    "otherMaterials": get_other_materials(o.other_material)
                },
                "processSequence": list(map(lambda x: get_process(x), o.process_sequence)),
                "factors": list(map(lambda x: get_factor(x), o.factors)),
                "characteristicCategories": get_characteristic_categories(o.characteristic_categories),
                "unitCategories": get_ontology_annotations(o.units),
                "comments": get_comments(o.comments),
                "assays": list(map(lambda x: get_assay(x), o.assays))
            }
        )

        def get_characteristic_categories(o):
            return list(map(lambda x: get_characteristic_category(x), o))

        def get_samples(o):
            return list(map(lambda x: get_sample(x), o))

        def get_other_materials(o):
            return list(map(lambda x: get_other_material(x), o))

        def get_processes(o):
            return list(map(lambda x: get_process(x), o))

        def get_assay(o):
            return clean_nulls(
                {
                    "measurementType": get_ontology_annotation(o.measurement_type),
                    "technologyType": get_ontology_annotation(o.technology_type),
                    "technologyPlatform": o.technology_platform,
                    "filename": o.filename,
                    "characteristicCategories": get_characteristic_categories(o.characteristic_categories),
                    "unitCategories": get_ontology_annotations(o.units),
                    "comments": get_comments(o.comments) if o.comments else [],
                    "materials": {
                        "samples": get_samples(o.samples),
                        "otherMaterials": get_other_materials(o.other_material)
                    },
                    "dataFiles": list(map(lambda x: get_data_file(x), o.data_files)),
                    "processSequence": get_processes(o.process_sequence)
                }
            )

        def get_data_file(o):
            return clean_nulls(
                {
                    "@id": id_gen(o),
                    "name": o.filename,
                    "type": o.label,
                    "comments": get_comments(o.comments)
                }
            )

        if isinstance(o, Investigation):
            return clean_nulls(
                {
                    "identifier": o.identifier,
                    "title": o.title,
                    "description": o.description,
                    "comments": get_comments(o.comments),
                    "ontologySourceReferences": list(map(lambda x: get_ontology_source(x), o.ontology_source_references)),
                    "people": get_people(o.contacts),
                    "publicReleaseDate": o.public_release_date,
                    "submissionDate": o.submission_date,
                    "publications": get_publications(o.publications),
                    "studies": list(map(lambda x: get_study(x), o.studies))
                }
            )
        elif isinstance(o, Study):
            return get_study(o)
        elif isinstance(o, OntologySource):
            return get_ontology_source(o)
        elif isinstance(o, OntologyAnnotation):
            return get_ontology_annotation(o)
        elif isinstance(o, Person):
            return get_person(o)
        elif isinstance(o, Publication):
            return get_publication(o)
        elif isinstance(o, Protocol):
            return get_protocol(o)
        elif isinstance(o, Characteristic):
            return get_characteristic(o)
        # TODO: enable dump of all objects and add some tests on them