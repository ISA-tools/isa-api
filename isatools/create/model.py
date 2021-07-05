"""
Model objects for storing study design settings, for consumption by
function or factory to create ISA model objects.
"""
from __future__ import absolute_import
import datetime
import itertools
import json
import re
from collections import OrderedDict, Iterable
from copy import deepcopy
import copy
import logging
from numbers import Number
from abc import ABC
from math import factorial
import os
import yaml
import uuid
import networkx as nx
from isatools.create import errors
from isatools.create.constants import (
    SCREEN, RUN_IN, WASHOUT, FOLLOW_UP, ELEMENT_TYPES, INTERVENTIONS, OBSERVATION_PERIOD,
    DURATION_FACTOR, BASE_FACTORS, SOURCE, SAMPLE, EXTRACT, LABELED_EXTRACT,
    DATA_FILE, GROUP_PREFIX, SUBJECT_PREFIX, SAMPLE_PREFIX,
    ASSAY_GRAPH_PREFIX,
    RUN_ORDER, STUDY_CELL, assays_opts,
    DEFAULT_SOURCE_TYPE, SOURCE_QC_SOURCE_NAME, QC_SAMPLE_NAME,
    QC_SAMPLE_TYPE_PRE_RUN, QC_SAMPLE_TYPE_POST_RUN,
    QC_SAMPLE_TYPE_INTERSPERSED, ZFILL_WIDTH, DEFAULT_PERFORMER,
    DEFAULT_STUDY_IDENTIFIER, IS_TREATMENT_EPOCH, SEQUENCE_ORDER_FACTOR
)
from isatools.model import (
    StudyFactor,
    FactorValue,
    OntologyAnnotation,
    OntologySource,
    Characteristic,
    Study,
    Sample,
    Comment,
    Assay,
    Protocol,
    Process,
    ProtocolParameter,
    ParameterValue,
    Source,
    Material,
    DataFile,
    RawDataFile,
    RawSpectralDataFile,
    FreeInductionDecayDataFile,
    ArrayDataFile,
    DerivedDataFile,
    DerivedSpectralDataFile,
    DerivedArrayDataFile,
    ProteinAssignmentFile,
    PeptideAssignmentFile,
    DerivedArrayDataMatrixFile,
    PostTranslationalModificationAssignmentFile,
    AcquisitionParameterDataFile,
    Extract,
    LabeledExtract,
    plink
)
from isatools.utils import urlify, n_digits

log = logging.getLogger('isatools')
log.setLevel(logging.INFO)

__author__ = 'massi'


def intersperse(lst, item):
    """
    Utility method to intersperse an item in a list
    :param lst: 
    :param item: the item to be interspersed
    :return: 
    """
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result


class Element(ABC):
    """
    Element is the building block of a study design
    The Element class is abstract and has two implementations:
        - NonTreatment
        - Treatment
    """

    def __init__(self):
        self.__type = None

    def __repr__(self):
        return 'Element(type={0})'.format(self.type)

    def __str__(self):
        return repr(self)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Element) and self.type == other.type

    def __ne__(self, other):
        return not self == other

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, element_type):
        self.__type = element_type

    @property
    def factor_values(self):
        return set()

    @property
    def duration(self):
        return 0

    def update_duration(self, duration_value, duration_unit=None):
        pass


class NonTreatment(Element):
    """
        A NonTreatment is defined only by 1 factor values specifying its duration
        and a type. Allowed types are SCREEN, RUN-IN, WASHOUT and FOLLOW-UP.
        A NonTreatment is an extension of the basic Element
    """
    def __init__(self, element_type=ELEMENT_TYPES['SCREEN'], duration_value=0.0, duration_unit=None):
        super(NonTreatment, self).__init__()
        if element_type not in ELEMENT_TYPES.values():
            raise ValueError('element treatment type provided: {}'.format(element_type))
        self.__type = element_type
        if not isinstance(duration_value, Number):
            raise ValueError('duration_value must be a Number. Value provided is {0}'.format(duration_value))
        self.__duration = FactorValue(factor_name=DURATION_FACTOR, value=duration_value, unit=duration_unit)

    def __repr__(self):
        return '{0}.{1}(type={2}, duration={3})'.format(
            self.__class__.__module__, self.__class__.__name__, repr(self.type), repr(self.duration)
        )

    def __str__(self):
        return """{0}(
            type={1},
            duration={2}
        )""".format(self.__class__.__name__, repr(self.type), repr(self.duration))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, NonTreatment) and self.type == other.type and self.duration == other.duration

    def __ne__(self, other):
        return not self == other

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, element_type):
        if element_type in ELEMENT_TYPES.values():
            self.__type = element_type
        else:
            raise ValueError('invalid treatment type provided: ')

    @property
    def factor_values(self):
        return {self.__duration}

    @property
    def duration(self):
        return self.__duration

    def update_duration(self, duration_value, duration_unit=None):
        if not isinstance(duration_value, Number):
            raise ValueError('duration_value must be a Number. Value provided is {0}'.format(duration_value))
        self.__duration.value = duration_value
        self.__duration.unit = duration_unit


class Treatment(Element):
    """
    A Treatment is defined as a set of factor values (as defined in the ISA
    model v1) and a treatment type
    A Treatment is an extension of the basic Element
    """
    def __init__(self, element_type=INTERVENTIONS['CHEMICAL'],
                 factor_values=None):
        """
        Creates a new Treatment
        :param element_type: treatment type
        :param factor_values: set of isatools.model.v1.FactorValue
        """
        super(Treatment, self).__init__()
        if not isinstance(element_type, (str, OntologyAnnotation)):
            raise ValueError('intervention_type must be string or OntologyAnnotation. {} was provided.'.format(
                element_type
            ))
        self.__type = element_type

        if factor_values is None:
            self.__factor_values = set()
        else:
            self.factor_values = factor_values

    def __repr__(self):
        return '{0}.{1}(type={2}, factor_values={3})'.format(
            self.__class__.__module__, self.__class__.__name__,
            self.type, sorted(self.factor_values, key=lambda x: repr(x)))

    def __str__(self):
        return """"{0}
        (type={1}, 
        factor_values={2})
        """.format(
            self.__class__.__name__,
            self.type, sorted(self.factor_values, key=lambda x: repr(x)))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Treatment) \
               and self.type == other.type \
               and self.factor_values == other.factor_values

    def __ne__(self, other):
        return not self == other

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, treatment_type):
        if treatment_type in INTERVENTIONS.values():
            self.__type = treatment_type
        else:
            raise ValueError('invalid treatment type provided: ')

    @property
    def factor_values(self):
        return self.__factor_values

    @factor_values.setter
    def factor_values(self, factor_values=()):
        if isinstance(factor_values, (tuple, list, set)) \
                and all([isinstance(factor_value, FactorValue)
                         for factor_value in factor_values]):
            self.__factor_values = set(factor_values)
        else:
            raise AttributeError('Data supplied is not correctly formatted for Treatment')

    @property
    def duration(self):
        return next(factor_value for factor_value in self.factor_values
                    if factor_value.factor_name == DURATION_FACTOR)

    def update_duration(self, duration_value, duration_unit=None):
        pass  # TODO


class StudyCell(object):
    """
    A StudyCell consists of a set of Elements who can be Treatment or NonTreatment Elements
    Under the current design all elements in a a cell are intended to be concomitant
    PROBLEM: what if different concomitant treatments within a cell have different durations?
    ANSWER: this must not be allowed
    PROBLEM: only allow concomitant treatments: concomitant non-treatments make no sense
    """

    def __init__(self, name, elements=None):
        self.__name = name if isinstance(name, str) else None   # FIXME can we allow name to be none?
        self.__elements = list()
        if elements is not None:
            self.elements = elements

    def __repr__(self):
        return '{0}.{1}(' \
               'name={name}, ' \
               'elements={elements}, ' \
               ')'.format(self.__class__.__module__, self.__class__.__name__, name=self.name, elements=[
                sorted(el, key=lambda e: hash(e)) if isinstance(el, set) else el for el in self.elements
        ])

    def __str__(self):
        return """{0}(
               name={name}, 
               elements={elements_count} items, 
               )""".format(self.__class__.__name__, name=self.name,
                           elements_count=len(self.elements))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, StudyCell) and self.name == other.name and self.elements == other.elements

    def __ne__(self, other):
        return not self == other

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise AttributeError('StudyCell name must be a string')
        self.__name = name

    @property
    def elements(self):
        return self.__elements

    @elements.setter
    def elements(self, x):
        if not isinstance(x, (Element, list, tuple)):
            raise AttributeError('elements must be an Element, a list of Elements, or a tuple of Elements')
        self.__elements.clear()
        try:
            if isinstance(x, Element):
                self.insert_element(x)
            else:
                for element in x:
                    self.insert_element(element)
        except ValueError as e:
            raise AttributeError(e)

    @staticmethod
    def _non_treatment_check(previous_elements, new_element, insertion_index=None):
        """
        Private method, to be called within insert_element()
        :param previous_elements: the list of previous elements
        :param new_element: the element to insert in the list of previous elements
        :param insertion_index: the position in the list where the new element will be inserted
        :return: bool 
        """
        if insertion_index is None:
            insertion_index = len(previous_elements)

        def check_observation_period():
            return True

        def check_screen():
            if len(previous_elements) > 1:
                return False
            if len(previous_elements) == 1:
                if previous_elements[0].type == RUN_IN and insertion_index == 0:
                    return True
                else:
                    return False
            return True

        def check_run_in():
            if len(previous_elements) > 1:
                return False
            if len(previous_elements) == 1:
                if previous_elements[0].type == SCREEN and abs(insertion_index) == 1:
                    return True
                else:
                    return False
            return True

        def check_washout():
            next_element = previous_elements[insertion_index] if insertion_index < len(previous_elements) else None
            previous_element = previous_elements[insertion_index - 1] if insertion_index > 0 else None
            if isinstance(next_element, NonTreatment) or isinstance(previous_element, NonTreatment):
                return False
            return True

        def check_follow_up():
            return not bool(len(previous_elements))

        switcher = {
            OBSERVATION_PERIOD: check_observation_period,
            SCREEN: check_screen,
            RUN_IN: check_run_in,
            WASHOUT: check_washout,
            FOLLOW_UP: check_follow_up
        }
        func = switcher.get(new_element.type, lambda: False)
        # lines = inspect.getsource(func)
        return func()

    @staticmethod
    def _treatment_check(previous_elements):
        """
        :param previous_elements: the list of previous elements 
        :return: bool
        """
        not_allowed_elements = filter(lambda el: getattr(el, 'type', None) in [SCREEN, RUN_IN, FOLLOW_UP],
                                      previous_elements)
        return not bool(len(list(not_allowed_elements)))

    def _concomitant_treatments_check(self, element_set):
        """
        This method checks that the duration value and unit are the same for all treatments within
        the provided element_set
        :param element_set: set
        :return: bool
        """
        if not self._treatment_check(self.elements):
            return False
        if any(not isinstance(el, Treatment) for el in element_set):
            return False
        duration_set = {el.duration for el in element_set}
        return True if len(duration_set) == 1 else False

    def insert_element(self, element, element_index=None):
        """
        Add an Element object to a StudyCell
        :param element: an Element or a set of Treatments (to represent concomitant treatments)
        :param element_index (int)
        Rules to insert an element or a set of elements:
        - Screen NonTreatments must either be in a 1-element StudyCell or in a 2-element if followed by a Run-in
        - Run-in NonTreatments must either be in a 1-element StudyCell or in a 2-element if preceded by a Screen
        - A Follow-up NonTreatment must be in a 1-element StudyCell
        - WAshout NonTreatments cannot be chained one after the other
        - Concomitant Treatments (if provided in a set) must have the same duration 
        :return: 
        """
        index = len(self.elements) if not isinstance(element_index, int) else \
            element_index if abs(element_index) < len(self.elements) else len(self.elements)
        if not isinstance(element, (Element, set)):
            raise ValueError('element must be either an Element or a set of treatments')
        is_valid = self._non_treatment_check(self.elements, element, index) if isinstance(element, NonTreatment) else \
            self._treatment_check(self.elements) if isinstance(element, Treatment) else \
            self._concomitant_treatments_check(element) if isinstance(element, set) else False
        if is_valid:
            self.__elements.insert(index, element)
        else:
            raise ValueError('Element is not valid')

    def contains_non_treatment_element_by_type(self, non_treatment_type):
        """
        Evaluates whether the current cell contains a NonTreatment of a specific type
        :param non_treatment_type: str - specifies whether it is a SCREEN, RUN-IN, WASHOUT, or FOLLOW-UP
        :return: bool 
        """
        return any(el for el in self.elements if isinstance(el, NonTreatment) and el.type == non_treatment_type)

    def get_all_elements(self):
        all_elements = []
        for el in self.elements:
            if isinstance(el, Element):
                all_elements.append(el)
            elif isinstance(el, set):
                for concomitant_el in el:
                    all_elements.append(concomitant_el)
        return all_elements

    @property
    def has_treatments(self):
        return any(isinstance(el, Treatment) for el in self.get_all_elements())

    @property
    def duration(self):
        # TODO recompute as sum of durations
        return None


class OntologyAnnotationEncoder(json.JSONEncoder):

    @staticmethod
    def ontology_source(obj):
        if isinstance(obj, str):
            return obj
        if isinstance(obj, OntologySource):
            res = {
                "name": obj.name
            }
            if obj.file:
                res["file"] = obj.file
            if obj.version:
                res["version"] = obj.version
            if obj.description:
                res["description"] = obj.description
            return res

    def ontology_annotation(self, obj):
        if isinstance(obj, str):
            return obj
        if isinstance(obj, OntologyAnnotation):
            res = {
                "term": obj.term
            }
            if obj.term_accession:
                res["termAccession"] = obj.term_accession
            if obj.term_source:
                res["termSource"] = self.ontology_source(obj.term_source)
            return res

    def default(self, obj):
        return self.ontology_annotation(obj)


class CharacteristicEncoder(json.JSONEncoder):

    @staticmethod
    def characteristic(obj):
        onto_encoder = OntologyAnnotationEncoder()
        if isinstance(obj, Characteristic):
            res = dict(
                category=onto_encoder.ontology_annotation(obj.category)
                if isinstance(obj.category, OntologyAnnotation) else obj.category,
                value=onto_encoder.ontology_annotation(obj.value)
                if isinstance(obj.value, OntologyAnnotation) else obj.value,
            )
            if obj.unit:
                res['unit'] = onto_encoder.ontology_annotation(obj.unit) \
                    if isinstance(obj.unit, OntologyAnnotation) else obj.unit
            return res

    def default(self, obj):
        return self.characteristic(obj)


class CharacteristicDecoder(object):

    @staticmethod
    def loads_ontology_annotation(ontology_annotation_dict):
        term_source = None
        if isinstance(ontology_annotation_dict.get("termSource", None), dict):
            term_source = OntologySource(**ontology_annotation_dict["termSource"])
        return OntologyAnnotation(
            term=ontology_annotation_dict["term"], term_accession=ontology_annotation_dict.get("termAccession", ''),
            term_source=term_source
        )

    def loads_characteristic(self, characteristic_dict):
        characteristic = Characteristic(
            category=self.loads_ontology_annotation(characteristic_dict["category"]) if isinstance(
                characteristic_dict["category"], dict
            ) else characteristic_dict['category'],
            value=self.loads_ontology_annotation(characteristic_dict["value"]) if isinstance(
                characteristic_dict["value"], dict
            ) else characteristic_dict['value']
        )
        if 'unit' in characteristic_dict:
            characteristic.unit = self.loads_ontology_annotation(characteristic_dict["unit"]) if isinstance(
                characteristic_dict["unit"], dict
            ) else characteristic_dict["unit"] if isinstance(
                characteristic_dict["unit"], str
            ) else None
        return characteristic

    def loads(self, json_text):
        return self.loads_characteristic(json.loads(json_text))


class StudyCellEncoder(json.JSONEncoder):

    @staticmethod
    def study_factor(obj):
        if isinstance(obj, StudyFactor):
            onto_encoder = OntologyAnnotationEncoder()
            return {
                "name": onto_encoder.ontology_annotation(obj.name),
                "type": onto_encoder.ontology_annotation(obj.factor_type)
            }

    def factor_value(self, obj):
        if isinstance(obj, FactorValue):
            onto_encoder = OntologyAnnotationEncoder()
            res = {
                "factor": self.study_factor(obj.factor_name),
                "value": obj.value if isinstance(obj.value, Number) else onto_encoder.ontology_annotation(obj.value)
            }
            if obj.unit:
                res["unit"] = onto_encoder.ontology_annotation(obj.unit)
            return res

    def element(self, obj):
        if isinstance(obj, Treatment):
            return {
                "isTreatment": True,
                "type": obj.type,
                "factorValues": [self.factor_value(fv) for fv in obj.factor_values]
            }
        if isinstance(obj, NonTreatment):
            return {
                "isTreatment": False,
                "type": obj.type,
                "factorValues": [self.factor_value(fv) for fv in obj.factor_values]
            }
        if isinstance(obj, set):
            return [self.element(el) for el in obj]

    def default(self, obj):
        if isinstance(obj, StudyCell):
            return {
                "name": obj.name,
                "elements": [self.element(el) for el in obj.elements]
            }


class StudyCellDecoder(object):

    def __init__(self):
        pass

    @staticmethod
    def loads_factor_value(factor_value_dict):
        unit = OntologyAnnotation(term=factor_value_dict["unit"]["term"]) if "unit" in factor_value_dict else None
        study_factor_type = OntologyAnnotation(term=factor_value_dict["factor"]["type"]["term"])
        study_factor = StudyFactor(name=factor_value_dict["factor"]["name"], factor_type=study_factor_type)
        return FactorValue(factor_name=study_factor, value=factor_value_dict["value"], unit=unit)

    def loads_element(self, element_struct):
        log.debug(element_struct)
        if isinstance(element_struct, list):
            # if element_stuct is a list it means that all the element in the list are concomitant
            return {self.loads_element(el_dict) for el_dict in element_struct}
        try:
            if element_struct["isTreatment"] is True:
                factor_values = [self.loads_factor_value(factor_value_dict)
                                 for factor_value_dict in element_struct["factorValues"]]
                return Treatment(element_type=element_struct["type"], factor_values=factor_values)
            else:
                duration_unit = OntologyAnnotation(**element_struct["factorValues"][0]["unit"]) \
                    if type(element_struct["factorValues"][0]["unit"]) == dict \
                    else element_struct["factorValues"][0]["unit"]
                return NonTreatment(element_type=element_struct["type"],
                                    duration_value=element_struct["factorValues"][0]["value"],
                                    duration_unit=duration_unit)
        except KeyError as ke:
            # missing 'isTreatment' property
            if len(element_struct["factorValues"]) == 1:
                pass     # non-treatment
            elif len(element_struct["factorValues"]) == 3:
                pass    # treatment
            else:
                pass    # raise error
            log.debug('Element has no \'isTreatment\' property: {}'.format(element_struct))
            raise ke

    def loads_cells(self, json_dict):
        cell = StudyCell(name=json_dict["name"])
        for element in json_dict["elements"]:
            try:
                cell.insert_element(self.loads_element(element))
            except ValueError as e:
                log.error('Element triggers error: {0}'.format(element))
                raise e
        return cell

    def loads(self, json_text):
        json_dict = json.loads(json_text)
        return self.loads_cells(json_dict)


class SequenceNode(ABC):

    pass


class ProtocolNode(SequenceNode, Protocol):

    """
    These class is a subclass of isatools.model.Protocol
    It represents a node in the AssayGraph which is a to create a Protocol
    """

    def __init__(self, id_=str(uuid.uuid4()), name='', protocol_type=None, uri='',
                 description='', version='', parameter_values=None, replicates=None):
        """

        :param id_:
        :param name: the name of the protocol
        :param protocol_type: the type of the protocol
        :param uri: a uri pointing to a resource describing the protocol
        :param description: a  textual description of the protocol
        :param version:
        :param parameter_values: the values to be supplied to the Protocol Parameters
        :param replicates: int - the number of replicates (biological or technical) for this Protocol step. Must be a
                                 positive integer (>= 1)
        """
        Protocol.__init__(self, id_=id_, name=name, protocol_type=protocol_type,
                          uri=uri, description=description, version=version)
        SequenceNode.__init__(self)
        self.__parameter_values = []
        self.__replicates = 1
        if parameter_values is not None:
            self.parameter_values = parameter_values
        if replicates:
            self.replicates = replicates

    @property
    def parameter_values(self):
        return self.__parameter_values

    @parameter_values.setter
    def parameter_values(self, parameter_values):
        if not isinstance(parameter_values, Iterable) or \
                not all(isinstance(parameter_value, ParameterValue) for parameter_value in parameter_values):
            raise AttributeError(errors.PARAMETER_VALUES_ERROR.format(parameter_values))
        self.__parameter_values = list(parameter_values)

    def add_parameter_value(self, protocol_parameter, value, unit=None):
        if isinstance(protocol_parameter, str):
            protocol_parameter = ProtocolParameter(parameter_name=protocol_parameter)
        parameter_value = ParameterValue(category=protocol_parameter, value=value, unit=unit)
        self.__parameter_values.append(parameter_value)

    @property
    def replicates(self):
        return self.__replicates or 1

    @replicates.setter
    def replicates(self, replicates):
        if not isinstance(replicates, int) or replicates < 1:
            raise AttributeError(errors.REPLICATES_ERROR.format(replicates))
        self.__replicates = replicates

    @property
    def parameters(self):
        return [parameter_value.category for parameter_value in self.parameter_values]

    @parameters.setter
    def parameters(self, parameters):
        raise AttributeError(errors.PARAMETERS_CANNOT_BE_SET_ERROR)

    @property
    def components(self):
        return []   # FIXME check if empty list works None triggers an error

    @components.setter
    def components(self, components):
        raise AttributeError(errors.COMPONENTS_CANNOT_BE_SET_ERROR)

    def __repr__(self):
        return '{0}.{1}(id={2.id}, name={2.name}, protocol_type={2.protocol_type}, ' \
               'uri={2.uri}, description={2.description}, version={2.version}, ' \
               'parameter_values={2.parameter_values})'.format(self.__class__.__module__,
                                                               self.__class__.__name__, self)

    def __str__(self):
        return """{0}(
        id={1.id}, 
        name={1.name}, 
        protocol_type={1.protocol_type}, 
        uri={1.uri}, 
        description={1.description}, 
        version={1.version}, 
        parameter_values={1.parameter_values})
        """.format(self.__class__.__name__, self)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, ProtocolNode) and self.id == other.id and self.name == other.name \
               and self.protocol_type == other.protocol_type and self.uri == other.uri \
               and self.description == other.description and self.version == other.version \
               and self.parameter_values == other.parameter_values

    def __ne__(self, other):
        return not self == other


class ProductNode(SequenceNode):

    """
    A ProductNode caputres information about the inputs or outputs of a process.
    It can contain info about a source, a sample (or its derivatives), or a data file
    """
    ALLOWED_TYPES = {SOURCE, SAMPLE, EXTRACT, LABELED_EXTRACT, DATA_FILE}

    def __init__(self, id_=str(uuid.uuid4()), node_type=SOURCE, name='', characteristics=[], size=0, extension=None):
        """
        ProductNode constructor method
        :param id_: an identifier for the ProductNode
        :param node_type: str - the type of ProductNode. Must be one of the allowed types.
        :param name: str - the name of the ProductNone
        :param characteristics: list<Characteristics> - characteristics of the node
        :param size: int
        :param extension: str/OntologyAnnotation - an extension to be appended to the elements generated from this
                          ProductNode. It can be used to specify file extensions to a DATA_FILE node
        """
        super().__init__()
        self.__id = id_
        self.__type = None
        self.__name = None
        self.__characteristics = []
        self.__size = None
        self.__extension = None
        self.type = node_type
        self.name = name
        self.characteristics = characteristics
        self.size = size
        if extension:
            self.extension = extension

    def __repr__(self):
        return '{0}.{1}(id={2.id}, type={2.type}, name={2.name}, ' \
               'characteristics={2.characteristics}, size={2.size}, ' \
               'extension={2.extension})'.format(
                self.__class__.__module__, self.__class__.__name__, self)

    def __str__(self):
        return """{0}(
        id={1.id},
        type={1.type},
        name={1.name},
        )""".format(self.__class__.__name__, self)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, ProductNode) and self.id == other.id and self.type == other.type \
               and self.name == other.name and self.characteristics == other.characteristics \
               and self.size == other.size and self.extension == other.extension

    def __ne__(self, other):
        return not self == other

    @property
    def id(self):
        return self.__id

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, node_type):
        if node_type not in self.ALLOWED_TYPES:
            raise AttributeError(errors.NOT_ALLOWED_TYPE_ERROR.format(self.ALLOWED_TYPES))
        self.__type = node_type

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise AttributeError(errors.PRODUCT_NODE_NAME_ERROR.format(name, type(name)))
        self.__name = name

    @property
    def characteristics(self):
        return self.__characteristics

    @characteristics.setter
    def characteristics(self, characteristics):
        self.__characteristics = []
        try:
            for characteristic in characteristics:
                self.add_characteristic(characteristic)
        except TypeError as e:
            raise AttributeError(e)

    def add_characteristic(self, characteristic):
        if not isinstance(characteristic, (str, Characteristic)):
            raise TypeError(errors.CHARACTERISTIC_TYPE_ERROR.format(type(characteristic)))
        if isinstance(characteristic, Characteristic):
            self.__characteristics.append(characteristic)
        if isinstance(characteristic, str):
            self.__characteristics.append(Characteristic(value=characteristic))

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        if not isinstance(size, int) or size < 0:
            raise AttributeError(errors.SIZE_ERROR)
        self.__size = size

    @property
    def extension(self):
        return self.__extension

    @extension.setter
    def extension(self, extension):
        if not isinstance(extension, (str, OntologyAnnotation)):
            raise AttributeError(errors.PRODUCT_NODE_EXTENSION_ERROR)
        self.__extension = extension


class QualityControlSource(Source):
    pass


class QualityControlSample(Sample):

    ALLOWED_QC_SAMPLE_TYPES = [QC_SAMPLE_TYPE_PRE_RUN, QC_SAMPLE_TYPE_INTERSPERSED, QC_SAMPLE_TYPE_POST_RUN]

    def __init__(self, **kwargs):
        log.debug('KWARGS are: {0}'.format(kwargs))
        qc_sample_type = kwargs.get('qc_sample_type', None)
        _kwargs = {key: val for key, val in kwargs.items() if key != 'qc_sample_type'}
        super(QualityControlSample, self).__init__(**_kwargs)
        self.__qc_sample_type = None
        if qc_sample_type:
            self.qc_sample_type = qc_sample_type

    @property
    def qc_sample_type(self):
        return self.__qc_sample_type

    @qc_sample_type.setter
    def qc_sample_type(self, qc_sample_type):
        if qc_sample_type not in self.ALLOWED_QC_SAMPLE_TYPES:
            raise AttributeError(errors.QC_SAMPLE_TYPE_ERROR.format(self.ALLOWED_QC_SAMPLE_TYPES))
        self.__qc_sample_type = qc_sample_type


class QualityControl(object):
    """
    This class captures information about a Quality Control Check. It comes attached to an Assay Graph object
    """

    def __init__(self, pre_run_sample_type=None, post_run_sample_type=None, interspersed_sample_type=None):
        self.__pre_run_sample_type = None
        self.__post_run_sample_type = None
        self.__interspersed_sample_types = []
        if pre_run_sample_type:
            self.pre_run_sample_type = pre_run_sample_type
        if post_run_sample_type:
            self.post_run_sample_type = post_run_sample_type
        if interspersed_sample_type:
            self.interspersed_sample_types = interspersed_sample_type

    def __repr__(self):
        return '{0}.{1}(pre_run_sample_type={2.pre_run_sample_type}, post_run_sample_type={2.post_run_sample_type}, ' \
               'interspersed_sample_types={2.interspersed_sample_types})'.format(
                    self.__class__.__module__, self.__class__.__name__, self
                )

    def __str__(self):
        return """{0}(
        pre_run_sample_type={1}
        post_run_sample_type={2} 
        interspersed_sample_types={3}
        )""".format(
            self.__class__.__name__,
            self.pre_run_sample_type.id if self.pre_run_sample_type else None,
            self.post_run_sample_type.id if self.post_run_sample_type else None,
            [(elem.id, n) for elem, n in self.interspersed_sample_types]
        )

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, QualityControl) and \
               self.pre_run_sample_type == other.pre_run_sample_type and \
               self.post_run_sample_type == other.post_run_sample_type and \
               self.interspersed_sample_types == other.interspersed_sample_types

    def __ne__(self, other):
        return not self == other

    @property
    def pre_run_sample_type(self):
        return self.__pre_run_sample_type

    @pre_run_sample_type.setter
    def pre_run_sample_type(self, pre_run_sample_type):
        if not isinstance(pre_run_sample_type, ProductNode):
            raise AttributeError(errors.PRE_BATCH_ATTRIBUTE_ERROR)
        self.__pre_run_sample_type = pre_run_sample_type

    @property
    def post_run_sample_type(self):
        return self.__post_run_sample_type

    @post_run_sample_type.setter
    def post_run_sample_type(self, post_run_sample_type):
        if not isinstance(post_run_sample_type, ProductNode):
            raise AttributeError(errors.POST_BATCH_ATTRIBUTE_ERROR)
        self.__post_run_sample_type = post_run_sample_type

    @property
    def interspersed_sample_types(self):
        return self.__interspersed_sample_types

    @interspersed_sample_types.setter
    def interspersed_sample_types(self, interspersed_sample_types):
        try:
            for sample_type, interspersing_interval in interspersed_sample_types:
                self.add_interspersed_sample_type(sample_type, interspersing_interval)
        except (TypeError, ValueError) as e:
            raise AttributeError(e)

    def add_interspersed_sample_type(self, sample_type, interspersing_interval=10):
        if not isinstance(sample_type, ProductNode):
            raise TypeError(errors.INTERSPERSED_SAMPLE_TYPE_NODE_ERROR)
        if not isinstance(interspersing_interval, int):
            raise TypeError(errors.INTERSPERSED_SAMPLE_TYPE_INTERVAL_TYPE_ERROR)
        if interspersing_interval < 1:
            raise ValueError(errors.INTERSPERSED_SAMPLE_TYPE_INTERVAL_VALUE_ERROR)
        self.__interspersed_sample_types.append((sample_type, interspersing_interval))


class AssayGraph(object):
    """
    The AssayGraph captures the structure and information of an assay workflow
    (e.g sample derivatives extraction, labelling, and the instrument analysis itself)
    This information is stored in a graph (a directed tree, more correctly) of ProductNodes and
    ProcessNodes. Each ProcessNode has ProductNodes as outputs and potentially as inputs.
    """

    def __init__(self, measurement_type, technology_type, id_=str(uuid.uuid4()), nodes=None, links=None,
                 quality_control=None):
        """
        initializes an AssayGraph object
        If no dictionary or None is given,
        an empty dictionary will be used
        """
        self.__id = id_
        self.__measurement_type = None
        self.__technology_type = None
        self.__graph_dict = {}
        self.__quality_control = None
        self.measurement_type = measurement_type
        self.technology_type = technology_type
        if nodes:
            self.add_nodes(nodes)
        if links:
            self.add_links(links)
        if quality_control:
            pass

    @classmethod
    def generate_assay_plan_from_dict(cls, assay_plan_dict,
                                      validation_template=None, quality_control=None,
                                      use_guids=False, **kwargs):
        """
        Alternative constructor that generates an AssayGraph object from a well structured dictionary
        :param assay_plan_dict: dict
        :param validation_template: dict, not used yet # TODO
        :param quality_control
        :param use_guids: boolean
        :return: AssayGraph
        """

        res = cls(
            id_=kwargs.get('id_', str(uuid.uuid4())),
            measurement_type=assay_plan_dict['measurement_type'],
            technology_type=assay_plan_dict['technology_type']
        )

        previous_nodes = []
        current_nodes = []
        for node_key, node_params in assay_plan_dict.items():

            if node_key in ('id', 'name', 'selected_sample_types', 'measurement_type', 'technology_type'):
                continue

            node_name = node_key.term if isinstance(node_key, OntologyAnnotation) else node_key

            if isinstance(node_params, list):    # the node is a ProductNode
                for i, node_params_dict in enumerate(node_params):
                    for j, prev_node in enumerate(previous_nodes):
                        # log.debug('count: {0}, prev_node: {1}'.format(j, prev_node.id))
                        product_node = ProductNode(
                            id_=str(uuid.uuid4()) if use_guids else '{0}_{1}_{2}'.format(
                                re.sub(r'\s+', '_', node_name), str(i).zfill(3), str(j).zfill(3)
                            ),
                            name=node_name, node_type=node_params_dict['node_type'], size=node_params_dict['size'],
                            extension=node_params_dict.get('extension', None),
                            characteristics=[
                                Characteristic(category=node_params_dict['characteristics_category'],
                                               value=node_params_dict['characteristics_value'])
                            ] if 'characteristics_category' in node_params_dict else [])
                        res.add_node(product_node)
                        res.add_link(prev_node, product_node)
                        current_nodes.append(product_node)
            else:       # the node is a ProtocolNode
                try:
                    replicates = node_params.get('#replicates', 1)
                except AttributeError as e:
                    raise e
                node_params = {key: val for key, val in node_params.items() if key != '#replicates'}
                # log.debug(node_params)
                pv_names, pv_all_values = list(node_params.keys()), list(node_params.values())
                pv_combinations = itertools.product(*[val for val in pv_all_values])
                for i, pv_combination in enumerate(pv_combinations):
                    log.debug('pv_combination: {0}'.format(pv_combination))
                    if not previous_nodes:
                        protocol_node = ProtocolNode(
                            id_=str(uuid.uuid4()) if use_guids else '{0}_{1}'.format(
                                re.sub(r'\s+', '_', node_name), str(i).zfill(ZFILL_WIDTH)
                            ),
                            name='assay{} - {}'.format(assay_plan_dict.get('id', 0), node_name),
                            protocol_type='assay{} - {}'.format(assay_plan_dict.get('id', 0), node_key),
                            parameter_values=[
                                ParameterValue(category=ProtocolParameter(parameter_name=pv_names[ix]),
                                               value=pv)
                                for ix, pv in enumerate(pv_combination)
                            ],
                            replicates=replicates
                        )
                        res.add_node(protocol_node)
                        current_nodes.append(protocol_node)
                    else:
                        for j, prev_node in enumerate(previous_nodes):
                            # log.debug('count: {0}, prev_node: {1}'.format(j, prev_node.id))
                            protocol_node = ProtocolNode(
                                id_=str(uuid.uuid4()) if use_guids else '{0}_{1}_{2}'.format(
                                    re.sub(r'\s+', '_', node_name), str(i).zfill(3), str(j).zfill(3)
                                ),
                                name='assay{} - {}'.format(assay_plan_dict.get('id', 0), node_name),
                                protocol_type='assay{} - {}'.format(assay_plan_dict.get('id', 0), node_key),
                                parameter_values=[
                                    ParameterValue(category=ProtocolParameter(parameter_name=pv_names[ix]),
                                                   value=pv)
                                    for ix, pv in enumerate(pv_combination)
                                ],
                                replicates=replicates
                            )
                            res.add_node(protocol_node)
                            res.add_link(prev_node, protocol_node)
                            current_nodes.append(protocol_node)
            previous_nodes = current_nodes
            current_nodes = []
        if quality_control:
            res.quality_control = quality_control
        return res

    @property
    def id(self):
        return self.__id

    @property
    def measurement_type(self):
        return self.__measurement_type

    @measurement_type.setter
    def measurement_type(self, measurement_type):
        if not isinstance(measurement_type, OntologyAnnotation) and not isinstance(measurement_type, str):
            raise AttributeError(errors.INVALID_MEASUREMENT_TYPE_ERROR.format(measurement_type))
        self.__measurement_type = measurement_type

    @property
    def technology_type(self):
        return self.__technology_type

    @technology_type.setter
    def technology_type(self, technology_type):
        if not isinstance(technology_type, OntologyAnnotation) and not isinstance(technology_type, str):
            raise AttributeError(errors.INVALID_TECHNOLOGY_TYPE_ERROR.format(technology_type))
        self.__technology_type = technology_type

    @property
    def name(self):
        first_term = self.measurement_type.term if isinstance(
            self.measurement_type, OntologyAnnotation
        ) else self.measurement_type
        second_term = self.technology_type.term if isinstance(
            self.technology_type, OntologyAnnotation
        ) else self.technology_type
        return '{}-{}'.format(first_term, second_term)

    @property
    def nodes(self):
        return set(self.__graph_dict.keys()) # should this be a list rather than a set?
        # return sorted(self.__graph_dict.keys(), key=lambda el: el.id)

    def add_node(self, node):
        if not isinstance(node, SequenceNode):
            raise TypeError(errors.INVALID_NODE_ERROR.format(type(node)))
        if node in self.__graph_dict.keys():
            raise ValueError(errors.NODE_ALREADY_PRESENT.format(node))
        self.__graph_dict[node] = []

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    @property
    def links(self):
        """ 
        A private method generating the edges of the 
        graph "graph". 
        """
        return set((node, target_node) for node, target_nodes in self.__graph_dict.items()
                   for target_node in target_nodes)

    def add_link(self, start_node, target_node):
        """
        if not (isinstance(start_node, ProductNode) and isinstance(target_node, ProtocolNode)) and \
                not (isinstance(start_node, ProtocolNode) and isinstance(target_node, ProductNode)):
        """
        if isinstance(start_node, ProductNode) and isinstance(target_node, ProductNode):
            raise TypeError(errors.INVALID_LINK_ERROR)
        if start_node not in self.__graph_dict.keys() or target_node not in self.__graph_dict.keys():
            raise ValueError(errors.MISSING_NODE_ERROR)
        self.__graph_dict[start_node].append(target_node)

    def add_links(self, links):
        """
        Add multiple links at once
        :param links: a list of two-elements lists/tuples. The two elemts must be valid nodes
        :return:
        """
        for link in links:
            self.add_link(*link)

    @property
    def start_nodes(self):
        return set(self.__graph_dict.keys()) - set(target_node for target_nodes in self.__graph_dict.values()
                                                   for target_node in target_nodes)

    def next_nodes(self, node):
        if not isinstance(node, SequenceNode):
            raise TypeError(errors.INVALID_NODE_ERROR)
        if node not in self.__graph_dict:
            raise ValueError(errors.MISSING_NODE_ERROR)
        return set(self.__graph_dict[node])

    def previous_nodes(self, node):
        if not isinstance(node, SequenceNode):
            raise TypeError(errors.INVALID_NODE_ERROR)
        if node not in self.__graph_dict:
            raise ValueError(errors.MISSING_NODE_ERROR)
        return {n for n in self.__graph_dict if node in self.__graph_dict[n]}

    def previous_protocol_nodes(self, protocol_node):
        """
        This method should return a set containing all the previous protocol nodes of a single protocol node.
        Ideally, there should be only one parent protocol node for any given protocol_node, but we can anticipate that
        in future scenarios there will be more than one
        :param protocol_node:
        :return:
        """
        if not isinstance(protocol_node, ProtocolNode):
            raise TypeError(errors.INVALID_NODE_ERROR)
        # previous_protocol_nodes = set()
        current_nodes = {protocol_node}
        previous_nodes = set()
        while current_nodes:
            # log.debug('current nodes are: {0}'.format(current_nodes))
            for node in current_nodes:
                previous_nodes.update(self.previous_nodes(node))
                # log.debug('Previous nodes after current node {0} are {1}'.format(node, previous_nodes))
            previous_protocol_nodes = list(filter(lambda n: isinstance(n, ProtocolNode), previous_nodes))
            # log.debug('Previous nodes now are: {0}'.format(previous_nodes))
            # log.debug('Previous protocol nodes now are: {0}'.format(previous_protocol_nodes))
            if previous_protocol_nodes:
                # log.debug('Returning...')
                return set(previous_protocol_nodes)
            else:
                current_nodes = previous_nodes
                previous_nodes = set()
                # log.debug('Current nodes are now {0}'.format(current_nodes))
                # log.debug('Previous nodes are now {0}'.format(previous_nodes))
        # log.debug('Exiting without return...')

    """
    @property
    def sample_nodes(self):
        return {node for node in self.start_nodes if node.type == SAMPLE}
    """

    @property
    def end_nodes(self):
        return set(node for node in self.__graph_dict.keys() if not self.__graph_dict[node])

    @property
    def quality_control(self):
        return self.__quality_control

    @quality_control.setter
    def quality_control(self, quality_control):
        if not isinstance(quality_control, QualityControl):
            raise AttributeError(errors.QUALITY_CONTROL_ERROR.format(type(quality_control)))
        self.__quality_control = quality_control

    def find_paths(self, start_node, end_node, path=[]):
        if start_node not in self.nodes or end_node not in self.nodes:
            raise ValueError(errors.MISSING_NODE_ERROR)
        path += [start_node]
        if start_node == end_node:
            return [path]
        paths = []
        for node in self.__graph_dict[start_node]:
            if node not in path:
                extended_paths = self.find_paths(node, end_node, path)

                for p in extended_paths:
                    paths.append(p)
        return paths

    def find_all_paths(self):
        paths = []
        for start_node in self.start_nodes:
            for end_node in self.end_nodes:
                paths += self.find_paths(start_node, end_node)
        return paths

    def as_networkx_graph(self):
        """leverage the Networkx graph library to draw the AssayGraph"""
        nx_graph = nx.DiGraph()
        for node in self.nodes:
            nx_graph.add_node(node.id, node_type=node.__class__.__name__, name=node.name)
        for start_node, end_node in self.links:
            nx_graph.add_edge(start_node.id, end_node.id)
        return nx_graph

    def __repr__(self):
        links = [(start_node.id, end_node.id) for start_node, end_node in self.links]
        return '{0}.{1}(id={2.id}, measurement_type={2.measurement_type}, technology_type={2.technology_type}, ' \
               'nodes={2.nodes}, links={3}, quality_control={2.quality_control})'.format(
                    self.__class__.__module__, self.__class__.__name__, self,
                    sorted(links, key=lambda link: (link[0], link[1]))
                )

    def __str__(self):
        links = [(start_node.id, end_node.id) for start_node, end_node in self.links]
        return """"{0}(
        id={1.id}
        measurement_type={1.measurement_type} 
        technology_type={1.technology_type}
        nodes={1.nodes} 
        links={2}
        )""".format(
            self.__class__.__name__, self, sorted(links, key=lambda link: (link[0], link[1]))
        )

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, AssayGraph) and self.measurement_type == other.measurement_type \
               and self.technology_type == other.technology_type \
               and self.nodes == other.nodes \
               and self.links == other.links and self.quality_control == other.quality_control

    def __ne__(self, other):
        return not self == other


def get_full_class_name(instance):
    return "{0}.{1}".format(instance.__class__.__module__, instance.__class__.__name__)


class SampleAndAssayPlan(object):

    """
    A SampleAndAssayPlan contains metadata about both the sample and assay plan to be applied to a specific
    StudyCell.
    - sample_plan is a set of ProductNodes of type SAMPLE. Each of them describes a type of sample provided
    as input to the each assay in the assay_plan
    - assay_plan is as set of AssayGraphs to support multiple assays to be run on the same batch of samples
    """

    def __init__(self, name, sample_plan=None, assay_plan=None):
        """
        SampleAndAssayPlan constructor method
        :param name: string - a unique name (within the Arm that identifies the current SampleAndAssayPlan)
        :param sample_plan: (set/list/Iterable) - a set of ProductNode objects of type SAMPLE
        :param assay_plan: (set/list/Iterable) - a set of AssayGraph objects
        """
        self.__name = None
        self.__sample_plan = set()
        self.__assay_plan = set()
        self.__sample_to_assay_map = {}
        self.name = name
        if sample_plan:
            self.sample_plan = sample_plan
        if assay_plan:
            self.assay_plan = assay_plan

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise AttributeError(errors.ASSAY_PLAN_NAME_ERROR.format(name))
        self.__name = name

    @property
    def sample_plan(self):
        # return sorted(self.__sample_plan, key=lambda sample_type: sample_type.id) if self.__sample_plan else []
        return self.__sample_plan

    @sample_plan.setter
    def sample_plan(self, sample_plan):
        if not isinstance(sample_plan, Iterable) or not all(isinstance(sample_type, ProductNode)
                                                            for sample_type in sample_plan):
            raise AttributeError()
        for sample_type in sample_plan:
            self.add_sample_type_to_plan(sample_type)

    def add_sample_type_to_plan(self, sample_type):
        if not isinstance(sample_type, ProductNode):
            raise TypeError()
        self.__sample_plan.add(sample_type)

    @property
    def assay_plan(self):
        # return sorted(self.__assay_plan, key=lambda assay_graph: assay_graph.id) if self.__assay_plan else []
        return self.__assay_plan

    @assay_plan.setter
    def assay_plan(self, assay_plan):
        if not isinstance(assay_plan, Iterable) or not all(isinstance(assay_graph, AssayGraph)
                                                           for assay_graph in assay_plan):
            raise AttributeError()
        for assay_graph in assay_plan:
            self.add_assay_graph_to_plan(assay_graph)

    def add_assay_graph_to_plan(self, assay_graph):
        if not isinstance(assay_graph, AssayGraph):
            raise TypeError()
        self.__assay_plan.add(assay_graph)

    @property
    def sample_to_assay_map(self):
        return self.__sample_to_assay_map

    @sample_to_assay_map.setter
    def sample_to_assay_map(self, sample_to_assay_map):
        for sample_node, assay_graphs in sample_to_assay_map.items():
            for assay_graph in assay_graphs:
                self.add_element_to_map(sample_node, assay_graph)

    def add_element_to_map(self, sample_node, assay_graph):
        if sample_node not in self.sample_plan:
            raise ValueError(errors.MISSING_SAMPLE_IN_PLAN)
        if assay_graph not in self.assay_plan:
            raise ValueError(errors.MISSING_ASSAY_IN_PLAN)
        if sample_node in self.__sample_to_assay_map:
            self.__sample_to_assay_map[sample_node].add(assay_graph)
        else:
            self.__sample_to_assay_map[sample_node] = {assay_graph}

    @classmethod
    def from_sample_and_assay_plan_dict(cls, name, sample_type_dicts, *assay_plan_dicts, validation_template=None,
                                        use_guids=False, quality_controls=[]):
        """
        An alternative constructor that builds the SampleAndAssayPlan graph object from a schema provided as an
        OrderedDict, which can optionally be validated against a validation_schema
        :param name: string, the name of the SampleAndAssayPlan to be created
        :param sample_type_dicts: list of dicts
        :param assay_plan_dicts: list of OrderedDicts
        :param validation_template: dict/OrderedDict
        :param use_guids: bool
        :param quality_controls: list of QualityControl objects. Ideally should be as long as the number
                                of assay_plan_dicts provided
        :return: SampleAndAssayPlan
        """
        res = cls(name)
        for i, sample_type_dict in enumerate(sample_type_dicts):
            sample_node = ProductNode(
                id_=str(uuid.uuid4()) if use_guids else '{0}_{1}'.format(SAMPLE, str(i).zfill(3)),
                name=SAMPLE, node_type=sample_type_dict['node_type'], size=sample_type_dict['size'],
                characteristics=[
                    Characteristic(category=sample_type_dict['characteristics_category'],
                                   value=sample_type_dict['characteristics_value'])
                ] if 'characteristics_category' in sample_type_dict else [])
            res.add_sample_type_to_plan(sample_node)
        assay_map = {}
        for i, assay_plan_dict in enumerate(assay_plan_dicts):
            assay_graph = AssayGraph.generate_assay_plan_from_dict(
                assay_plan_dict,
                # FIXME: this id cannot work as it is
                id_=str(uuid.uuid4()) if use_guids
                else '{}{}'.format(ASSAY_GRAPH_PREFIX, assay_plan_dict['id']) if 'id' in assay_plan_dict
                else '{}{}'.format(
                    ASSAY_GRAPH_PREFIX, str(i).zfill(n_digits(len(assay_plan_dicts)))
                ),
                quality_control=quality_controls[i] if len(quality_controls) > i else None
            )
            res.add_assay_graph_to_plan(assay_graph)
            assay_map[assay_graph] = assay_plan_dict
        for sample_node in res.sample_plan:
            for assay_graph in res.assay_plan:
                if 'selected_sample_types' not in assay_map[assay_graph]:
                    res.add_element_to_map(sample_node, assay_graph)
                elif any(map(
                        lambda char: char.value in assay_map[assay_graph]['selected_sample_types'],
                        sample_node.characteristics
                )):
                    res.add_element_to_map(sample_node, assay_graph)
        return res

    def __repr__(self):
        s2a_map = {}
        for [st, ags] in self.sample_to_assay_map.items():
            s2a_map[st] = sorted({ag.id for ag in ags})
        sample_plan = sorted(self.sample_plan, key=lambda s_t: s_t.id)
        return '{0}.{1}(name={2.name}, sample_plan={4}, assay_plan={2.assay_plan}, ' \
               'sample_to_assay_map={3})'.format(
                    self.__class__.__module__, self.__class__.__name__, self, s2a_map, sample_plan
                )

    def __str__(self):
        return """{0}(
        name={1.name},
        sample_plan={1.sample_plan}, 
        assay_plan={1.assay_plan}
        )""".format(self.__class__.__name__, self)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, SampleAndAssayPlan) \
               and self.sample_plan == other.sample_plan \
               and self.name == other.name \
               and self.assay_plan == other.assay_plan \
               and self.sample_to_assay_map == other.sample_to_assay_map

    def __ne__(self, other):
        return not self == other


class SampleAndAssayPlanEncoder(json.JSONEncoder):

    @staticmethod
    def node(obj):
        onto_encoder = OntologyAnnotationEncoder()
        if isinstance(obj, ProtocolNode):
            return {
                "@id": obj.id,
                # "@type": get_full_class_name(obj),
                "name": obj.name,
                "protocolType": obj.protocol_type
                if isinstance(obj.protocol_type, str)
                else onto_encoder.ontology_annotation(obj.protocol_type),
                "description": obj.description,
                "uri": obj.uri,
                "version": obj.version,
                "parameterValues": [{
                    "name": onto_encoder.ontology_annotation(parameter_value.category.parameter_name),
                    "value": parameter_value.value if isinstance(parameter_value.value, Number)
                    else onto_encoder.ontology_annotation(parameter_value.value),
                    "unit": onto_encoder.ontology_annotation(parameter_value.unit)
                } for parameter_value in obj.parameter_values],
                # "components": []
            }
        if isinstance(obj, ProductNode):
            return {
                "@id": obj.id,
                # "@type": get_full_class_name(obj),
                "name": obj.name,
                "productType": obj.type,
                "size": obj.size,
                "characteristics": [{
                    "category": onto_encoder.ontology_annotation(char.category),
                    "value": char.value if isinstance(char.value, Number)
                    else onto_encoder.ontology_annotation(char.value)
                } for char in obj.characteristics if isinstance(char, Characteristic)]
            }

    @staticmethod
    def link(obj):
        if isinstance(obj, tuple):
            start_node, end_node = obj
            return [start_node.id, end_node.id]

    def assay_graph(self, obj):
        if isinstance(obj, AssayGraph):
            onto_encoder = OntologyAnnotationEncoder()
            return {
                "@id": obj.id,
                "measurementType": obj.measurement_type
                if isinstance(obj.measurement_type, str)
                else onto_encoder.ontology_annotation(obj.measurement_type),
                "technologyType": obj.technology_type
                if isinstance(obj.technology_type, str)
                else onto_encoder.ontology_annotation(obj.technology_type),
                "nodes": [self.node(node) for node in obj.nodes],
                "links": [self.link(link) for link in obj.links]
            }

    def default(self, obj):
        if isinstance(obj, SampleAndAssayPlan):
            return {
                "name": obj.name,
                "samplePlan": [self.node(sample_node) for sample_node in sorted(obj.sample_plan, key=lambda el: el.id)],
                "assayPlan": [self.assay_graph(assay_graph) for assay_graph in sorted(obj.assay_plan,
                                                                                      key=lambda el: el.id)],
                "sampleToAssayMap": {
                    sample_node.id: [assay_graph.id for assay_graph in assay_graphs]
                    for sample_node, assay_graphs in obj.sample_to_assay_map.items()
                }
            }


class SampleAndAssayPlanDecoder(object):

    @staticmethod
    def loads_parameter_value(pv_dict):
        pv_name = pv_dict["name"]
        return ParameterValue(
            category=ProtocolParameter(
                parameter_name=CharacteristicDecoder.loads_ontology_annotation(pv_name)
                if isinstance(pv_name, dict) else pv_name
            ),
            value=pv_dict["value"],
            unit=pv_dict.get('unit', None)
        )

    @staticmethod
    def loads_protocol_type(pt_dict):
        return OntologyAnnotation(**pt_dict)

    def loads_node(self, node_dict):
        char_decoder = CharacteristicDecoder()
        # if node_dict["@type"] == "{0}.{1}".format(ProtocolNode.__module__, ProtocolNode.__name__):
        if "protocolType" in node_dict:
            return ProtocolNode(id_=node_dict["@id"], name=node_dict["name"], description=node_dict["description"],
                                uri=node_dict["uri"], version=node_dict["version"],
                                parameter_values=[
                                    self.loads_parameter_value(param) for param in node_dict["parameterValues"]
                                ],
                                protocol_type=self.loads_protocol_type(node_dict["protocolType"]))
        elif "productType" in node_dict:
            return ProductNode(id_=node_dict["@id"], name=node_dict["name"], size=node_dict["size"],
                               node_type=node_dict["productType"],
                               characteristics=[
                                   char_decoder.loads_characteristic(chr) for chr in node_dict["characteristics"]
                               ])

    def loads_assay_graph(self, assay_graph_dict):
        measurement_type = assay_graph_dict["measurementType"] if isinstance(assay_graph_dict["measurementType"], str) \
            else OntologyAnnotation(**assay_graph_dict["measurementType"])
        technology_type = assay_graph_dict["technologyType"] if isinstance(assay_graph_dict["technologyType"], str) \
            else OntologyAnnotation(**assay_graph_dict["technologyType"])
        assay_graph = AssayGraph(id_=assay_graph_dict["@id"], measurement_type=measurement_type,
                                 technology_type=technology_type)
        nodes = [self.loads_node(node_dict) for node_dict in assay_graph_dict["nodes"]]
        assay_graph.add_nodes(nodes)
        for [start_node_id, end_node_id] in assay_graph_dict["links"]:
            assay_graph.add_link(next(node for node in assay_graph.nodes if node.id == start_node_id),
                                 next(node for node in assay_graph.nodes if node.id == end_node_id))
        return assay_graph

    def loads_sample_and_assay_plan(self, json_dict):
        plan = SampleAndAssayPlan(
            name=json_dict["name"],
            sample_plan=[self.loads_node(sample_dict) for sample_dict in json_dict["samplePlan"]],
            assay_plan=[self.loads_assay_graph(graph_dict) for graph_dict in json_dict["assayPlan"]]
        )
        plan.sample_to_assay_map = {
            next(sample_node for sample_node in plan.sample_plan if sample_node.id == sample_node_id):
                [assay_graph for assay_graph in plan.assay_plan if assay_graph.id in assay_ids]
            for sample_node_id, assay_ids in json_dict["sampleToAssayMap"].items()
        }
        return plan

    def loads(self, json_text):
        json_dict = json.loads(json_text)
        return self.loads_sample_and_assay_plan(json_dict)


class StudyArm(object):
    """
    Each study Arm is constituted by a mapping (ordered dict?) StudyCell -> SampleAndAssayPlan
    We call this mapping arm_map
    """

    DEFAULT_SOURCE_TYPE = DEFAULT_SOURCE_TYPE

    def __init__(
            self,
            name,
            arm_map=None,
            source_type=None,
            source_characteristics=None,
            group_size=0
    ):
        """
        The default constructor.
        :param name: string
        :param arm_map: OrderedDict - a StudyCell -> SampleAndAssayPlan ordered mapping
        :param source_type: Characteristic/str - determines the "type" of the subjects/sources
        :param group_size: int - a positive integer who specifies the number of subject in the Arm
        """
        self.__name = ''
        self.__source_type = None
        self.__source_characteristics = set()
        self.__group_size = None
        self.__arm_map = OrderedDict()
        self.name = name
        self.group_size = group_size
        if arm_map is not None:
            self.arm_map = arm_map
        if source_type:
            self.source_type = source_type
        if source_characteristics:
            self.source_characteristics = source_characteristics

    def __repr__(self):
        return '{0}.{1}(' \
               'name={name}, ' \
               'source_type={source_type}, ' \
               'source_characteristics={source_characteristics}, ' \
               'group_size={group_size}, ' \
               'cells={cells}, ' \
               'sample_assay_plans={sample_assay_plans})'.format(
                    self.__class__.__module__, self.__class__.__name__,
                    name=self.name, source_type=self.source_type,
                    source_characteristics=[sc for sc in sorted(
                        self.source_characteristics,
                        key=lambda sc: sc.category if isinstance(sc.category, str) else sc.category.term
                    )],
                    group_size=self.group_size,
                    cells=self.cells, sample_assay_plans=self.sample_assay_plans
                )

    def __str__(self):
        return """"{0}(
               name={name},
               source_type={source_type},
               group_size={group_size}, 
               no. cells={cells},
               no. sample_assay_plans={sample_assay_plans}
               )""".format(
                    self.__class__.__name__, name=self.name, group_size=self.group_size,
                    source_type=self.source_type,
                    cells=len([cell.name for cell in self.cells]),
                    sample_assay_plans=len([plan.name for plan in sorted(self.sample_assay_plans)])
        )

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, StudyArm) and \
               self.name == other.name and \
               self.source_type == other.source_type and \
               self.source_characteristics == other.source_characteristics and \
               self.group_size == other.group_size and \
               self.arm_map == other.arm_map

    def __ne__(self, other):
        return not self == other

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise AttributeError('StudyArm name must be a string')
        self.__name = name

    @property
    def source_type(self):
        if self.__source_type is not None:
            return self.__source_type
        else:
            return self.DEFAULT_SOURCE_TYPE

    @source_type.setter
    def source_type(self, source_type):
        if not isinstance(source_type, (str, Characteristic)):
            raise AttributeError(errors.SOURCE_TYPE_ERROR.format(source_type))
        self.__source_type = source_type

    @property
    def source_characteristics(self):
        return self.__source_characteristics

    @source_characteristics.setter
    def source_characteristics(self, source_characteristics):
        if not (
                isinstance(source_characteristics, Iterable) and
                all(isinstance(sc, Characteristic) for sc in source_characteristics)
        ):
            raise AttributeError("all source characteristics must be instance of Characteristic")
        self.__source_characteristics = {sc for sc in source_characteristics}

    @property
    def group_size(self):
        return self.__group_size

    @group_size.setter
    def group_size(self, group_size):
        if isinstance(group_size, int) and group_size >= 0:
            self.__group_size = group_size
        else:
            raise AttributeError('group_size must be a positive integer; {0} provided'.format(group_size))

    @property
    def arm_map(self):
        return self.__arm_map or OrderedDict()

    @arm_map.setter
    def arm_map(self, arm_map):
        if not isinstance(arm_map, OrderedDict):
            raise AttributeError(errors.ARM_MAP_ASSIGNMENT_ERROR)
        self.__arm_map.clear()
        try:
            for cell, sample_assay_plan in arm_map.items():
                self.add_item_to_arm_map(cell, sample_assay_plan)
        except ValueError as ve:
            raise AttributeError(ve.args[0])

    @property
    def cells(self):
        return list(self.arm_map.keys())

    @property
    def sample_assay_plans(self):
        return list(self.arm_map.values())

    @property
    def numeric_id(self):
        try:
            digits = re.findall(r'\d+', self.name)
            return int(digits[0])
        except IndexError:
            return -1

    def is_completed(self):
        """
        A StudyArm is considered completed if it contains a FOLLOW-UP cells
        :return: bool
        """
        return bool([el for cell in self.arm_map.keys() for el in cell.get_all_elements()
                     if el.type == FOLLOW_UP])

    def add_item_to_arm_map(self, cell, sample_assay_plan=None):
        """
        inserts a mapping StudyCell -> SampleAndAssayPlans to the StudyArm arm_map
        There are a few insertion rules for cells
        - To insert a cell containing a SCREEN the arm_map *must* be empty
        - To insert a cell containing a RUN-IN alone the arm_map *must* contain a SCREEN-only cell and no other cells
        - To insert a cell containing one or more Treatments (and washouts) the arm_map must not contain a FOLLOW-UP 
            cell. Moreover if the cell contains a WASHOUT we must ensure that the previous cell does not contain a 
            NonTreatment of any type as the latest element
        - To insert a cell containing a FOLLOW-UP the arm_map *must not* contain already a FOLLOW-UP cell
            Moreover, this cell cannot be inserted immediately after a SCREEN or a RUN-IN cell
        :param cell: (StudyCell)
        :param sample_assay_plan: (SampleAndAssayPlans/None)
        :return: 
        """
        if not isinstance(cell, StudyCell):
            raise TypeError('{0} is not a StudyCell object'.format(cell))
        if sample_assay_plan is not None and not isinstance(sample_assay_plan, SampleAndAssayPlan):
            raise TypeError('{0} is not a SampleAndAssayPlans object'.format(sample_assay_plan))
        if self.is_completed():
            raise ValueError(errors.COMPLETE_ARM_ERROR_MESSAGE)
        if cell.contains_non_treatment_element_by_type(SCREEN):
            if len(self.arm_map.keys()):
                raise ValueError(errors.SCREEN_ERROR_MESSAGE)
            self.__arm_map[cell] = sample_assay_plan
        elif cell.contains_non_treatment_element_by_type(RUN_IN):
            previous_cells = list(self.arm_map.keys())
            if len(previous_cells) == 1 and previous_cells[0].contains_non_treatment_element_by_type(SCREEN):
                self.__arm_map[cell] = sample_assay_plan
            else:
                raise ValueError(errors.RUN_IN_ERROR_MESSAGE)
        elif cell.contains_non_treatment_element_by_type(WASHOUT) and cell.get_all_elements()[0].type == WASHOUT:
            latest_cell = list(self.arm_map.keys())[-1]
            latest_element = latest_cell.get_all_elements()[-1]
            if isinstance(latest_element, NonTreatment):
                raise ValueError(errors.WASHOUT_ERROR_MESSAGE)
        elif cell.contains_non_treatment_element_by_type(FOLLOW_UP):
            previous_cells = list(self.arm_map.keys())
            if not len(previous_cells):
                raise ValueError(errors.FOLLOW_UP_EMPTY_ARM_ERROR_MESSAGE)
            latest_cell = list(self.arm_map.keys())[-1]
            if latest_cell.contains_non_treatment_element_by_type(SCREEN) or \
                    latest_cell.contains_non_treatment_element_by_type(RUN_IN):
                raise ValueError(errors.FOLLOW_UP_ERROR_MESSAGE)
        self.__arm_map[cell] = sample_assay_plan

    @property
    def treatments(self):
        """
        Returns all the Treatment elements contained in a StudyArm
        :return set - all the treatments in the StudyArm
        """
        # TODO should this be a set or a list or something else?
        return {elem for cell in self.arm_map.keys() for elem in cell.get_all_elements() if isinstance(elem, Treatment)}


class StudyArmEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, StudyArm):
            characteristic_encoder = CharacteristicEncoder()
            study_cell_encoder = StudyCellEncoder()
            sample_assay_plan_encoder = SampleAndAssayPlanEncoder()
            log.debug('StudyArm source_type is: {0}'.format(o.source_type))
            res = dict(
                name=o.name, groupSize=o.group_size,
                sourceType=characteristic_encoder.characteristic(o.source_type),
                sourceCharacteristics=[characteristic_encoder.characteristic(sc) for sc in o.source_characteristics],
                cells=[], sampleAndAssayPlans=[], mappings=[]
            )
            i = 0
            sample_assay_plan_set = set()
            for cell, sample_assay_plan in o.arm_map.items():
                # log.debug('Now appending cell {0}'.format(cell.name))
                res['cells'].append(study_cell_encoder.default(cell))
                if sample_assay_plan is not None and sample_assay_plan not in sample_assay_plan_set:
                    # log.debug('Now appending sample_assay_plan {0}'.format(sample_assay_plan.name))
                    res['sampleAndAssayPlans'].append(sample_assay_plan_encoder.default(sample_assay_plan))
                    sample_assay_plan_set.add(sample_assay_plan)
                res['mappings'].append([cell.name, sample_assay_plan.name if sample_assay_plan is not None else None])
                i += 1
            # log.debug('Mappings: {0}'.format(res['mappings']))
            return res


class StudyArmDecoder(object):

    def __init__(self):
        self.characteristic_decoder = CharacteristicDecoder()
        self.cell_decoder = StudyCellDecoder()
        self.sample_assay_plan_decoder = SampleAndAssayPlanDecoder()

    def loads_arm(self, json_dict):
        arm = StudyArm(
            name=json_dict['name'],
            source_type=self.characteristic_decoder.loads_characteristic(json_dict['sourceType']),
            source_characteristics=[
                self.characteristic_decoder.loads_characteristic(
                    json_sc
                ) for json_sc in json_dict['sourceCharacteristics']
            ],
            group_size=json_dict['groupSize']
        )
        sample_assay_plan_set = {
            self.sample_assay_plan_decoder.loads_sample_and_assay_plan(json_sample_assay_plan)
            for json_sample_assay_plan in json_dict['sampleAndAssayPlans']
        }
        for i, [cell_name, sample_assay_plan_name] in enumerate(json_dict['mappings']):
            # log.debug('i = {0}, mapping = {1}'.format(i, [cell_name, sample_assay_plan_name]))
            json_cell = json_dict['cells'][i]
            if json_cell['name'] != cell_name:
                raise ValueError()   # FIXME which is the right error type here?
            cell = self.cell_decoder.loads_cells(json_cell)
            sample_assay_plan = next(sap for sap in sample_assay_plan_set if sap.name == sample_assay_plan_name) \
                if sample_assay_plan_name is not None else None
            arm.add_item_to_arm_map(cell, sample_assay_plan)
        return arm

    def loads(self, json_text):
        json_dict = json.loads(json_text)
        return self.loads_arm(json_dict)


class StudyDesign(object):

    """
    Top-level class for the isatools.create module, and the study design planning.
    A class representing a study design, which is composed of a collection of
    study arms.
    StudyArms of different lengths (i.e. different number of cells) are allowed.
    """

    def __init__(
            self,
            identifier=None,
            name='Study Design',
            design_type=None,
            description=None,
            source_type=DEFAULT_SOURCE_TYPE,
            study_arms=None
    ):
        """
        :param identifier: str
        :param name: str
        :param description: str
        :param source_type: str or OntologyAnnotation
        :param study_arms: Iterable
        """
        self.identifier = identifier
        self.__study_arms = set()
        self.__name = name if isinstance(name, str) else 'Study Design'
        self.__design_type = None
        self.__description = None
        self.__source_type = None

        self.source_type = source_type
        if study_arms:
            self.study_arms = study_arms
        if description:
            self.description = description
        if design_type:
            self.design_type = design_type

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise AttributeError(errors.NAME_PROPERTY_ASSIGNMENT_ERROR)
        self.__name = name

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        if not isinstance(description, str):
            raise AttributeError(errors.DESCRIPTION_PROPERTY_ASSIGNMENT_ERROR)
        self.__description = description

    @property
    def design_type(self):
        return self.__design_type

    @design_type.setter
    def design_type(self, design_type):
        if not isinstance(design_type, (str, OntologyAnnotation)):
            raise AttributeError(errors.DESIGN_TYPE_PROPERTY_ASSIGNMENT_ERROR)
        self.__design_type = design_type

    @property
    def source_type(self):
        return self.__source_type

    @source_type.setter
    def source_type(self, source_type):
        if not isinstance(source_type, Characteristic):
            raise AttributeError('')
        self.__source_type = source_type

    @property
    def study_arms(self):
        return sorted(self.__study_arms, key=lambda arm: arm.name)

    @study_arms.setter
    def study_arms(self, study_arms):
        if not isinstance(study_arms, Iterable):
            raise AttributeError(errors.STUDY_ARM_PROPERTY_ASSIGNMENT_ERROR)
        try:
            for arm in study_arms:
                self.add_study_arm(arm)
        except (TypeError, ValueError) as e:
            raise AttributeError(e.args[0])

    def add_study_arm(self, study_arm):
        """
        add a StudyArm object to the study_arm set. 
        Arms of diff 
        :param study_arm: StudyArm
        """
        if not isinstance(study_arm, StudyArm):
            raise TypeError('{0}: {1}'.format(errors.ADD_STUDY_ARM_PARAMETER_TYPE_ERROR, study_arm))
        if any({arm for arm in self.study_arms if arm.name == study_arm.name}):
            raise ValueError('{0}'.format(errors.ADD_STUDY_ARM_NAME_ALREADY_PRESENT_ERROR))
        self.__study_arms.add(study_arm)

    @property
    def treatments(self):
        return {treatment for arm in self.study_arms for treatment in arm.treatments}

    def get_epoch(self, index=0):
        """
        Slices the StudyDesign at a specific epoch
        :param index: int the epoch index
        :return: list containing StudyCells one per arm, sliced at that epoch
        """
        epoch_cells = [arm.cells[index] if len(arm.cells) > index else None for arm in self.study_arms]
        if all([cell is None for cell in epoch_cells]):
            raise IndexError(errors.GET_EPOCH_INDEX_OUT_OR_BOUND_ERROR)
        return epoch_cells

    @staticmethod
    def _idgen_sources(group_id, subject_number):
        """
        Identifiers generator
        :param group_id: group ID
        :param subject_number: subject ID
        :return: str
        """
        idarr = []
        if group_id != '':
            idarr.append('{}{}'.format(GROUP_PREFIX, group_id))  # study group
        if subject_number != '':
            idarr.append('{}{}'.format(SUBJECT_PREFIX, subject_number))
        return '_'.join(idarr).replace(' ', '-')

    @staticmethod
    def _idgen_samples(source_name, cell_name, sample_number, sample_type):
        """
        Identifiers generator
        :param source_name: subject ID
        :param sample_number: sample Number
        :param sample_type: sample Term
        :return: 
        """
        idarr = []
        if source_name != '':
            idarr.append('{}'.format(source_name))
        if cell_name != '':
            idarr.append('{}'.format(cell_name))
        smparr = []
        smparr.append('{}'.format(SAMPLE_PREFIX))
        if sample_type != '':
            smparr.append(sample_type)
        if sample_number != '':
            smparr.append('{}'.format(sample_number))
        idarr.append('-'.join(smparr))
        return '_'.join(idarr).replace(' ', '-')

    def _generate_sources(self, ontology_source_references):
        """
        Private method to be used in 'generate_isa_study'.
        :return: 
        """
        src_map = dict()
        for s_ix, s_arm in enumerate(self.study_arms):
            source_prototype = Source(
                characteristics=[
                   s_arm.source_type if isinstance(s_arm.source_type, Characteristic) else Characteristic(
                       category=OntologyAnnotation(term=s_arm.source_type),
                       value=OntologyAnnotation(term=s_arm.source_type)
                   )
                ] + [sc for sc in sorted(
                    s_arm.source_characteristics, key=lambda sc: sc.category.term if isinstance(
                        sc.category, OntologyAnnotation
                    ) else sc.category
                )]
            )
            srcs = set()
            digits = n_digits(s_arm.group_size)
            for subj_n in (str(ix).zfill(digits) for ix in range(1, s_arm.group_size + 1)):
                src = copy.copy(source_prototype)
                src.name = self._idgen_sources(
                    s_arm.numeric_id if s_arm.numeric_id > -1 else s_ix + 1,  # start counting from 1
                    subj_n
                )
                srcs.add(src)
            src_map[s_arm.name] = list(srcs)
        return src_map

    def _generate_samples_and_assays(self, sources_map, sampling_protocol, performer):
        """
        Private method to be used in 'generate_isa_study'.
        :param sources_map: dict - the output of '_generate_sources'
        :param sampling_protocol: isatools.model.Protocol
        :param performer: str
        :return: 
        """
        factors = {SEQUENCE_ORDER_FACTOR}
        ontology_sources = set()
        samples = []
        sample_count = 0
        process_sequence = []
        assays = []
        protocols = set()
        unique_assay_types = {
            assay_graph for arm in self.study_arms
            for sample_assay_plan in arm.arm_map.values() if sample_assay_plan is not None
            for assay_graph in sample_assay_plan.assay_plan if assay_graph is not None
        }
        samples_grouped_by_assay_graph = {
            assay_graph: [] for assay_graph in unique_assay_types
        }

        # generate samples
        for arm in self.study_arms:
            epoch_nb = 0
            for cell, sample_assay_plan in arm.arm_map.items():
                is_treatment_comment = Comment(
                    name=IS_TREATMENT_EPOCH,
                    value='YES' if cell.has_treatments else 'NO'
                )
                seq_order_fv = FactorValue(
                    factor_name=SEQUENCE_ORDER_FACTOR,
                    value=epoch_nb
                )
                if not sample_assay_plan:
                    continue
                sample_batches = {sample_node: [] for sample_node in sample_assay_plan.sample_plan}
                factor_values = [seq_order_fv]
                for element in cell.get_all_elements():
                    factors.update([f_val.factor_name for f_val in element.factor_values])
                    # all the factor values up to the current element in the cell are actually serialised
                    # FIXME could this be an issue for concomitant treatments?
                    factor_values.extend([f_val for f_val in element.factor_values])
                for sample_node in sample_assay_plan.sample_plan:
                    for source in sources_map[arm.name]:
                        sample_type, sampling_size = sample_node.characteristics[0], sample_node.size
                        sample_term_source = sample_type.value.term_source if \
                            hasattr(sample_type.value, 'term_source') and sample_type.value.term_source else ''
                        if sample_term_source:
                            ontology_sources.add(sample_term_source)
                        sample_term = sample_type.value.term if \
                            isinstance(sample_type.value, OntologyAnnotation) else sample_type.value
                        for samp_idx in range(0, sampling_size):
                            sample = Sample(
                                name=self._idgen_samples(source.name, cell.name, str(samp_idx + 1), sample_term),
                                factor_values=factor_values,
                                characteristics=[sample_type],
                                derives_from=[source],
                                comments=[is_treatment_comment]
                            )
                            sample_batches[sample_node].append(sample)
                            sample_count += 1
                            process = Process(
                                executes_protocol=sampling_protocol, inputs=[source], outputs=[sample],
                                performer=performer,
                                date_=datetime.date.isoformat(datetime.date.today()),
                                parameter_values=[
                                    ParameterValue(
                                        category=sampling_protocol.get_param(RUN_ORDER),
                                        value=str(sample_count).zfill(3)
                                    ), ParameterValue(
                                        category=sampling_protocol.get_param(STUDY_CELL),
                                        value=str(cell.name)
                                    )
                                ]
                            )
                            process_sequence.append(process)
                for sample_node in sample_assay_plan.sample_plan:
                    samples.extend(sample_batches[sample_node])

                for assay_graph in sample_assay_plan.assay_plan:
                    for sample_node in sample_assay_plan.sample_plan:
                        if assay_graph in sample_assay_plan.sample_to_assay_map[sample_node]:
                            try:
                                samples_grouped_by_assay_graph[assay_graph] += sample_batches[sample_node]
                            except AttributeError:
                                log.error('Assay graph is: {}'.format(assay_graph))
                                problematic_sample_group = samples_grouped_by_assay_graph[assay_graph]
                                log.error('Sample bach for assay graph is: {}'.format(
                                    problematic_sample_group
                                ))
                epoch_nb += 1
        # generate assays
        for assay_graph in unique_assay_types:
            protocols.update({node for node in assay_graph.nodes if isinstance(node, Protocol)})
            assays.append(self.generate_assay(assay_graph, samples_grouped_by_assay_graph[assay_graph]))

        return factors, protocols, samples, assays, process_sequence, ontology_sources

    @staticmethod
    def _increment_counter_by_node_type(counter, node):
        if isinstance(node, ProductNode):
            # use node.name for DATA_FILE, node.type for other Product Nodes
            if node.type == DATA_FILE:
                counter[node.name] = counter[node.name] + 1 if node.name in counter else 1
            else:
                counter[node.type] = counter[node.type] + 1 if node.type in counter else 1

        if isinstance(node, ProtocolNode):
            # the attribute "name" should contain the same value as "protocol_type.term"
            counter[node.name] = counter[node.name] + 1 if node.name in counter else 1
        return counter

    @staticmethod
    def _generate_isa_elements_from_node(
            node,
            assay_graph,
            assay_file_prefix,  # to ensure uniqueness of node names within a study
            processes=None,
            other_materials=None,
            data_files=None,
            previous_items=None,
            start_node_index=0,
            counter=None
    ):
        if counter is None:
            counter = {}
        if previous_items is None:
            previous_items = []
        if data_files is None:
            data_files = []
        if other_materials is None:
            other_materials = []
        if processes is None:
            processes = []
        log.debug('# processes: {0} - ix: {1}'.format(len(processes), start_node_index))
        counter = StudyDesign._increment_counter_by_node_type(counter, node)
        item = StudyDesign._isa_objects_factory(
            node, assay_file_prefix, start_node_index, counter,
            measurement_type=assay_graph.measurement_type,
            technology_type=assay_graph.technology_type
        )
        if isinstance(item, Process):
            item.inputs = previous_items
            processes.append(item)
        elif isinstance(item, Material):
            other_materials.append(item)
        elif isinstance(item, DataFile):
            data_files.append(item)
        next_nodes = assay_graph.next_nodes(node)
        for ii, next_node in enumerate(next_nodes):
            size = next_node.size if isinstance(next_node, ProductNode) \
                else next_node.replicates if isinstance(next_node, ProtocolNode) \
                else 1
            for jj in range(size):
                log.debug('ii = {} - jj = {}'.format(ii, jj))
                # counter += 1
                processes, other_materials, data_files, next_item, counter = \
                    StudyDesign._generate_isa_elements_from_node(
                        next_node, assay_graph, assay_file_prefix, processes, other_materials, data_files,
                        [item], start_node_index=start_node_index, counter=counter
                )
                if isinstance(node, ProtocolNode):
                    item.outputs.append(next_item)
                    # the hypothesis here is that there is only one previous protocol node. Hence popping it
                    previous_protocol_nodes = assay_graph.previous_protocol_nodes(node)
                    previous_protocol_node = previous_protocol_nodes.pop() \
                        if previous_protocol_nodes and len(previous_protocol_nodes) == 1 \
                        else None
                    if previous_protocol_node:
                        previous_process = next(
                            process for process in processes[::-1]
                            if process.executes_protocol == previous_protocol_node
                        )
                        assert isinstance(previous_process, Process)
                        assert isinstance(item, Process)
                        log.debug('linking process {0} to process {1}'.format(previous_process.name, item.name))
                        plink(previous_process, item)  # TODO check if this generates any issue
        return processes, other_materials, data_files, item, counter

    @staticmethod
    def generate_assay(assay_graph, assay_samples):
        if not isinstance(assay_graph, AssayGraph):
            raise TypeError()
        """
        sample_char_value = getattr(sample_node.characteristics[0], 'value', None) \
            if isinstance(sample_node, ProductNode) and sample_node.characteristics \
            else None
        """
        measurement_type, technology_type = assay_graph.measurement_type, assay_graph.technology_type
        assay = Assay(
            measurement_type=measurement_type,
            technology_type=technology_type,
            filename=urlify('a_{0}_{1}_{2}.txt'.format(
                assay_graph.id,
                measurement_type.term if isinstance(measurement_type, OntologyAnnotation) else measurement_type,
                technology_type.term if isinstance(technology_type, OntologyAnnotation) else technology_type
            ))
        )
        log.debug('assay measurement type: {0} - technology type: {1}'.format(measurement_type,
                                                                              assay.technology_type))
        # assay.samples = assay_samples
        # assay.sources = {source for sample in assay_samples for source in sample.derives_from}
        # assay.process_sequence = sampling_processes
        for i, node in enumerate(assay_graph.start_nodes):
            size = node.size if isinstance(node, ProductNode) \
                else node.replicates if isinstance(node, ProtocolNode) \
                else 1
            log.debug('Size: {0}'.format(size))
            for j, sample in enumerate(assay_samples):
                log.debug('Iteration: {0} - Sample: {1}'.format(i, sample.name))
                for k in range(size):
                    ix = i * len(assay_samples) * size + j * size + k
                    log.debug('i = {0}, j = {1}, k={2}, ix={3}'.format(i, j, k, ix))
                    processes, other_materials, data_files, _, __ = StudyDesign._generate_isa_elements_from_node(
                        node, assay_graph, assay_graph.id, start_node_index=ix + 1, counter=None, processes=[],
                        other_materials=[], data_files=[], previous_items=[sample]
                    )
                    assay.other_material.extend(other_materials)
                    assay.process_sequence.extend(processes)
                    assay.data_files.extend(data_files)
                    log.debug('i={0}, i={1}, num_processes={2}, num_assay_files={3}'.format(i, j, len(processes),
                                                                                            len(data_files)))
        return assay

    @staticmethod
    def _isa_objects_factory(
            node,
            assay_file_prefix,
            start_node_index,
            counter,
            measurement_type=None,
            technology_type=None,
            performer=DEFAULT_PERFORMER
    ):
        """
        This method generates an ISA element from an ISA node
        :param technology_type:
        :param measurement_type:
        :param node: SequenceNode - can be either a ProductNode or a ProtocolNode
        :param assay_file_prefix: str
        :param start_node_index: int the index of the starting node in the graph
        :param counter: dict containing the counts for this specific subgraph
        :param performer: str/Person
        :return: either a Sample or a Material or a DataFile. So far only RawDataFile is supported among files
        """
        if isinstance(node, ProtocolNode):
            return Process(
                name='{}-S{}-{}-Acquisition-R{}'.format(
                    assay_file_prefix, start_node_index, urlify(node.name), counter[node.name]
                ),
                executes_protocol=node,
                performer=performer,
                parameter_values=node.parameter_values,
                inputs=[],
                outputs=[],
            )
        if isinstance(node, ProductNode):
            if node.type == SAMPLE:
                return Sample(
                    name='{}-S{}-Sample-R{}'.format(assay_file_prefix, start_node_index, counter[SAMPLE]),
                    characteristics=node.characteristics
                )
            if node.type == EXTRACT:
                return Extract(
                    name='{}-S{}-Extract-R{}'.format(assay_file_prefix, start_node_index, counter[EXTRACT]),
                    characteristics=node.characteristics
                )
            if node.type == LABELED_EXTRACT:
                return LabeledExtract(
                    name='{}-S{}-LE-R{}'.format(assay_file_prefix, start_node_index, counter[LABELED_EXTRACT]),
                    characteristics=node.characteristics
                )
            # under the hypothesis that we deal only with raw data files
            # derived data file would require a completely separate approach
            if node.type == DATA_FILE:
                try:
                    log.debug('Assay conf. found: {}; {};'.format(
                        measurement_type, technology_type)
                    )
                    m_type_term = measurement_type.term if isinstance(measurement_type, OntologyAnnotation) \
                        else measurement_type
                    t_type_term = technology_type.term if isinstance(technology_type, OntologyAnnotation) \
                        else technology_type
                    curr_assay_opt = next(
                        opt for opt in assays_opts if opt['measurement type'] == m_type_term and
                        opt['technology type'] == t_type_term
                    )
                    log.debug('Assay conf. found: {}; {}; {};'.format(
                        measurement_type, technology_type, curr_assay_opt)
                    )
                    isa_class = globals()[curr_assay_opt['raw data file'].replace(' ', '')]
                    assert isa_class in {
                        # expand this set if needed
                        RawDataFile, RawSpectralDataFile, ArrayDataFile, FreeInductionDecayDataFile,
                        DerivedDataFile, DerivedSpectralDataFile, DerivedArrayDataFile,
                        ProteinAssignmentFile, PeptideAssignmentFile, DerivedArrayDataMatrixFile,
                        PostTranslationalModificationAssignmentFile, AcquisitionParameterDataFile
                    }
                    file_extension = '.{}'.format(node.extension) if node.extension else ''
                    return isa_class(
                        filename='{}-S{}-{}-R{}{}'.format(
                            assay_file_prefix,
                            start_node_index,
                            urlify(node.name),
                            counter[node.name],
                            file_extension
                        )
                    )
                except StopIteration:
                    file_extension = '.{}'.format(node.extension) if node.extension else ''
                    return RawDataFile(
                        filename='{}-S{}-{}-R{}-{}'.format(
                            assay_file_prefix,
                            start_node_index,
                            urlify(node.name),
                            counter[node.name],
                            file_extension
                        )
                    )

    def generate_isa_study(self, identifier=None):
        """
        this is the core method to return the fully populated ISA Study object from the StudyDesign
        :return: isatools.model.Study
        """
        with open(os.path.join(os.path.dirname(__file__), '..', 'resources', 'config', 'yaml',
                               'study-creator-config.yml')) as yaml_file:
            config = yaml.load(yaml_file, Loader=yaml.FullLoader)
        study_config = config['study']
        study = Study(
            identifier=self.identifier or identifier or DEFAULT_STUDY_IDENTIFIER,
            title=self.name,
            filename=urlify(study_config['filename']),
            description=self.description,
            design_descriptors=[self.design_type] if isinstance(self.design_type, OntologyAnnotation) else None
        )
        study.ontology_source_references = [
            OntologySource(**study_config['ontology_source_references'][0])
        ]
        study.protocols = [
            Protocol(**protocol_config) for protocol_config in study_config['protocols']
        ]
        # log.debug('Sampling protocol is {0}'.format(study.protocols[0]))
        sources_map = self._generate_sources(study.ontology_source_references)
        study.sources = [source for sources in sources_map.values() for source in sources]
        study.factors, protocols, study.samples, study.assays, study.process_sequence, \
            study.ontology_source_references = \
            self._generate_samples_and_assays(
                sources_map, study.protocols[0], study_config['performers'][0]['name']
            )
        for protocol in protocols:
            study.add_protocol(protocol)
        return study

    def __repr__(self):
        return '{0}.{1}(' \
               'identifier={identifier}, ' \
               'name={name}, ' \
               'design_type={design_type}, ' \
               'description={description} ' \
               'source_type={source_type}, ' \
               'study_arms={study_arms}' \
               ')'.format(self.__class__.__module__, self.__class__.__name__, study_arms=self.study_arms,
                          identifier=self.identifier, name=self.name,
                          design_type=self.design_type, description=self.description,
                          source_type=self.source_type)

    def __str__(self):
        return """{0}(
               identifier={identifier}, 
               name={name},
               description={description},
               study_arms={study_arms}
               )""".format(self.__class__.__name__,
                           description=self.description,
                           study_arms=[arm.name for arm in sorted(self.study_arms)],
                           identifier=self.identifier, name=self.name)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, StudyDesign) and self.name == other.name and self.study_arms == other.study_arms

    def __ne__(self, other):
        return not self == other


class QualityControlService(object):

    def __init__(self):
        pass

    @classmethod
    def augment_study(cls, study, study_design, in_place=False):
        """
        Augment a study with QualityControl samples and modifies the assay
        :param study: Study
        :param study_design: StudyDesign
        :param in_place: boolean
        :return:
        """
        assert isinstance(in_place, bool)
        if not isinstance(study, Study):
            raise TypeError('study must be a valid Study object')
        if not isinstance(study_design, StudyDesign):
            raise TypeError('study must be a valid StudyDesign object')
        qc_study = deepcopy(study) if in_place is False else study
        for arm in study_design.study_arms:
            for cell, study_assay_plan in arm.arm_map.items():
                if study_assay_plan:
                    for assay_graph in study_assay_plan.assay_plan:
                        assert isinstance(assay_graph, AssayGraph)
                        if assay_graph.quality_control:
                            # CHECK the assumption here is that an assay file can unequivocally be identified
                            # by StudyCell name, corresponding AssayGraph id and measurement type
                            # Such an assumption is correct as far a the Assay filename convention is not modified
                            measurement_type, technology_type = assay_graph.measurement_type, \
                                assay_graph.technology_type
                            assay_filename = urlify('a_{0}_{1}_{2}.txt'.format(
                                assay_graph.id,
                                measurement_type.term if isinstance(measurement_type, OntologyAnnotation)
                                else measurement_type,
                                technology_type.term if isinstance(technology_type, OntologyAnnotation)
                                else technology_type
                            ))
                            assay_to_expand = next(assay for assay in qc_study.assays
                                                   if assay.filename == assay_filename)
                            index = qc_study.assays.index(assay_to_expand)
                            samples_in_assay_to_expand = {
                                sample for process in assay_to_expand.process_sequence
                                for sample in process.inputs if type(sample) == Sample
                            }
                            log.debug('Number of input samples for assay {0} are {1}'.format(
                                assay_filename, len(samples_in_assay_to_expand)
                            ))
                            qc_sources, qc_samples_pre_run, qc_samples_interspersed, qc_samples_post_run, qc_processes \
                                = cls._generate_quality_control_samples(
                                    assay_graph.quality_control, cell, sample_size=len(samples_in_assay_to_expand),
                                    # FIXME? the assumption here is that the first protocol is the sampling protocol
                                    sampling_protocol=qc_study.protocols[0]
                            )
                            qc_study.sources += qc_sources
                            qc_study.samples.extend(qc_samples_pre_run + qc_samples_post_run)
                            for qc_samples in qc_samples_interspersed.values():
                                qc_study.samples.extend(qc_samples)
                            qc_study.process_sequence.extend(qc_processes)
                            augmented_samples = cls._augment_sample_batch_with_qc_samples(
                                samples_in_assay_to_expand, pre_run_samples=qc_samples_post_run,
                                post_run_samples=qc_samples_post_run,
                                interspersed_samples=qc_samples_interspersed
                            )
                            qc_study.assays[index] = StudyDesign.generate_assay(assay_graph, augmented_samples)
        return qc_study

    @staticmethod
    def _augment_sample_batch_with_qc_samples(samples, pre_run_samples=None, post_run_samples=None,
                                              interspersed_samples=None):
        """

        :param samples:
        :param pre_run_samples:
        :param post_run_samples:
        :param interspersed_samples:
        :return:
        """
        sorted_samples = sorted(samples, key=lambda s: s.name)
        assay_samples = [s for s in sorted_samples]  # this variable will contain all samples
        # pdb.set_trace()
        if interspersed_samples:
            for (qc_sample_node, interspersing_interval), qc_samples in interspersed_samples.items():
                for ix, qc_sample in enumerate(qc_samples):
                    index_to_insert = assay_samples.index(
                        sorted_samples[(ix + 1) * interspersing_interval])  # FIXME +1 or no ??
                    assay_samples.insert(index_to_insert, qc_sample)
        if pre_run_samples:
            assay_samples = pre_run_samples + assay_samples
        if post_run_samples:
            assay_samples = assay_samples + post_run_samples
        return assay_samples

    @staticmethod
    def _generate_quality_control_samples(quality_control, study_cell, sample_size=0,
                                          sampling_protocol=Protocol(), performer=None):
        """
        This method generates all the QC samples for a specific quality_control plan
        :param quality_control: A QualityControl object
        :param study_cell: The StudyCell to which the SampleAndAssayPlans belong
        :param sample_size:
        :param sampling_protocol:
        :param performer:
        :return:
        """
        log.debug("Quality control sample size = {0}".format(sample_size))
        qc_sources = []
        qc_samples_pre_run = []
        qc_samples_post_run = []
        qc_samples_interspersed = {}
        qc_processes = []
        if not isinstance(quality_control, QualityControl):
            raise TypeError()
        qc_pre = quality_control.pre_run_sample_type
        assert isinstance(qc_pre, ProductNode)
        cell_name = study_cell.name
        for i in range(qc_pre.size):
            dummy_source = QualityControlSource(
                name='SRC-QC-PRE-{}_{}_{}'.format(cell_name, SOURCE_QC_SOURCE_NAME, str(i).zfill(4))
            )
            qc_sources.append(dummy_source)
            sample = QualityControlSample(
                name='SMP-QC-PRE-{}_{}_{}'.format(cell_name, QC_SAMPLE_NAME, str(i).zfill(4)),
                factor_values=[],
                characteristics=[qc_pre.characteristics[i] if i < len(qc_pre.characteristics)
                                 else qc_pre.characteristics[-1]],
                derives_from=[dummy_source]
            )
            qc_samples_pre_run.append(sample)
            process = Process(
                executes_protocol=sampling_protocol, inputs=[dummy_source], outputs=[sample],
                performer=performer,
                date_=datetime.date.isoformat(datetime.date.today()),
                parameter_values=[
                    ParameterValue(
                        category=sampling_protocol.get_param(RUN_ORDER),
                        value=-1
                    ), ParameterValue(
                        category=sampling_protocol.get_param(STUDY_CELL),
                        value=str(study_cell.name)
                    )
                ]
            )
            qc_processes.append(process)
        log.debug("Completed pre-batch samples")
        for sample_node, interspersing_interval in quality_control.interspersed_sample_types:
            log.debug("sample node is {0}".format(sample_node))
            log.debug("interspersing interval is {0}, sample size is {1}".format(interspersing_interval, sample_size))
            qc_samples_interspersed[(sample_node, interspersing_interval)] = []
            for i in range(interspersing_interval, sample_size, interspersing_interval):
                dummy_source = QualityControlSource(
                    name='SRC-QC-INT-{}_{}_{}'.format(cell_name, SOURCE_QC_SOURCE_NAME, str(i).zfill(4))
                )
                qc_sources.append(dummy_source)
                sample = QualityControlSample(
                    name='SMP-QC-INT-{}_{}_{}'.format(cell_name, QC_SAMPLE_NAME, str(i).zfill(4)),
                    factor_values=[],
                    characteristics=sample_node.characteristics,
                    derives_from=[dummy_source],
                )
                qc_samples_interspersed[(sample_node, interspersing_interval)].append(sample)
        log.debug("Completed interspersed samples")
        qc_post = quality_control.post_run_sample_type
        assert isinstance(qc_post, ProductNode)
        for i in range(qc_post.size):
            dummy_source = QualityControlSource(
                name='SRC-QC-POST_{}_{}_{}'.format(cell_name, SOURCE_QC_SOURCE_NAME, str(i).zfill(4))
            )
            qc_sources.append(dummy_source)
            sample = QualityControlSample(
                name='SMP-QC-POST-{}_{}_{}'.format(cell_name, QC_SAMPLE_NAME, str(i).zfill(4)),
                factor_values=[],
                characteristics=[qc_post.characteristics if i < len(qc_post.characteristics)
                                 else qc_post.characteristics[-1]],
                derives_from=[dummy_source]
            )
            qc_samples_post_run.append(sample)
            process = Process(
                executes_protocol=sampling_protocol, inputs=[dummy_source], outputs=[sample],
                performer=performer,
                date_=datetime.date.isoformat(datetime.date.today()),
                parameter_values=[
                    ParameterValue(
                        category=sampling_protocol.get_param(RUN_ORDER),
                        value=-1
                    ), ParameterValue(
                        category=sampling_protocol.get_param(STUDY_CELL),
                        value=str(study_cell.name)
                    )
                ]
            )
            qc_processes.append(process)
            i += 1
        log.debug("Completed post-batch samples")
        return qc_sources, qc_samples_pre_run, qc_samples_interspersed, qc_samples_post_run, qc_processes


class StudyDesignEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, StudyDesign):
            arm_encoder = StudyArmEncoder()
            onto_encoder = OntologyAnnotationEncoder()
            study_arms_dict = {
                arm.name: arm_encoder.default(arm) for arm in obj.study_arms
            }
            # log.debug(study_arms_dict)
            for arm in study_arms_dict.values():
                arm.pop('name')
            return {
                'name': obj.name,
                'designType': onto_encoder.ontology_annotation(obj.design_type),
                'description': obj.description,
                'studyArms': study_arms_dict
            }


class StudyDesignDecoder(object):

    def __init__(self):
        self.arm_decoder = StudyArmDecoder()

    def loads(self, json_text):

        json_dict = json.loads(json_text)
        for name, arm_dict in json_dict["studyArms"].items():
            arm_dict['name'] = name
        study_arms = {self.arm_decoder.loads_arm(arm_dict) for arm_dict in json_dict["studyArms"].values()}

        study_design = StudyDesign(
            name=json_dict['name'],
            description=json_dict['description'],
            design_type=CharacteristicDecoder.loads_ontology_annotation(json_dict['designType']) if isinstance(
                json_dict['designType'], dict
            ) else json_dict['designType'],
            study_arms=study_arms
        )
        return study_design


class TreatmentFactory(object):
    """
      A factory class to build a set of Treatments given an intervention_type and a set of factors.
     """

    def __init__(self, intervention_type=INTERVENTIONS['CHEMICAL'],
                 factors=BASE_FACTORS):

        if intervention_type not in INTERVENTIONS.values():
            raise ValueError('invalid treatment type provided: ')

        self.__intervention_type = intervention_type
        self.__factors = OrderedDict([(factor, set()) for factor in factors])

    @property
    def intervention_type(self):
        return self.__intervention_type

    @property
    def factors(self):
        return self.__factors

    def add_factor_value(self, factor, factor_value):
        """
        Add a single factor value or a list of factor value to the relevant set
        :param factor: isatools.model.StudyFactor
        :param factor_value: string/list
        :return: None
        """
        if factor in self.factors:
            current_factors = self.factors.get(factor, set())
            if isinstance(factor_value, (str, Number)):
                current_factors.add(factor_value)
            elif isinstance(factor_value, Iterable):
                current_factors.update(factor_value)
        else:
            raise KeyError('The factor {} is not present in the design'.format(
                factor.name))

    def compute_full_factorial_design(self):
        """
        Computes the full factorial design on the basis of the stored factor and
        factor values. If one of the factors has no associated values an empty
        set is returned :return: set - the full factorial design as a set of
        Treatments
        """
        factor_values = [
            [FactorValue(
                factor_name=factor_name, value=value, unit=None
              ) for value in values]
            for factor_name, values in self.factors.items()
        ]
        if set() not in self.factors.values():
            return {Treatment(element_type=self.intervention_type, factor_values=treatment_factors)
                    for treatment_factors in itertools.product(*factor_values)}
        else:
            return set()


class StudyDesignFactory(object):
    """
      A factory class to build a set of study arms.
    """

    @staticmethod
    def _validate_maps(treatments_map, screen_map=None, run_in_map=None, washout_map=None, follow_up_map=None):
        """Validates Treatment and NonTreatment maps"""
        # TODO allow concomitant treatments as first element in a treatment map???
        if not isinstance(treatments_map, list):
            if not all(isinstance(el, tuple) for el in treatments_map):
                raise TypeError(errors.TREATMENT_MAP_ERROR)
        treatments, sample_plans = zip(*treatments_map)
        if not all(isinstance(treatment, Treatment) for treatment in treatments):
            raise TypeError(errors.TREATMENT_MAP_ERROR)
        if not all(isinstance(sample_plan, SampleAndAssayPlan) for sample_plan in sample_plans):
            raise TypeError(errors.TREATMENT_MAP_ERROR)
        for nt_map, nt_type in [(screen_map, SCREEN), (run_in_map, RUN_IN), (washout_map, WASHOUT),
                                (follow_up_map, FOLLOW_UP)]:
            if nt_map is None:
                continue
            if not isinstance(nt_map, tuple) or not isinstance(nt_map[0], NonTreatment) \
                    or not nt_map[0].type == nt_type or not (
                            nt_map[1] is None or isinstance(nt_map[1], SampleAndAssayPlan)):
                raise TypeError('Map for NonTreatment {0} is not correctly set.'.format(nt_type))

    @staticmethod
    def _validate_maps_multi_element_cell(treatments, sample_assay_plan, washout=None, screen_map=None,
                                          run_in_map=None, follow_up_map=None):
        """Validates Treatment and NonTreatment maps"""
        # TODO allow concomitant treatments as first element in a treatment map???
        if not isinstance(treatments, (list, tuple)) or \
                not all(isinstance(treatment, Treatment) for treatment in treatments):
            raise TypeError(errors.TREATMENT_MAP_ERROR)
        if not isinstance(sample_assay_plan, SampleAndAssayPlan):
            raise TypeError(errors.TREATMENT_MAP_ERROR)
        if washout and (not isinstance(washout, NonTreatment) or not washout.type == WASHOUT):
            raise TypeError('{0} is not a valid NonTreatment of type WASHOUT'.format(washout))
        for nt_map, nt_type in [(screen_map, SCREEN), (run_in_map, RUN_IN), (follow_up_map, FOLLOW_UP)]:
            if nt_map is None:
                continue
            if not isinstance(nt_map, tuple) or not isinstance(nt_map[0], NonTreatment) \
                    or not nt_map[0].type == nt_type or not (
                            nt_map[1] is None or isinstance(nt_map[1], SampleAndAssayPlan)):
                raise TypeError('Map for NonTreatment {0} is not correctly set.'.format(nt_type))

    @staticmethod
    def compute_crossover_design(treatments_map, group_sizes, screen_map=None, run_in_map=None,
                                 washout_map=None, follow_up_map=None):
        """
        Computes the crossover trial design on the basis of a number of
        treatments, each of them mapped to a SampleAndAssayPlans object. Optionally NonTreatments can be provided
        for SCREEN, RUN-IN, WASHOUT(s), and FOLLOW-UP
        :param treatments_map - a list containing tuples with pairs (Treatment, SampleAndAssayPlans/None).
        :param group_sizes - int/list The size(s) of the groups (i.e. number of subjects) for each study arm.
                                      If an integer is provided all the output arms will have the same group_size
                                      If a tuple/list of integers is provided its length must euqual T! where
                                      T is the number of Treatments in the treatment map
        :param screen_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type SCREEN
        :param run_in_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type RUN-IN
        :param washout_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type WASHOUT. A WASHOUT cell will be added between each pair of Treatment cell
        :param follow_up_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type FOLLOW-UP
        :return: StudyDesign - the crossover design. It contains T! study_arms, where T is the number of Treatments
                               provided in the treatment_map
        """
        if not isinstance(group_sizes, int):
            if not all(isinstance(el, int) for el in group_sizes) or \
                    not len(group_sizes) == factorial(len(treatments_map)):
                raise TypeError(errors.GROUP_SIZES_ERROR)
        StudyDesignFactory._validate_maps(treatments_map, screen_map, run_in_map, washout_map, follow_up_map)
        treatments, sample_plans = zip(*treatments_map)
        treatment_permutations = list(itertools.permutations(treatments))
        design = StudyDesign()
        for i, permutation in enumerate(treatment_permutations):
            counter = 0
            arm_map = []
            if screen_map:
                arm_map.append([StudyCell('ARM_{0}_CELL_{1}'.format(str(i).zfill(2), str(counter).zfill(2)),
                                          elements=[screen_map[0]]), screen_map[1]])
                counter += 1
            if run_in_map:
                arm_map.append([StudyCell('ARM_{0}_CELL_{1}'.format(str(i).zfill(2), str(counter).zfill(2)),
                                          elements=[run_in_map[0]]), run_in_map[1]])
                counter += 1
            for j, treatment in enumerate(permutation):
                sa_plan = next(el for el in treatments_map if el[0] == treatment)[1]
                arm_map.append([StudyCell('ARM_{0}_CELL_{1}'.format(str(i).zfill(2), str(counter).zfill(2)),
                                          elements=[treatment]), sa_plan])
                counter += 1
                if washout_map and j < len(permutation) - 1:  # do not add a washout after the last treatment cell
                    arm_map.append([StudyCell('ARM_{0}_CELL_{1}'.format(str(i).zfill(2), str(counter).zfill(2)),
                                              elements=[washout_map[0]]), washout_map[1]])
                    counter += 1
            if follow_up_map:
                arm_map.append([StudyCell('ARM_{0}_CELL_{1}'.format(str(i).zfill(2), str(counter).zfill(2)),
                                          elements=[follow_up_map[0]]), follow_up_map[1]])
            group_size = group_sizes if type(group_sizes) == int else group_sizes[i]
            arm = StudyArm('ARM_{0}'.format(str(i).zfill(2)), group_size=group_size, arm_map=OrderedDict(arm_map))
            design.add_study_arm(arm)
        return design

    @staticmethod
    def compute_parallel_design(treatments_map, group_sizes, screen_map=None, run_in_map=None,
                                washout_map=None, follow_up_map=None):
        """
        Computes the parallel trial design on the basis of a number of
        treatments, each of them mapped to a SampleAndAssayPlans object. Optionally NonTreatments can be provided
        for SCREEN, RUN-IN, WASHOUT(s), and FOLLOW-UP

        :param treatments_map - a list containing tuples with pairs (Treatment, SampleAndAssayPlans/None).
        :param group_sizes - int/list The size(s) of the groups (i.e. number of subjects) for each study arm.
                                      If an integer is provided all the output arms will have the same group_size
                                      If a tuple/list of integers is provided its length must equal T where
                                      T is the number of Treatments in the treatment map
        :param screen_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type SCREEN
        :param run_in_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type RUN-IN
        :param washout_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type WASHOUT. A WASHOUT cell will be added between each pair of Treatment cell
        :param follow_up_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type FOLLOW-UP
        :return: StudyDesign - the parallel design. It contains T study_arms, where T is the number of Treatments
                               provided in the treatment_map
        """
        if not isinstance(group_sizes, int):
            if not all(isinstance(el, int) for el in group_sizes) or not len(group_sizes) == len(treatments_map):
                raise TypeError(errors.GROUP_SIZES_ERROR)
        StudyDesignFactory._validate_maps(treatments_map, screen_map=screen_map, run_in_map=run_in_map,
                                          follow_up_map=follow_up_map)
        treatments, sample_plans = zip(*treatments_map)
        design = StudyDesign()
        for i, treatment in enumerate(treatments):
            counter = 0
            arm_map = []
            if screen_map:
                arm_map.append([StudyCell('ARM_{0}_CELL_{1}'.format(str(i).zfill(2), str(counter).zfill(2)),
                                          elements=[screen_map[0]]), screen_map[1]])
                counter += 1
            if run_in_map:
                arm_map.append([StudyCell('ARM_{0}_CELL_{1}'.format(str(i).zfill(2), str(counter).zfill(2)),
                                          elements=[run_in_map[0]]), run_in_map[1]])
                counter += 1
            arm_map.append([StudyCell('ARM_{0}_CELL_{1}'.format(str(i).zfill(2), str(counter).zfill(2)),
                                      elements=[treatment]), sample_plans[i]])
            counter += 1
            if follow_up_map:
                arm_map.append([StudyCell('ARM_{0}_CELL_{1}'.format(str(i).zfill(2), str(counter).zfill(2)),
                                          elements=[follow_up_map[0]]), follow_up_map[1]])
            group_size = group_sizes if type(group_sizes) == int else group_sizes[i]
            arm = StudyArm('ARM_{0}'.format(str(i).zfill(2)), group_size=group_size, arm_map=OrderedDict(arm_map))
            design.add_study_arm(arm)
        return design

    @staticmethod
    def compute_single_arm_design(treatments_map, group_size, screen_map=None, run_in_map=None,
                                  washout_map=None, follow_up_map=None):
        """
        Computes the single arm trial design on the basis of a number of
        treatments, each of them mapped to a SampleAndAssayPlans object. Optionally NonTreatments can be provided
        for SCREEN, RUN-IN, WASHOUT(s), and FOLLOW-UP

        :param treatments_map - a list containing tuples with pairs (Treatment, SampleAndAssayPlans/None).
        :param group_size - int The size of the group of the study arm.
        :param screen_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type SCREEN
        :param run_in_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type RUN-IN
        :param washout_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type WASHOUT. A WASHOUT cell will be added between each pair of Treatment cell
        :param follow_up_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type FOLLOW-UP
        :return: StudyDesign - the single arm design. As the name surmises, it contains 1 study arm
        """
        if not isinstance(group_size, int):
            raise TypeError(errors.GROUP_SIZES_ERROR)
        StudyDesignFactory._validate_maps(treatments_map, screen_map=screen_map, run_in_map=run_in_map,
                                          washout_map=washout_map, follow_up_map=follow_up_map)
        treatments, sample_plans = zip(*treatments_map)
        design = StudyDesign()
        counter = 0
        arm_map = []
        if screen_map:
            arm_map.append([StudyCell('ARM_00_CELL_{0}'.format(str(counter).zfill(2)),
                                      elements=[screen_map[0]]), screen_map[1]])
            counter += 1
        if run_in_map:
            arm_map.append([StudyCell('ARM_00_CELL_{0}'.format(str(counter).zfill(2)),
                                      elements=[run_in_map[0]]), run_in_map[1]])
            counter += 1
        for j, treatment in enumerate(treatments):
            sa_plan = next(el for el in treatments_map if el[0] == treatment)[1]
            arm_map.append([StudyCell('ARM_00_CELL_{0}'.format(str(counter).zfill(2)),
                                      elements=[treatment]), sa_plan])
            counter += 1
            if washout_map and j < len(treatments) - 1:  # do not add a washout after the last treatment cell
                arm_map.append([StudyCell('ARM_00_CELL_{0}'.format(str(counter).zfill(2)),
                                          elements=[washout_map[0]]), washout_map[1]])
                counter += 1
        if follow_up_map:
            arm_map.append([StudyCell('ARM_00_CELL_{0}'.format(str(counter).zfill(2)),
                                      elements=[follow_up_map[0]]), follow_up_map[1]])
        arm = StudyArm('ARM_00', group_size=group_size, arm_map=OrderedDict(arm_map))
        design.add_study_arm(arm)
        return design

    @staticmethod
    def compute_concomitant_treatments_design(treatments, sample_assay_plan, group_size, screen_map=None,
                                              run_in_map=None, follow_up_map=None):
        """
        Computes a study design with only one treatment cell. All treatments provided as input are considered
        concomitant within that cell
        :param treatments - a list containing Treatment(s).
        :param sample_assay_plan - SampleAndAssayPlans. This sample+assay plan will be applied to the multi-element
                                   cell built from the treatments provided a the first parameter
        :param group_size - int The size of the group of the study arm.
        :param screen_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type SCREEN
        :param run_in_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type RUN-IN 
        :param follow_up_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type FOLLOW-UP
        :return: StudyDesign - the single arm design. It contains 1 study arm
        """
        if not isinstance(group_size, int):
            raise TypeError(errors.GROUP_SIZES_ERROR)
        StudyDesignFactory._validate_maps_multi_element_cell(treatments, sample_assay_plan, screen_map=screen_map,
                                                             run_in_map=run_in_map, follow_up_map=follow_up_map)
        design = StudyDesign()
        counter = 0
        arm_map = []
        if screen_map:
            arm_map.append([StudyCell('ARM_00_CELL_{0}'.format(str(counter).zfill(2)),
                                      elements=[screen_map[0]]), screen_map[1]])
            counter += 1
        if run_in_map:
            arm_map.append([StudyCell('ARM_00_CELL_{0}'.format(str(counter).zfill(2)),
                                      elements=[run_in_map[0]]), run_in_map[1]])
            counter += 1
        concomitant_treatments = set(treatments)
        arm_map.append([StudyCell('ARM_00_CELL_{0}'.format(str(counter).zfill(2)), elements=[concomitant_treatments]),
                        sample_assay_plan])
        counter += 1
        if follow_up_map:
            arm_map.append([StudyCell('ARM_00_CELL_{0}'.format(str(counter).zfill(2)),
                                      elements=[follow_up_map[0]]), follow_up_map[1]])
        arm = StudyArm('ARM_00', group_size=group_size, arm_map=OrderedDict(arm_map))
        design.add_study_arm(arm)
        return design

    @staticmethod
    def compute_crossover_design_multi_element_cell(treatments, sample_assay_plan, group_sizes, washout=None,
                                                    screen_map=None, run_in_map=None, follow_up_map=None):
        """
        Computes the crossover trial design on the basis of a number of
        treatments, each of them mapped to a SampleAndAssayPlans object. Optionally NonTreatments can be provided
        for SCREEN, RUN-IN, WASHOUT(s), and FOLLOW-UP

        :param treatments - a list containing Treatment(s).
        :param sample_assay_plan - SampleAndAssayPlans. This sample+assay plan will be applied to the multi-element
                                   cell built from the treatments provided a the first parameter
        :param group_sizes - int/list The size(s) of the groups (i.e. number of subjects) for each study arm.
                                      If an integer is provided all the output arms will have the same group_size
                                      If a tuple/list of integers is provided its length must euqual T! where
                                      T is the number of Treatments in the treatment map
        :param washout - NonTreatment. The NonTreatment must be of type WASHOUT. 
                         A WASHOUT cell will be added between each pair of Treatment cell
        :param screen_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type SCREEN
        :param run_in_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type RUN-IN
        :param follow_up_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type FOLLOW-UP
        :return: StudyDesign - the crossover design. It contains T! study_arms, where T is the number of Treatments
                               provided in the treatment_map
        """
        if not isinstance(group_sizes, int):
            if not all(isinstance(el, int) for el in group_sizes) or \
                    not len(group_sizes) == factorial(len(treatments)):
                raise TypeError(errors.GROUP_SIZES_ERROR)
        StudyDesignFactory._validate_maps_multi_element_cell(treatments, sample_assay_plan, washout, screen_map,
                                                             run_in_map, follow_up_map)
        treatment_permutations = list(itertools.permutations(treatments))
        design = StudyDesign()
        for i, permutation in enumerate(treatment_permutations):
            counter = 0
            arm_map = []
            if screen_map:
                arm_map.append([StudyCell('ARM_{0}_CELL_{1}'.format(str(i).zfill(2), str(counter).zfill(2)),
                                          elements=[screen_map[0]]), screen_map[1]])
                counter += 1
            if run_in_map:
                arm_map.append([StudyCell('ARM_{0}_CELL_{1}'.format(str(i).zfill(2), str(counter).zfill(2)),
                                          elements=[run_in_map[0]]), run_in_map[1]])
                counter += 1
            multi_element_cell = StudyCell('ARM_{0}_CELL_{1}'.format(str(i).zfill(2), str(counter).zfill(2)),
                                           elements=intersperse(permutation, washout) if washout else permutation)
            arm_map.append([multi_element_cell, sample_assay_plan])
            counter += 1
            if follow_up_map:
                arm_map.append([StudyCell('ARM_{0}_CELL_{1}'.format(str(i).zfill(2), str(counter).zfill(2)),
                                          elements=[follow_up_map[0]]), follow_up_map[1]])
            group_size = group_sizes if type(group_sizes) == int else group_sizes[i]
            arm = StudyArm('ARM_{0}'.format(str(i).zfill(2)), group_size=group_size, arm_map=OrderedDict(arm_map))
            design.add_study_arm(arm)
        return design

    @staticmethod
    def compute_single_arm_design_multi_element_cell(treatments, sample_assay_plan, group_size, washout=None,
                                                     screen_map=None, run_in_map=None, follow_up_map=None):
        """
        Computes the single arm trial design on the basis of a number of
        treatments, each of them mapped to a SampleAndAssayPlans object. Optionally NonTreatments can be provided
        for SCREEN, RUN-IN, WASHOUT(s), and FOLLOW-UP

        :param treatments - a list containing Treatments.
        :param sample_assay_plan - SampleAndAssayPlans. This sample+assay plan will be applied to the multi-element
                                   cell built from the treatments provided a the first parameter
        :param group_size - int The size of the group of the study arm.
        :param washout - NonTreatment. The NonTreatment must be of type WASHOUT. 
                         A WASHOUT cell will be added between each pair of Treatment cell
        :param screen_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type SCREEN
        :param run_in_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type RUN-IN 
        :param follow_up_map - a tuple containing the pair (NonTreatment, SampleAndAssayPlans/None). The NonTreatment
                            must be of type FOLLOW-UP
        :return: StudyDesign - the single arm design. As the name surmises, it contains 1 study arm
        """
        if not isinstance(group_size, int):
            raise TypeError(errors.GROUP_SIZES_ERROR)
        StudyDesignFactory._validate_maps_multi_element_cell(treatments, sample_assay_plan, washout, screen_map,
                                                             run_in_map, follow_up_map)
        design = StudyDesign()
        counter = 0
        arm_map = []
        if screen_map:
            arm_map.append([StudyCell('ARM_00_CELL_{0}'.format(str(counter).zfill(2)),
                                      elements=[screen_map[0]]), screen_map[1]])
            counter += 1
        if run_in_map:
            arm_map.append([StudyCell('ARM_00_CELL_{0}'.format(str(counter).zfill(2)),
                                      elements=[run_in_map[0]]), run_in_map[1]])
            counter += 1
        multi_element_cell = StudyCell('ARM_00_CELL_{0}'.format(str(counter).zfill(2)),
                                       elements=intersperse(treatments, washout) if washout else treatments)
        arm_map.append([multi_element_cell, sample_assay_plan])
        counter += 1
        if follow_up_map:
            arm_map.append([StudyCell('ARM_00_CELL_{0}'.format(str(counter).zfill(2)),
                                      elements=[follow_up_map[0]]), follow_up_map[1]])
        arm = StudyArm('ARM_00', group_size=group_size, arm_map=OrderedDict(arm_map))
        design.add_study_arm(arm)
        return design
