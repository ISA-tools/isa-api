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



