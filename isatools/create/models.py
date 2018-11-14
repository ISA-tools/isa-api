"""
Model objects for storing study design settings, for consumption by
function or factory to create ISA model objects.
"""
from __future__ import absolute_import
import datetime
import itertools
import json
import random
from collections import Iterable
from collections import OrderedDict
from numbers import Number
import copy
from isatools.model import *
from isatools.errors import *
from abc import ABC, abstractmethod
import inspect
import pdb



log = logging.getLogger('isatools')

__author__ = 'massi'

# NON TREATMENT TYPES
SCREEN = 'screen'
RUN_IN = 'run in'
WASHOUT = 'washout'
FOLLOW_UP = 'follow-up'

ELEMENT_TYPES = dict(SCREEN=SCREEN, RUN_IN=RUN_IN, WASHOUT=WASHOUT, FOLLOW_UP=FOLLOW_UP)

INTERVENTIONS = dict(CHEMICAL='chemical intervention',
                     BEHAVIOURAL='behavioural intervention',
                     SURGICAL='surgical intervention',
                     BIOLOGICAL='biological intervention',
                     RADIOLOGICAL='radiological intervention',
                     DIET='dietary intervention')

FACTOR_TYPES = dict(AGENT_VALUES='agent values',
                    INTENSITY_VALUES='intensity values',
                    DURATION_VALUES='duration values')

DURATION_FACTOR_ = dict(name='DURATION', type=OntologyAnnotation(term="time"),
                        display_singular='DURATION VALUE',
                        display_plural='DURATION VALUES', values=set())

DURATION_FACTOR = StudyFactor(name=DURATION_FACTOR_['name'], factor_type=DURATION_FACTOR_.get('type', None))

BASE_FACTORS_ = [
    dict(
        name='AGENT', type=OntologyAnnotation(term="perturbation agent"),
        display_singular='AGENT VALUE',
        display_plural='AGENT VALUES', values=set()
    ),
    dict(
        name='INTENSITY', type=OntologyAnnotation(term="intensity"),
        display_singular='INTENSITY VALUE',
        display_plural='INTENSITY VALUES', values=set()
    ),
    DURATION_FACTOR_
]

BASE_FACTORS = [
    StudyFactor(name=BASE_FACTORS_[0]['name'],
                factor_type=BASE_FACTORS_[0].get('type', None)),
    StudyFactor(name=BASE_FACTORS_[1]['name'],
                factor_type=BASE_FACTORS_[1].get('type', None)),
    DURATION_FACTOR,
]


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


class NonTreatment(Element):

    def __init__(self, element_type=ELEMENT_TYPES['SCREEN'], duration_value=0.0, duration_unit=None):
        super(NonTreatment, self).__init__()
        if element_type not in ELEMENT_TYPES.values():
            raise ValueError('element treatment type provided: ')
        self.__type = element_type
        if not isinstance(duration_value, Number):
            raise ValueError('duration_value must be a Number. Value provided is {0}'.format(duration_value))
        self.__duration = FactorValue(factor_name=DURATION_FACTOR, value=duration_value, unit=duration_unit)

    def __repr__(self):
        return 'isatools.create.models.NonTreatment(type={0}, duration={1})'.format(repr(self.type), repr(self.duration))

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
        if element_type in INTERVENTIONS.values():
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
    A Treatment is defined as a tuple of factor values (as defined in the ISA
    model v1) and a treatment type
    A Treatment is an extension of the basic Element
    """
    def __init__(self, treatment_type=INTERVENTIONS['CHEMICAL'],
                 factor_values=None, group_size=0):
        """
        Creates a new Treatment
        :param treatment_type: treatment type
        :param factor_values: set of isatools.model.v1.FactorValue
        :param group_size: number of subjects in this group
        """
        super(Treatment, self).__init__()
        if treatment_type not in INTERVENTIONS.values():
            raise ValueError('invalid treatment type provided: ')

        self.__type = treatment_type

        if factor_values is None:
            self.__factor_values = set()
        else:
            self.factor_values = factor_values
        self.__group_size = group_size
    
    def __repr__(self):
        return 'isatools.create.models.Treatment(type={0}, factor_values={1}, ' \
               'group_size={2})'.format(self.type, sorted(
                self.factor_values, key=lambda x: repr(x)), self.group_size)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Treatment) \
               and self.type == other.type \
               and self.factor_values == other.factor_values \
               and self.group_size == other.group_size

    def __ne__(self, other):
        return not self == other

    # TODO move group_size to StudyArm
    @property
    def group_size(self):
        return self.__group_size

    @group_size.setter
    def group_size(self, group_size):
        if not isinstance(group_size, int):
            raise TypeError('{} is not a valid value for group_size. Please '
                            'provide an integer.'.format(group_size))
        if group_size < 0:
            raise ValueError('group_size must be greater than 0.')
        self.__group_size = group_size

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
        if isinstance(factor_values, tuple) \
                and all([isinstance(factor_value, FactorValue)
                         for factor_value in factor_values]):
            self.__factor_values = factor_values
        else:
            raise TypeError('Data supplied is not correctly formatted for '
                            'Treatment')

    @property
    def duration(self):
        return next(factor_value for factor_value in self.factor_values
                    if factor_value.factor_name == DURATION_FACTOR)


class StudyCell(object):
    """
    A StudyCell consists of a set of Elements who can be Treatment or NonTreatment Elements
    Under the current design all elements in a a cell are intended to be concomitant
    PROBLEM: what if different elements within a cell have different durations?
    ANSWER: this must not be allowed
    PROBLEM: only allow concomitant treatments: concomitant non-treatments make no sense
    """

    def __init__(self, name, elements=None):
        self.__name = name if isinstance(name, str) else None   # FIXME can we allow name to be none?
        self.__elements = list()
        if elements is not None:
            self.elements = elements

    def __repr__(self):
        return 'isatools.create.models.StudyCell(' \
               'name={name}, ' \
               'elements={elements}, ' \
               ')'.format(name=self.name, elements=repr(self.elements))

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
            raise ISAModelAttributeError('Epoch name must be a string')
        self.__name = name

    @property
    def elements(self):
        return self.__elements

    @elements.setter
    def elements(self, x):
        if not isinstance(x, (Element, list, tuple)):
            raise ISAModelAttributeError('elements must be an Element, a list of Elements, or a tuple of Elements')
        self.__elements.clear()
        try:
            if isinstance(x, Element):
                self.insert_element(x)
            else:
                for element in x:
                    self.insert_element(element)
        except ISAModelValueError as e:
            raise ISAModelAttributeError(e)

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
            SCREEN: check_screen,
            RUN_IN: check_run_in,
            WASHOUT: check_washout,
            FOLLOW_UP: check_follow_up
        }
        func = switcher.get(new_element.type, lambda: False)
        # lines = inspect.getsource(func)
        # print('Element type: {element_type} \nfunc: {func}'.format(element_type=new_element.type, func=lines))
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
        - Run-in NonTreatments must either be in a 1-element StudyCell or in a 2-element if preceeded by a Screen
        - A Follow-up NonTreatment must be in a 1-element StudyCell
        - Rest NonTreatments cannot be chained one after the other
        - Concomitant Treatments (if provided in a set) must have the same duration 
        :return: 
        """
        index = len(self.elements) if not isinstance(element_index, int) else \
            element_index if abs(element_index) < len(self.elements) else len(self.elements)
        if not isinstance(element, (Element, set)):
            raise ISAModelValueError('element must be either an Element or a set of treatments')
        is_valid = self._non_treatment_check(self.elements, element, index) if isinstance(element, NonTreatment) else \
            self._treatment_check(self.elements) if isinstance(element, Treatment) else \
            self._concomitant_treatments_check(element) if isinstance(element, set) else False
        if is_valid:
            self.__elements.insert(index, element)
        else:
            raise ISAModelValueError('Element is not valid')

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
    def duration(self):
        # TODO recompute as sum of durations
        pass
        """
        element = next(iter(self.elements))
        return next(factor_value for factor_value in element.factor_values
                    if factor_value.factor_name == DURATION_FACTOR)
        """


class StudyArm(object):
    """
    Each study Arm is constituted by a mapping (ordered dict?) StudyCell -> SampleAssayPlan
    We call this mapping arm_map
    """

    SCREEN_ERROR_MESSAGE = 'A SCREEN cell can only be inserted into an empty arm_map.'
    RUN_IN_ERROR_MESSAGE = 'A RUN-IN cell can only be inserted into an arm_map containing a SCREEN.'
    WASHOUT_ERROR_MESSAGE = 'A WASHOUT cell cannot be put next to a cell ending with a WASHOUT.'
    COMPLETE_ARM_ERROR_MESSAGE = 'StudyArm complete. No more cells can be added after a FOLLOW-UP cell.'
    FOLLOW_UP_ERROR_MESSAGE = 'A FOLLOW-UP cell cannot be put next to a SCREEN or a RUN-IN cell.'
    FOLLOW_UP_EMPTY_ARM_ERROR_MESSAGE = 'A FOLLOW-UP cell cannot be put into an empty StudyArm.'

    ARM_MAP_ASSIGNMENT_ERROR = 'arm_map must be an OrderedDict'

    def __init__(self, name, arm_map=None, group_size=0):
        self.name = name
        self.__group_size = None
        self.__arm_map = OrderedDict()
        self.group_size = group_size
        if arm_map is not None:
            self.arm_map = arm_map

    def __repr__(self):
        return 'isatools.create.models.StudyArm(' \
               'name={name}, ' \
               'group_size={group_size}, ' \
               'cells={cells}, ' \
               'sample_assay_plans={sample_assay_plans})'.format(name=self.name, group_size=self.group_size,
                                                                 cells=self.cells,
                                                                 sample_assay_plans=self.sample_assay_plans)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, StudyArm) and self.name == other.name and self.group_size == other.group_size and \
               self.arm_map == other.arm_map

    def __ne__(self, other):
        return not self == other

    @property
    def group_size(self):
        return self.__group_size

    @group_size.setter
    def group_size(self, group_size):
        if isinstance(group_size, int) and group_size >= 0:
            self.__group_size = group_size
        else:
            raise ISAModelAttributeError('group_size must be a positive integer; {0} provided'.format(group_size))

    @property
    def arm_map(self):
        return self.__arm_map or OrderedDict()

    @arm_map.setter
    def arm_map(self, arm_map):
        if not isinstance(arm_map, OrderedDict):
            raise ISAModelAttributeError(self.ARM_MAP_ASSIGNMENT_ERROR)
        self.__arm_map.clear()
        try:
            for cell, sample_assay_plan in arm_map.items():
                self.add_item_to_arm_map(cell, sample_assay_plan)
        except ISAModelValueError as ve:
            raise ISAModelAttributeError(ve.args[0])

    @property
    def cells(self):
        return list(self.arm_map.keys())

    @property
    def sample_assay_plans(self):
        return list(self.arm_map.values())

    def is_completed(self):
        """
        A StudyArm is considered completed if it contains a FOLLOW-UP cells
        :return: bool
        """
        return bool([el for cell in self.arm_map.keys() for el in cell.get_all_elements()
                     if el.type == FOLLOW_UP])

    def add_item_to_arm_map(self, cell, sample_assay_plan=None):
        """
        inserts a mapping StudyCell -> SampleAssayPlan to the StudyArm arm_map
        There are a few insertion rules for cells
        - To insert a cell containing a SCREEN the arm_map *must* be empty
        - To insert a cell containing a RUN-IN alone the arm_map *must* contain a SCREEN-only cell and no other cells
        - To insert a cell containing one or more Treatments (and washouts) the arm_map must not contain a FOLLOW-UP 
            cell. Moreover if the cell contains a WASHOUT we must ensure that the previous cell does not contain a 
            NonTreatment of any type as the latest element
        - To insert a cell containing a FOLLOW-UP the arm_map *must not* contain already a FOLLOW-UP cell
            Moreover, this cell cannot be inserted immediately afer a SCREEN or a RUN-IN cell
        :param cell: (StudyCell)
        :param sample_assay_plan: (SampleAssayPlan/None) 
        :return: 
        """
        if not isinstance(cell, StudyCell):
            raise TypeError('{0} is not a StudyCell object'.format(cell))
        if sample_assay_plan is not None and not isinstance(sample_assay_plan, SampleAssayPlan):
            raise TypeError('{0} is not a SampleAssayPlan object'.format(sample_assay_plan))
        if self.is_completed():
            raise ISAModelValueError(self.COMPLETE_ARM_ERROR_MESSAGE)
        if cell.contains_non_treatment_element_by_type(SCREEN):
            if len(self.arm_map.keys()):
                raise ISAModelValueError(self.SCREEN_ERROR_MESSAGE)
            self.__arm_map[cell] = sample_assay_plan
        elif cell.contains_non_treatment_element_by_type(RUN_IN):
            previous_cells = list(self.arm_map.keys())
            if len(previous_cells) == 1 and previous_cells[0].contains_non_treatment_element_by_type(SCREEN):
                self.__arm_map[cell] = sample_assay_plan
            else:
                raise ISAModelValueError(self.RUN_IN_ERROR_MESSAGE)
        elif cell.contains_non_treatment_element_by_type(WASHOUT) and cell.get_all_elements()[0].type == WASHOUT:
            latest_cell = list(self.arm_map.keys())[-1]
            latest_element = latest_cell.get_all_elements()[-1]
            if isinstance(latest_element, NonTreatment):
                raise ISAModelValueError(self.WASHOUT_ERROR_MESSAGE)
        elif cell.contains_non_treatment_element_by_type(FOLLOW_UP):
            previous_cells = list(self.arm_map.keys())
            if not len(previous_cells):
                raise ISAModelValueError(self.FOLLOW_UP_EMPTY_ARM_ERROR_MESSAGE)
            latest_cell = list(self.arm_map.keys())[-1]
            if latest_cell.contains_non_treatment_element_by_type(SCREEN) or \
                    latest_cell.contains_non_treatment_element_by_type(RUN_IN):
                raise ISAModelValueError(self.FOLLOW_UP_ERROR_MESSAGE)
        self.__arm_map[cell] = sample_assay_plan

    @property
    def treatments(self):
        """
        Returns all the Treatment elements contained in a StudyArm
        :return set - all the treatments in the StudyArm
        """
        # TODO should this be a set or a list or something else?
        return {elem for cell in self.arm_map.keys() for elem in cell.get_all_elements() if isinstance(elem, Treatment)}


class StudyDesign(object):

    NAME_PROPERTY_ASSIGNMENT_ERROR = 'The value assigned to \'name\' must be a sting'
    STUDY_ARM_PROPERTY_ASSIGNMENT_ERROR = 'The value assigned to \'study_arms\' must be an iterable'
    ADD_STUDY_ARM_PARAMETER_TYPE_ERROR = 'Not a valid study arm'
    ADD_STUDY_ARM_NAME_ALREADY_PRESENT_ERROR = 'A StudyArm with the same name is already present in the StudyDesign'

    """
    A class representing a study design, which is composed of a collection of
    study arms.
    StudyArms of different lengths (i.e. different number of cells) are allowed.
    """

    def __init__(self, name='Study Design', study_arms=None):
        """
        
        :param study_arms: Iterable
        """
        self.__study_arms = set()
        self.__name = name if isinstance(name, str) else 'Study Design'
        if study_arms:
            self.study_arms = study_arms

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise ISAModelAttributeError(self.NAME_PROPERTY_ASSIGNMENT_ERROR)
        self.__name = name

    @property
    def study_arms(self):
        return sorted(self.__study_arms, key=lambda arm: arm.name)

    @study_arms.setter
    def study_arms(self, study_arms):
        if not isinstance(study_arms, Iterable):
            raise ISAModelAttributeError(self.STUDY_ARM_PROPERTY_ASSIGNMENT_ERROR)
        try:
            for arm in study_arms:
                self.add_study_arm(arm)
        except (ISAModelTypeError, ISAModelValueError) as e:
            raise ISAModelAttributeError(e.args[0])

    def add_study_arm(self, study_arm):
        """
        add a StudyArm object to the study_arm set. 
        Arms of diff 
        :param study_arm: StudyArm
        """
        if not isinstance(study_arm, StudyArm):
            raise ISAModelTypeError('{0}: {1}'.format(self.ADD_STUDY_ARM_PARAMETER_TYPE_ERROR, study_arm))
        if any({arm for arm in self.study_arms if arm.name == study_arm.name}):
            raise ISAModelValueError('{0}'.format(self.ADD_STUDY_ARM_NAME_ALREADY_PRESENT_ERROR))
        self.__study_arms.add(study_arm)

    @property
    def treatments(self):
        treatment_set = set()
        return treatment_set

    def __repr__(self):
        return 'isatools.create.models.StudyDesign(' \
               'name={name}, ' \
               'study_arms={study_arms}' \
               ')'.format(study_arms=self.study_arms, name=self.name)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, StudyDesign) and self.name == other.name and self.study_arms == other.study_arms

    def __ne__(self, other):
        return not self == other


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
            [ FactorValue(
                factor_name=factor_name, value=value, unit=None
              ) for value in values]
            for factor_name, values in self.factors.items()
        ]
        if set() not in self.factors.values():
            return { Treatment(treatment_type=self.intervention_type,
                              factor_values=treatment_factors)
                    for treatment_factors in itertools.product(*factor_values)}
        else:
            return set()


class AssayType(object):
    """
       A type of assay, determined by a measurement_type, a technology_type and a set of topology_modifiers 
       (of type AssayTopologyModifiers).
    """

    def __init__(self, measurement_type=None, technology_type=None,
                 topology_modifiers=None):
        if isinstance(measurement_type, OntologyAnnotation):
            self.__measurement_type = measurement_type
        elif isinstance(measurement_type, str):
            self.__measurement_type = OntologyAnnotation(term=measurement_type)
        elif measurement_type is None:
            self.__measurement_type = None
        else:
            raise TypeError('{0} is an invalid value for measurement_type. '
                            'Please provide an OntologyAnnotation or string.'
                            .format(measurement_type))

        if isinstance(technology_type, OntologyAnnotation):
            self.__technology_type = technology_type
        elif isinstance(technology_type, str):
            self.__technology_type = OntologyAnnotation(term=technology_type)
        elif technology_type is None:
            self.__technology_type = None
        else:
            raise TypeError('{0} is an invalid value for technology_type. '
                            'Please provide an OntologyAnnotation or string.'
                            .format(technology_type))

        if isinstance(topology_modifiers, (NMRTopologyModifiers,
                                           MSTopologyModifiers,
                                           GenericAssayTopologyModifiers)):
            self.__topology_modifiers = topology_modifiers
        elif topology_modifiers is None:
            self.__topology_modifiers = None
        else:
            raise TypeError('{0} is an invalid value for topology_modifiers. '
                            'Please provide a supported AssayTopologyModifiers '
                            'object (currently NMR or MS).'
                            .format(topology_modifiers))

    @property
    def measurement_type(self):
        return self.__measurement_type

    @measurement_type.setter
    def measurement_type(self, measurement_type):
        if isinstance(measurement_type, OntologyAnnotation):
            self.__measurement_type = measurement_type
        elif isinstance(measurement_type, str):
            self.__measurement_type = OntologyAnnotation(term=measurement_type)
        elif measurement_type is None:
            self.__measurement_type = None
        else:
            raise TypeError('{0} is an invalid value for measurement_type. '
                            'Please provide an OntologyAnnotation or string.'
                            .format(measurement_type))

    @property
    def technology_type(self):
        return self.__technology_type

    @technology_type.setter
    def technology_type(self, technology_type):
        if isinstance(technology_type, OntologyAnnotation):
            self.__technology_type = technology_type
        elif isinstance(technology_type, str):
            self.__technology_type = OntologyAnnotation(term=technology_type)
        elif technology_type is None:
            self.__technology_type = None
        else:
            raise TypeError('{0} is an invalid value for technology_type. '
                            'Please provide an OntologyAnnotation or string.'
                            .format(technology_type))

    @property
    def topology_modifiers(self):
        return self.__topology_modifiers

    @topology_modifiers.setter
    def topology_modifiers(self, topology_modifiers):
        if isinstance(topology_modifiers, (NMRTopologyModifiers,
                                           MSTopologyModifiers,
                                           GenericAssayTopologyModifiers)):
            self.__topology_modifiers = topology_modifiers
        elif topology_modifiers is None:
            self.__topology_modifiers = None
        else:
            raise TypeError('{0} is an invalid value for measurement_type. '
                            'Please provide a supported AssayTopologyModifiers '
                            'object (currently NMR or MS or Generic).'
                            .format(topology_modifiers))

    def __repr__(self):
        return 'AssayType(measurement_type={0}, technology_type={1}, ' \
               'topology_modifiers={2})' \
               .format(repr(self.measurement_type), repr(self.technology_type),
                       self.topology_modifiers)

    def __hash__(self):
        return hash(repr(self))

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return isinstance(other, AssayType) \
               and self.measurement_type == other.measurement_type \
               and self.technology_type == other.technology_type


class GenericAssayTopologyModifiers(object):

    def __init__(self, technical_replicates=1, instruments=None):
        self.__technical_replicates = technical_replicates
        if instruments is None:  # scanning instruments
            self.__instruments = set()
        else:
            self.instruments = instruments

    @property
    def technical_replicates(self):
        return self.__technical_replicates

    @technical_replicates.setter
    def technical_replicates(self, val):
        if not isinstance(val, int):
            raise TypeError('{0} is an invalid value for technical_replicates. '
                            'Please provide an integer.')
        if val < 1:
            raise ValueError('technical_replicates must be greater than 0.')
        self.__technical_replicates = val

    @property
    def instruments(self):
        return self.__instruments

    @instruments.setter
    def instruments(self, val):
        if not isinstance(val, set):
            raise TypeError('{0} is an invalid value for instruments. '
                            'Please provide an set of string.'.format(val))
        if not all(isinstance(x, str) for x in val):
            raise ValueError('all instruments need to be of type string')
        self.__instruments = val


class NMRTopologyModifiers(GenericAssayTopologyModifiers):

    def __init__(self, acquisition_modes=None,
                 pulse_sequences=None, technical_replicates=1,
                 instruments=None, injection_modes=None, magnet_power=None):
        super().__init__(technical_replicates=technical_replicates,
                         instruments=instruments)
        if pulse_sequences is None:
            self.__pulse_sequences = set()
        else:
            self.pulse_sequences = pulse_sequences
        if injection_modes is None:
            self.__injection_modes = set()
        else:
            self.injection_modes = injection_modes
        if acquisition_modes is None:
            self.__acquisition_modes = set()
        else:
            self.acquisition_modes = acquisition_modes
        self.magnet_power = magnet_power

    @property
    def pulse_sequences(self):
        return self.__pulse_sequences

    @pulse_sequences.setter
    def pulse_sequences(self, val):
        if not isinstance(val, set):
            raise TypeError('{0} is an invalid value for pulse_sequences. '
                            'Please provide an set of string.')
        if not all(isinstance(x, str) for x in val):
            raise ValueError('all pulse sequences need to be of type string')
        self.__pulse_sequences = val

    @property
    def injection_modes(self):
        return self.__injection_modes

    @injection_modes.setter
    def injection_modes(self, val):
        injection_mode_values = ('FIA', 'GC', 'LC')
        if not isinstance(val, set):
            raise TypeError('{0} is an invalid value for injection_modes. '
                            'Please provide an set of string.')
        if not all(isinstance(x, str) for x in val):
            raise ValueError('all injection modes need to be of type string')
        if not all(x in injection_mode_values for x in val):
            raise ValueError('injection modes must be one of {}'.format(
                injection_mode_values))
        self.__injection_modes = val

    @property
    def acquisition_modes(self):
        return self.__acquisition_modes

    @acquisition_modes.setter
    def acquisition_modes(self, val):
        if not isinstance(val, set):
            raise TypeError('{0} is an invalid value for acquisition_modes. '
                            'Please provide an set of string.')
        if not all(isinstance(x, str) for x in val):
            raise ValueError('all acquisition modes need to be of type string')
        self.__acquisition_modes = val

    def __repr__(self):
        return 'NMRTopologyModifiers(' \
               'acquisition_modes={0}, ' \
               'pulse_sequences={1}, ' \
               'technical_replicates={2}, ' \
               'instruments={3}, injection_modes={4})'.format(
                sorted(self.acquisition_modes),
                sorted(self.pulse_sequences),
                self.technical_replicates,
                sorted(self.instruments),
                sorted(self.acquisition_modes)
                )

    def __hash__(self):
        return hash(repr(self))

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return isinstance(other, NMRTopologyModifiers) \
               and self.injection_modes == other.injection_modes \
               and self.acquisition_modes == other.acquisition_modes \
               and self.pulse_sequences == other.pulse_sequences \
               and self.technical_replicates == other.technical_replicates \
               and self.instruments == other.instruments


class MSAcquisitionMode(object):

    def __init__(self, acquisition_method, technical_repeats=1):
        self.__acquisition_method = acquisition_method
        self.__technical_repeats = technical_repeats

    @property
    def acquisition_method(self):
        return self.__acquisition_method

    @acquisition_method.setter
    def acquisition_method(self, val):
        if val not in ('positive', 'negative', 'positive/negative'):
            raise ValueError('Acquisition method must be one of positive, '
                             'negative or positive/negative')
        self.__acquisition_method = val

    @property
    def technical_repeats(self):
        return self.__technical_repeats

    @technical_repeats.setter
    def technical_repeats(self, val):
        if not isinstance(val, int):
            raise ValueError('Technical repeats must be specified in integer'
                             'numbers')
        self.__technical_repeats = val


    def __repr__(self):
        return 'MSAcquisitionMode(' \
               'acquisition_method={acquisition_method}, ' \
               'technical_repeats={technical_repeats})'.format(
                acquisition_method=self.acquisition_method,
                technical_repeats=self.technical_repeats)


class MSInjectionMode(object):

    def __init__(self, injection_mode='DI',
                 chromatography_instrument='none reported',
                 chromatography_column='none reported',
                 acquisition_modes=None, ms_instrument=None,
                 derivatizations=None):
        self.injection_mode = injection_mode
        self.__chromatography_instrument = chromatography_instrument
        self.__chromatography_column = chromatography_column
        if injection_mode in ('GC', 'LC'):
            self.chromatography_instrument = chromatography_instrument
        else:
            self.__chromatography_column = None
        if self.injection_mode in ('LC'):
            self.chromatography_column = chromatography_column
        else:
            self.__chromatography_column = None
        if acquisition_modes is None:
            self.__acquisition_modes = set()
        else:
            self.__acquisition_modes = acquisition_modes
        if ms_instrument is None:
            self.__ms_instrument = None
        else:
            self.__ms_instrument = ms_instrument
        if injection_mode in ('GC') and derivatizations:
            self.__derivatizations = derivatizations
        else:
            self.__derivatizations = set()

    @property
    def injection_mode(self):
        return self.__injection_mode

    @injection_mode.setter
    def injection_mode(self, val):
        if val not in ('FIA', 'GC', 'LC', 'DI'):
            raise TypeError('{0} is an invalid value for injection_modes. '
                            'Please provide one of FIA, GC, LC, or DI.')
        self.__injection_mode = val

    @property
    def ms_instrument(self):
        return self.__ms_instrument

    @ms_instrument.setter
    def ms_instrument(self, val):
        self.__ms_instrument = val

    @property
    def chromatography_instrument(self):
        if self.injection_mode in ('GC', 'LC'):
            return self.__chromatography_instrument

    @chromatography_instrument.setter
    def chromatography_instrument(self, val):
        if self.injection_mode not in ('GC', 'LC'):
            raise ValueError('Cannot set chromatography instrument if '
                             'injection mode is not GC or LC')
        self.__chromatography_instrument = val

    @property
    def chromatography_column(self):
        if self.injection_mode in ('LC'):
            return self.__chromatography_column

    @chromatography_column.setter
    def chromatography_column(self, val):
        if self.injection_mode not in ('LC'):
            raise ValueError('Cannot set chromatography column if '
                             'injection mode is not LC')
        self.__chromatography_column = val

    @property
    def acquisition_modes(self):
        return self.__acquisition_modes

    @acquisition_modes.setter
    def acquisition_modes(self, val):
        if not isinstance(val, set):
            raise TypeError('{0} is an invalid value for acquisition_modes. '
                            'Please provide an set of '
                            'MSAcquisitionMode.')
        if not all(isinstance(x, MSAcquisitionMode) for x in val):
            raise ValueError('Acquisition modes must be of type '
                             'MSAcquisitionMode')
        self.__acquisition_modes.add(val)

    @property
    def derivatizations(self):
        return self.__derivatizations

    @derivatizations.setter
    def derivatizations(self, val):
        if not isinstance(val, set):
            raise TypeError('{0} is an invalid value for derivatizations. '
                            'Please provide an set of string.')
        if not all(isinstance(x, str) for x in val):
            raise ValueError('All derivatizations  must be of string')
        self.__derivatizations.add(val)

    def __repr__(self):
        return 'MSInjectionMode(' \
               'injection_mode={injection_mode}, ' \
               'ms_instrument={ms_instrument}, ' \
               'chromatography_instrument={chromatography_instrument}, ' \
               'chromatography_column={chromatography_column}, ' \
               'acquisition_modes={acquisition_modes}, ' \
               'derivatizations={derivatizations})'.format(
                injection_mode=self.injection_mode,
                ms_instrument=self.ms_instrument,
                chromatography_instrument=self.chromatography_instrument,
                chromatography_column=self.chromatography_column,
                acquisition_modes=list(self.acquisition_modes),
                derivatizations=list(self.derivatizations)
        )


class MSTopologyModifiers(object):

    def __init__(self, sample_fractions=None,
                 injection_modes=None):
        if sample_fractions is None:
            self.__sample_fractions = set()
        else:
            self.sample_fractions = sample_fractions
        if injection_modes is None:
            self.__injection_modes = set()
        else:
            self.injection_modes = injection_modes

    @property
    def sample_fractions(self):
        return self.__sample_fractions

    @sample_fractions.setter
    def sample_fractions(self, val):
        if not isinstance(val, set):
            raise TypeError('{0} is an invalid value for sample_fractions. '
                            'Please provide an set of polar or non-polar.'
                            .format(val))
        if not all(x in ('polar', 'non-polar') for x in val):
            raise ValueError('all acquisition modes need to be one of polar or'
                             'non-polar')
        self.__sample_fractions = val

    @property
    def injection_modes(self):
        return self.__injection_modes

    @injection_modes.setter
    def injection_modes(self, val):
        if not isinstance(val, set):
            raise TypeError('{0} is an invalid value for injection_modes. '
                            'Please provide an set of MSInjectionMode.')
        if not all(isinstance(x, MSInjectionMode) for x in val):
            raise ValueError(
                'all injection modes need to be of type MSInjectionMode')
        self.__injection_modes = val

    def __repr__(self):
        return 'MSTopologyModifiers(' \
               'sample_fractions={num_sample_fractions}, ' \
               'injection_modes={num_injection_modes})'.format(
                num_sample_fractions=sorted(self.sample_fractions),
                num_injection_modes=list(self.injection_modes))

    def __hash__(self):
        return hash(repr(self))

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return isinstance(other, MSTopologyModifiers) \
               and self.injection_modes == other.injection_modes \
               and self.sample_fractions == other.sample_fractions


class DNASeqAssayTopologyModifiers(GenericAssayTopologyModifiers):

    def __init__(self, distinct_libraries=0, technical_replicates=1,
                 instruments=None):
        super().__init__(technical_replicates=technical_replicates,
                         instruments=instruments)
        self.__distinct_libraries = distinct_libraries

    @property
    def distinct_libraries(self):
        return self.__distinct_libraries

    @distinct_libraries.setter
    def distinct_libraries(self, distinct_libraries):
        if not isinstance(distinct_libraries, int):
            raise TypeError('{0} is an invalid value for distinct_libraries. '
                            'Please provide an integer.')
        if distinct_libraries < 0:
            raise ValueError('distinct_libraries must be greater than 0.')
        self.__distinct_libraries = distinct_libraries

    def __repr__(self):
        return 'DNASeqAssayTopologyModifiers(' \
               'technical_replicates={0}, ' \
               'instruments={1}, distinct_libraries={2})'.format(
                self.technical_replicates,
                sorted(self.instruments),
                self.distinct_libraries
                )

    def __hash__(self):
        return hash(repr(self))

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return isinstance(other, DNASeqAssayTopologyModifiers) \
               and self.technical_replicates == other.technical_replicates \
               and self.instruments == other.instruments \
               and self.distinct_libraries == other.distinct_libraries


class DNAMicroAssayTopologyModifiers(GenericAssayTopologyModifiers):

    def __init__(self, array_designs=None, technical_replicates=1):
        super().__init__(technical_replicates=technical_replicates)
        if array_designs is None:
            self.__array_designs = set()
        else:
            self.array_designs = array_designs

    @property
    def instruments(self):
        raise NotImplementedError(
            'instruments property not implemented for DNA Microarray topology '
            'modifiers')

    @property
    def array_designs(self):
        return self.__array_designs

    @array_designs.setter
    def array_designs(self, val):
        if not isinstance(val, set):
            raise TypeError('{0} is an invalid value for array_designs. '
                            'Please provide an set of string.')
        if not all(isinstance(x, str) for x in val):
            raise ValueError('all array designs need to be of type string')
        self.__array_designs = val

    def __repr__(self):
        return 'DNAMicroAssayTopologyModifiers(' \
               'technical_replicates={0}, array_designs={1})'.format(
                self.technical_replicates, sorted(self.array_designs))

    def __hash__(self):
        return hash(repr(self))

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return isinstance(other, DNAMicroAssayTopologyModifiers) \
               and self.technical_replicates == other.technical_replicates \
               and self.array_designs == other.array_designs


class SampleAssayPlan(object):
    """
    A class representing the sampling plan and the assay plan.
    """

    def __init__(self, group_size=0, sample_plan=None, assay_plan=None,
                 sample_qc_plan=None):
        self.__group_size = 0
        self.__sample_types = set()
        self.__assay_types = set()
        self.group_size = group_size
        if sample_plan is None:
            self.__sample_plan = {}
        else:
            self.sample_types = {key for key in sample_plan}
            self.sample_plan = sample_plan
        if assay_plan is None:
            self.__assay_plan = set()
        else:
            self.assay_types = {value for key, value in assay_plan}
            self.assay_plan = assay_plan
        if sample_qc_plan is None:
            self.__sample_qc_plan = {}
        else:
            for k, v in assay_plan:
                self.assay_types.add(v)
            self.__sample_qc_plan = sample_qc_plan
        self.__pre_run_batch = None
        self.__post_run_batch = None

    @property
    def group_size(self):
        return self.__group_size

    @group_size.setter
    def group_size(self, group_size):
        if not isinstance(group_size, int):
            raise TypeError('{} is not a valid value for group_size. Please '
                            'provide an integer.'.format(group_size))
        if group_size < 0:
            raise ValueError('group_size must be greater than 0.')
        self.__group_size = group_size

    def add_sample_type(self, sample_type):
        if isinstance(sample_type, Characteristic):
            self.__sample_types.add(sample_type)
        elif isinstance(sample_type, OntologyAnnotation):
            characteristic = Characteristic(
                category=OntologyAnnotation(term='organism part'),
                value=sample_type)
            self.__sample_types.add(characteristic)
        elif isinstance(sample_type, str):
            characteristic = Characteristic(
                category=OntologyAnnotation(term='organism part'),
                value=OntologyAnnotation(term=sample_type))
            self.__sample_types.add(characteristic)
        else:
            raise TypeError('Not a valid sample type: {0}'.format(sample_type))

    def add_sample_qc_plan_record(self, material_type, injection_interval):
        """
        :param material_type: (Characteristic/str) a sample type of QC material
        :param injection_interval: (int) for the provided sample type how
            often in the run order a QC sampling event should occur.
        :return:
        """
        if isinstance(material_type, str):
            material_type = Characteristic(
                category=OntologyAnnotation(term='Material Type'),
                value=OntologyAnnotation(term=material_type))
        elif isinstance(material_type, OntologyAnnotation):
            material_type = Characteristic(
                category=OntologyAnnotation(term='Material Type'),
                value=material_type)
        elif not material_type.category.term == 'Material Type':
            raise TypeError('invalid characteristic for QC material type: {0}'
                            .format(material_type))
        if not isinstance(injection_interval, int):
            raise TypeError('injection_interval must be a natural number')
        if isinstance(injection_interval, int) and injection_interval < 0:
            raise ValueError('injection_interval value must be a positive integer')
        self.__sample_qc_plan[material_type] = injection_interval

    @property
    def sample_types(self):
        return self.__sample_types

    @sample_types.setter
    def sample_types(self, sample_types):
        if not isinstance(sample_types, Iterable):
            raise TypeError('wrong sample types: {0}'.format(sample_types))
        for sample_type in sample_types:
            self.add_sample_type(sample_type)

    def add_assay_type(self, assay_type):
        if isinstance(assay_type, AssayType):
            self.__assay_types.add(assay_type)
        elif isinstance(assay_type, str):
            assay_type = AssayType(measurement_type=assay_type)
            self.__assay_types.add(assay_type)
        else:
            raise TypeError('Not a valid assay type: {0}'.format(assay_type))

    @property
    def assay_types(self):
        return self.__assay_types

    @assay_types.setter
    def assay_types(self, assay_types):
        for assay_type in assay_types:
            self.add_assay_type(assay_type)

    def add_sample_plan_record(self, sample_type, sampling_size=0):
        """
        :param sample_type: (Characteristic/OntologyAnnotation/str) a sample type
        :param sampling_size: (int/tuple of int) for the provided sample type
            how many sampling events happen for a single source/subject. This
            can be specified throughout the whole sequence with a single
            integer value, or with a tuple of value, each value for an
            epoch. Missing values will be considered as zero (no sampling).
        :return: 
        """
        if isinstance(sample_type, str):
            if sample_type not in [x.value.term for x in self.sample_types]:
                raise TypeError(
                    'nonexistent sample type: {0}'.format(sample_type))
            sample_type = next(x for x in self.sample_types if x.value.term
                               == sample_type)
        elif isinstance(sample_type, OntologyAnnotation):
            if sample_type not in [x.value for x in self.sample_types]:
                raise TypeError(
                    'nonexistent sample type: {0}'.format(sample_type))
            sample_type = next(x for x in self.sample_types if x.value.term
                               == sample_type.term)
        elif sample_type not in self.sample_types:
            raise TypeError('nonexistent sample type: {0}'.format(sample_type))
        if not isinstance(sampling_size, int) \
                and not isinstance(sampling_size, tuple):
            raise TypeError('sampling_size must be a natural number or a tuple '
                            'of natural numbers')
        if isinstance(sampling_size, int) and sampling_size < 0:
            raise ValueError('sampling_size value must be a positive integer')
        if isinstance(sampling_size, tuple) \
                and not all(isinstance(el, int)
                            and el >= 0 for el in sampling_size):
            raise ValueError('all values in the sampling_size tuple must be '
                             'positive integers')
        self.__sample_plan[sample_type] = sampling_size

    @property
    def sample_plan(self):
        return self.__sample_plan

    @sample_plan.setter
    def sample_plan(self, sample_plan):
        for sample_type, sampling_size in sample_plan.items():
            self.add_sample_plan_record(sample_type, sampling_size)

    def add_assay_plan_record(self, sample_type, assay_type):
        if isinstance(sample_type, str):
            sample_type = Characteristic(category=OntologyAnnotation(
                term='organism part'), value=OntologyAnnotation(
                term=sample_type))
        elif isinstance(sample_type, OntologyAnnotation):
            if sample_type not in [x.value for x in self.sample_types]:
                raise TypeError(
                    'nonexistent sample type: {0}'.format(sample_type))
            sample_type = next(x for x in self.sample_types if x.value.term
                               == sample_type.term)
        if sample_type not in self.sample_types:
            raise ValueError('nonexistent sample type: {0}. These are the '
                             'available sample types: {1}'
                             .format(sample_type, self.sample_types))
        if isinstance(assay_type, str):
            assay_type = AssayType(measurement_type=assay_type)
        if assay_type.measurement_type not in \
                [x.measurement_type for x in self.assay_types]:
            raise ValueError('nonexistent assay type: {0}. These are the assay '
                             'types available in the plan: {1}'
                             .format(assay_type, self.assay_types))
        self.__assay_plan.add((sample_type, assay_type))

    @property
    def assay_plan(self):
        return self.__assay_plan

    @assay_plan.setter
    def assay_plan(self, assay_plan):
        if not isinstance(assay_plan, set):
            raise TypeError('Assay plan must be a set of (SampleType, '
                            'AssayType)')
        for sample_type, assay_type in assay_plan:
            self.add_assay_plan_record(sample_type, assay_type)

    @property
    def sample_qc_plan(self):
        return self.__sample_qc_plan

    @sample_qc_plan.setter
    def sample_qc_plan(self, val):
        for sample_type, injection_interval in val.items():
            self.add_sample_qc_plan_record(sample_type, injection_interval)

    @property
    def pre_run_batch(self):
        return self.__pre_run_batch

    @pre_run_batch.setter
    def pre_run_batch(self, qc_batch):
        if not isinstance(qc_batch, SampleQCBatch):
            raise TypeError('QC batch must be of type SampleQCBatch')
        self.__pre_run_batch = qc_batch
        
    @property
    def post_run_batch(self):
        return self.__post_run_batch

    @post_run_batch.setter
    def post_run_batch(self, qc_batch):
        if not isinstance(qc_batch, SampleQCBatch):
            raise TypeError('QC batch must be of type SampleQCBatch')
        self.__post_run_batch = qc_batch

    def __repr__(self):
        return 'isatools.create.models.SampleAssayPlan(' \
               'group_size={sample_assay_plan.group_size}, ' \
               'sample_plan={sample_plan}, assay_plan={assay_plan}, ' \
               'sample_qc_plan={sample_qc_plan})'.format(
                sample_assay_plan=self,
                sample_plan=set(map(lambda x: x, self.sample_plan)),
                assay_plan=set(map(lambda x: x, self.assay_plan)),
                sample_qc_plan=set(map(lambda x: x, self.sample_qc_plan)))

    def __eq__(self, other):
        return hash(repr(self)) == hash(repr(other))

    def __ne__(self, other):
        return hash(repr(self)) != hash(repr(other))


class SampleQCBatch(object):

    def __init__(self, material=None, parameter_values=None,
                 characteristic_values=None):
        self.material = material
        if parameter_values is None:
            self.parameter_values = []
        else:
            self.parameter_values = parameter_values
        if characteristic_values is None:
            self.characteristic_values = []
        else:
            self.characteristic_values = characteristic_values


class StudyDesignFactory(object):
    """
      A factory class to build a set of study arms.
    """

    # TODO: Add screen epoch
    # TODO: Add follow up epoch
    # TODO: Add Rest/washout epochs?

    def __init__(self, treatments, sample_plan):
        self.__treatments = treatments
        self.__sample_plan = sample_plan

    @property
    def treatments(self):
        return self.__treatments

    @property
    def sample_plan(self):
        return self.__sample_plan

    def compute_crossover_design(self, screen=False, follow_up=False):
        """
        Computes the crossover trial design on the basis of the set of
        treatments and either a single sample plan uniformly applied at each
        treatment or an ordered set of sample plans that matches the number of
        treatments (otherwise raises an error).

        :return: set - the crossover design as a set of StudyArms
        """
        if set() not in self.treatments:
            return [
            StudyArm(name='arm_{i}'.format(i=i),
                     epochs=[StudyCell(
                         name='epoch_{j}'.format(j=j), rank=j, elements=[y],
                         sample_plan=self.sample_plan) for j, y
                             in enumerate(x)]) for i, x in
                enumerate(itertools.product(self.treatments))
            ]
        else:
            return set()

    def compute_parallel_design(self, num_arms=2, screen=False, follow_up=False):
        """
        Computes the parallel trial design on the basis of the set of
        treatments and either a single sample plan uniformly applied at each
        treatment or an ordered set of sample plans that matches the number of
        treatments (otherwise raises an error).

        :return: set - the parallel design as a set of StudyArms
        """
        if set() not in self.treatments:
            study_arms = []
            for _ in range(0, num_arms):
                arm = self.compute_single_arm_design()[-1]
                arm.name = 'arm_{}'.format(_)
                study_arms.append(arm)
            # rank_before_tmin = min(x.rank for x in next(iter(study_arms))) - 1
            # rank_after_tmax = max(x.rank for x in next(iter(study_arms))) + 1
            # for arm in study_arms:
            #     if screen:
            #         arm.add(StudyCell(name='screen',
            #                            rank=rank_before_tmin,
            #                            sample_plan=self.sample_plan))
            #     if follow_up:
            #         arm.add(StudyCell(name='follow_up',
            #                            rank=rank_after_tmax,
            #                            sample_plan=self.sample_plan))
            return study_arms
        else:
            return set()

    def compute_single_arm_design(self, screen=False, follow_up=False):
        """
        Computes the single arm design on the basis of the set of
        treatments and either a single sample plan uniformly applied at each
        treatment or an ordered set of sample plans that matches the number of
        treatments (otherwise raises an error).

        :return: set - the single arm design as a set of StudyArms
        """
        if len(set([x.group_size for x in self.treatments])) != 1:
           raise ValueError('Group size for all treatments must be the same if '
                            'computing a single-arm design. Found {}'.format(
               set([x.group_size for x in self.treatments])))
        if set() not in self.treatments:
            arm = StudyArm(name='arm_0')
            arm.epochs = [
                StudyCell(name='epoch_{i}'.format(i=i), rank=i, elements=[x],
                          sample_plan=self.sample_plan)
                for i, x in enumerate(self.treatments)]
            return [arm]
        else:
            return set()

    def compute_single_epoch_design(self, screen=False, follow_up=False):
        """
        Computes the single arm design on the basis of the set of
        treatments and either a single sample plan uniformly applied at each
        treatment or an ordered set of sample plans that matches the number of
        treatments (otherwise raises an error).

        :return: set - the single arm design as a set of StudyArms
        """
        if len(set([x.group_size for x in self.treatments])) != 1:
           raise ValueError('Group size for all treatments must be the same if '
                            'computing a single-arm design. Found {}'.format(
               set([x.group_size for x in self.treatments])))
        if set() not in self.treatments:
            arms = []
            for i, treatment_group in enumerate(self.treatments):
                arm = StudyArm(name='arm_{}'.format(i))
                arm.epochs = [
                    StudyCell(name='epoch_{i}'.format(i=0), rank=0,
                              elements=[treatment_group],
                              sample_plan=self.sample_plan)]
                arms.append(arm)
            return arms
        else:
            return set()


class IsaModelObjectFactory(object):
    """
    A factory class to create ISA content given a StudyDesign object.
    """

    def __init__(self, study_design):
        self.__study_design = study_design
        self.__ops = ['Alice', 'Bob', 'Carol', 'Dan', 'Erin', 'Frank']
        random.shuffle(self.__ops)

    def _idgen(self, gid='', subn='', samn='', samt=''):
        idarr = []
        if gid != '':
            idarr.append('Group-{}'.format(gid))  # study group
        if subn != '':
            idarr.append('Subject-{}'.format(subn))
        if samt != '':
            idarr.append(samt)
        if samn != '':
            idarr.append('{}'.format(samn))
        return '.'.join(idarr)

    @property
    def ops(self):
        """Shuffles every time it is called, so use it once in context if you
        want to preserve the current order"""
        return self.__ops

    @property
    def study_design(self):
        return self.__study_design

    @study_design.setter
    def study_design(self, study_design):
        if not isinstance(study_design, StudyDesign):
            raise ISAModelAttributeError(
                'study_design must be an object of type StudyDesign')
        else:
            self.__study_design = study_design

    def create_study_from_plan(self):
        # FIXME remove all the refernces to a TreatmentSequence.
        # FIXME This method will need refactoring anyway (massi 17/10/2018)

        study_arm = self.study_design.study_arms  # only get first arm for now

        study = Study(filename='s_study_arm01.txt')
        # set default declarations in study
        study.ontology_source_references  = [
            OntologySource(name='OBI',
                           file='https://raw.githubusercontent.com/obi-ontology'
                                '/obi/v2018-02-12/obi.owl',
                           version='v2018-02-12',
                           description='Ontology for Biomedical Investigations')
        ]
        study.protocols = [
            Protocol(name='sample collection', protocol_type=
                OntologyAnnotation(term='sample collection'))
        ]

        sample_collection = study.get_prot('sample collection')
        sample_collection.add_param('run order')
        sample_collection.add_param('collection event rank')

        source_prototype = Source(
            characteristics=[
                Characteristic(
                    category=OntologyAnnotation(term='Material Type'),
                    value=OntologyAnnotation(
                        term='specimen',
                        term_source=study.ontology_source_references[0],
                        term_accession='0100051'))
            ]
        )

        def generate_sources(arms):
            sources_map = dict()
            for arm in arms:
                sources = set()
                for epoch in arm.epochs:
                    for subjn in (str(x).zfill(3) for x in
                                  range(1, epoch.sample_plan.group_size + 1)):
                        source = copy.copy(source_prototype)
                        source.name = self._idgen(arm.name, subjn)
                        sources.add(source)
                    sources_map[arm.name] = list(sources)
            return sources_map

        sources_map = generate_sources(self.study_design.study_arms)
        for x in sources_map.values():
            for y in x:
                study.sources.append(y)

        # create the main batch first
        factors = set()
        ontology_sources = set()
        samples = []
        sample_count = 0
        process_sequence = []
        param_run_order = sample_collection.get_param('run order')
        for arm in self.study_design.study_arms:  # each arm set Group
            group_id = arm.name
            group_sources = sources_map[arm.name]
            for epoch in arm.epochs:  # each epoch is a rank in group
                epoch_name = epoch.name
                rank = epoch.rank
                sample_plan = epoch.sample_plan
                for treatment in epoch.elements:
                    fvs = treatment.factor_values
                    for factor in [x.factor_name for x in fvs]:
                        factors.add(factor)
                    for source in group_sources:
                        for sample_type, sampling_size in \
                                sample_plan.sample_plan.items():
                            if sample_type.value.term_source:
                                ontology_sources.add(
                                    sample_type.value.term_source)
                            sampc = 0
                            for sampn in range(0, sampling_size):
                                sampc += 1
                                # normal sample collection
                                sample = Sample(name=self._idgen(
                                    group_id, source.name, str(sampc),
                                    sample_type.value.term),
                                    factor_values=fvs)
                                sample.characteristics = [sample_type]
                                sample.derives_from = [source]
                                samples.append(sample)
                                sample_count += 1
                                process = Process(
                                    executes_protocol=sample_collection,
                                    inputs=[source], outputs=[sample],
                                    performer=self.ops[0], date_=
                                    datetime.date.isoformat(
                                        datetime.date.today()),
                                    parameter_values=[ParameterValue(
                                        category=param_run_order,
                                        value=str(sample_count).zfill(3))])
                                process.parameter_values.append(
                                    ParameterValue(
                                        category=sample_collection.get_param(
                                            'collection event rank'),
                                        value=str(rank)))
                                process_sequence.append(process)
        study.characteristic_categories = list(
            set(study.characteristic_categories))
        study.samples = samples
        study.process_sequence = process_sequence
        study.factors = list(factors)
        study.ontology_source_references = list(ontology_sources)

        return study
        #  insert_qcs()
        # FIXME
        treatment_sequence, sample_assay_plan = \
            self.study_design.sequences_plan.popitem()
        self.sample_assay_plan = sample_assay_plan

        if sample_assay_plan is None:
            raise ISAModelAttributeError('sample_assay_plan must be set to '
                                         'create model objects in factory')

        # if sample_assay_plan.group_size < 1:
        #     raise ISAModelAttributeError('group_size cannot be less than 1')
        # group_size = sample_assay_plan.group_size

        if sample_assay_plan.sample_plan == {}:
            raise ISAModelAttributeError('sample_plan is not defined')
        sample_plan = sample_assay_plan.sample_plan
        ranked_treatment_set = set()
        for x, _ in treatment_sequence.ranked_treatments: #FIXME
            ranked_treatment_set.add(x)
        groups_ids = [
            (str(i+1).zfill(3), x) for i, x in enumerate(ranked_treatment_set)]
        ranks = set([y for _, y in treatment_sequence.ranked_treatments]) #FIXME

        group_rank_map = dict()
        for group_id, rank in itertools.product(groups_ids, ranks):
            if group_id not in group_rank_map.keys():
                group_rank_map[group_id] = set()
            group_rank_map[group_id].add(rank)
        sources = []
        samples = []
        process_sequence = []
        study = Study(filename='study.txt')
        sample_collection = Protocol(name='sample collection',
                                     protocol_type=OntologyAnnotation(
                                         term='sample collection'))
        sample_collection.add_param('run order')
        sample_collection.add_param('collection event rank')
        param_run_order = sample_collection.get_param('run order')
        study.protocols = [sample_collection]

        sample_count = 0
        qc_param_set = set()

        sample_qc_plan = sample_assay_plan
        prebatch = sample_qc_plan.pre_run_batch
        factors = set()
        ontology_sources = set()
        if isinstance(prebatch, SampleQCBatch):
            for i, c in enumerate(prebatch.characteristic_values):
                var_characteristic = c.category
                qcsource = Source(
                    name='QC.{}.{}'.format(prebatch.material.term,
                                           str(i + 1).zfill(3)),
                    characteristics=[
                        Characteristic(
                            category=OntologyAnnotation(term='Material Type'),
                            value=prebatch.material),
                            Characteristic(category=var_characteristic,
                                           value=c.value)
                    ])
                if var_characteristic not in study.characteristic_categories:
                    study.characteristic_categories.append(var_characteristic)
                sources.append(qcsource)
                if not prebatch.parameter_values:
                    sample = Sample(name=qcsource.name)
                    process = Process(executes_protocol=study.get_prot(
                        'sample collection'), inputs=[qcsource],
                        outputs=[sample], performer=self.ops[0], date_=
                        datetime.date.isoformat(
                            datetime.date.today()))
                    process.parameter_values = [
                        ParameterValue(category=param_run_order, value=-1)
                    ]
                    samples.append(sample)
                    process_sequence.append(process)
                else:
                    for j, (p, v) in enumerate(prebatch.parameter_values):
                        qc_param_set.add(p)
                        sample = Sample(name=qcsource.name)
                        qc_param = sample_collection.get_param(p)
                        if qc_param is None:
                            sample_collection.add_param(p)
                        process = Process(executes_protocol=study.get_prot(
                            'sample collection'), inputs=[qcsource],
                            outputs=[sample], performer=self.ops[0], date_=
                            datetime.date.isoformat(
                                datetime.date.today()))
                        process.parameter_values = [
                            ParameterValue(
                                category=param_run_order, value=-1),
                            ParameterValue(
                                category=sample_collection.get_param(p),
                                value=v),
                        ]
                        samples.append(sample)
                        process_sequence.append(process)
            if not prebatch.parameter_values:
                qcsource = Source(name='QC.{}'.format(prebatch.material.term), characteristics=[
                    Characteristic(
                        category=OntologyAnnotation(term='Material Type'),
                        value=prebatch.material)])
                sources.append(qcsource)
                for i, (p, v) in enumerate(prebatch.parameter_values):
                    qc_param_set.add(p)
                    sample = Sample(name='QC.{}.{}'.format(prebatch.material.term, str(i+1).zfill(3)))
                    qc_param = sample_collection.get_param(p)
                    if qc_param is None:
                        sample_collection.add_param(p)
                    process = Process(executes_protocol=study.get_prot(
                        'sample collection'), inputs=[qcsource],
                        outputs=[sample], performer=self.ops[0], date_=
                        datetime.date.isoformat(
                            datetime.date.today()))
                    process.parameter_values=[
                        ParameterValue(
                            category=param_run_order, value=-1),
                        ParameterValue(category=sample_collection.get_param(p),
                                       value=v),
                    ]
                    samples.append(sample)
                    process_sequence.append(process)
        # Main batch
        for (group_id, treatment), ranks in group_rank_map.items():
            fvs = treatment.factor_values
            group_size = treatment.group_size
            for factor in [x.factor_name for x in fvs]:
                factors.add(factor)
            for subjn in (str(x).zfill(3) for x in range(1, group_size+1)):
                obi = OntologySource(name='OBI')
                ontology_sources.add(obi)
                material_type = Characteristic(
                    category=OntologyAnnotation(term='Material Type'),
                    value=OntologyAnnotation(term='specimen',
                                             term_source=obi,
                                             term_accession='0100051'))
                source = Source(name=self._idgen(group_id, subjn))
                source.characteristics = [material_type]

                if prebatch is not None:
                    if prebatch.characteristic_values is not None:
                        c = next(iter(prebatch.characteristic_values))
                        var_characteristic = c.category
                        source.characteristics.append(Characteristic(
                            category=var_characteristic))
                if sample_qc_plan.post_run_batch is not None:
                    if sample_qc_plan.post_run_batch.characteristic_values is not None:
                        if len(sample_qc_plan.post_run_batch.characteristic_values) > 0:
                            c = next(iter(sample_qc_plan.post_run_batch.characteristic_values))
                            var_characteristic = c.category
                            source.characteristics.append(Characteristic(
                                category=var_characteristic))
                sources.append(source)
                for sample_type, sampling_size in sample_plan.items():
                    if sample_type.value.term_source:
                        ontology_sources.add(sample_type.value.term_source)
                    sampc = 0
                    for rank in ranks:
                        for sampn in range(0, sampling_size):
                            sampc += 1
                            for qc_material_type in sample_assay_plan \
                                    .sample_qc_plan.keys():
                                if sample_count % sample_assay_plan \
                                        .sample_qc_plan[qc_material_type] == 0:
                                    # insert QC sample collection
                                    qcsource = Source(
                                        name=self._idgen(group_id, subjn) + '_QC')
                                    qcsource.characteristics = [qc_material_type]
                                    sources.append(qcsource)
                                    sample = Sample(
                                        name=self._idgen(
                                            group_id, subjn,
                                            'QC', qc_material_type.value.term))
                                    sample.derives_from = [qcsource]
                                    samples.append(sample)
                                    process = Process(
                                        executes_protocol=sample_collection,
                                        inputs=[qcsource],
                                        outputs=[sample], performer=self.ops[0],
                                        date_=datetime.date.isoformat(
                                            datetime.date.today()))
                                    process.parameter_values.append(
                                        ParameterValue(
                                            category=param_run_order, value=str(
                                                sample_count+1).zfill(3)))
                                    process_sequence.append(process)
                            # normal sample collection
                            sample = Sample(name=self._idgen(
                                group_id, subjn, str(sampc), sample_type.value.term),
                                factor_values=fvs)
                            sample.characteristics = [sample_type]
                            sample.derives_from = [source]
                            samples.append(sample)
                            sample_count += 1
                            process = Process(executes_protocol=sample_collection,
                                              inputs=[source], outputs=[sample],
                                              performer=self.ops[0], date_=
                                datetime.date.isoformat(datetime.date.today()),
                            parameter_values=[ParameterValue(
                                category=param_run_order,
                                value=str(sample_count).zfill(3))])
                            process.parameter_values.append(
                                ParameterValue(
                                    category=sample_collection.get_param(
                                        'collection event rank'),
                                    value=str(rank)))
                            process_sequence.append(process)
        postbatch = sample_qc_plan.post_run_batch
        if isinstance(postbatch, SampleQCBatch):
            if not postbatch.characteristic_values:
                qcsource = Source(name='source_QC', characteristics=[
                    Characteristic(
                        category=OntologyAnnotation(term='Material Type'),
                        value=postbatch.material)])
                sources.append(qcsource)
            else:
                for i, c in enumerate(postbatch.characteristic_values):
                    var_characteristic = c.category
                    qcsource = Source(
                        name='QC.{}.{}'.format(
                            postbatch.material.term, str(i + 1).zfill(3)),
                        characteristics=[
                            Characteristic(
                                category=OntologyAnnotation(
                                    term='Material Type'),
                                value=postbatch.material),
                            Characteristic(category=var_characteristic,
                                           value=c.value)])
                    if var_characteristic not in study.characteristic_categories:
                        study.characteristic_categories.append(var_characteristic)

                    if not postbatch.parameter_values:
                        sample = Sample(name='QC.{}.{}'.format(postbatch.material.term, str(i+1).zfill(3)))
                        process = Process(executes_protocol=study.get_prot(
                            'sample collection'), inputs=[qcsource],
                            outputs=[sample], performer=self.ops[0], date_=
                            datetime.date.isoformat(
                                datetime.date.today()))
                        process.parameter_values = [
                            ParameterValue(
                                category=param_run_order, value=-1)
                        ]
                        samples.append(sample)
                        process_sequence.append(process)
                    else:
                        for j, p in enumerate(postbatch.parameter_values):
                            qc_param_set.add(p)
                            sample = Sample(name='QC.{}.{}'.format(postbatch.material.term, str(j+1).zfill(3)))
                            qc_param = sample_collection.get_param(
                                p.category.parameter_name.term)
                            if qc_param is None:
                                sample_collection.add_param(p)
                            process = Process(executes_protocol=study.get_prot(
                                'sample collection'), inputs=[qcsource],
                                outputs=[sample], performer=self.ops[0], date_=
                                datetime.date.isoformat(
                                    datetime.date.today()))
                            process.parameter_values = [
                                ParameterValue(category=param_run_order,
                                               value=-1),
                                ParameterValue(
                                    category=sample_collection.get_param(
                                        p.category.parameter_name.term),
                                    value=p.value),
                            ]
                            samples.append(sample)
                            process_sequence.append(process)
            if not postbatch.parameter_values:
                qcsource = Source(name='source_QC', characteristics=[
                    Characteristic(
                        category=OntologyAnnotation(term='Material Type'),
                        value=postbatch.material)])
                sources.append(qcsource)
                for i, p in enumerate(postbatch.parameter_values):
                    qc_param_set.add(p)
                    sample = Sample(
                        name='QC.{}.{}'.format(postbatch.material.term,
                                               str(i + 1).zfill(3)))
                    qc_param = sample_collection.get_param(
                        p.category.parameter_name.term)
                    if qc_param is None:
                        sample_collection.add_param(
                            p.category.parameter_name.term)
                    process = Process(executes_protocol=study.get_prot(
                        'sample collection'), inputs=[qcsource],
                        outputs=[sample], performer=self.ops[0], date_=
                        datetime.date.isoformat(datetime.date.today()))
                    process.parameter_values=[
                        ParameterValue(category=param_run_order, value=-1),
                        ParameterValue(category=sample_collection.get_param(
                            p.category.parameter_name.term), value=p.value),
                    ]
                    samples.append(sample)
                    process_sequence.append(process)
        # normalize size of params across all processes
        study.characteristic_categories = list(
            set(study.characteristic_categories))
        for process in process_sequence:
            missing = qc_param_set - set(
                [x.category.parameter_name.term for x in
                 process.parameter_values])
            for each in missing:
                qc_param_missing = sample_collection.get_param(each)
                process.parameter_values.append(
                    ParameterValue(category=qc_param_missing))
        study.sources = sources
        study.samples = samples
        study.process_sequence = process_sequence
        study.factors = list(factors)
        study.ontology_source_references = list(ontology_sources)
        return study

    def create_nmr_assays_from_plan(self, study, samples, sample_type, assay_type):
        for pulse_seq, acq_mode in itertools.product(
                assay_type.topology_modifiers.pulse_sequences,
                assay_type.topology_modifiers.acquisition_modes):
            random.shuffle(self.__ops)

            assay = Assay(measurement_type=assay_type.measurement_type,
                          technology_type=assay_type.technology_type,
                          filename='a_{0}_nmr_{1}_{2}_assay.txt'.format(
                              sample_type.value.term, acq_mode, pulse_seq))
            try:
                study.add_prot(
                    protocol_name='metabolite extraction',
                    protocol_type='extraction')
            except ISAModelAttributeError:
                pass

            mp_protocol_name = '{0}-{1} nmr spectroscopy' \
                .format(acq_mode, pulse_seq)
            try:
                study.add_prot(protocol_name=mp_protocol_name,
                               protocol_type='nmr spectroscopy',
                               use_default_params=True)
            except ISAModelAttributeError:
                pass
            nmr_prot = study.get_prot(mp_protocol_name)
            try:
                nmr_prot.add_param('run order')
            except ISAModelAttributeError:
                pass
            try:
                nmr_prot.add_param('acquisition mode')
            except ISAModelAttributeError:
                pass
            try:
                nmr_prot.add_param('pulse sequence')
            except ISAModelAttributeError:
                pass
            try:
                nmr_prot.add_param('magnetic field strength')
            except ISAModelAttributeError:
                pass
            num_samples_in_stype = len(samples)
            technical_replicates = \
                assay_type.topology_modifiers.technical_replicates
            total_expected_runs = \
                num_samples_in_stype * technical_replicates
            run_order = list(range(1, total_expected_runs + 1))
            # random.shuffle(run_order)  # does random shuffle inplace
            run_counter = 0

            for i, samp in enumerate(samples):
                biorepl = str(i + 1).zfill(3)
                # build assay path
                assay.samples.append(samp)

                extr = Extract(name='{0}_extract-{1}'.format(
                    samp.name, i))
                assay.other_material.append(extr)
                eproc = Process(executes_protocol=study
                                .get_prot('metabolite extraction'),
                                inputs=[samp], outputs=[extr],
                                performer=self.ops[1],
                                date_=datetime.date.isoformat(
                                    datetime.date.today()))
                assay.process_sequence.append(eproc)
                for j in range(1, technical_replicates + 1):
                    techrepl = str(j).zfill(3)
                    nmr_prot = study.get_prot(mp_protocol_name)
                    aproc = Process(executes_protocol=nmr_prot,
                                    name='assay-{0}_run-{1}'.format(i, j),
                                    inputs=[extr],
                                    performer=self.ops[2],
                                    date_=datetime.date.isoformat(
                                        datetime.date.today()))
                    aproc.parameter_values = [
                        ParameterValue(category=nmr_prot.get_param(
                            'run order'),
                            value=str(run_counter)),
                        ParameterValue(category=nmr_prot.get_param(
                            'acquisition mode'), value=acq_mode),
                        ParameterValue(category=nmr_prot.get_param(
                            'instrument'), value=next(
                            iter(assay_type.topology_modifiers
                                 .instruments))),
                        ParameterValue(category=nmr_prot.get_param(
                            'pulse sequence'), value=pulse_seq),
                    ]
                    if assay_type.topology_modifiers.magnet_power is not None:
                        aproc.parameter_values.append(
                            ParameterValue(category=nmr_prot.get_param(
                                'magnetic field strength'), value=assay_type.topology_modifiers.magnet_power)
                        )
                    run_counter += 1
                    plink(eproc, aproc)
                    assaycode = 'A002'  # TODO: Find out what NMR assay codes they use, if any
                    dfile = FreeInductionDecayDataFile(
                        filename='{assaycode}_{pulse_seq}_{acq_mode}_{biorepl}_{techrepl}.nmrml'.format(
                            assaycode=assaycode, biorepl=biorepl,
                            pulse_seq=pulse_seq, acq_mode=acq_mode,
                            techrepl=techrepl))
                    assay.data_files.append(dfile)
                    aproc.outputs = [dfile]
                    assay.process_sequence.append(aproc)
            if assay is not None:
                study.assays.append(assay)

    def create_ms_assays_from_plan(self, study, samples, sample_type, assay_type):
        top_mods = assay_type.topology_modifiers
        if isinstance(top_mods, MSTopologyModifiers):
            if len(top_mods.sample_fractions) == 0:
                # skip looping sample_fractions
                for injection_mode in top_mods.injection_modes:
                    if not injection_mode.derivatizations:
                        injection_mode.derivatizations.add('none reported')
                    for acquisition_mode in injection_mode.acquisition_modes:
                        random.shuffle(self.__ops)
                        assay = Assay(
                            measurement_type=assay_type.measurement_type,
                            technology_type=assay_type.technology_type,
                            filename='a_{sample_type}_{injection_mode}_{acquisition_method}_assay.txt'.format(
                                sample_type=sample_type.value.term,
                                injection_mode=injection_mode.injection_mode,
                                acquisition_method=acquisition_mode.acquisition_method))
                        try:
                            study.add_prot(
                                protocol_name='metabolite extraction',
                                protocol_type='extraction')
                        except ISAModelAttributeError:
                            pass
                        ext_protocol = study.get_prot('metabolite extraction')
                        if injection_mode.injection_mode in ('LC', 'GC'):
                            try:
                                ext_protocol.add_param('chromatography instrument')
                            except ISAModelAttributeError:
                                pass
                            try:
                                ext_protocol.add_param('chromatography column')
                            except ISAModelAttributeError:
                                pass
                        if injection_mode.injection_mode == 'GC':
                            try:
                                study.add_prot(
                                    protocol_name='derivatization',
                                    protocol_type='derivatization')
                            except ISAModelAttributeError:
                                pass
                        mp_protocol_name = '{0}-{1} mass spectrometry'.format(
                            injection_mode.injection_mode,
                            acquisition_mode.acquisition_method)
                        try:
                            study.add_prot(protocol_name=mp_protocol_name,
                                           protocol_type='mass spectrometry',
                                           use_default_params=True)
                        except ISAModelAttributeError:
                            pass
                        ms_prot = study.get_prot(mp_protocol_name)
                        try:
                            ms_prot.add_param('run order')
                        except ISAModelAttributeError:
                            pass
                        try:
                            ms_prot.add_param('injection mode')
                        except ISAModelAttributeError:
                            pass
                        try:
                            ms_prot.add_param('scan polarity')
                        except ISAModelAttributeError:
                            pass
                        der_protocol = study.get_prot('derivatization')
                        if der_protocol is not None:
                            try:
                                der_protocol.add_param('derivatization agent')
                            except:
                                pass
                        num_samples_in_stype = len(samples)
                        technical_replicates = acquisition_mode.technical_repeats
                        num_derivations_per_sample = len(injection_mode.derivatizations)
                        if len(injection_mode.derivatizations) > 1:
                            total_expected_runs = num_samples_in_stype * technical_replicates * num_derivations_per_sample
                        else:
                            total_expected_runs = num_samples_in_stype * technical_replicates
                        run_order = list(range(1, total_expected_runs+1))
                        # random.shuffle(run_order)  # does random shuffle inplace
                        run_counter = 0
                        for i, samp in enumerate(samples):
                            biorepl = str(i+1).zfill(3)
                            # build assay path
                            assay.samples.append(samp)
                            # add extraction process
                            extr = Extract(name='{0}.Extract-{1}'.format(
                                samp.name, biorepl))
                            assay.other_material.append(extr)
                            eproc = Process(executes_protocol=ext_protocol,
                                            inputs=[samp], outputs=[extr],
                                            performer=self.ops[1],
                                            date_=datetime.date.isoformat(
                                                datetime.date.today()))
                            assay.process_sequence.append(eproc)
                            if injection_mode.injection_mode == 'GC':
                                if not injection_mode.derivatizations:
                                    injection_mode.derivatizations.add('none reported')
                                for lcount, dervivatization in enumerate(injection_mode.derivatizations):
                                    chromat_instr = injection_mode.chromatography_instrument
                                    chromat_col = injection_mode.chromatography_column
                                    # add GC-specific params to extraction process
                                    eproc.parameter_values.append(
                                        ParameterValue(
                                            category=ext_protocol.get_param(
                                                'chromatography instrument'),
                                            value=chromat_instr)
                                    )

                                    eproc.parameter_values.append(
                                        ParameterValue(
                                            category=ext_protocol.get_param(
                                                'chromatography column'),
                                            value=chromat_col)
                                    )
                                    # add derivatization/labeling process
                                    lextr = LabeledExtract(
                                        name='{0}.LE-{1}'.format(extr.name,
                                                                 lcount+1))
                                    assay.other_material.append(lextr)
                                    der_prot = study.get_prot('derivatization')
                                    dproc = Process(executes_protocol=der_prot,
                                        inputs=[extr], outputs=[lextr],
                                        performer=self.ops[1],
                                        date_=datetime.date.isoformat(
                                            datetime.date.today()))
                                    dproc.parameter_values.append(
                                        ParameterValue(
                                            category=der_prot.get_param(
                                                'derivatization agent'),
                                            value=dervivatization)
                                    )
                                    assay.process_sequence.append(dproc)
                                    plink(eproc, dproc)
                                    for j in range(1, technical_replicates + 1):
                                        techrepl = str(j).zfill(3)
                                        ms_prot = study.get_prot(
                                            mp_protocol_name)
                                        aproc = Process(
                                            executes_protocol=ms_prot,
                                            name='{extract_name}.MSASSAY-{run_count}'
                                            .format(extract_name=lextr.name,
                                                    run_count=techrepl),
                                            inputs=[lextr],
                                            performer=self.ops[2],
                                            date_=datetime.date.isoformat(
                                                datetime.date.today()))
                                        aproc.parameter_values = [
                                            ParameterValue(
                                                category=ms_prot.get_param(
                                                    'run order'),
                                                value=str(
                                                    run_order[run_counter])),
                                            ParameterValue(
                                                category=ms_prot.get_param(
                                                    'injection mode'),
                                                value=injection_mode.injection_mode),
                                            ParameterValue(
                                                category=ms_prot.get_param(
                                                    'instrument'),
                                                value=injection_mode.ms_instrument
                                            ),
                                            ParameterValue(
                                                category=ms_prot.get_param(
                                                    'scan polarity'),
                                                value=acquisition_mode.acquisition_method),
                                        ]
                                        run_counter += 1
                                        plink(dproc, aproc)
                                        # Birmingham encoding
                                        assaycode = 'A100'  # unknown assay type; default as any LCMS
                                        if injection_mode.injection_mode == 'LC':
                                            if chromat_col == 'RF':
                                                assaycode = 'A101'
                                            elif chromat_col == 'HILIC':
                                                assaycode = 'A102'
                                            elif chromat_col == 'LIPIDS':
                                                assaycode = 'A103'
                                        # London encoding
                                        # ...
                                        dfile = RawSpectralDataFile(
                                            filename='{assaycode}_{inj_mode}_{acq_mode}_{biorepl}.{extcnt}_{techrepl}.mzml'.format(
                                                assaycode=assaycode,
                                                biorepl=biorepl,
                                                extcnt=lcount+1,
                                                inj_mode=injection_mode.injection_mode,
                                                acq_mode=acquisition_mode.acquisition_method,
                                                techrepl=techrepl))
                                        assay.data_files.append(dfile)
                                        aproc.outputs = [dfile]
                                        assay.process_sequence.append(aproc)
                            else:
                                if injection_mode.injection_mode in ('LC', 'GC'):
                                    chromat_instr = injection_mode.chromatography_instrument
                                    chromat_col = injection_mode.chromatography_column
                                    # add GC-specific params to extraction process
                                    eproc.parameter_values.append(
                                        ParameterValue(
                                            category=ext_protocol.get_param(
                                                'chromatography instrument'),
                                            value=chromat_instr)
                                    )
                                    eproc.parameter_values.append(
                                        ParameterValue(
                                            category=ext_protocol.get_param(
                                                'chromatography column'),
                                            value=chromat_col)
                                    )
                                for j in range(1, technical_replicates + 1):
                                    techrepl = str(j).zfill(3)
                                    ms_prot = study.get_prot(mp_protocol_name)
                                    aproc = Process(executes_protocol=ms_prot,
                                                    name='{extract_name}.MSASSAY-{run_count}'
                                                    .format(extract_name=extr.name, run_count=techrepl),
                                                    inputs=[extr],
                                                    performer=self.ops[2],
                                                    date_=datetime.date.isoformat(
                                                        datetime.date.today()))
                                    aproc.parameter_values = [
                                        ParameterValue(category=ms_prot.get_param(
                                            'run order'),
                                            value=str(run_order[run_counter])),
                                        ParameterValue(category=ms_prot.get_param(
                                            'injection mode'), value=injection_mode.injection_mode),
                                        ParameterValue(
                                            category=ms_prot.get_param(
                                                'instrument'),
                                            value=injection_mode.ms_instrument
                                        ),
                                        ParameterValue(category=ms_prot.get_param(
                                            'scan polarity'), value=acquisition_mode.acquisition_method),
                                    ]
                                    run_counter += 1
                                    if eproc is not None:
                                        plink(eproc, aproc)
                                    # Birmingham encoding
                                    assaycode = 'A100'  # unknown assay type; default as any LCMS
                                    if injection_mode.injection_mode  == 'LC':
                                        if chromat_col == 'RF':
                                            assaycode = 'A101'
                                        elif chromat_col == 'HILIC':
                                            assaycode = 'A102'
                                        elif chromat_col == 'LIPIDS':
                                            assaycode = 'A103'
                                    # London encoding
                                    # ...
                                    dfile = RawSpectralDataFile(
                                        filename='{assaycode}_{inj_mode}_{acq_mode}_{biorepl}_{techrepl}.mzml'.format(
                                            assaycode=assaycode, biorepl=biorepl,
                                            inj_mode=injection_mode.injection_mode , acq_mode=acquisition_mode.acquisition_method,
                                            techrepl=techrepl))
                                    assay.data_files.append(dfile)
                                    aproc.outputs = [dfile]
                                    assay.process_sequence.append(aproc)
                        if assay is not None:
                            study.assays.append(assay)
            else:
                for sample_fraction in top_mods.sample_fractions:
                    for injection_mode in top_mods.injection_modes:
                        for acquisition_mode in injection_mode.acquisition_modes:
                            random.shuffle(self.__ops)
                            assay = Assay(
                                measurement_type=assay_type.measurement_type,
                                technology_type=assay_type.technology_type,
                                filename='a_{sample_type}_{sample_fraction}_{injection_mode}_{acquisition_method}_assay.txt'.format(
                                    sample_type=sample_type.value.term,
                                    sample_fraction=sample_fraction,
                                    injection_mode=injection_mode.injection_mode,
                                    acquisition_method=acquisition_mode.acquisition_method))
                            study.add_prot(protocol_name='metabolite extraction', protocol_type='extraction')
                            ext_protocol = study.get_prot('metabolite extraction')
                            if injection_mode.injection_mode in ('LC', 'GC'):
                                ext_protocol.add_param('chromatography instrument')
                                ext_protocol.add_param('chromatography column')
                                ext_protocol.add_param('elution program')
                            mp_protocol_name = '{0}-{1} mass spectrometry'.format(
                                injection_mode.injection_mode,
                                acquisition_mode.acquisition_method)
                            study.add_prot(protocol_name=mp_protocol_name, protocol_type='mass spectrometry')
                            ms_prot = study.get_prot(mp_protocol_name)
                            ms_prot.add_param('run order')
                            ms_prot.add_param('injection mode')
                            ms_prot.add_param('scan polarity')
                            num_samples_in_stype = len(samples)
                            technical_replicates = acquisition_mode.technical_repeats
                            total_expected_runs = num_samples_in_stype * technical_replicates
                            run_order = list(range(1, total_expected_runs + 1))
                            # random.shuffle(run_order)  # does random shuffle inplace
                            run_counter = 0
                            for i, samp in enumerate(samples):
                                biorepl = str(i + 1).zfill(3)
                                # build assay path
                                assay.samples.append(samp)

                                extr = Extract(name='{0}.Extract-{1}'.format(
                                    samp.name, biorepl))
                                assay.other_material.append(extr)
                                eproc = Process(executes_protocol=study.get_prot('metabolite extraction'),
                                                inputs=[samp], outputs=[extr],
                                                performer=self.ops[1],
                                                date_=datetime.date.isoformat(
                                                    datetime.date.today()))
                                if injection_mode.injection_mode in ('LC', 'GC'):
                                    eproc.parameter_values.append(
                                        ParameterValue(category=ext_protocol.get_param('chromatography instrument'),
                                            value=injection_mode.chromatography_instrument)
                                    )
                                    chromat_col = injection_mode.chromatography_column
                                    eproc.parameter_values.append(
                                        ParameterValue(
                                            category=ext_protocol.get_param('chromatography column'),
                                            value=chromat_col)
                                    )
                                assay.process_sequence.append(eproc)
                                for j in range(1, technical_replicates + 1):
                                    techrepl = str(j).zfill(3)
                                    ms_prot = study.get_prot(mp_protocol_name)
                                    aproc = Process(executes_protocol=ms_prot,
                                                    name='{extract_name}.MSASSAY-{run_count}'
                                                    .format(
                                                        extract_name=extr.name,
                                                        run_count=techrepl),
                                                    inputs=[extr],
                                                    performer=self.ops[2],
                                                    date_=datetime.date.isoformat(
                                                        datetime.date.today()))
                                    aproc.parameter_values = [
                                        ParameterValue(
                                            category=ms_prot.get_param(
                                                'run order'),
                                            value=str(run_order[run_counter])),
                                        ParameterValue(
                                            category=ms_prot.get_param(
                                                'injection mode'),
                                            value=injection_mode.injection_mode),
                                        ParameterValue(
                                            category=ms_prot.get_param(
                                                'instrument'),
                                            value=injection_mode.ms_instrument
                                        ),
                                        ParameterValue(
                                            category=ms_prot.get_param(
                                                'scan polarity'),
                                            value=acquisition_mode.acquisition_method),
                                    ]
                                    run_counter += 1
                                    plink(eproc, aproc)
                                    # Birmingham encoding
                                    assaycode = 'A100'  # unknown assay type; default as any LCMS
                                    if injection_mode.injection_mode == 'LC':
                                        if chromat_col == 'RF':
                                            assaycode = 'A101'
                                        elif chromat_col == 'HILIC':
                                            assaycode = 'A102'
                                        elif chromat_col == 'LIPIDS':
                                            assaycode = 'A103'
                                    # London encoding
                                    # ...
                                    dfile = RawSpectralDataFile(
                                        filename='{assaycode}_{inj_mode}_{acq_mode}_{biorepl}_{techrepl}.mzml'.format(
                                            assaycode=assaycode,
                                            biorepl=biorepl,
                                            inj_mode=injection_mode.injection_mode,
                                            acq_mode=acquisition_mode.acquisition_method,
                                            techrepl=techrepl))
                                    assay.data_files.append(dfile)
                                    aproc.outputs = [dfile]
                                    assay.process_sequence.append(aproc)
                            if assay is not None:
                                study.assays.append(assay)

    def create_microarray_assays_from_plan(self):
        study = self.create_study_from_plan()
        if self.sample_assay_plan.assay_plan == {}:
            raise ISAModelAttributeError('assay_plan is not defined')
        for stype, atype in self.sample_assay_plan.assay_plan:
            # first get all samples of stype
            samples_filtered_on_stype = [x for x in study.samples if
                                         stype in x.characteristics]

            lowered_tt = atype.technology_type.term.lower()
            if atype.technology_type.term == 'DNA microarray':
                assay = Assay(measurement_type=atype.measurement_type,
                              technology_type=atype.technology_type)

                study.add_prot('RNA extraction', 'RNA extraction')
                study.add_prot('nucleic acid hybridization',
                               'nucleic acid hybridization')
                study.add_prot('data collection', 'data collection')

                run_count = 0
                for i, sample in enumerate(samples_filtered_on_stype):
                    assay.samples.append(sample)

                    if len(atype.topology_modifiers.array_designs) > 0:
                        assay.filename = 'a_{0}_microarray_{1}_assay.txt'\
                            .format(stype.value.term,
                                    '_'.join(atype.topology_modifiers
                                             .array_designs))
                        for array_design, technical_replicate_num in \
                                itertools.product(
                                    atype.topology_modifiers.array_designs,
                                    range(0, atype.topology_modifiers
                                            .technical_replicates)):
                            run_count += 1

                            extract = Extract(name='{0}_extract-{1}'.format(
                                sample.name, i))
                            assay.other_material.append(extract)
                            extraction_process = Process(
                                executes_protocol=study.get_prot(
                                    'RNA extraction'))
                            extraction_process.inputs = [sample]
                            extraction_process.output = [extract]
                            extraction_process.performer = self.ops[1]
                            extraction_process.date = datetime.date.isoformat(
                                datetime.date.today())

                            hyb_protocol = study.get_prot(
                                'nucleic acid hybridization')
                            hyb_process = Process(
                                executes_protocol=hyb_protocol)
                            hyb_process.inputs = [extract]
                            hyb_process.performer = self.ops[2]
                            hyb_process.date = datetime.date.isoformat(
                                datetime.date.today())

                            hyb_process.array_design_ref = array_design
                            hyb_process.name = '{0}_hyb{1}'.format(
                                extract.name, i)

                            plink(extraction_process, hyb_process)

                            array_data_file = ArrayDataFile(
                                filename='output-file-{}.sff'.format(run_count))
                            assay.data_files.append(array_data_file)
                            seq_process = Process(
                                executes_protocol=study.get_prot(
                                    'data collection'))
                            seq_process.outputs = [array_data_file]
                            seq_process.performer = self.ops[3]
                            seq_process.date = datetime.date.isoformat(
                                datetime.date.today())
                            seq_process.name = '{0}_Scan{1}'.format(
                                hyb_process.name, i)

                            plink(hyb_process, seq_process)

                            assay.process_sequence.append(extraction_process)
                            assay.process_sequence.append(hyb_process)
                            assay.process_sequence.append(seq_process)
                    else:
                        raise ISAModelAttributeError('At least one array '
                                                     'design must be specified')
                if assay is not None:
                    study.assays.append(assay)
        return study

    def create_seq_assays_from_plan(self):
        study = self.create_study_from_plan()
        if self.sample_assay_plan.assay_plan == {}:
            raise ISAModelAttributeError('assay_plan is not defined')
        for stype, atype in self.sample_assay_plan.assay_plan:
            # first get all samples of stype
            samples_filtered_on_stype = [x for x in study.samples if
                             stype in x.characteristics]

            lowered_tt = atype.technology_type.term.lower()
            if atype.technology_type.term == 'nucleotide sequencing':
                assay = Assay(measurement_type=atype.measurement_type,
                              technology_type=atype.technology_type)

                study.add_prot('nucleic acid extraction',
                               'nucleic acid extraction')
                study.add_prot('library construction', 'library construction')
                study.add_prot('nucleic acid sequencing',
                               'nucleic acid sequencing')

                run_count = 0
                for i, sample in enumerate(samples_filtered_on_stype):
                    assay.samples.append(sample)

                    if len(atype.topology_modifiers.instruments) > 0:
                        assay.filename = 'a_{0}_dnaseq_{1}_assay.txt' \
                            .format(stype.value.term,
                                    '_'.join(atype.topology_modifiers
                                             .instruments))
                        for instrument, technical_replicate_num in \
                                itertools.product(
                                    atype.topology_modifiers.instruments,
                                    range(0, atype.topology_modifiers
                                            .technical_replicates)):
                            run_count += 1

                            extract = Extract(name='{0}_extract-{1}'.format(
                                sample.name, i))
                            assay.other_material.append(extract)
                            extraction_process = Process(
                                executes_protocol=study.get_prot(
                                    'nucleic acid extraction'))
                            extraction_process.inputs = [sample]
                            extraction_process.output = [extract]
                            extraction_process.performer = self.ops[1]
                            extraction_process.date = datetime.date.isoformat(
                                datetime.date.today())

                            lib_protocol = study.get_prot(
                                'library construction')
                            lib_process = Process(
                                executes_protocol=lib_protocol)
                            lib_process.inputs = [extract]
                            lib_process.performer = self.ops[2]
                            lib_process.date = datetime.date.isoformat(
                                datetime.date.today())

                            plink(extraction_process, lib_process)

                            raw_data_file = RawDataFile(
                                filename='output-file-{}.sff'.format(run_count))
                            assay.data_files.append(raw_data_file)
                            seq_protocol = study.get_prot(
                                'nucleic acid sequencing')
                            seq_process = Process(
                                executes_protocol=seq_protocol)
                            seq_process.outputs = [raw_data_file]
                            seq_process.performer = self.ops[3]
                            seq_process.date = datetime.date.isoformat(
                                datetime.date.today())
                            seq_process.name = '{0}_Scan{1}'.format(
                                extract.name, i)
                            seq_process.parameter_values.append(
                                    ParameterValue(
                                        category=seq_protocol.get_param(
                                            'sequencing instrument'),
                                        value=instrument
                                    )
                                )

                            plink(lib_process, seq_process)

                            assay.process_sequence.append(extraction_process)
                            assay.process_sequence.append(lib_process)
                            assay.process_sequence.append(seq_process)
                    else:
                        raise ISAModelAttributeError('At least one instrument '
                                                     'must be specified')

                if assay is not None:
                    study.assays.append(assay)
        return study

    def create_assays_from_plan(self):
        study = self.create_study_from_plan()
        # TODO: Implement new assay writer
        raise NotImplementedError
        for stype, atype in self.sample_assay_plan.assay_plan:
            # first get all samples of stype
            samples_stype = [x for x in study.samples if
                             stype in x.characteristics]
            lowered_mt = atype.measurement_type.term.lower()
            lowered_tt = atype.technology_type.term.lower()
            if lowered_mt == 'metabolite profiling' \
                    and lowered_tt == 'mass spectrometry':
                self.create_ms_assays_from_plan(study, samples_stype, stype, atype)  # pass filtered samples list, sample type, assay type

            elif lowered_mt == 'metabolite profiling' \
                    and lowered_tt == 'nmr spectroscopy':
                self.create_nmr_assays_from_plan(study, samples_stype, stype, atype)

            elif lowered_tt == 'dna microarray':
                assay = Assay(measurement_type=atype.measurement_type,
                              technology_type=atype.technology_type)

                study.add_prot('RNA extraction', 'RNA extraction')
                study.add_prot('nucleic acid hybridization',
                               'nucleic acid hybridization')
                study.add_prot('data collection', 'data collection')

                run_count = 0
                for i, sample in enumerate(samples_stype):
                    assay.samples.append(sample)

                    if len(atype.topology_modifiers.array_designs) > 0:
                        assay.filename = 'a_{0}_dnamicro_{1}_assay.txt' \
                            .format(stype.value.term,
                                    '_'.join(atype.topology_modifiers
                                             .array_designs))
                        for array_design, technical_replicate_num in \
                                itertools.product(
                                    atype.topology_modifiers.array_designs,
                                    range(0, atype.topology_modifiers
                                            .technical_replicates)):
                            run_count += 1

                            extract = Extract(name='{0}_extract-{1}'.format(
                                sample.name, str(i).zfill(3)))
                            assay.other_material.append(extract)
                            extraction_process = Process(
                                executes_protocol=study.get_prot(
                                    'RNA extraction'))
                            extraction_process.inputs = [sample]
                            extraction_process.output = [extract]
                            extraction_process.performer = self.ops[1]
                            extraction_process.date = datetime.date.isoformat(
                                datetime.date.today())

                            hyb_protocol = study.get_prot(
                                'nucleic acid hybridization')
                            hyb_process = Process(
                                executes_protocol=hyb_protocol)
                            hyb_process.inputs = [extract]
                            hyb_process.performer = self.ops[2]
                            hyb_process.date = datetime.date.isoformat(
                                datetime.date.today())

                            hyb_process.array_design_ref = array_design
                            hyb_process.name = '{0}_hyb{1}'.format(
                                extract.name, i)

                            plink(extraction_process, hyb_process)

                            array_data_file = ArrayDataFile(
                                filename='output-file-{run_count}.sff'.format(
                                    run_count=str(run_count).zfill(3)))
                            assay.data_files.append(array_data_file)
                            seq_process = Process(
                                executes_protocol=study.get_prot(
                                    'data collection'))
                            seq_process.outputs = [array_data_file]
                            seq_process.performer = self.ops[3]
                            seq_process.date = datetime.date.isoformat(
                                datetime.date.today())
                            seq_process.name = '{0}_Scan{1}'.format(
                                hyb_process.name, i)

                            plink(hyb_process, seq_process)

                            assay.process_sequence.append(
                                extraction_process)
                            assay.process_sequence.append(hyb_process)
                            assay.process_sequence.append(seq_process)
                    else:
                        raise ISAModelAttributeError('At least one array '
                                                     'design must be specified')
                if assay is not None:
                    study.assays.append(assay)

            elif lowered_tt == 'nucleotide sequencing':
                assay = Assay(measurement_type=atype.measurement_type,
                              technology_type=atype.technology_type)

                study.add_prot('nucleic acid extraction',
                               'nucleic acid extraction')
                study.add_prot('library construction', 'library construction')
                study.add_prot('nucleic acid sequencing',
                               'nucleic acid sequencing')

                run_count = 0
                for i, sample in enumerate(samples_stype):
                    assay.samples.append(sample)

                    if len(atype.topology_modifiers.instruments) > 0:
                        assay.filename = 'a_{0}_dnaseq_{1}_assay.txt'\
                            .format(stype.value.term,
                                    '_'.join(atype.topology_modifiers
                                             .instruments))
                        for instrument, technical_replicate_num in \
                                itertools.product(
                                    atype.topology_modifiers.instruments,
                                    range(0, atype.topology_modifiers
                                            .technical_replicates)):
                            run_count += 1

                            extract = Extract(name='{0}_extract-{1}'.format(
                                sample.name, str(i).zfill(3)))
                            assay.other_material.append(extract)
                            extraction_process = Process(
                                executes_protocol=study.get_prot(
                                    'nucleic acid extraction'))
                            extraction_process.inputs = [sample]
                            extraction_process.output = [extract]
                            extraction_process.performer = self.ops[1]
                            extraction_process.date = datetime.date.isoformat(
                                datetime.date.today())

                            lib_protocol = study.get_prot(
                                'library construction')
                            lib_process = Process(
                                executes_protocol=lib_protocol)
                            lib_process.inputs = [extract]
                            lib_process.performer = self.ops[2]
                            lib_process.date = datetime.date.isoformat(
                                datetime.date.today())

                            plink(extraction_process, lib_process)

                            raw_data_file = RawDataFile(
                                filename='output-file-{run_count}.sff'.format(
                                    run_count=str(run_count).zfill(3)))
                            assay.data_files.append(raw_data_file)
                            seq_protocol = study.get_prot(
                                'nucleic acid sequencing')
                            seq_process = Process(
                                executes_protocol=seq_protocol)
                            seq_process.outputs = [raw_data_file]
                            seq_process.performer = self.ops[3]
                            seq_process.date = datetime.date.isoformat(
                                datetime.date.today())
                            seq_process.name = '{0}_Scan{1}'.format(
                                extract.name, i)
                            seq_process.parameter_values.append(
                                    ParameterValue(
                                        category=seq_protocol.get_param(
                                            'sequencing instrument'),
                                        value=instrument
                                    )
                                )

                            plink(lib_process, seq_process)

                            assay.process_sequence.append(extraction_process)
                            assay.process_sequence.append(lib_process)
                            assay.process_sequence.append(seq_process)
                    else:
                        raise ISAModelAttributeError('At least one instrument '
                                                     'must be specified')

                if assay is not None:
                    study.assays.append(assay)
        return study


class SampleAssayPlanEncoder(json.JSONEncoder):

    def get_acquisition_mode(self, o):
        if isinstance(o, MSAcquisitionMode):
            return {
                'acquisition_method': o.acquisition_method,
                'technical_repeats': o.technical_repeats
            }

    def get_top_mods(self, o):
        if isinstance(o, DNAMicroAssayTopologyModifiers):
            return {
                'array_designs': sorted(o.array_designs),
                'technical_replicates': o.technical_replicates
            }
        if isinstance(o, DNASeqAssayTopologyModifiers):
            return {
                'distinct_libraries': o.distinct_libraries,
                'technical_replicates': o.technical_replicates,
                'instruments': sorted(o.instruments)
            }
        if isinstance(o, MSTopologyModifiers):
            return {
                'sample_fractions': list(o.sample_fractions),
                'injection_modes': [self.get_injection_mode(x) for
                                    x in o.injection_modes]
            }
        if isinstance(o, NMRTopologyModifiers):
            return {
                'injection_modes': sorted(o.injection_modes),
                'acquisition_modes': sorted(o.acquisition_modes),
                'pulse_sequences': sorted(o.pulse_sequences),
                'technical_replicates': o.technical_replicates,
                'instruments': sorted(o.instruments)
            }

    def get_injection_mode(self, o):
        if isinstance(o, MSInjectionMode):
            j = {
                'injection_mode': o.injection_mode,
                'acquisition_modes': [self.get_acquisition_mode(x) for
                                      x in o.acquisition_modes]
            }
            if o.ms_instrument:
                j['instrument'] = o.ms_instrument
            if o.chromatography_instrument:
                j['chromatography_instrument'] = o.chromatography_instrument
            if o.chromatography_column:
                j['chromatography_column'] = o.chromatography_column
            return j

    def get_assay_type(self, o):
        return {
            'measurement_type': o.measurement_type.term
            if o.measurement_type else '',
            'technology_type': o.technology_type.term
            if o.technology_type else '',
            'topology_modifiers': self.get_top_mods(o.topology_modifiers)
            if o.topology_modifiers else []
        }

    @staticmethod
    def get_sample_plan(sample_plan):
        sample_plan_record_list = []
        for k in iter(sample_plan.keys()):
            sample_type_characteristic = k
            sampling_size = sample_plan[k]
            sample_type = sample_type_characteristic.value.term
            sample_plan_record_list.append(
                {
                    'sample_type': sample_type,
                    'sampling_size': sampling_size
                }
            )
        return sample_plan_record_list

    @staticmethod
    def get_sample_qc_plan(sample_qc_plan):
        sample_qc_plan_record_list = []
        for k in sample_qc_plan.keys():
            sample_type_characteristic = k
            injection_interval = sample_qc_plan[k]
            sample_type = sample_type_characteristic.value.term
            sample_qc_plan_record_list.append(
                {
                    'sample_type': sample_type,
                    'injection_interval': injection_interval
                }
            )
        return sample_qc_plan_record_list

    @staticmethod
    def get_sample_qc_batch_plan(sample_qc_batch_plan):
        if isinstance(sample_qc_batch_plan, SampleQCBatch):
            if len(sample_qc_batch_plan.parameter_values) > 0 and \
                    len(sample_qc_batch_plan.characteristic_values) > 0:
                raise ISAModelAttributeError(
                    'Must only set a range of parameter values OR '
                    'characteristic values. Not both.')
            qc_batch_plan_json = {
                'material': sample_qc_batch_plan.material,
            }
            if len(sample_qc_batch_plan.characteristic_values) > 0:
                qc_batch_plan_json['variable_type'] = 'characteristic'
                qc_batch_plan_json['variable_name'] = next(
                    iter(sample_qc_batch_plan.characteristic_values))\
                    .characteristic_category.term
                qc_batch_plan_json['values'] = [
                    x.value for x in sample_qc_batch_plan.characteristic_values]
            else:
                qc_batch_plan_json['variable_type'] = 'parameter'
                qc_batch_plan_json['variable_name'] = next(
                    iter(sample_qc_batch_plan.parameter_values)) \
                    .category.parameter_name.term
                qc_batch_plan_json['values'] = [
                    x.value for x in sample_qc_batch_plan.parameter_values]
            return qc_batch_plan_json

    def get_assay_plan(self, assay_plan):
        assay_plan_record_list = []
        for mapping in assay_plan:
            sample_type = mapping[0]
            assay_type = mapping[1]
            assay_plan_record_list.append(
                {
                    'sample_type': sample_type.value.term,
                    'assay_type': self.get_assay_type(assay_type)
                }
            )
        return assay_plan_record_list

    def default(self, o):
        if isinstance(o, (GenericAssayTopologyModifiers, MSTopologyModifiers)):
            return self.get_top_mods(o)
        elif isinstance(o, AssayType):
            return self.get_assay_type(o)
        elif isinstance(o, SampleAssayPlan):
            sample_assay_plan_json = {
                'group_size': o.group_size,
                'sample_types': sorted([x.value.term for x in o.sample_types]),
                'assay_types': [self.get_assay_type(x) for x in o.assay_types],
                'sample_plan': self.get_sample_plan(o.sample_plan),
                'sample_qc_plan': self.get_sample_qc_plan(o.sample_qc_plan),
                'assay_plan': self.get_assay_plan(o.assay_plan)
            }
            if o.pre_run_batch:
                sample_assay_plan_json['pre_run_batch'] = \
                    self.get_sample_qc_batch_plan(o.pre_run_batch)
            if o.post_run_batch:
                sample_assay_plan_json['post_run_batch'] = \
                    self.get_sample_qc_batch_plan(o.post_run_batch)
            return sample_assay_plan_json


class SampleAssayPlanDecoder(object):

    def __init__(self):
        self.dna_micro_key_signature = ('technical_replicates', 'array_designs')
        self.dna_seq_key_signature = (
            'technical_replicates', 'distinct_libraries', 'instruments')
        self.ms_key_signature = (
            'technical_replicates', 'injection_modes', 'acquisition_modes',
            'instruments', 'chromatography_instruments')
        self.nmr_key_signature = (
            'technical_replicates', 'injection_modes', 'acquisition_modes',
            'pulse_sequences', 'instruments')

    def load_top_mods(self, top_mods_json):
        # do a bit of duck-typing
        top_mods = None
        key_signature = top_mods_json.keys()
        if set(self.dna_micro_key_signature).issubset(key_signature):
            top_mods = DNAMicroAssayTopologyModifiers()
            top_mods.array_designs = set(
                map(lambda x: x, top_mods_json['array_designs']))
            top_mods.technical_replicates = top_mods_json[
                'technical_replicates']
        elif set(self.dna_seq_key_signature).issubset(key_signature):
            top_mods = DNASeqAssayTopologyModifiers()

            top_mods.distinct_libraries = top_mods_json['distinct_libraries']
            top_mods.technical_replicates = top_mods_json[
                'technical_replicates']
            top_mods.instruments = set(
                map(lambda x: x, top_mods_json['instruments']))
        elif set(self.ms_key_signature).issubset(key_signature):
            top_mods = MSTopologyModifiers()
            top_mods.injection_modes = set(
                map(lambda x: x, top_mods_json['injection_modes']))
            top_mods.acquisition_modes = set(
                map(lambda x: x, top_mods_json['acquisition_modes']))
            top_mods.technical_replicates = top_mods_json[
                'technical_replicates']
            top_mods.instruments = set(
                map(lambda x: x, top_mods_json['instruments']))
            top_mods.chromatography_instruments = set(
                map(lambda x: x, top_mods_json['chromatography_instruments']))
        elif set(self.nmr_key_signature).issubset(key_signature):
            top_mods = NMRTopologyModifiers()
            top_mods.injection_modes = set(
                map(lambda x: x, top_mods_json['injection_modes']))
            top_mods.acquisition_modes = set(
                map(lambda x: x, top_mods_json['acquisition_modes']))
            top_mods.pulse_sequences = set(
                map(lambda x: x, top_mods_json['pulse_sequences']))
            top_mods.technical_replicates = top_mods_json[
                'technical_replicates']
            top_mods.instruments = set(
                map(lambda x: x, top_mods_json['instruments']))
        return top_mods

    def load_assay_type(self, assay_type_json):
        assay_type = AssayType(
            measurement_type=assay_type_json['measurement_type'],
            technology_type=assay_type_json['technology_type'],
            topology_modifiers=self.load_top_mods(
                assay_type_json['topology_modifiers']
            )
        )
        return assay_type

    def load(self, fp):
        sample_assay_plan_json = json.load(fp)

        sample_assay_plan = SampleAssayPlan(
            group_size=sample_assay_plan_json['group_size'],
        )

        for sample_type in sample_assay_plan_json['sample_types']:
            sample_assay_plan.add_sample_type(sample_type=sample_type)
        for sample_plan_record in sample_assay_plan_json['sample_plan']:
            sample_assay_plan.add_sample_plan_record(
                sample_type=sample_plan_record['sample_type'],
                sampling_size=sample_plan_record['sampling_size']
            )

        for assay_type in sample_assay_plan_json['assay_types']:
            sample_assay_plan.add_assay_type(
                assay_type=self.load_assay_type(assay_type))
        for assay_plan_record in sample_assay_plan_json['assay_plan']:
            sample_assay_plan.add_assay_plan_record(
                sample_type=assay_plan_record['sample_type'],
                assay_type=self.load_assay_type(assay_plan_record['assay_type'])
            )

        for sample_qc_plan_record in sample_assay_plan_json['sample_qc_plan']:
            sample_assay_plan.add_sample_qc_plan_record(
                material_type=sample_qc_plan_record['sample_type'],
                injection_interval=sample_qc_plan_record['injection_interval']
            )
        try:
            pre_run_batch_json =  sample_assay_plan_json['pre_run_batch']
            pre_run_batch = SampleQCBatch()
            pre_run_batch.material = pre_run_batch_json['material']
            sample_assay_plan.pre_run_batch = pre_run_batch
        except KeyError:
            pass
        try:
            post_run_batch_json = sample_assay_plan_json['post_run_batch']
            post_run_batch = SampleQCBatch()
            post_run_batch.material = post_run_batch_json['material']
            sample_assay_plan.post_run_batch = sample_assay_plan_json['post_run_batch']
        except KeyError:
            pass

        return sample_assay_plan


class StudyEpochEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, StudyCell):
            return {}


class StudyEpochDecoder(object):

    pass


"""
class TreatmentSequenceEncoder(json.JSONEncoder):

    def get_ontology_annotation(self, ontology_annotation):
        return {
            "annotationValue": ontology_annotation.term,
            "termAccession": ontology_annotation.term_accession,
            "termSource": ontology_annotation.term_source.name if
            ontology_annotation.term_source else ''
        }

    def get_study_factor(self, study_factor):
        return {
            "factorName": study_factor.name,
            "factorType": self.get_ontology_annotation(study_factor.factor_type)
        }

    def get_factor_value(self, factor_value):
        return {
            'category': self.get_study_factor(factor_value.factor_name),
            'value': factor_value.value.term if isinstance(
                factor_value.value, OntologyAnnotation) else factor_value.value
        }

    def get_treatment(self, treatment):
        return {
            'treatmentType': treatment.treatment_type,
            'factorValues' : sorted(
                [self.get_factor_value(x) for x in treatment.factor_values],
                key=lambda x: x['category']['factorName'])
        }

    def default(self, o):
        if isinstance(o, TreatmentSequence):
            return {
                'rankedTreatments':[{
                    'treatment': self.get_treatment(x[0]),
                    'rank': x[1]
                } for x in o.ranked_treatments]
            }


class TreatmentSequenceDecoder(object):

    def __init__(self):
        self.factors = dict()

    def get_study_factor(self, factor_json):
        factor = StudyFactor(
            name=factor_json["factorName"],
            factor_type=OntologyAnnotation(
                term=factor_json["factorType"]["annotationValue"],
                term_accession=factor_json["factorType"]["termAccession"])
        )
        if factor.name in self.factors.keys():
            return self.factors.get(factor.name)
        else:
            self.factors[factor.name] = factor
            return factor

    def load(self, fp):
        treatment_sequence_json = json.load(fp)

        treatment_sequence = TreatmentSequence()

        for treatment_tuple in treatment_sequence_json['rankedTreatments']:
            treatment_json = treatment_tuple['treatment']
            treatment = Treatment(
                treatment_type=treatment_json['treatmentType'])
            for factor_json in treatment_json['factorValues']:
                fv = FactorValue(
                    factor_name=self.get_study_factor(factor_json['category']),
                    value=factor_json['value'])
                treatment.factor_values.add(fv)

            treatment_sequence.add_treatment(treatment, treatment_tuple['rank'])
        return treatment_sequence


def make_summary_from_treatment_sequence(treatment_sequence):
    factor_values = set()
    for treatment, rank in treatment_sequence.ranked_treatments:
        factor_values = factor_values.union(treatment.factor_values)
    factors_dict = dict()
    for factor_value in factor_values:
        factors_dict[factor_value.factor_name.name] = []
    for factor_value in factor_values:
        factors_dict[factor_value.factor_name.name].append(factor_value.value)
    ranks = set()
    treatments = []
    for treatment, rank in treatment_sequence.ranked_treatments:
        ranks.add(rank)
        fv_tuples = [{
            'factor': x.factor_name.name,
            'value': x.value} for x in
            treatment.factor_values]
        treatments.append(fv_tuples)
    len_full_factorial = len(list(itertools.product(*factors_dict.values())))
    len_treatment_sequence = len(treatment_sequence.ranked_treatments)
    is_full_factorial = len_full_factorial == len_treatment_sequence

    report = {
        'full_factorial': is_full_factorial,
        'number_of_factors': len(factors_dict.keys()),
        'number_of_factor_levels_per_factor': factors_dict,
        'number_of_treatments': len(treatment_sequence.ranked_treatments),
        'length_of_treatment_sequence': len(ranks),
        'list_of_treatments': treatments,
        'number_of_treatment': len(treatments)
    }
    return report
"""
