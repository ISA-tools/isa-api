import unittest
from collections import OrderedDict

from isatools.model import *
from isatools.create.models import *

NAME = 'name'
FACTORS_0_VALUE = 'nitroglycerin'
FACTORS_1_VALUE = 5
FACTORS_1_UNIT = 'kg/m^3'
FACTORS_2_VALUE = 100.0
FACTORS_2_VALUE_ALT = 50.0
FACTORS_2_UNIT = 's'

TEST_EPOCH_0_NAME = 'test epoch 0'
TEST_EPOCH_1_NAME = 'test epoch 1'
TEST_EPOCH_2_NAME = 'test epoch 2'
TEST_STUDY_ARM_NAME = 'test arm'

TEST_EPOCH_0_RANK = 0


# class SamplePlanTest(unittest.TestCase):
#
#     def setUp(self):
#         self.sample_plan = SampleAssayPlan()
#
#     def test_init_default(self):
#         sample_plan = self.sample_plan
#         self.assertEqual(sample_plan.group_size, 0)
#         self.assertEqual(sample_plan.sample_types_map, {})
#
#     def test_init_group_size(self):
#         group_size = 100
#         sample_plan = SampleAssayPlan(group_size=group_size)
#         self.assertEqual(sample_plan.group_size, group_size)
#
#     def test_add_sample_type_sampling_plan_single_value(self):
#         sampling_size = 12
#         sample_type = Characteristic(category=OntologyAnnotation(term='organism part'), value='liver')
#         self.sample_plan.add_sample_plan_record(sample_type, sampling_size=sampling_size)
#         self.assertEqual(self.sample_plan.sample_types_map, {
#            sample_type: sampling_size
#         })
#
#     def test_add_sample_type_sampling_plan_multiple_value(self):
#         sampling_size = (10, 0, 8, 5)
#         sample_type = Characteristic(category=OntologyAnnotation(term='organism part'), value='liver')
#         self.sample_plan.add_sample_plan_record(sample_type, sampling_size=sampling_size)
#         self.assertEqual(self.sample_plan.sample_types_map, {
#             sample_type: sampling_size
#         })
#
#     def test_sample_types_property(self):
#         liver_sample_type = Characteristic(category=OntologyAnnotation(term='organism part'), value='liver')
#         blood_sample_type = Characteristic(category=OntologyAnnotation(term='organism part'), value='blood')
#         self.sample_plan.sample_types_map = {
#             liver_sample_type: (0, 1, 1),
#             blood_sample_type: (3, 3, 4)
#         }
#         self.assertEqual(self.sample_plan.sample_types, { liver_sample_type, blood_sample_type })
#
#     def test_sample_types_property_empty(self):
#         self.assertEqual(self.sample_plan.sample_types, set())

class NonTreatmentTest(unittest.TestCase):

    DURATION_VALUE = 10.0
    DURATION_UNIT = OntologyAnnotation(term='day')
    OTHER_DURATION_VALUE = 12.0

    def setUp(self):
        self.non_treatment = NonTreatment(duration_value=self.DURATION_VALUE, duration_unit=self.DURATION_UNIT)

    def test_init_and_propeties(self):
        self.assertEqual(self.non_treatment.type, ELEMENT_TYPES['SCREEN'])
        self.assertEqual(self.non_treatment.duration, FactorValue(factor_name=DURATION_FACTOR,
                                                                  value=self.DURATION_VALUE,
                                                                  unit=self.DURATION_UNIT))

    def test_repr(self):
        print(self.non_treatment.duration)
        self.assertEqual(repr(self.non_treatment),
                         "NonTreatment(type='screen', duration=isatools.model.FactorValue("
                         "factor_name=isatools.model.StudyFactor(name='DURATION', "
                         "factor_type=isatools.model.OntologyAnnotation(term='time', term_source=None, "
                         "term_accession='', comments=[]), comments=[]), value=10.0, "
                         "unit=isatools.model.OntologyAnnotation(term='day', term_source=None, term_accession='', "
                         "comments=[])))")

    def test_hash(self):
        self.assertEqual(hash(self.non_treatment), hash(repr(self.non_treatment)))

    def test_eq(self):
        same_non_treatment = NonTreatment(duration_value=self.DURATION_VALUE, duration_unit=self.DURATION_UNIT)
        self.assertEqual(self.non_treatment, same_non_treatment)

    def test_ne(self):
        other_non_treatment = NonTreatment(duration_value=self.OTHER_DURATION_VALUE,
                                           duration_unit=self.DURATION_UNIT)
        self.assertNotEqual(self.non_treatment, other_non_treatment)


class TreatmentTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS_[0][NAME], value=FACTORS_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS_[1][NAME], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS_[2][NAME], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))

    def test_repr(self):
        self.assertEqual(repr(self.treatment),
                         "Treatment(type=chemical intervention, "
                         "factor_values=[isatools.model.FactorValue("
                         "factor_name='AGENT', value='nitroglycerin', "
                         "unit=None), isatools.model.FactorValue("
                         "factor_name='DURATION', value=100.0, unit='s'), "
                         "isatools.model.FactorValue(factor_name='INTENSITY', "
                         "value=5, unit='kg/m^3')], group_size=0)")

    def test_hash(self):
        self.assertEqual(hash(self.treatment), hash(repr(self.treatment)))

    def test_eq(self):
        same_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS_[0][NAME], value=FACTORS_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS_[1][NAME], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS_[2][NAME], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))
        self.assertEqual(self.treatment, same_treatment)
        self.assertEqual(hash(self.treatment), hash(same_treatment))

    def test_ne(self):
        other_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS_[0][NAME], value=FACTORS_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS_[1][NAME], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS_[2][NAME], value=FACTORS_2_VALUE_ALT, unit=FACTORS_2_UNIT)
        ))
        self.assertNotEqual(self.treatment, other_treatment)
        self.assertNotEqual(hash(self.treatment), hash(other_treatment))


class TreatmentFactoryTest(unittest.TestCase):

    def setUp(self):
        self.factory = TreatmentFactory()

    def test_init(self):
        self.assertEqual(self.factory.intervention_type, INTERVENTIONS['CHEMICAL'])
        self.assertTrue(isinstance(self.factory.factors, OrderedDict))

    def test_add_factor_value_str(self):
        factor = StudyFactor(name=BASE_FACTORS_[0]['name'], factor_type=BASE_FACTORS_[0]['type'])
        self.factory.add_factor_value(factor, 'agent_orange')
        self.assertEqual(self.factory.factors.get(factor), {'agent_orange'})

    def test_add_factor_value_number(self):
        factor = StudyFactor(name=BASE_FACTORS_[1]['name'], factor_type=BASE_FACTORS_[1]['type'])
        self.factory.add_factor_value(factor, 1.05)
        self.assertEqual(self.factory.factors.get(factor), {1.05})

    def test_add_factor_value_list(self):
        values_to_add = ['agent_orange', 'crack, cocaine']
        factor = StudyFactor(name=BASE_FACTORS_[0]['name'], factor_type=BASE_FACTORS_[0]['type'])
        self.factory.add_factor_value(factor, values_to_add)
        self.assertEqual(self.factory.factors.get(factor), set(values_to_add))

    def test_add_factor_value_set(self):
        values_to_add = {'agent_orange', 'crack, cocaine'}
        factor = StudyFactor(name=BASE_FACTORS_[0]['name'], factor_type=BASE_FACTORS_[0]['type'])
        self.factory.add_factor_value(factor, values_to_add)
        self.assertEqual(self.factory.factors.get(factor), values_to_add)

    def test_compute_full_factorial_design(self):

        agent = StudyFactor(name=BASE_FACTORS_[0]['name'], factor_type=BASE_FACTORS_[0]['type'])
        intensity = StudyFactor(name=BASE_FACTORS_[1]['name'], factor_type=BASE_FACTORS_[1]['type'])
        duration = StudyFactor(name=BASE_FACTORS_[2]['name'], factor_type=BASE_FACTORS_[2]['type'])

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

        agent = StudyFactor(name=BASE_FACTORS_[0]['name'], factor_type=BASE_FACTORS_[0]['type'])
        intensity = StudyFactor(name=BASE_FACTORS_[1]['name'], factor_type=BASE_FACTORS_[1]['type'])
        duration = StudyFactor(name=BASE_FACTORS_[2]['name'], factor_type=BASE_FACTORS_[2]['type'])

        self.factory.add_factor_value(agent, set())
        self.factory.add_factor_value(intensity, {'low', 'medium', 'high'})
        self.factory.add_factor_value(duration, {'short', 'long'})

        full_factorial = self.factory.compute_full_factorial_design()
        self.assertEqual(full_factorial, set())

    def test_compute_full_factorial_design_empty_intensities(self):
        agent = StudyFactor(name=BASE_FACTORS_[0]['name'], factor_type=BASE_FACTORS_[0]['type'])
        intensity = StudyFactor(name=BASE_FACTORS_[1]['name'], factor_type=BASE_FACTORS_[1]['type'])
        duration = StudyFactor(name=BASE_FACTORS_[2]['name'], factor_type=BASE_FACTORS_[2]['type'])
        self.factory.add_factor_value(agent, {'cocaine', 'crack', 'aether'})
        self.factory.add_factor_value(intensity, set())
        self.factory.add_factor_value(duration, {'short', 'long'})

        full_factorial = self.factory.compute_full_factorial_design()
        self.assertEqual(full_factorial, set())

"""
class TreatmentSequenceTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.sequence = TreatmentSequence()
        self.agent = StudyFactor(name=BASE_FACTORS_[0]['name'], factor_type=BASE_FACTORS_[0]['type'])
        self.intensity = StudyFactor(name=BASE_FACTORS_[1]['name'], factor_type=BASE_FACTORS_[1]['type'])
        self.duration = StudyFactor(name=BASE_FACTORS_[2]['name'], factor_type=BASE_FACTORS_[2]['type'])
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
        self.assertEqual("TreatmentSequence([(Treatment(type=chemical "
                         "intervention, factor_values=[isatools.model."
                         "FactorValue(factor_name=isatools.model.StudyFactor("
                         "name='AGENT', factor_type="
                         "isatools.model.OntologyAnnotation("
                         "term='perturbation agent', term_source=None, "
                         "term_accession='', comments=[]), comments=[]), "
                         "value='crack', unit=None), "
                         "isatools.model.FactorValue("
                         "factor_name=isatools.model.StudyFactor("
                         "name='DURATION', "
                         "factor_type=isatools.model.OntologyAnnotation("
                         "term='time', term_source=None, term_accession='', "
                         "comments=[]), comments=[]), value='long', "
                         "unit=None), isatools.model.FactorValue("
                         "factor_name=isatools.model.StudyFactor("
                         "name='INTENSITY', factor_type="
                         "isatools.model.OntologyAnnotation(term='intensity', "
                         "term_source=None, term_accession='', comments=[]), "
                         "comments=[]), value='low', unit=None)], group_size=0)"
                         ", 2), ("
                         "Treatment(type=chemical intervention, "
                         "factor_values=[isatools.model.FactorValue("
                         "factor_name=isatools.model.StudyFactor(name='AGENT', "
                         "factor_type=isatools.model.OntologyAnnotation("
                         "term='perturbation agent', term_source=None, "
                         "term_accession='', comments=[]), comments=[]), "
                         "value='crack', unit=None), "
                         "isatools.model.FactorValue(factor_name="
                         "isatools.model.StudyFactor(name='DURATION', "
                         "factor_type=isatools.model.OntologyAnnotation("
                         "term='time', term_source=None, term_accession='', "
                         "comments=[]), comments=[]), value='short', "
                         "unit=None), isatools.model.FactorValue("
                         "factor_name=isatools.model.StudyFactor("
                         "name='INTENSITY', factor_type="
                         "isatools.model.OntologyAnnotation(term='intensity', "
                         "term_source=None, term_accession='', comments=[]), "
                         "comments=[]), value='low', unit=None)], group_size=0), 1)])",
                         repr(new_sequence))

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
        second_sequence = TreatmentSequence(list(reversed(treatments)))
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
"""

class SampleAssayPlanTest(unittest.TestCase):

    def setUp(self):
        self.plan = SampleAssayPlan()

    def test_init_default(self):
        sample_plan = self.plan
        self.assertEqual(sample_plan.group_size, 0)
        self.assertEqual(sample_plan.sample_types, set())

    def test_init_group_size(self):
        group_size = 100
        sample_assay_plan = SampleAssayPlan(group_size=group_size)
        self.assertEqual(sample_assay_plan.group_size, group_size)

    def test_add_sample_type(self):
        liver_sample_type = Characteristic(category=OntologyAnnotation(
            term='organism part'), value='liver')
        self.plan.add_sample_type(liver_sample_type)
        self.assertEqual(self.plan.sample_types, { liver_sample_type })

    def test_add_sample_type_str(self):
        liver_sample_type = 'liver'
        self.plan.add_sample_type(liver_sample_type)
        self.assertEqual(self.plan.sample_types, {
            Characteristic(category=OntologyAnnotation(term='organism part'),
                           value=OntologyAnnotation(term=liver_sample_type))
        })

    def test_sample_types_property_from_set(self):
        liver_sample_type = Characteristic(category=OntologyAnnotation(
            term='organism part'), value='liver')
        blood_sample_type = Characteristic(category=OntologyAnnotation(
            term='organism part'), value='blood')
        heart_sample_type = Characteristic(category=OntologyAnnotation(
            term='organism part'), value='heart')
        test_sample_types = {liver_sample_type, blood_sample_type,
                             heart_sample_type}
        self.plan.sample_types = test_sample_types
        self.assertEqual(self.plan.sample_types, test_sample_types)

    def test_sample_types_property_from_list(self):
        liver_sample_type = Characteristic(category=OntologyAnnotation(
            term='organism part'), value='liver')
        blood_sample_type = Characteristic(category=OntologyAnnotation(
            term='organism part'), value='blood')
        brain_sample_type = 'brain'
        test_sample_types = [liver_sample_type, blood_sample_type,
                             liver_sample_type, brain_sample_type]
        self.plan.sample_types = test_sample_types
        self.assertEqual(self.plan.sample_types, {
            blood_sample_type, liver_sample_type,
            Characteristic(category=OntologyAnnotation(term='organism part'),
                           value=OntologyAnnotation(term=brain_sample_type))
        })

    def test_add_assay_type(self):
        ngs = OntologyAnnotation(term='ngs')
        test_assay_type = AssayType(measurement_type=ngs)
        self.plan.add_assay_type(test_assay_type)
        self.assertEqual(self.plan.assay_types, {test_assay_type})

    def test_add_assay_type_str(self):
        ngs = 'ngs'
        self.plan.add_assay_type(ngs)
        assay_type = AssayType(measurement_type=ngs)
        self.assertEqual(self.plan.assay_types, {assay_type})

    def test_add_assay_type_err(self):
        not_an_assay = OntologyAnnotation(term='bao')
        self.assertRaises(TypeError, self.plan.add_assay_type, not_an_assay)

    def test_add_sample_plan_record(self):
        liver_sample_type = Characteristic(category=OntologyAnnotation(
            term='organism part'), value=OntologyAnnotation(term='liver'))
        self.plan.add_sample_type(liver_sample_type)
        self.plan.add_sample_plan_record(liver_sample_type, 5)
        self.assertEqual(self.plan.sample_plan, {liver_sample_type: 5})

    def test_add_sample_plan_record_err(self):
        liver_sample_type = Characteristic(category=OntologyAnnotation(
            term='organism part'), value=OntologyAnnotation(term='liver'))
        self.plan.add_sample_type(liver_sample_type)
        self.assertRaises(TypeError,  self.plan.add_sample_plan_record,
                          liver_sample_type, 'five')

    def test_add_assay_plan_record(self):
        liver_sample_type = Characteristic(category=OntologyAnnotation(
            term='organism part'), value=OntologyAnnotation(term='liver'))
        self.plan.add_sample_type(liver_sample_type)
        self.plan.add_sample_plan_record(liver_sample_type, 5)
        ngs_assay_type = AssayType(measurement_type='ngs')
        self.plan.add_assay_type(ngs_assay_type)
        self.plan.add_assay_plan_record(liver_sample_type, ngs_assay_type)
        self.assertEqual(self.plan.assay_plan, {(liver_sample_type,
                                                 ngs_assay_type)})

    def test_add_assay_plan_record_err(self):
        liver_sample_type = Characteristic(category=OntologyAnnotation(
            term='organism part'), value=OntologyAnnotation(term='liver'))
        self.plan.add_sample_type(liver_sample_type)
        self.plan.add_sample_plan_record(liver_sample_type, 5)
        ngs_assay_type = AssayType(measurement_type='ngs')
        self.plan.add_assay_type(ngs_assay_type)
        blood_sample_type = Characteristic(category=OntologyAnnotation(
            term='organism part'), value=OntologyAnnotation(term='blood'))
        self.assertRaises(ValueError, self.plan.add_assay_plan_record,
                          blood_sample_type, ngs_assay_type)


class StudyEpochTest(unittest.TestCase):

    def setUp(self):
        self.epoch = StudyCell(name=TEST_EPOCH_0_NAME)

    def test__init__(self):
        self.assertEqual(self.epoch.name, TEST_EPOCH_0_NAME)
        self.assertEqual(self.epoch.rank, TEST_EPOCH_0_RANK)

class StudyArmTest(unittest.TestCase):

    def setUp(self):
        self.arm = StudyArm(name=TEST_STUDY_ARM_NAME)
        self.epoch = StudyCell()
        self.sample_assay_plan = SampleAssayPlan()

    def test__init__(self):
        self.assertEqual(self.arm.name, TEST_STUDY_ARM_NAME)

    def test_add_epoch2sample_assay_plan_mapping(self):
        pass

class StudyDesignTest(unittest.TestCase):

    def setUp(self):
        self.design = StudyDesign()
        self.agent = StudyFactor(name=BASE_FACTORS_[0]['name'], factor_type=BASE_FACTORS_[0]['type'])
        self.intensity = StudyFactor(name=BASE_FACTORS_[1]['name'], factor_type=BASE_FACTORS_[1]['type'])
        self.duration = StudyFactor(name=BASE_FACTORS_[2]['name'], factor_type=BASE_FACTORS_[2]['type'])
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
        # self.test_sequence = TreatmentSequence(ranked_treatments=[(self.first_treatment, 1), (self.second_treatment, 2)])
        self.test_arm = StudyArm()
        self.sample_plan = SampleAssayPlan(group_size=10)

    def test_sequences_plan_property(self):
        # other_test_sequence = TreatmentSequence(ranked_treatments=[(self.first_treatment, 2), (self.second_treatment, 1)])
        other_test_arm = StudyArm()
        other_sample_plan = SampleAssayPlan(group_size=12)
        """
        sequences_plan = {
            self.test_sequence: self.sample_plan,
            other_test_sequence: other_sample_plan
        }
        """
        self.design.sequences_plan = sequences_plan
        self.assertEqual(self.design.sequences_plan, sequences_plan)

    def test_sequences_plan_properties(self):
        not_a_sequences_plan_object = [self.test_sequence, self.sample_plan]
        self.assertRaises(TypeError, self.design.study_arms, not_a_sequences_plan_object)

    def test_sample_types_property(self):
        pass


class IsaModelObjectFactoryTest(unittest.TestCase):

    def setUp(self):
        self.investigation = Investigation(identifier='I1')
        self.f1 = StudyFactor(name='AGENT', factor_type=OntologyAnnotation(
            term='pertubation agent'))
        self.f2 = StudyFactor(name='INTENSITY',
                              factor_type=OntologyAnnotation(term='intensity'))
        self.f3 = StudyFactor(name='DURATION',
                              factor_type=OntologyAnnotation(term='time'))
        self.agent = StudyFactor(name=BASE_FACTORS_[0]['name'], factor_type=BASE_FACTORS_[0]['type'])
        self.intensity = StudyFactor(name=BASE_FACTORS_[1]['name'], factor_type=BASE_FACTORS_[1]['type'])
        self.duration = StudyFactor(name=BASE_FACTORS_[2]['name'], factor_type=BASE_FACTORS_[2]['type'])
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

    def test_add_treatment_epoch_not_starting_with_1(self):
        treatment_sequence = TreatmentSequence()
        self.assertRaises(TypeError, treatment_sequence.add_treatment, self.first_treatment, 3)

    def test_add_treatment_epoch_not_sequential(self):
        treatment_sequence = TreatmentSequence()
        treatment_sequence.add_treatment(self.first_treatment, 1)
        self.assertTrue(treatment_sequence.ranked_treatments.__len__() == 1)
        self.assertRaises(TypeError, treatment_sequence.add_treatment, self.second_treatment, 4)

    def test_add_treatment_epoch_not_sequential2(self):
        treatment_sequence = TreatmentSequence()
        treatment_sequence.add_treatment(self.first_treatment, 1)
        self.assertTrue(treatment_sequence.ranked_treatments.__len__() == 1)
        treatment_sequence.add_treatment(self.second_treatment, 2)
        self.assertRaises(TypeError, treatment_sequence.add_treatment, self.second_treatment, 4)

    def test_constructor(self):
        treatment_factory = TreatmentFactory(factors=[self.agent, self.intensity, self.duration])

        treatment_factory.add_factor_value(self.agent, {'acetyl salicylic acid', 'acetaminophen', 'ibuprofen'})
        treatment_factory.add_factor_value(self.intensity, {'high dose', 'low dose', 'medium dose'})
        treatment_factory.add_factor_value(self.duration, {'2 hr', '4 hr'})

        factorial_design_treatments = treatment_factory.compute_full_factorial_design()

        treatment_sequence = TreatmentSequence(ranked_treatments={
            (x, (i+1)) for i, x in enumerate(factorial_design_treatments)})

    def test_create_study_from_plan(self):
        plan = SampleAssayPlan()
        plan.add_sample_type('liver')
        plan.add_sample_plan_record('liver', 5)
        plan.add_sample_type('blood')
        plan.add_sample_plan_record('blood', 3)
        plan.group_size = 2
        treatment_factory = TreatmentFactory(
            factors=[self.f1, self.f2, self.f3])
        treatment_factory.add_factor_value(
            self.f1, {'cocaine', 'crack', 'aether'})
        treatment_factory.add_factor_value(self.f2, {'low', 'medium', 'high'})
        treatment_factory.add_factor_value(self.f3, {'short', 'long'})
        factorial_design_treatments = \
            treatment_factory.compute_full_factorial_design()
        for treatment in factorial_design_treatments:
            treatment.group_size = 2
        treatment_sequence = TreatmentSequence(
            ranked_treatments={(x, 1) for x in factorial_design_treatments})
        # makes each study group ranked in sequence
        study_design = StudyDesign()
        study_design.add_single_sequence_plan(
            treatment_sequence=treatment_sequence, study_plan=plan)
        study = IsaModelObjectFactory(study_design).create_study_from_plan()
        study.filename = 's_study.txt'
        self.investigation.studies = [study]
        self.assertEqual(36, len(study.sources))
        self.assertEqual(288, len(study.samples))

    def test_create_study_from_plan_single_arm_design(self):
        plan = SampleAssayPlan()
        plan.add_sample_type('liver')
        plan.add_sample_plan_record('liver', 5)
        plan.add_sample_type('blood')
        plan.add_sample_plan_record('blood', 3)
        plan.group_size = 2
        treatment_factory = TreatmentFactory(
            factors=[self.f1, self.f2, self.f3])
        treatment_factory.add_factor_value(
            self.f1, {'cocaine', 'crack', 'aether'})
        treatment_factory.add_factor_value(self.f2, {'low', 'medium', 'high'})
        treatment_factory.add_factor_value(self.f3, {'short', 'long'})
        factorial_design_treatments = \
            treatment_factory.compute_full_factorial_design()
        for treatment in factorial_design_treatments:
            treatment.group_size = 2

        design_factory = StudyDesignFactory(
            treatments=factorial_design_treatments, sample_plan=plan)
        # makes each study group ranked in sequence
        study_design = StudyDesign()
        study_design.study_arms = design_factory.compute_single_arm_design()
        study = IsaModelObjectFactory(study_design).create_study_from_plan()
        study.filename = 's_study.txt'
        self.investigation.studies = [study]
        self.assertEqual(2, len(study.sources))
        self.assertEqual(288, len(study.samples))

    def test_create_study_from_plan_parallel_design_3_arms(self):
        plan = SampleAssayPlan()
        plan.add_sample_type('liver')
        plan.add_sample_plan_record('liver', 5)
        plan.add_sample_type('blood')
        plan.add_sample_plan_record('blood', 3)
        plan.group_size = 2
        treatment_factory = TreatmentFactory(
            factors=[self.f1, self.f2, self.f3])
        treatment_factory.add_factor_value(
            self.f1, {'cocaine', 'crack', 'aether'})
        treatment_factory.add_factor_value(self.f2, {'low', 'medium', 'high'})
        treatment_factory.add_factor_value(self.f3, {'short', 'long'})
        factorial_design_treatments = \
            treatment_factory.compute_full_factorial_design()
        for treatment in factorial_design_treatments:
            treatment.group_size = 2

        design_factory = StudyDesignFactory(
            treatments=factorial_design_treatments, sample_plan=plan)
        # makes each study group ranked in sequence
        study_design = StudyDesign()
        study_design.study_arms = design_factory.compute_parallel_design(3)
        study = IsaModelObjectFactory(study_design).create_study_from_plan()
        study.filename = 's_study.txt'
        self.investigation.studies = [study]
        self.assertEqual(6, len(study.sources))
        self.assertEqual(288 * 3, len(study.samples))

    def test_create_study_from_plan_single_epoch_design(self):
        plan = SampleAssayPlan()
        plan.add_sample_type('liver')
        plan.add_sample_plan_record('liver', 5)
        plan.add_sample_type('blood')
        plan.add_sample_plan_record('blood', 3)
        plan.group_size = 2
        treatment_factory = TreatmentFactory(
            factors=[self.f1, self.f2, self.f3])
        treatment_factory.add_factor_value(
            self.f1, {'cocaine', 'crack', 'aether'})
        treatment_factory.add_factor_value(self.f2, {'low', 'medium', 'high'})
        treatment_factory.add_factor_value(self.f3, {'short', 'long'})
        factorial_design_treatments = \
            treatment_factory.compute_full_factorial_design()
        for treatment in factorial_design_treatments:
            treatment.group_size = 2

        design_factory = StudyDesignFactory(
            treatments=factorial_design_treatments, sample_plan=plan)
        # makes each study group ranked in sequence
        study_design = StudyDesign()
        study_design.study_arms = design_factory.compute_single_epoch_design()
        study = IsaModelObjectFactory(study_design).create_study_from_plan()
        study.filename = 's_study.txt'
        self.investigation.studies = [study]
        self.assertEqual(36, len(study.sources))
        self.assertEqual(288, len(study.samples))

    def test_create_study_from_plan_crossover_design(self):
        plan = SampleAssayPlan()
        plan.add_sample_type('liver')
        plan.add_sample_plan_record('liver', 5)
        plan.add_sample_type('blood')
        plan.add_sample_plan_record('blood', 3)
        plan.group_size = 2
        treatment_factory = TreatmentFactory(
            factors=[self.f1, self.f2, self.f3])
        treatment_factory.add_factor_value(
            self.f1, {'cocaine', 'crack', 'aether'})
        treatment_factory.add_factor_value(self.f2, {'low', 'medium', 'high'})
        treatment_factory.add_factor_value(self.f3, {'short', 'long'})
        factorial_design_treatments = \
            treatment_factory.compute_full_factorial_design()
        for treatment in factorial_design_treatments:
            treatment.group_size = 2

        design_factory = StudyDesignFactory(
            treatments=factorial_design_treatments, sample_plan=plan)
        # makes each study group ranked in sequence
        study_design = StudyDesign()
        study_design.study_arms = design_factory.compute_crossover_design()
        study = IsaModelObjectFactory(study_design).create_study_from_plan()
        study.filename = 's_study.txt'
        self.investigation.studies = [study]
        self.assertEqual(36, len(study.sources))
        self.assertEqual(288, len(study.samples))

    def test_create_study_from_plan_with_qc_parameters(self):
        plan = SampleAssayPlan()
        plan.add_sample_type('liver')
        plan.add_sample_plan_record('liver', 5)
        plan.add_sample_type('blood')
        plan.add_sample_plan_record('blood', 3)
        plan.group_size = 2
        plan.add_sample_type('solvent')
        plan.add_sample_qc_plan_record('solvent', 8)
        treatment_factory = TreatmentFactory(
            factors=[self.f1, self.f2, self.f3])
        treatment_factory.add_factor_value(
            self.f1, {'cocaine', 'crack', 'aether'})
        treatment_factory.add_factor_value(self.f2, {'low', 'medium', 'high'})
        treatment_factory.add_factor_value(self.f3, {'short', 'long'})
        ffactorial_design_treatments = \
            treatment_factory.compute_full_factorial_design()
        for treatment in ffactorial_design_treatments:
            treatment.group_size = 2
        treatment_sequence = TreatmentSequence(
            ranked_treatments={(x, 1) for x in ffactorial_design_treatments})
        # makes each study group ranked in sequence
        study_design = StudyDesign()
        study_design.add_single_sequence_plan(treatment_sequence, plan)
        study = IsaModelObjectFactory(study_design).create_study_from_plan()
        study.filename = 's_study.txt'
        self.investigation.studies = [study]
        # 36 sources, 36 QC sources
        self.assertEqual(72, len(study.sources))
        self.assertEqual(36, len(
            [x for x in study.sources
             if x.get_char('Material Type').value.term == 'solvent']))
        # 288 samples plus 36 QC samples
        self.assertEqual(324, len(study.samples))
        self.assertEqual(3, len(study.factors))

    def test_create_study_from_plan_with_qc_source_characteristics(self):
        plan = SampleAssayPlan()
        plan.add_sample_type('liver')
        plan.add_sample_plan_record('liver', 5)
        plan.add_sample_type('blood')
        plan.add_sample_plan_record('blood', 3)
        plan.group_size = 2
        plan.add_sample_type('solvent')
        plan.add_sample_qc_plan_record('solvent', 8)
        batch1 = SampleQCBatch()
        batch1.material = OntologyAnnotation(term='blank')
        batch1.characteristic_values = [
            Characteristic(category=OntologyAnnotation(term='charac1'),
                           value=5),
            Characteristic(category=OntologyAnnotation(term='charac1'),
                           value=4),
            Characteristic(category=OntologyAnnotation(term='charac1'),
                           value=3),
            Characteristic(category=OntologyAnnotation(term='charac1'),
                           value=2),
            Characteristic(category=OntologyAnnotation(term='charac1'),
                           value=1),
            Characteristic(category=OntologyAnnotation(term='charac1'),
                           value=1),
            Characteristic(category=OntologyAnnotation(term='charac1'),
                           value=1),
            Characteristic(category=OntologyAnnotation(term='charac1'),
                           value=1),
            Characteristic(category=OntologyAnnotation(term='charac1'),
                           value=1),
            Characteristic(category=OntologyAnnotation(term='charac1'),
                           value=1),
            Characteristic(category=OntologyAnnotation(term='charac1'),
                           value=1)
        ]
        plan.pre_run_batch = batch1
        batch2 = SampleQCBatch()
        batch2.material = OntologyAnnotation(term='solvent')
        batch2.characteristic_values = [
            Characteristic(category=OntologyAnnotation(term='charac2'), value=x)
            for x in reversed([x.value for x in batch1.parameter_values])]
        plan.post_run_batch = batch2

        treatment_factory = TreatmentFactory(
            factors=[self.f1, self.f2, self.f3])
        treatment_factory.add_factor_value(
            self.f1, {'cocaine', 'crack', 'aether'})
        treatment_factory.add_factor_value(self.f2, {'low', 'medium', 'high'})
        treatment_factory.add_factor_value(self.f3, {'short', 'long'})
        ffactorial_design_treatments = \
            treatment_factory.compute_full_factorial_design()
        for treatment in ffactorial_design_treatments:
            treatment.group_size = 2
        treatment_sequence = TreatmentSequence(
            ranked_treatments={(x, 1) for x in ffactorial_design_treatments})
        study_design = StudyDesign()
        study_design.add_single_sequence_plan(treatment_sequence, plan)
        study = IsaModelObjectFactory(study_design).create_study_from_plan()
        study.filename = 's_study.txt'
        self.investigation.studies = [study]
        # 36 sources, 56 QC sources
        self.assertEqual(86, len(study.sources))
        self.assertEqual(38, len(
            [x for x in study.sources
             if x.get_char('Material Type').value.term == 'solvent']))
        self.assertEqual(12, len(
            [x for x in study.sources
             if x.get_char('Material Type').value.term == 'blank']))
        # 288 samples plus 36 QC samples
        self.assertEqual(335, len(study.samples))

    def test_study_from_2_level_factorial_plan(self):
        factor = StudyFactor(name='1')
        treatment_factory = TreatmentFactory(factors=[factor])
        treatment_factory.add_factor_value(factor, 'a')
        treatment_factory.add_factor_value(factor, 'b')
        treatments = treatment_factory.compute_full_factorial_design()
        for treatment in treatments:
            treatment.group_size = 5
        self.assertEqual(len(treatments), 2)
        sample_assay_plan = SampleAssayPlan()
        sample_assay_plan.group_size = 5
        sample_assay_plan.add_sample_type('liver')
        sample_assay_plan.add_sample_type('blood')
        sample_assay_plan.add_sample_type('urine')
        sample_assay_plan.add_sample_plan_record('liver', 1)
        sample_assay_plan.add_sample_plan_record('blood', 4)
        sample_assay_plan.add_sample_plan_record('urine', 10)
        design_factory = StudyDesignFactory(
            treatments=treatments, sample_plan=sample_assay_plan)
        study_design = StudyDesign()
        study_design.study_arms = design_factory.compute_crossover_design()
        study = IsaModelObjectFactory(study_design).create_study_from_plan()
        self.assertEqual(len(study.sources), 10)  # number of subjects
        self.assertEqual(len(study.samples), 150)

        ms_assay_type = AssayType(measurement_type='metabolite profiling',
                                  technology_type='mass spectrometry')
        ms_assay_type.topology_modifiers = MSTopologyModifiers(
            sample_fractions=set(),
            injection_modes={MSInjectionMode(
                injection_mode='FIA',
                acquisition_modes={
                    MSAcquisitionMode(acquisition_method='negative',
                                      technical_repeats=2),
                    MSAcquisitionMode(acquisition_method='positive',
                                      technical_repeats=2),
                }
            )}
        )
        ngs_assay_type = AssayType(
            measurement_type='nucleotide sequencing', technology_type='NGS')
        ngs_assay_type.topology_modifiers = DNASeqAssayTopologyModifiers(
            technical_replicates=1, distinct_libraries=1
        )
        sample_assay_plan.add_assay_type(ms_assay_type)
        sample_assay_plan.add_assay_type(ngs_assay_type)
        sample_assay_plan.add_assay_plan_record('liver', ms_assay_type)
        sample_assay_plan.add_assay_plan_record('blood', ms_assay_type)
        sample_assay_plan.add_assay_plan_record('urine', ms_assay_type)
        sample_assay_plan.add_assay_plan_record('liver', ngs_assay_type)
        sample_assay_plan.add_assay_plan_record('blood', ngs_assay_type)
        sample_assay_plan.add_assay_plan_record('urine', ngs_assay_type)
        design_factory = StudyDesignFactory(
            treatments=treatments, sample_plan=sample_assay_plan)
        study_design = StudyDesign()
        study_design.study_arms = design_factory.compute_crossover_design()
        study = IsaModelObjectFactory(study_design).create_assays_from_plan()
        self.assertEqual(len(study.assays), 6)
        self.assertEqual(len(study.protocols), 4)

    def test_study_from_2_by_3_by_2_factorial_plan(self):
        factor1 = StudyFactor(name='1')
        factor2 = StudyFactor(name='2')
        factor3 = StudyFactor(name='3')
        treatment_factory = TreatmentFactory(
            factors=[factor1, factor2, factor3])
        treatment_factory.add_factor_value(factor1, 'a')
        treatment_factory.add_factor_value(factor1, 'b')
        treatment_factory.add_factor_value(factor2, 'i')
        treatment_factory.add_factor_value(factor2, 'ii')
        treatment_factory.add_factor_value(factor2, 'iii')
        treatment_factory.add_factor_value(factor3, 'alpha')
        treatment_factory.add_factor_value(factor3, 'beta')
        treatments = treatment_factory.compute_full_factorial_design()
        for treatment in treatments:
            treatment.group_size = 3
        self.assertEqual(len(treatments), 12)
        sample_assay_plan = SampleAssayPlan()
        sample_assay_plan.group_size = 3
        sample_assay_plan.add_sample_type('liver')
        sample_assay_plan.add_sample_type('blood')
        sample_assay_plan.add_sample_type('urine')
        sample_assay_plan.add_sample_plan_record('liver', 1)
        sample_assay_plan.add_sample_plan_record('blood', 1)
        sample_assay_plan.add_sample_plan_record('urine', 2)
        design_factory = StudyDesignFactory(
            treatments=treatments, sample_plan=sample_assay_plan)
        study_design = StudyDesign()
        study_design.study_arms = design_factory.compute_crossover_design()
        study = IsaModelObjectFactory(study_design).create_study_from_plan()
        self.assertEqual(len(study.sources), 36)  # number of subjects
        self.assertEqual(len(study.samples), 144)

        ms_assay_type = AssayType(measurement_type='metabolite profiling',
                                  technology_type='mass spectrometry')
        ms_assay_type.topology_modifiers = MSTopologyModifiers(
            sample_fractions={'polar'},
            injection_modes={MSInjectionMode()}
        )
        ngs_assay_type = AssayType(
            measurement_type='nucleotide sequencing', technology_type='NGS')
        ngs_assay_type.topology_modifiers = DNASeqAssayTopologyModifiers(
            technical_replicates=1, distinct_libraries=1
        )
        sample_assay_plan.add_assay_type(ms_assay_type)
        sample_assay_plan.add_assay_type(ngs_assay_type)
        sample_assay_plan.add_assay_plan_record('liver', ms_assay_type)
        sample_assay_plan.add_assay_plan_record('liver', ngs_assay_type)
        sample_assay_plan.add_assay_plan_record('blood', ms_assay_type)
        sample_assay_plan.add_assay_plan_record('blood', ngs_assay_type)

        ms_assay_type1 = AssayType(measurement_type='metabolite profiling',
                                  technology_type='mass spectrometry')
        ms_assay_type1.topology_modifiers = MSTopologyModifiers(
            sample_fractions=set(),
            injection_modes={MSInjectionMode(
                injection_mode='LC',
                acquisition_modes={MSAcquisitionMode(
                    acquisition_method='negative', technical_repeats=1)}
            )}
        )
        sample_assay_plan.add_assay_type(ms_assay_type1)
        ms_assay_type2 = AssayType(measurement_type='metabolite profiling',
                                   technology_type='mass spectrometry')
        ms_assay_type2.topology_modifiers = MSTopologyModifiers(
            sample_fractions=set(),
            injection_modes={MSInjectionMode(
                injection_mode='FIA',
                acquisition_modes={
                    MSAcquisitionMode(acquisition_method='negative',
                                      technical_repeats=2),
                    MSAcquisitionMode(acquisition_method='positive',
                                      technical_repeats=2),
                }
            )}
        )
        sample_assay_plan.add_assay_type(ms_assay_type2)
        sample_assay_plan.add_assay_plan_record('urine', ms_assay_type1)
        sample_assay_plan.add_assay_plan_record('urine', ms_assay_type2)
        sample_assay_plan.add_assay_type(ngs_assay_type)
        design_factory = StudyDesignFactory(
            treatments=treatments, sample_plan=sample_assay_plan)
        study_design = StudyDesign()
        study_design.study_arms = design_factory.compute_crossover_design()
        study = IsaModelObjectFactory(study_design).create_assays_from_plan()
        self.assertEqual(len(study.assays), 3)
        self.assertEqual(len(study.protocols), 5)

    def test_study_from_repeated_measure_plan(self):
        factor1 = StudyFactor(name='1')
        factor2 = StudyFactor(name='2')
        factor3 = StudyFactor(name='3')
        treatment_factory = TreatmentFactory(
            factors=[factor1, factor2, factor3])
        treatment_factory.add_factor_value(factor1, 'a')
        treatment_factory.add_factor_value(factor1, 'b')
        treatment_factory.add_factor_value(factor2, 'i')
        treatment_factory.add_factor_value(factor2, 'ii')
        treatment_factory.add_factor_value(factor2, 'iii')
        treatment_factory.add_factor_value(factor3, 'alpha')
        treatment_factory.add_factor_value(factor3, 'beta')
        treatments = treatment_factory.compute_full_factorial_design()
        for treatment in treatments:
            treatment.group_size = 3
        self.assertEqual(len(treatments), 12)
        sample_assay_plan = SampleAssayPlan()
        sample_assay_plan.add_sample_type('liver')
        sample_assay_plan.add_sample_type('blood')
        sample_assay_plan.add_sample_type('urine')
        sample_assay_plan.add_sample_plan_record('liver', 1)
        sample_assay_plan.add_sample_plan_record('blood', 1)
        sample_assay_plan.add_sample_plan_record('urine', 2)
        design_factory = StudyDesignFactory(
            treatments=treatments, sample_plan=sample_assay_plan)
        study_design = StudyDesign()
        study_design.study_arms = design_factory.compute_single_arm_design()
        study = IsaModelObjectFactory(study_design).create_study_from_plan()
        self.assertEqual(len(study.sources), 36)  # number of subjects
        self.assertEqual(len(study.samples), 288)
        ms_assay_type = AssayType(measurement_type='metabolite profiling',
                                  technology_type='mass spectrometry')
        ms_assay_type.topology_modifiers = MSTopologyModifiers(
            sample_fractions=set(),
            injection_modes={MSInjectionMode(
                injection_mode='FIA',
                acquisition_modes={
                    MSAcquisitionMode(acquisition_method='negative',
                                      technical_repeats=2),
                    MSAcquisitionMode(acquisition_method='positive',
                                      technical_repeats=2),
                }
            ),
            MSInjectionMode(
                injection_mode='LC',
                acquisition_modes={
                    MSAcquisitionMode(acquisition_method='negative',
                                      technical_repeats=2),
                    MSAcquisitionMode(acquisition_method='positive',
                                      technical_repeats=2),
                }
            )
            }
        )
        ngs_assay_type = AssayType(
            measurement_type='nucleotide sequencing', technology_type='NGS')
        ngs_assay_type.topology_modifiers = DNASeqAssayTopologyModifiers(
            technical_replicates=1, distinct_libraries=1
        )
        sample_assay_plan.add_assay_type(ms_assay_type)
        sample_assay_plan.add_assay_type(ngs_assay_type)
        sample_assay_plan.add_assay_plan_record('liver', ms_assay_type)
        sample_assay_plan.add_assay_plan_record('liver', ngs_assay_type)
        sample_assay_plan.add_assay_plan_record('blood', ms_assay_type)
        sample_assay_plan.add_assay_plan_record('blood', ngs_assay_type)

        ms_assay_type1 = AssayType(measurement_type='metabolite profiling',
                                   technology_type='mass spectrometry')
        ms_assay_type1.topology_modifiers = MSTopologyModifiers(
            injection_modes={MSInjectionMode(
                injection_mode='LC',
                acquisition_modes={
                    MSAcquisitionMode(acquisition_method='negative',
                                      technical_repeats=1)
                }
            )}
        )
        sample_assay_plan.add_assay_type(ms_assay_type1)
        ms_assay_type2 = AssayType(measurement_type='metabolite profiling',
                                   technology_type='mass spectrometry')
        ms_assay_type2.topology_modifiers = MSTopologyModifiers(
            injection_modes={MSInjectionMode(
                injection_mode='FIA',
                acquisition_modes={
                    MSAcquisitionMode(acquisition_method='positive',
                                      technical_repeats=2),
                    MSAcquisitionMode(acquisition_method='negative',
                                      technical_repeats=2)
                }
            )}
        )
        sample_assay_plan.add_assay_type(ms_assay_type2)
        sample_assay_plan.add_assay_plan_record('urine', ms_assay_type1)
        sample_assay_plan.add_assay_plan_record('urine', ms_assay_type2)

        sample_assay_plan.add_assay_type(ngs_assay_type)
        design_factory = StudyDesignFactory(
            treatments=treatments, sample_plan=sample_assay_plan)
        study_design = StudyDesign()
        study_design.study_arms = design_factory.compute_crossover_design()
        study = IsaModelObjectFactory(study_design).create_assays_from_plan()
        self.assertEqual(len(study.assays), 11)
        self.assertEqual(len(study.protocols), 6)