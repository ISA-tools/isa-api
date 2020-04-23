from isatools.model import OntologyAnnotation, OntologySource
from isatools.create.models import AssayGraph
from collections import OrderedDict
from numbers import Number


def _map_ontology_annotations(annotation):
    if isinstance(annotation, dict):
        res = OntologyAnnotation(
            term=annotation['term'],
            term_accession=annotation.get('iri', None)
        )
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
    if isinstance(onto_annotation, OntologyAnnotation):
        res = dict(term=onto_annotation.term, iri=onto_annotation.term_accession)
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
        return res
    else:
        return onto_annotation


def assay_template_convert_json_to_ordered_dict(assay_template_json):
    res = OrderedDict()
    res['measurement_type'] = assay_template_json['measurement_type']
    res['technology_type'] = assay_template_json['technology_type']
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
    res = dict()
    res['measurement_type'] = assay_template_odict['measurement_type']
    res['technology_type'] = assay_template_odict['technology_type']
    res['workflow'] = [
        [name, item] for name, item in assay_template_odict.items() if name not in [
            'measurement_type', 'technology_type'
        ]
    ]
    return res
