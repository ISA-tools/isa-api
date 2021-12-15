import unittest

from isatools import isatab
from isatools.isajson import ISAJSONEncoder
from collections import OrderedDict
from isatools.model import (
    Investigation,
    OntologySource,
    OntologyAnnotation,
    FactorValue,
    Characteristic
)
from isatools.create.model import (
    Treatment,
    NonTreatment,
    StudyCell,
    StudyArm,
    ProductNode,
    SampleAndAssayPlan,
    StudyDesign,
    QualityControl
)
from isatools.create.constants import (
    BASE_FACTORS,
    SCREEN,
    RUN_IN,
    WASHOUT,
    FOLLOW_UP,
    SAMPLE,
    EXTRACT,
    LABELED_EXTRACT,
    DATA_FILE
)
from isatools.isatab import dump_tables_to_dataframes as dumpdf
import os
import json



class MyTestCase(unittest.TestCase):
    def test_something(self):
        # self.assertEqual(True, False)  # add assertion here

        # ontologies
        ontologies = {
            "chebi": OntologySource(
                name = "CHEBI",
                description = "Chemical Entities of Biological Interest"),
            "chmo": OntologySource(
                name = "CHMO",
                description = "Chemical Methods Ontology"),
            "msio": OntologySource(
                name = "MSIO",
                description = "Metabolite Standards Initiative Ontology"),
            "ncbitaxon": OntologySource(
                name = "NCBITAXON",
                description = "NCBI organismal classification"),
            "ncit": OntologySource(
                name = "NCIT",
                description = "NCI Thesaurus OBO Edition"),
            "obi": OntologySource(
                name = "OBI",
                description = "Ontology for Biomedical Investigations"),
            "uo": OntologySource(
                name = "UO",
                description = "UO - the Unit Ontology"),
            "pato": OntologySource(
                name = "PATO",
                description = "PATO - the Phenotype And Trait Ontology"),
            "uberon": OntologySource(
                name = "UBERON",
                description = "Uber-anatomy ontology")
        }
        # add ontologies to investigation

        isa_investigation = Investigation()

        for o in ontologies.values():
            isa_investigation.ontology_source_references.append(o)


        NAME = 'name'
        FACTORS_0_VALUE = OntologyAnnotation(term='cadmium chloride', term_accession='http://purl.obolibrary.org/obo/CHEBI_35456', term_source='CHEBI') #,
        FACTORS_0_VALUE_ALT = OntologyAnnotation(term='ethoprophos', term_accession='http://purl.obolibrary.org/obo/CHEBI_38665', term_source='CHEBI')
        FACTORS_0_VALUE_THIRD = OntologyAnnotation(term='pirinixic acid', term_accession='http://purl.obolibrary.org/obo/CHEBI_32509', term_source='CHEBI')

        FACTORS_1_VALUE = 5
        FACTORS_2_VALUE_ALT = "BMD"
        FACTORS_2_VALUE_THIRD = "EC25"
        FACTORS_1_UNIT = OntologyAnnotation(term='kg/m^3', term_accession='http://purl.obolibrary.org/obo/UO_0000083', term_source='UO')

        FACTORS_2_VALUE = 0
        FACTORS_2_VALUE_ALT = 4
        FACTORS_2_VALUE_2 = 24
        FACTORS_2_VALUE_3 = 48
        FACTORS_2_UNIT = OntologyAnnotation(term='hr')

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
        DURATION_UNIT = OntologyAnnotation(term='day', term_accession='http://purl.obolibrary.org/obo/UO_0000033', term_source='UO')

        sample_list = [
            {
                'node_type': SAMPLE,
                'characteristics_category': OntologyAnnotation(term='organism part'),
                'characteristics_value': OntologyAnnotation(term='whole organism', term_accession='http://purl.obolibrary.org/obo/OBI_0100026', term_source='OBI'),
                'size': 1,
                'technical_replicates': None,
                'is_input_to_next_protocols': True
            }
        ]



        # A Mass Spectrometry based metabolite profiling assay

        ms_assay_dict = OrderedDict([
            ('measurement_type', OntologyAnnotation(term='metabolite profiling', term_source="OBI", term_accession="http://purl.obolibrary.org/obo/OBI_0100026")),
            ('technology_type', OntologyAnnotation(term='mass spectrometry', term_source="OBI", term_accession="http://purl.obolibrary.org/obo/OBI_0100026")),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type', term_source="", term_accession=""),
                    'characteristics_value': OntologyAnnotation(term='polar fraction', term_source="", term_accession=""),
                    'size': 1,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type', term_source="", term_accession=""),
                    'characteristics_value': OntologyAnnotation(term='lipids', term_source="", term_accession=""),
                    'size': 1,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('derivatization', {
                '#replicates': 1,
                OntologyAnnotation(term='derivatization', term_source="", term_accession=""): ['sylalation'],
                OntologyAnnotation(term='derivatization', term_source="", term_accession=""): ['bis(trimethylsilyl)acetamide'],
            }),
            ('labeled extract', [
                {
                    'node_type': LABELED_EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='labeled extract type', term_source="", term_accession=""),
                    'characteristics_value': '',
                    'size': 1,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('mass spectrometry', {
                '#replicates': 2,
                OntologyAnnotation(term='instrument', term_source="OBI", term_accession="http://purl.obolibrary.org/obo/OBI_0100026"): ['Agilent QTOF'],
                OntologyAnnotation(term='injection_mode', term_source="", term_accession=""): ['GC'],
                OntologyAnnotation(term='acquisition_mode', term_source="", term_accession=""): ['positive mode', 'negative mode']
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
            ('measurement_type', OntologyAnnotation(term='phenotyping', term_source="", term_accession="")),
            ('technology_type', OntologyAnnotation(term='high-throughput imaging', term_source="", term_accession="")),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type', term_source="", term_accession=""),
                    'characteristics_value': OntologyAnnotation(term='supernatant', term_source="OBI", term_accession="http://purl.obolibrary.org/obo/OBI_0100026"),
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('phenotyping by high throughput imaging', {
                OntologyAnnotation(term="instrument", term_source="OBI", term_accession="http://purl.obolibrary.org/obo/OBI_0100026"): ['lemnatech gigant'],
                OntologyAnnotation(term="acquisition_mode", term_source="OBI", term_accession="http://purl.obolibrary.org/obo/OBI_0100026"): ['UV light','near-IR light','far-IR light','visible light'],
                OntologyAnnotation(term="camera position", term_source="OBI", term_accession="http://purl.obolibrary.org/obo/OBI_0100026"): ['top','120 degree','240 degree','360 degree'],
                OntologyAnnotation(term="imaging daily schedule",  term_source="OBI", term_accession="http://purl.obolibrary.org/obo/OBI_0100026"): ['06.00','19.00']
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

        # A RNA-Seq based transcription profiling assay

        rnaseq_assay_dict = OrderedDict([
            ('measurement_type', OntologyAnnotation(term='transcription profiling', term_source="OBI", term_accession="http://purl.obolibrary.org/obo/OBI_000066")), #
            ('technology_type', OntologyAnnotation(term='nucleotide sequencing', term_source="OBI", term_accession="http://purl.obolibrary.org/obo/OBI_0000234")), #
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type', term_source="", term_accession=""),
                    'characteristics_value': OntologyAnnotation(term='mRNA', term_source="OBI", term_accession="http://purl.obolibrary.org/obo/OBI_03234235"),
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('library_preparation', {
                OntologyAnnotation(term="library strategy", term_source="", term_accession=""): ['RNA-SEQ'],
                OntologyAnnotation(term="library layout", term_source="", term_accession=""): ['PAIRED'],
                OntologyAnnotation(term="size", term_source="", term_accession=""): ['40'],
            }),
            ('nucleic acid sequencing', {
                OntologyAnnotation(term="sequencing instrument", term_source="OBI", term_accession="http://purl.obolibrary.org/obo/OBI_0100026"): ['DNBSEQ-T7']
            }),
            ('raw_data_file', [
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

        #screen = NonTreatment(element_type=SCREEN, duration_value=SCREEN_DURATION_VALUE, duration_unit=DURATION_UNIT)
        #run_in = NonTreatment(element_type=RUN_IN, duration_value=WASHOUT_DURATION_VALUE, duration_unit=DURATION_UNIT)
        #washout = NonTreatment(element_type=WASHOUT, duration_value=WASHOUT_DURATION_VALUE, duration_unit=DURATION_UNIT)
        #follow_up = NonTreatment(element_type=FOLLOW_UP, duration_value=FOLLOW_UP_DURATION_VALUE, duration_unit=DURATION_UNIT)
        #potential_concomitant_washout = NonTreatment(element_type=WASHOUT, duration_value=FACTORS_2_VALUE,
        #                                                          duration_unit=FACTORS_2_UNIT)
        #cell_screen = StudyCell(SCREEN, elements=(screen,))
        #cell_run_in = StudyCell(RUN_IN, elements=(run_in,))
        #cell_other_run_in = StudyCell('OTHER RUN-IN', elements=(run_in,))
        #cell_screen_and_run_in = StudyCell('SCREEN AND RUN-IN', elements=[screen, run_in])
        #cell_concomitant_treatments = StudyCell('CONCOMITANT TREATMENTS',
        #                                                     elements=([{second_treatment, fourth_treatment}]))
        #cell_washout_00 = StudyCell(WASHOUT, elements=(washout,))
        #cell_washout_01 = StudyCell('ANOTHER WASHOUT', elements=(washout,))
        cell_single_treatment_00 = StudyCell('SINGLE TREATMENT FIRST', elements=[first_treatment])
        cell_single_treatment_01 = StudyCell('SINGLE TREATMENT SECOND', elements=[second_treatment])
        cell_single_treatment_02 = StudyCell('SINGLE TREATMENT THIRD', elements=[third_treatment])
        #cell_multi_elements = StudyCell('MULTI ELEMENTS',
        #                                             elements=[{first_treatment, second_treatment,
        #                                                        fourth_treatment}, washout, second_treatment])
        #cell_multi_elements_padded = StudyCell('MULTI ELEMENTS PADDED',
        #                                                    elements=[first_treatment, washout, {
        #                                                        second_treatment,
        #                                                        fourth_treatment
        #                                                    }, washout, third_treatment, washout])
        #cell_follow_up = StudyCell(FOLLOW_UP, elements=(follow_up,))
        #cell_follow_up_01 = StudyCell('ANOTHER FOLLOW_UP', elements=(follow_up,))
        #qc = QualityControl()

        ms_sample_assay_plan = SampleAndAssayPlan.from_sample_and_assay_plan_dict("ms_sap", sample_list, ms_assay_dict)
        rnaseq_sample_assay_plan = SampleAndAssayPlan.from_sample_and_assay_plan_dict("rnaseq_sap", sample_list, rnaseq_assay_dict)
        phti_sample_assay_plan = SampleAndAssayPlan.from_sample_and_assay_plan_dict("phti_sap", sample_list, phti_assay_dict)

        first_arm = StudyArm(name=TEST_STUDY_ARM_NAME_00, group_size=3, arm_map=OrderedDict([
            #  (cell_screen, None), (cell_run_in, None),
            (cell_single_treatment_00, ms_sample_assay_plan),
            (cell_single_treatment_00, rnaseq_sample_assay_plan)
            # (cell_follow_up, ms_sample_assay_plan)
        ]))
        second_arm = StudyArm(name=TEST_STUDY_ARM_NAME_01, group_size=3, arm_map=OrderedDict([
            # (cell_screen, None), (cell_run_in, None),
            (cell_single_treatment_01, ms_sample_assay_plan),
            (cell_single_treatment_01, rnaseq_sample_assay_plan)
            #(cell_multi_elements, ms_sample_assay_plan),
            # (cell_follow_up, ms_sample_assay_plan)
        ]))
        third_arm = StudyArm(name=TEST_STUDY_ARM_NAME_02, group_size=3, arm_map=OrderedDict([
            # (cell_screen, None), (cell_run_in, None),
            (cell_single_treatment_02,rnaseq_sample_assay_plan),
            (cell_single_treatment_02, ms_sample_assay_plan)

            # (cell_multi_elements_padded, ms_sample_assay_plan),
            # (cell_follow_up, ms_sample_assay_plan)
        ]))
        #third_arm_no_run_in = StudyArm(name=TEST_STUDY_ARM_NAME_02, group_size=3, arm_map=OrderedDict([
        # (cell_screen, None),
        #   (cell_multi_elements_padded, ms_sample_assay_plan),
        # (cell_follow_up, ms_sample_assay_plan)
        #]))
        #arm_same_name_as_third = StudyArm(name=TEST_STUDY_ARM_NAME_02, group_size=3, arm_map=OrderedDict([
        #(cell_screen, None), (cell_run_in, None),
        #    (cell_single_treatment_01, ms_sample_assay_plan),
        #(cell_follow_up, ms_sample_assay_plan)
        #]))


        # Sample QC (for mass spectroscopy and other)
        #pre_run_sample_type = ProductNode(
        #    id_='pre/00', node_type=SAMPLE, name='water', size=2, characteristics=(
        #        Characteristic(category='dilution', value=10, unit='mg/L'),
        #    )
        #)
        #post_run_sample_type = ProductNode(
        #    id_='post/00', node_type=SAMPLE, name='ethanol', size=2, characteristics=(
        #        Characteristic(category='dilution', value=1000, unit='mg/L'),
        #        Characteristic(category='dilution', value=100, unit='mg/L'),
        #        Characteristic(category='dilution', value=10, unit='mg/L'),
        #        Characteristic(category='dilution', value=1, unit='mg/L'),
        #        Characteristic(category='dilution', value=0.1, unit='mg/L')
        #    ))
        #dummy_sample_type = ProductNode(id_='dummy/01', node_type=SAMPLE, name='dummy')
        #more_dummy_sample_type = ProductNode(id_='dummy/02', node_type=SAMPLE, name='more dummy')
        #interspersed_sample_types = [(dummy_sample_type, 20)]

        #qc = QualityControl(
        #    interspersed_sample_type=interspersed_sample_types,
        #    pre_run_sample_type=pre_run_sample_type,
        #    post_run_sample_type=post_run_sample_type
        #)

        study_design = StudyDesign(study_arms=(first_arm, second_arm, third_arm))

        study = study_design.generate_isa_study()

        treatment_assay = next(iter(study.assays))

        treatment_assay.graph

        [(process.name, getattr(process.prev_process, 'name', None), getattr(process.next_process, 'name', None)) for process in treatment_assay.process_sequence]
        a_graph = treatment_assay.graph

        len(a_graph.nodes)

        isa_investigation.studies=[study]

        isa_tables = dumpdf(isa_investigation)

        from isatools.model import _build_assay_graph

        gph = _build_assay_graph(treatment_assay.process_sequence)

        [key for key in isa_tables.keys()]

        isa_tables['s_study_01.txt']

        isa_tables['a_AT0_transcription-profiling_nucleotide-sequencing.txt']

        isa_tables['a_AT0_metabolite-profiling_mass-spectrometry.txt']

        final_dir = os.path.abspath(os.path.join('notebook-output', 'sd-test'))

        isatab.dump(isa_obj=isa_investigation, output_path=final_dir)

        isa_j = json.dumps(isa_investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': '))
        with open(os.path.join(final_dir, "isa_as_json_from_dumps2.json"), "w") as isajson_output:
            isajson_output.write(isa_j) # this call write the string 'isa_j' to the file called 'isa_as_json_from_dumps.json'


if __name__ == '__main__':
    unittest.main()
