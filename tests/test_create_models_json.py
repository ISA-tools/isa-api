"""Tests on serializing planning objects in isatools.create.models to JSON"""
import json
import os
import unittest
from io import StringIO

from isatools.create.models import *
from isatools.tests import utils


def ordered(o):  # to enable comparison of JSONs with lists using ==
    if isinstance(o, dict):
        return sorted((k, ordered(v)) for k, v in o.items())
    if isinstance(o, list):
        return sorted(ordered(x) for x in o if x is not None)
    else:
        return o

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

TEST_STUDY_ARM_NAME_00 = 'first arm'
TEST_STUDY_ARM_NAME_01 = 'second arm'
TEST_STUDY_ARM_NAME_02 = 'third arm'

TEST_STUDY_DESIGN_NAME = 'test study design'
TEST_STUDY_DESIGN_NAME_THREE_ARMS = 'TEST STUDY DESIGN WITH THREE ARMS'
TEST_STUDY_DESIGN_NAME_TWO_ARMS_MULTI_ELEMENT_CELLS = 'TEST STUDY DESIGN WITH TWO ARMS (MULTI-ELEMENT CELLS)'

TEST_EPOCH_0_RANK = 0

SCREEN_DURATION_VALUE = 100
FOLLOW_UP_DURATION_VALUE = 5 * 366
WASHOUT_DURATION_VALUE = 30
DURATION_UNIT = OntologyAnnotation(term='day')

DIETARY_FACTOR_0_VALUE = 'Vitamin A'
DIETARY_FACTOR_1_VALUE = 30.0
DIETARY_FACTOR_1_UNIT = OntologyAnnotation(term='mg')
DIETARY_FACTOR_2_VALUE = 50
DIETARY_FACTOR_2_UNIT = OntologyAnnotation(term='day')

RADIOLOGICAL_FACTOR_0_VALUE = 'Gamma ray'
RADIOLOGICAL_FACTOR_1_VALUE = 12e-3
RADIOLOGICAL_FACTOR_1_UNIT = OntologyAnnotation(term='Gy')
RADIOLOGICAL_FACTOR_2_VALUE = 5
RADIOLOGICAL_FACTOR_2_UNIT = OntologyAnnotation(term='hour')

BIOLOGICAL_FACTOR_0_VALUE = 'Anthrax'
BIOLOGICAL_FACTOR_1_VALUE = 12e-3
BIOLOGICAL_FACTOR_1_UNIT = OntologyAnnotation(term='mg')
BIOLOGICAL_FACTOR_2_VALUE = 7
BIOLOGICAL_FACTOR_2_UNIT = OntologyAnnotation(term='day')


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
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
        self.fifth_treatment = Treatment(element_type=INTERVENTIONS['DIET'], factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=DIETARY_FACTOR_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS[1], value=DIETARY_FACTOR_1_VALUE, unit=DIETARY_FACTOR_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=DIETARY_FACTOR_2_VALUE, unit=DIETARY_FACTOR_2_UNIT)
        ))
        self.sixth_treatment = Treatment(element_type=INTERVENTIONS['RADIOLOGICAL'], factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=RADIOLOGICAL_FACTOR_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS[1], value=RADIOLOGICAL_FACTOR_1_VALUE,
                        unit=RADIOLOGICAL_FACTOR_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=RADIOLOGICAL_FACTOR_2_VALUE,
                        unit=RADIOLOGICAL_FACTOR_2_UNIT)
        ))
        self.seventh_treatment = Treatment(element_type=INTERVENTIONS['BIOLOGICAL'], factor_values=(
            FactorValue(factor_name=BASE_FACTORS[0], value=BIOLOGICAL_FACTOR_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS[1], value=BIOLOGICAL_FACTOR_1_VALUE, unit=BIOLOGICAL_FACTOR_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=BIOLOGICAL_FACTOR_2_VALUE, unit=BIOLOGICAL_FACTOR_2_UNIT)
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
        self.cell_screen = StudyCell('SCREEN CELL', elements=(self.screen,))
        self.cell_run_in = StudyCell('RUN-IN CELL', elements=(self.run_in,))
        self.cell_single_treatment_00 = StudyCell('SINGLE-TREATMENT CELL', elements=[self.first_treatment])
        self.cell_single_treatment_01 = StudyCell('ANOTHER SINGLE-TREATMENT CELL', elements=[self.second_treatment])
        self.cell_single_treatment_02 = StudyCell('YET ANOTHER SINGLE-TREATMENT CELL', elements=[self.third_treatment])
        self.cell_single_treatment_diet = StudyCell('DIET CELL', elements=[self.fifth_treatment])
        self.cell_single_treatment_radiological = StudyCell('RADIOLOGICAL CELL', elements=[self.sixth_treatment])
        self.cell_single_treatment_biological = StudyCell('BIOLOGICAL CELL', elements=[self.seventh_treatment])
        self.cell_multi_elements = StudyCell('MULTI-ELEMENT CELL',
                                             elements=[{self.first_treatment, self.second_treatment,
                                                        self.fourth_treatment}, self.washout, self.second_treatment])
        self.cell_multi_elements_padded = StudyCell('PADDED MULTI-ELEMENT CELL',
                                                    elements=[self.first_treatment, self.washout, {
                                                        self.second_treatment,
                                                        self.fourth_treatment
                                                    }, self.washout, self.third_treatment, self.washout])
        self.cell_multi_elements_bio_diet = StudyCell('MULTI-ELEMENT CELL BIO-DIET',
                                                     elements=[{
                                                           self.second_treatment,
                                                           self.fourth_treatment,
                                                           self.first_treatment
                                                       }, self.washout, self.fifth_treatment, self.washout,
                                                           self.seventh_treatment])
        self.cell_follow_up = StudyCell('FOLLOW-UP CELL', elements=(self.follow_up,))
        self.cell_washout_00 = StudyCell('WASHOUT CELL', elements=(self.washout,))
        self.cell_washout_01 = StudyCell('ANOTHER WASHOUT', elements=[self.washout])
        self.sample_assay_plan_for_screening = SampleAssayPlan(name='SAMPLE ASSAY PLAN FOR SCREENING')
        self.sample_assay_plan_for_treatments = SampleAssayPlan(name='SAMPLE ASSAY PLAN FOR TREATMENTS')
        self.sample_assay_plan_for_washout = SampleAssayPlan(name='SAMPLE ASSAY PLAN FOR WASHOUT')
        self.sample_assay_plan_for_follow_up = SampleAssayPlan(name='FOLLOW-UP SAMPLE ASSAY PLAN')
        self.single_treatment_cell_arm = StudyArm(name=TEST_STUDY_ARM_NAME_00, group_size=10, arm_map=OrderedDict([
            [self.cell_screen, None], [self.cell_run_in, None],
            [self.cell_single_treatment_00, self.sample_assay_plan_for_treatments],
            [self.cell_washout_00, self.sample_assay_plan_for_washout],
            [self.cell_single_treatment_01, self.sample_assay_plan_for_treatments],
            [self.cell_follow_up, self.sample_assay_plan_for_follow_up]
        ]))
        self.single_treatment_cell_arm_01 = StudyArm(name=TEST_STUDY_ARM_NAME_01, group_size=30, arm_map=OrderedDict([
            [self.cell_screen, None], [self.cell_run_in, None],
            [self.cell_single_treatment_00, self.sample_assay_plan_for_treatments],
            [self.cell_washout_00, self.sample_assay_plan_for_washout],
            [self.cell_single_treatment_biological, self.sample_assay_plan_for_treatments],
            [self.cell_follow_up, self.sample_assay_plan_for_follow_up]
        ]))
        self.single_treatment_cell_arm_02 = StudyArm(name=TEST_STUDY_ARM_NAME_02, group_size=24, arm_map=OrderedDict([
            [self.cell_screen, None], [self.cell_run_in, None],
            [self.cell_single_treatment_diet, self.sample_assay_plan_for_treatments],
            [self.cell_washout_00, self.sample_assay_plan_for_washout],
            [self.cell_single_treatment_radiological, self.sample_assay_plan_for_treatments],
            [self.cell_follow_up, self.sample_assay_plan_for_follow_up]
        ]))
        self.multi_treatment_cell_arm = StudyArm(name=TEST_STUDY_ARM_NAME_00, group_size=35, arm_map=OrderedDict([
            [self.cell_screen, self.sample_assay_plan_for_screening],
            [self.cell_multi_elements_padded, self.sample_assay_plan_for_treatments],
            [self.cell_follow_up, self.sample_assay_plan_for_follow_up]
        ]))
        self.multi_treatment_cell_arm_01 = StudyArm(name=TEST_STUDY_ARM_NAME_01, group_size=5, arm_map=OrderedDict([
            [self.cell_screen, self.sample_assay_plan_for_screening],
            [self.cell_multi_elements_bio_diet, self.sample_assay_plan_for_treatments],
            [self.cell_follow_up, self.sample_assay_plan_for_follow_up]
        ]))


class StudyCellEncoderTest(BaseTestCase):

    def setUp(self):
        return super(StudyCellEncoderTest, self).setUp()

    def test_encode_single_treatment_cell(self):
        actual_json_cell = json.loads(json.dumps(self.cell_single_treatment_00, cls=StudyCellEncoder))
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'single-treatment-cell.json')) as expected_json_fp:
            expected_json_cell = json.load(expected_json_fp)
        self.assertEqual(ordered(actual_json_cell), ordered(expected_json_cell))

    def test_encode_multi_treatment_cell(self):
        self.maxDiff = None
        json_cell = json.loads(json.dumps(self.cell_multi_elements_padded, cls=StudyCellEncoder))
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'multi-treatment-padded-cell.json')) as expected_json_fp:
            expected_json_cell = json.load(expected_json_fp)
        self.assertEqual(ordered(json_cell), ordered(expected_json_cell))


class StudyCellDecoderTest(BaseTestCase):

    def setUp(self):
        return super(StudyCellDecoderTest, self).setUp()

    def test_decode_single_treatment_cell(self):
        decoder = StudyCellDecoder()
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'single-treatment-cell.json')) as expected_json_fp:
            json_text = json.dumps(json.load(expected_json_fp))
            actual_cell = decoder.loads(json_text)
        # print(self.cell_single_treatment)
        # print('\n')
        # print(actual_cell)
        # self.assertEqual(self.cell_single_treatment.elements[0], actual_cell.elements[0])
        self.assertEqual(self.cell_single_treatment_00, actual_cell)

    def test_decode_multi_treatment_cell(self):
        decoder = StudyCellDecoder()
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'multi-treatment-padded-cell.json')) as expected_json_fp:
            json_text = json.dumps(json.load(expected_json_fp))
            actual_cell = decoder.loads(json_text)
        self.assertEqual(len(self.cell_multi_elements_padded.elements), len(actual_cell.elements))
        for i in range(len(actual_cell.elements)):
            print(i)
            print(actual_cell.elements[i])
            print(self.cell_multi_elements_padded.elements[i])
            self.assertEqual(self.cell_multi_elements_padded.elements[i], actual_cell.elements[i])
        self.assertEqual(self.cell_multi_elements_padded, actual_cell)


class SampleAndAssayPlanEncoderAndDecoderTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.plan = SampleAndAssayPlan()
        self.first_assay_graph = AssayGraph(id_="assay-graph/00")
        self.second_assay_graph = AssayGraph(id_="assay-graph/01")
        self.tissue_char = Characteristic(category='organism part', value='tissue')
        self.blood_char = Characteristic(category='organism part', value='blood')
        self.tissue_node = ProductNode(id_='product-node/0000', name='tissue', node_type=SAMPLE, size=2, characteristics=[self.tissue_char])
        self.blood_node = ProductNode(id_='product-node/0001', name='blood',
                                      node_type=SAMPLE, size=3, characteristics=[self.blood_char])
        self.dna_char = Characteristic(category='nucleic acid', value='DNA')
        self.mirna_char = Characteristic(category='nucleic acid', value='miRNA')
        self.mrna_char = Characteristic(category='nucleic acid', value='mRNA')
        self.extraction_instrument = ParameterValue(category=ProtocolParameter(parameter_name='instrument'),
                                                    value='Maxwell RSC 48')
        self.protocol_node_dna = ProtocolNode(id_='protocol-node/0000', name='DNA extraction', version="1.0.0",
                                              parameter_values=[self.extraction_instrument])
        self.protocol_node_rna = ProtocolNode(id_='protocol-node/0001', name='RNA extraction', version="0.1",
                                              parameter_values=[self.extraction_instrument])
        self.dna_node = ProductNode(id_='product-node/0002', name='DNA', node_type=SAMPLE, size=3,
                                    characteristics=[self.dna_char])
        self.mrna_node = ProductNode(id_='product-node/0003', name='mRNA', node_type=SAMPLE, size=3,
                                     characteristics=[self.mrna_char])
        self.mirna_node = ProductNode(id_='product-node/0004', name='miRNA', node_type=SAMPLE, size=5,
                                      characteristics=[self.mirna_char])
        self.plan.sample_plan = [self.tissue_node, self.blood_node]
        self.first_assay_graph.add_nodes([self.protocol_node_dna, self.dna_node])
        self.second_assay_graph.add_nodes([self.protocol_node_rna, self.mrna_node, self.mirna_node])
        self.first_assay_graph.add_links([(self.protocol_node_dna, self.dna_node)])
        self.second_assay_graph.add_links([(self.protocol_node_rna, self.mirna_node),
                                           (self.protocol_node_rna, self.mrna_node)])
        self.plan.assay_plan = [self.first_assay_graph, self.second_assay_graph]

    def test_encode_dna_rna_extraction_plan(self):
        actual_json_plan = json.loads(json.dumps(self.plan, cls=SampleAndAssayPlanEncoder))
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'dna-rna-extraction-sample-and-assay-plan.json')) as expected_json_fp:
            expected_json_plan = json.load(expected_json_fp)
        self.assertEqual(ordered(actual_json_plan), ordered(expected_json_plan))

    def test_decode_dna_rna_extraction_plan(self):
        decoder = SampleAndAssayPlanDecoder()
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'dna-rna-extraction-sample-and-assay-plan.json')) as expected_json_fp:
            json_text = json.dumps(json.load(expected_json_fp))
            actual_plan = decoder.loads(json_text)
        """
        print("Expected Assay Plan:")
        for graph in self.plan.assay_plan:
            print(graph)
        print("\nActual Assay Plan:")
        for graph in actual_plan.assay_plan:
            print(graph)
        """
        self.assertEqual(self.plan.sample_plan, actual_plan.sample_plan)
        unmatched_expected = self.plan.assay_plan - actual_plan.assay_plan
        unmatched_actual = actual_plan.assay_plan - self.plan.assay_plan
        print(unmatched_actual)
        print(unmatched_expected)
        if unmatched_expected and unmatched_actual:
            print('here we are')
            unmatched_expected_el = unmatched_expected.pop()
            unmatched_actual_el = unmatched_actual.pop()
            self.assertEqual(unmatched_expected_el.id, unmatched_actual_el.id)
            self.assertEqual(unmatched_expected_el.nodes, unmatched_actual_el.nodes)
            self.assertEqual(unmatched_expected_el.links, unmatched_actual_el.links)
            self.assertEqual(repr(unmatched_expected_el), repr(unmatched_actual_el))
            self.assertEqual(unmatched_expected_el, unmatched_actual_el)
            print('all these test passed')
        self.assertEqual(self.plan.assay_plan, actual_plan.assay_plan)
        self.assertEqual(self.plan, actual_plan)


class StudyArmEncoderTest(BaseTestCase):

    def setUp(self):
        return super(StudyArmEncoderTest, self).setUp()

    def test_encode_arm_with_single_element_cells(self):
        actual_json_arm = json.loads(json.dumps(self.single_treatment_cell_arm, cls=StudyArmEncoder))
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'study-arm-with-single-element-cells.json')) as expected_json_fp:
            expected_json_arm = json.load(expected_json_fp)
        print(actual_json_arm)
        self.assertEqual(ordered(actual_json_arm), ordered(expected_json_arm))

    def test_encode_arm_with_multi_element_cell(self):
        actual_json_arm = json.loads(json.dumps(self.multi_treatment_cell_arm, cls=StudyArmEncoder))
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'study-arm-with-multi-element-cell.json')) as expected_json_fp:
            expected_json_arm = json.load(expected_json_fp)
        self.assertEqual(ordered(actual_json_arm), ordered(expected_json_arm))


class StudyArmDecoderTest(BaseTestCase):

    def setUp(self):
        return super(StudyArmDecoderTest, self).setUp()

    def test_decode_arm_with_single_element_cells(self):
        decoder = StudyArmDecoder()
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'study-arm-with-single-element-cells.json')) as expected_json_fp:
            json_text = json.dumps(json.load(expected_json_fp))
            actual_arm = decoder.loads(json_text)
        self.assertEqual(self.single_treatment_cell_arm, actual_arm)

    def test_decode_arm_with_multi_element_cells(self):
        decoder = StudyArmDecoder()
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'study-arm-with-multi-element-cell.json')) as expected_json_fp:
            json_text = json.dumps(json.load(expected_json_fp))
            actual_arm = decoder.loads(json_text)
        self.assertEqual(self.multi_treatment_cell_arm, actual_arm)


class StudyDesignEncoderTest(BaseTestCase):

    def setUp(self):
        super(StudyDesignEncoderTest, self).setUp()
        self.three_arm_study_design = StudyDesign(name=TEST_STUDY_DESIGN_NAME_THREE_ARMS, study_arms={
            self.single_treatment_cell_arm,
            self.single_treatment_cell_arm_01,
            self.single_treatment_cell_arm_02
        })
        self.multi_element_cell_two_arm_study_design = StudyDesign(
            name=TEST_STUDY_DESIGN_NAME_TWO_ARMS_MULTI_ELEMENT_CELLS, study_arms=[
                self.multi_treatment_cell_arm,
                self.multi_treatment_cell_arm_01
            ])

    def test_encode_study_design_with_three_arms(self):
        actual_json_study_design = json.loads(json.dumps(self.three_arm_study_design, cls=StudyDesignEncoder))
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'study-design-with-three-arms-single-element-cells.json')) as expected_json_fp:
            expected_json_study_design = json.load(expected_json_fp)
        self.assertEqual(ordered(actual_json_study_design), ordered(expected_json_study_design))

    def test_encode_study_design_with_two_arms_with_multi_element_cells(self):
        actual_json_study_design = json.loads(json.dumps(self.multi_element_cell_two_arm_study_design,
                                                         cls=StudyDesignEncoder))
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'study-design-with-two-arms-multi-element-cells.json')) as expected_json_fp:
            expected_json_study_design = json.load(expected_json_fp)
        self.assertEqual(ordered(actual_json_study_design), ordered(expected_json_study_design))


class StudyDesignDecoderTest(BaseTestCase):

    def setUp(self):
        super(StudyDesignDecoderTest, self).setUp()
        self.three_arm_study_design = StudyDesign(name=TEST_STUDY_DESIGN_NAME_THREE_ARMS, study_arms={
            self.single_treatment_cell_arm,
            self.single_treatment_cell_arm_01,
            self.single_treatment_cell_arm_02
        })
        self.multi_element_cell_two_arm_study_design = StudyDesign(
            name=TEST_STUDY_DESIGN_NAME_TWO_ARMS_MULTI_ELEMENT_CELLS, study_arms=[
                self.multi_treatment_cell_arm,
                self.multi_treatment_cell_arm_01
            ])

    def test_decode_study_design_with_three_arms(self):
        decoder = StudyDesignDecoder()
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'study-design-with-three-arms-single-element-cells.json')) as expected_json_fp:
            json_text = json.dumps(json.load(expected_json_fp))
            actual_study_design = decoder.loads(json_text)
        # print("\nExpected:\n")
        # print(self.three_arm_study_design)
        # print("\nActual:\n")
        # print(actual_study_design)
        # print("\nDifference:\n")
        import difflib
        # difflib.ndiff(repr(self.three_arm_study_design), repr(actual_study_design))
        self.assertEqual(self.three_arm_study_design.name, actual_study_design.name)
        """
        for i, arm in enumerate(self.three_arm_study_design.study_arms):
            print("comparing study arm #{0} - {1}".format(i, arm.name))
            print("Difference:\n")
            difflib.ndiff(arm, actual_study_design.study_arms[i])
            print("\nExpected:\n")
            print(arm)
            print("\nActual:\n")
            print(actual_study_design.study_arms[i])
            self.assertEqual(arm, actual_study_design.study_arms[i])
        self.assertEqual(self.three_arm_study_design.study_arms[0], actual_study_design.study_arms[0])
        self.assertEqual(self.three_arm_study_design.study_arms[1], actual_study_design.study_arms[1])
        expected_third_arm = self.three_arm_study_design.study_arms[2]
        self.assertEqual(expected_third_arm.name, actual_study_design.study_arms[2].name)
        self.assertEqual(expected_third_arm.group_size,
                         actual_study_design.study_arms[2].group_size)
        # print("Arm map:")
        # print(list(actual_study_design.study_arms[2].arm_map.keys()))
        i = 0
        for cell, sample_assay_plan in expected_third_arm.arm_map.items():
            print("testing cell {0}".format(cell.name))
            print(cell)
            print(list(actual_study_design.study_arms[2].arm_map.keys())[i])
            self.assertTrue(cell in actual_study_design.study_arms[2].arm_map)
            self.assertEqual(sample_assay_plan, actual_study_design.study_arms[2].arm_map[cell])
            i = i + 1
        self.assertEqual(self.three_arm_study_design.study_arms[2], actual_study_design.study_arms[2])
        # self.assertEqual(self.three_arm_study_design.study_arms[2], actual_study_design.study_arms[2])
        """
        self.assertEqual(self.three_arm_study_design, actual_study_design)

    def test_decode_study_design_with_two_arms_with_multi_element_cells(self):
        decoder = StudyDesignDecoder()
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'study-design-with-two-arms-multi-element-cells.json')) as expected_json_fp:
            json_text = json.dumps(json.load(expected_json_fp))
            actual_study_design = decoder.loads(json_text)
        self.assertEqual(self.multi_element_cell_two_arm_study_design, actual_study_design)


