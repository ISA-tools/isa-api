import unittest
from collections import OrderedDict
from isatools.model.v1 import StudyFactor
from isatools.create.models import Treatment, TreatmentFactory, INTERVENTIONS, BASE_FACTORS


class TreatmentTest(unittest.TestCase):

    def setUp(self):
        self.treatment = Treatment()

    """
    def test_setter_agent_values_multiple(self):
        test_values = ['agent_orange', 'agent_007', 'agent_mercury']
        self.treatment.agent_values = test_values
        self.assertEqual(self.treatment.agent_values, set(test_values), 'correctly sets multiple agent values')

    def test_setter_agent_values_single(self):
        test_value = 'agent_orange'
        self.treatment.agent_values = test_value
        self.assertEqual(self.treatment.agent_values, {test_value}, 'correctly sets single agent value')

    def test_setter_intensity_values_multiple(self):
        test_values = ['low', 'medium', 'high']
        self.treatment.intensity_values = test_values
        self.assertEqual(self.treatment.intensity_values, set(test_values),
                         'correctly sets multiple intensity values')

    def test_setter_intensity_values_single(self):
        test_value = 'single_intensity'
        self.treatment.intensity_values = test_value
        self.assertEqual(self.treatment.intensity_values, {test_value}, 'correctly sets single intensity value')

    def test_setter_duration_values_multiple(self):
        test_values = ['short', 'medium', 'long']
        self.treatment.duration_values = test_values
        self.assertEqual(self.treatment.duration_values, set(test_values), 'correctly sets multiple duration values')

    def test_setter_duration_values_single(self):
        test_value = 'single_duration'
        self.treatment.duration_values = test_value
        self.assertEqual(self.treatment.duration_values, {test_value}, 'correctly sets single duration value')


    def test_compute_full_factorial_design(self):
        test_agents = {'cocaine', 'crack', 'ether'}
        test_intensities = {'low', 'medium', 'high'}
        test_durations = {'short', 'long'}
        self.treatment.agent_values = test_agents
        self.treatment.intensity_values = test_intensities
        self.treatment.duration_values = test_durations
        full_factorial = self.treatment.compute_full_factorial_design()
        self.assertEqual(full_factorial, {
            ('cocaine', 'high', 'long'),
            ('cocaine', 'high', 'short'),
            ('cocaine', 'low', 'long'),
            ('cocaine', 'low', 'short'),
            ('cocaine', 'medium', 'long'),
            ('cocaine', 'medium', 'short'),
            ('crack', 'high', 'long'),
            ('crack', 'high', 'short'),
            ('crack', 'low', 'long'),
            ('crack', 'low', 'short'),
            ('crack', 'medium', 'long'),
            ('crack', 'medium', 'short'),
            ('ether', 'high', 'long'),
            ('ether', 'high', 'short'),
            ('ether', 'low', 'long'),
            ('ether', 'low', 'short'),
            ('ether', 'medium', 'long'),
            ('ether', 'medium', 'short')
        })

    def test_compute_full_factorial_design_empty_agents(self):
        test_agents = set()
        test_intensities = {'low', 'medium', 'high'}
        test_durations = {'short', 'long'}
        self.treatment.agent_values = test_agents
        self.treatment.intensity_values = test_intensities
        self.treatment.duration_values = test_durations
        full_factorial = self.treatment.compute_full_factorial_design()
        self.assertEqual(full_factorial, set())

    def test_compute_full_factorial_design_empty_intensities(self):
        test_agents = {'cocaine', 'crack', 'ether'}
        test_intensities = set()
        test_durations = {'short', 'long'}
        self.treatment.agent_values = test_agents
        self.treatment.intensity_values = test_intensities
        self.treatment.duration_values = test_durations
        full_factorial = self.treatment.compute_full_factorial_design()
        self.assertEqual(full_factorial, set())

    """


class TreatmentFactoryTest(unittest.TestCase):

    def setUp(self):
        self.factory = TreatmentFactory()

    def test_init(self):
        self.assertEqual(self.factory.type, INTERVENTIONS['CHEMICAL'])
        self.assertTrue(isinstance(self.factory.factors, OrderedDict))

    def test_add_factor_value(self):
        factor = StudyFactor(name=BASE_FACTORS[0]['name'], factor_type=BASE_FACTORS[0]['type'])
        self.factory.add_factor_value(factor, 'agent_orange')
        self.assertEqual(self.factory.factors.get(factor), {'agent_orange'})
