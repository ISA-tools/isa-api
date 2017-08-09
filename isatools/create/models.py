"""Model objects for storing study design settings, for consumption by
function or factory to create ISA model objects.
"""
from __future__ import absolute_import
import datetime
import itertools
import logging
import uuid
from collections import Iterable
from collections import OrderedDict
from operator import itemgetter
from numbers import Number

from isatools import config
from isatools.model import *


logging.basicConfig(level=config.log_level)
log = logging.getLogger(__name__)

__author__ = 'massi'

INTERVENTIONS = dict(CHEMICAL='chemical intervention', BEHAVIOURAL='behavioural intervention',
                     SURGICAL='surgical intervention', BIOLOGICAL='biological intervention',
                     RADIOLOGICAL='radiological intervention')

FACTOR_TYPES = dict(AGENT_VALUES='agent values', INTENSITY_VALUES='intensity values', DURATION_VALUES='duration values')

BASE_FACTORS_ = [
    dict(
        name='AGENT', type=OntologyAnnotation(term="perturbation agent"), display_singular='AGENT VALUE',
        display_plural='AGENT VALUES', values=set()
    ),
    dict(
        name='INTENSITY', type=OntologyAnnotation(term="intensity"), display_singular='INTENSITY VALUE',
        display_plural='INTENSITY VALUES', values=set()
    ),
    dict(
        name='DURATION', type=OntologyAnnotation(term="time"), display_singular='DURATION VALUE',
        display_plural='DURATION VALUES', values=set()
    )
]

BASE_FACTORS = [
    StudyFactor(name=BASE_FACTORS_[0]['name'], factor_type=BASE_FACTORS_[0].get('type', None)),
    StudyFactor(name=BASE_FACTORS_[1]['name'], factor_type=BASE_FACTORS_[1].get('type', None)),
    StudyFactor(name=BASE_FACTORS_[2]['name'], factor_type=BASE_FACTORS_[2].get('type', None)),
]

""" DEPRECATED
class SamplePlan(object):

    def __init__(self, group_size=0, sample_type_map=None):
        self.__group_size = group_size if isinstance(group_size, int) and group_size > 0 else 0
        self.__sample_types_map = {}

        if sample_type_map:
            self.sample_types_map = sample_type_map

    @property
    def group_size(self):
        return self.__group_size

    @group_size.setter
    def group_size(self, group_size):
        if not isinstance(group_size, int):
            raise TypeError('{0} is not a valid value for group_size. Please provide an integer.')
        if group_size < 0:
            raise ValueError('group_size must be greater than 0.')
        self.__group_size = group_size

    @property
    def sample_types_map(self):
        return self.__sample_types_map

    @sample_types_map.setter
    def sample_types_map(self, sample_types_map):
        for sample_type, sampling_size in sample_types_map.items():
            self.add_sample_type_sampling_plan(sample_type, sampling_size)

    def add_sample_type_sampling_plan(self, sample_type, sampling_size=0):
        
        
        :param sample_type: (Characteristic/str) a sample type
        :param sampling_size: (int/tuple of int) for the provided sample type how many sampling events happen for a single
                                                 source/subject. This can be specified throughout the whole sequence with
                                                 a single integer value, or with a tuple of value, each value for an 
                                                 epoch. Missing values will be considered as zero (no sampling.
        :return: 
        
        if not isinstance(sampling_size, int) and not isinstance(sampling_size, tuple):
            raise TypeError('sampling_size must be a natural number or a tuple of natural numbers')
        if isinstance(sampling_size, int) and sampling_size < 0:
            raise ValueError('sampling_size value must be a positive integer')
        if isinstance(sampling_size, tuple) and not all(isinstance(el, int) and el >= 0 for el in sampling_size):
            raise ValueError('all values in the sampling_size tuple must be positive integers')
        if isinstance(sample_type, Characteristic):
            self.__sample_types_map[sample_type] = sampling_size
        elif isinstance(sample_type, str):  # TODO should we remove this case?
            characteristic = Characteristic(category=OntologyAnnotation(term='organism part'),
                                            value=OntologyAnnotation(term=sample_type))
            self.__sample_types_map[characteristic] = sampling_size
        else:
            raise TypeError('wrong sample type {0}'.format(sample_type))

    @property
    def sample_types(self):
        return {sample_type for sample_type in self.__sample_types_map}
"""


class Treatment(object):
    """
    A Treatment is defined as a tuple of factor values (as defined in the ISA model v1) and a treatment type
    """
    def __init__(self, treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=()):
        """
        Creates a new Treatment
        :param factor_values: tuple of isatools.model.v1.FactorValue
        """

        if treatment_type not in INTERVENTIONS.values():
            raise ValueError('invalid treatment type provided: ')

        self.__treatment_type = treatment_type
        self.__factor_values = ()

        self.factor_values = factor_values

    def __repr__(self):
        return 'Treatment(factor_type={0}, factor_values={1})'.format(self.treatment_type, self.factor_values)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Treatment) and self.treatment_type == other.treatment_type \
               and self.factor_values == other.factor_values

    def __ne__(self, other):
        return not self == other

    @property
    def treatment_type(self):
        return self.__treatment_type

    @treatment_type.setter
    def treatment_type(self, treatment_type):
        if treatment_type in INTERVENTIONS.values():
            self.__treatment_type = treatment_type
        else:
            raise ValueError('invalid treatment type provided: ')

    @property
    def factor_values(self):
        return self.__factor_values

    @factor_values.setter
    def factor_values(self, factor_values=()):
        if isinstance(factor_values, tuple) and all([isinstance(factor_value, FactorValue)
                                                     for factor_value in factor_values]):
            self.__factor_values = factor_values
        else:
            raise TypeError('Data supplied is not correctly formatted for Treatment')


class TreatmentFactory(object):

    def __init__(self, intervention_type=INTERVENTIONS['CHEMICAL'], factors=BASE_FACTORS):

        if intervention_type not in INTERVENTIONS.values():
            raise ValueError('invalid treatment type provided: ')

        self.__intervention_type = intervention_type
        self.__factors = OrderedDict([(factor, set()) for factor in factors])

        # self._factorial_design = set()

    @property
    def intervention_type(self):
        return self.__intervention_type

    @property
    def factors(self):
        return self.__factors

    def add_factor_value(self, factor, factor_value):
        """
        Add a single factor value or a list of factor value to the relevant set set
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
            raise KeyError('The factor {} is not present in the design'.format(factor.name))

    def compute_full_factorial_design(self):
        """
        Computes the ful factorial design on the basis of the stored factor and factor values.
        If one of the factors has no associated values an empty set is returned
        :return: set - the full factorial design as a set of Treatments
        """
        factor_values = [
            [FactorValue(factor_name=factor_name, value=value, unit=None) for value in values]
            for factor_name, values in self.factors.items()
        ]
        if set() not in self.factors.values():
            return {Treatment(treatment_type=self.intervention_type,
                              factor_values=treatment_factors)
                    for treatment_factors in itertools.product(*factor_values)}
        else:
            return set()


class TreatmentSequence:
    """
    A treatment sequence is an ordered (graph-like) combination of treatment
    """

    def __init__(self, ranked_treatments=[], subject_count=10):
        """
        :param ranked_treatments: Treatment or list of Treatments of list of tuples (Treatment, int) where the second 
               term represents the  epoch
        """
        self.__ranked_treatments = set()
        # self.__subject_count = subject_count if isinstance(subject_count, int) and subject_count >= 0 else 0
        # self.__sample_map = {}

        self.add_multiple_treatments(ranked_treatments)

    def __repr__(self):
        return 'TreatmentSequence({0})'.format(sorted(self.ranked_treatments, key=itemgetter(1)))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, TreatmentSequence) and self.ranked_treatments == other.ranked_treatments

    def __ne__(self, other):
        return not self == other

    @property
    def ranked_treatments(self):
        return self.__ranked_treatments

    @ranked_treatments.setter
    def ranked_treatments(self, ranked_treatments):
        self.add_multiple_treatments(ranked_treatments)

    """
    @property
    def subject_count(self):
        return self.__subject_count if isinstance(self.__subject_count, int) and self.__subject_count >= 0 else 0

    @subject_count.setter
    def subject_count(self, subject_count):
        self.__subject_count = subject_count if isinstance(subject_count, int) and subject_count >= 0 else 0

    @property
    def sample_map(self):
        return self.__sample_map
    """

    def add_multiple_treatments(self, elements_to_add):
        if isinstance(elements_to_add, Treatment):
            self.add_treatment(elements_to_add)
        elif isinstance(elements_to_add, Iterable):
            for elem in elements_to_add:
                if isinstance(elem, Treatment):
                    self.add_treatment(elem)
                elif isinstance(elem, tuple):
                    self.add_treatment(*elem)
                else:
                    raise TypeError('The argument {0} is not of the correct type.'.format(elem))
        else:
            raise TypeError('The argument {0} is not of the correct type.'.format(elements_to_add))

    def add_treatment(self, treatment, epoch=1):
        if isinstance(treatment, Treatment) and isinstance(epoch, int):
            # TODO check epoch
            self.__ranked_treatments.add((treatment, epoch))


class AssayType(object):

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

        if isinstance(topology_modifiers, AssayTopologyModifiers):
            self.__topology_modifiers = topology_modifiers
        elif topology_modifiers is None:
            self.__topology_modifiers = None
        else:
            raise TypeError('{0} is an invalid value for topology_modifiers. '
                            'Please provide a AssayTopologyModifiers object.'
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
        if isinstance(topology_modifiers, AssayTopologyModifiers):
            self.__topology_modifiers = topology_modifiers
        elif topology_modifiers is None:
            self.__topology_modifiers = None
        else:
            raise TypeError('{0} is an invalid value for measurement_type. '
                            'Please provide a AssayTopologyModifiers object.'
                            .format(topology_modifiers))

    def __repr__(self):
        return 'AssayType(measurement_type={0}, technology_type={1}, ' \
               'topology_modifiers={2})' \
               .format(self.measurement_type, self.technology_type,
                       self.topology_modifiers)

    def __hash__(self):
        return hash(repr(self))

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return isinstance(other, AssayType) \
               and self.measurement_type == other.measurement_type \
               and self.technology_type == other.technology_type


class AssayTopologyModifiers(object):

    def __init__(self, distinct_libraries=0, distinct_array_designs=0,
                 injection_modes=0, acquisition_modes=0, pulse_sequences=0,
                 technical_replicates=0):
        self.__distinct_libraries = distinct_libraries
        self.__distinct_array_designs = distinct_array_designs
        self.__injection_modes = injection_modes
        self.__acquisition_modes = acquisition_modes
        self.__pulse_sequences = pulse_sequences
        self.__technical_replicates = technical_replicates

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

    @property
    def distinct_array_designs(self):
        return self.__distinct_array_designs

    @distinct_array_designs.setter
    def distinct_array_designs(self, distinct_array_designs):
        if not isinstance(distinct_array_designs, int):
            raise TypeError('{0} is an invalid value for distinct_array_'
                            'designs. Please provide an integer.')
        if distinct_array_designs < 0:
            raise ValueError('distinct_array_designs must be greater than 0.')
        self.__distinct_array_designs = distinct_array_designs

    @property
    def injection_modes(self):
        return self.__injection_modes

    @injection_modes.setter
    def injection_modes(self, injection_modes):
        if not isinstance(injection_modes, int):
            raise TypeError('{0} is an invalid value for injection_modes. '
                            'Please provide an integer.')
        if injection_modes < 0:
            raise ValueError('injection_modes must be greater than 0.')
        self.__injection_modes = injection_modes

    @property
    def acquisition_modes(self):
        return self.__acquisition_modes

    @acquisition_modes.setter
    def acquisition_modes(self, acquisition_modes):
        if not isinstance(acquisition_modes, int):
            raise TypeError('{0} is an invalid value for acquisition_modes. '
                            'Please provide an integer.')
        if acquisition_modes < 0:
            raise ValueError('acquisition_modes must be greater than 0.')
        self.__acquisition_modes = acquisition_modes

    @property
    def pulse_sequences(self):
        return self.__pulse_sequences

    @pulse_sequences.setter
    def pulse_sequences(self, pulse_sequences):
        if not isinstance(pulse_sequences, int):
            raise TypeError('{0} is an invalid value for pulse_sequences. '
                            'Please provide an integer.')
        if pulse_sequences < 0:
            raise ValueError('injection_modes must be greater than 0.')
        self.__pulse_sequences = pulse_sequences

    @property
    def technical_replicates(self):
        return self.__technical_replicates

    @technical_replicates.setter
    def technical_replicates(self, technical_replicates):
        if not isinstance(technical_replicates, int):
            raise TypeError('{0} is an invalid value for technical_replicates. '
                            'Please provide an integer.')
        if technical_replicates < 0:
            raise ValueError('injection_modes must be greater than 0.')
        self.__technical_replicates = technical_replicates

    def __repr__(self):
        return 'AssayTopologyModifiers(' \
               'distinct_libraries={0}, ' \
               'distinct_array_designs={1}, ' \
               'injection_modes={2}, ' \
               'acquisition_modes={3}, ' \
               'pulse_sequences={4}, ' \
               'technical_replicates={5})'.format(
                self.distinct_libraries,
                self.distinct_array_designs,
                self.injection_modes,
                self.acquisition_modes,
                self.pulse_sequences,
                self.technical_replicates
                )

    def __hash__(self):
        return hash(repr(self))

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return isinstance(other, AssayTopologyModifiers) \
               and self.distinct_libraries == other.distinct_libraries \
               and self.distinct_array_designs == other.distinct_array_designs \
               and self.injection_modes == other.injection_modes \
               and self.acquisition_modes == other.acquisition_modes \
               and self.pulse_sequences == other.pulse_sequences \
               and self.technical_replicates == other.technical_replicates

"""
class AssayPlan(object):

    def __init__(self, sample_plan=SamplePlan()):
        self.__sample_plan = set()
        self.__assay_types_map = {}
        self.__assay_topologies_map = {}

        self.sample_plan = sample_plan

    @property
    def sample_plan(self):
        return self.__sample_plan

    @sample_plan.setter
    def sample_plan(self, sample_plan):
        if not isinstance(sample_plan, SamplePlan):
            raise TypeError('{0} is an invalid value for sample_plan. Please provide a SamplePlan object.')
        missing_sample_types = { sample_type for sample_type in self.__assay_types_map } - sample_plan.sample_types
        if missing_sample_types != set():
            raise ValueError('Some of the sample_types required by the assay plan are not declared in the sample plan'
                             '{0}'.format(missing_sample_types))
        self.__sample_plan = sample_plan

    @property
    def assay_types_map(self):
        return self.__assay_types_map

    @assay_types_map.setter
    def assay_types_map(self, assay_types_map):
        for sample_type, assay_type in assay_types_map.items():
            self.add_sample_to_assay_type_mapping(sample_type, assay_type)

    def add_sample_to_assay_type_mapping(self, sample_type, assay_type):
        if not isinstance(sample_type, (Characteristic, str)):
            raise TypeError('invalid sample_type {0}'.format(sample_type))
        elif not isinstance(assay_type, AssayType):
            raise TypeError('invalid assay_type {0}'.format(assay_type))
        if isinstance(sample_type, str):
            characteristic = Characteristic(category=OntologyAnnotation(term='organism part'),
                                            value=OntologyAnnotation(term=sample_type))
            if characteristic not in self.sample_plan.sample_types_map.keys():
                print('warning: sample type {0} is not present in the sample plan provided'
                      .format(repr(characteristic)))
            self.__assay_types_map[characteristic] = assay_type
        else:
            self.__assay_types_map[sample_type] = assay_type

    @property
    def assay_topologies_map(self):
        return self.__assay_topologies_map

    @assay_topologies_map.setter
    def assay_topologies_map(self, assay_topologies_map):
        for assay_type, assay_topology_modifiers in assay_topologies_map.items():
            self.set_assay_type_topology(assay_type, assay_topology_modifiers)

    def set_assay_type_topology(self, assay_type, assay_topology_modifiers):
        if isinstance(assay_type, AssayType) and assay_type in self.assay_types_map.keys():
            self.__assay_topologies_map[assay_type] = assay_topology_modifiers
        else:
            raise TypeError('invalid assay_type {0}'.format(assay_topology_modifiers))
        if isinstance(assay_topology_modifiers, AssayTopologyModifiers):
            self.__assay_topologies_map[assay_type] = assay_topology_modifiers
        else:
            raise TypeError('invalid assay_topology_modifiers type {0}'.format(assay_topology_modifiers))
"""


class SampleAssayPlan(object):
    def __init__(self, group_size=0, sample_plan={}, assay_plan=set()):
        # TODO test initialization from sample_plan and assay_plan!!
        self.__group_size = 0
        self.__sample_types = set()
        self.__assay_types = set()
        self.__sample_plan = {}
        self.__assay_plan = set()

        self.group_size = group_size
        if sample_plan is not None:
            self.sample_types = {key for key in sample_plan}
            self.sample_plan = sample_plan
        if assay_plan is not None:
            self.assay_types = {value for key, value in assay_plan}
            self.assay_plan = assay_plan

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
        elif isinstance(sample_type, str):
            characteristic = Characteristic(
                category=OntologyAnnotation(term='organism part'),
                value=OntologyAnnotation(term=sample_type))
            self.__sample_types.add(characteristic)
        else:
            raise TypeError('Not a valid sample type: {0}'.format(sample_type))

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

        :param sample_type: (Characteristic/str) a sample type
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


class BaseStudyDesign(object):
    pass


class InterventionStudyDesign(BaseStudyDesign):

    def __init__(self, sequences_plan=[]):
        super().__init__()
        self.__sequences_plan = {}
        # self.sequences = sequences

    @property
    def sequences_plan(self):
        return self.__sequences_plan if self.__sequences_plan else OrderedDict()

    @sequences_plan.setter
    def sequences_plan(self, sequences_plan):
        if not isinstance(sequences_plan, dict):
            raise TypeError('{0} is not a valid input. please provide a dictionary mapping Treatment Sequences to'
                            'Sample Plans')
        for treatment_sequence, sample_plan in sequences_plan.items():
            self.add_single_sequence_plan(treatment_sequence, sample_plan)

    def add_single_sequence_plan(self, treatment_sequence, study_plan):
        if not isinstance(treatment_sequence, TreatmentSequence):
            raise TypeError('Please provide a valid TreatmentSequence. '
                            '{0} not a valid Treatment Sequence.'.format([treatment_sequence]))
        if not isinstance(study_plan, SampleAssayPlan):
            raise TypeError('Please provide a valid SampleAssayPlan. {0} not a valid SampleAssayPlan.'.format(study_plan))
        self.__sequences_plan[treatment_sequence] = study_plan


class IsaModelObjectFactory(object):

    def __init__(self, sample_assay_plan, treatment_sequence=None):
        self.__sample_assay_plan = sample_assay_plan
        if treatment_sequence is None:
            self.__treatment_sequence = set()
        else:
            self.__treatment_sequence = treatment_sequence

    def _idgen(self, gid='', subn='', samn='', samt=''):
        idarr = []
        if gid != '':
            idarr.append('studygroup_{}'.format(gid))
        if subn != '':
            idarr.append('subject#{}'.format(subn))
        if samn != '':
            idarr.append('sample#{}'.format(samn))
        if samt != '':
            idarr.append(samt)
        return '_'.join(idarr)

    @property
    def sample_assay_plan(self):
        return self.__sample_assay_plan

    @sample_assay_plan.setter
    def sample_assay_plan(self, sample_assay_plan):
        if not isinstance(sample_assay_plan, SampleAssayPlan):
            raise ISAModelAttributeError('sample_assay_plan must be an object'
                                         'of type SampleAssayPlan')
        else:
            self.__sample_assay_plan = sample_assay_plan

    @property
    def treatment_sequence(self):
        return self.__treatment_sequence

    @treatment_sequence.setter
    def treatment_sequence(self, treatment_sequence):
        if not isinstance(treatment_sequence, set):
            raise ISAModelAttributeError('treatment_sequence must be a set '
                                         'of tuples of type (Treatment, int)')
        else:
            self.__treatment_sequence = treatment_sequence

    def create_study_from_plan(self):
        if self.sample_assay_plan is None:
            raise ISAModelAttributeError('sample_assay_plan must be set to '
                                         'create model objects in factory')

        if self.sample_assay_plan.group_size < 1:
            raise ISAModelAttributeError('group_size cannot be less than 1')
        group_size = self.sample_assay_plan.group_size

        if self.sample_assay_plan.sample_plan == {}:
            raise ISAModelAttributeError('sample_plan is not defined')
        sample_plan = self.sample_assay_plan.sample_plan

        groups_ids = [(uuid.uuid4(), x.factor_values, y) for x, y in
                      self.treatment_sequence.ranked_treatments]

        if len(groups_ids) == 0:
            groups_ids = ['']
        sources = []
        samples = []
        process_sequence = []
        study = Study(filename='study.txt')
        study.protocols = [Protocol(name='sample collection', protocol_type=
                                    OntologyAnnotation(term='sample collection')
                                    )]
        collection_event_rank_characteristic = OntologyAnnotation(
            term='collection_event_rank_characteristic')
        study.characteristic_categories.append(
            collection_event_rank_characteristic)
        for group_id, fvs, rank in groups_ids:
            collection_event_rank = Characteristic(
                category=collection_event_rank_characteristic,
                value=rank)
            for subjn in range(group_size):
                source = Source(name=self._idgen(group_id, subjn))
                sources.append(source)
                for sample_type, sampling_size in sample_plan.items():
                    for sampn in range(0, sampling_size):
                        sample = Sample(name=self._idgen(
                            group_id, subjn, sampn, sample_type.value.term),
                            factor_values=fvs)
                        sample.characteristics = [sample_type,
                                                  collection_event_rank]
                        sample.derives_from = [source]
                        samples.append(sample)

                        process = Process(executes_protocol=study.get_prot(
                            'sample collection'), inputs=[source],
                            outputs=[sample], performer='bob', date_=
                            datetime.date.isoformat(datetime.datetime.now()))
                        process_sequence.append(process)
        study.sources = sources
        study.samples = samples
        study.process_sequence = process_sequence
        return study

    def create_assays_from_plan(self):
        study = self.create_study_from_plan()
        study.protocols.append(Protocol(name='metabolite extraction',
                                        protocol_type=OntologyAnnotation(
                                            term='extraction')))
        study.protocols.append(Protocol(name='mass spectrometry',
                                        protocol_type=OntologyAnnotation(
                                            term='mass spectrometry'
                                        )))
        if self.sample_assay_plan.assay_plan == {}:
            raise ISAModelAttributeError('assay_plan is not defined')
        for stype, atype in self.sample_assay_plan.assay_plan:
            # first get all samples of stype
            samples_stype = [x for x in study.samples if
                             stype in x.characteristics]
            assay = Assay(measurement_type=atype.measurement_type,
                          technology_type=atype.technology_type,
                          filename='a_assay.txt')
            for i, samp in enumerate(samples_stype): # do we really need count?
                # build assay path
                extr = Extract(name='{0}_extract-{1}'.format(samp.name, i))
                eproc = Process(executes_protocol=study
                                .get_prot('metabolite extraction'),
                                inputs=[samp], outputs=[extr], performer='bob',
                                date_=datetime.date.isoformat(
                                    datetime.datetime.now()))
                assay.process_sequence.append(eproc)
                for j in range(atype.topology_modifiers.technical_replicates):
                    aproc = Process(executes_protocol=study
                                    .get_prot('mass spectrometry'),
                                    name='assay-name-{0}_run-{1}'.format(i, j),
                                    inputs=[extr])
                    plink(eproc, aproc)
                    dfile = RawSpectralDataFile(filename='{0}{1}'
                                                .format(aproc.name, '.mzml.gz'))
                    aproc.outputs = [dfile]
                    assay.process_sequence.append(aproc)

            study.assays.append(assay)
        return study
