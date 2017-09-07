"""Model objects for storing study design settings, for consumption by
function or factory to create ISA model objects.
"""
from __future__ import absolute_import
import datetime
import itertools
import logging
import random
import uuid
from collections import Iterable
from collections import OrderedDict
from json import JSONEncoder
from operator import itemgetter
from numbers import Number

from isatools import config
from isatools.model import *


logging.basicConfig(level=config.log_level)
log = logging.getLogger(__name__)

__author__ = 'massi'

INTERVENTIONS = dict(CHEMICAL='chemical intervention',
                     BEHAVIOURAL='behavioural intervention',
                     SURGICAL='surgical intervention',
                     BIOLOGICAL='biological intervention',
                     RADIOLOGICAL='radiological intervention')

FACTOR_TYPES = dict(AGENT_VALUES='agent values',
                    INTENSITY_VALUES='intensity values',
                    DURATION_VALUES='duration values')

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
    dict(
        name='DURATION', type=OntologyAnnotation(term="time"),
        display_singular='DURATION VALUE',
        display_plural='DURATION VALUES', values=set()
    )
]

BASE_FACTORS = [
    StudyFactor(name=BASE_FACTORS_[0]['name'],
                factor_type=BASE_FACTORS_[0].get('type', None)),
    StudyFactor(name=BASE_FACTORS_[1]['name'],
                factor_type=BASE_FACTORS_[1].get('type', None)),
    StudyFactor(name=BASE_FACTORS_[2]['name'],
                factor_type=BASE_FACTORS_[2].get('type', None)),
]


class Treatment(object):
    """
    A Treatment is defined as a tuple of factor values (as defined in the ISA
    model v1) and a treatment type
    """
    def __init__(self, treatment_type=INTERVENTIONS['CHEMICAL'],
                 factor_values=None):
        """
        Creates a new Treatment
        :param factor_values: tuple of isatools.model.v1.FactorValue
        """

        if treatment_type not in INTERVENTIONS.values():
            raise ValueError('invalid treatment type provided: ')

        self.__treatment_type = treatment_type

        if factor_values is None:
            self.__factor_values = ()
        else:
            self.factor_values = factor_values

    def __repr__(self):
        return 'Treatment(factor_type={0}, factor_values={1})'.format(
            self.treatment_type, self.factor_values)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, Treatment) \
               and self.treatment_type == other.treatment_type \
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
        if isinstance(factor_values, tuple) \
                and all([isinstance(factor_value, FactorValue)
                         for factor_value in factor_values]):
            self.__factor_values = factor_values
        else:
            raise TypeError('Data supplied is not correctly formatted for '
                            'Treatment')


class TreatmentFactory(object):

    def __init__(self, intervention_type=INTERVENTIONS['CHEMICAL'],
                 factors=BASE_FACTORS):

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
        Computes the ful factorial design on the basis of the stored factor and
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
        :param ranked_treatments: Treatment or list of Treatments of list of
               tuples (Treatment, int) where the second term represents the
               epoch
        """
        self.__ranked_treatments = set()
        # self.__subject_count = subject_count if isinstance(
        # subject_count, int) and subject_count >= 0 else 0
        # self.__sample_map = {}

        self.add_multiple_treatments(ranked_treatments)

    def __repr__(self):
        return 'TreatmentSequence({0})'.format(
            sorted(self.ranked_treatments, key=itemgetter(1)))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return isinstance(other, TreatmentSequence) \
               and self.ranked_treatments == other.ranked_treatments

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

    def __init__(self, distinct_libraries=0, array_designs=None,
                 injection_modes=None, acquisition_modes=None,
                 pulse_sequences=None, technical_replicates=1,
                 instruments=None, chromatography_instruments=None):
        
        self.__distinct_libraries = distinct_libraries
        
        if array_designs is None:
            self.__array_designs = set()
        else:
            self.array_designs = array_designs
            
        if injection_modes is None:
            self.__injection_modes = set()
        else:
            self.injection_modes = injection_modes
        
        if acquisition_modes is None:
            self.__acquisition_modes = set()
        else:
            self.acquisition_modes = acquisition_modes
        
        if pulse_sequences is None:  # only applies to NMR
            self.__pulse_sequences = set()
        else:
            self.pulse_sequences = pulse_sequences
            
        self.__technical_replicates = technical_replicates
        
        if instruments is None:  # scanning instruments
            self.__instruments = set()
        else:
            self.instruments = instruments
            
        if chromatography_instruments is None:  # chromatography instruments
            self.__chromatography_instruments = set()
        else:
            self.chromatography_instruments = chromatography_instruments

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
    def technical_replicates(self):
        return self.__technical_replicates

    @technical_replicates.setter
    def technical_replicates(self, val):
        if not isinstance(val, int):
            raise TypeError('{0} is an invalid value for technical_replicates. '
                            'Please provide an integer.')
        if val < 1:
            raise ValueError('injection_modes must be greater than 0.')
        self.__technical_replicates = val

    @property
    def instruments(self):
        return self.__instruments

    @instruments.setter
    def instruments(self, val):
        if not isinstance(val, set):
            raise TypeError('{0} is an invalid value for instruments. '
                            'Please provide an set of string.')
        if not all(isinstance(x, str) for x in val):
            raise ValueError('all instruments need to be of type string')
        self.__instruments = val
        
    @property
    def chromatography_instruments(self):
        return self.__chromatography_instruments

    @chromatography_instruments.setter
    def chromatography_instruments(self, val):
        if not isinstance(val, set):
            raise TypeError('{0} is an invalid value for chromatography_'
                            'instruments. Please provide an set of string.')
        if not all(isinstance(x, str) for x in val):
            raise ValueError('all chromatography instruments need to be of '
                             'type string')
        self.__chromatography_instruments = val

    def __repr__(self):
        return 'AssayTopologyModifiers(' \
               'distinct_libraries={0}, ' \
               'array_designs={1}, ' \
               'injection_modes={2}, ' \
               'acquisition_modes={3}, ' \
               'pulse_sequences={4}, ' \
               'technical_replicates={5}, ' \
               'instruments={6}, ' \
               'chromatography_instruments={7})'.format(
                self.distinct_libraries,
                sorted(self.array_designs),
                sorted(self.injection_modes),
                sorted(self.acquisition_modes),
                sorted(self.pulse_sequences),
                self.technical_replicates,
                sorted(self.instruments),
                sorted(self.chromatography_instruments)
                )

    def __hash__(self):
        return hash(repr(self))

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return isinstance(other, AssayTopologyModifiers) \
               and self.distinct_libraries == other.distinct_libraries \
               and self.array_designs == other.array_designs \
               and self.injection_modes == other.injection_modes \
               and self.acquisition_modes == other.acquisition_modes \
               and self.pulse_sequences == other.pulse_sequences \
               and self.technical_replicates == other.technical_replicates \
               and self.instruments == other.instruments \
               and self.chromatography_instruments == \
               other.chromatography_instruments


class SampleAssayPlan(object):
    def __init__(self, group_size=0, sample_plan=None, assay_plan=None,
                 sample_qc_plan=None):
        # TODO test initialization from sample_plan and assay_plan!!
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

    @property
    def sample_qc_plan(self):
        return self.__sample_qc_plan

    @sample_qc_plan.setter
    def sample_qc_plan(self, val):
        for sample_type, injection_interval in val.items():
            self.add_sample_qc_plan_record(sample_type, injection_interval)

class BaseStudyDesign(object):
    pass


class InterventionStudyDesign(BaseStudyDesign):

    def __init__(self):
        super().__init__()
        self.__sequences_plan = {}

    @property
    def sequences_plan(self):
        return self.__sequences_plan if self.__sequences_plan else OrderedDict()

    @sequences_plan.setter
    def sequences_plan(self, sequences_plan):
        if not isinstance(sequences_plan, dict):
            raise TypeError('{0} is not a valid input. please provide a '
                            'dictionary mapping Treatment Sequences to'
                            'Sample Plans')
        for treatment_sequence, sample_plan in sequences_plan.items():
            self.add_single_sequence_plan(treatment_sequence, sample_plan)

    def add_single_sequence_plan(self, treatment_sequence, study_plan):
        if not isinstance(treatment_sequence, TreatmentSequence):
            raise TypeError('Please provide a valid TreatmentSequence. '
                            '{0} not a valid Treatment Sequence.'
                            .format([treatment_sequence]))
        if not isinstance(study_plan, SampleAssayPlan):
            raise TypeError('Please provide a valid SampleAssayPlan. {0} not a '
                            'valid SampleAssayPlan.'.format(study_plan))
        self.__sequences_plan[treatment_sequence] = study_plan


class IsaModelObjectFactory(object):

    def __init__(self, sample_assay_plan, treatment_sequence=None):
        self.__sample_assay_plan = sample_assay_plan
        if treatment_sequence is None:
            self.__treatment_sequence = set()
        else:
            self.__treatment_sequence = treatment_sequence

        self.__ops = ['Alice', 'Bob', 'Carol', 'Dan', 'Erin', 'Frank']
        random.shuffle(self.__ops)

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
    def ops(self):
        """Shuffles every time it is called, so use it once in context if you
        want to preserve the current order"""
        return self.__ops

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
    def treatment_sequence(self, treatment_sequence):  # TODO: Implement repeated measure writer
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

        sample_count = 0

        for group_id, fvs, rank in groups_ids:
            collection_event_rank = Characteristic(
                category=collection_event_rank_characteristic,
                value=rank)
            for subjn in range(group_size):
                material_type = Characteristic(
                    category=OntologyAnnotation(
                        term='Material Type'),
                    value=OntologyAnnotation(term='specimen'))
                source = Source(name=self._idgen(group_id, subjn))
                source.characteristics = [material_type]
                sources.append(source)
                for sample_type, sampling_size in sample_plan.items():
                    for sampn in range(0, sampling_size):
                        try:
                            qc_material_type = next(
                                iter(self.sample_assay_plan
                                     .sample_qc_plan.keys()))

                            if sample_count % self.sample_assay_plan\
                                .sample_qc_plan[qc_material_type] == 0:
                                # insert QC sample collection
                                qcsource = Source(
                                    name=self._idgen(group_id, subjn) + '_qc')
                                qcsource.characteristics = [qc_material_type]
                                sources.append(qcsource)

                                sample = Sample(
                                    name=self._idgen(
                                        group_id, subjn,
                                        'qc', qc_material_type.value.term))
                                sample.derives_from = [qcsource]
                                samples.append(sample)

                                process = Process(executes_protocol=study.get_prot(
                                    'sample collection'), inputs=[qcsource],
                                    outputs=[sample], performer=self.ops[0], date_=
                                    datetime.date.isoformat(
                                        datetime.datetime.now()),
                                parameter_values=[ParameterValue(
                                    category=ProtocolParameter(
                                        parameter_name=OntologyAnnotation(
                                            term='Run Order')),
                                    value=str(sample_count))])
                                process_sequence.append(process)
                        except StopIteration:
                            pass  # if no QC plan
                        # normal sample collection
                        sample = Sample(name=self._idgen(
                            group_id, subjn, sampn, sample_type.value.term),
                            factor_values=fvs)
                        sample.characteristics = [sample_type,
                                                  collection_event_rank]
                        sample.derives_from = [source]
                        samples.append(sample)
                        sample_count += 1

                        process = Process(executes_protocol=study.get_prot(
                            'sample collection'), inputs=[source],
                            outputs=[sample], performer=self.ops[0], date_=
                            datetime.date.isoformat(datetime.datetime.now()),
                        parameter_values=[ParameterValue(
                            category=ProtocolParameter(
                                parameter_name=OntologyAnnotation(
                                    term='Run Order')),
                            value=str(sample_count))])
                        process_sequence.append(process)
        study.sources = sources
        study.samples = samples
        study.process_sequence = process_sequence
        return study

    def create_ms_assays_from_plan(self):
        study = self.create_study_from_plan()
        if self.sample_assay_plan.assay_plan == {}:
            raise ISAModelAttributeError('assay_plan is not defined')

        for stype, atype in self.sample_assay_plan.assay_plan:

            if atype.measurement_type.term != 'metabolite profiling':
                raise ISAModelAttributeError('Measurement type must be of type '
                                             '"metabolite profiling"')

            # first get all samples of stype
            samples_stype = [x for x in study.samples if
                             stype in x.characteristics]
            for inj_mode, acq_mode in itertools.product(
                    atype.topology_modifiers.injection_modes,
                    atype.topology_modifiers.acquisition_modes):
                random.shuffle(self.__ops)

                assay = Assay(measurement_type=atype.measurement_type,
                              technology_type=atype.technology_type,
                              filename='a_mp_{0}_{1}_assay.txt'.format(
                                  inj_mode, acq_mode))
                mp_protocol_name = None
                if atype.technology_type.term == 'mass spectrometry':
                    try:
                        study.add_prot(
                            protocol_name='metabolite extraction',
                            protocol_type='extraction')
                    except ISAModelAttributeError:
                        pass
                    ext_protocol = study.get_prot('metabolite extraction')
                    if inj_mode in ('LC', 'GC'):
                        try:
                            ext_protocol.add_param('chromatography instrument')
                        except ISAModelAttributeError:
                            pass
                        try:
                            ext_protocol.add_param('chromatography column')
                        except ISAModelAttributeError:
                            pass
                        try:
                            ext_protocol.add_param('elution program')
                        except ISAModelAttributeError:
                            pass

                    mp_protocol_name = '{0}-{1} mass spectrometry' \
                        .format(inj_mode, acq_mode)
                    try:
                        study.add_prot(protocol_name=mp_protocol_name,
                                       protocol_type='mass spectrometry',
                                       use_default_params=True)
                    except ISAModelAttributeError:
                        pass
                    ms_prot = study.get_prot(mp_protocol_name)
                    try:
                        ms_prot.add_param('randomized run order')
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

                    num_samples_in_stype = len(samples_stype)
                    technical_replicates = \
                        atype.topology_modifiers.technical_replicates
                    total_expected_runs = \
                        num_samples_in_stype * technical_replicates
                    run_order = list(range(0, total_expected_runs))
                    random.shuffle(run_order)  # does random shuffle inplace
                    run_counter = 0

                    for i, samp in enumerate(samples_stype):
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
                        if inj_mode in ('LC', 'GC'):
                            eproc.parameter_values.append(
                                ParameterValue(
                                    category=ext_protocol.get_param(
                                        'chromatography instrument'),
                                    value=next(
                                        iter(atype.topology_modifiers
                                             .chromatography_instruments))
                                )
                            )
                            eproc.parameter_values.append(
                                ParameterValue(
                                    category=ext_protocol.get_param(
                                        'chromatography column'),
                                    value='AB Hydroxyapatite'
                                )
                            )
                            eproc.parameter_values.append(
                                ParameterValue(
                                    category=ext_protocol.get_param(
                                        'elution program'),
                                    value='Acetonitrile 90%, water 10% for 30 '
                                          'min, flow rate: 1ml/min'
                                )
                            )
                        assay.process_sequence.append(eproc)
                        for j in range(0, technical_replicates):
                            ms_prot = study.get_prot(mp_protocol_name)
                            aproc = Process(executes_protocol=ms_prot,
                                            name='assay-name-{0}_run-{1}'
                                            .format(i, j),
                                            inputs=[extr],
                                            performer=self.ops[2],
                                            date_=datetime.date.isoformat(
                                                datetime.date.today()))
                            aproc.parameter_values = [
                                ParameterValue(category=ms_prot.get_param(
                                    'randomized run order'),
                                    value=str(run_counter)),
                                ParameterValue(category=ms_prot.get_param(
                                    'injection mode'), value=inj_mode),
                                ParameterValue(
                                    category=ms_prot.get_param('instrument'),
                                    value=next(
                                        iter(atype.topology_modifiers
                                             .instruments))
                                ),
                                ParameterValue(category=ms_prot.get_param(
                                    'scan polarity'), value=acq_mode),
                            ]
                            run_counter += 1
                            plink(eproc, aproc)
                            dfile = RawSpectralDataFile(
                                filename=
                                'acquired-data-{0}_platform-{1}_{2}_run-{3}'
                                '.mzml.gz'.format(i, inj_mode, acq_mode, j))
                            assay.data_files.append(dfile)
                            aproc.outputs = [dfile]
                            assay.process_sequence.append(aproc)
                    if assay is not None:
                        study.assays.append(assay)
        return study

    def create_nmr_assays_from_plan(self):
        study = self.create_study_from_plan()

        if self.sample_assay_plan.assay_plan == {}:
            raise ISAModelAttributeError('assay_plan is not defined')

        for stype, atype in self.sample_assay_plan.assay_plan:

            if atype.technology_type.term == 'nmr spectroscopy':
                if atype.measurement_type.term != 'metabolite profiling':
                    raise ISAModelAttributeError(
                        'Measurement type must be of type '
                        '"metabolite profiling"')
                samples_stype = [x for x in study.samples if
                                 stype in x.characteristics]
                for pulse_seq, acq_mode in itertools.product(
                        atype.topology_modifiers.pulse_sequences,
                        atype.topology_modifiers.acquisition_modes):
                    random.shuffle(self.__ops)

                    assay = Assay(measurement_type=atype.measurement_type,
                                  technology_type=atype.technology_type,
                                  filename='a_nmr_{0}_{1}_assay.txt'.format(
                                      acq_mode, pulse_seq))

                    if atype.technology_type.term == 'nmr spectroscopy':
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
                            nmr_prot.add_param('randomized run order')
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

                        num_samples_in_stype = len(samples_stype)
                        technical_replicates = \
                            atype.topology_modifiers.technical_replicates
                        total_expected_runs = \
                            num_samples_in_stype * technical_replicates
                        run_order = list(range(0, total_expected_runs))
                        random.shuffle(run_order)  # does random shuffle inplace
                        run_counter = 0

                        for i, samp in enumerate(samples_stype):
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
                            for j in range(0, technical_replicates):
                                nmr_prot = study.get_prot(mp_protocol_name)
                                aproc = Process(executes_protocol=nmr_prot,
                                                name='assay-name-{0}_run-{1}'
                                                .format(i, j),
                                                inputs=[extr],
                                                performer=self.ops[2],
                                                date_=datetime.date.isoformat(
                                                    datetime.date.today()))
                                aproc.parameter_values = [
                                    ParameterValue(category=nmr_prot.get_param(
                                        'randomized run order'),
                                        value=str(run_counter)),
                                    ParameterValue(category=nmr_prot.get_param(
                                        'acquisition mode'), value=acq_mode),
                                    ParameterValue(category=nmr_prot.get_param(
                                        'instrument'), value=next(
                                        iter(atype.topology_modifiers
                                             .instruments))),
                                    ParameterValue(category=nmr_prot.get_param(
                                        'pulse sequence'), value=pulse_seq),
                                ]
                                run_counter += 1
                                plink(eproc, aproc)
                                dfile = RawSpectralDataFile(
                                    filename=
                                    'acquired-data-{0}_platform-{1}_{2}_run-{3}'
                                    '.zip'.format(i, acq_mode, pulse_seq, j))
                                assay.data_files.append(dfile)
                                aproc.outputs = [dfile]
                                assay.process_sequence.append(aproc)

                    if assay is not None:
                        study.assays.append(assay)
        return study

    def create_microarray_assays_from_plan(self):
        study = self.create_study_from_plan()
        if self.sample_assay_plan.assay_plan == {}:
            raise ISAModelAttributeError('assay_plan is not defined')
        for stype, atype in self.sample_assay_plan.assay_plan:
            # first get all samples of stype
            samples_filtered_on_stype = [x for x in study.samples if
                                         stype in x.characteristics]

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
                        assay.filename = 'a_tp_{0}_assay.txt'\
                            .format('_'.join(atype.topology_modifiers
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
                        assay.filename = 'a_ngs_{0}_assay.txt'\
                            .format('_'.join(atype.topology_modifiers
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
        if self.sample_assay_plan.assay_plan == {}:
            raise ISAModelAttributeError('assay_plan is not defined')

        for stype, atype in self.sample_assay_plan.assay_plan:

            # first get all samples of stype
            samples_stype = [x for x in study.samples if
                             stype in x.characteristics]
            if atype.measurement_type.term == 'metabolite profiling' \
                    and atype.technology_type.term == 'mass spectrometry':
                for inj_mode, acq_mode in itertools.product(
                        atype.topology_modifiers.injection_modes,
                        atype.topology_modifiers.acquisition_modes):
                    random.shuffle(self.__ops)

                    assay = Assay(measurement_type=atype.measurement_type,
                                  technology_type=atype.technology_type,
                                  filename='a_ms_{0}_{1}_assay.txt'.format(
                                      inj_mode, acq_mode))
                    try:
                        study.add_prot(
                            protocol_name='metabolite extraction',
                            protocol_type='extraction')
                    except ISAModelAttributeError:
                        pass
                    ext_protocol = study.get_prot('metabolite extraction')
                    if inj_mode in ('LC', 'GC'):
                        try:
                            ext_protocol.add_param('chromatography instrument')
                        except ISAModelAttributeError:
                            pass
                        try:
                            ext_protocol.add_param('chromatography column')
                        except ISAModelAttributeError:
                            pass
                        try:
                            ext_protocol.add_param('elution program')
                        except ISAModelAttributeError:
                            pass

                    mp_protocol_name = '{0}-{1} mass spectrometry' \
                        .format(inj_mode, acq_mode)
                    try:
                        study.add_prot(protocol_name=mp_protocol_name,
                                       protocol_type='mass spectrometry',
                                       use_default_params=True)
                    except ISAModelAttributeError:
                        pass
                    ms_prot = study.get_prot(mp_protocol_name)
                    try:
                        ms_prot.add_param('randomized run order')
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

                    num_samples_in_stype = len(samples_stype)
                    technical_replicates = \
                        atype.topology_modifiers.technical_replicates
                    total_expected_runs = \
                        num_samples_in_stype * technical_replicates
                    run_order = list(range(0, total_expected_runs))
                    random.shuffle(run_order)  # does random shuffle inplace
                    run_counter = 0

                    for i, samp in enumerate(samples_stype):
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
                        if inj_mode in ('LC', 'GC'):
                            eproc.parameter_values.append(
                                ParameterValue(
                                    category=ext_protocol.get_param(
                                        'chromatography instrument'),
                                    value=next(
                                        iter(atype.topology_modifiers
                                             .chromatography_instruments))
                                )
                            )
                            eproc.parameter_values.append(
                                ParameterValue(
                                    category=ext_protocol.get_param(
                                        'chromatography column'),
                                    value='AB Hydroxyapatite'
                                )
                            )
                            eproc.parameter_values.append(
                                ParameterValue(
                                    category=ext_protocol.get_param(
                                        'elution program'),
                                    value='Acetonitrile 90%, water 10% for 30 '
                                          'min, flow rate: 1ml/min'
                                )
                            )
                        assay.process_sequence.append(eproc)
                        for j in range(0, technical_replicates):
                            ms_prot = study.get_prot(mp_protocol_name)
                            aproc = Process(executes_protocol=ms_prot,
                                            name='assay-name-{0}_run-{1}'
                                            .format(i, j),
                                            inputs=[extr],
                                            performer=self.ops[2],
                                            date_=datetime.date.isoformat(
                                                datetime.date.today()))
                            aproc.parameter_values = [
                                ParameterValue(category=ms_prot.get_param(
                                    'randomized run order'),
                                    value=str(run_counter)),
                                ParameterValue(category=ms_prot.get_param(
                                    'injection mode'), value=inj_mode),
                                ParameterValue(
                                    category=ms_prot.get_param('instrument'),
                                    value=next(
                                        iter(atype.topology_modifiers
                                             .instruments))
                                ),
                                ParameterValue(category=ms_prot.get_param(
                                    'scan polarity'), value=acq_mode),
                            ]
                            run_counter += 1
                            plink(eproc, aproc)
                            dfile = RawSpectralDataFile(
                                filename=
                                'acquired-data-{0}_platform-{1}_{2}_run-{3}'
                                '.mzml.gz'.format(i, inj_mode, acq_mode, j))
                            assay.data_files.append(dfile)
                            aproc.outputs = [dfile]
                            assay.process_sequence.append(aproc)
                    if assay is not None:
                        study.assays.append(assay)

            elif atype.measurement_type.term == 'metabolite profiling' \
                    and atype.technology_type.term == 'nmr spectroscopy':
                for pulse_seq, acq_mode in itertools.product(
                        atype.topology_modifiers.pulse_sequences,
                        atype.topology_modifiers.acquisition_modes):
                    random.shuffle(self.__ops)

                    assay = Assay(measurement_type=atype.measurement_type,
                                  technology_type=atype.technology_type,
                                  filename='a_nmr_{0}_{1}_assay.txt'.format(
                                      acq_mode, pulse_seq))

                    if atype.technology_type.term == 'nmr spectroscopy':
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
                            nmr_prot.add_param('randomized run order')
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

                        num_samples_in_stype = len(samples_stype)
                        technical_replicates = \
                            atype.topology_modifiers.technical_replicates
                        total_expected_runs = \
                            num_samples_in_stype * technical_replicates
                        run_order = list(range(0, total_expected_runs))
                        random.shuffle(run_order)  # does random shuffle inplace
                        run_counter = 0

                        for i, samp in enumerate(samples_stype):
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
                            for j in range(0, technical_replicates):
                                nmr_prot = study.get_prot(mp_protocol_name)
                                aproc = Process(executes_protocol=nmr_prot,
                                                name='assay-name-{0}_run-{1}'
                                                .format(i, j),
                                                inputs=[extr],
                                                performer=self.ops[2],
                                                date_=datetime.date.isoformat(
                                                    datetime.date.today()))
                                aproc.parameter_values = [
                                    ParameterValue(category=nmr_prot.get_param(
                                        'randomized run order'),
                                        value=str(run_counter)),
                                    ParameterValue(category=nmr_prot.get_param(
                                        'acquisition mode'), value=acq_mode),
                                    ParameterValue(category=nmr_prot.get_param(
                                        'instrument'), value=next(
                                        iter(atype.topology_modifiers
                                             .instruments))),
                                    ParameterValue(category=nmr_prot.get_param(
                                        'pulse sequence'), value=pulse_seq),
                                ]
                                run_counter += 1
                                plink(eproc, aproc)
                                dfile = RawSpectralDataFile(
                                    filename=
                                    'acquired-data-{0}_platform-{1}_{2}_run-{3}'
                                    '.zip'.format(i, acq_mode, pulse_seq, j))
                                assay.data_files.append(dfile)
                                aproc.outputs = [dfile]
                                assay.process_sequence.append(aproc)

                    if assay is not None:
                        study.assays.append(assay)
            elif atype.technology_type.term == 'DNA microarray':
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
                        assay.filename = 'a_tp_{0}_assay.txt' \
                            .format('_'.join(atype.topology_modifiers
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
                                filename='output-file-{}.sff'.format(
                                    run_count))
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

            elif atype.technology_type.term == 'nucleotide sequencing':
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
                        assay.filename = 'a_ngs_{0}_assay.txt'\
                            .format('_'.join(atype.topology_modifiers
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


class SampleAssayPlanEncoder(JSONEncoder):

    def get_top_mods(self, o):
        return {
            'distinct_libraries': o.distinct_libraries,
            'array_designs': sorted(o.array_designs),
            'injection_modes': sorted(o.injection_modes),
            'acquisition_modes': sorted(o.acquisition_modes),
            'pulse_sequences': sorted(o.pulse_sequences),
            'technical_replicates': o.technical_replicates,
            'instruments': sorted(o.instruments),
            'chromatography_instruments': sorted(
                o.chromatography_instruments)
        }

    def get_assay_type(self, o):
        return {
            'measurement_type': o.measurement_type.term
            if o.measurement_type else '',
            'technology_type': o.technology_type.term
            if o.technology_type else '',
            'topology_modifiers': self.get_top_mods(o.topology_modifiers)
            if o.topology_modifiers else []
        }

    def get_sample_plan(self, sample_plan):
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

    def get_sample_qc_plan(self, sample_qc_plan):
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
        if isinstance(o, AssayTopologyModifiers):
            return self.get_top_mods(o)
        elif isinstance(o, AssayType):
            return self.get_assay_type(o)
        elif isinstance(o, SampleAssayPlan):
            return {
                'group_size': o.group_size,
                'sample_types': sorted([x.value.term for x in o.sample_types]),
                'assay_types': sorted([self.get_assay_type(x) for x in o.assay_types]),
                'sample_plan': self.get_sample_plan(o.sample_plan),
                'sample_qc_plan': self.get_sample_qc_plan(o.sample_qc_plan),
                'assay_plan': self.get_assay_plan(o.assay_plan)
            }