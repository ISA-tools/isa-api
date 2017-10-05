import unittest
from collections import OrderedDict

from isatools import isatab
from isatools.model import (Investigation, StudyFactor, FactorValue,
                            OntologyAnnotation)
from isatools.create.models import (InterventionStudyDesign, Treatment,
                                    Characteristic, TreatmentFactory,
                                    TreatmentSequence, AssayType,
                                    SampleAssayPlan, INTERVENTIONS,
                                    BASE_FACTORS_ as BASE_FACTORS,
                                    IsaModelObjectFactory)

NAME = 'name'
FACTORS_0_VALUE = 'nitroglycerin'
FACTORS_1_VALUE = 5
FACTORS_1_UNIT = 'kg/m^3'
FACTORS_2_VALUE = 100.0
FACTORS_2_VALUE_ALT = 50.0
FACTORS_2_UNIT = 's'


""""
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
        sample_type = Characteristic(category=OntologyAnnotation(term='organism part'), value='liver')
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

    def test_sample_types_property(self):
        liver_sample_type = Characteristic(category=OntologyAnnotation(term='organism part'), value='liver')
        blood_sample_type = Characteristic(category=OntologyAnnotation(term='organism part'), value='blood')
        self.sample_plan.sample_types_map = {
            liver_sample_type: (0, 1, 1),
            blood_sample_type: (3, 3, 4)
        }
        self.assertEqual(self.sample_plan.sample_types, { liver_sample_type, blood_sample_type })

    def test_sample_types_property_empty(self):
        self.assertEqual(self.sample_plan.sample_types, set())
"""


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
                         "Treatment(factor_type=chemical intervention, factor_values=("
                         "isatools.model.FactorValue(factor_name='{0}', value={1}, unit=None), "
                         "isatools.model.FactorValue(factor_name='{2}', value={3}, unit={4}), "
                         "isatools.model.FactorValue(factor_name='{5}', value={6}, unit={7})"
                         "))".format(BASE_FACTORS[0][NAME], repr(FACTORS_0_VALUE),
                                     BASE_FACTORS[1][NAME], FACTORS_1_VALUE, repr(FACTORS_1_UNIT),
                                     BASE_FACTORS[2][NAME], FACTORS_2_VALUE, repr(FACTORS_2_UNIT)))

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

    def test_add_factor_value_set(self):
        values_to_add = {'agent_orange', 'crack, cocaine'}
        factor = StudyFactor(name=BASE_FACTORS[0]['name'], factor_type=BASE_FACTORS[0]['type'])
        self.factory.add_factor_value(factor, values_to_add)
        self.assertEqual(self.factory.factors.get(factor), values_to_add)

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
        self.assertEqual("TreatmentSequence([(Treatment(factor_type=chemical "
                         "intervention, factor_values=(isatools.model.FactorValue(factor_name="
                         "isatools.model.StudyFactor(name='AGENT', factor_type="
                         "isatools.model.OntologyAnnotation("
                         "term='perturbation agent', term_source=None, "
                         "term_accession='', comments=[]), comments=[]), "
                         "value='crack', unit=None), isatools.model.FactorValue("
                         "factor_name=isatools.model.StudyFactor("
                         "name='INTENSITY', "
                         "factor_type=isatools.model.OntologyAnnotation("
                         "term='intensity', term_source=None, "
                         "term_accession='', comments=[]), comments=[]), "
                         "value='low', unit=None), isatools.model.FactorValue("
                         "factor_name=isatools.model.StudyFactor("
                         "name='DURATION', "
                         "factor_type=isatools.model.OntologyAnnotation("
                         "term='time', term_source=None, term_accession='', "
                         "comments=[]), comments=[]), value='short', "
                         "unit=None))), 1), (Treatment("
                         "factor_type=chemical intervention, "
                         "factor_values=(isatools.model.FactorValue("
                         "factor_name=isatools.model.StudyFactor(name='AGENT', "
                         "factor_type=isatools.model.OntologyAnnotation("
                         "term='perturbation agent', term_source=None, "
                         "term_accession='', comments=[]), comments=[]), "
                         "value='crack', unit=None), isatools.model.FactorValue(factor_name="
                         "isatools.model.StudyFactor(name='INTENSITY', "
                         "factor_type=isatools.model.OntologyAnnotation("
                         "term='intensity', term_source=None, "
                         "term_accession='', comments=[]), comments=[]), "
                         "value='low', unit=None), isatools.model.FactorValue("
                         "factor_name=isatools.model.StudyFactor("
                         "name='DURATION', "
                         "factor_type=isatools.model.OntologyAnnotation("
                         "term='time', term_source=None, term_accession='', "
                         "comments=[]), comments=[]), value='long', "
                         "unit=None))), 2)])",
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
        self.sample_plan = SampleAssayPlan(group_size=10, sample_plan={}, assay_plan=None)

    def test_add_single_sequence_plan(self):
        self.design.add_single_sequence_plan(treatment_sequence=self.test_sequence, study_plan=self.sample_plan)
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
        other_sample_plan = SampleAssayPlan(group_size=12)
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


class IsaModelObjectFactoryTest(unittest.TestCase):

    def setUp(self):
        self.investigation = Investigation(identifier='I1')
        self.f1 = StudyFactor(name='AGENT', factor_type=OntologyAnnotation(
            term='pertubation agent'))
        self.f2 = StudyFactor(name='INTENSITY',
                              factor_type=OntologyAnnotation(term='intensity'))
        self.f3 = StudyFactor(name='DURATION',
                              factor_type=OntologyAnnotation(term='time'))

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
        ffactorial_design_treatments = \
            treatment_factory.compute_full_factorial_design()
        treatment_sequence = TreatmentSequence(
            ranked_treatments={
                (x, i) for i, x in enumerate(ffactorial_design_treatments)})
        # makes each study group ranked in sequence
        study = IsaModelObjectFactory(
            plan, treatment_sequence).create_study_from_plan()
        study.filename = 's_study.txt'
        self.investigation.studies = [study]
        self.assertEqual(36, len(study.sources))
        self.assertEqual(288, len(study.samples))

    def test_create_study_from_plan_with_qc(self):
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
        treatment_sequence = TreatmentSequence(
            ranked_treatments={(x, i) for i, x in
                               enumerate(ffactorial_design_treatments)})
        # makes each study group ranked in sequence
        study = IsaModelObjectFactory(
            plan,  treatment_sequence).create_study_from_plan()
        study.filename = 's_study.txt'
        # print(isatab.dumps(self.investigation))
        self.investigation.studies = [study]
        # 36 sources, 36 QC sources
        self.assertEqual(72, len(study.sources))
        self.assertEqual(36, len(
            [x for x in study.sources
             if x.get_char('Material Type').value.term == 'solvent']))
        # 288 samples plus 36 QC samples
        self.assertEqual(324, len(study.samples))