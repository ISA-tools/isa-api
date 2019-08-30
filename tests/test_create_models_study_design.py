import unittest
from functools import reduce
from collections import OrderedDict

from isatools.model import *
from isatools.errors import *

from isatools.create.models import *

import networkx as nx
import uuid
import logging

log = logging.getLogger('isatools')
log.setLevel(logging.DEBUG)

NAME = 'name'
FACTORS_0_VALUE = 'nitroglycerin'
FACTORS_0_VALUE_ALT = 'alcohol'
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

sample_list = [
        {
            'node_type': SAMPLE,
            'characteristics_category': 'organism part',
            'characteristics_value': 'liver',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'organism part',
            'characteristics_value': 'blood',
            'size': 5,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': 'organism part',
            'characteristics_value': 'heart',
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        }
]

ms_assay_dict = OrderedDict([
    ('measurement_type', 'metabolite profiling'),
    ('technology_type', 'mass spectrometry'),
    ('extraction', {}),
    ('extract', [
        {
            'node_type': EXTRACT,
            'characteristics_category': 'extract type',
            'characteristics_value': 'polar fraction',
            'size': 1,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': EXTRACT,
            'characteristics_category': 'extract type',
            'characteristics_value': 'lipids',
            'size': 1,
            'is_input_to_next_protocols': True
        }
    ]),
    ('labelling', {
        '#replicates': 2
    }),
    ('labelled extract', [
        {
            'node_type': LABELED_EXTRACT,
            'characteristics_category': 'labelled extract type',
            'characteristics_value': '',
            'size': 1,
            'is_input_to_next_protocols': True
        }
    ]),
    ('mass spectrometry', {
        '#replicates': 2,
        'instrument': ['Agilent QTQF §'],
        'injection_mode': ['FIA', 'LC'],
        'acquisition_mode': ['positive mode']
    }),
    ('raw spectral data file', [
        {
            'node_type': DATA_FILE,
            'size': 2,
            'is_input_to_next_protocols': False
        }
    ])
])

phti_assay_dict = OrderedDict([
    ('measurement_type', 'phenotyping'),
    ('technology_type', 'high-throughput imaging'),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'supernatant',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': EXTRACT,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'pellet',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('phenotyping by high throughput imaging', {
                'instrument': ['lemnatech gigant'],
                'acquisition_mode': ['UV light','near-IR light','far-IR light','visible light'],
                'camera position': ['top','120 degree','240 degree','360 degree'],
                'imaging daily schedule': ['06.00','19.00']
            }),
            ('raw_spectral_data_file', [
                {
                    'node_type': DATA_FILE,
                    'size': 1,
                    'technical_replicates': 2,
                    'is_input_to_next_protocols': False
                }
            ])
        ])

lcdad_assay_dict = OrderedDict([
    ('measurement_type', 'metabolite identification'),
    ('technology_type', 'liquid chromatography diode-array detector'),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'supernatant',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': EXTRACT,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'pellet',
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('lcdad_spectroscopy', {
                'instrument': ['Shimadzu DAD 400'],
            }),
            ('raw_spectral_data_file', [
                {
                    'node_type': DATA_FILE,
                    'size': 1,
                    'technical_replicates': 2,
                    'is_input_to_next_protocols': False
                }
            ])
        ])

nmr_assay_dict = OrderedDict([
    ('measurement_type', 'metabolite profiling'),
    ('technology_type', 'nmr spectroscopy'),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'supernatant',
                    'size': 1,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': EXTRACT,
                    'characteristics_category': 'extract type',
                    'characteristics_value': 'pellet',
                    'size': 1,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('nmr_spectroscopy', {
                '#replicates': 2,
                'instrument': ['Bruker AvanceII 1 GHz'],
                'acquisition_mode': ['1D 13C NMR', '2D 13C-13C NMR'],
                'pulse_sequence': ['CPMG', 'watergate']
                # 'acquisition_mode': ['1D 13C NMR', '1D 1H NMR', '2D 13C-13C NMR'],
                # 'pulse_sequence': ['CPMG', 'TOCSY', 'HOESY', 'watergate']
            }),
            ('raw_spectral_data_file', [
                {
                    'node_type': DATA_FILE,
                    'size': 1,
                    'is_input_to_next_protocols': False
                }
            ])
        ])


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
                         "comments=[]))])")

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

    def test_factor_values_property(self):
        self.assertIsInstance(self.treatment.factor_values, set)
        self.assertEqual(self.treatment.factor_values, {
            FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE),
            FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
            FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
        })


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
                        'A WASHOUT element can be added at the end of a cell with 2 treatments interspersed '
                        'by a washout')
        self.assertTrue(self.cell._non_treatment_check([
            self.first_treatment, self.washout, self.second_treatment
        ], self.washout), 'A WASHOUT element can be added at the beginning of a cell with 2 treatments '
                          'interspersed by a washout')

    def test_non_treatment_check_multi_element_cell_01(self):
        self.assertTrue(self.cell._non_treatment_check([
            {self.first_treatment, self.second_treatment}, self.washout, self.second_treatment
        ], self.washout), 'A WASHOUT element can be added at the end of a cell with a treatment set and a treatment '
                          'interspersed by a washout')
        self.assertTrue(self.cell._non_treatment_check([
            {self.first_treatment, self.second_treatment}, self.washout, self.second_treatment
        ], self.washout, 0), 'A WASHOUT element can be added at the beginning of a cell with a treatment set and a '
                             'treatment interspersed by a washout')

    def test_non_treatment_check_multi_element_cell_02(self):
        self.assertTrue(self.cell._non_treatment_check([
            self.first_treatment, self.washout, {self.fourth_treatment, self.second_treatment}
        ], self.washout), 'A WASHOUT element can be added at the end of a cell with a treatment and a treatment set'
                          'interspersed by a washout')
        self.assertTrue(self.cell._non_treatment_check([
            self.first_treatment, self.washout, {self.fourth_treatment, self.second_treatment}
        ], self.washout, 0), 'A WASHOUT element can be added at the beginning of a cell with a treatment and a '
                             'treatment set interspersed by a washout')

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
                        'A treatment can be inserted into a cell with a treatment a concomitant treatment and two '
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
        self.assertRaises(ValueError, self.cell.insert_element, self.screen,
                          'A SCREEN cannot be added to a a cell with a SCREEN')
        self.assertEqual(self.cell.elements, [self.screen])
        self.assertRaises(ValueError, self.cell.insert_element, self.first_treatment,
                          'A treatment cannot be added to a cell with a SCREEN')
        self.assertEqual(self.cell.elements, [self.screen])
        self.assertRaises(ValueError, self.cell.insert_element, self.follow_up,
                          'A FOLLOW-UP cannot ba added to a cell with a SCREEN')
        self.assertEqual(self.cell.elements, [self.screen])
        self.assertRaises(ValueError, self.cell.insert_element, {
            self.first_treatment, self.fourth_treatment
        }, 'A treatment set cannot be added to a cell with a SCREEN')
        self.cell.insert_element(self.run_in)
        self.assertEqual(self.cell.elements, [self.screen, self.run_in], 'A RUN-IN is inserted in the cell after the'
                                                                         'SCREEN')

    def test_insert_element_run_in(self):
        self.assertEqual(self.cell.elements, list(), 'The initialized elements set is empty')
        self.cell.insert_element(self.run_in)
        self.assertEqual(self.cell.elements, [self.run_in])
        self.assertRaises(ValueError, self.cell.insert_element, self.screen,
                          'A SCREEN cannot be added to a a cell with a RUN-IN after the RUN-IN')
        self.assertEqual(self.cell.elements, [self.run_in])
        self.assertRaises(ValueError, self.cell.insert_element, self.first_treatment,
                          'A treatment cannot be added to a cell with a RUN-IN')
        self.assertEqual(self.cell.elements, [self.run_in])
        self.assertRaises(ValueError, self.cell.insert_element, self.follow_up,
                          'A FOLLOW-UP cannot ba added to a cell with a RUN-IN')
        self.assertEqual(self.cell.elements, [self.run_in])
        self.assertRaises(ValueError, self.cell.insert_element, {
            self.first_treatment, self.fourth_treatment
        }, 'A treatment set cannot be added to a cell with a RUN-IN')
        self.cell.insert_element(self.screen, 0)
        self.assertEqual(self.cell.elements, [self.screen, self.run_in], 'A SCREEN is inserted in the cell before the'
                                                                         'RUN-IN')

    def test_insert_element_washout__00(self):
        self.assertEqual(self.cell.elements, list(), 'The initialized elements set is empty')
        self.cell.insert_element(self.washout)
        self.assertEqual(self.cell.elements, [self.washout])
        self.assertRaises(ValueError, self.cell.insert_element, self.screen,
                          'A SCREEN cannot be added to a a cell with a WASHOUT')
        self.assertEqual(self.cell.elements, [self.washout])
        self.assertRaises(ValueError, self.cell.insert_element, self.run_in,
                          'A RUN-IN cannot be added to a cell with a WASHOUT')
        self.assertEqual(self.cell.elements, [self.washout])
        self.assertRaises(ValueError, self.cell.insert_element, self.follow_up,
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
        self.assertRaises(ValueError, self.cell.insert_element, self.screen,
                          'A SCREEN cannot be added to a a cell with a FOLLOW-UP')
        self.assertEqual(self.cell.elements, [self.follow_up])
        self.assertRaises(ValueError, self.cell.insert_element, self.first_treatment,
                          'A treatment cannot be added to a cell with a FOLLOW-UP')
        self.assertEqual(self.cell.elements, [self.follow_up])
        self.assertRaises(ValueError, self.cell.insert_element, self.follow_up,
                          'A FOLLOW-UP cannot ba added to a cell with a FOLLOW-UP')
        self.assertEqual(self.cell.elements, [self.follow_up])
        self.assertRaises(ValueError, self.cell.insert_element, {self.first_treatment, self.fourth_treatment},
                          'A treatment set cannot be added to a cell with a FOLLOW-UP')
        self.assertRaises(ValueError, self.cell.insert_element, self.run_in,
                          'A RUN-IN cannot be added to a cell with a FOLLOW-UP')

    def test_insert_element_treatment(self):
        self.assertEqual(self.cell.elements, list(), 'The initialized elements list is empty')
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
        self.assertRaises(ValueError, self.cell.insert_element, self.washout,
                          'A washout cannot be added if there is one before the position where it is to be inserted')
        self.assertRaises(ValueError, self.cell.insert_element, self.washout, 0)
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
        self.assertRaises(ValueError, self.cell.insert_element, self.washout,
                          'A washout cannot be added if there is one before the position where it is to be inserted')
        self.assertRaises(ValueError, self.cell.insert_element, self.washout, 0)
        self.assertTrue(True, 'A washout cannot be added if there is one after the position where it is to be inserted')

    def test_contains_non_treatment_by_type_empty_cell(self):
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(SCREEN), False,
                         'An empty cell contains no SCREEN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(RUN_IN), False,
                         'An empty cell contains no RUN-IN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(WASHOUT), False,
                         'An empty cell contains no WASHOUT')
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
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(SCREEN), False,
                         'A WASHOUT cell contains no SCREEN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(RUN_IN), False,
                         'A WASHOUT cell contains no RUN-IN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(WASHOUT), True,
                         'A WASHOUT cell contains a WASHOUT')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(FOLLOW_UP), False,
                         'A WASHOUT cell contains no FOLLOW_UP')

    def test_contains_non_treatment_by_type_follow_up_cell(self):
        self.cell.elements = [self.follow_up]
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(SCREEN), False,
                         'A FOLLOW-UP cell contains no SCREEN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(RUN_IN), False,
                         'A FOLLOW-UP cell contains no RUN-IN')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(WASHOUT), False,
                         'A FOLLOW-UP cell contains a WASHOUT')
        self.assertEqual(self.cell.contains_non_treatment_element_by_type(FOLLOW_UP), True,
                         'A FOLLOW-UP cell contains no FOLLOW_UP')

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


class ProtocolNodeTest(unittest.TestCase):

    def test_constructor(self):
        node = ProtocolNode(name='sampling', protocol_type='sampling', replicates=2)
        self.assertIsInstance(node, ProtocolNode)

    def test_add_parameter_value(self):
        node = ProtocolNode()
        test_parameter_name = 'test param'
        test_parameter_value = 'param value'
        node.add_parameter_value(test_parameter_name, test_parameter_value)
        actual_parameter_value = node.parameter_values[0]
        self.assertIsInstance(actual_parameter_value, ParameterValue)
        self.assertEqual(actual_parameter_value.category, ProtocolParameter(parameter_name=test_parameter_name))
        self.assertEqual(actual_parameter_value.value, test_parameter_value)
        self.assertEqual(actual_parameter_value.unit, None)

    def test_properties(self):
        node = ProtocolNode()
        self.assertEqual(node.parameter_values, [])
        self.assertEqual(node.parameters, [])
        self.assertEqual(node.components, [])
        self.assertEqual(node.replicates, 1)
        test_parameter_values = [
            ParameterValue(category=ProtocolParameter(parameter_name='test param'), value='tot'),
            ParameterValue(category=ProtocolParameter(parameter_name='another test param'), value='quot', unit='z')
        ]
        node.parameter_values = test_parameter_values
        self.assertEqual(node.parameter_values, test_parameter_values)
        self.assertEqual(node.parameters, [test_pv.category for test_pv in test_parameter_values])
        node.replicates = 3
        self.assertEqual(node.replicates, 3)


class ProductNodeTest(unittest.TestCase):

    def setUp(self):
        self.node = ProductNode()

    def test_id_property(self):
        self.assertIsInstance(uuid.UUID(hex=self.node.id), type(uuid.uuid4()))

    def test_extract_node(self):
        node = ProductNode(node_type=EXTRACT)
        self.assertEqual(node.type, EXTRACT)

    def test_labeled_extract_node(self):
        node = ProductNode(node_type=LABELED_EXTRACT)
        self.assertEqual(node.type, LABELED_EXTRACT)


class QualityControlSourceTest(unittest.TestCase):

    pass


class QualityControlSampleTest(unittest.TestCase):

    def setUp(self):
        self.sample_characteristic = Characteristic(category='sample', value='water')

    def test_init(self):
        qc_sample = QualityControlSample(characteristics=self.sample_characteristic, name='qc_sample_test',
                                         qc_sample_type=QC_SAMPLE_TYPE_PRE_RUN)
        self.assertIsInstance(qc_sample, Sample)
        self.assertIsInstance(qc_sample, QualityControlSample)
        self.assertEqual(qc_sample.characteristics, self.sample_characteristic)
        self.assertEqual(qc_sample.qc_sample_type, QC_SAMPLE_TYPE_PRE_RUN)

    def test_properties(self):
        qc_sample = QualityControlSample(characteristics=self.sample_characteristic, name='qc_sample_test',
                                         qc_sample_type=QC_SAMPLE_TYPE_INTERSPERSED)
        self.assertEqual(qc_sample.qc_sample_type, QC_SAMPLE_TYPE_INTERSPERSED)
        with self.assertRaises(AttributeError, msg='qc_sample_type must be one from allowed values') as ex_cm:
            qc_sample.qc_sample_type = 'some incorrect QC sample type'


class QualityControlTest(unittest.TestCase):

    def setUp(self):
        self.pre_run_sample_type = ProductNode(id_='pre/00', node_type=SAMPLE, name='water')
        self.post_run_sample_type = ProductNode(id_='post/00', node_type=SAMPLE, name='ethanol')
        self.dummy_sample_type = ProductNode(id_='dummy/01', node_type=SAMPLE, name='dummy')
        self.more_dummy_sample_type = ProductNode(id_='dummy/02', node_type=SAMPLE, name='more dummy')
        self.interspersed_sample_types = [(self.dummy_sample_type, 20)]

    def test_init(self):
        qc = QualityControl()
        self.assertIsInstance(qc, QualityControl)

    def test_properties(self):
        qc = QualityControl()
        self.assertEqual(qc.interspersed_sample_types, [])
        self.assertEqual(qc.pre_run_sample_type, None)
        self.assertEqual(qc.post_run_sample_type, None)
        qc.pre_run_sample_type = self.pre_run_sample_type
        qc.post_run_sample_type = self.post_run_sample_type
        qc.interspersed_sample_types = self.interspersed_sample_types
        self.assertEqual(qc.pre_run_sample_type, self.pre_run_sample_type)
        self.assertEqual(qc.post_run_sample_type, self.post_run_sample_type)
        self.assertEqual(qc.interspersed_sample_types, self.interspersed_sample_types)

    def test_eq(self):
        qc_0 = QualityControl(interspersed_sample_type=self.interspersed_sample_types,
                              pre_run_sample_type=self.pre_run_sample_type,
                              post_run_sample_type=self.post_run_sample_type)
        qc_1 = QualityControl()
        qc_1.pre_run_sample_type = self.pre_run_sample_type
        qc_1.post_run_sample_type = self.post_run_sample_type
        qc_1.interspersed_sample_types = self.interspersed_sample_types
        self.assertEqual(qc_0, qc_1)

    def test_ne(self):
        qc_0 = QualityControl(interspersed_sample_type=self.interspersed_sample_types,
                              pre_run_sample_type=self.pre_run_sample_type,
                              post_run_sample_type=self.post_run_sample_type)
        qc_1 = QualityControl()
        qc_1.pre_run_sample_type = self.pre_run_sample_type
        qc_1.post_run_sample_type = self.post_run_sample_type
        qc_1.interspersed_sample_types = [(self.more_dummy_sample_type, 10)]
        self.assertNotEqual(qc_0, qc_1)

    def test_repr(self):
        qc_0 = QualityControl(interspersed_sample_type=self.interspersed_sample_types,
                              pre_run_sample_type=self.pre_run_sample_type,
                              post_run_sample_type=self.post_run_sample_type)
        qc_1 = QualityControl()
        qc_1.pre_run_sample_type = self.pre_run_sample_type
        qc_1.post_run_sample_type = self.post_run_sample_type
        qc_1.interspersed_sample_types = self.interspersed_sample_types
        self.assertEqual(repr(qc_0), repr(qc_1))

    def test_str(self):
        qc = QualityControl()
        self.assertEqual(str(qc).replace(" ", ""), """QualityControl(
        pre_run_sample_type=None
        post_run_sample_type=None
        interspersed_sample_types=[]
        )""".replace(" ", ""))
        qc = QualityControl(interspersed_sample_type=self.interspersed_sample_types,
                            pre_run_sample_type=self.pre_run_sample_type,
                            post_run_sample_type=self.post_run_sample_type)
        self.assertEqual(str(qc).replace(" ", ""), """QualityControl(
        pre_run_sample_type={0}
        post_run_sample_type={1}
        interspersed_sample_types=[('{2}',{3})]
        )""".format(self.pre_run_sample_type.id, self.post_run_sample_type.id, self.dummy_sample_type.id, 20)
                         .replace(" ", ""))


class AssayGraphTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.assay_graph = AssayGraph(measurement_type='genomic extraction', technology_type='nucleic acid extraction')
        self.tissue_char = Characteristic(category='organism part', value='tissue')
        self.dna_char = Characteristic(category='nucleic acid', value='DNA')
        self.mirna_char = Characteristic(category='nucleic acid', value='miRNA')
        self.mrna_char = Characteristic(category='nucleic acid', value='mRNA')
        self.sample_node = ProductNode(node_type=SAMPLE, size=3, characteristics=[self.tissue_char])
        self.protocol_node_dna = ProtocolNode(name='DNA extraction')
        self.protocol_node_rna = ProtocolNode(name='RNA extraction')
        self.dna_node = ProductNode(node_type=SAMPLE, size=3, characteristics=[self.dna_char])
        self.mrna_node = ProductNode(node_type=SAMPLE, size=3, characteristics=[self.mrna_char])
        self.mirna_node = ProductNode(node_type=SAMPLE, size=5, characteristics=[self.mirna_char])
        self.nodes = [self.protocol_node_dna, self.protocol_node_rna, self.dna_node, self.mrna_node, self.mirna_node]
        self.links = [
            (self.protocol_node_dna, self.dna_node),
            (self.protocol_node_rna, self.mrna_node),
            (self.protocol_node_rna, self.mirna_node)
        ]
        self.pre_run_sample_type = ProductNode(id_='pre/00', node_type=SAMPLE, name='water')
        self.post_run_sample_type = ProductNode(id_='post/00', node_type=SAMPLE, name='ethanol')
        self.dummy_sample_type = ProductNode(id_='dummy/01', node_type=SAMPLE, name='dummy')
        self.more_dummy_sample_type = ProductNode(id_='dummy/02', node_type=SAMPLE, name='more dummy')
        self.interspersed_sample_types = [(self.dummy_sample_type, 20)]
        self.qc = QualityControl(
            interspersed_sample_type=self.interspersed_sample_types,
            pre_run_sample_type=self.pre_run_sample_type,
            post_run_sample_type=self.post_run_sample_type
        )

    def test_init(self):
        assay_graph = AssayGraph(measurement_type='genomic extraction', technology_type='nucleic acid extraction',
                                 nodes=self.nodes, links=self.links)
        self.assertEqual(assay_graph.measurement_type, 'genomic extraction')
        self.assertEqual(assay_graph.technology_type, 'nucleic acid extraction')
        self.assertEqual(assay_graph.nodes, set(self.nodes))
        for link in self.links:
            self.assertIn(link, assay_graph.links)

    def test_generate_assay_plan_from_dict_00(self):
        self.assay_graph = AssayGraph.generate_assay_plan_from_dict(
            assay_plan_dict=lcdad_assay_dict, id_='assay-plan/00'
        )
        self.assertIsInstance(self.assay_graph, AssayGraph)
        self.assertEqual(self.assay_graph.id, 'assay-plan/00')

    def test_generate_assay_plan_from_dict_00(self):
        nmr_assay_graph = AssayGraph.generate_assay_plan_from_dict(nmr_assay_dict)
        self.assertIsInstance(self.assay_graph, AssayGraph)
        self.assertIsNotNone(nmr_assay_graph.id)
        self.assertIsInstance(nmr_assay_graph.id, str)
        nmr_nodes = list(filter(lambda n: n.name == 'nmr_spectroscopy', nmr_assay_graph.nodes))
        self.assertEqual(len(nmr_nodes), 8)
        for node in nmr_nodes:
            self.assertEqual(node.replicates, 2)

    def test_properties_success(self):
        self.assertEqual(self.assay_graph.measurement_type, 'genomic extraction')
        self.assertEqual(self.assay_graph.technology_type, 'nucleic acid extraction')
        self.assay_graph.measurement_type = 'some other measurement'
        self.assay_graph.technology_type = 'some other tech'
        self.assertEqual(self.assay_graph.measurement_type, 'some other measurement')
        self.assertEqual(self.assay_graph.technology_type, 'some other tech')
        self.assay_graph.measurement_type = OntologyAnnotation(term='some other measurement')
        self.assay_graph.technology_type = OntologyAnnotation(term='some other tech')
        self.assertEqual(self.assay_graph.measurement_type, OntologyAnnotation(term='some other measurement'))
        self.assertEqual(self.assay_graph.technology_type, OntologyAnnotation(term='some other tech'))
        self.assertEqual(self.assay_graph.quality_control, None)
        self.assay_graph.quality_control = self.qc
        self.assertEqual(self.assay_graph.quality_control, self.qc)

    def test_properties_raises(self):
        # TODO complete this test
        with self.assertRaises(AttributeError, msg='An integer is not a valid measurement_type') as ex_cm:
            self.assay_graph.measurement_type = 120
        self.assertIsNotNone(ex_cm.exception.args[0])
        with self.assertRaises(AttributeError, msg='A string is not a valid quality_control') as ex_cm:
            self.assay_graph.quality_control = 'bao'
        self.assertEqual(ex_cm.exception.args[0], AssayGraph.QUALITY_CONTROL_ERROR.format(type('bao')))

    def test_add_first_node(self):
        first_node = ProductNode(node_type=SOURCE, size=10)
        self.assay_graph.add_node(first_node)
        self.assertEqual(len(self.assay_graph.nodes), 1)
        self.assertEqual(self.assay_graph.nodes.pop(), first_node)

    def test_create_three_level_graph_success(self):
        self.assay_graph.add_node(self.sample_node)
        self.assay_graph.add_node(self.protocol_node_dna)
        self.assay_graph.add_node(self.protocol_node_rna)
        self.assay_graph.add_node(self.dna_node)
        self.assay_graph.add_node(self.mrna_node)
        self.assay_graph.add_node(self.mirna_node)
        self.assay_graph.add_link(self.sample_node, self.protocol_node_rna)
        self.assay_graph.add_link(self.sample_node, self.protocol_node_dna)
        self.assay_graph.add_link(self.protocol_node_dna, self.dna_node)
        self.assay_graph.add_link(self.protocol_node_rna, self.mrna_node)
        self.assay_graph.add_link(self.protocol_node_rna, self.mrna_node)
        self.assertEqual(len(self.assay_graph.nodes), 6)
        self.assertIn(self.sample_node, self.assay_graph.nodes)
        self.assertIn(self.dna_node, self.assay_graph.nodes)
        self.assertIn(self.mrna_node, self.assay_graph.nodes)
        self.assertIn(self.mirna_node, self.assay_graph.nodes)
        self.assertIn((self.protocol_node_dna, self.dna_node), self.assay_graph.links)
        self.assertIn((self.protocol_node_rna, self.mrna_node), self.assay_graph.links)
        self.assertIn((self.protocol_node_rna, self.mrna_node), self.assay_graph.links)
        
    def test_add_nodes_and_links_success(self):
        nodes = [self.sample_node, self.protocol_node_rna, self.mrna_node, self.mirna_node]
        links = [(self.sample_node, self.protocol_node_rna), (self.protocol_node_rna, self.mrna_node),
                 (self.protocol_node_rna, self.mirna_node)]
        self.assay_graph.add_nodes(nodes)
        self.assay_graph.add_links(links)
        self.assertEqual(len(self.assay_graph.nodes), len(nodes))
        self.assertEqual(set(self.assay_graph.nodes), set(nodes))
        self.assertEqual(len(self.assay_graph.links), len(links))

    def test_start_nodes_property(self):
        assay_graph = AssayGraph(measurement_type='genomic extraction', technology_type='nucleic acid extraction',
                                 nodes=self.nodes, links=self.links)
        self.assertEqual(assay_graph.start_nodes, {self.protocol_node_dna, self.protocol_node_rna})

    def test_next_nodes(self):
        assay_graph = AssayGraph(measurement_type='genomic extraction', technology_type='nucleic acid extraction',
                                 nodes=self.nodes, links=self.links)
        self.assertEqual(assay_graph.next_nodes(self.protocol_node_rna), {
            self.mirna_node, self.mrna_node
        })
        self.assertEqual(assay_graph.next_nodes(self.protocol_node_dna), {self.dna_node})
        self.assertEqual(assay_graph.next_nodes(self.mrna_node), set())
        self.assertRaises(TypeError, assay_graph.next_nodes, 'this is not a node')
        self.assertRaises(ValueError, assay_graph.next_nodes, ProductNode(node_type=SAMPLE, size=10))

    def test_previous_nodes(self):
        assay_graph = AssayGraph(measurement_type='genomic extraction', technology_type='nucleic acid extraction',
                                 nodes=self.nodes, links=self.links)
        self.assertEqual(assay_graph.previous_nodes(self.mrna_node), {self.protocol_node_rna})
        self.assertEqual(assay_graph.previous_nodes(self.dna_node), {self.protocol_node_dna})
        self.assertEqual(assay_graph.previous_nodes(self.protocol_node_dna), set())
        self.assertRaises(TypeError, assay_graph.previous_nodes, 'this is not a node')
        self.assertRaises(ValueError, assay_graph.previous_nodes, ProductNode(node_type=SAMPLE, size=10))

    def test_previous_protocol_nodes(self):
        nmr_assay_graph = AssayGraph.generate_assay_plan_from_dict(nmr_assay_dict)
        extraction_node = next(node for node in nmr_assay_graph.nodes if node.name == 'extraction')
        nmr_nodes = list(filter(lambda node: node.name == 'nmr_spectroscopy', nmr_assay_graph.nodes))
        self.assertEqual(len(nmr_nodes), 8)
        for nmr_node in nmr_nodes:
            self.assertEqual(nmr_assay_graph.previous_protocol_nodes(nmr_node), {extraction_node})

    def test_as_networkx_graph(self):
        self.assay_graph.add_nodes(self.nodes)
        self.assay_graph.add_links(self.links)
        nx_graph = self.assay_graph.as_networkx_graph()
        self.assertIsInstance(nx_graph, nx.DiGraph)
        self.assertEqual(set(nx_graph.nodes), {
            node.id for node in self.assay_graph.nodes
        })
        self.assertEqual(nx_graph.edges, {
            (u.id, v.id) for u, v in self.assay_graph.links
        })

    def test_eq(self):
        nodes = [self.sample_node, self.protocol_node_rna, self.mrna_node, self.mirna_node]
        links = [(self.sample_node, self.protocol_node_rna), (self.protocol_node_rna, self.mrna_node),
                 (self.protocol_node_rna, self.mirna_node)]
        first_plan = AssayGraph(id_='assay-graph/00',
                                measurement_type='genomic extraction', technology_type='nucleic acid extraction')
        first_plan.add_nodes(nodes)
        first_plan.add_links(links)
        second_plan = AssayGraph(id_='assay-graph/00',
                                 measurement_type='genomic extraction', technology_type='nucleic acid extraction')
        second_plan.add_nodes(nodes[::-1])
        second_plan.add_links(links[::-1])
        self.assertEqual(first_plan.nodes, second_plan.nodes)
        self.assertEqual(first_plan.links, second_plan.links)
        self.assertEqual(first_plan, second_plan)

    def test_ne(self):
        nodes = [self.sample_node, self.protocol_node_rna, self.mrna_node, self.mirna_node]
        links = [(self.sample_node, self.protocol_node_rna), (self.protocol_node_rna, self.mrna_node)]
        first_plan = AssayGraph(id_='assay-graph/00',
                                measurement_type='genomic extraction', technology_type='nucleic acid extraction')
        first_plan.add_nodes(nodes)
        first_plan.add_links(links)
        second_plan = AssayGraph(id_='assay-graph/00',
                                 measurement_type='genomic extraction', technology_type='nucleic acid extraction')
        links.append((self.protocol_node_rna, self.mirna_node))
        second_plan.add_nodes(nodes)
        second_plan.add_links(links)
        self.assertNotEqual(first_plan, second_plan)

    def test_repr(self):
        """
        ensures that representation is unique and the same for equal AssayGraphs
        :return:
        """
        nodes = [self.protocol_node_rna, self.mrna_node, self.mirna_node]
        links = [(self.protocol_node_rna, self.mrna_node), (self.protocol_node_rna, self.mirna_node)]
        first_graph = AssayGraph(id_='assay-graph-01', measurement_type='genomic extraction',
                                 technology_type='nucleic acid extraction')
        first_graph.add_nodes(nodes)
        first_graph.add_links(links)
        second_graph = AssayGraph(id_='assay-graph-01', measurement_type='genomic extraction',
                                  technology_type='nucleic acid extraction')
        second_graph.add_nodes(nodes)
        second_graph.add_links(links[::-1])
        self.assertEqual(repr(first_graph), repr(second_graph))

    """
    def test_sample_nodes(self):
        self.assay_graph.graph_dict = self.graph_dict
        self.assertEqual(self.assay_graph.sample_nodes, {self.sample_node})
    """


class SampleAndAssayPlanTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.tissue_char = Characteristic(category='organism part', value='tissue')
        self.blood_char = Characteristic(category='organism part', value='blood')
        self.tissue_node = ProductNode(name='tissue', node_type=SAMPLE, size=2, characteristics=[self.tissue_char])
        self.blood_node = ProductNode(name='blood',
                                      node_type=SAMPLE, size=3, characteristics=[self.blood_char])
        self.genomic_assay_graph = AssayGraph(
            id_='assay-graph/00',
            measurement_type='genomic extraction',
            technology_type='nucleic acid extraction'
        )
        self.metabolomic_assay_graph = AssayGraph(
            id_='assay-graph/01',
            measurement_type='metabolomic analysis',
            technology_type='mass spectrometry'
        )

    def test_properties(self):
        plan = SampleAndAssayPlan()
        self.assertEqual(plan.assay_plan, set())
        self.assertEqual(plan.sample_plan, set())
        sample_plan = {self.tissue_node, self.blood_node}
        assay_plan = {self.genomic_assay_graph, self.metabolomic_assay_graph}
        plan.sample_plan = sample_plan
        plan.assay_plan = assay_plan
        self.assertEqual(plan.sample_plan, sample_plan)
        self.assertEqual(plan.assay_plan, assay_plan)
        self.assertEqual(plan.sample_to_assay_map, {})
        sample_to_assay_map = {
            self.tissue_node: {self.genomic_assay_graph, self.metabolomic_assay_graph},
            self.blood_node: {self.metabolomic_assay_graph}
        }
        plan.sample_to_assay_map = sample_to_assay_map
        self.assertEqual(plan.sample_to_assay_map, sample_to_assay_map)

    def test_eq_ne_repr(self):
        first_plan = SampleAndAssayPlan(name='first plan')

        sample_plan = {self.tissue_node, self.blood_node}
        assay_plan = {self.genomic_assay_graph, self.metabolomic_assay_graph}
        first_plan.sample_plan = sample_plan
        first_plan.assay_plan = assay_plan
        second_plan = SampleAndAssayPlan(name='second plan')
        second_plan.sample_plan = sample_plan
        second_plan.assay_plan = assay_plan
        self.assertNotEqual(first_plan, second_plan)
        self.assertNotEqual(repr(first_plan), repr(second_plan))
        second_plan.name = 'first plan'
        self.assertEqual(first_plan, second_plan)
        self.assertEqual(repr(first_plan), repr(second_plan))
        first_plan.sample_to_assay_map = {
            self.tissue_node: [self.genomic_assay_graph],
            self.blood_node: [self.metabolomic_assay_graph]
        }
        second_plan.sample_to_assay_map = {
            self.tissue_node: [self.genomic_assay_graph, self.metabolomic_assay_graph],
            self.blood_node: [self.metabolomic_assay_graph]
        }
        self.assertNotEqual(first_plan, second_plan)
        self.assertNotEqual(repr(first_plan), repr(second_plan))

    def test_add_element_to_map_success(self):
        plan = SampleAndAssayPlan()
        sample_plan = {self.tissue_node, self.blood_node}
        assay_plan = {self.genomic_assay_graph, self.metabolomic_assay_graph}
        plan.sample_plan = sample_plan
        plan.assay_plan = assay_plan
        plan.add_element_to_map(self.blood_node, self.genomic_assay_graph)
        self.assertEqual(plan.sample_to_assay_map, {
            self.blood_node: {self.genomic_assay_graph}
        })
        plan.add_element_to_map(self.tissue_node, self.genomic_assay_graph)
        self.assertEqual(plan.sample_to_assay_map, {
            self.blood_node: {self.genomic_assay_graph},
            self.tissue_node: {self.genomic_assay_graph}
        })
        plan.add_element_to_map(self.tissue_node, self.metabolomic_assay_graph)
        self.assertEqual(plan.sample_to_assay_map, {
            self.blood_node: {self.genomic_assay_graph},
            self.tissue_node: {self.metabolomic_assay_graph, self.genomic_assay_graph}
        })

    def test_add_element_to_map_raises(self):
        plan = SampleAndAssayPlan()
        with self.assertRaises(ValueError, msg='The sample has not been added to the plan yet') as ex_cm:
            plan.add_element_to_map(self.blood_node, self.genomic_assay_graph)
        self.assertEqual(ex_cm.exception.args[0], SampleAndAssayPlan.MISSING_SAMPLE_IN_PLAN)
        sample_plan = {self.tissue_node, self.blood_node}
        plan.sample_plan = sample_plan
        with self.assertRaises(ValueError, msg='The assay has not been added to the plan yet') as ex_cm:
            plan.add_element_to_map(self.blood_node, self.genomic_assay_graph)
        self.assertEqual(ex_cm.exception.args[0], SampleAndAssayPlan.MISSING_ASSAY_IN_PLAN)

    def test_from_sample_and_assay_plan_dict_no_validation(self):
        assay_list = [ms_assay_dict, nmr_assay_dict]
        smp_ass_plan = SampleAndAssayPlan.from_sample_and_assay_plan_dict(sample_list, *assay_list)
        # print([node.name for node in ms_assay_plan.nodes])
        self.assertEqual(len(smp_ass_plan.sample_plan), len(sample_list))
        self.assertEqual(len(smp_ass_plan.assay_plan), 2)
        ms_assay_graph = sorted(smp_ass_plan.assay_plan, key=lambda el: el.technology_type)[0]
        self.assertIsInstance(ms_assay_graph, AssayGraph)
        self.assertEqual(ms_assay_graph.measurement_type, ms_assay_dict['measurement_type'])
        self.assertEqual(ms_assay_graph.technology_type, ms_assay_dict['technology_type'])
        self.assertEqual(len(ms_assay_graph.nodes), 15)
        self.assertEqual(len(ms_assay_graph.links), 14)
        self.assertEqual(len(list(filter(lambda node: node.name == 'extraction', ms_assay_graph.nodes))), 1)
        self.assertEqual(len(list(filter(lambda node: node.name == 'extract', ms_assay_graph.nodes))), 2)
        self.assertEqual(len(list(filter(lambda node: node.name == 'labelling', ms_assay_graph.nodes))), 2)
        self.assertEqual(len(list(filter(lambda node: node.name == 'labelled extract', ms_assay_graph.nodes))), 2)
        self.assertEqual(len(list(filter(lambda node: node.name == 'mass spectrometry', ms_assay_graph.nodes))), 4)
        self.assertEqual(len(list(filter(lambda node: node.name == 'raw spectral data file',
                                         ms_assay_graph.nodes))), 4)
        self.assertEqual(len(smp_ass_plan.sample_to_assay_map.keys()), len(sample_list))
        for item in smp_ass_plan.sample_to_assay_map.values():
            self.assertIsInstance(item, set)
            self.assertEqual(len(item), len(assay_list))


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
        self.cell_washout_01 = StudyCell('ANOTHER WASHOUT', elements=(self.washout, ))
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
        self.sample_assay_plan = SampleAndAssayPlan()

    def test__init__(self):
        self.assertEqual(self.arm.name, TEST_STUDY_ARM_NAME_00)

    def test_add_item_to_arm__single_unit_cells_00(self):
        self.arm.add_item_to_arm_map(self.cell_screen, None)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 1, 'One mapping has been added to the arm')
        self.assertEqual(cells[0], self.cell_screen, 'The SCREEN cell has been added to the arm')
        self.assertEqual(plans[0], None, 'There is non sample plan for this specific cell')
        with self.assertRaises(ValueError, msg='Another cell containing a screen cannot be added to the '
                                               'StudyArm') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_screen_and_run_in, None)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.SCREEN_ERROR_MESSAGE)
        self.arm.add_item_to_arm_map(self.cell_run_in, None)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 2, 'One mapping has been added to the arm')
        self.assertEqual(cells[1], self.cell_run_in, 'The RUN-IN cell has been added to the arm')
        self.assertEqual(plans[1], None, 'There is non sample plan for this specific cell')

        with self.assertRaises(ValueError, msg='Another cell containing a screen cannot be added to the '
                                               'StudyArm') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_screen_and_run_in, None)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.SCREEN_ERROR_MESSAGE)

        with self.assertRaises(ValueError, msg='Another cell containing a run-in cannot be added to the '
                                               'StudyArm') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_other_run_in, None)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.RUN_IN_ERROR_MESSAGE)

        self.arm.add_item_to_arm_map(self.cell_single_treatment_00, self.sample_assay_plan)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 3, 'One mapping has been added to the arm')
        self.assertEqual(cells[2], self.cell_single_treatment_00, 'The 1st treatment cell has been added to the arm')
        self.assertEqual(plans[2], self.sample_assay_plan, 'There is non sample plan for this specific cell')

        with self.assertRaises(ValueError, msg='Another cell containing a screen cannot be added to the '
                                               'StudyArm') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_screen_and_run_in, None)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.SCREEN_ERROR_MESSAGE)

        with self.assertRaises(ValueError, msg='Another cell containing a run-in cannot be added to the '
                                               'StudyArm') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_other_run_in, None)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.RUN_IN_ERROR_MESSAGE)

        self.arm.add_item_to_arm_map(self.cell_washout_00, None)
        cells, plans = zip(*self.arm.arm_map.items())
        self.assertEqual(len(cells), 4, 'One mapping has been added to the arm')
        self.assertEqual(cells[3], self.cell_washout_00, 'The WASHOUT cell has been added to the arm')
        self.assertEqual(plans[3], None, 'There is non sample plan for this specific cell')

        with self.assertRaises(ValueError, msg='Another cell containing a WASHOUT cannot be added to the '
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

        with self.assertRaises(ValueError, msg='No more items can be added after a FOLLOW-UP') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_multi_elements, self.sample_assay_plan)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.COMPLETE_ARM_ERROR_MESSAGE)

    def test_add_item_to_arm__multi_unit_cells_00(self):
        self.arm.add_item_to_arm_map(self.cell_screen_and_run_in, None)
        with self.assertRaises(ValueError, msg='A cell beginning with a WASHOUT element cannot be added to a'
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
        with self.assertRaises(ValueError, msg='A cell beginning with a FOLLOW-UP element cannot be added to a'
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
        with self.assertRaises(ValueError, msg='A cell beginning with a FOLLOW-UP element cannot be added to '
                                                       'an empty arm.') as ex_cm:
            self.arm.add_item_to_arm_map(self.cell_follow_up, self.sample_assay_plan)
        self.assertEqual(ex_cm.exception.args[0], StudyArm.FOLLOW_UP_EMPTY_ARM_ERROR_MESSAGE)

    def test_source_type_property(self):
        self.assertIsInstance(self.arm.source_type, Characteristic)
        self.assertEqual(self.arm.source_type, DEFAULT_SOURCE_TYPE)
        self.arm.source_type = 'mouse'
        self.assertEqual(self.arm.source_type, 'mouse')
        source_type = Characteristic(
            category=OntologyAnnotation(
                term='Study Subject',
                term_source=default_ontology_source_reference,
                term_accession='http://purl.obolibrary.org/obo/NCIT_C41189'
            ),
            value=OntologyAnnotation(
                term='Rat',
                term_source=default_ontology_source_reference,
                term_accession='http://purl.obolibrary.org/obo/NCIT_C14266'
            )
        )
        self.arm.source_type = source_type
        self.assertEqual(self.arm.source_type, source_type)

    def test_source_type_property_fail(self):
        with self.assertRaises(AttributeError, msg='source_type can be only string or Characteristic') as ex_cm:
            self.arm.source_type = 128
        self.assertEqual(ex_cm.exception.args[0], 'The source_type property must be either a string or a '
                                                  'Characteristic. 128 was supplied.')

    def test_group_size_property(self):
        self.assertEqual(self.arm.group_size, 10)
        self.arm.group_size = 100
        self.assertEqual(self.arm.group_size, 100)

    def test_group_size_property_fail_00(self):
        with self.assertRaises(AttributeError,
                               msg='Only positive integers can be assigned to group_size') as ex_cm:
            self.arm.group_size = -5
        self.assertEqual(ex_cm.exception.args[0], 'group_size must be a positive integer; -5 provided')

    def test_arm_map_property_success_00(self):
        self.assertEqual(self.arm.arm_map, OrderedDict(), 'The ordered mapping StudyCell -> SampleAndAssayPlan '
                                                          'is empty.')
        ord_dict = OrderedDict([(self.cell_screen, None), (self.cell_run_in, None),
                                (self.cell_single_treatment_00, self.sample_assay_plan),
                                (self.cell_washout_00, None),
                                (self.cell_single_treatment_01, self.sample_assay_plan),
                                (self.cell_washout_01, None), (self.cell_follow_up, self.sample_assay_plan)
                                ])
        self.arm.arm_map = ord_dict
        self.assertEqual(self.arm.arm_map, ord_dict, 'The ordered mapping StudyCell -> SampleAndAssayPlan has been '
                                                     'correctly set for single-treatment cells.')

    def test_arm_map_property_success_01(self):
        self.assertEqual(self.arm.arm_map, OrderedDict(), 'The ordered mapping StudyCell -> SampleAndAssayPlan '
                                                          'is empty.')
        ord_dict = OrderedDict([(self.cell_screen, None),
                                (self.cell_multi_elements_padded, self.sample_assay_plan),
                                (self.cell_follow_up, self.sample_assay_plan)
                                ])
        self.arm.arm_map = ord_dict
        self.assertEqual(self.arm.arm_map, ord_dict, 'The ordered mapping StudyCell -> SampleAndAssayPlan has been '
                                                     'correctly set for single-treatment cells.')

    def test_arm_map_property_fail_wrong_type(self):
        with self.assertRaises(AttributeError, msg='An error is raised if an object of the wrong type is '
                                                   'provided to the assignment.') as ex_cm:
            self.arm.arm_map = ['wrong', 'object']
        self.assertEqual(ex_cm.exception.args[0], StudyArm.ARM_MAP_ASSIGNMENT_ERROR)

    def test_arm_map_property_fail_wrong_value_00(self):
        with self.assertRaises(AttributeError, msg='An error is raised if an object of the wrong value is '
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
        with self.assertRaises(AttributeError, msg='An error is raised if an object of the wrong value is '
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


class BaseStudyDesignTest(unittest.TestCase):

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
        self.cell_washout_01 = StudyCell('ANOTHER WASHOUT', elements=(self.washout,))
        self.cell_single_treatment_00 = StudyCell('SINGLE TREATMENT FIRST', elements=[self.first_treatment])
        self.cell_single_treatment_01 = StudyCell('SINGLE TREATMENT SECOND', elements=[self.second_treatment])
        self.cell_single_treatment_02 = StudyCell('SINGLE TREATMENT THIRD', elements=[self.third_treatment])
        self.cell_multi_elements = StudyCell('MULTI ELEMENTS',
                                             elements=[{self.first_treatment, self.second_treatment,
                                                        self.fourth_treatment}, self.washout, self.second_treatment])
        self.cell_multi_elements_padded = StudyCell('MULTI ELEMENTS PADDED',
                                                    elements=[self.first_treatment, self.washout, {
                                                        self.second_treatment,
                                                        self.fourth_treatment
                                                    }, self.washout, self.third_treatment, self.washout])
        self.cell_follow_up = StudyCell(FOLLOW_UP, elements=(self.follow_up,))
        self.cell_follow_up_01 = StudyCell('ANOTHER FOLLOW_UP', elements=(self.follow_up,))
        self.qc = QualityControl()
        self.ms_sample_assay_plan = SampleAndAssayPlan.from_sample_and_assay_plan_dict(sample_list, ms_assay_dict)
        self.nmr_sample_assay_plan = SampleAndAssayPlan.from_sample_and_assay_plan_dict(sample_list, nmr_assay_dict)
        self.first_arm = StudyArm(name=TEST_STUDY_ARM_NAME_00, group_size=10, arm_map=OrderedDict([
            (self.cell_screen, None), (self.cell_run_in, None),
            (self.cell_single_treatment_00, self.ms_sample_assay_plan),
            (self.cell_follow_up, self.ms_sample_assay_plan)
        ]))
        self.second_arm = StudyArm(name=TEST_STUDY_ARM_NAME_01, group_size=25, arm_map=OrderedDict([
            (self.cell_screen, None), (self.cell_run_in, None),
            (self.cell_multi_elements, self.ms_sample_assay_plan),
            (self.cell_follow_up, self.ms_sample_assay_plan)
        ]))
        self.third_arm = StudyArm(name=TEST_STUDY_ARM_NAME_02, group_size=20, arm_map=OrderedDict([
            (self.cell_screen, None), (self.cell_run_in, None),
            (self.cell_multi_elements_padded, self.ms_sample_assay_plan),
            (self.cell_follow_up, self.ms_sample_assay_plan)
        ]))
        self.third_arm_no_run_in = StudyArm(name=TEST_STUDY_ARM_NAME_02, group_size=20, arm_map=OrderedDict([
            (self.cell_screen, None),
            (self.cell_multi_elements_padded, self.ms_sample_assay_plan),
            (self.cell_follow_up, self.ms_sample_assay_plan)
        ]))
        self.arm_same_name_as_third = StudyArm(name=TEST_STUDY_ARM_NAME_02, group_size=10, arm_map=OrderedDict([
            (self.cell_screen, None), (self.cell_run_in, None),
            (self.cell_single_treatment_01, self.ms_sample_assay_plan),
            (self.cell_follow_up, self.ms_sample_assay_plan)
        ]))
        # Sample QC (for mass spectroscopy and other)
        self.pre_run_sample_type = ProductNode(
            id_='pre/00', node_type=SAMPLE, name='water', size=5, characteristics=(
                Characteristic(category='dilution', value=10, unit='mg/L'),
            )
        )
        self.post_run_sample_type = ProductNode(
            id_='post/00', node_type=SAMPLE, name='ethanol', size=5, characteristics=(
                Characteristic(category='dilution', value=1000, unit='mg/L'),
                Characteristic(category='dilution', value=100, unit='mg/L'),
                Characteristic(category='dilution', value=10, unit='mg/L'),
                Characteristic(category='dilution', value=1, unit='mg/L'),
                Characteristic(category='dilution', value=0.1, unit='mg/L')
            ))
        self.dummy_sample_type = ProductNode(id_='dummy/01', node_type=SAMPLE, name='dummy')
        self.more_dummy_sample_type = ProductNode(id_='dummy/02', node_type=SAMPLE, name='more dummy')
        self.interspersed_sample_types = [(self.dummy_sample_type, 20)]
        self.qc = QualityControl(
            interspersed_sample_type=self.interspersed_sample_types,
            pre_run_sample_type=self.pre_run_sample_type,
            post_run_sample_type=self.post_run_sample_type
        )
        self.study_design = StudyDesign()


class StudyDesignTest(BaseStudyDesignTest):

    def setUp(self):
        return super(StudyDesignTest, self).setUp()

    def test_init(self):
        self.assertIsInstance(getattr(self.study_design, '_StudyDesign__name', None), str,
                              'The __name has been initialized as a string')
        self.assertEqual(getattr(self.study_design, '_StudyDesign__study_arms', None), set(),
                         'An empty set has been initialized for __study_arms')
        self.assertEqual(self.study_design.source_type, DEFAULT_SOURCE_TYPE)

    def test_name_property(self):
        self.assertEqual(self.study_design.name, 'Study Design')
        self.study_design.name = TEST_STUDY_DESIGN_NAME
        self.assertEqual(self.study_design.name, TEST_STUDY_DESIGN_NAME)
        with self.assertRaises(AttributeError, msg='An integer cannot be assigned as StudyDesign name') as ex_cm:
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
        with self.assertRaises(ValueError,
                               msg='An integer cannot be assigned as StudyDesign name') as ex_cm:
            self.study_design.add_study_arm(self.arm_same_name_as_third)
        self.assertEqual(ex_cm.exception.args[0], StudyDesign.ADD_STUDY_ARM_NAME_ALREADY_PRESENT_ERROR)
        self.assertEqual(self.study_design.study_arms, [self.second_arm, self.third_arm])
        self.study_design.add_study_arm(self.first_arm)
        self.assertEqual(self.study_design.study_arms, [self.second_arm, self.first_arm, self.third_arm])

    def test_add_study_arm_02(self):
        with self.assertRaises(TypeError,
                               msg='A Treatment cannot be added to a StudyDesign, only StudyArms') as ex_cm:
            self.study_design.add_study_arm(self.second_treatment)
        self.assertIn(StudyDesign.ADD_STUDY_ARM_PARAMETER_TYPE_ERROR, ex_cm.exception.args[0])

    def test_treatments_property_00(self):
        self.study_design.study_arms = [self.first_arm, self.second_arm]
        treatment_set = self.study_design.treatments
        self.assertEqual(treatment_set, {self.first_treatment, self.second_treatment, self.fourth_treatment})

    def test_treatments_property_01(self):
        self.study_design.study_arms = [self.first_arm, self.third_arm]
        treatment_set = self.study_design.treatments
        self.assertEqual(treatment_set, {self.first_treatment, self.second_treatment,
                                         self.third_treatment, self.fourth_treatment})

    def test_get_epoch_ith_index(self):
        self.study_design.study_arms = [self.first_arm, self.second_arm, self.third_arm]
        for i in range(4):
            epoch_cells = self.study_design.get_epoch(i)
            self.assertEqual(type(epoch_cells), list)
            self.assertEqual(len(epoch_cells), len(self.study_design.study_arms))
            self.assertEqual(epoch_cells[0], self.second_arm.cells[i])
            self.assertEqual(epoch_cells[1], self.first_arm.cells[i])
            self.assertEqual(epoch_cells[2], self.third_arm.cells[i])

    def test_get_epoch_4th_index_shorter_arm(self):
        self.study_design.study_arms = [self.first_arm, self.second_arm, self.third_arm_no_run_in]
        epoch_cells = self.study_design.get_epoch(3)
        self.assertEqual(type(epoch_cells), list)
        self.assertEqual(len(epoch_cells), len(self.study_design.study_arms))
        self.assertEqual(epoch_cells[0], self.second_arm.cells[3])
        self.assertEqual(epoch_cells[1], self.first_arm.cells[3])
        self.assertEqual(epoch_cells[2], None)

    def test_get_epoch_out_of_bounds_index(self):
        self.study_design.study_arms = [self.first_arm, self.second_arm, self.third_arm]
        with self.assertRaises(IndexError, msg='An index error is raised if the epoch is out of bounds '
                                               'for all the StudyArms.') as ex_cm:
            epoch_cells = self.study_design.get_epoch(4)
        self.assertEqual(ex_cm.exception.args[0], StudyDesign.GET_EPOCH_INDEX_OUT_OR_BOUND_ERROR)

    # FIXME still failing - sort this out
    """
    def test_generate_isa_study_00(self):
        with open(os.path.join(os.path.dirname(__file__), '..', 'isatools', 'resources', 'config', 'yaml',
                               'study-creator-config.yaml')) as yaml_file:
            config = yaml.load(yaml_file)
        study_config = config['study']
        print('study_config: {0}'.format(study_config))
        self.study_design.study_arms = [self.first_arm, self.second_arm, self.third_arm]
        study = self.study_design.generate_isa_study()
        self.assertIsInstance(study, Study)
        self.assertEqual(study.filename, study_config['filename'])
        self.assertEqual(len(study.sources), self.first_arm.group_size + self.second_arm.group_size +
                         self.third_arm.group_size)
        print('Sources: {0}'.format(study.sources))
    """

    def test__generate_isa_elements_from_node(self):
        assay_graph = AssayGraph.generate_assay_plan_from_dict(nmr_assay_dict)
        node = next(iter(assay_graph.start_nodes))
        processes, other_materials, data_files, next_item = StudyDesign._generate_isa_elements_from_node(
            node, assay_graph
        )
        # one extraction protocol + 16 NRM protocols (4 combinations, 2 replicates)
        print('Processes are {0}'.format([process.executes_protocol.name for process in processes]))
        extraction_processes = [process for process in processes if process.executes_protocol.name == 'extraction']
        self.assertEqual(len(extraction_processes), 1)
        nmr_processes = [process for process in processes if process.executes_protocol.name == 'nmr_spectroscopy']
        self.assertEqual(len(nmr_processes), 8*2)
        self.assertEqual(len(processes), 1+8*2)
        self.assertEqual(len(other_materials), 2)
        self.assertEqual(len(data_files), 8*2)      # 16 raw data files
        for nmr_process in nmr_processes:
            self.assertIsInstance(nmr_process, Process)
            print('expected previous process: {0}'.format(extraction_processes[0]))
            print('actual previous process: {0}'.format(nmr_process.prev_process))
            self.assertEqual(nmr_process.prev_process, extraction_processes[0])
            self.assertEqual(nmr_process.next_process, None)
        self.assertEqual(extraction_processes[0].prev_process, None)
        self.assertEqual(extraction_processes[0].next_process, nmr_processes[-1])
        # self.assertIsInstance(next_item, DataFile)

    def test_generate_isa_study_single_arm_single_cell_elements(self):
        with open(os.path.join(os.path.dirname(__file__), '..', 'isatools', 'resources', 'config', 'yaml',
                               'study-creator-config.yaml')) as yaml_file:
            config = yaml.load(yaml_file)
        study_config = config['study']
        single_arm = StudyArm(name=TEST_STUDY_ARM_NAME_00, group_size=10, arm_map=OrderedDict([
            (self.cell_screen, None), (self.cell_run_in, None),
            (self.cell_single_treatment_00, self.nmr_sample_assay_plan),
            (self.cell_follow_up, self.nmr_sample_assay_plan)
        ]))
        study_design = StudyDesign(study_arms=(single_arm,))
        study = study_design.generate_isa_study()
        self.assertIsInstance(study, Study)
        self.assertEqual(study.filename, study_config['filename'])
        self.assertEqual(len(study.sources), single_arm.group_size)
        for source in study.sources:
            self.assertEqual(len(source.characteristics), 1)
            self.assertEqual(source.characteristics[0], DEFAULT_SOURCE_TYPE)

        expected_num_of_samples_per_plan = reduce(lambda acc_value, sample_node: acc_value+sample_node.size,
                                                  self.nmr_sample_assay_plan.sample_plan, 0) * single_arm.group_size
        expected_num_of_samples = expected_num_of_samples_per_plan * len([
            a_plan for a_plan in single_arm.arm_map.values() if a_plan is not None
        ])
        print('Expected number of samples is: {0}'.format(expected_num_of_samples))
        self.assertEqual(len(study.samples), expected_num_of_samples)
        self.assertEqual(len(study.assays), 2)
        treatment_assay = next(iter(study.assays))
        self.assertIsInstance(treatment_assay, Assay)
        # self.assertEqual(len(treatment_assay.samples), expected_num_of_samples_per_plan)
        self.assertEqual(treatment_assay.measurement_type, nmr_assay_dict['measurement_type'])
        self.assertEqual(treatment_assay.technology_type, nmr_assay_dict['technology_type'])
        # pdb.set_trace()
        extraction_processes = [process for process in treatment_assay.process_sequence
                                if process.executes_protocol.name == 'extraction']
        nmr_processes = [process for process in treatment_assay.process_sequence
                         if process.executes_protocol.name == 'nmr_spectroscopy']
        self.assertEqual(len(extraction_processes), expected_num_of_samples_per_plan)
        self.assertEqual(len(nmr_processes), 8*nmr_assay_dict['nmr_spectroscopy']['#replicates']
                         * expected_num_of_samples_per_plan)
        self.assertEqual(len(treatment_assay.process_sequence), (8*nmr_assay_dict['nmr_spectroscopy']['#replicates']
                                                                 + 1)*expected_num_of_samples_per_plan)
        for ix, process in enumerate(nmr_processes):
            self.assertIsInstance(process, Process)
            # 1 extraction protocol feeds into 16 nmr processes
            self.assertEqual(process.prev_process, extraction_processes[ix//(8*2)])
            # 1 extract ends up into 8 different nmr protocol runs (i.e. processes)
            self.assertEqual(process.inputs, [treatment_assay.other_material[ix//8]])
            self.assertEqual(process.outputs, [treatment_assay.data_files[ix]])
        log.debug('Process sequence: {0}'.format([
            (process.name, getattr(process.prev_process, 'name', None),
             getattr(process.next_process, 'name', None)) for process in treatment_assay.process_sequence
        ]))
        log.debug('NMR assay graph: {0}'.format([(getattr(el, 'name', None), type(el))
                                                 for el in treatment_assay.graph.nodes()]))

    def test_generate_isa_study_single_arm_single_cell_elements_split_assay_by_sample_type(self):
        with open(os.path.join(os.path.dirname(__file__), '..', 'isatools', 'resources', 'config', 'yaml',
                               'study-creator-config.yaml')) as yaml_file:
            config = yaml.load(yaml_file)
        # study_config = config['study']
        single_arm = StudyArm(name=TEST_STUDY_ARM_NAME_00, group_size=10, arm_map=OrderedDict([
            (self.cell_screen, None), (self.cell_run_in, None),
            (self.cell_single_treatment_00, self.nmr_sample_assay_plan),
            (self.cell_follow_up, self.nmr_sample_assay_plan)
        ]))
        study_design = StudyDesign(study_arms=(single_arm,))
        study = study_design.generate_isa_study(split_assays_by_sample_type=True)
        self.assertEqual(len(study.assays), 6)
        treatment_assay_st0, treatment_assay_st1, treatment_assay_st2 = study.assays[0:3]
        self.assertIsInstance(treatment_assay_st0, Assay)
        self.assertEqual(treatment_assay_st0.measurement_type, nmr_assay_dict['measurement_type'])
        self.assertEqual(treatment_assay_st0.technology_type, nmr_assay_dict['technology_type'])
        extraction_processes = [process for process in treatment_assay_st0.process_sequence
                                if process.executes_protocol.name == 'extraction']
        nmr_processes = [process for process in treatment_assay_st0.process_sequence
                         if process.executes_protocol.name == 'nmr_spectroscopy']
        expected_num_of_samples_per_plan = reduce(lambda acc_value, sample_node: acc_value+sample_node.size,
                                                  self.nmr_sample_assay_plan.sample_plan, 0) * single_arm.group_size
        expected_num_of_samples_first = sample_list[0]['size'] * single_arm.group_size
        self.assertEqual(len(extraction_processes), expected_num_of_samples_first)
        self.assertEqual(len(nmr_processes), 8 * 2 * expected_num_of_samples_first)
        self.assertEqual(len(treatment_assay_st0.process_sequence), (8 * 2 + 1) * expected_num_of_samples_first)

    def test_generate_isa_study_two_arms_single_cell_elements(self):
        first_arm = StudyArm(name=TEST_STUDY_ARM_NAME_00, group_size=20, arm_map=OrderedDict([
            (self.cell_screen, None), (self.cell_run_in, None),
            (self.cell_single_treatment_00, self.ms_sample_assay_plan),
            (self.cell_follow_up, self.nmr_sample_assay_plan)
        ]))
        second_arm = StudyArm(name=TEST_STUDY_ARM_NAME_01, group_size=10, arm_map=OrderedDict([
            (self.cell_screen, None), (self.cell_run_in, None),
            (self.cell_single_treatment_01, self.nmr_sample_assay_plan),
            (self.cell_follow_up_01, self.nmr_sample_assay_plan)
        ]))
        study_design = StudyDesign(study_arms=(first_arm, second_arm))
        study = study_design.generate_isa_study()
        self.assertEqual(len(study.assays), 4)
        expected_num_of_samples_nmr_plan_first_arm = reduce(
            lambda acc_value, sample_node: acc_value + sample_node.size,
            self.nmr_sample_assay_plan.sample_plan, 0) * first_arm.group_size
        expected_num_of_samples_ms_plan_first_arm = reduce(
            lambda acc_value, sample_node: acc_value + sample_node.size,
            self.ms_sample_assay_plan.sample_plan, 0) * first_arm.group_size
        expected_num_of_samples_nmr_plan_second_arm = reduce(
            lambda acc_value, sample_node: acc_value + sample_node.size,
            self.nmr_sample_assay_plan.sample_plan, 0) * second_arm.group_size
        expected_num_of_samples_tot = 2 * expected_num_of_samples_nmr_plan_second_arm + \
            expected_num_of_samples_ms_plan_first_arm + expected_num_of_samples_nmr_plan_first_arm
        self.assertEqual(len(study.samples), expected_num_of_samples_tot)
        ms_assay = next(assay for assay in study.assays if assay.technology_type == ms_assay_dict['technology_type'])
        # print('MS Assay is: {0}'.format(ms_assay))
        self.assertIsNotNone(ms_assay)
        self.assertIsInstance(ms_assay, Assay)
        # self.assertEqual(len(ms_assay.samples), expected_num_of_samples_ms_plan_first_arm)
        ms_processes = [process for process in ms_assay.process_sequence
                        if process.executes_protocol.name == 'mass spectrometry']
        self.assertEqual(len(ms_processes), 2 * 2 * 2 * 2 * expected_num_of_samples_ms_plan_first_arm)


class QualityControlServiceTest(BaseStudyDesignTest):

    def setUp(self):
        return super(QualityControlServiceTest, self).setUp()

    def test_expansion_of_single_mass_spectrometry_assay(self):
        """
        ms_assay_graph = next(ag for ag in self.ms_sample_assay_plan.assay_plan
                              if ag.technology_type == ms_assay_dict['technology_type'])
        self.assertIsInstance(ms_assay_graph, AssayGraph)
        ms_assay_graph.quality_control = self.qc
        print('MS assay graph start nodes are: {0}'.format(ms_assay_graph.start_nodes))
        """
        ms_sample_assay_plan = SampleAndAssayPlan.from_sample_and_assay_plan_dict(
            sample_list, ms_assay_dict, quality_controls=[self.qc]
        )
        # print(self.ms_sample_assay_plan.assay_plan)
        first_arm = StudyArm(name=TEST_STUDY_ARM_NAME_00, group_size=20, arm_map=OrderedDict([
            (self.cell_screen, None), (self.cell_run_in, None),
            (self.cell_single_treatment_00, ms_sample_assay_plan),
            (self.cell_follow_up, self.nmr_sample_assay_plan)
        ]))
        second_arm = StudyArm(name=TEST_STUDY_ARM_NAME_01, group_size=10, arm_map=OrderedDict([
            (self.cell_screen, None), (self.cell_run_in, None),
            (self.cell_single_treatment_01, self.nmr_sample_assay_plan),
            (self.cell_follow_up_01, self.nmr_sample_assay_plan)
        ]))
        study_design = StudyDesign(study_arms=(first_arm, second_arm))
        study_no_qc = study_design.generate_isa_study()
        for assay in study_no_qc.assays:
            print('Assay is: {0}'.format(assay))
        ms_assay_no_qc = next(assay for assay in study_no_qc.assays
                              if assay.technology_type == ms_assay_dict['technology_type'])
        expected_num_of_samples_ms_plan_first_arm = reduce(
            lambda acc_value, sample_node: acc_value + sample_node.size,
            ms_sample_assay_plan.sample_plan, 0) * first_arm.group_size
        ms_processes = [process for process in ms_assay_no_qc.process_sequence
                        if process.executes_protocol.name == 'mass spectrometry']
        self.assertEqual(len(ms_processes), 2 * 2 * 2 * 2 * expected_num_of_samples_ms_plan_first_arm)
        # print('MS Assay no QC: {0}'.format(ms_assay_no_qc))
        study_with_qc = QualityControlService.augment_study(study_no_qc, study_design)
        self.assertIsInstance(study_with_qc, Study)
        self.assertIsNot(study_no_qc, study_with_qc)
        ms_assay_no_qc = next(assay for assay in study_no_qc.assays
                              if assay.technology_type == ms_assay_dict['technology_type'])
        ms_assay_with_qc = next(assay for assay in study_with_qc.assays
                                if assay.technology_type == ms_assay_dict['technology_type'])
        self.assertIsInstance(ms_assay_no_qc, Assay)
        self.assertIsInstance(ms_assay_with_qc, Assay)
        self.assertNotEqual(ms_assay_with_qc, ms_assay_no_qc)
        """
        ms_processes = [process for process in ms_assay_with_qc.process_sequence
                        if process.executes_protocol.name == 'mass spectrometry']
        qc_samples_size = self.qc.pre_run_sample_type.size + self.qc.post_run_sample_type.size + \
            expected_num_of_samples_ms_plan_first_arm // self.interspersed_sample_types[0][1]
        print('expected qc_samples_size: {0}'.format(qc_samples_size))
        self.assertEqual(len(ms_processes), 2 * 2 * 2 * 2 *
                         (expected_num_of_samples_ms_plan_first_arm + qc_samples_size))
        """


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
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='cocaine'),
                FactorValue(factor_name=intensity, value='high'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='cocaine'),
                FactorValue(factor_name=intensity, value='high'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='cocaine'),
                FactorValue(factor_name=intensity, value='low'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='cocaine'),
                FactorValue(factor_name=intensity, value='low'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='cocaine'),
                FactorValue(factor_name=intensity, value='medium'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='cocaine'),
                FactorValue(factor_name=intensity, value='medium'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='crack'),
                FactorValue(factor_name=intensity, value='high'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='crack'),
                FactorValue(factor_name=intensity, value='high'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='crack'),
                FactorValue(factor_name=intensity, value='low'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='crack'),
                FactorValue(factor_name=intensity, value='low'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='crack'),
                FactorValue(factor_name=intensity, value='medium'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='crack'),
                FactorValue(factor_name=intensity, value='medium'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='aether'),
                FactorValue(factor_name=intensity, value='high'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='aether'),
                FactorValue(factor_name=intensity, value='high'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='aether'),
                FactorValue(factor_name=intensity, value='low'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='aether'),
                FactorValue(factor_name=intensity, value='low'),
                FactorValue(factor_name=duration, value='short')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
                FactorValue(factor_name=agent, value='aether'),
                FactorValue(factor_name=intensity, value='medium'),
                FactorValue(factor_name=duration, value='long')
            )),
            Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
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

"""


class StudyDesignFactoryTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.factory = StudyDesignFactory()
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
        self.treatments = [self.first_treatment, self.second_treatment, self.third_treatment, self.fourth_treatment]
        self.sample_assay_plan = SampleAndAssayPlan()
        self.sample_assay_plan_list = [SampleAndAssayPlan(), SampleAndAssayPlan(), SampleAndAssayPlan(),
                                       SampleAndAssayPlan()]

    """
    def test_property_treatments(self):
        self.assertEqual(self.factory.treatments, None)

        self.factory.treatments = self.treatments
        self.assertEqual(self.factory.treatments, self.treatments)

    def test_property_sample_assay_plan(self):
        self.assertEqual(self.factory.sample_assay_plans, None)
        self.factory.sample_assay_plans = self.sample_assay_plan
        self.assertEqual(self.factory.sample_assay_plans, self.sample_assay_plan)
        self.factory.sample_assay_plans = self.sample_assay_plan_list
        self.assertEqual(self.factory.sample_assay_plans, self.sample_assay_plan_list)
    """

    def test_compute_crossover_design_2_treatments(self):
        treatments_map = [(self.first_treatment, self.sample_assay_plan),
                          (self.second_treatment, self.sample_assay_plan)]
        crossover_design = self.factory.compute_crossover_design(
            treatments_map=treatments_map,
            group_sizes = 10,
            screen_map=(self.screen, None),
            washout_map=(self.washout, None),
            follow_up_map=(self.follow_up, self.sample_assay_plan)
        )
        self.assertIsInstance(crossover_design, StudyDesign)
        self.assertEqual(len(crossover_design.study_arms), len(treatments_map))
        self.assertEqual(crossover_design.study_arms[0],
                         StudyArm(name='ARM_00', group_size=10, arm_map=OrderedDict(
                             [
                                 [StudyCell('ARM_00_CELL_00', elements=(self.screen,)), None],
                                 [StudyCell('ARM_00_CELL_01', elements=(self.first_treatment,)), self.sample_assay_plan],
                                 [StudyCell('ARM_00_CELL_02', elements=(self.washout,)), None],
                                 [StudyCell('ARM_00_CELL_03', elements=(self.second_treatment,)), self.sample_assay_plan],
                                 [StudyCell('ARM_00_CELL_04', elements=(self.follow_up,)), self.sample_assay_plan]
                             ]
                         )))
        self.assertEqual(crossover_design.study_arms[1],
                         StudyArm(name='ARM_01', group_size=10, arm_map=OrderedDict(
                             [
                                 [StudyCell('ARM_01_CELL_00', elements=(self.screen,)), None],
                                 [StudyCell('ARM_01_CELL_01', elements=(self.second_treatment,)), self.sample_assay_plan],
                                 [StudyCell('ARM_01_CELL_02', elements=(self.washout,)), None],
                                 [StudyCell('ARM_01_CELL_03', elements=(self.first_treatment,)), self.sample_assay_plan],
                                 [StudyCell('ARM_01_CELL_04', elements=(self.follow_up,)), self.sample_assay_plan]
                             ]
                         )))

    def test_compute_crossover_design_3_treatments(self):
        treatments_map = [(self.first_treatment, self.sample_assay_plan),
                          (self.second_treatment, self.sample_assay_plan),
                          (self.third_treatment, self.sample_assay_plan)]
        crossover_design = self.factory.compute_crossover_design(
            treatments_map=treatments_map,
            group_sizes=(10, 15, 12, 15, 12, 20),
            screen_map=(self.screen, None),
            run_in_map=(self.run_in, None),
            washout_map=(self.washout, None),
            follow_up_map=(self.follow_up, self.sample_assay_plan)
        )
        self.assertEqual(len(crossover_design.study_arms), 6) # three treatments means six permutations
        self.assertEqual(crossover_design.study_arms[0],
                         StudyArm(name='ARM_00', group_size=10, arm_map=OrderedDict(
                             [
                                 [StudyCell('ARM_00_CELL_00', elements=(self.screen,)), None],
                                 [StudyCell('ARM_00_CELL_01', elements=(self.run_in,)), None],
                                 [StudyCell('ARM_00_CELL_02', elements=(self.first_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_00_CELL_03', elements=(self.washout,)), None],
                                 [StudyCell('ARM_00_CELL_04', elements=(self.second_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_00_CELL_05', elements=(self.washout,)), None],
                                 [StudyCell('ARM_00_CELL_06', elements=(self.third_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_00_CELL_07', elements=(self.follow_up,)), self.sample_assay_plan]
                             ]
                         )))
        self.assertEqual(crossover_design.study_arms[1],
                         StudyArm(name='ARM_01', group_size=15, arm_map=OrderedDict(
                             [
                                 [StudyCell('ARM_01_CELL_00', elements=(self.screen,)), None],
                                 [StudyCell('ARM_01_CELL_01', elements=(self.run_in,)), None],
                                 [StudyCell('ARM_01_CELL_02', elements=(self.first_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_01_CELL_03', elements=(self.washout,)), None],
                                 [StudyCell('ARM_01_CELL_04', elements=(self.third_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_01_CELL_05', elements=(self.washout,)), None],
                                 [StudyCell('ARM_01_CELL_06', elements=(self.second_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_01_CELL_07', elements=(self.follow_up,)), self.sample_assay_plan]
                             ]
                         )))
        self.assertEqual(crossover_design.study_arms[2],
                         StudyArm(name='ARM_02', group_size=12, arm_map=OrderedDict(
                             [
                                 [StudyCell('ARM_02_CELL_00', elements=(self.screen,)), None],
                                 [StudyCell('ARM_02_CELL_01', elements=(self.run_in,)), None],
                                 [StudyCell('ARM_02_CELL_02', elements=(self.second_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_02_CELL_03', elements=(self.washout,)), None],
                                 [StudyCell('ARM_02_CELL_04', elements=(self.first_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_02_CELL_05', elements=(self.washout,)), None],
                                 [StudyCell('ARM_02_CELL_06', elements=(self.third_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_02_CELL_07', elements=(self.follow_up,)), self.sample_assay_plan]
                             ]
                         )))

    def test_compute_crossover_design_raises_treatment_map_error(self):
        treatments_map = [(self.first_treatment, self.second_treatment)]
        with self.assertRaises(TypeError, msg='The treatment map is malformed') as ex_cm:
            StudyDesignFactory.compute_crossover_design(treatments_map, 10)
        self.assertEqual(ex_cm.exception.args[0], StudyDesignFactory.TREATMENT_MAP_ERROR)

    def test_compute_crossover_design_raises_group_sizes_error(self):
        treatments_map = [(self.first_treatment, self.sample_assay_plan),
                          (self.second_treatment, self.sample_assay_plan),
                          (self.third_treatment, self.sample_assay_plan)]
        with self.assertRaises(TypeError, msg='The group_sizes list has the wrong length') as ex_cm:
            StudyDesignFactory.compute_crossover_design(treatments_map, [10, 12, 19])
        self.assertEqual(ex_cm.exception.args[0], StudyDesignFactory.GROUP_SIZES_ERROR)

    def test_compute_parallel_design_three_treatments(self):
        treatments_map = [(self.first_treatment, self.sample_assay_plan),
                          (self.second_treatment, self.sample_assay_plan),
                          (self.third_treatment, self.sample_assay_plan)]
        parallel_design = StudyDesignFactory.compute_parallel_design(treatments_map,
                                                                     group_sizes=[10, 15, 14],
                                                                     screen_map=(self.screen, None),
                                                                     run_in_map=(self.run_in, None),
                                                                     follow_up_map=(self.follow_up,
                                                                                    self.sample_assay_plan)
                                                                     )
        self.assertEqual(len(parallel_design.study_arms), 3)
        self.assertEqual(parallel_design.study_arms[0],
                         StudyArm(name='ARM_00', group_size=10, arm_map=OrderedDict(
                             [
                                 [StudyCell('ARM_00_CELL_00', elements=(self.screen,)), None],
                                 [StudyCell('ARM_00_CELL_01', elements=(self.run_in,)), None],
                                 [StudyCell('ARM_00_CELL_02', elements=(self.first_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_00_CELL_03', elements=(self.follow_up,)), self.sample_assay_plan]
                             ]
                         )))
        self.assertEqual(parallel_design.study_arms[1],
                         StudyArm(name='ARM_01', group_size=15, arm_map=OrderedDict(
                             [
                                 [StudyCell('ARM_01_CELL_00', elements=(self.screen,)), None],
                                 [StudyCell('ARM_01_CELL_01', elements=(self.run_in,)), None],
                                 [StudyCell('ARM_01_CELL_02', elements=(self.second_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_01_CELL_03', elements=(self.follow_up,)), self.sample_assay_plan]
                             ]
                         )))
        self.assertEqual(parallel_design.study_arms[2],
                         StudyArm(name='ARM_02', group_size=14, arm_map=OrderedDict(
                             [
                                 [StudyCell('ARM_02_CELL_00', elements=(self.screen,)), None],
                                 [StudyCell('ARM_02_CELL_01', elements=(self.run_in,)), None],
                                 [StudyCell('ARM_02_CELL_02', elements=(self.third_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_02_CELL_03', elements=(self.follow_up,)), self.sample_assay_plan]
                             ]
                         )))

    def test_compute_parallel_design_group_sizes_error(self):
        treatments_map = [(self.first_treatment, self.sample_assay_plan),
                          (self.second_treatment, self.sample_assay_plan),
                          (self.third_treatment, self.sample_assay_plan)]
        with self.assertRaises(TypeError, msg='The group_sizes list has the wrong length') as ex_cm:
            parallel_design = StudyDesignFactory.compute_parallel_design(treatments_map,
                                                                           group_sizes=[10, 12])
        self.assertEqual(ex_cm.exception.args[0], StudyDesignFactory.GROUP_SIZES_ERROR)

    def test_compute_single_arm_design_tree_treatments(self):
        treatments_map =  [(self.second_treatment, self.sample_assay_plan),
                          (self.fourth_treatment, self.sample_assay_plan),
                          (self.third_treatment, self.sample_assay_plan)]
        parallel_design = StudyDesignFactory.compute_single_arm_design(treatments_map,
                                                                       group_size=19,
                                                                       screen_map=(self.screen, None),
                                                                       run_in_map=(self.run_in, None),
                                                                       washout_map=(self.washout, None),
                                                                       follow_up_map=(self.follow_up,
                                                                                      self.sample_assay_plan)
                                                                       )
        self.assertEqual(len(parallel_design.study_arms), 1)
        self.assertEqual(parallel_design.study_arms[0],
                         StudyArm(name='ARM_00', group_size=19, arm_map=OrderedDict(
                             [
                                 [StudyCell('ARM_00_CELL_00', elements=(self.screen,)), None],
                                 [StudyCell('ARM_00_CELL_01', elements=(self.run_in,)), None],
                                 [StudyCell('ARM_00_CELL_02', elements=(self.second_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_00_CELL_03', elements=(self.washout,)), None],
                                 [StudyCell('ARM_00_CELL_04', elements=(self.fourth_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_00_CELL_05', elements=(self.washout,)), None],
                                 [StudyCell('ARM_00_CELL_06', elements=(self.third_treatment,)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_00_CELL_07', elements=(self.follow_up,)), self.sample_assay_plan]
                             ]
                         )))

    def test_compute_single_arm_design_raises_treatment_map_error(self):
        treatments_map = [(self.first_treatment, self.second_treatment)]
        with self.assertRaises(TypeError, msg='The treatment map is malformed') as ex_cm:
            StudyDesignFactory.compute_single_arm_design(treatments_map, group_size=12)
        self.assertEqual(ex_cm.exception.args[0], StudyDesignFactory.TREATMENT_MAP_ERROR)

    def test_compute_single_arm_design_group_sizes_error(self):
        treatments_map = [(self.first_treatment, self.sample_assay_plan),
                          (self.second_treatment, self.sample_assay_plan),
                          (self.third_treatment, self.sample_assay_plan)]
        with self.assertRaises(TypeError, msg='The group_sizes list has the wrong length') as ex_cm:
            single_arm_design = StudyDesignFactory.compute_single_arm_design(treatments_map,
                                                                             group_size=[10, 12])
        self.assertEqual(ex_cm.exception.args[0], StudyDesignFactory.GROUP_SIZES_ERROR)

    def test_compute_concomitant_treatment_design_three_treatments(self):
        treatments = [self.first_treatment, self.second_treatment, self.fourth_treatment]
        concomitant_treatment_design = StudyDesignFactory.compute_concomitant_treatments_design(
            treatments, self.sample_assay_plan, group_size=30, follow_up_map=(self.follow_up, self.sample_assay_plan)
        )
        self.assertEqual(len(concomitant_treatment_design.study_arms), 1)
        self.assertEqual(list(concomitant_treatment_design.study_arms[0].arm_map.keys())[0],
                         StudyCell('ARM_00_CELL_00', elements=({self.fourth_treatment,
                                                                self.second_treatment,
                                                                self.first_treatment},)))
        """
        self.assertEqual(repr(list(concomitant_treatment_design.study_arms[0].arm_map.keys())[0].elements),
                         repr(sorted({self.fourth_treatment, self.second_treatment, self.first_treatment},
                                     key=lambda el: hash(el))))
        """
        self.assertEqual(concomitant_treatment_design.study_arms[0],
                            StudyArm(name='ARM_00', group_size=30, arm_map=OrderedDict([
                                [StudyCell('ARM_00_CELL_00', elements=({self.fourth_treatment,
                                                                       self.second_treatment,
                                                                       self.first_treatment},)),
                                 self.sample_assay_plan],
                                [StudyCell('ARM_00_CELL_01', elements=(self.follow_up,)), self.sample_assay_plan]
                            ]))
                        )

    def test_compute_concomitant_treatment_design_group_size_error(self):
        treatments = [self.first_treatment, self.third_treatment, self.fourth_treatment]
        with self.assertRaises(TypeError, msg='The group_sizes list has the wrong length') as ex_cm:
            concomitant_treatment_design = StudyDesignFactory.compute_concomitant_treatments_design(
                treatments, self.sample_assay_plan, group_size=[10, 12, 13]
            )
        self.assertEqual(ex_cm.exception.args[0], StudyDesignFactory.GROUP_SIZES_ERROR)

    def test_compute_crossover_design_multi_element_cell_three_treatments(self):
        treatments = [self.first_treatment, self.third_treatment, self.fourth_treatment]
        crossover_design_with_multi_element_cell = StudyDesignFactory.compute_crossover_design_multi_element_cell(
            treatments, self.sample_assay_plan, group_sizes=(10, 15, 12, 15, 12, 20), washout=self.washout,
            screen_map=(self.screen, None),
            run_in_map=(self.run_in, None),
            follow_up_map=(self.follow_up, self.sample_assay_plan)
        )
        self.assertEqual(len(crossover_design_with_multi_element_cell.study_arms), 6)  # three treatments means
                                                                                       # six permutations
        self.assertEqual(crossover_design_with_multi_element_cell.study_arms[0],
                         StudyArm(name='ARM_00', group_size=10, arm_map=OrderedDict(
                             [
                                 [StudyCell('ARM_00_CELL_00', elements=(self.screen,)), None],
                                 [StudyCell('ARM_00_CELL_01', elements=(self.run_in,)), None],
                                 [StudyCell('ARM_00_CELL_02', elements=(self.first_treatment, self.washout,
                                                                        self.third_treatment, self.washout,
                                                                        self.fourth_treatment)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_00_CELL_03', elements=(self.follow_up,)), self.sample_assay_plan]
                             ]
                         )))
        self.assertEqual(crossover_design_with_multi_element_cell.study_arms[1],
                         StudyArm(name='ARM_01', group_size=15, arm_map=OrderedDict(
                             [
                                 [StudyCell('ARM_01_CELL_00', elements=(self.screen,)), None],
                                 [StudyCell('ARM_01_CELL_01', elements=(self.run_in,)), None],
                                 [StudyCell('ARM_01_CELL_02', elements=(self.first_treatment, self.washout,
                                                                        self.fourth_treatment, self.washout,
                                                                        self.third_treatment)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_01_CELL_03', elements=(self.follow_up,)), self.sample_assay_plan]
                             ]
                         )))
        self.assertEqual(crossover_design_with_multi_element_cell.study_arms[2],
                         StudyArm(name='ARM_02', group_size=12, arm_map=OrderedDict(
                             [
                                 [StudyCell('ARM_02_CELL_00', elements=(self.screen,)), None],
                                 [StudyCell('ARM_02_CELL_01', elements=(self.run_in,)), None],
                                 [StudyCell('ARM_02_CELL_02', elements=(self.third_treatment, self.washout,
                                                                        self.first_treatment, self.washout,
                                                                        self.fourth_treatment)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_02_CELL_03', elements=(self.follow_up,)), self.sample_assay_plan]
                             ]
                         )))

    def test_compute_crossover_design_multi_element_cell_group_sizes_error(self):
        treatments = [self.first_treatment, self.third_treatment, self.fourth_treatment]
        with self.assertRaises(TypeError, msg='The group_sizes list has the wrong length') as ex_cm:
            crossover_design_with_multi_element_cell = StudyDesignFactory.compute_crossover_design_multi_element_cell(
                treatments, self.sample_assay_plan, group_sizes=(10, 15, 12, 15, 12), washout=self.washout,
                screen_map=(self.screen, None),
                run_in_map=(self.run_in, None),
                follow_up_map=(self.follow_up, self.sample_assay_plan)
            )
        self.assertEqual(ex_cm.exception.args[0], StudyDesignFactory.GROUP_SIZES_ERROR)

    def test_compute_single_arm_design_multi_element_cell_three_treatments(self):
        treatments = [self.first_treatment, self.third_treatment, self.fourth_treatment]
        crossover_design_with_multi_element_cell = StudyDesignFactory.compute_single_arm_design_multi_element_cell(
            treatments, self.sample_assay_plan, group_size=12, washout=self.washout,
            screen_map=(self.screen, None),
            run_in_map=(self.run_in, None),
            follow_up_map=(self.follow_up, self.sample_assay_plan)
        )
        self.assertEqual(len(crossover_design_with_multi_element_cell.study_arms), 1)  # three treatments means
                                                                                       # six permutations
        self.assertEqual(crossover_design_with_multi_element_cell.study_arms[0],
                         StudyArm(name='ARM_00', group_size=12, arm_map=OrderedDict(
                             [
                                 [StudyCell('ARM_00_CELL_00', elements=(self.screen,)), None],
                                 [StudyCell('ARM_00_CELL_01', elements=(self.run_in,)), None],
                                 [StudyCell('ARM_00_CELL_02', elements=(self.first_treatment, self.washout,
                                                                        self.third_treatment, self.washout,
                                                                        self.fourth_treatment)),
                                  self.sample_assay_plan],
                                 [StudyCell('ARM_00_CELL_03', elements=(self.follow_up,)), self.sample_assay_plan]
                             ]
                         )))

    def test_compute_single_arm_design_multi_element_cell_group_sizes_error(self):
        treatments = [self.first_treatment, self.third_treatment, self.fourth_treatment]
        with self.assertRaises(TypeError, msg='The group_sizes list has the wrong length') as ex_cm:
            crossover_design_with_multi_element_cell = StudyDesignFactory.compute_single_arm_design_multi_element_cell(
                treatments, self.sample_assay_plan, group_size=(10, 15, 12), washout=self.washout,
                screen_map=(self.screen, None),
                run_in_map=(self.run_in, None),
                follow_up_map=(self.follow_up, self.sample_assay_plan)
            )
        self.assertEqual(ex_cm.exception.args[0], StudyDesignFactory.GROUP_SIZES_ERROR)


"""
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
        self.first_treatment = Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
            FactorValue(factor_name=self.agent, value='crack'),
            FactorValue(factor_name=self.intensity, value='low'),
            FactorValue(factor_name=self.duration, value='medium')
        ))
        self.second_treatment = Treatment(element_type=INTERVENTIONS['CHEMICAL'], factor_values=(
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
"""

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