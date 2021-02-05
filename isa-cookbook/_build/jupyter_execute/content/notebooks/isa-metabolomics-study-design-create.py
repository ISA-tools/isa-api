#

## Abstract:
    
In this notebook, we'll show how to generate an ISA-Tab and an ISA JSON representation of a metabolomics study.
The study uses GC-MS and 13C NMR on 3 distinct sample types (liver, blood and heart) collected from study subjects assigned to 3 distinct study arms.

GC-MS acquisition were carried out in duplicate, extracts were derivatized using BSA and acquired on an Agilent QTOF in both positive and negative modes.
13C NMR free induction decays were acquired on a Bruker Avance, using CPMG and PSEQ pulse sequences in duplicates.



### 1. Loading ISA-API model and relevant library

from isatools.model import *
from isatools.create.model import *
from isatools import isatab
from isatools import isajson
from isatools.isajson import ISAJSONEncoder
from isatools.model import (Investigation, Study, Assay, Person, Material,
                            DataFile, plink,
                            OntologySource, OntologyAnnotation, Sample,
                            Source, Characteristic, Protocol, Process)

from isatools.isatab import dump_tables_to_dataframes as dumpdf
import networkx as nx
import numpy as np
import os

### 2. Setting variables:

NAME = 'name'
FACTORS_0_VALUE = OntologyAnnotation(term='nitroglycerin')
FACTORS_0_VALUE_ALT = OntologyAnnotation(term='alcohol')
FACTORS_0_VALUE_THIRD = OntologyAnnotation(term='water')

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
FOLLOW_UP_DURATION_VALUE = 5*366
WASHOUT_DURATION_VALUE = 30
DURATION_UNIT = OntologyAnnotation(term='day')

### 3. Declaration of ISA Sample / Biomaterial templates for liver, blood and heart

sample_list = [
        {
            'node_type': SAMPLE,
            'characteristics_category': OntologyAnnotation(term='organism part'),
            'characteristics_value': OntologyAnnotation(term='liver'),
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': OntologyAnnotation(term='organism part'),
            'characteristics_value': OntologyAnnotation(term='blood'),
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': SAMPLE,
            'characteristics_category': OntologyAnnotation(term='organism part'),
            'characteristics_value': OntologyAnnotation(term='heart'),
            'size': 1,
            'technical_replicates': None,
            'is_input_to_next_protocols': True
        }
]

### 4. Declaration of ISA Assay templates as Python `OrderedDict`

# A Mass Spectrometry based metabolite profiling assay

ms_assay_dict = OrderedDict([
    ('measurement_type', OntologyAnnotation(term='metabolite profiling')),
    ('technology_type', OntologyAnnotation(term='mass spectrometry')),
    ('extraction', {}),
    ('extract', [
        {
            'node_type': EXTRACT,
            'characteristics_category': OntologyAnnotation(term='extract type'),
            'characteristics_value': OntologyAnnotation(term='polar fraction'),
            'size': 1,
            'is_input_to_next_protocols': True
        },
        {
            'node_type': EXTRACT,
            'characteristics_category': OntologyAnnotation(term='extract type'),
            'characteristics_value': OntologyAnnotation(term='lipids'),
            'size': 1,
            'is_input_to_next_protocols': True
        }
    ]),
    ('derivatization', {
        '#replicates': 1,
        OntologyAnnotation(term='derivatization'): ['sylalation'],
        OntologyAnnotation(term='derivatization'): ['bis(trimethylsilyl)acetamide'],
    }),
    ('labeled extract', [
        {
            'node_type': LABELED_EXTRACT,
            'characteristics_category': OntologyAnnotation(term='labeled extract type'),
            'characteristics_value': '',
            'size': 1,
            'is_input_to_next_protocols': True
        }
    ]),
    ('mass spectrometry', {
        '#replicates': 2,
        OntologyAnnotation(term='instrument'): ['Agilent QTOF'],
        OntologyAnnotation(term='injection_mode'): ['GC'],
        OntologyAnnotation(term='acquisition_mode'): ['positive mode','negative mode']
    }),
    ('raw spectral data file', [
        {
            'node_type': DATA_FILE,
            'size': 1,
            'is_input_to_next_protocols': False
        }
    ])
])


# A high-throughput phenotyping imaging based phenotyping assay

phti_assay_dict = OrderedDict([
    ('measurement_type', OntologyAnnotation(term='phenotyping')),
    ('technology_type', OntologyAnnotation(term='high-throughput imaging')),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type'),
                    'characteristics_value': OntologyAnnotation(term='supernatant'),
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type'),
                    'characteristics_value': OntologyAnnotation(term='pellet'),
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('phenotyping by high throughput imaging', {
                'OntologyAnnotation(term=instrument)': ['lemnatech gigant'],
                'OntologyAnnotation(term=acquisition_mode)': ['UV light','near-IR light','far-IR light','visible light'],
                'OntologyAnnotation(term=camera position)': ['top','120 degree','240 degree','360 degree'],
                'OntologyAnnotation(term=imaging daily schedule)': ['06.00','19.00']
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

# A liquid chromatography diode-array based metabolite profiling assay

lcdad_assay_dict = OrderedDict([
    ('measurement_type', OntologyAnnotation(term='metabolite identification')),
    ('technology_type', OntologyAnnotation(term='liquid chromatography diode-array detector')),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type'),
                    'characteristics_value': OntologyAnnotation(term='supernatant'),
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type'),
                    'characteristics_value': OntologyAnnotation(term='pellet'),
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('lcdad_spectroscopy', {
                'OntologyAnnotation(term=instrument)': ['Shimadzu DAD 400'],
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


# A NMR spectroscopy based metabolite profiling assay:
nmr_assay_dict = OrderedDict([
    ('measurement_type', OntologyAnnotation(term='metabolite profiling')),
    ('technology_type', OntologyAnnotation(term='nmr spectroscopy')),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category':  OntologyAnnotation(term='extract type'),
                    'characteristics_value': OntologyAnnotation(term='supernatant'),
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': EXTRACT,
                    'characteristics_category':  OntologyAnnotation(term='extract type'),
                    'characteristics_value': OntologyAnnotation(term='pellet'),
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('nmr spectroscopy', {
                OntologyAnnotation(term='instrument'): [OntologyAnnotation(term='Bruker AvanceII 1 GHz')],
                OntologyAnnotation(term='acquisition_mode'): [OntologyAnnotation(term='1D 13C NMR')],
                OntologyAnnotation(term='pulse_sequence'): [OntologyAnnotation(term='CPMG')]
            }),
            ('raw_spectral_data_file', [
                {
                    'node_type': DATA_FILE,
                    'size': 1,
                    'technical_replicates': 1,
                    'is_input_to_next_protocols': False
                }
            ])
    ])

first_treatment = Treatment(factor_values=(
    FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE),
    FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
    FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
))
second_treatment = Treatment(factor_values=(
    FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE_ALT),
    FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
    FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
))
third_treatment = Treatment(factor_values=(
    FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE_ALT),
    FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
    FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE_ALT, unit=FACTORS_2_UNIT)
))
fourth_treatment = Treatment(factor_values=(
    FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE_THIRD),
    FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE, unit=FACTORS_1_UNIT),
    FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE, unit=FACTORS_2_UNIT)
))
screen = NonTreatment(element_type=SCREEN, duration_value=SCREEN_DURATION_VALUE, duration_unit=DURATION_UNIT)
run_in = NonTreatment(element_type=RUN_IN, duration_value=WASHOUT_DURATION_VALUE, duration_unit=DURATION_UNIT)
washout = NonTreatment(element_type=WASHOUT, duration_value=WASHOUT_DURATION_VALUE, duration_unit=DURATION_UNIT)
follow_up = NonTreatment(element_type=FOLLOW_UP, duration_value=FOLLOW_UP_DURATION_VALUE, duration_unit=DURATION_UNIT)
potential_concomitant_washout = NonTreatment(element_type=WASHOUT, duration_value=FACTORS_2_VALUE,
                                                          duration_unit=FACTORS_2_UNIT)
cell_screen = StudyCell(SCREEN, elements=(screen,))
cell_run_in = StudyCell(RUN_IN, elements=(run_in,))
cell_other_run_in = StudyCell('OTHER RUN-IN', elements=(run_in,))
cell_screen_and_run_in = StudyCell('SCREEN AND RUN-IN', elements=[screen, run_in])
cell_concomitant_treatments = StudyCell('CONCOMITANT TREATMENTS',
                                                     elements=([{second_treatment, fourth_treatment}]))
cell_washout_00 = StudyCell(WASHOUT, elements=(washout,))
cell_washout_01 = StudyCell('ANOTHER WASHOUT', elements=(washout,))
cell_single_treatment_00 = StudyCell('SINGLE TREATMENT FIRST', elements=[first_treatment])
cell_single_treatment_01 = StudyCell('SINGLE TREATMENT SECOND', elements=[second_treatment])
cell_single_treatment_02 = StudyCell('SINGLE TREATMENT THIRD', elements=[third_treatment])
cell_multi_elements = StudyCell('MULTI ELEMENTS',
                                             elements=[{first_treatment, second_treatment,
                                                        fourth_treatment}, washout, second_treatment])
cell_multi_elements_padded = StudyCell('MULTI ELEMENTS PADDED',
                                                    elements=[first_treatment, washout, {
                                                        second_treatment,
                                                        fourth_treatment
                                                    }, washout, third_treatment, washout])
cell_follow_up = StudyCell(FOLLOW_UP, elements=(follow_up,))
cell_follow_up_01 = StudyCell('ANOTHER FOLLOW_UP', elements=(follow_up,))
qc = QualityControl()

ms_sample_assay_plan = SampleAndAssayPlan.from_sample_and_assay_plan_dict("ms_sap", sample_list, ms_assay_dict)
nmr_sample_assay_plan = SampleAndAssayPlan.from_sample_and_assay_plan_dict("nmr_sap", sample_list, nmr_assay_dict)

first_arm = StudyArm(name=TEST_STUDY_ARM_NAME_00, group_size=3, arm_map=OrderedDict([
    (cell_screen, None), (cell_run_in, None),
    (cell_single_treatment_00, ms_sample_assay_plan),
    (cell_follow_up, ms_sample_assay_plan)
]))
second_arm = StudyArm(name=TEST_STUDY_ARM_NAME_01, group_size=5, arm_map=OrderedDict([
    (cell_screen, None), (cell_run_in, None),
    (cell_multi_elements, ms_sample_assay_plan),
    (cell_follow_up, ms_sample_assay_plan)
]))
third_arm = StudyArm(name=TEST_STUDY_ARM_NAME_02, group_size=3, arm_map=OrderedDict([
    (cell_screen, None), (cell_run_in, None),
    (cell_multi_elements_padded, ms_sample_assay_plan),
    (cell_follow_up, ms_sample_assay_plan)
]))
third_arm_no_run_in = StudyArm(name=TEST_STUDY_ARM_NAME_02, group_size=3, arm_map=OrderedDict([
    (cell_screen, None),
    (cell_multi_elements_padded, ms_sample_assay_plan),
    (cell_follow_up, ms_sample_assay_plan)
]))
arm_same_name_as_third = StudyArm(name=TEST_STUDY_ARM_NAME_02, group_size=5, arm_map=OrderedDict([
    (cell_screen, None), (cell_run_in, None),
    (cell_single_treatment_01, ms_sample_assay_plan),
    (cell_follow_up, ms_sample_assay_plan)
]))
        # Sample QC (for mass spectroscopy and other)
pre_run_sample_type = ProductNode(
    id_='pre/00', node_type=SAMPLE, name='water', size=2, characteristics=(
        Characteristic(category='dilution', value=10, unit='mg/L'),
    )
)
post_run_sample_type = ProductNode(
    id_='post/00', node_type=SAMPLE, name='ethanol', size=2, characteristics=(
        Characteristic(category='dilution', value=1000, unit='mg/L'),
        Characteristic(category='dilution', value=100, unit='mg/L'),
        Characteristic(category='dilution', value=10, unit='mg/L'),
        Characteristic(category='dilution', value=1, unit='mg/L'),
        Characteristic(category='dilution', value=0.1, unit='mg/L')
    ))
dummy_sample_type = ProductNode(id_='dummy/01', node_type=SAMPLE, name='dummy')
more_dummy_sample_type = ProductNode(id_='dummy/02', node_type=SAMPLE, name='more dummy')
interspersed_sample_types = [(dummy_sample_type, 20)]
qc = QualityControl(
    interspersed_sample_type=interspersed_sample_types,
    pre_run_sample_type=pre_run_sample_type,
    post_run_sample_type=post_run_sample_type
)

single_arm = StudyArm(name=TEST_STUDY_ARM_NAME_00, group_size=10, arm_map=OrderedDict([
    (cell_screen, ms_sample_assay_plan), (cell_run_in,ms_sample_assay_plan),
    (cell_single_treatment_00, nmr_sample_assay_plan),
    (cell_follow_up, nmr_sample_assay_plan)
]))
study_design = StudyDesign(study_arms=(single_arm,))
study = study_design.generate_isa_study()

study

treatment_assay = next(iter(study.assays))

treatment_assay.graph

[(process.name, getattr(process.prev_process, 'name', None), getattr(process.next_process, 'name', None)) for process in treatment_assay.process_sequence]

a_graph = treatment_assay.graph

len(a_graph.nodes)

isa_investigation = Investigation(studies=[study])

isa_tables = dumpdf(isa_investigation)

[type(x) for x in study.assays[0].graph.nodes()]

[(getattr(el, 'name', None), type(el))for el in treatment_assay.graph.nodes()]

from isatools.model import _build_assay_graph

gph = _build_assay_graph(treatment_assay.process_sequence)

[key for key in isa_tables.keys()]

isa_tables['s_study_01.txt']

isa_tables['a_AT0_metabolite-profiling_nmr-spectroscopy.txt']

isa_tables['a_AT0_metabolite-profiling_mass-spectrometry.txt']

final_dir = os.path.abspath(os.path.join('notebook-output', 'sd-test'))

isa_j = json.dumps(isa_investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': '))
open(os.path.join(final_dir,"isa_as_json_from_dumps2.json"),"w").write(isa_j) # this call write the string 'isa_j' to the file called 'isa_as_json_from_dumps.json'

isatab.dump(isa_obj=isa_investigation, output_path=final_dir)

print(final_dir)
with open(os.path.join(final_dir,'i_investigation.txt')) as isa:
    validation_report=isatab.validate(isa)

validation_report["errors"]

## Conclusion:



## About this notebook

- authors: philippe.rocca-serra@oerc.ox.ac.uk, massimiliano.izzo@oerc.ox.ac.uk
- license: CC-BY 4.0
- support: isatools@googlegroups.com
- issue tracker: https://github.com/ISA-tools/isa-api/issues