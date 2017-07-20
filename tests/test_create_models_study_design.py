import unittest
from collections import OrderedDict
from isatools.model.v1 import StudyFactor, FactorValue
from isatools.create.models import InterventionStudyDesign, Treatment, SamplePlan, Characteristic, TreatmentFactory, \
    TreatmentSequence, OntologyAnnotation, INTERVENTIONS, BASE_FACTORS

NAME = 'name'
FACTORS_0_VALUE = 'nitoglycerin'
FACTORS_1_VALUE = 5
FACTORS_1_UNIT = 'kg/m^3'
FACTORS_2_VALUE = 100.0
FACTORS_2_VALUE_ALT = 50.0
FACTORS_2_UNIT = 's'


class TreatmentTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0][NAME], value=FACTORS_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS[1][NAME], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2][NAME], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))

    def test_repr(self):
        self.assertEqual(repr(self.treatment),
                         'Treatment(factor_type=chemical intervention, factor_values=('
                         'FactorValue(factor_name={0}, value={1}, unit=None), '
                         'FactorValue(factor_name={2}, value={3}, unit={4}), '
                         'FactorValue(factor_name={5}, value={6}, unit={7})'
                         '))'.format(BASE_FACTORS[0][NAME], FACTORS_0_VALUE,
                                     BASE_FACTORS[1][NAME], FACTORS_1_VALUE, FACTORS_1_UNIT,
                                     BASE_FACTORS[2][NAME], FACTORS_2_VALUE, FACTORS_2_UNIT))

    def test_hash(self):
        self.assertEqual(hash(self.treatment), hash(repr(self.treatment)))

    def test_eq(self):
        same_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0][NAME], value=FACTORS_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS[1][NAME], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2][NAME], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))
        self.assertEqual(self.treatment, same_treatment)
        self.assertEqual(hash(self.treatment), hash(same_treatment))

    def test_ne(self):
        other_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0][NAME], value=FACTORS_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS[1][NAME], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2][NAME], value=FACTORS_2_VALUE_ALT, unit=FACTORS_2_UNIT)
        ))
        self.assertNotEqual(self.treatment, other_treatment)
        self.assertNotEqual(hash(self.treatment), hash(other_treatment))


class SamplePlanTest(unittest.TestCase):

    def setUp(self):
        self.sample_plan = SamplePlan()

    def test_init_default(self):
        sample_plan = self.sample_plan
        self.assertEqual(sample_plan.group_size, 0)
        self.assertEqual(sample_plan.sample_types_map, {})

    def test_init_group_size(self):
        group_size = 100
        sample_plan = SamplePlan(group_size=group_size)
        self.assertEqual(sample_plan.group_size, group_size)

    def test_add_sample_type_sampling_plan_single_value(self):
        sampling_size = 12
        sample_type = Characteristic(category=OntologyAnnotation(term='organism part'), value='blood')
        self.sample_plan.add_sample_type_sampling_plan(sample_type, sampling_size=sampling_size)
        self.assertEqual(self.sample_plan.sample_types_map, {
           sample_type: sampling_size
        })

    def test_add_sample_type_sampling_plan_multiple_value(self):
        sampling_size = (10, 0, 8, 5)
        sample_type = Characteristic(category=OntologyAnnotation(term='organism part'), value='liver')
        self.sample_plan.add_sample_type_sampling_plan(sample_type, sampling_size=sampling_size)
        self.assertEqual(self.sample_plan.sample_types_map, {
            sample_type: sampling_size
        })


class TreatmentFactoryTest(unittest.TestCase):

    def setUp(self):
        self.factory = TreatmentFactory()

    def test_init(self):
        self.assertEqual(self.factory.intervention_type, INTERVENTIONS['CHEMICAL'])
        self.assertTrue(isinstance(self.factory.factors, OrderedDict))

    def test_add_factor_value_str(self):
        factor = StudyFactor(name=BASE_FACTORS[0]['name'], factor_type=BASE_FACTORS[0]['type'])
        self.factory.add_factor_value(factor, 'agent_orange')
        self.assertEqual(self.factory.factors.get(factor), {'agent_orange'})

    def test_add_factor_value_number(self):
        factor = StudyFactor(name=BASE_FACTORS[1]['name'], factor_type=BASE_FACTORS[1]['type'])
        self.factory.add_factor_value(factor, 1.05)
        self.assertEqual(self.factory.factors.get(factor), {1.05})

    def test_add_factor_value_list(self):
        values_to_add = ['agent_orange', 'crack, cocaine']
        factor = StudyFactor(name=BASE_FACTORS[0]['name'], factor_type=BASE_FACTORS[0]['type'])
        self.factory.add_factor_value(factor, values_to_add)
        self.assertEqual(self.factory.factors.get(factor), set(values_to_add))

    def test_compute_full_factorial_design(self):

        agent = StudyFactor(name=BASE_FACTORS[0]['name'], factor_type=BASE_FACTORS[0]['type'])
        intensity = StudyFactor(name=BASE_FACTORS[1]['name'], factor_type=BASE_FACTORS[1]['type'])
        duration = StudyFactor(name=BASE_FACTORS[2]['name'], factor_type=BASE_FACTORS[2]['type'])

        self.factory.add_factor_value(agent, {'cocaine', 'crack', 'aether'})
        self.factory.add_factor_value(intensity, {'low', 'medium', 'high'})
        self.factory.add_factor_value(duration, {'short', 'long'})

        full_factorial = self.factory.compute_full_factorial_design()
        self.assertEqual(full_factorial, {
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='cocaine'),
                FactorValue(factor_name=intensity, value='high'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='cocaine'),
                FactorValue(factor_name=intensity, value='high'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='cocaine'),
                FactorValue(factor_name=intensity, value='low'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='cocaine'),
                FactorValue(factor_name=intensity, value='low'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='cocaine'),
                FactorValue(factor_name=intensity, value='medium'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='cocaine'),
                FactorValue(factor_name=intensity, value='medium'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='crack'),
                FactorValue(factor_name=intensity, value='high'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='crack'),
                FactorValue(factor_name=intensity, value='high'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='crack'),
                FactorValue(factor_name=intensity, value='low'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='crack'),
                FactorValue(factor_name=intensity, value='low'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='crack'),
                FactorValue(factor_name=intensity, value='medium'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='crack'),
                FactorValue(factor_name=intensity, value='medium'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='aether'),
                FactorValue(factor_name=intensity, value='high'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='aether'),
                FactorValue(factor_name=intensity, value='high'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='aether'),
                FactorValue(factor_name=intensity, value='low'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='aether'),
                FactorValue(factor_name=intensity, value='low'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='aether'),
                FactorValue(factor_name=intensity, value='medium'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='aether'),
                FactorValue(factor_name=intensity, value='medium'),
                FactorValue(factor_name=duration, value='short')
            ))
        })

    def test_compute_full_factorial_design_empty_agents(self):

        agent = StudyFactor(name=BASE_FACTORS[0]['name'], factor_type=BASE_FACTORS[0]['type'])
        intensity = StudyFactor(name=BASE_FACTORS[1]['name'], factor_type=BASE_FACTORS[1]['type'])
        duration = StudyFactor(name=BASE_FACTORS[2]['name'], factor_type=BASE_FACTORS[2]['type'])

        self.factory.add_factor_value(agent, set())
        self.factory.add_factor_value(intensity, {'low', 'medium', 'high'})
        self.factory.add_factor_value(duration, {'short', 'long'})

        full_factorial = self.factory.compute_full_factorial_design()
        self.assertEqual(full_factorial, set())

    def test_compute_full_factorial_design_empty_intensities(self):
        agent = StudyFactor(name=BASE_FACTORS[0]['name'], factor_type=BASE_FACTORS[0]['type'])
        intensity = StudyFactor(name=BASE_FACTORS[1]['name'], factor_type=BASE_FACTORS[1]['type'])
        duration = StudyFactor(name=BASE_FACTORS[2]['name'], factor_type=BASE_FACTORS[2]['type'])
        self.factory.add_factor_value(agent, {'cocaine', 'crack', 'aether'})
        self.factory.add_factor_value(intensity, set())
        self.factory.add_factor_value(duration, {'short', 'long'})

        full_factorial = self.factory.compute_full_factorial_design()
        self.assertEqual(full_factorial, set())


class TreatmentSequenceTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.sequence = TreatmentSequence()
        self.agent = StudyFactor(name=BASE_FACTORS[0]['name'], factor_type=BASE_FACTORS[0]['type'])
        self.intensity = StudyFactor(name=BASE_FACTORS[1]['name'], factor_type=BASE_FACTORS[1]['type'])
        self.duration = StudyFactor(name=BASE_FACTORS[2]['name'], factor_type=BASE_FACTORS[2]['type'])
        self.test_treatment = Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
            FactorValue(factor_name=self.agent, value='crack'),
            FactorValue(factor_name=self.intensity, value='low'),
            FactorValue(factor_name=self.duration, value='short')
        ))

    def test_init_with_single_treatment(self):
        treatment = Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
            FactorValue(factor_name=self.agent, value='crack'),
            FactorValue(factor_name=self.intensity, value='low'),
            FactorValue(factor_name=self.duration, value='short')
        ))
        new_sequence = TreatmentSequence(ranked_treatments=treatment)
        self.assertTrue((treatment, 1) in new_sequence.ranked_treatments)

    def test_init_with_treatments_list_no_rank(self):
        treatments = [
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=self.agent, value='crack'),
                FactorValue(factor_name=self.intensity, value='low'),
                FactorValue(factor_name=self.duration, value='short')
            )),
            Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=self.agent, value='crack'),
                FactorValue(factor_name=self.intensity, value='low'),
                FactorValue(factor_name=self.duration, value='long')
            ))
        ]
        new_sequence = TreatmentSequence(ranked_treatments=treatments)
        self.assertTrue((treatments[0], 1) in new_sequence.ranked_treatments)
        self.assertTrue((treatments[1], 1) in new_sequence.ranked_treatments)

    def test_init_with_treatments_list_with_rank(self):
        treatments = [
            (Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=self.agent, value='crack'),
                FactorValue(factor_name=self.intensity, value='low'),
                FactorValue(factor_name=self.duration, value='short')
            )), 1),
            (Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=self.agent, value='crack'),
                FactorValue(factor_name=self.intensity, value='low'),
                FactorValue(factor_name=self.duration, value='long')
            )), 2)
        ]
        new_sequence = TreatmentSequence(ranked_treatments=treatments)
        self.assertTrue(isinstance(new_sequence.ranked_treatments, set))
        self.assertTrue(treatments[0] in new_sequence.ranked_treatments)
        self.assertTrue(treatments[1] in new_sequence.ranked_treatments)

    def test_add_treatment_single(self):
        self.sequence.add_treatment(self.test_treatment)
        self.assertEqual(self.sequence.ranked_treatments, {
            (self.test_treatment, 1)
        })

    def test_repr(self):
        treatments = [
            (Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=self.agent, value='crack'),
                FactorValue(factor_name=self.intensity, value='low'),
                FactorValue(factor_name=self.duration, value='short')
            )), 1),
            (Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=self.agent, value='crack'),
                FactorValue(factor_name=self.intensity, value='low'),
                FactorValue(factor_name=self.duration, value='long')
            )), 2)
        ]
        new_sequence = TreatmentSequence(ranked_treatments=treatments)
        self.assertEqual(repr(new_sequence), 'TreatmentSequence([(Treatment(factor_type=chemical intervention, '
                                             'factor_values=(FactorValue(factor_name=StudyFactor(name=AGENT), '
                                             'value=crack, unit=None), FactorValue(factor_name=StudyFactor(name=INTENSITY), '
                                             'value=low, unit=None), FactorValue(factor_name=StudyFactor(name=DURATION), '
                                             'value=short, unit=None))), 1), (Treatment(factor_type=chemical intervention, '
                                             'factor_values=(FactorValue(factor_name=StudyFactor(name=AGENT), value=crack, '
                                             'unit=None), FactorValue(factor_name=StudyFactor(name=INTENSITY), value=low, '
                                             'unit=None), FactorValue(factor_name=StudyFactor(name=DURATION), value=long, '
                                             'unit=None))), 2)])')

    def test_eq(self):
        treatments = [
            (Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=self.agent, value='crack'),
                FactorValue(factor_name=self.intensity, value='low'),
                FactorValue(factor_name=self.duration, value='short')
            )), 1),
            (Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=self.agent, value='crack'),
                FactorValue(factor_name=self.intensity, value='low'),
                FactorValue(factor_name=self.duration, value='long')
            )), 2)
        ]
        first_sequence = TreatmentSequence(treatments)
        second_sequence = TreatmentSequence(reversed(treatments))
        self.assertEqual(first_sequence, second_sequence)
        self.assertEqual(hash(first_sequence), hash(second_sequence))

    def test_neq(self):
        treatments = [
            (Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=self.agent, value='crack'),
                FactorValue(factor_name=self.intensity, value='low'),
                FactorValue(factor_name=self.duration, value='short')
            )), 1),
            (Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=self.agent, value='crack'),
                FactorValue(factor_name=self.intensity, value='low'),
                FactorValue(factor_name=self.duration, value='long')
            )), 2)
        ]
        other_treatments = [
            (Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=self.agent, value='spirit'),
                FactorValue(factor_name=self.intensity, value='low'),
                FactorValue(factor_name=self.duration, value='short')
            )), 1),
            (Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=self.agent, value='spirit'),
                FactorValue(factor_name=self.intensity, value='low'),
                FactorValue(factor_name=self.duration, value='long')
            )), 2)
        ]
        first_sequence = TreatmentSequence(treatments)
        second_sequence = TreatmentSequence(other_treatments)
        self.assertNotEqual(first_sequence, second_sequence)
        self.assertNotEqual(hash(first_sequence), hash(second_sequence))

    def test_ranked_treatments_setter(self):
        treatments = [
            (Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=self.agent, value='crack'),
                FactorValue(factor_name=self.intensity, value='low'),
                FactorValue(factor_name=self.duration, value='short')
            )), 2),
            (Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=self.agent, value='crack'),
                FactorValue(factor_name=self.intensity, value='low'),
                FactorValue(factor_name=self.duration, value='long')
            )), 1)
        ]
        self.sequence.ranked_treatments = treatments
        self.assertTrue(isinstance(self.sequence.ranked_treatments, set))
        self.assertTrue(treatments[0] in self.sequence.ranked_treatments)
        self.assertTrue(treatments[1] in self.sequence.ranked_treatments)

    def test_subject_count_setter(self):
        subject_count = 20
        self.sequence.subject_count = subject_count
        self.assertTrue(self.sequence.subject_count, subject_count)


class InterventionStudyDesignTest(unittest.TestCase):

    def setUp(self):
        self.design = InterventionStudyDesign()
        self.agent = StudyFactor(name=BASE_FACTORS[0]['name'], factor_type=BASE_FACTORS[0]['type'])
        self.intensity = StudyFactor(name=BASE_FACTORS[1]['name'], factor_type=BASE_FACTORS[1]['type'])
        self.duration = StudyFactor(name=BASE_FACTORS[2]['name'], factor_type=BASE_FACTORS[2]['type'])
        self.first_treatment = Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
            FactorValue(factor_name=self.agent, value='crack'),
            FactorValue(factor_name=self.intensity, value='low'),
            FactorValue(factor_name=self.duration, value='medium')
        ))
        self.second_treatment = Treatment(treatment_type=INTERVENTIONS['CHEMICAL'], factor_values=(
            FactorValue(factor_name=self.agent, value='crack'),
            FactorValue(factor_name=self.intensity, value='high'),
            FactorValue(factor_name=self.duration, value='medium')
        ))
        self.test_sequence = TreatmentSequence(ranked_treatments=[(self.first_treatment, 1), (self.second_treatment, 2)])
        self.sample_plan = SamplePlan(group_size=10, sample_type_map={})

    def test_add_single_sequence_plan(self):
        self.design.add_single_sequence_plan(treatment_sequence=self.test_sequence, sample_plan=self.sample_plan)
        self.assertEqual(self.design.sequences_plan.get(self.test_sequence, None), self.sample_plan)

    def test_add_single_sequence_error_sequence(self):
        wrong_sequence = 'This is not a sequence'
        self.assertRaises(TypeError, self.design.add_single_sequence_plan, treatment_sequence=wrong_sequence,
                          sample_plan=self.sample_plan)

    def test_add_single_sequence_error_sample_plan(self):
        wrong_sample_plan = 'This is not a sample plan'
        self.assertRaises(TypeError, self.design.add_single_sequence_plan, treatment_sequence=self.test_sequence,
                          sample_plan=wrong_sample_plan)

    def test_sequences_plan_property(self):
        other_test_sequence = TreatmentSequence(ranked_treatments=[(self.first_treatment, 2), (self.second_treatment, 1)])
        other_sample_plan = SamplePlan(group_size=12, sample_type_map={})
        sequences_plan = {
            self.test_sequence: self.sample_plan,
            other_test_sequence: other_sample_plan
        }
        self.design.sequences_plan = sequences_plan
        self.assertEqual(self.design.sequences_plan, sequences_plan)

    def test_sequences_plan_properties(self):
        not_a_sequences_plan_object = [self.test_sequence, self.sample_plan]
        self.assertRaises(TypeError, self.design.sequences_plan, not_a_sequences_plan_object)

    def test_sample_types_property(self):
        pass