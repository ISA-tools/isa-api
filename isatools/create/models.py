import itertools
from isatools.model.v1 import StudyFactor

__author__ = 'massi'

INTERVENTIONS = dict(CHEMICAL='chemical intervention', BEHAVIOURAL='behavioural interention',
                     SURGICAL='surgical intervention', BIOLOGICAL='biological intervention',
                     RADIOLOGICAL='radiological intervention')

FACTOR_TYPES = dict(AGENT_VALUES='agent values', INTENSITY_VALUES='intensity_values', DURATION_VALUES='duration values')

BASE_FACTORS = [
    dict(
        name='AGENT', display_singular='AGENT VALUE',
        display_plural='AGENT VALUES', uri='', values=set()
    ),
    dict(
        name='INTENSITY', display_singular='INTENSITY VALUE',
        display_plural='INTENSITY VALUES', uri='', values=set()
    ),
    dict(
        name='DURATION', display_singular='DURATION VALUE',
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



    def __init__(self):
        pass

#FIXME use the factor class??
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
        self._factors = factors
        self._factorial_design = set()

    def add_factor_value(self, factor_name, factor_value):
        factor_names = [factor.get('name') for factor in self.factors]
        if factor_name in factor_names:
            self.factors['values'].update(factor_value)
        else:
            raise KeyError('The factor {} is not present in the design'.format(factor_name))

    @property
    def type(self):
        return self._type

    @property
    def factors(self):
        return self._factors

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

    def compute_full_factorial_design(self):
        if self._agent_values and self._intensity_values and self.duration_values:
            return {el for el in itertools.product(self.agent_values, self.intensity_values, self.duration_values)}
        else:
            return set()

    """
    


