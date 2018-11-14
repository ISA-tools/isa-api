import unittest
from collections import OrderedDict

from isatools.model import *
from isatools.create.models import *
from isatools.errors import ISAModelAttributeError, ISAModelValueError

NAME = 'name'
FACTORS_0_VALUE = 'nitroglycerin'
FACTORS_0_VALUE_ALT = 'alchohol'
FACTORS_0_VALUE_THIRD = 'water'
FACTORS_1_VALUE = 5
FACTORS_1_UNIT = OntologyAnnotation(term='kg/m^3')
FACTORS_2_VALUE = 100.0
FACTORS_2_VALUE_ALT = 50.0
FACTORS_2_UNIT = OntologyAnnotation(term='s')

TEST_EPOCH_0_NAME = 'test epoch 0'
TEST_EPOCH_1_NAME = 'test epoch 1'
TEST_EPOCH_2_NAME = 'test epoch 2'

TEST_STUDY_ARM_NAME_00 = 'test arm'
TEST_STUDY_ARM_NAME_01 = 'another arm'
TEST_STUDY_ARM_NAME_02 = 'yet another arm'

TEST_STUDY_DESIGN_NAME = 'test study design'

TEST_EPOCH_0_RANK = 0

SCREEN_DURATION_VALUE = 100
FOLLOW_UP_DURATION_VALUE = 5 * 366
WASHOUT_DURATION_VALUE = 30
DURATION_UNIT = OntologyAnnotation(term='day')


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
                         "isatools.create.models.NonTreatment(type='screen', duration=isatools.model.FactorValue("
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
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))

    def test_repr(self):
        self.assertEqual(repr(self.treatment),
                         "isatools.create.models.Treatment(type=chemical intervention, "
                         "factor_values=[isatools.model.FactorValue(factor_name=isatools.model.StudyFactor(name='AGENT'"
                         ", factor_type=isatools.model.OntologyAnnotation(term='perturbation agent', term_source=None, "
                         "term_accession='', comments=[]), comments=[]), value='nitroglycerin', unit=None), "
                         "isatools.model.FactorValue(factor_name=isatools.model.StudyFactor(name='DURATION', "
                         "factor_type=isatools.model.OntologyAnnotation(term='time', term_source=None, "
                         "term_accession='', comments=[]), comments=[]), value=100.0, "
                         "unit=isatools.model.OntologyAnnotation(term='s', term_source=None, term_accession='', "
                         "comments=[])), isatools.model.FactorValue(factor_name=isatools.model.StudyFactor("
                         "name='INTENSITY', factor_type=isatools.model.OntologyAnnotation(term='intensity', "
                         "term_source=None, term_accession='', comments=[]), comments=[]), value=5, "
                         "unit=isatools.model.OntologyAnnotation(term='kg/m^3', term_source=None, term_accession='', "
                         "comments=[]))], group_size=0)")

    def test_hash(self):
        self.assertEqual(hash(self.treatment), hash(repr(self.treatment)))

    def test_eq(self):
        same_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))
        self.assertEqual(self.treatment, same_treatment)
        self.assertEqual(hash(self.treatment), hash(same_treatment))

    def test_ne(self):
        other_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE_ALT, unit=FACTORS_2_UNIT)
        ))
        self.assertNotEqual(self.treatment, other_treatment)
        self.assertNotEqual(hash(self.treatment), hash(other_treatment))


class StudyCellTest(unittest.TestCase):

    def setUp(self):
        self.cell = StudyCell(name=TEST_EPOCH_0_NAME)
        self.first_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))
        self.second_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE_ALT),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))
        self.third_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE_ALT),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE_ALT, unit=FACTORS_2_UNIT)
        ))
        self.fourth_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE_THIRD),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))
        self.screen = NonTreatment(element_type=SCREEN,
                                   duration_value=SCREEN_DURATION_VALUE, duration_unit=DURATION_UNIT)
        self.run_in = NonTreatment(element_type=RUN_IN,
                                    duration_value=WASHOUT_DURATION_VALUE, duration_unit=DURATION_UNIT)
        self.washout = NonTreatment(element_type=WASHOUT,
                                    duration_value=WASHOUT_DURATION_VALUE, duration_unit=DURATION_UNIT)
        self.follow_up = NonTreatment(element_type=FOLLOW_UP,
                                      duration_value=FOLLOW_UP_DURATION_VALUE, duration_unit=DURATION_UNIT)
        self.potential_concomitant_washout = NonTreatment(element_type=WASHOUT, duration_value=FACTORS_2_VALUE,
                                                          duration_unit=FACTORS_2_UNIT)

    def test__init__(self):
        self.assertEqual(self.cell.name, TEST_EPOCH_0_NAME)

    def test_elements_property(self):
        elements = (self.first_treatment, self.second_treatment)
        self.assertEqual(self.cell.elements, list(), 'The initialized elements set is empty')
        self.cell.elements = elements
        self.assertEqual(self.cell.elements, list(elements), 'After assignment the elements list contains two elements')

    # _non_treatment_check() tests
    def test_non_treatment_check__empty_cell_00(self):
        self.assertTrue(self.cell._non_treatment_check([], self.screen),
                        'A SCREEN element can alway be added to an empty cell')

    def test_non_treatment_check__empty_cell_01(self):
        self.assertTrue(self.cell._non_treatment_check([], self.run_in),
                        'A RUN-IN element can alway be added to an empty cell')

    def test_non_treatment_check__empty_cell_02(self):
        self.assertTrue(self.cell._non_treatment_check([], self.washout),
                        'A WASHOUT element can alway be added to an empty cell')

    def test_non_treatment_check__empty_cell_03(self):
        self.assertTrue(self.cell._non_treatment_check([], self.follow_up),
                        'A FOLLOW-UP element can alway be added to an empty cell')

    def test_non_treatment_check__screen_cell_00(self):
        self.assertFalse(self.cell._non_treatment_check([self.screen], self.screen),
                         'A SCREEN element cannot be added to a cell with a SCREEN')

    def test_non_treatment_check__screen_cell_01(self):
        self.assertTrue(self.cell._non_treatment_check([self.screen], self.run_in),
                        'A RUN-IN element can be added to a cell with a SCREEN after the SCREEN')

    def test_non_treatment_check__screen_cell_02(self):
        self.assertFalse(self.cell._non_treatment_check([self.screen], self.run_in, 0),
                        'A RUN-IN element cannot be added to a cell with a SCREEN before the SCREEN')

    def test_non_treatment_check__screen_cell_03(self):
        self.assertFalse(self.cell._non_treatment_check([self.screen], self.washout),
                        'A WASHOUT element cannot be added to a cell with a SCREEN')

    def test_non_treatment_check__screen_cell_04(self):
        self.assertFalse(self.cell._non_treatment_check([self.screen], self.follow_up),
                         'A FOLLOW-UP element cannot be added to a cell with a SCREEN')

    def test_non_treatment_check__run_in_cell_00(self):
        self.assertFalse(self.cell._non_treatment_check([self.run_in], self.screen),
                         'A SCREEN element cannot be added to a cell with a RUN-IN after the RUN-IN')

    def test_non_treatment_check__run_in_cell_01(self):
        self.assertTrue(self.cell._non_treatment_check([self.run_in], self.screen, 0),
                        'A RUN-IN element can be added to a cell with a RUN-IN before the RUN-IN')

    def test_non_treatment_check__run_in_cell_02(self):
        self.assertFalse(self.cell._non_treatment_check([self.run_in], self.run_in),
                        'A RUN-IN element can be added to a cell with a RUN-IN')

    def test_non_treatment_check__run_in_cell_03(self):
        self.assertFalse(self.cell._non_treatment_check([self.run_in], self.washout),
                        'A WASHOUT element cannot be added to a cell with a RUN-IN')

    def test_non_treatment_check__run_in_cell_04(self):
        self.assertFalse(self.cell._non_treatment_check([self.run_in], self.follow_up),
                         'A FOLLOW-UP element cannot be added to a cell with a RUN-IN')

    def test_non_treatment_check__washout_cell_00(self):
        self.assertFalse(self.cell._non_treatment_check([self.washout], self.screen),
                         'A SCREEN element cannot be added to a cell with a WASHOUT')

    def test_non_treatment_check__washout_cell_01(self):
        self.assertFalse(self.cell._non_treatment_check([self.washout], self.run_in),
                        'A RUN-IN element can be added to a cell with a WASHOUT')

    def test_non_treatment_check__washout_cell_02(self):
        self.assertFalse(self.cell._non_treatment_check([self.washout], self.washout),
                         'A WASHOUT element cannot be added to a cell with a WASHOUT '
                         'immediately after the first WASHOUT')

    def test_non_treatment_check__washout_cell_03(self):
        self.assertFalse(self.cell._non_treatment_check([self.washout], self.follow_up),
                         'A FOLLOW-UP element cannot be added to a cell with a WASHOUT')

    def test_non_treatment_check__follow_up_cell_00(self):
        self.assertFalse(self.cell._non_treatment_check([self.follow_up], self.screen),
                         'A SCREEN element cannot be added to a cell with a FOLLOW-UP')

    def test_non_treatment_check__follow_up_cell_01(self):
        self.assertFalse(self.cell._non_treatment_check([self.follow_up], self.run_in),
                        'A RUN-IN element can be added to a cell with a FOLLOW-UP')

    def test_non_treatment_check__follow_up_cell_02(self):
        self.assertFalse(self.cell._non_treatment_check([self.follow_up], self.washout),
                        'A WASHOUT element cannot be added to a cell with a WASHOUT immediately after the FOLLOW-UP')

    def test_non_treatment_check__follow_up_cell_03(self):
        self.assertFalse(self.cell._non_treatment_check([self.follow_up], self.follow_up),
                         'A FOLLOW-UP element cannot be added to a cell with a FOLLOW-UP')

    def test_non_treatment_check__treatment_cell_00(self):
        self.assertFalse(self.cell._non_treatment_check([self.first_treatment], self.screen),
                         'A SCREEN element cannot be added to a cell with a treatment')
        self.assertFalse(self.cell._non_treatment_check([self.first_treatment], self.screen, 0),
                         'A SCREEN element cannot be added to a cell with a treatment before the treatment')

    def test_non_treatment_check__treatment_cell_01(self):
        self.assertFalse(self.cell._non_treatment_check([self.first_treatment], self.run_in),
                        'A RUN-IN element can be added to a cell with a treatment')
        self.assertFalse(self.cell._non_treatment_check([self.first_treatment], self.run_in, 0),
                        'A RUN-IN element can be added to a cell with a treatment before the treatment')

    def test_non_treatment_check__treatment_cell_02(self):
        self.assertTrue(self.cell._non_treatment_check([self.first_treatment], self.washout),
                        'A WASHOUT element can be added to a cell with a treatment after the treatment')
        self.assertTrue(self.cell._non_treatment_check([self.first_treatment], self.washout, 0),
                        'A WASHOUT element can be added to a cell with a treatment before the treatment')

    def test_non_treatment_check__treatment_cell_03(self):
        self.assertFalse(self.cell._non_treatment_check([self.first_treatment], self.follow_up),
                         'A FOLLOW-UP element cannot be added to a cell with a treatment')
        self.assertFalse(self.cell._non_treatment_check([self.first_treatment], self.follow_up, 0),
                         'A FOLLOW-UP element cannot be added to a cell with a treatment after the treatment')

    def test_non_treatment_check__multi_element_cell_00(self):
        self.assertTrue(self.cell._non_treatment_check([self.first_treatment, self.washout, self.second_treatment],
                                                       self.washout),
                        'A WASHOUT element can be added at the end of a cell with 2 treatments intersped by a washout')
        self.assertTrue(self.cell._non_treatment_check([
            self.first_treatment, self.washout, self.second_treatment
        ], self.washout), 'A WASHOUT element can be added at the beginning of a cell with 2 treatments '
                          'intersped by a washout')

    def test_non_treatment_check_multi_element_cell_01(self):
        self.assertTrue(self.cell._non_treatment_check([
            {self.first_treatment, self.second_treatment}, self.washout, self.second_treatment
        ], self.washout), 'A WASHOUT element can be added at the end of a cell with a treatment set and a treatment '
                          'intersped by a washout')
        self.assertTrue(self.cell._non_treatment_check([
            {self.first_treatment, self.second_treatment}, self.washout, self.second_treatment
        ], self.washout, 0), 'A WASHOUT element can be added at the beginning of a cell with a treatment set and a '
                             'treatment intersped by a washout')

    def test_non_treatment_check_multi_element_cell_02(self):
        self.assertTrue(self.cell._non_treatment_check([
            self.first_treatment, self.washout, {self.fourth_treatment, self.second_treatment}
        ], self.washout), 'A WASHOUT element can be added at the end of a cell with a treatment and a treatment set'
                          'intersped by a washout')
        self.assertTrue(self.cell._non_treatment_check([
            self.first_treatment, self.washout, {self.fourth_treatment, self.second_treatment}
        ], self.washout, 0), 'A WASHOUT element can be added at the beginning of a cell with a treatment and a '
                             'treatment set intersped by a washout')

    # _treatment_check() tests
    def test_treatment_check__screen_cell(self):
        self.assertFalse(self.cell._treatment_check([self.screen]), 'A treatment cannot be inserted into a SCREEN cell')

    def test_treatment_check__run_in_cell(self):
        self.assertFalse(self.cell._treatment_check([self.run_in]), 'A treatment cannot be inserted into a RUN-IN cell')

    def test_treatment_check__washout_cell(self):
        self.assertTrue(self.cell._treatment_check([self.washout]),
                         'A treatment can be inserted into a WASHOUT cell')

    def test_treatment_check__follow_up_cell(self):
        self.assertFalse(self.cell._treatment_check([self.follow_up]),
                         'A treatment cannot be inserted into a FOLLOW-UP cell')

    def test_treatment_check__screen_cell(self):
        self.assertFalse(self.cell._treatment_check([self.screen]), 'A treatment cannot be inserted into a screen cell')

    def test_treatment_check__treatment_cell_00(self):
        self.assertTrue(self.cell._treatment_check([self.first_treatment]),
                         'A treatment can be inserted into a cell with a treatment')

    def test_treatment_check__treatment_cell_01(self):
        self.assertTrue(self.cell._treatment_check([self.first_treatment, self.second_treatment]),
                         'A treatment can be inserted into a cell with two treatment')

    def test_treatment_check__treatment_cell_02(self):
        self.assertTrue(self.cell._treatment_check([self.first_treatment, {self.second_treatment,
                                                                           self.third_treatment}]),
                         'A treatment can be inserted into a cell with a treatment and a concomitant treatment')

    def test_treatment_check__treatment_cell_02(self):
        self.assertTrue(self.cell._treatment_check([self.first_treatment,
                                                    self.washout, {
                                                        self.second_treatment,
                                                        self.third_treatment
                                                    }, self.washout]),
                         'A treatment can be inserted into a cell with a treatment a concomitant treatment and two'
                         'washouts')

    # _concomitant_treatment_check() tests
    def test_concomitant_treatments_check_00(self):
        self.assertTrue(self.cell._concomitant_treatments_check({self.first_treatment, self.second_treatment}),
                        'Concomitant treatment must have same duration (no semantic reasoning on units)')

    def test_concomitant_treatments_check_01(self):
        self.assertFalse(self.cell._concomitant_treatments_check({
            self.first_treatment,
            self.second_treatment,
            self.potential_concomitant_washout
        }), 'Concomitant elements must all be treatment')

    def test_concomitant_treatments_check_02(self):
        self.assertTrue(self.cell._concomitant_treatments_check({
            self.first_treatment,
            self.second_treatment,
            self.fourth_treatment
        }), 'Concomitant treatment must have same duration (no semantic reasoning on units)')

    def test_concomitant_treatments_check_03(self):
        self.assertFalse(self.cell._concomitant_treatments_check({
            self.first_treatment,
            self.second_treatment,
            self.third_treatment
        }), 'Concomitant treatment must have same duration (no semantic reasoning on units)')



    def test_insert_element_screen(self):
        self.assertEqual(self.cell.elements, list(), 'The initialized elements set is empty')
        self.cell.insert_element(self.screen)
        self.assertEqual(self.cell.elements, [self.screen])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.screen,
                          'A SCREEN cannot be added to a a cell with a SCREEN')
        self.assertEqual(self.cell.elements, [self.screen])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.first_treatment,
                               'A treatment cannot be added to a cell with a SCREEN')
        self.assertEqual(self.cell.elements, [self.screen])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.follow_up,
                          'A FOLLOW-UP cannot ba added to a cell with a SCREEN')
        self.assertEqual(self.cell.elements, [self.screen])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, {
            self.first_treatment, self.fourth_treatment
        }, 'A treatment set cannot be added to a cell with a SCREEN')
        self.cell.insert_element(self.run_in)
        self.assertEqual(self.cell.elements, [self.screen, self.run_in], 'A RUN-IN is inserted in the cell after the'
                                                                         'SCREEN')

    def test_insert_element_run_in(self):
        self.assertEqual(self.cell.elements, list(), 'The initialized elements set is empty')
        self.cell.insert_element(self.run_in)
        self.assertEqual(self.cell.elements, [self.run_in])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.screen,
                          'A SCREEN cannot be added to a a cell with a RUN-IN after the RUN-IN')
        self.assertEqual(self.cell.elements, [self.run_in])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.first_treatment,
                          'A treatment cannot be added to a cell with a RUN-IN')
        self.assertEqual(self.cell.elements, [self.run_in])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.follow_up,
                          'A FOLLOW-UP cannot ba added to a cell with a RUN-IN')
        self.assertEqual(self.cell.elements, [self.run_in])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, {
            self.first_treatment, self.fourth_treatment
        }, 'A treatment set cannot be added to a cell with a RUN-IN')
        self.cell.insert_element(self.screen, 0)
        self.assertEqual(self.cell.elements, [self.screen, self.run_in], 'A SCREEN is inserted in the cell before the'
                                                                         'RUN-IN')

    def test_insert_element_washout__00(self):
        self.assertEqual(self.cell.elements, list(), 'The initialized elements set is empty')
        self.cell.insert_element(self.washout)
        self.assertEqual(self.cell.elements, [self.washout])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.screen,
                          'A SCREEN cannot be added to a a cell with a WASHOUT')
        self.assertEqual(self.cell.elements, [self.washout])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.run_in,
                          'A RUN-IN cannot be added to a cell with a WASHOUT')
        self.assertEqual(self.cell.elements, [self.washout])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.follow_up,
                          'A FOLLOW-UP cannot ba added to a cell with a WASHOUT')
        self.assertEqual(self.cell.elements, [self.washout])
        self.cell.insert_element({self.first_treatment, self.fourth_treatment})
        self.assertEqual(self.cell.elements, [self.washout, {self.first_treatment, self.fourth_treatment}],
                         'A treatment set can be added to a cell with a WASHOUT')

    def test_insert_element_washout__01(self):
        self.assertEqual(self.cell.elements, list(), 'The initialized elements set is empty')
        self.cell.insert_element(self.washout)
        self.assertEqual(self.cell.elements, [self.washout])
        self.cell.insert_element(self.second_treatment)
        self.assertEqual(self.cell.elements, [self.washout, self.second_treatment],
                         'A treatment is added after the WASHOUT')
        self.cell.insert_element(self.first_treatment, 0)
        self.assertEqual(self.cell.elements, [self.first_treatment, self.washout, self.second_treatment],
                         'A treatment is added before the WASHOUT')

    def test_insert_element_follow_up(self):
        self.assertEqual(self.cell.elements, list(), 'The initialized elements set is empty')
        self.cell.insert_element(self.follow_up)
        self.assertEqual(self.cell.elements, [self.follow_up])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.screen,
                          'A SCREEN cannot be added to a a cell with a FOLLOW-UP')
        self.assertEqual(self.cell.elements, [self.follow_up])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.first_treatment,
                          'A treatment cannot be added to a cell with a FOLLOW-UP')
        self.assertEqual(self.cell.elements, [self.follow_up])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.follow_up,
                          'A FOLLOW-UP cannot ba added to a cell with a FOLLOW-UP')
        self.assertEqual(self.cell.elements, [self.follow_up])
        self.assertRaises(ISAModelValueError, self.cell.insert_element, {self.first_treatment, self.fourth_treatment},
                          'A treatment set cannot be added to a cell with a FOLLOW-UP')
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.run_in,
                          'A RUN-IN cannot be added to a cell with a FOLLOW-UP')

    def test_insert_element_treatment(self):
        self.assertEqual(self.cell.elements, list(), 'The initialized elements set is empty')
        self.cell.insert_element(self.first_treatment)
        self.assertEqual(self.cell.elements, [self.first_treatment])
        self.cell.insert_element(self.second_treatment)
        self.assertEqual(self.cell.elements, [self.first_treatment, self.second_treatment],
                         'A second treatment can be added to a cell with a treatment')
        self.cell.insert_element(self.washout, 1)
        self.assertEqual(self.cell.elements, [self.first_treatment, self.washout, self.second_treatment],
                         'A washout can be added to a cell with two treatments between them')
        self.cell.insert_element(self.washout, 0)
        self.assertEqual(self.cell.elements,
                         [self.washout, self.first_treatment, self.washout, self.second_treatment],
                         'A washout can be added to a cell with two treatments before them')
        self.cell.insert_element(self.washout)
        self.assertEqual(self.cell.elements,
                         [self.washout, self.first_treatment, self.washout, self.second_treatment, self.washout],
                         'A washout can be added to a cell with two treatments at the end')
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.washout,
                          'A washout cannot be added if there is one before the position where it is to be inserted')
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.washout, 0)
        self.assertTrue(True, 'A washout cannot be added if there is one after the position where it is to be inserted')
        self.cell.insert_element({self.first_treatment, self.second_treatment, self.fourth_treatment})
        self.assertEqual(self.cell.elements, [
            self.washout, self.first_treatment, self.washout, self.second_treatment, self.washout, {
                self.first_treatment,
                self.second_treatment,
                self.fourth_treatment
            }
        ], 'A treatment set can be added to a cell with two treatments and washout periods')

    def test_insert_element_concomitant_treatment(self):
        self.assertEqual(self.cell.elements, list(), 'The initialized elements set is empty')
        self.cell.insert_element({self.first_treatment, self.second_treatment})
        self.assertEqual(self.cell.elements, [{self.first_treatment, self.second_treatment}])
        self.cell.insert_element(self.second_treatment)
        self.assertEqual(self.cell.elements, [{self.first_treatment, self.second_treatment}, self.second_treatment],
                         'A second treatment can be added to a cell with a treatment set')
        self.cell.insert_element(self.washout, 1)
        self.assertEqual(self.cell.elements, [
            {self.first_treatment, self.second_treatment}, self.washout, self.second_treatment
        ], 'A washout can be added to a cell with a treatment set and a treatment, between them')
        self.cell.insert_element(self.washout, 0)
        self.assertEqual(self.cell.elements, [
            self.washout, {self.first_treatment, self.second_treatment}, self.washout, self.second_treatment
        ], 'A washout can be added to a cell with a treatment set and a treatment, before them')
        self.cell.insert_element(self.washout)
        self.assertEqual(self.cell.elements, [
            self.washout, {self.first_treatment, self.second_treatment}, self.washout, self.second_treatment,
            self.washout], 'A washout can be added to a cell with a treatment set and a treatment, at the end')
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.washout,
                          'A washout cannot be added if there is one before the position where it is to be inserted')
        self.assertRaises(ISAModelValueError, self.cell.insert_element, self.washout, 0)
        self.assertTrue(True, 'A washout cannot be added if there is one after the position where it is to be inserted')

    def test_contains_non_treatment_by_type_empty_cell(self):
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(SCREEN), False, 'An empty cell contains no SCREEN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(RUN_IN), False, 'An empty cell contains no RUN-IN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(WASHOUT), False, 'An empty cell contains no WASHOUT')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(FOLLOW_UP), False,
                                                                  'An empty cell contains no FOLLOW_UP')

    def test_contains_non_treatment_by_type_screen_cell(self):
        self.cell.elements = [self.screen]
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(SCREEN), True,
                         'A SCREEN cell contains a SCREEN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(RUN_IN), False,
                         'A SCREEN cell contains no RUN-IN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(WASHOUT), False,
                         'A SCREEN cell contains no WASHOUT')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(FOLLOW_UP), False,
                         'A SCREEN cell contains no FOLLOW_UP')

    def test_contains_non_treatment_by_type_run_in_cell(self):
        self.cell.elements = [self.run_in]
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(SCREEN), False,
                         'A RUN-IN cell contains no SCREEN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(RUN_IN), True,
                         'A RUN-IN cell contains a RUN-IN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(WASHOUT), False,
                         'A RUN-IN cell contains no WASHOUT')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(FOLLOW_UP), False,
                         'A RUN-IN cell contains no FOLLOW_UP')

    def test_contains_non_treatment_by_type_washout_cell(self):
        self.cell.elements = [self.washout]
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(SCREEN), False, 'A WASHOUT cell contains no SCREEN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(RUN_IN), False, 'A WASHOUT cell contains no RUN-IN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(WASHOUT), True, 'A WASHOUT cell contains a WASHOUT')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(FOLLOW_UP), False,
                         'A WASHOUT cell contains no FOLLOW_UP')

    def test_contains_non_treatment_by_type_follow_up_cell(self):
        self.cell.elements = [self.follow_up]
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(SCREEN), False, 'A FOLLOW-UP cell contains no SCREEN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(RUN_IN), False, 'A FOLLOW-UP cell contains no RUN-IN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(WASHOUT), False, 'A FOLLOW-UP cell contains a WASHOUT')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(FOLLOW_UP), True, 'A FOLLOW-UP cell contains no FOLLOW_UP')

    def test_contains_non_treatment_by_type_single_treatment_cell(self):
        self.cell.elements = [self.first_treatment]
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(SCREEN), False,
                         'A single treatment cell contains no SCREEN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(RUN_IN), False,
                         'A single treatment cell contains no RUN-IN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(WASHOUT), False,
                         'A single treatment cell contains a WASHOUT')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(FOLLOW_UP), False,
                         'A single treatment cell contains no FOLLOW_UP')

    def test_contains_non_treatment_by_type_multi_treatment_cell(self):
        self.cell.elements = [self.first_treatment, self.washout, {self.second_treatment, self.fourth_treatment},
                              self.washout]
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(SCREEN), False,
                         'This multi-treatment cell contains no SCREEN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(RUN_IN), False,
                         'This multi-treatment cell contains no RUN-IN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(WASHOUT), True,
                         'This multi-treatment cell contains two WASHOUT elements')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(FOLLOW_UP), False,
                         'This multi-treatment cell contains no FOLLOW_UP')

    def test_get_all_elements_00(self):
        self.cell.elements = [self.first_treatment, self.washout, self.second_treatment, self.fourth_treatment,
                              self.washout]
        self.assertEqual(self.cell.get_all_elements(), [self.first_treatment, self.washout, self.second_treatment,
                                                        self.fourth_treatment, self.washout])

    def test_get_all_elements_01(self):
        self.cell.elements = [self.first_treatment, self.washout, {self.second_treatment, self.fourth_treatment},
                              self.washout]
        self.assertEqual(set(self.cell.get_all_elements()), {self.first_treatment, self.washout,
                                                             self.second_treatment, self.fourth_treatment})

    def test_get_all_elements_02(self):
        self.cell.elements = [self.follow_up]
        self.assertEqual(self.cell.get_all_elements(), [self.follow_up])

class StudyArmTest(unittest.TestCase):

    def setUp(self):
        self.arm = StudyArm(name=TEST_STUDY_ARM_NAME_00, group_size=10)
        self.first_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))
        self.second_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE_ALT),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))
        self.third_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE_ALT),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE_ALT, unit=FACTORS_2_UNIT)
        ))
        self.fourth_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE_THIRD),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))
        self.screen = NonTreatment(element_type=SCREEN,
                                   duration_value=SCREEN_DURATION_VALUE, duration_unit=DURATION_UNIT)
        self.run_in = NonTreatment(element_type=RUN_IN,
                                    duration_value=WASHOUT_DURATION_VALUE, duration_unit=DURATION_UNIT)
        self.washout = NonTreatment(element_type=WASHOUT,
                                    duration_value=WASHOUT_DURATION_VALUE, duration_unit=DURATION_UNIT)
        self.follow_up = NonTreatment(element_type=FOLLOW_UP,
                                      duration_value=FOLLOW_UP_DURATION_VALUE, duration_unit=DURATION_UNIT)
        self.potential_concomitant_washout = NonTreatment(element_type=WASHOUT, duration_value=FACTORS_2_VALUE,
                                                          duration_unit=FACTORS_2_UNIT)
        self.cell_screen = StudyCell(SCREEN, elements=(self.screen,))
        self.cell_run_in = StudyCell(RUN_IN, elements=(self.run_in,))
        self.cell_other_run_in = StudyCell('OTHER RUN-IN', elements=(self.run_in,))
        self.cell_screen_and_run_in = StudyCell('SCREEN AND RUN-IN', elements=[self.screen, self.run_in])
        self.cell_concomitant_treatments = StudyCell('CONCOMITANT TREATMENTS',
                                                     elements=([{self.second_treatment, self.fourth_treatment}]))
        self.cell_washout_00 = StudyCell(WASHOUT, elements=(self.washout,))
        self.cell_washout_01 = StudyCell('ANOTHER WASHOUT', elements=(self.washout))
        self.cell_single_treatment_00 = StudyCell('SINGLE TREATMENT', elements=[self.first_treatment])
        self.cell_single_treatment_01 = StudyCell('SINGLE TREATMENT', elements=[self.second_treatment])
        self.cell_single_treatment_02 = StudyCell('SINGLE TREATMENT', elements=[self.third_treatment])
        self.cell_multi_elements = StudyCell('MULTI ELEMENTS',
                                             elements=[{self.first_treatment, self.second_treatment,
                                                        self.fourth_treatment}, self.washout, self.second_treatment])
        self.cell_multi_elements_padded = StudyCell('MULTI ELEMENTS PADDED',
                                                    elements=[self.first_treatment, self.washout, {
                                                        self.second_treatment,
                                                        self.fourth_treatment
                                                    }, self.washout, self.third_treatment, self.washout])
        self.cell_follow_up = StudyCell(FOLLOW_UP, elements=(self.follow_up,))
        self.sample_assay_plan = SampleAssayPlan()

    def test__init__(self):
        self.assertEqual(self.arm.name, TEST_STUDY_ARM_NAME_00)

    def test_add_item_to_arm__single_unit_cells_00(self):
        self.arm.add_item_to_arm_map(self.cell_screen, None)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 1, 'One mapping has been added to the arm')
        self.assertEqual(cells[0], self.cell_screen, 'The SCREEN cell has been added to the arm')
        self.assertEqual(plans[0], None, 'There is non sample plan for this specific cell')
        with self.assertRaises(ISAModelValueError, msg='Another cell containing a screen cannot be added to the '
                                                       'StudyArm') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_screen_and_run_in, None)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.SCREEN_ERROR_MESSAGE)
        self.arm.add_item_to_arm_map(self.cell_run_in, None)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 2, 'One mapping has been added to the arm')
        self.assertEqual(cells[1], self.cell_run_in, 'The RUN-IN cell has been added to the arm')
        self.assertEqual(plans[1], None, 'There is non sample plan for this specific cell')

        with self.assertRaises(ISAModelValueError, msg='Another cell containing a screen cannot be added to the '
                                                       'StudyArm') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_screen_and_run_in, None)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.SCREEN_ERROR_MESSAGE)

        with self.assertRaises(ISAModelValueError, msg='Another cell containing a run-in cannot be added to the '
                                                       'StudyArm') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_other_run_in, None)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.RUN_IN_ERROR_MESSAGE)

        self.arm.add_item_to_arm_map(self.cell_single_treatment_00, self.sample_assay_plan)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 3, 'One mapping has been added to the arm')
        self.assertEqual(cells[2], self.cell_single_treatment_00, 'The 1st treatment cell has been added to the arm')
        self.assertEqual(plans[2], self.sample_assay_plan, 'There is non sample plan for this specific cell')

        with self.assertRaises(ISAModelValueError, msg='Another cell containing a screen cannot be added to the '
                                                       'StudyArm') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_screen_and_run_in, None)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.SCREEN_ERROR_MESSAGE)

        with self.assertRaises(ISAModelValueError, msg='Another cell containing a run-in cannot be added to the '
                                                       'StudyArm') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_other_run_in, None)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.RUN_IN_ERROR_MESSAGE)

        self.arm.add_item_to_arm_map(self.cell_washout_00, None)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 4, 'One mapping has been added to the arm')
        self.assertEqual(cells[3], self.cell_washout_00, 'The WASHOUT cell has been added to the arm')
        self.assertEqual(plans[3], None, 'There is non sample plan for this specific cell')

        with self.assertRaises(ISAModelValueError, msg='Another cell containing a WASHOUT cannot be added to the '
                                                       'StudyArm') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_washout_01, None)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.WASHOUT_ERROR_MESSAGE)

        self.arm.add_item_to_arm_map(self.cell_single_treatment_02, self.sample_assay_plan)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 5, 'One mapping has been added to the arm')
        self.assertEqual(cells[4], self.cell_single_treatment_02, 'The 3rd treatment cell has been added to the arm')
        self.assertEqual(plans[4], self.sample_assay_plan, 'There is non sample plan for this specific cell')
        self.arm.add_item_to_arm_map(self.cell_washout_01, None)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 6, 'One mapping has been added to the arm')
        self.assertEqual(cells[5], self.cell_washout_01, 'The WASHOUT cell has been added to the arm')
        self.assertEqual(plans[5], None, 'There is non sample plan for this specific cell')
        self.arm.add_item_to_arm_map(self.cell_concomitant_treatments, self.sample_assay_plan)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 7, 'One mapping has been added to the arm')
        self.assertEqual(cells[6], self.cell_concomitant_treatments, 'The concomitant treatments cell '
                                                                     'has been added to the arm')
        self.assertEqual(plans[6], self.sample_assay_plan, 'There is non sample plan for this specific cell')
        self.arm.add_item_to_arm_map(self.cell_follow_up, self.sample_assay_plan)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 8, 'One mapping has been added to the arm')
        self.assertEqual(cells[7], self.cell_follow_up, 'The FOLLOW-UP cell has been added to the arm')
        self.assertEqual(plans[7], self.sample_assay_plan, 'There is non sample plan for this specific cell')

        with self.assertRaises(ISAModelValueError, msg='No more items can be added after a FOLLOW-UP') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_multi_elements, self.sample_assay_plan)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.COMPLETE_ARM_ERROR_MESSAGE)

    def test_add_item_to_arm__multi_unit_cells_00(self):
        self.arm.add_item_to_arm_map(self.cell_screen_and_run_in, None)
        with self.assertRaises(ISAModelValueError, msg='A cell beginning with a WASHOUT element cannot be added to a'
                                                       'an ARM ending with a RUN-IN') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_washout_00, self.sample_assay_plan)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.WASHOUT_ERROR_MESSAGE)
        self.arm.add_item_to_arm_map(self.cell_multi_elements, self.sample_assay_plan)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 2, 'One mapping has been added to the arm')
        self.assertEqual(cells[1], self.cell_multi_elements, 'The multi-step treatment cell has been added to the arm')
        self.assertEqual(plans[1], self.sample_assay_plan, 'There is a sample plan for this specific cell')
        self.arm.add_item_to_arm_map(self.cell_follow_up, self.sample_assay_plan)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 3, 'One mapping has been added to the arm')
        self.assertEqual(cells[2], self.cell_follow_up, 'The FOLLOW-UP cell has been added to the arm')
        self.assertEqual(plans[2], self.sample_assay_plan, 'There is a sample plan for this specific cell')

    def test_add_item_to_arm__multi_unit_cells_01(self):
        self.arm.add_item_to_arm_map(self.cell_screen, None)
        with self.assertRaises(ISAModelValueError, msg='A cell beginning with a FOLLOW-UP element cannot be added to a'
                                                       'an ARM ending with a SCREEN') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_follow_up, None)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.FOLLOW_UP_ERROR_MESSAGE)
        self.arm.add_item_to_arm_map(self.cell_multi_elements_padded, self.sample_assay_plan)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 2, 'One mapping has been added to the arm')
        self.assertEqual(cells[1], self.cell_multi_elements_padded, 'The multi-step treatment cell has been added to '
                                                                    'the arm')
        self.assertEqual(plans[1], self.sample_assay_plan, 'There is a sample plan for this specific cell')
        self.arm.add_item_to_arm_map(self.cell_follow_up, self.sample_assay_plan)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 3, 'One mapping has been added to the arm')
        self.assertEqual(cells[2], self.cell_follow_up, 'The FOLLOW-UP cell has been added to the arm')
        self.assertEqual(plans[2], self.sample_assay_plan, 'There is a sample plan for this specific cell')

    def test_add_item_to_arm__follow_up_to_empty_cell(self):
        with self.assertRaises(ISAModelValueError, msg='A cell beginning with a FOLLOW-UP element cannot be added to '
                                                       'an empty arm.') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_follow_up, self.sample_assay_plan)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.FOLLOW_UP_EMPTY_ARM_ERROR_MESSAGE)

    def test_group_size_property(self):
        self.assertEqual(self.arm.group_size, 10)
        self.arm.group_size = 100
        self.assertEqual(self.arm.group_size, 100)

    def test_group_size_property_fail_00(self):
        with self.assertRaises(ISAModelAttributeError,
                               msg='Only positive integers can be assinged to group_size') as ex_cm:
            self.arm.group_size = -5
        self.assertEqual(ex_cm.exception.args[0], 'group_size must be a positive integer; -5 provided')

    def test_arm_map_property_success_00(self):
        self.assertEqual(self.arm.arm_map, OrderedDict(), 'The ordered mapping StudyCell -> SampleAssayPlan is empty.')
        ord_dict = OrderedDict([(self.cell_screen, None), (self.cell_run_in, None),
                                (self.cell_single_treatment_00, self.sample_assay_plan),
                                (self.cell_washout_00, None),
                                (self.cell_single_treatment_01, self.sample_assay_plan),
                                (self.cell_washout_01, None), (self.cell_follow_up, self.sample_assay_plan)
                                ])
        self.arm.arm_map = ord_dict
        self.assertEqual(self.arm.arm_map, ord_dict, 'The ordered mapping StudyCell -> SampleAssayPlan has been '
                                                     'correctly set for single-treatment cells.')
    def test_arm_map_property_success_01(self):
        self.assertEqual(self.arm.arm_map, OrderedDict(), 'The ordered mapping StudyCell -> SampleAssayPlan is empty.')
        ord_dict = OrderedDict([(self.cell_screen, None),
                                (self.cell_multi_elements_padded, self.sample_assay_plan),
                                (self.cell_follow_up, self.sample_assay_plan)
                                ])
        self.arm.arm_map = ord_dict
        self.assertEqual(self.arm.arm_map, ord_dict, 'The ordered mapping StudyCell -> SampleAssayPlan has been '
                                                     'correctly set for single-treatment cells.')

    def test_arm_map_property_fail_wrong_type(self):
        with self.assertRaises(ISAModelAttributeError, msg='An error is raised if an object of the wrong type is '
                                                           'provided to the assignment.') as ex_cm:
            self.arm.arm_map = ['wrong', 'object']
        self.assertEqual(ex_cm.exception.args[0], StudyArm.ARM_MAP_ASSIGNMENT_ERROR)

    def test_arm_map_property_fail_wrong_value_00(self):
        with self.assertRaises(ISAModelAttributeError, msg='An error is raised if an object of the wrong value is '
                                                           'provided to the assignment.') as ex_cm:
            ord_dict = OrderedDict([(self.cell_screen, None), (self.cell_run_in, None),
                                (self.cell_single_treatment_00, self.sample_assay_plan),
                                (self.cell_washout_00, None),
                                (self.cell_single_treatment_01, self.sample_assay_plan),
                                (self.cell_follow_up, self.sample_assay_plan),
                                (self.cell_washout_01, None)
                                ])
            self.arm.arm_map = ord_dict
        self.assertEqual(ex_cm.exception.args[0], StudyArm.COMPLETE_ARM_ERROR_MESSAGE)

    def test_arm_map_property_fail_wrong_value_01(self):
        with self.assertRaises(ISAModelAttributeError, msg='An error is raised if an object of the wrong value is '
                                                           'provided to the assignment.') as ex_cm:
            ord_dict = OrderedDict([(self.cell_screen, None), (self.cell_run_in, None),
                                (self.cell_single_treatment_00, self.sample_assay_plan),
                                (self.cell_single_treatment_01, self.sample_assay_plan),
                                (self.cell_washout_00, None),
                                (self.cell_washout_01, None),
                                (self.cell_follow_up, self.sample_assay_plan)
                                ])
            self.arm.arm_map = ord_dict
        self.assertEqual(ex_cm.exception.args[0], StudyArm.WASHOUT_ERROR_MESSAGE)

    def test_treatments_property(self):
        self.arm.arm_map = OrderedDict([(self.cell_screen, None),
                                        (self.cell_multi_elements_padded, self.sample_assay_plan),
                                        (self.cell_follow_up, self.sample_assay_plan)])
        self.assertEqual(self.arm.treatments, {
            self.first_treatment, self.second_treatment, self.fourth_treatment, self.third_treatment
        })


class StudyDesignTest(unittest.TestCase):

    def setUp(self):

        self.first_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))
        self.second_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE_ALT),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))
        self.third_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE_ALT),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE_ALT, unit=FACTORS_2_UNIT)
        ))
        self.fourth_treatment = Treatment(factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE_THIRD),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        ))
        self.screen = NonTreatment(element_type=SCREEN,
                                   duration_value=SCREEN_DURATION_VALUE, duration_unit=DURATION_UNIT)
        self.run_in = NonTreatment(element_type=RUN_IN,
                                    duration_value=WASHOUT_DURATION_VALUE, duration_unit=DURATION_UNIT)
        self.washout = NonTreatment(element_type=WASHOUT,
                                    duration_value=WASHOUT_DURATION_VALUE, duration_unit=DURATION_UNIT)
        self.follow_up = NonTreatment(element_type=FOLLOW_UP,
                                      duration_value=FOLLOW_UP_DURATION_VALUE, duration_unit=DURATION_UNIT)
        self.potential_concomitant_washout = NonTreatment(element_type=WASHOUT, duration_value=FACTORS_2_VALUE,
                                                          duration_unit=FACTORS_2_UNIT)
        self.cell_screen = StudyCell(SCREEN, elements=(self.screen,))
        self.cell_run_in = StudyCell(RUN_IN, elements=(self.run_in,))
        self.cell_other_run_in = StudyCell('OTHER RUN-IN', elements=(self.run_in,))
        self.cell_screen_and_run_in = StudyCell('SCREEN AND RUN-IN', elements=[self.screen, self.run_in])
        self.cell_concomitant_treatments = StudyCell('CONCOMITANT TREATMENTS',
                                                     elements=([{self.second_treatment, self.fourth_treatment}]))
        self.cell_washout_00 = StudyCell(WASHOUT, elements=(self.washout,))
        self.cell_washout_01 = StudyCell('ANOTHER WASHOUT', elements=(self.washout))
        self.cell_single_treatment_00 = StudyCell('SINGLE TREATMENT', elements=[self.first_treatment])
        self.cell_single_treatment_01 = StudyCell('SINGLE TREATMENT', elements=[self.second_treatment])
        self.cell_single_treatment_02 = StudyCell('SINGLE TREATMENT', elements=[self.third_treatment])
        self.cell_multi_elements = StudyCell('MULTI ELEMENTS',
                                             elements=[{self.first_treatment, self.second_treatment,
                                                        self.fourth_treatment}, self.washout, self.second_treatment])
        self.cell_multi_elements_padded = StudyCell('MULTI ELEMENTS PADDED',
                                                    elements=[self.first_treatment, self.washout, {
                                                        self.second_treatment,
                                                        self.fourth_treatment
                                                    }, self.washout, self.third_treatment, self.washout])
        self.cell_follow_up = StudyCell(FOLLOW_UP, elements=(self.follow_up,))
        self.sample_assay_plan = SampleAssayPlan()
        self.first_arm = StudyArm(name=TEST_STUDY_ARM_NAME_00, group_size=10, arm_map=OrderedDict([
            (self.cell_screen, None), (self.cell_run_in, None), (self.cell_single_treatment_00, self.sample_assay_plan),
            (self.cell_follow_up, self.sample_assay_plan)
        ]))
        self.second_arm = StudyArm(name=TEST_STUDY_ARM_NAME_01, group_size=25, arm_map=OrderedDict([
            (self.cell_screen, None), (self.cell_run_in, None), (self.cell_multi_elements, self.sample_assay_plan),
            (self.cell_follow_up, self.sample_assay_plan)
        ]))
        self.third_arm = StudyArm(name=TEST_STUDY_ARM_NAME_02, group_size=20, arm_map=OrderedDict([
            (self.cell_screen, None), (self.cell_run_in, None),
            (self.cell_multi_elements_padded, self.sample_assay_plan),
            (self.cell_follow_up, self.sample_assay_plan)
        ]))
        self.arm_same_name_as_third = StudyArm(name=TEST_STUDY_ARM_NAME_02, group_size=10, arm_map=OrderedDict([
            (self.cell_screen, None), (self.cell_run_in, None), (self.cell_single_treatment_01, self.sample_assay_plan),
            (self.cell_follow_up, self.sample_assay_plan)
        ]))
        self.study_design = StudyDesign()

    def test_init(self):
        self.assertIsInstance(getattr(self.study_design, '_StudyDesign__name', None), str,
                              'The __name has been initialized as a string')
        self.assertEqual(getattr(self.study_design, '_StudyDesign__study_arms', None), set(),
                         'An empty set has been initialized for __study_arms')

    def test_name_property(self):
        self.assertEqual(self.study_design.name, 'Study Design')
        self.study_design.name = TEST_STUDY_DESIGN_NAME
        self.assertEqual(self.study_design.name, TEST_STUDY_DESIGN_NAME)
        with self.assertRaises(ISAModelAttributeError, msg='An integer cannot be assigned as StudyDesign name') as ex_cm:
            self.study_design.name = 128
        self.assertEqual(ex_cm.exception.args[0], StudyDesign.NAME_PROPERTY_ASSIGNMENT_ERROR)

    def test_study_arms_property(self):
        pass

    def test_add_study_arm_00(self):
        self.study_design.add_study_arm(self.first_arm)
        self.assertIn(self.first_arm, self.study_design.study_arms, 'The Study Arm has been correctly added to the '
                                                                    'StudyDesign')

    def test_add_study_arm_01(self):
        self.study_design.add_study_arm(self.third_arm)
        self.assertIn(self.third_arm, self.study_design.study_arms, 'The Study Arm has been correctly added to the '
                                                                    'StudyDesign')
        self.study_design.add_study_arm(self.second_arm)
        self.assertIn(self.second_arm, self.study_design.study_arms, 'The Study Arm has been correctly added to the '
                                                                    'StudyDesign')
        with self.assertRaises(ISAModelValueError,
                               msg='An integer cannot be assigned as StudyDesign name') as ex_cm:
            self.study_design.add_study_arm(self.arm_same_name_as_third)
        self.assertEqual(ex_cm.exception.args[0], StudyDesign.ADD_STUDY_ARM_NAME_ALREADY_PRESENT_ERROR)
        self.assertEqual(self.study_design.study_arms, [self.second_arm, self.third_arm])
        self.study_design.add_study_arm(self.first_arm)
        self.assertEqual(self.study_design.study_arms, [self.second_arm, self.first_arm, self.third_arm])

    def test_add_study_arm_02(self):
        with self.assertRaises(ISAModelTypeError,
                               msg='A Treatment cannot be added to a StudyDesign, only StudyArms') as ex_cm:
            self.study_design.add_study_arm(self.second_treatment)
        self.assertIn(StudyDesign.ADD_STUDY_ARM_PARAMETER_TYPE_ERROR, ex_cm.exception.args[0])

    def test_treatments_property(self):
        pass


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


if __name__ == '__main__':
    # Run only the tests in the specified classes

    test_classes_to_run = [NonTreatmentTest, TreatmentTest, StudyCellTest]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)