import re
from json import JSONEncoder

from isatools.model import (
    Investigation, OntologyAnnotation, OntologySource, Publication, Person, Study, Protocol, Characteristic, Material
)


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

        def get_comment(obj):
            return clean_nulls(
                {
                    "name": obj.name,
                    "value": obj.value
                }
            )

        def get_comments(obj):
            return list(map(lambda x: get_comment(x), obj if obj else []))

        def get_ontology_source(obj):
            return clean_nulls(
                {
                    "name": obj.name,
                    "description": obj.description,
                    "file": obj.file,
                    "version": obj.version,
                    "comments": get_comments(obj.comments) if obj.comments else []
                }
            )

        def get_ontology_annotation(obj):
            ontology_annotation = {}

            if obj is not None and isinstance(obj, OntologyAnnotation):
                ontology_annotation["@id"] = "#ontology_annotation/" + obj.id
                if isinstance(obj.term_source, OntologySource):
                    ontology_annotation['termSource'] = obj.term_source.name
                else:
                    ontology_annotation['termSource'] = obj.term_source
                ontology_annotation['annotationValue'] = obj.term
                ontology_annotation['termAccession'] = obj.term_accession
                ontology_annotation["comments"] = get_comments(obj.comments)

            return clean_nulls(ontology_annotation)

        def get_ontology_annotations(obj):
            return list(map(lambda x: get_ontology_annotation(x), obj))

        def get_person(obj):
            return clean_nulls(
                {
                    "address": obj.address,
                    "affiliation": obj.affiliation,
                    "comments": get_comments(obj.comments),
                    "email": obj.email,
                    "fax": obj.fax,
                    "firstName": obj.first_name,
                    "lastName": obj.last_name,
                    "midInitials": obj.mid_initials if obj.mid_initials else '',
                    "phone": obj.phone,
                    "roles": get_ontology_annotations(obj.roles)
                }
            )

        def get_people(obj):
            return list(map(lambda x: get_person(x), obj))

        def get_publication(obj):
            return clean_nulls(
                {
                    "authorList": obj.author_list,
                    "doi": obj.doi,
                    "pubMedID": obj.pubmed_id,
                    "status": get_ontology_annotation(obj.status) if obj.status else {"@id": ''},
                    "title": obj.title,
                    "comments": get_comments(obj.comments) if obj.comments else []
                }
            )

        def get_publications(obj):
            return list(map(lambda x: get_publication(x), obj))

        def get_protocol(obj):
            return clean_nulls(
                {
                    "@id": id_gen(obj),
                    "description": obj.description,
                    "parameters": list(map(lambda x: {
                        "@id": id_gen(x),
                        "parameterName": get_ontology_annotation(x.parameter_name)
                    }, obj.parameters)),  # TODO: Deal with Array Design REF
                    "name": obj.name,
                    "protocolType": get_ontology_annotation(obj.protocol_type),
                    "uri": obj.uri,
                    "comments": get_comments(obj.comments) if obj.comments else [],
                    "components": [],  # TODO: Output components
                    "version": obj.version
                }
            )

        def get_source(obj):
            return clean_nulls(
                {
                    "@id": id_gen(obj),
                    "name": obj.name,
                    "characteristics": get_characteristics(obj.characteristics),
                    "comments": get_comments(obj.comments) if obj.comments else []
                }
            )

        def get_characteristic(obj):
            return clean_nulls(
                {
                    "category": {"@id": id_gen(obj.category)} if obj.category else None,
                    # "category": get_value(o.category) if o.category else None,
                    "value": get_value(obj.value),
                    "unit": {"@id": id_gen(obj.unit)} if obj.unit else None,
                    "comments": get_comments(obj.comments) if obj.comments else []
                }
            )

        def get_characteristics(obj):
            return list(map(lambda x: get_characteristic(x), obj))

        def get_value(obj):
            if isinstance(obj, OntologyAnnotation):
                return get_ontology_annotation(obj)
            elif isinstance(obj, (str, int, float)):
                return obj
            else:
                raise ValueError("Unexpected value type found: " + type(obj))

        def get_characteristic_category(obj):  # TODO: Deal with Material Type
            if isinstance(obj, OntologyAnnotation):
                res = clean_nulls(
                    {
                        "@id": "#characteristic_category/" + str(obj.id),
                        "characteristicType": {
                            "@id": "#ontology_annotation/" + str(obj.id),
                            "annotationValue": obj.term["annotationValue"] if not isinstance(obj.term, str) else "",
                            "termAccession": obj.term["termAccession"] if not isinstance(obj.term, str) else "",
                            "termSource": obj.term["termSource"] if not isinstance(obj.term, str) else ""
                        }
                    }
                )

            elif isinstance(obj, Characteristic):
                res = clean_nulls(
                    {
                        "@id": "#characteristic_category/" + str(obj.category.id),
                        "characteristicType":
                            {
                                "@id": "#ontology_annotation/" + obj.category.id,
                                "annotationValue": obj.category.term,
                                "termAccession": obj.category.term_accession,
                                "termSource": obj.category.term_source
                            }

                    }
                )

            else:
                res = clean_nulls(
                    {
                        "@id": "#characteristic_category/" + obj.id if isinstance(obj, OntologyAnnotation) else None,
                        "characteristicType": obj.category.term if isinstance(obj, OntologyAnnotation) else None
                    }
                )

            return res

        def get_sample(obj):
            return clean_nulls(
                {
                    "@id": id_gen(obj),
                    "name": obj.name,
                    "characteristics": get_characteristics(obj.characteristics),
                    "factorValues": list(map(lambda x: clean_nulls(
                        {
                            "category": {"@id": id_gen(x.factor_name)} if x.factor_name else None,
                            "value": get_value(x.value),
                            "unit": {"@id": id_gen(x.unit)} if x.unit else None
                        }
                    ), obj.factor_values)),
                    "derivesFrom": list(
                        map(lambda x: {"@id": id_gen(x)}, obj.derives_from)) if obj.derives_from else [],
                    "comments": get_comments(obj.comments) if obj.comments else []
                })

        def get_factor(obj):
            return clean_nulls(
                {
                    "@id": id_gen(obj),
                    "factorName": obj.name,
                    "factorType": get_ontology_annotation(obj.factor_type),
                    "comments": get_comments(obj.comments) if obj.comments else []
                }
            )

        def get_other_material(obj):
            return clean_nulls(
                {
                    "@id": id_gen(obj),
                    "name": obj.name,
                    "type": obj.type,
                    "characteristics": get_characteristics(obj.characteristics),
                    "comments": get_comments(obj.comments) if obj.comments else []
                }
            )

        def sqeezstr(s):
            return s.replace(' ', '').lower()

        def id_gen(obj):
            """
            generates a unique node identifier for the given ISA object based on object type and identifier
            """
            if obj:
                o_id = getattr(obj, 'id', None)

                # regex convert CamelCase to snake_case
                name = re.sub(r'(?<!^)(?=[A-Z])', '_', type(obj).__name__).lower()

                if not o_id:
                    o_id = str(id(obj))

                if isinstance(obj, Material):
                    if obj.type == 'Extract Name':
                        return '#material/extract-' + o_id
                    elif obj.type == 'Labeled Extract Name':
                        return '#material/labeledextract-' + o_id
                    else:
                        raise TypeError("Could not resolve data type labeled: " + obj.type)
                else:
                    return "#" + str(name) + "/" + o_id
            else:
                return None

        def get_process(obj):
            return clean_nulls(
                {
                    "@id": id_gen(obj),
                    "name": obj.name,
                    "executesProtocol": {"@id": id_gen(obj.executes_protocol)},
                    "parameterValues": list(map(lambda x: get_parameter_value(x), obj.parameter_values)),
                    "performer": obj.performer,
                    "date": obj.date,
                    "previousProcess": {"@id": id_gen(obj.prev_process)} if obj.prev_process else None,
                    "nextProcess": {"@id": id_gen(obj.next_process)} if obj.next_process else None,
                    "inputs": list(map(lambda x: {"@id": id_gen(x)}, obj.inputs)),
                    "outputs": list(map(lambda x: {"@id": id_gen(x)}, obj.outputs)),
                    "comments": get_comments(obj.comments)
                }
            )

        def get_parameter_value(obj):
            return clean_nulls(
                {
                    "category": {"@id": id_gen(obj.category)} if obj.category else None,
                    "value": get_value(obj.value),
                    "unit": {"@id": id_gen(obj.unit)} if obj.unit else None
                }
            )

        def get_study(obj):
            return clean_nulls(
                {
                    "filename": obj.filename,
                    "identifier": obj.identifier,
                    "title": obj.title,
                    "description": obj.description,
                    "submissionDate": obj.submission_date,
                    "publicReleaseDate": obj.public_release_date,
                    "publications": get_publications(obj.publications),
                    "people": get_people(obj.contacts),
                    "studyDesignDescriptors": get_ontology_annotations(obj.design_descriptors),
                    "protocols": list(map(lambda x: get_protocol(x), obj.protocols)),
                    "materials": {
                        "sources": list(map(lambda x: get_source(x), obj.sources)),
                        "samples": get_samples(obj.samples),
                        "otherMaterials": get_other_materials(obj.other_material)
                    },
                    "processSequence": list(map(lambda x: get_process(x), obj.process_sequence)),
                    "factors": list(map(lambda x: get_factor(x), obj.factors)),
                    "characteristicCategories": get_characteristic_categories(obj.characteristic_categories),
                    "unitCategories": get_ontology_annotations(obj.units),
                    "comments": get_comments(obj.comments),
                    "assays": list(map(lambda x: get_assay(x), obj.assays))
                }
            )

        def get_characteristic_categories(obj):
            return list(map(lambda x: get_characteristic_category(x), obj))

        def get_samples(obj):
            return list(map(lambda x: get_sample(x), obj))

        def get_other_materials(obj):
            return list(map(lambda x: get_other_material(x), obj))

        def get_processes(obj):
            return list(map(lambda x: get_process(x), obj))

        def get_assay(obj):
            return clean_nulls(
                {
                    "measurementType": get_ontology_annotation(obj.measurement_type),
                    "technologyType": get_ontology_annotation(obj.technology_type),
                    "technologyPlatform": obj.technology_platform,
                    "filename": obj.filename,
                    "characteristicCategories": get_characteristic_categories(obj.characteristic_categories),
                    "unitCategories": get_ontology_annotations(obj.units),
                    "comments": get_comments(obj.comments) if obj.comments else [],
                    "materials": {
                        "samples": get_samples(obj.samples),
                        "otherMaterials": get_other_materials(obj.other_material)
                    },
                    "dataFiles": list(map(lambda x: get_data_file(x), obj.data_files)),
                    "processSequence": get_processes(obj.process_sequence)
                }
            )

        def get_data_file(obj):
            return clean_nulls(
                {
                    "@id": id_gen(obj),
                    "name": obj.filename,
                    "type": obj.label,
                    "comments": get_comments(obj.comments)
                }
            )

        if isinstance(o, Investigation):
            return clean_nulls(
                {
                    "identifier": o.identifier,
                    "title": o.title,
                    "description": o.description,
                    "comments": get_comments(o.comments),
                    "ontologySourceReferences": list(
                        map(lambda x: get_ontology_source(x), o.ontology_source_references)),
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
