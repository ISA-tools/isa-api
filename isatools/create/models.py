import itertools
from numbers import Number
from collections import OrderedDict, Iterable
from isatools.model.v1 import StudyFactor, FactorValue, OntologyAnnotation

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


class DesignedStudy(object):
    pass


class InterventionDesignedStudy(DesignedStudy):

    def __init__(self, sequences = []):
        super().__init__()
        self.__sequences = set()


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
        return not self.factor_values == other.factor_values

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
    A treatment sequence is an ordered (graph-like) combination of treatments
    """

    def __init__(self, ranked_treatments=[]):
        """
        :param ranked_treatments: Treatment or list of Treatments of list of tuples (Treatment, int) where the second term represents the 
            epoch
        """
        self.__ranked_treatments = set()

        self.add_multiple_treatments(ranked_treatments)

    @property
    def ranked_treatments(self):
        return self.__ranked_treatments

    @ranked_treatments.setter
    def ranked_treatments(self, ranked_treatments):
        self.add_multiple_treatments(ranked_treatments)

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


