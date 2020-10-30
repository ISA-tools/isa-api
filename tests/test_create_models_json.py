"""Tests on serializing planning objects in isatools.create.models to JSON"""
import json
import os
import unittest
from io import StringIO

from isatools.create.models import *
from isatools.tests import utils
from tests.create_sample_assay_plan_odicts import nmr_assay_dict


def ordered(o):  # to enable comparison of JSONs with lists using ==

    def handle_inner_lists(el):
        # log.info('el = {}'.format(el))
        if isinstance(el, list):
            # log.info('El is list, returning el[0]:{}'.format(el[0]))
            return handle_inner_lists(el[0])
        else:
            # log.info('El is not list, returning el: '.format(el))
            return el

    if isinstance(o, dict):
        return sorted((k, ordered(v)) for k, v in o.items())
    try:
        if isinstance(o, list):
            return sorted((ordered(x) for x in o if x is not None), key=handle_inner_lists)
    except TypeError as e:
        log.error('Object who raised error is {}'.format(o))
        log.error('Object which raised error is of type {}'.format(type(o)))
        for x in o:
            log.error('x = {}; type(x) = {}'.format(x, type(x)))
        raise e
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


class OrderedTest(unittest.TestCase):

    def test_lists_of_lists(self):
        test_list = [
            {
                'id': 3
            }, {
                'id': 1
            }, {
                'id': 0
            }, [
                {
                    'id': 2
                }, {
                    'id': 7
                }, {
                    'id': 5
                }
            ], {
                'id': 6
            }
        ]
        filtered_test_list = [el for el in test_list if not isinstance(el, list)]
        ordered_filtered_list = ordered(filtered_test_list)
        self.assertIsInstance(ordered_filtered_list, list)
        ordered_list = ordered(test_list)
        self.assertIsInstance(ordered_list, list)


class OntologyAnnotationTest(unittest.TestCase):

    def test_simple_ontology_annotation(self):
        annotation = OntologyAnnotation(term="aspirin")
        annotation_json = json.dumps(annotation, cls=OntologyAnnotationEncoder, sort_keys=True, indent=4)
        print(annotation_json)
        self.assertEqual(json.loads(annotation_json), {"term": "aspirin"})


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
        self.fifth_treatment = Treatment(element_type=INTERVENTIONS['DIETARY'], factor_values=(
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
        self.sample_assay_plan_for_screening = SampleAndAssayPlan(name='SAMPLE ASSAY PLAN FOR SCREENING')
        self.sample_assay_plan_for_treatments = SampleAndAssayPlan(name='SAMPLE ASSAY PLAN FOR TREATMENTS')
        self.sample_assay_plan_for_washout = SampleAndAssayPlan(name='SAMPLE ASSAY PLAN FOR WASHOUT')
        self.sample_assay_plan_for_follow_up = SampleAndAssayPlan(name='FOLLOW-UP SAMPLE ASSAY PLAN')
        self.test_source_characteristics_00 = [
            Characteristic(category='sex', value='M'),
            Characteristic(category='age group', value='old')
        ]
        self.test_source_characteristics_01 = [
            Characteristic(category='sex', value='F'),
            Characteristic(category='age group', value='old')
        ]
        self.test_source_characteristics_02 = [
            Characteristic(category='sex', value='M'),
            Characteristic(category='age group', value='young')
        ]
        self.single_treatment_cell_arm = StudyArm(
            name=TEST_STUDY_ARM_NAME_00,
            source_type=DEFAULT_SOURCE_TYPE,
            source_characteristics=self.test_source_characteristics_00,
            group_size=10,
            arm_map=OrderedDict([
                (self.cell_screen, None), (self.cell_run_in, None),
                (self.cell_single_treatment_00, self.sample_assay_plan_for_treatments),
                (self.cell_washout_00, self.sample_assay_plan_for_washout),
                (self.cell_single_treatment_01, self.sample_assay_plan_for_treatments),
                (self.cell_follow_up, self.sample_assay_plan_for_follow_up)
            ])
        )
        self.single_treatment_cell_arm_01 = StudyArm(
            name=TEST_STUDY_ARM_NAME_01,
            source_type=DEFAULT_SOURCE_TYPE,
            source_characteristics=self.test_source_characteristics_01,
            group_size=30,
            arm_map=OrderedDict([
                (self.cell_screen, None), (self.cell_run_in, None),
                (self.cell_single_treatment_00, self.sample_assay_plan_for_treatments),
                (self.cell_washout_00, self.sample_assay_plan_for_washout),
                (self.cell_single_treatment_biological, self.sample_assay_plan_for_treatments),
                (self.cell_follow_up, self.sample_assay_plan_for_follow_up)
            ])
        )
        self.single_treatment_cell_arm_02 = StudyArm(
            name=TEST_STUDY_ARM_NAME_02,
            source_type=DEFAULT_SOURCE_TYPE,
            source_characteristics=self.test_source_characteristics_02,
            group_size=24,
            arm_map=OrderedDict([
                (self.cell_screen, None), (self.cell_run_in, None),
                (self.cell_single_treatment_diet, self.sample_assay_plan_for_treatments),
                (self.cell_washout_00, self.sample_assay_plan_for_washout),
                (self.cell_single_treatment_radiological, self.sample_assay_plan_for_treatments),
                (self.cell_follow_up, self.sample_assay_plan_for_follow_up)
            ])
        )
        self.multi_treatment_cell_arm = StudyArm(
            name=TEST_STUDY_ARM_NAME_00,
            source_type=DEFAULT_SOURCE_TYPE,
            source_characteristics=self.test_source_characteristics_00,
            group_size=35,
            arm_map=OrderedDict([
                (self.cell_screen, self.sample_assay_plan_for_screening),
                (self.cell_multi_elements_padded, self.sample_assay_plan_for_treatments),
                (self.cell_follow_up, self.sample_assay_plan_for_follow_up)
            ])
        )
        self.multi_treatment_cell_arm_01 = StudyArm(
            name=TEST_STUDY_ARM_NAME_01,
            source_type=DEFAULT_SOURCE_TYPE,
            source_characteristics=self.test_source_characteristics_01,
            group_size=5,
            arm_map=OrderedDict([
                (self.cell_screen, self.sample_assay_plan_for_screening),
                (self.cell_multi_elements_bio_diet, self.sample_assay_plan_for_treatments),
                (self.cell_follow_up, self.sample_assay_plan_for_follow_up)
            ])
        )
        self.mouse_source_type = Characteristic(
            category=OntologyAnnotation(
                term="Study Subject", term_accession="http://purl.obolibrary.org/obo/NCIT_C41189",
                term_source=default_ontology_source_reference
            ),
            value=OntologyAnnotation(
                term="Mouse", term_accession="http://purl.obolibrary.org/obo/NCIT_C14238",
                term_source=default_ontology_source_reference
            )
        )
        self.multi_treatment_cell_arm_mouse = StudyArm(
            source_type=self.mouse_source_type,
            name=TEST_STUDY_ARM_NAME_00, group_size=35, arm_map=OrderedDict([
                (self.cell_screen, self.sample_assay_plan_for_screening),
                (self.cell_multi_elements_padded, self.sample_assay_plan_for_treatments),
                (self.cell_follow_up, self.sample_assay_plan_for_follow_up)
            ])
        )


class CharacteristicEncoderTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_with_ontology_annotations(self):
        ncit = OntologySource(name='NCIT')
        characteristic = Characteristic(
            category=OntologyAnnotation(
                term='length',
                term_accession='http://purl.obolibrary.org/obo/NCIT_C25334',
                term_source=ncit
            ),
            value=200,
            unit=OntologyAnnotation(
                term='meter',
                term_accession='http://purl.obolibrary.org/obo/NCIT_C41139',
                term_source=ncit
            )
        )
        # log.info('Characteristic is {0}'.format(characteristic))
        actual_json_characteristic = json.loads(json.dumps(characteristic, cls=CharacteristicEncoder))
        expected_json_characteristic = {
            'category': {
                'term': characteristic.category.term,
                'termAccession': characteristic.category.term_accession,
                'termSource': {'name': ncit.name}
            },
            'value': characteristic.value,
            'unit': {
                'term': characteristic.unit.term,
                'termAccession': characteristic.unit.term_accession,
                'termSource': {'name': ncit.name}
            }
        }
        self.assertEqual(ordered(actual_json_characteristic), ordered(expected_json_characteristic))

    def test_with_strings(self):
        characteristic = Characteristic(category='organism', value='homo sapiens sapiens')
        # log.info('Characteristic is {0}'.format(characteristic))
        actual_json_characteristic = json.loads(json.dumps(characteristic, cls=CharacteristicEncoder))
        expected_json_characteristic = {
            'category': characteristic.category,
            'value': characteristic.value
        }
        self.assertEqual(ordered(actual_json_characteristic), ordered(expected_json_characteristic))


class CharacteristicDecoderTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_characteristic_complete(self):
        characteristic_complete = Characteristic(
            category=OntologyAnnotation(
                term='Length', term_accession='http://purl.obolibrary.org/obo/NCIT_C25334',
                term_source=default_ontology_source_reference
            ),
            value=9.9,
            unit=OntologyAnnotation(
                term='m', term_accession='http://purl.obolibrary.org/obo/NCIT_C41139',
                term_source=default_ontology_source_reference
            )
        )
        decoder = CharacteristicDecoder()
        with open(
                os.path.join(os.path.dirname(__file__), 'data', 'json', 'create', 'characteristic-complete.json')
        ) as expected_json_fp:
            json_text = json.dumps(json.load(expected_json_fp))
            actual_characteristic = decoder.loads(json_text)
        self.assertEqual(characteristic_complete, actual_characteristic)

    def test_characteristic_no_unit(self):
        characteristic_no_unit = Characteristic(
            category=OntologyAnnotation(
                term='Study Subject', term_accession='http://purl.obolibrary.org/obo/NCIT_C41189',
                term_source=default_ontology_source_reference
            ),
            value=OntologyAnnotation(
                term='Human', term_accession='http://purl.obolibrary.org/obo/NCIT_C14225',
                term_source=default_ontology_source_reference
            )
        )
        decoder = CharacteristicDecoder()
        with open(
                os.path.join(os.path.dirname(__file__), 'data', 'json', 'create', 'characteristic-no-unit.json')
        ) as expected_json_fp:
            json_text = json.dumps(json.load(expected_json_fp))
            actual_characteristic = decoder.loads(json_text)
        self.assertEqual(characteristic_no_unit, actual_characteristic)

    def test_characteristics_string(self):
        characteristic_string_dict = {
            'category': 'Time',
            'value': 126.4,
            'unit': 'sec.'
        }
        characteristic_plain = Characteristic(category='Time', value=126.4, unit='sec.')
        decoder = CharacteristicDecoder()
        json_text = json.dumps(characteristic_string_dict)
        actual_characteristic = decoder.loads(json_text)
        self.assertEqual(actual_characteristic, characteristic_plain)


class StudyCellEncoderTest(BaseTestCase):

    def setUp(self):
        return super(StudyCellEncoderTest, self).setUp()

    def test_encode_single_treatment_cell(self):
        actual_json_cell = json.loads(json.dumps(self.cell_single_treatment_00, cls=StudyCellEncoder))
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'single-treatment-cell.json')) as expected_json_fp:
            expected_json_cell = json.load(expected_json_fp)
        self.assertEqual(ordered(actual_json_cell), ordered(expected_json_cell))

    def test_encode_single_treatment_cell_with_ontology_annotations(self):
        f1 = StudyFactor(name='painkiller', factor_type=OntologyAnnotation(term="chemical compound"))
        f2 = StudyFactor(name='dose', factor_type=OntologyAnnotation(term="quantity"))
        f3 = StudyFactor(name='time post exposure', factor_type=OntologyAnnotation(term="time"))
        f1v1 = FactorValue(factor_name=f1, value=OntologyAnnotation(term="aspirin"))
        f2v1 = FactorValue(factor_name=f2, value=OntologyAnnotation(term='low dose'))
        f3v1 = FactorValue(factor_name=f3, value='1', unit=OntologyAnnotation(term='hr'))
        te1 = Treatment()
        te1.type = 'chemical intervention'
        te1.factor_values = [f1v1, f2v1, f3v1]
        cell = StudyCell(name='test_cell', elements=(te1, ))
        json_cell = json.loads(json.dumps(cell, cls=StudyCellEncoder))
        print(json.dumps(cell, cls=StudyCellEncoder, indent=4, sort_keys=True))
        for factor_value_dict in json_cell['elements'][0]['factorValues']:
            self.assertIsNotNone(factor_value_dict['value'])

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
        self.plan = SampleAndAssayPlan(name='TEST SAMPLE AND ASSAY PLAN')
        self.first_assay_graph = AssayGraph(id_="assay-graph/00", measurement_type='genomic extraction',
                                            technology_type='nucleic acid extraction')
        self.second_assay_graph = AssayGraph(id_="assay-graph/01",  measurement_type='genomic extraction',
                                             technology_type='nucleic acid extraction')
        self.third_assay_graph = AssayGraph(id_='assay-graph/02',
                                            measurement_type=OntologyAnnotation(term='genomic extraction'),
                                            technology_type=OntologyAnnotation(term='nucleic acid extraction'))
        self.tissue_char = Characteristic(category='organism part', value='tissue')
        self.blood_char = Characteristic(category='organism part', value='blood')
        self.tissue_node = ProductNode(id_='product-node/0000', name='tissue', node_type=SAMPLE, size=2,
                                       characteristics=[self.tissue_char])
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
        self.dna_node = ProductNode(id_='product-node/0002', name='DNA', node_type=EXTRACT, size=3,
                                    characteristics=[self.dna_char])
        self.mrna_node = ProductNode(id_='product-node/0003', name='mRNA', node_type=EXTRACT, size=3,
                                     characteristics=[self.mrna_char])
        self.mirna_node = ProductNode(id_='product-node/0004', name='miRNA', node_type=EXTRACT, size=5,
                                      characteristics=[self.mirna_char])
        self.plan.sample_plan = [self.tissue_node, self.blood_node]
        self.first_assay_graph.add_nodes([self.protocol_node_dna, self.dna_node])
        self.second_assay_graph.add_nodes([self.protocol_node_rna, self.mrna_node, self.mirna_node])
        self.first_assay_graph.add_links([(self.protocol_node_dna, self.dna_node)])
        self.second_assay_graph.add_links([(self.protocol_node_rna, self.mirna_node),
                                           (self.protocol_node_rna, self.mrna_node)])
        self.plan.assay_plan = [self.first_assay_graph, self.second_assay_graph]
        self.plan.sample_to_assay_map = {
            self.tissue_node: [self.first_assay_graph, self.second_assay_graph],
            self.blood_node: [self.first_assay_graph, self.second_assay_graph]
        }

    def test_encode_dna_rna_extraction_plan(self):
        actual_json_plan = json.loads(json.dumps(self.plan, cls=SampleAndAssayPlanEncoder))
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'dna-rna-extraction-sample-and-assay-plan.json')) as expected_json_fp:
            expected_json_plan = json.load(expected_json_fp)
        self.assertEqual(ordered(actual_json_plan), ordered(expected_json_plan))

    def test_encode_sample_from_dictionary(self):   # TODO
        pass

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
            self.assertEqual(repr(unmatched_expected_el.links), repr(unmatched_actual_el.links))
            self.assertEqual(repr(unmatched_expected_el), repr(unmatched_actual_el))
            self.assertEqual(unmatched_expected_el, unmatched_actual_el)
            print('all these test passed')
        self.assertEqual(self.plan.assay_plan, actual_plan.assay_plan)
        self.assertEqual(self.plan.sample_to_assay_map, actual_plan.sample_to_assay_map)
        self.assertEqual(self.plan, actual_plan)

    def test_encode_and_decode_assay_graph_with_ontology_annotation(self):
        encoder = SampleAndAssayPlanEncoder()
        decoder = SampleAndAssayPlanDecoder()
        ag_dict = encoder.assay_graph(self.third_assay_graph)
        assay_graph_reconstructed = decoder.loads_assay_graph(ag_dict)
        self.assertIsInstance(assay_graph_reconstructed, AssayGraph)
        self.assertEqual(assay_graph_reconstructed.technology_type, self.third_assay_graph.technology_type)
        self.assertEqual(assay_graph_reconstructed.measurement_type, self.third_assay_graph.measurement_type)
        self.assertEqual(assay_graph_reconstructed.id, self.third_assay_graph.id)

    def test_encode_sample_and_assay_plan_with_ontology_annotations(self):
        input_material = ProductNode(
            id_="MAT1", name="liver", node_type=SAMPLE, size=1,
            characteristics=[
                Characteristic(
                    category=OntologyAnnotation(term='organism part'), value=OntologyAnnotation(term='liver')
                )
            ]
        )
        nmr_assay_graph = AssayGraph.generate_assay_plan_from_dict(nmr_assay_dict)
        sap1 = SampleAndAssayPlan(name='A TEST SA PLAN', sample_plan=[input_material], assay_plan=[nmr_assay_graph])
        sample2assay_plan = {input_material: [nmr_assay_graph]}
        sap1.sample_to_assay_map = sample2assay_plan
        actual_json_plan = json.loads(json.dumps(sap1, cls=SampleAndAssayPlanEncoder))
        print(json.dumps(sap1, cls=SampleAndAssayPlanEncoder, indent=4, sort_keys=True))
        assay_node_json = next(node for node in actual_json_plan["assayPlan"][0]["nodes"]
                               if node["@id"] == "nmr_spectroscopy_000_000")
        for param_val_json in assay_node_json["parameterValues"]:
            self.assertIsNotNone(param_val_json["name"])
            self.assertIsNotNone(param_val_json["value"])


class StudyArmEncoderTest(BaseTestCase):

    def setUp(self):
        return super(StudyArmEncoderTest, self).setUp()

    def test_encode_arm_with_single_element_cells(self):
        actual_json_arm = json.loads(json.dumps(self.single_treatment_cell_arm, cls=StudyArmEncoder))
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'study-arm-with-single-element-cells.json')) as expected_json_fp:
            expected_json_arm = json.load(expected_json_fp)
        print('expected source type is {}'.format(expected_json_arm['sourceType']))
        print('actual source type is {}'.format(actual_json_arm['sourceType']))
        self.assertEqual(ordered(actual_json_arm["sourceType"]), ordered(expected_json_arm["sourceType"]))
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

    def test_decode_arm_with_multi_element_cells_mouse(self):
        decoder = StudyArmDecoder()
        with open(os.path.join(os.path.dirname(__file__), 'data', 'json', 'create',
                               'study-arm-with-multi-element-cell-mouse.json')) as expected_json_fp:
            json_text = json.dumps(json.load(expected_json_fp))
            actual_arm = decoder.loads(json_text)
        self.assertIsInstance(actual_arm, StudyArm)
        log.info('Expected Arm source type: {}'.format(self.multi_treatment_cell_arm_mouse.source_type))
        log.info('Actual Arm source type: {}'.format(actual_arm.source_type))
        self.assertEqual(self.multi_treatment_cell_arm_mouse, actual_arm)


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




