from isatools.model import OntologyAnnotation, OntologySource, FactorValue
from isatools.create.models import StudyDesign, NonTreatment, Treatment, StudyCell, StudyArm, SampleAndAssayPlan, \
    SAMPLE, ORGANISM_PART
from isatools.create.models import SCREEN, RUN_IN, FOLLOW_UP, WASHOUT, BASE_FACTORS, INTERVENTIONS
from collections import OrderedDict

AGENT = 'agent'

EVENT_TYPE_SAMPLING = 'sampling'
EVENT_TYPE_ASSAY = 'assay'


def _map_ontology_annotations(annotation, expand_strings=False):
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
        return OntologyAnnotation(term=annotation) if expand_strings else annotation


def _reverse_map_ontology_annotation(onto_annotation, compress_strings=False):
    """
    converts an OntologyAnnotation into its serializable form (i.e. a dict with string keys)
    no comments or ids are serialized by this special serializer
    if the input is a string the string itself is returned.
    :param onto_annotation: str or OntologyAnnotation
    :param compress_strings Bool - if true compress to strings onto_annotation objects missing a term_accession
    :return: dict or string - to be serialized as JSON
    """
    if isinstance(onto_annotation, OntologyAnnotation):
        if not onto_annotation.term_accession and compress_strings:
            return onto_annotation.term
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


def assay_template_to_ordered_dict(assay_template):
    """
    deserializes a JSON plain dictionary into an OrderedDictionary to be consumed by
        isatools.create.models.AssayGraph.generate_assay_plan_from_dict() to generate a full AssayGraph
    :param assay_template: dict
    :return: OrderedDict.
    """
    res = OrderedDict()
    res['measurement_type'] = _map_ontology_annotations(assay_template['measurement_type'])
    res['technology_type'] = _map_ontology_annotations(assay_template['technology_type'])
    for name, nodes in assay_template['workflow']:
        prepared_nodes = None
        if isinstance(nodes, list):
            # "nodes" represent a list of ProductNodes
            prepared_nodes = [
                {key: _map_ontology_annotations(value) for key, value in el.items()} for el in nodes
            ]
        if isinstance(nodes, dict):
            # "nodes" represent a ProtocolNode
            prepared_nodes = {}
            for candidate_param_name, param_values in nodes.items():
                # if it is a special key (e.g."#replicates") leave it alone
                if candidate_param_name[0] == '#' and not isinstance(param_values, list):
                    prepared_nodes[candidate_param_name] = param_values
                else:
                    # this is really a parameter name
                    param_name = _map_ontology_annotations(candidate_param_name, expand_strings=True)
                    prepared_nodes[param_name] = [
                        _map_ontology_annotations(param_value) for param_value in param_values
                    ]
        res[_map_ontology_annotations(name)] = prepared_nodes
    return res


def assay_ordered_dict_to_template(assay_ord_dict):
    """
    Serializes an OrderedDict compatible with isatools.create.models.AssayGraph.generate_assay_plan_from_dict() into a
        JSON representation that can be consumed by external applications (e.g. Datascriptor and other client
        applications)
    :param assay_ord_dict: OrderedDictionary
    :return: dict, can be directly serialized to JSON
    """
    res = dict()
    res['measurement_type'] = _reverse_map_ontology_annotation(assay_ord_dict['measurement_type'])
    res['technology_type'] = _reverse_map_ontology_annotation(assay_ord_dict['technology_type'])
    res['workflow'] = []
    for name, nodes in assay_ord_dict.items():
        if name in {'measurement_type', 'technology_type'}:
            continue
        if isinstance(nodes, dict):
            # "nodes" represent a ProtocolNode
            serialized_nodes = {}
            for node_prop, prop_values in nodes.items():
                if isinstance(prop_values, list):
                    serialized_nodes[_reverse_map_ontology_annotation(node_prop, compress_strings=True)] = [
                        _reverse_map_ontology_annotation(prop_value) for prop_value in prop_values
                    ]
                else:
                    serialized_nodes[node_prop] = prop_values
        elif isinstance(nodes, list):
            # "nodes" represent a list of ProductNodes
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


def _generate_element(datascriptor_element_dict):
    """
    Generates elements (Treatement and NonTreatment) from their description as Datascriptor dicts
    :param datascriptor_element_dict: dict
    :return: isatools.create.models.Element
    """
    if 'agent' in datascriptor_element_dict:
        agent = FactorValue(
            factor_name=BASE_FACTORS[0],
            value=_map_ontology_annotations(datascriptor_element_dict['agent']),
            unit=_map_ontology_annotations(datascriptor_element_dict.get('agentUnit', None))
        )
        intensity = FactorValue(
            factor_name=BASE_FACTORS[1],
            value=_map_ontology_annotations(datascriptor_element_dict.get('intensity', None)),
            unit=_map_ontology_annotations(datascriptor_element_dict.get('intensityUnit', None))
        )
        duration = FactorValue(
            factor_name=BASE_FACTORS[2],
            value=datascriptor_element_dict.get('duration', 0),
            unit=_map_ontology_annotations(datascriptor_element_dict.get('durationUnit', 's'))
        )
        treatment_type = datascriptor_element_dict.get('type', '')
        element = Treatment(
            element_type=treatment_type if treatment_type in INTERVENTIONS.values() else None,
            factor_values=[agent, intensity, duration]
        )
    else:
        element = NonTreatment(
            element_type=datascriptor_element_dict.get('type', SCREEN),
            duration_value=datascriptor_element_dict['duration'],
            duration_unit=_map_ontology_annotations(datascriptor_element_dict['durationUnit'])
        )
    return element


def _generate_sample_dict_from_config(sample_type_config):
    return dict(
        node_type=SAMPLE,
        characteristics_category=_map_ontology_annotations(
            sample_type_config.get('outputCategory', ORGANISM_PART)
        ),
        characteristics_value=_map_ontology_annotations(sample_type_config['output']),
        size=sample_type_config.get('outputSize', 1),
        is_input_to_next_protocols=sample_type_config.get('isAssayInput', True)
    )


def generate_isa_study_design_from_datascriptor_config(datascriptor_design_config):
    """
    Generates the StudyDesign object out of the Datascriptor representation of it.
    :param datascriptor_design_config: dict - a dictionary describing a study design as produced by Datascriptor ()
    :return: isatools.models.create.StudyDesign
    """
    # create each StudyCell and each SampleAndAssayPlan while iterating over the studyArms
    arms = []
    for arm_dict in datascriptor_design_config['arms']:
        arm_map = OrderedDict()
        for epoch_ix, epoch_dict in enumerate(arm_dict['epochs']):
            element_ids = epoch_dict.get('elements', [])
            elements = [
                _generate_element(element_dict) for element_dict in
                filter(lambda el: el['id'] in element_ids, datascriptor_design_config['elements'])
            ]
            cell_name = 'CELL_{}_{}'.format(arm_dict['name'], epoch_ix)
            cell = StudyCell(name=cell_name, elements=elements)
            sample_type_dicts = [
                _generate_sample_dict_from_config(st_config) for st_config in filter(
                    lambda ev: ev['id'] in epoch_dict.get('events', []) and ev['action'] == EVENT_TYPE_SAMPLING,
                    datascriptor_design_config['events']
                )
            ]
            assay_ord_dicts = [
                assay_template_to_ordered_dict(at_dict['template']) for at_dict in filter(
                    lambda ev: ev['id'] in epoch_dict.get('events', []) and ev['action'] == EVENT_TYPE_ASSAY,
                    datascriptor_design_config['events']
                )
            ]
            sa_plan_name = 'SA_PLAN_{}_{}'.format(arm_dict['name'], epoch_ix)
            sa_plan = SampleAndAssayPlan.from_sample_and_assay_plan_dict(
                sa_plan_name, sample_type_dicts, *assay_ord_dicts
            )
            arm_map[cell] = sa_plan
        arm = StudyArm(
            name=arm_dict['name'],
            source_type=_map_ontology_annotations(arm_dict['subjectType']),
            group_size=arm_dict.get('size', 0),
            arm_map=arm_map
        )
        arms.append(arm)
    return StudyDesign(name=datascriptor_design_config['type'], study_arms=arms)

