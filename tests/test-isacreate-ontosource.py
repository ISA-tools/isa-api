import unittest

import source as source

import isatools

from isatools import isatab
from isatools.convert import json2isatab
from isatools.isajson import ISAJSONEncoder
from collections import OrderedDict
from isatools.model import (
    Investigation,
    OntologySource,
    OntologyAnnotation,
    # FactorValue,
    Characteristic,
    Comment,
    Person
)
from isatools.create.model import (
    Treatment,
    TreatmentFactory,
    # NonTreatment,
    # StudyCell,
    # StudyArm,
    # ProductNode,
    SampleAndAssayPlan,
    StudyDesign,
    StudyDesignFactory,
    # QualityControl
)
from isatools.create.constants import (
    BASE_FACTORS,
    # SCREEN,
    # RUN_IN,
    # WASHOUT,
    # FOLLOW_UP,
    set_defaulttype_value as set_default_species,
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

        # creating a new ISA investigation object:
        isa_investigation = Investigation()

        # declaring ontologies used for annotating the project
        ontologies = {
            "chebi": OntologySource(
                name="CHEBI",
                description="Chemical Entities of Biological Interest"),
            "chmo": OntologySource(
                name="CHMO",
                description="Chemical Methods Ontology"),
            "msio": OntologySource(
                name="MSIO",
                description="Metabolite Standards Initiative Ontology"),
            "ncbitaxon": OntologySource(
                name="NCBITAXON",
                description="NCBI organismal classification"),
            "ncit": OntologySource(
                name="NCIT",
                description="NCI Thesaurus OBO Edition"),
            "obi": OntologySource(
                name="OBI",
                description="Ontology for Biomedical Investigations"),
            "ms": OntologySource(
                name="MS",
                description="MS - the Mass Spectrometry Ontology"),
            "uo": OntologySource(
                name="UO",
                description="UO - the Unit Ontology"),
            "pato": OntologySource(
                name="PATO",
                description="PATO - the Phenotype And Trait Ontology"),
            "uberon": OntologySource(
                name="UBERON",
                description="Uber-anatomy ontology")
        }

        # add ontologies to investigation
        for o in ontologies.values():
            isa_investigation.ontology_source_references.append(o)

        # Setting the Species used in the PrecisionTox study:
        PTox_NAM = "Danio rerio"

        if PTox_NAM == "Daphnia magna":
            set_default_species(term=PTox_NAM,
                                term_accession="http://purl.obolibrary.org/obo/NCBITaxon_35525",
                                term_source=ontologies["ncbitaxon"])
        elif PTox_NAM == "Danio rerio":
            set_default_species(term=PTox_NAM,
                                term_accession="http://purl.obolibrary.org/obo/NCBITaxon_7955",
                                term_source=ontologies["ncbitaxon"])
        elif PTox_NAM == "Xenopus laevis":
            set_default_species(term=PTox_NAM,
                                term_accession="http://purl.obolibrary.org/obo/NCBITaxon_8355",
                                term_source=ontologies["ncbitaxon"])
        elif PTox_NAM == "Caenorhabditis elegans":
            set_default_species(term=PTox_NAM,
                                term_accession="http://purl.obolibrary.org/obo/NCBITaxon_6239",
                                term_source=ontologies["ncbitaxon"])
        elif PTox_NAM == "Drosophila melanogaster":
            set_default_species(term=PTox_NAM,
                                term_accession="http://purl.obolibrary.org/obo/NCBITaxon_7227",
                                term_source=ontologies["ncbitaxon"])
        elif PTox_NAM == "Homo sapiens":
            set_default_species(term=PTox_NAM,
                                term_accession="http://purl.obolibrary.org/obo/NCBITaxon_9606",
                                term_source=ontologies["ncbitaxon"])

        NAME = 'name'

        # declaring the sets which will hold the `factor_values values`
        factors_0_values = set()
        factors_1_values = set()
        factors_2_values = set()

        # creating `factor_value values`
        # factor values for the first factor (agent)
        FACTORS_0_VALUE_0 = (OntologyAnnotation(term='cadmium chloride',
                                                term_accession='https://purl.obolibrary.org/obo/CHEBI_35456',
                                                term_source='CHEBI'), None)
        FACTORS_0_VALUE_1 = (OntologyAnnotation(term='ethoprophos',
                                                term_accession='https://purl.obolibrary.org/obo/CHEBI_38665',
                                                term_source='CHEBI'), None)
        FACTORS_0_VALUE_2 = (OntologyAnnotation(term='pirinixic acid',
                                                term_accession='https://purl.obolibrary.org/obo/CHEBI_32509',
                                                term_source='CHEBI'), None)

        # factor values for the second factor (intensity)
        FACTORS_1_UNIT = OntologyAnnotation(term='kg/m^3',
                                            term_accession='https://purl.obolibrary.org/obo/UO_0000083',
                                            term_source='UO')

        FACTORS_1_VALUE_1 = (OntologyAnnotation(term="BMD"), FACTORS_1_UNIT)
        FACTORS_1_VALUE_2 = (OntologyAnnotation(term="EC25"), FACTORS_1_UNIT)
        # FACTORS_1_VALUE_1 = (25, FACTORS_1_UNIT)
        # FACTORS_1_VALUE_2 = (100, FACTORS_1_UNIT)

        # factor values for the third factor (duration)
        FACTORS_2_UNIT = OntologyAnnotation(term='hr',
                                            term_accession='https://purl.obolibrary.org/obo/UO_0000032',
                                            term_source='UO')
        FACTORS_2_VALUE_0 = (0, FACTORS_2_UNIT)
        FACTORS_2_VALUE_1 = (4, FACTORS_2_UNIT)
        FACTORS_2_VALUE_2 = (24, FACTORS_2_UNIT)
        FACTORS_2_VALUE_3 = (48, FACTORS_2_UNIT)

        # adding the values to the relevant sets
        factors_0_values.add(FACTORS_0_VALUE_0)
        # factors_0_values.add(FACTORS_0_VALUE_1)
        # factors_0_values.add(FACTORS_0_VALUE_2)

        factors_1_values.add(FACTORS_1_VALUE_1)
        factors_1_values.add(FACTORS_1_VALUE_2)

        factors_2_values.add(FACTORS_2_VALUE_0)
        # factors_2_values.add(FACTORS_2_VALUE_1)
        # factors_2_values.add(FACTORS_2_VALUE_2)
        # factors_2_values.add(FACTORS_2_VALUE_3)

        # creating a new treatment factory instance and passing the Factors and associated Factor Values
        tf = TreatmentFactory()
        tf.add_factor_value(BASE_FACTORS[0], factors_0_values)
        tf.add_factor_value(BASE_FACTORS[1], factors_1_values)
        tf.add_factor_value(BASE_FACTORS[2], factors_2_values)

        sample_list = [
            {
                'node_type': SAMPLE,
                'characteristics_category': OntologyAnnotation(term='organism part'),
                'characteristics_value': OntologyAnnotation(term='whole organism',
                                                            term_accession='https://purl.obolibrary.org/obo/OBI_0100026',
                                                            term_source='OBI'),
                'size': 1,
                'technical_replicates': None,
                'is_input_to_next_protocols': True
            },
            # {
            #     'node_type': SAMPLE,
            #     'characteristics_category': OntologyAnnotation(term='organism part'),
            #     'characteristics_value': OntologyAnnotation(term='liver',
            #                                                 term_accession='https://purl.obolibrary.org/obo/UBERON_0100026',
            #                                                 term_source='UBERON'),
            #     'size': 2,
            #     'technical_replicates': None,
            #     'is_input_to_next_protocols': True
            # }
        ]

        # A Mass Spectrometry based metabolite profiling assay
        ms_assay_dict = OrderedDict([
            ('id', '0'),
            ('measurement_type', OntologyAnnotation(term='metabolite profiling',
                                                    term_source="OBI",
                                                    term_accession="https://purl.obolibrary.org/obo/OBI_0100026")),
            ('technology_type', OntologyAnnotation(term='mass spectrometry',
                                                   term_source="OBI",
                                                   term_accession="https://purl.obolibrary.org/obo/OBI_0100026")),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type',
                                                                   term_source="",
                                                                   term_accession=""),
                    'characteristics_value': OntologyAnnotation(term='polar fraction',
                                                                term_source="",
                                                                term_accession=""),
                    'size': 1,
                    'is_input_to_next_protocols': True
                },
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type',
                                                                   term_source="",
                                                                   term_accession=""),
                    'characteristics_value': OntologyAnnotation(term='lipid',
                                                                term_source="CHEBI",
                                                                term_accession="http://purl.obolibrary.org/obo/CHEBI_18059"),
                    'size': 1,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('derivatization', {
                '#replicates': 1,
                OntologyAnnotation(term='derivatization',
                                   term_source="MSIO",
                                   term_accession="http://purl.obolibrary.org/obo/MSIO_0000111"):
                    [OntologyAnnotation(term='silylation',
                                        term_source="MSIO",
                                        term_accession="http://purl.obolibrary.org/obo/MSIO_0000117")
                                                        ],
                OntologyAnnotation(term='derivatization agent',
                                   term_source="MSIO",
                                   term_accession="http://purl.obolibrary.org/obo/MSIO_0000029"):
                    [OntologyAnnotation(term='N-(tert-butyldimethylsilyl)-N-methyltrifluoroacetamide',
                                        term_source="CHEBI",
                                        term_accession="http://purl.obolibrary.org/obo/CHEBI_85060")
                                                        ],
            }),
            ('labeled extract', [
                {
                    'node_type': LABELED_EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='labeled extract type',
                                                                   term_source="",
                                                                   term_accession=""),
                    'characteristics_value': OntologyAnnotation(term='',
                                                                term_source="",
                                                                term_accession=""),
                    'size': 1,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('mass spectrometry', {
                '#replicates': 1,
                OntologyAnnotation(term='instrument',
                                   term_source="MS",
                                   term_accession="http://purl.obolibrary.org/obo/MS_1000463"):
                    [OntologyAnnotation(term='7000A Triple Quadrupole GC/MS',
                                        term_source="MS",
                                        term_accession="http://purl.obolibrary.org/obo/MS_1002802")],

                OntologyAnnotation(term='injection_mode',
                                   term_source="",
                                   term_accession=""):
                    [OntologyAnnotation(term='GC',
                                        term_source="MS",
                                        term_accession="http://purl.obolibrary.org/obo/MS_1002272")],
                OntologyAnnotation(term='acquisition_mode',
                                   term_source="MS",
                                   term_accession="http://purl.obolibrary.org/obo/MS_1000465"):
                    [OntologyAnnotation(term='positive mode',
                                        term_source="MS",
                                        term_accession="http://purl.obolibrary.org/obo/MS_1000130"),
                     OntologyAnnotation(term='negative mode',
                                        term_source="MS",
                                        term_accession="http://purl.obolibrary.org/obo/MS_1000129"
                                        )]
            }),
            ('raw spectral data file', [
                {
                    'node_type': DATA_FILE,
                    'size': 1,
                    'extension': "mzml.gz",
                    'is_input_to_next_protocols': False
                }
            ])
        ])

        # A high-throughput phenotyping imaging based phenotyping assay
        phti_assay_dict = OrderedDict([
            ('measurement_type', OntologyAnnotation(term='phenotyping',
                                                    term_source="",
                                                    term_accession="")),
            ('technology_type', OntologyAnnotation(term='high-throughput imaging',
                                                   term_source="",
                                                   term_accession="")),
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type',
                                                                   term_source="",
                                                                   term_accession=""),
                    'characteristics_value': OntologyAnnotation(term='supernatant',
                                                                term_source="OBI",
                                                                term_accession="https://purl.obolibrary.org/obo/OBI_0100026"),
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('phenotyping by high throughput imaging', {
                OntologyAnnotation(term="instrument",
                                   term_source="OBI",
                                   term_accession="https://purl.obolibrary.org/obo/OBI_0100026"):
                    [OntologyAnnotation(term="lemnatech gigant")],
                OntologyAnnotation(term="acquisition_mode",
                                   term_source="OBI",
                                   term_accession="https://purl.obolibrary.org/obo/OBI_0100026"):
                    [OntologyAnnotation(term="UV light"),
                     OntologyAnnotation(term="near-IR light"),
                     OntologyAnnotation(term="far-IR light"),
                     OntologyAnnotation(term="visible light")],
                OntologyAnnotation(term="camera position",
                                   term_source="OBI",
                                   term_accession="https://purl.obolibrary.org/obo/OBI_0100026"):
                    ['top', '120 degree', '240 degree', '360 degree'],
                OntologyAnnotation(term="imaging daily schedule",
                                   term_source="OBI",
                                   term_accession="https://purl.obolibrary.org/obo/OBI_0100026"): ['06.00', '19.00']
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
            ('id', '1'),
            ('measurement_type', OntologyAnnotation(term='transcription profiling',
                                                    term_source="OBI",
                                                    term_accession="https://purl.obolibrary.org/obo/OBI_000066")),  #
            ('technology_type', OntologyAnnotation(term='nucleotide sequencing',
                                                   term_source="OBI",
                                                   term_accession="https://purl.obolibrary.org/obo/OBI_0000234")),  #
            ('extraction', {}),
            ('extract', [
                {
                    'node_type': EXTRACT,
                    'characteristics_category': OntologyAnnotation(term='extract type',
                                                                   term_source="",
                                                                   term_accession=""),
                    'characteristics_value': OntologyAnnotation(term='mRNA',
                                                                term_source="OBI",
                                                                term_accession="https://purl.obolibrary.org/obo/OBI_03234235"),
                    'size': 1,
                    'technical_replicates': None,
                    'is_input_to_next_protocols': True
                }
            ]),
            ('library_preparation', {
                OntologyAnnotation(term="library strategy",
                                   term_source="",
                                   term_accession=""): [
                    OntologyAnnotation(term="RNA-SEQ",
                                       term_source="OBI",
                                       term_accession="https://purl.obolibrary.org/obo/OBI_0100023")],
                OntologyAnnotation(term="library layout",
                                   term_source="",
                                   term_accession=""): [OntologyAnnotation(term="PAIRED")],
                OntologyAnnotation(term="size",
                                   term_source="",
                                   term_accession=""): ['40'],
            }),
            ('nucleic acid sequencing', {
                OntologyAnnotation(term="sequencing instrument",
                                   term_source="OBI",
                                   term_accession="https://purl.obolibrary.org/obo/OBI_0100026"):
                    [OntologyAnnotation(term="DNBSEQ-T7",
                                        term_source="OBI",
                                        term_accession="https://purl.obolibrary.org/obo/OBI_0100026")]
            }),
            ('raw_data_file', [
                {
                    'node_type': DATA_FILE,
                    'extension': "fastq.gz",
                    'size': 1,
                    'technical_replicates': 1,
                    'is_input_to_next_protocols': False
                }
            ])
        ])

        # first_treatment = Treatment(factor_values=(
        #     FactorValue(factor_name=BASE_FACTORS[0], value=FACTORS_0_VALUE_0),
        #     FactorValue(factor_name=BASE_FACTORS[1], value=FACTORS_1_VALUE_0, unit=FACTORS_1_UNIT),
        #     FactorValue(factor_name=BASE_FACTORS[2], value=FACTORS_2_VALUE_0, unit=FACTORS_2_UNIT)
        # ))
        #

        # qc = QualityControl()

        # ms_sample_assay_plan = SampleAndAssayPlan.from_sample_and_assay_plan_dict("ms_sap", sample_list, ms_assay_dict)
        # rnaseq_sample_assay_plan = SampleAndAssayPlan.from_sample_and_assay_plan_dict("rnaseq_sap", sample_list,
        #                                                                               rnaseq_assay_dict)
        # # this is a placeholder and this plan is not used yet
        # phti_sample_assay_plan = SampleAndAssayPlan.from_sample_and_assay_plan_dict("phti_sap", sample_list,
        #                                                                             phti_assay_dict)

        sample_assay_plan = SampleAndAssayPlan.from_sample_and_assay_plan_dict("test", sample_list, ms_assay_dict,
                                                                               rnaseq_assay_dict)

        # instantiating a new StudyDesignFactory object to build the full factorial design
        sdf = StudyDesignFactory()

        # initializing a study treatment map list, which is an input to the `compute_parallel_design` method:
        study_tmaps = []

        # for each treatment computed from the set of factor values supplied, a treatment/assay plan map is created
        for t in tf.compute_full_factorial_design():
            study_tmaps.append((t, sample_assay_plan))
            # study_tmaps.append((t, rnaseq_sample_assay_plan))

        # assuming a parallel group design and single treatment, the study arms are computed
        study_design_test = sdf.compute_parallel_design(treatments_map=study_tmaps, group_sizes=2)

        # print("study design factory: ", study_design_test)
        # print("study design arms: ", study_design_test.study_arms)

        #
        # Sample QC (for mass spectroscopy and other)
        # pre_run_sample_type = ProductNode(
        #    id_='pre/00', node_type=SAMPLE, name='water', size=2, characteristics=(
        #        Characteristic(category='dilution', value=10, unit='mg/L'),
        #    )
        # )
        # post_run_sample_type = ProductNode(
        #    id_='post/00', node_type=SAMPLE, name='ethanol', size=2, characteristics=(
        #        Characteristic(category='dilution', value=1000, unit='mg/L'),
        #        Characteristic(category='dilution', value=100, unit='mg/L'),
        #        Characteristic(category='dilution', value=10, unit='mg/L'),
        #        Characteristic(category='dilution', value=1, unit='mg/L'),
        #        Characteristic(category='dilution', value=0.1, unit='mg/L')
        #    ))
        # dummy_sample_type = ProductNode(id_='dummy/01', node_type=SAMPLE, name='dummy')
        # more_dummy_sample_type = ProductNode(id_='dummy/02', node_type=SAMPLE, name='more dummy')
        # interspersed_sample_types = [(dummy_sample_type, 20)]
        #
        # qc = QualityControl(
        #    interspersed_sample_type=interspersed_sample_types,
        #    pre_run_sample_type=pre_run_sample_type,
        #    post_run_sample_type=post_run_sample_type
        # )

        # creating a study design objects by passing the list of study arms computed before:
        study_design = StudyDesign(study_arms=study_design_test.study_arms)

        # creating the ISA study based on study design information (treatment, arms, sampling and assay plans)
        study = study_design.generate_isa_study()

        treatment_assay = next(iter(study.assays))

        # print(treatment_assay.graph)

        [(process.name, getattr(process.prev_process, 'name', None), getattr(process.next_process, 'name', None)) for
         process in treatment_assay.process_sequence]

        # a_graph = treatment_assay.graph
        # print(len(a_graph.nodes))

        isa_investigation.studies = [study]

        isa_investigation.studies[0].comments.append(Comment(name="SRA Broker Name", value="OXFORD"))
        isa_investigation.studies[0].comments.append(Comment(name="SRA Center Name", value="OXFORD"))
        isa_investigation.studies[0].comments.append(Comment(name="SRA Center Project Name", value="OXFORD"))
        isa_investigation.studies[0].comments.append(Comment(name="SRA Lab Name", value="Oxford e-Research Centre"))
        isa_investigation.studies[0].comments.append(Comment(name="SRA Submission Action", value="ADD"))

        isa_investigation.studies[0].contacts.append(Person(first_name="John",
                                                            last_name="Colbourne",
                                                            email="J.K.Colbourne@bham.ac.uk",
                                                            affiliation="University of Birmingham",
                                                            roles=[OntologyAnnotation(term="principal investigator role"),
                                                                   OntologyAnnotation(term="SRA Inform On Status"),
                                                                   OntologyAnnotation(term="SRA Inform On Error")],
                                                            comments=[Comment(name="Study Person REF",
                                                                              value="https://orcid.org/0000-0002-6966-2972")]))

        for ps in isa_investigation.studies[0].process_sequence:
            print("PS: ", ps.inputs[0].name, "|", ps.outputs[0].name, "|", len(isa_investigation.studies[0].process_sequence))
            print("PS: ", ps.id)
            print("PS derives_from: ", ps.outputs[0].derives_from[-1].name)
            print("PS nextitem:", ps)
        for source in isa_investigation.studies[0].sources:
            print("SOURCES: ", source.name, "|", source.id)

        # for protocol in isa_investigation.studies[0].protocols:
        #     print("PROT: ", protocol.id, "|", protocol.name)

        for assay in isa_investigation.studies[0].assays:
            if "metabolite profiling" in assay.measurement_type.term:
                for ps in assay.process_sequence:
                    ps.performer = "University of Birmingham"
            elif "transcription profiling" in assay.measurement_type.term:
                for ps in assay.process_sequence:
                    ps.performer = "MGI Latvia"

        # isa_tables = dumpdf(isa_investigation)
        #
        # from isatools.model import _build_assay_graph
        # gph = _build_assay_graph(treatment_assay.process_sequence)

        # [print(key) for key in isa_tables.keys()]
        # print(isa_tables['s_study_01.txt'])
        # print(isa_tables['a_AT1_transcription-profiling_nucleotide-sequencing.txt'])
        # print(isa_tables['a_AT0_metabolite-profiling_mass-spectrometry.txt'])

        final_dir = os.path.abspath(os.path.join('notebook-output', 'sd-test'))

        isatab.dump(isa_obj=isa_investigation, output_path=final_dir,write_factor_values_in_assay_table=False)

        isa_j = json.dumps(isa_investigation, cls=ISAJSONEncoder, sort_keys=True, indent=4, separators=(',', ': '))
        with open(os.path.join(final_dir, "isa_as_json_from_dumps2.json"), "w") as isajson_output:
            # this call write the string 'isa_j' to the file called 'isa_as_json_from_dumps.json'
            isajson_output.write(isa_j)

        with open(os.path.join(final_dir, 'isa_as_json_from_dumps2.json')) as json_fp:
            json2isatab.convert(json_fp, os.path.join(final_dir, 'convert/c1'), validate_first=False)


if __name__ == '__main__':
    unittest.main()
