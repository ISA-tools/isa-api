"""
Model objects for storing study design settings, for consumption by
function or factory to create ISA model objects.
"""
from __future__ import absolute_import
import datetime
import itertools
import json
import logging
import random
import uuid
from collections import Iterable
from collections import OrderedDict
from numbers import Number

from isatools.model import *


log = logging.getLogger('isatools')

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
        :param factor_values: set of isatools.model.v1.FactorValue
        """

        if treatment_type not in INTERVENTIONS.values():
            raise ValueError('invalid treatment type provided: ')

        self.__treatment_type = treatment_type

        if factor_values is None:
            self.__factor_values = set()
        else:
            self.factor_values = factor_values

    def __repr__(self):
        return 'Treatment(factor_type={0}, factor_values={1})'.format(
            self.treatment_type, sorted(
                self.factor_values, key=lambda x: repr(x)))

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


class TreatmentSequence:
    """
    A treatment sequence is an ordered (graph-like) combination of treatments (as a list), each with an associated rank.
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
        return 'TreatmentSequence({0})'.format(sorted(self.ranked_treatments, key=lambda x: repr(x)))

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
        """
        Adds multiple treatments to the sequence. To satisfy the epoch criteria,
        the treatments need to be added according to the order/rank determined by the epoch
        number.
        :param elements_to_add:
        :return:
        """
        if isinstance(elements_to_add, Treatment):
            self.add_treatment(elements_to_add)
        elif isinstance(elements_to_add, Iterable):
            if any(True for _ in elements_to_add):
                elems_copy = elements_to_add
                if (isinstance(next(iter(elements_to_add)), tuple)):
                    elements_to_add = sorted(elems_copy, key=lambda x: x[1])
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
        if isinstance(treatment, Treatment):
            if isinstance(epoch, int):
                if self.check_epochs(epoch):
                    self.__ranked_treatments.add((treatment, epoch))
                else:
                    raise TypeError('The epoch number {0} is either not greater than 1 or it does not complete the sequence of epochs, which should start in 1 and have no values missing up to the highest epoch value '.format(epoch))
            else:
                raise TypeError('The arguemnt {0} is not an integer'.format(epoch))
        else:
            raise TypeError('The argument {0} is not a treatment'.format(treatment))



    def check_epochs(self, new_epoch):
        """
        Checks that the list of epochs in the __ranked_treatments have 1 as the lowest value and no value is missing from the lowest to the highest value
        :return: true if the list of epochs satisfies the criteria above, false otherwise
        """
        epoch_list = [x[1] for x in self.__ranked_treatments]
        epoch_list.append(new_epoch)
        if epoch_list.__len__() == 1:
            return (1 in epoch_list)
        try:
            epoch_list = sorted(list(set(epoch_list)))
            it = (x for x in epoch_list)
            first = next(it)
            return any(i == 1 for i in epoch_list) and all(i >= 1 for i in epoch_list) and all(a == b for a, b in enumerate(it, first + 1))
        except StopIteration:
            log.error("StopIteration - shouldn't occur!")

class AssayType(object):
    """
       A type of assay, determined by a measurement_type, a technology_type and a set of topology_modifiers (of type AssayTopologyModifiers).
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


class AssayTopologyModifiers(object):

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


class NMRAssayTopologyModifiers(AssayTopologyModifiers):

    def __init__(self, acquisition_modes=None,
                 pulse_sequences=None, technical_replicates=1,
                 instruments=None, injection_modes=None):
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
        return 'NMRAssayTopologyModifiers(' \
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
        return isinstance(other, NMRAssayTopologyModifiers) \
               and self.injection_modes == other.injection_modes \
               and self.acquisition_modes == other.acquisition_modes \
               and self.pulse_sequences == other.pulse_sequences \
               and self.technical_replicates == other.technical_replicates \
               and self.instruments == other.instruments


class MSAssayTopologyModifiers(AssayTopologyModifiers):

    def __init__(self, acquisition_modes=None,
                 chromatography_instruments=None, technical_replicates=1,
                 instruments=None, injection_modes=None):
        super().__init__(technical_replicates=technical_replicates,
                         instruments=instruments)
        if injection_modes is None:
            self.__injection_modes = set()
        else:
            self.injection_modes = injection_modes
        if acquisition_modes is None:
            self.__acquisition_modes = set()
        else:
            self.acquisition_modes = acquisition_modes
        if chromatography_instruments is None:
            self.__chromatography_instruments = set()
        else:
            self.chromatography_instruments = chromatography_instruments

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
        return 'MSAssayTopologyModifiers(' \
               'technical_replicates={0}, ' \
               'instruments={1}, injection_modes={2}, ' \
               'acquisition_modes={3}, ' \
               'chromatography_instruments={4})'.format(
                self.technical_replicates,
                sorted(self.instruments),
                sorted(self.injection_modes),
                sorted(self.acquisition_modes),
                sorted(self.chromatography_instruments)
                )

    def __hash__(self):
        return hash(repr(self))

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return isinstance(other, MSAssayTopologyModifiers) \
               and self.injection_modes == other.injection_modes \
               and self.acquisition_modes == other.acquisition_modes \
               and self.technical_replicates == other.technical_replicates \
               and self.instruments == other.instruments \
               and self.chromatography_instruments == \
                   other.chromatography_instruments


class DNASeqAssayTopologyModifiers(AssayTopologyModifiers):

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


class DNAMicroAssayTopologyModifiers(AssayTopologyModifiers):

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

    @property
    def pre_run_batch(self):
        return self.__pre_run_batch

    @pre_run_batch.setter
    def pre_run_batch(self, qc_batch_dict):
        pre_run_batch = SampleQCBatch()
        pre_run_batch.material = qc_batch_dict['material']
        var_type = qc_batch_dict['variable_type']
        var_name = qc_batch_dict['variable_name']
        var_values = qc_batch_dict['values']
        if var_type == 'parameter':
            pre_run_batch.parameter_values = list(
                map(lambda x: (var_name, x), var_values))
        elif var_type == 'characteristic':
            pre_run_batch.characteristic_values = list(
                map(lambda x: (var_name, x), var_values))
        self.__pre_run_batch = pre_run_batch
        
    @property
    def post_run_batch(self):
        return self.__post_run_batch

    @post_run_batch.setter
    def post_run_batch(self, qc_batch_dict):
        post_run_batch = SampleQCBatch()
        post_run_batch.material = qc_batch_dict['material']
        var_type = qc_batch_dict['variable_type']
        var_name = qc_batch_dict['variable_name']
        var_values = qc_batch_dict['values']
        if var_type == 'parameter':
            post_run_batch.parameter_values = list(
                map(lambda x: (var_name, x), var_values))
        elif var_type == 'characteristic':
            post_run_batch.characteristic_values = list(
                map(lambda x: (var_name, x), var_values))
        self.__post_run_batch = post_run_batch

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
        self.parameter_values = parameter_values
        self.characteristic_values = characteristic_values


class BaseStudyDesign(object):
    pass


class InterventionStudyDesign(BaseStudyDesign):
    """
    A class representing an intervention study design, which is composed of an
    ordered dictionary of pairs of treatment sequences and samples plans.
    """

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
    """
    A factory class to create ISA content given a SampleAssayPlan object and a TreatmentSequence object.
    """

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
        ranked_treatment_set = set()
        for x, _ in self.treatment_sequence.ranked_treatments:
            ranked_treatment_set.add(x)
        groups_ids = [(uuid.uuid4(), x) for x in ranked_treatment_set]
        ranks = set([y for _, y in self.treatment_sequence.ranked_treatments])

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
        sample_collection.add_param('Run Order')
        study.protocols = [sample_collection]
        collection_event_rank_characteristic = OntologyAnnotation(
            term='collection_event_rank_characteristic')
        study.characteristic_categories.append(
            collection_event_rank_characteristic)

        sample_count = 0
        qc_param_set = set()

        sample_qc_plan = self.sample_assay_plan
        prebatch = sample_qc_plan.pre_run_batch
        factors = set()
        if isinstance(prebatch, SampleQCBatch):
            if prebatch.characteristic_values is None:
                qcsource = Source(name='qc_prebatch_in', characteristics=[
                    Characteristic(
                        category=OntologyAnnotation(term='Material Type'),
                        value=OntologyAnnotation(term=prebatch.material))])
                sources.append(qcsource)
            else:
                for i, (c, v) in enumerate(prebatch.characteristic_values):
                    var_characteristic = OntologyAnnotation(term=c)
                    qcsource = Source(
                        name='qc_prebatch_in-{}'.format(i), characteristics=[
                        Characteristic(
                            category=OntologyAnnotation(term='Material Type'),
                            value=OntologyAnnotation(term=prebatch.material)),
                            Characteristic(category=var_characteristic,
                                           value=v)])
                    if var_characteristic not in study.characteristic_categories:
                        study.characteristic_categories.append(var_characteristic)
                    sources.append(qcsource)
                    if prebatch.parameter_values is None:
                        sample = Sample(name='qc_prebatch_out-{}'.format(i))
                        process = Process(executes_protocol=study.get_prot(
                            'sample collection'), inputs=[qcsource],
                            outputs=[sample], performer=self.ops[0], date_=
                            datetime.datetime.isoformat(
                                datetime.datetime.now()))
                        process.parameter_values = [
                            ParameterValue(
                                category=sample_collection.get_param(
                                    'Run Order'),
                                value=-1)
                        ]
                        samples.append(sample)
                        process_sequence.append(process)
                    else:
                        for j, (p, v) in enumerate(prebatch.parameter_values):
                            qc_param_set.add(p)
                            sample = Sample(name='qc_prebatch_out-{}'.format(j))
                            qc_param = sample_collection.get_param(p)
                            if qc_param is None:
                                sample_collection.add_param(p)
                            process = Process(executes_protocol=study.get_prot(
                                'sample collection'), inputs=[qcsource],
                                outputs=[sample], performer=self.ops[0], date_=
                                datetime.datetime.isoformat(
                                    datetime.datetime.now()))
                            process.parameter_values = [
                                ParameterValue(
                                    category=sample_collection.get_param(
                                        'Run Order'),
                                    value=-1),
                                ParameterValue(
                                    category=sample_collection.get_param(p),
                                    value=v),
                            ]
                            samples.append(sample)
                            process_sequence.append(process)
            if prebatch.parameter_values is not None:
                qcsource = Source(name='qc_prebatch_in', characteristics=[
                    Characteristic(
                        category=OntologyAnnotation(term='Material Type'),
                        value=OntologyAnnotation(term=prebatch.material))])
                sources.append(qcsource)
                for i, (p, v) in enumerate(prebatch.parameter_values):
                    qc_param_set.add(p)
                    sample = Sample(name='qc_prebatch_out-{}'.format(i))
                    qc_param = sample_collection.get_param(p)
                    if qc_param is None:
                        sample_collection.add_param(p)
                    process = Process(executes_protocol=study.get_prot(
                        'sample collection'), inputs=[qcsource],
                        outputs=[sample], performer=self.ops[0], date_=
                        datetime.datetime.isoformat(
                            datetime.datetime.now()))
                    process.parameter_values=[
                        ParameterValue(
                            category=sample_collection.get_param('Run Order'),
                            value=-1),
                        ParameterValue(category=sample_collection.get_param(p),
                                       value=v),
                    ]
                    samples.append(sample)
                    process_sequence.append(process)
        # Main batch
        for (group_id, treatment), ranks in group_rank_map.items():
            fvs = treatment.factor_values
            for factor in [x.factor_name for x in fvs]:
                factors.add(factor)
            for subjn in (str(x) for x in range(group_size)):
                material_type = Characteristic(
                    category=OntologyAnnotation(
                        term='Material Type'),
                    value=OntologyAnnotation(term='specimen'))
                source = Source(name=self._idgen(group_id, subjn))
                source.characteristics = [material_type]
                if prebatch is not None:
                    if prebatch.characteristic_values is not None:
                        c, v = next(iter(prebatch.characteristic_values))
                        var_characteristic = OntologyAnnotation(term=c)
                        source.characteristics.append(Characteristic(
                            category=var_characteristic))
                if sample_qc_plan.post_run_batch is not None:
                    if sample_qc_plan.post_run_batch.characteristic_values is not None:
                        c, v = next(iter(sample_qc_plan.post_run_batch.characteristic_values))
                        var_characteristic = OntologyAnnotation(term=c)
                        source.characteristics.append(Characteristic(
                            category=var_characteristic))
                sources.append(source)
                for rank in ranks:
                    for sample_type, sampling_size in sample_plan.items():
                        for sampn in (str(x) for x in range(0, sampling_size)):
                            for qc_material_type in self.sample_assay_plan \
                                    .sample_qc_plan.keys():
                                if sample_count % self.sample_assay_plan \
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
                                    process = Process(
                                        executes_protocol=sample_collection,
                                        inputs=[qcsource],
                                        outputs=[sample], performer=self.ops[0],
                                        date_=datetime.datetime.isoformat(
                                            datetime.datetime.now()),
                                        parameter_values=[ParameterValue(
                                            category=sample_collection.get_param(
                                                'Run Order'), value=str(
                                                sample_count))])
                                    process_sequence.append(process)
                            # normal sample collection
                            sample = Sample(name=self._idgen(
                                group_id, subjn, sampn, sample_type.value.term),
                                factor_values=fvs)
                            collection_event_rank = Characteristic(
                                category=collection_event_rank_characteristic,
                                value=rank)
                            sample.characteristics = [sample_type,
                                                      collection_event_rank]
                            sample.derives_from = [source]
                            samples.append(sample)
                            sample_count += 1
                            process = Process(executes_protocol=sample_collection,
                                              inputs=[source], outputs=[sample],
                                              performer=self.ops[0], date_=
                                datetime.date.isoformat(datetime.date.today()),
                            parameter_values=[ParameterValue(
                                category=sample_collection.get_param('Run Order'),
                                value=str(sample_count))])
                            process_sequence.append(process)
        postbatch = sample_qc_plan.post_run_batch
        if isinstance(postbatch, SampleQCBatch):
            if postbatch.characteristic_values is None:
                qcsource = Source(name='qc_postbatch_in', characteristics=[
                    Characteristic(
                        category=OntologyAnnotation(term='Material Type'),
                        value=OntologyAnnotation(term=postbatch.material))])
                sources.append(qcsource)
            else:
                for i, (c, v) in enumerate(postbatch.characteristic_values):
                    qcsource = Source(
                        name='qc_postbatch_in-{}'.format(i), characteristics=[
                        Characteristic(
                            category=OntologyAnnotation(term='Material Type'),
                            value=OntologyAnnotation(term=postbatch.material)),
                            Characteristic(category=OntologyAnnotation(term=c),
                                           value=v)])
                    sources.append(qcsource)
                    if postbatch.parameter_values is None:
                        sample = Sample(name='qc_postbatch_out-{}'.format(i))
                        process = Process(executes_protocol=study.get_prot(
                            'sample collection'), inputs=[qcsource],
                            outputs=[sample], performer=self.ops[0], date_=
                            datetime.datetime.isoformat(
                                datetime.datetime.now()))
                        process.parameter_values = [
                            ParameterValue(
                                category=sample_collection.get_param(
                                    'Run Order'),
                                value=-1)
                        ]
                        samples.append(sample)
                        process_sequence.append(process)
                    else:
                        for j, (p, v) in enumerate(postbatch.parameter_values):
                            qc_param_set.add(p)
                            sample = Sample(name='qc_postbatch_out-{}'.format(j))
                            qc_param = sample_collection.get_param(p)
                            if qc_param is None:
                                sample_collection.add_param(p)
                            process = Process(executes_protocol=study.get_prot(
                                'sample collection'), inputs=[qcsource],
                                outputs=[sample], performer=self.ops[0], date_=
                                datetime.datetime.isoformat(
                                    datetime.datetime.now()))
                            process.parameter_values = [
                                ParameterValue(
                                    category=sample_collection.get_param(
                                        'Run Order'),
                                    value=-1),
                                ParameterValue(
                                    category=sample_collection.get_param(p),
                                    value=v),
                            ]
                            samples.append(sample)
                            process_sequence.append(process)
            if postbatch.parameter_values is not None:
                qcsource = Source(name='qc_prebatch_in', characteristics=[
                    Characteristic(
                        category=OntologyAnnotation(term='Material Type'),
                        value=OntologyAnnotation(term=prebatch.material))])
                sources.append(qcsource)
                for i, (p, v) in enumerate(postbatch.parameter_values):
                    qc_param_set.add(p)
                    sample = Sample(name='qc_postbatch_out-{}'.format(i))
                    qc_param = sample_collection.get_param(p)
                    if qc_param is None:
                        sample_collection.add_param(p)
                    process = Process(executes_protocol=study.get_prot(
                        'sample collection'), inputs=[qcsource],
                        outputs=[sample], performer=self.ops[0], date_=
                        datetime.datetime.isoformat(
                            datetime.datetime.now()))
                    process.parameter_values=[
                        ParameterValue(
                            category=sample_collection.get_param('Run Order'),
                            value=-1),
                        ParameterValue(category=sample_collection.get_param(p),
                                       value=v),
                    ]
                    samples.append(sample)
                    process_sequence.append(process)
        # normalize size of params across all processes
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
                              filename='a_{0}_mp_{1}_{2}_assay.txt'.format(
                                  stype.value.term, inj_mode, acq_mode))
                mp_protocol_name = None
                lowered_tt = atype.technology_type.term.lower()
                if lowered_tt == 'mass spectrometry':
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

            lowered_tt = atype.technology_type.term.lower()
            if lowered_tt == 'nmr spectroscopy':
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
                                  filename='a_{0}_nmr_{1}_{2}_assay.txt'.format(
                                      stype.value.term, acq_mode, pulse_seq))

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
        if self.sample_assay_plan.assay_plan == {}:
            raise ISAModelAttributeError('assay_plan is not defined')

        for stype, atype in self.sample_assay_plan.assay_plan:
            # first get all samples of stype
            samples_stype = [x for x in study.samples if
                             stype in x.characteristics]
            lowered_mt = atype.measurement_type.term.lower()
            lowered_tt = atype.technology_type.term.lower()
            if lowered_mt == 'metabolite profiling' \
                    and lowered_tt == 'mass spectrometry':
                for inj_mode, acq_mode in itertools.product(
                        atype.topology_modifiers.injection_modes,
                        atype.topology_modifiers.acquisition_modes):
                    random.shuffle(self.__ops)

                    assay = Assay(measurement_type=atype.measurement_type,
                                  technology_type=atype.technology_type,
                                  filename='a_{0}_ms_{1}_{2}_assay.txt'.format(
                                      stype.value.term, inj_mode, acq_mode))
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
                                             .chromatography_instruments), '')
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
                                             .instruments), '')
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

            elif lowered_mt == 'metabolite profiling' \
                    and lowered_tt == 'nmr spectroscopy':
                for pulse_seq, acq_mode in itertools.product(
                        atype.topology_modifiers.pulse_sequences,
                        atype.topology_modifiers.acquisition_modes):
                    random.shuffle(self.__ops)

                    assay = Assay(measurement_type=atype.measurement_type,
                                  technology_type=atype.technology_type,
                                  filename='a_{0}_nmr_{1}_{2}_assay.txt'.format(
                                      stype.value.term, acq_mode, pulse_seq))

                    if lowered_tt == 'nmr spectroscopy':
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


class SampleAssayPlanEncoder(json.JSONEncoder):

    @staticmethod
    def get_top_mods(o):
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
        if isinstance(o, MSAssayTopologyModifiers):
            return {
                'injection_modes': sorted(o.injection_modes),
                'acquisition_modes': sorted(o.acquisition_modes),
                'technical_replicates': o.technical_replicates,
                'instruments': sorted(o.instruments),
                'chromatography_instruments': sorted(
                    o.chromatography_instruments)
            }
        if isinstance(o, NMRAssayTopologyModifiers):
            return {
                'injection_modes': sorted(o.injection_modes),
                'acquisition_modes': sorted(o.acquisition_modes),
                'pulse_sequences': sorted(o.pulse_sequences),
                'technical_replicates': o.technical_replicates,
                'instruments': sorted(o.instruments)
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
                'assay_types': [self.get_assay_type(x) for x in o.assay_types],
                'sample_plan': self.get_sample_plan(o.sample_plan),
                'sample_qc_plan': self.get_sample_qc_plan(o.sample_qc_plan),
                'assay_plan': self.get_assay_plan(o.assay_plan)
            }


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
            top_mods = MSAssayTopologyModifiers()
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
            top_mods = NMRAssayTopologyModifiers()
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

        return sample_assay_plan


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
