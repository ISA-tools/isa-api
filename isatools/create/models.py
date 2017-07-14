import itertools
from operator import itemgetter
from numbers import Number
from collections import OrderedDict, Iterable
from isatools.model.v1 import StudyFactor, FactorValue, OntologyAnnotation, Characteristic

__author__ = 'massi'

INTERVENTIONS = dict(CHEMICAL='chemical intervention', BEHAVIOURAL='behavioural intervention',
                     SURGICAL='surgical intervention', BIOLOGICAL='biological intervention',
                     RADIOLOGICAL='radiological intervention')

FACTOR_TYPES = dict(AGENT_VALUES='agent values', INTENSITY_VALUES='intensity values', DURATION_VALUES='duration values')

BASE_FACTORS = [
    dict(
        name='AGENT', type=OntologyAnnotation(term="perturbation agent"), display_singular='AGENT VALUE',
        display_plural='AGENT VALUES', uri='', values=set()
    ),
    dict(
        name='INTENSITY', type=OntologyAnnotation(term="intensity"), display_singular='INTENSITY VALUE',
        display_plural='INTENSITY VALUES', uri='', values=set()
    ),
    dict(
        name='DURATION', type=OntologyAnnotation(term="time"), display_singular='DURATION VALUE',
        display_plural='DURATION VALUES', uri='', values=set()
    )
]


class BaseStudyDesign(object):
    pass


class InterventionStudyDesign(BaseStudyDesign):

    def __init__(self, sequences=[]):
        super().__init__()
        self.__sequences = OrderedDict()
        # self.sequences = sequences

    @property
    def sequences(self):
        return self.__sequences if self.__sequences else OrderedDict()

    @sequences.setter
    def sequences(self, sequences):
        pass
        """
        if isinstance(sequences, Iterable) and all([isinstance(elem, TreatmentSequence) for elem in sequences]):
            self.__sequences = sequences
        else:
            raise TypeError('The object supplied is not a valid iterable of TreatmentSequence: {0}'.format(sequences))
        """

    def add_sequence(self, sequence, group_size=0, sample_plan_map={}):
        if isinstance(sequence, TreatmentSequence):
            self.sequences[sequence] = {
                'group_size': group_size if isinstance(group_size, int) else 0,
                'sample_plan_map': sample_plan_map if isinstance(sample_plan_map, dict) and {
                    isinstance(key, Characteristic) for key in sample_plan_map} else {}
            }
        else:
            raise TypeError('{0} is not a valid sequence'.format(sequence))

    def add_group_size_to_sequence(self, group_size, sequence=None):
        if sequence is None:
            sequence = self.sequences.keys()[0]


class SamplePlan(object):

    def __init__(self, group_size=0):
        self.__group_size = group_size if isinstance(group_size, int) and group_size > 0 else 0
        self.__sample_types_map = {}

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

    def add_sample_type_sampling_plan(self, sample_type, sampling_size):
        if not isinstance(sampling_size, int):
            raise TypeError('sampling_size must be a natural number')
        if sampling_size < 0:
            raise ValueError('sampling_size must be a natural number')
        if isinstance(sample_type, Characteristic):
            self.__sample_types_map[sample_type] = sampling_size
        elif isinstance(sample_type, str):
            characteristic = Characteristic(category=OntologyAnnotation(term='organism part'),
                                            value=OntologyAnnotation(term=sample_type))
            self.__sample_types_map[characteristic] = sampling_size
        else:
            raise TypeError('wrong sample type {0}'.format(sample_type))


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
        if type in INTERVENTIONS.values():
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
        self.__factors = OrderedDict([(StudyFactor(name=factor.get('name'), factor_type=factor.get('type')), set())
                                      for factor in factors])

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
        :param factor: isatools.model.v1.StudyFactor
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
        :return: set - the ful factorial design as a set of Treatments 
        """
        factor_values = [
            [FactorValue(factor_name=factor_name, value=value, unit=None) for value in values]
            for factor_name, values in self.factors.items()
        ]
        if set() not in self.factors.values():
            return {Treatment(treatment_type=self.intervention_type,  factor_values=treatment_factors)
                    for treatment_factors in itertools.product(*factor_values)}
        else:
            return set()


class TreatmentSequence:
    """
    A treatment sequence is an ordered (graph-like) combination of treatment
    """

    def __init__(self, ranked_treatments=[], subject_count=10):
        """
        :param ranked_treatments: Treatment or list of Treatments of list of tuples (Treatment, int) where the second term represents the 
            epoch
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

    def __init__(self, measurement_type=None, technology_type=None):
        if isinstance(measurement_type, OntologyAnnotation):
            self.__measurement_type = measurement_type
        elif isinstance(measurement_type, str):
            self.__measurement_type = OntologyAnnotation(term=measurement_type)
        elif measurement_type is None:
            self.__measurement_type = None
        else:
            raise TypeError('{0} is not a valid value for technology_type. '
                            'Please provide an OntologyAnnotation or string.')
        if isinstance(technology_type, OntologyAnnotation):
            self.__technology_type = technology_type
        elif isinstance(technology_type, str):
            self.__technology_type = OntologyAnnotation(term=technology_type)
        elif technology_type is None:
            self.__technology_type = None
        else:
            raise TypeError('{0} is not a valid value for technology_type. '
                            'Please provide an OntologyAnnotation or string.')

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
            raise TypeError('{0} is not a valid value for measurement_type. '
                            'Please provide an OntologyAnnotation or string.')

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
            raise TypeError('{0} is not a valid value for technology_type. '
                            'Please provide an OntologyAnnotation or string.')

    def __repr__(self):
        return 'AssayType(mt={0}, tt={1})'.format(self.measurement_type.term, self.technology_type.term)

    def __hash__(self):
        return hash(repr(self))

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return isinstance(other, AssayType) \
               and isinstance(other.measurement_type, OntologyAnnotation) \
               and isinstance(other.technology_type, OntologyAnnotation) \
               and self.measurement_type.term == other.measurement_type.term \
               and self.technology_type.term == other.technology_type.term


class AssayTopologyModifiers(object):

    def __init__(self, distinct_libraries=0, distinct_array_designs=0, injection_modes=0, acquisition_modes=0,
                 pulse_sequences=0, technical_replicates=0):
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
            raise TypeError('{0} is not a valid value for distinct_libraries. Please provide an integer.')
        if distinct_libraries < 0:
            raise ValueError('distinct_libraries must be greater than 0.')
        self.__distinct_libraries = distinct_libraries

    @property
    def distinct_array_designs(self):
        return self.__distinct_array_designs

    @distinct_array_designs.setter
    def distinct_array_designs(self, distinct_array_designs):
        if not isinstance(distinct_array_designs, int):
            raise TypeError('{0} is not a valid value for distinct_array_designs. Please provide an integer.')
        if distinct_array_designs < 0:
            raise ValueError('distinct_array_designs must be greater than 0.')
        self.__distinct_array_designs = distinct_array_designs

    @property
    def injection_modes(self):
        return self.__injection_modes

    @injection_modes.setter
    def injection_modes(self, injection_modes):
        if not isinstance(injection_modes, int):
            raise TypeError('{0} is not a valid value for injection_modes. Please provide an integer.')
        if injection_modes < 0:
            raise ValueError('injection_modes must be greater than 0.')
        self.__injection_modes = injection_modes

    @property
    def acquisition_modes(self):
        return self.__acquisition_modes

    @acquisition_modes.setter
    def acquisition_modes(self, acquisition_modes):
        if not isinstance(acquisition_modes, int):
            raise TypeError('{0} is not a valid value for acquisition_modes. Please provide an integer.')
        if acquisition_modes < 0:
            raise ValueError('injection_modes must be greater than 0.')
        self.__acquisition_modes = acquisition_modes

    @property
    def pulse_sequences(self):
        return self.__pulse_sequences

    @pulse_sequences.setter
    def pulse_sequences(self, pulse_sequences):
        if not isinstance(pulse_sequences, int):
            raise TypeError('{0} is not a valid value for pulse_sequences. Please provide an integer.')
        if pulse_sequences < 0:
            raise ValueError('injection_modes must be greater than 0.')
        self.__pulse_sequences = pulse_sequences

    @property
    def technical_replicates(self):
        return self.__technical_replicates

    @technical_replicates.setter
    def technical_replicates(self, technical_replicates):
        if not isinstance(technical_replicates, int):
            raise TypeError('{0} is not a valid value for technical_replicates. Please provide an integer.')
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


class AssayPlan(object):

    def __init__(self, sample_plan=None):
        self.__sample_plan = sample_plan
        self.__assay_types_map = None
        self.__assay_topologies_map = None

    @property
    def sample_plan(self):
        return self.__sample_plan

    @sample_plan.setter
    def sample_plan(self, sample_plan):
        if not isinstance(sample_plan, (SamplePlan, None)):
            raise TypeError('{0} is not a valid value for sample_plan. Please provide a SamplePlan object.')
        self.__sample_plan = sample_plan

    @property
    def assay_types_map(self):
        return self.__assay_types_map

    @assay_types_map.setter
    def assay_types_map(self, assay_types_map):
        for sample_type, assay_type in assay_types_map.items():
            self.add_sample_type_assay_plan(sample_type, assay_type)

    def add_sample_type_assay_plan(self, sample_type, assay_type):
        if not isinstance(sample_type, Characteristic):
            raise TypeError('wrong sample_type {0}'.format(sample_type))
        elif not isinstance(assay_type, AssayType):
            raise TypeError('wrong assay_type {0}'.format(assay_type))
        elif isinstance(sample_type, str):
            characteristic = Characteristic(category=OntologyAnnotation(term='organism part'),
                                            value=OntologyAnnotation(term=sample_type))
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
            raise TypeError('wrong assay_type type {0}'.format(assay_topology_modifiers))
        if isinstance(assay_topology_modifiers, AssayTopologyModifiers):
            self.__assay_topologies_map[assay_type] = assay_topology_modifiers
        else:
            raise TypeError('wrong assay_topology_modifiers type {0}'.format(assay_topology_modifiers))
