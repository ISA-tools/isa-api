import unittest
from isatools.create.models import Treatment


class TreatmentTest(unittest.TestCase):

    def setUp(self):
        self.treatment = Treatment()

    def test_setter_agent_values_list(self):
        test_values = ['agent_orange', 'agent_007', 'agent_mercury']
        self.treatment.agent_values = test_values
        self.assertEqual(self.treatment.agent_values, test_values, 'correctly sets multiple agent values')

    def test_setter_agent_values_single(self):
        test_value = 'agent_orange'
        self.treatment.agent_values = test_value
        self.assertEqual(self.treatment.agent_values, ['agent_orange'], 'correctly sets single agent value')
