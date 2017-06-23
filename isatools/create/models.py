import itertools
from numbers import Number
from collections import OrderedDict, Iterable
from isatools.model.v1 import StudyFactor, FactorValue, OntologyAnnotation

__author__ = 'massi'

INTERVENTIONS = dict(CHEMICAL='chemical intervention', BEHAVIOURAL='behavioural interention',
                     SURGICAL='surgical intervention', BIOLOGICAL='biological intervention',
                     RADIOLOGICAL='radiological intervention')

FACTOR_TYPES = dict(AGENT_VALUES='agent values', INTENSITY_VALUES='intensity_values', DURATION_VALUES='duration values')

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


class StudyDesigner(object):
    pass


class InterventionStudyDesign(StudyDesigner):

    def __init__(self, treatments_count):
        super().__init__()
        self._treatments_count = 0

    @property
    def treatments_count(self):
        return self._treatments_count

    @treatments_count.setter
    def treatments_count(self, treatments_count):
        self._treatments_count = treatments_count


class Treatment(object):
    """
    """
    def __init__(self, factor_values):
        """
        Creates a new Treatment
        :param factor_values: tuple of isatools.model.v1.FactorValue
        """
        self._factor_values = ()

        self.factor_values = factor_values

    def __hash__(self):
        pass

    @property
    def factor_values(self):
        return self._factor_values

    @factor_values.setter
    def factor_values(self, factor_values=()):
        if isinstance(factor_values, tuple) and all([isinstance(factor_value, FactorValue)
                                                     for factor_value in factor_values]):
            self._factor_values = factor_values
        else:
            raise TypeError('Data supplied is not correctly formatted for Treatment')


# FIXME use the factor class??
class TreatmentFactory(object):

    def __init__(self, intervention_type=INTERVENTIONS['CHEMICAL'], factors=BASE_FACTORS):

        if intervention_type not in INTERVENTIONS.values():
            raise ValueError('invalid treatment type provided: ')

        self._type = intervention_type
        """
        self._agent_values = set()
        self._intensity_values = set()
        self._duration_values = set()
        self._factors = [factor.get('name', None) for factor in factors]
        """
        self._factors = OrderedDict([(StudyFactor(name=factor.get('name'), factor_type=factor.get('type')), set())
                                     for factor in factors])

        self._factorial_design = set()

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

    @property
    def type(self):
        return self._type

    @property
    def factors(self):
        return self._factors

    def compute_full_factorial_design(self):
        factor_values = [FactorValue(factor_name=factor_name, value=value, unit=None)
                         for factor_name, values in self.factors.items() for value in values]
        if set() not in self.factors.values():
            return [Treatment(treatment_factors) for treatment_factors in itertools.product(*factor_values)]
        else:
            return []

    """
    @property
    def agent_values(self):
        return self._agent_values



    @property
    def intensity_values(self):
        return self._intensity_values

    @property
    def duration_values(self):
        return self._duration_values

    @type.setter
    def type(self, value):
        if value in INTERVENTIONS.values():
            self._type = value
        else:
            raise ValueError('Invalid value type for treatment type property')

    @agent_values.setter
    def agent_values(self, value):
        if isinstance(value, list):
            self._agent_values = set(value)
        elif isinstance(value, set):
            self._agent_values = value
        else:
            self._agent_values = {value}

    @intensity_values.setter
    def intensity_values(self, value):
        if isinstance(value, list):
            self._intensity_values = set(value)
        elif isinstance(value, set):
            self._intensity_values = value
        else:
            self._intensity_values = {value}

    @duration_values.setter
    def duration_values(self, value):
        if isinstance(value, list):
            self._duration_values = set(value)
        elif isinstance(value, set):
            self._duration_values = value
        else:
            self._duration_values = {value}

    """
    


