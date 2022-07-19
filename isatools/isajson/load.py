import json
from logging import getLogger

from isatools.model import (
    Investigation, OntologyAnnotation, Comment, OntologySource, Publication, Person, Study, Protocol, ProtocolParameter,
    ProtocolComponent, StudyFactor, Source, Characteristic, Sample, FactorValue, Process, ParameterValue, Assay,
    DataFile, Material
)


log = getLogger('isatools')


def loads(fp):
    """Loads an ISA-JSON file and returns an Investigation object.

    :param fp: A file-like object or a string containing the JSON data.
    :return: An Investigation object.
    """
    investigation_json = json.load(fp)
    investigation = Investigation()
    investigation.from_dict(investigation_json)
    return investigation


def load(fp):
    def get_comments(commentable_dict):
        comments = [
            Comment(
                name=comm_dict.get('name', ''),
                value=comm_dict.get('value', '')
            ) for comm_dict in commentable_dict.get("comments", [])
        ]
        return comments

    def get_roles(j):
        roles = None
        if "roles" in j.keys():
            roles = list()
            for role_json in j["roles"]:
                term = role_json["annotationValue"]
                term_accession = role_json["termAccession"]
                term_source = term_source_dict.get('role_json', {}).get("termSource", '')
                role = OntologyAnnotation(term, term_source, term_accession)
                roles.append(role)
        return roles

    def get_characteristic_category(characteristics_cats_dict):
        res = OntologyAnnotation(
            id_=characteristics_cats_dict["@id"],  # Here we use the id for the CharacteristicType \
            # to back support older JSON serializations # TODO FIX THIS
            term=characteristics_cats_dict["characteristicType"]["annotationValue"],
            term_source=term_source_dict[characteristics_cats_dict["characteristicType"]["termSource"]] \
                if isinstance(characteristics_cats_dict["characteristicType"]["termSource"], OntologySource) \
                else "", term_accession=characteristics_cats_dict["characteristicType"]["termAccession"],
        )
        try:
            res.comments = get_comments(characteristics_cats_dict)
        except KeyError:
            pass
        return res

    def get_parameter_value(p_val_dict):
        res = ParameterValue(
            category=parameters_dict[p_val_dict["category"]["@id"]],
            comments=get_comments(p_val_dict)
        )
        try:
            res.value = OntologyAnnotation(
                term=p_val_dict["value"]["annotationValue"],
                term_accession=p_val_dict["value"]["termAccession"],
                term_source=term_source_dict[p_val_dict["value"]["termSource"]],
                comments=get_comments(p_val_dict["value"])
            )
        except TypeError:
            res.value = p_val_dict["value"]
        return res

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
            description=ontologySourceReference_json["description"],
            comments=get_comments(ontologySourceReference_json)
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
            role.comments = get_comments(role_json)
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
                characteristic_category = get_characteristic_category(assay_characteristics_category_json)
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
            characteristic_category = get_characteristic_category(study_characteristics_category_json)
            categories_dict[characteristic_category.id] = characteristic_category
            study.characteristic_categories.append(characteristic_category)
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
                    term_accession=protocol_json["protocolType"]["termAccession"]
                    if "termAccession" in protocol_json["protocolType"].keys() else "",
                    term_source=term_source_dict[protocol_json["protocolType"]["termSource"]]
                    if "termSource" in protocol_json["protocolType"].keys() else None,
                )
            )
            for parameter_json in protocol_json["parameters"]:
                parameter = ProtocolParameter(
                    id_=parameter_json["@id"],
                    parameter_name=OntologyAnnotation(
                        term=parameter_json["parameterName"]["annotationValue"],
                        term_source=term_source_dict[parameter_json["parameterName"]["termSource"]],
                        term_accession=parameter_json["parameterName"]["termAccession"]
                    ),
                    comments=get_comments(parameter_json)
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
                    ),
                    comments=get_comments(component_json)
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
                ),
                comments=get_comments(factor_json)
            )
            study.factors.append(factor)
            factors_dict[factor.id] = factor
        for source_json in study_json["materials"]["sources"]:
            source = Source(
                id_=source_json["@id"],
                # name=source_json["name"][7:],
                name=source_json["name"].replace("source-", ""),
                comments=get_comments(source_json)
            )
            for characteristic_json in source_json["characteristics"]:
                value = characteristic_json["value"]
                unit = None
                characteristic = Characteristic(
                    category=categories_dict[characteristic_json["category"]["@id"]],
                    comments=get_comments(characteristic_json)
                )

                if isinstance(value, dict):
                    try:
                        term = characteristic_json["value"]["annotationValue"]
                        if isinstance(term, (int, float)):
                            term = str(term)
                        value = OntologyAnnotation(
                            term=term,
                            term_source=term_source_dict[characteristic_json["value"]["termSource"]],
                            term_accession=characteristic_json["value"]["termAccession"],
                            comments=get_comments(characteristic_json["value"])
                        )
                    except KeyError as ke:
                        raise IOError("Can't create value as annotation: " + str(ke)
                                      + " \n object: " + str(characteristic_json))
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
                # name=sample_json["name"][7:],
                name=sample_json["name"].replace("sample-", ""),
                comments=get_comments(sample_json)
            )
            for characteristic_json in sample_json["characteristics"]:
                value = characteristic_json["value"]
                unit = None
                characteristic = Characteristic(
                    category=categories_dict[characteristic_json["category"]["@id"]],
                    comments=get_comments(characteristic_json)
                )
                if isinstance(value, dict):
                    try:
                        value = OntologyAnnotation(
                            term=characteristic_json["value"]["annotationValue"],
                            term_source=term_source_dict[characteristic_json["value"]["termSource"]],
                            term_accession=characteristic_json["value"]["termAccession"],
                            comments=get_comments(characteristic_json["value"])
                        )
                    except KeyError as ke:
                        raise IOError("Can't create value as annotation: " + str(ke)
                                      + "\n object: " + str(characteristic_json))
                elif isinstance(value, int) or isinstance(value, float):
                    try:
                        unit = units_dict[characteristic_json["unit"]["@id"]]
                    except KeyError:
                        unit = None
                        # unit = characteristic_json.get('unit', None)
                elif not isinstance(value, str):
                    raise IOError("Unexpected type in characteristic value")
                characteristic.value = value
                characteristic.unit = unit
                sample.characteristics.append(characteristic)
            for factor_value_json in sample_json["factorValues"]:
                value = factor_value_json["value"]
                unit = None
                factor_value = FactorValue(
                    factor_name=factors_dict[factor_value_json["category"]["@id"]],
                    comments=get_comments(factor_value_json)
                )
                if isinstance(value, dict):
                    try:
                        value = OntologyAnnotation(
                            term=factor_value_json["value"]["annotationValue"],
                            term_accession=factor_value_json["value"]["termAccession"],
                            term_source=term_source_dict[factor_value_json["value"]["termSource"]],
                            comments=get_comments(factor_value_json["value"])
                        )
                    except KeyError as ke:
                        raise IOError("Can't create value as annotation: " + str(ke)
                                      + "\n object: " + str(factor_value_json))
                elif isinstance(value, (int, float)):
                    try:
                        unit = units_dict[factor_value_json["unit"]["@id"]]
                    except KeyError:
                        unit = None
                        # unit = factor_value_json.get("unit", None)
                elif not isinstance(value, str):
                    raise IOError("Unexpected type in factor value")
                factor_value.value = value
                factor_value.unit = unit
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
                        comments=get_comments(parameter_value_json)
                    )
                    process.parameter_values.append(parameter_value)
                else:
                    parameter_value = get_parameter_value(parameter_value_json)
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
                filename=assay_json["filename"],
                comments=get_comments(assay_json)
            )
            for assay_unit_json in assay_json["unitCategories"]:
                unit = OntologyAnnotation(
                    id_=assay_unit_json["@id"],
                    term=assay_unit_json["annotationValue"],
                    term_source=term_source_dict[assay_unit_json["termSource"]],
                    term_accession=assay_unit_json["termAccession"],
                    comments=get_comments(assay_unit_json)
                )
                units_dict[unit.id] = unit
                assay.units.append(unit)

            data_dict = dict()
            for data_json in assay_json["dataFiles"]:
                data_file = DataFile(
                    id_=data_json["@id"],
                    filename=data_json["name"],
                    label=data_json["type"],
                    comments=get_comments(data_json)
                )
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
                characteristic_category = OntologyAnnotation(
                    # id_=assay_characteristics_category_json["characteristicType"]["@id"],
                    term=assay_characteristics_category_json["characteristicType"]["annotationValue"],
                    term_source=term_source_dict[assay_characteristics_category_json["characteristicType"]["termSource"]
                    ],
                    term_accession=assay_characteristics_category_json["characteristicType"]["termAccession"],
                    comments=get_comments(assay_characteristics_category_json["characteristicType"])
                )
                study.characteristic_categories.append(characteristic_category)
                categories_dict[characteristic_category.id] = characteristic_category

            other_materials_dict = dict()
            for other_material_json in assay_json["materials"]["otherMaterials"]:
                material_name = other_material_json["name"].replace("labeledextract-", "").replace("extract-", "")

                material = Material(
                    id_=other_material_json["@id"],
                    name=material_name,
                    type_=other_material_json["type"],
                    comments=get_comments(other_material_json)
                )
                for characteristic_json in other_material_json["characteristics"]:
                    if not isinstance(characteristic_json["value"], str):
                        characteristic = Characteristic(
                            category=categories_dict[
                                characteristic_json["category"]["@id"]
                            ],
                            value=OntologyAnnotation(
                                term=characteristic_json["value"]["annotationValue"],
                                term_source=term_source_dict[characteristic_json["value"]["termSource"]],
                                term_accession=characteristic_json["value"]["termAccession"],
                                comments=get_comments(characteristic_json["value"])
                            ),
                            comments=get_comments(characteristic_json)
                        )
                    else:
                        characteristic = Characteristic(
                            category=categories_dict[
                                characteristic_json["category"]["@id"]
                            ],
                            value=OntologyAnnotation(
                                term=characteristic_json["value"]
                            ),
                            comments=get_comments(characteristic_json)
                        )
                    material.characteristics.append(characteristic)
                assay.other_material.append(material)
                other_materials_dict[material.id] = material

            for assay_process_json in assay_json["processSequence"]:
                process = Process(
                    id_=assay_process_json["@id"],
                    executes_protocol=protocols_dict[assay_process_json["executesProtocol"]["@id"]],
                    comments=get_comments(assay_process_json)
                )
                # additional properties, currently hard-coded special cases
                if process.executes_protocol.protocol_type.term == "data collection" and \
                        assay.technology_type.term == "DNA microarray":
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
                                comments=get_comments(parameter_value_json)
                            )
                            if "unit" in parameter_value_json.keys():
                                parameter_value.unit = units_dict[parameter_value_json["unit"]["@id"]]
                            process.parameter_values.append(parameter_value)
                        else:
                            parameter_value = get_parameter_value(parameter_value_json)
                            process.parameter_values.append(parameter_value)
                    else:
                        log.warning("warning: parameter category not found for instance {}".format(parameter_json))
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
