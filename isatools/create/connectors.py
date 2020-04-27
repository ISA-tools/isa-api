from isatools.model import OntologyAnnotation, OntologySource
from collections import OrderedDict


def _map_ontology_annotations(annotation):
    """
    converts an input annotation into an OntologyAnnotation. If the input is a string it is kept as it is and not
    cast as an OntologyAnnotation
    :param annotation: str/dict
    :return: str/OntologyAnnotation
    """
    if isinstance(annotation, dict):
        res = OntologyAnnotation(
            term=annotation['term']
        )
        if annotation.get('iri', None):
            res.term_accession = annotation['iri']
        source = annotation.get('source', None)
        if source:
            if isinstance(source, str):
                res.term_source = OntologySource(name=source)
            elif isinstance(source, dict):
                res.term_source = OntologySource(**source)
        return res
    else:
        return annotation


def _reverse_map_ontology_annotation(onto_annotation):
    """
    converts an OntologyAnnotation into its serializable form (i.e. a dict with string keys)
    no comments or ids are serialized by this special serializer
    if the input is a string the string itself is retuned
    :param onto_annotation: str or OntologyAnnotation
    :return: dict - to be serialized as JSON
    """
    if isinstance(onto_annotation, OntologyAnnotation):
        res = dict(term=onto_annotation.term, iri=onto_annotation.term_accession or None)
        if onto_annotation.term_source:
            if isinstance(onto_annotation.term_source, str):
                res['source'] = onto_annotation.term_source
            elif isinstance(onto_annotation.term_source, OntologySource):
                res['source'] = dict(
                    name=onto_annotation.term_source.name,
                    file=onto_annotation.term_source.file,
                    version=onto_annotation.term_source.version,
                    description=onto_annotation.term_source.description
                )
        else:
            res['source'] = None
        return res
    else:
        return onto_annotation


def assay_template_convert_json_to_ordered_dict(assay_template_json):
    """
    deserializes a JSON plain dictionary into an OrderedDictionary to be consumed by
        isatools.create.models.AssayGraph.generate_assay_plan_from_dict() to generate a full AssayGraph
    :param assay_template_json: dict
    :return: OrderedDict.
    """
    res = OrderedDict()
    res['measurement_type'] = _map_ontology_annotations(assay_template_json['measurement_type'])
    res['technology_type'] = _map_ontology_annotations(assay_template_json['technology_type'])
    for name, nodes in assay_template_json['workflow']:
        prepared_nodes = None
        if isinstance(nodes, list):
            prepared_nodes = [
                {key: _map_ontology_annotations(value) for key, value in el.items()} for el in nodes
            ]
        if isinstance(nodes, dict):
            prepared_nodes = {}
            for param_name, param_values in nodes.items():
                # if it is a special key (e.g."#replicates") leave it alone
                if param_name[0] == '#' and not isinstance(param_values, list):
                    prepared_nodes[param_name] = param_values
                else:
                    prepared_nodes[param_name] = [
                        _map_ontology_annotations(param_value) for param_value in param_values
                    ]
        res[_map_ontology_annotations(name)] = prepared_nodes
    return res


def assay_template_convert_ordered_dict_to_json(assay_template_odict):
    """
    Serializes an OrderedDict compatible with isatools.create.models.AssayGraph.generate_assay_plan_from_dict() into a
        JSON representation that can be consumed by external applications (e.g. Datascriptor and other client
        applications)
    :param assay_template_odict: OrderedDictionary
    :return: dict, can be directly serialized to JSON
    """
    res = dict()
    res['measurement_type'] = _reverse_map_ontology_annotation(assay_template_odict['measurement_type'])
    res['technology_type'] = _reverse_map_ontology_annotation(assay_template_odict['technology_type'])
    res['workflow'] = []
    for name, nodes in assay_template_odict.items():
        if name in {'measurement_type', 'technology_type'}:
            continue
        if isinstance(nodes, dict):
            serialized_nodes = {}
            for node_prop, prop_values in nodes.items():
                if isinstance(prop_values, list):
                    serialized_nodes[node_prop] = [
                        _reverse_map_ontology_annotation(prop_value) for prop_value in prop_values
                    ]
                else:
                    serialized_nodes[node_prop] = prop_values
        elif isinstance(nodes, list):
            serialized_nodes = [
                {key: _reverse_map_ontology_annotation(val) for key, val in node.items()} for node in nodes
            ]
        else:
            serialized_nodes = {}
        res['workflow'].append([
            _reverse_map_ontology_annotation(name),
            serialized_nodes
        ])
    return res
