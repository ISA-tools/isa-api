from collections import OrderedDict

from isatools import isatab
from isatools.create.connectors import (
    assay_template_to_ordered_dict,
    assay_ordered_dict_to_template,
    generate_study_design,
    generate_assay_ord_dict_from_config
)

import unittest
import os
import json

from isatools.model import (
    Characteristic,
    OntologyAnnotation
)
from isatools.model import (
    Study,
    Investigation,
    Sample
)
from isatools.create.model import (
    StudyDesign,
    StudyArm,
    StudyCell,
    SampleAndAssayPlan,
    AssayGraph
)
from isatools.create.constants import DATA_FILE, DEFAULT_EXTENSION
from isatools.create.constants import DEFAULT_STUDY_IDENTIFIER, BASE_FACTORS, IS_TREATMENT_EPOCH, SEQUENCE_ORDER_FACTOR_
from isatools.isajson import ISAJSONEncoder
from isatools.tests.create_sample_assay_plan_odicts import (
    ms_assay_dict,
    annotated_ms_assay_dict
)

SLOW_TESTS = int(os.getenv('SLOW_TESTS', '0'))


class TestMappings(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.met_prof_jsons = []
        filenames = (
            'metabolite-profiling-ms.json',
            'metabolite-profiling-ms-annotated.json',
            'metabolite-profiling-nmr.json'
        )
        for filename in filenames:
            file_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    'data', 'json', 'create', 'templates',
                    filename
                )
            )
            with open(file_path) as json_fp:
                self.met_prof_jsons.append(json.load(json_fp))

    def test_assay_template_convert_json_to_ordered_dict_met_prof_mass_spec(self):
        actual_odict_mp_ms = assay_template_to_ordered_dict(self.met_prof_jsons[0])
        self.assertEqual(actual_odict_mp_ms, ms_assay_dict)

    def test_assay_template_convert_json_to_ordered_dict_met_prof_mass_spec_annotated(self):
        actual_annotated_odict_mp_ms = assay_template_to_ordered_dict(self.met_prof_jsons[1])
        self.assertEqual(actual_annotated_odict_mp_ms, annotated_ms_assay_dict)

    def test_assay_template_convert_ordered_dict_to_json_met_prof_mass_spec(self):
        actual_json_mp_ms = assay_ordered_dict_to_template(ms_assay_dict)
        self.assertEqual(actual_json_mp_ms, self.met_prof_jsons[0])

    def test_assay_template_convert_ordered_dict_to_json_met_prof_mass_spec_annotated(self):
        actual_annotated_json_mp_ms = assay_ordered_dict_to_template(annotated_ms_assay_dict)
        self.assertEqual(actual_annotated_json_mp_ms, {
            key: value for key, value in self.met_prof_jsons[1].items() if key not in ['@context']
        })

    @staticmethod
    def _load_config(file_name):
        ds_design_config_file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), 'data', 'json', 'create', 'datascriptor',
                file_name
            )
        )
        with open(ds_design_config_file_path) as json_fp:
            ds_design_config = json.load(json_fp)
        return ds_design_config

    def test_generate_assay_ord_dict_from_datascriptor_config(self):
        ds_design_config = self._load_config('factorial-study-design-12-arms-blood-saliva-genomeseq-ms.json')
        assay_config = ds_design_config['assayPlan'][0]
        test_arm_name = ds_design_config['arms']['selected'][0]['name']
        test_epoch_no = -1   # last epoch, follow-up
        assay_odict = generate_assay_ord_dict_from_config(assay_config, test_arm_name, test_epoch_no)
        self.assertIsInstance(assay_odict, OrderedDict)
        assay_graph = AssayGraph.generate_assay_plan_from_dict(assay_odict)
        self.assertIsInstance(assay_graph, AssayGraph)

    def test_generate_assay_ord_dict_from_datascriptor_config_fail_missing_param_value(self):
        assay_config_with_empty_param_value = self._load_config('assay-empty-param-value.json')
        test_arm_name = next(key for key in assay_config_with_empty_param_value['selectedCells'].keys())
        test_epoch_no = -1  # last epoch, follow-up
        self.assertRaises(
            ValueError, generate_assay_ord_dict_from_config, assay_config_with_empty_param_value,
            test_arm_name, test_epoch_no
        )

    def test_generate_assay_ord_dict_from_datascriptor_config_fail_missing_char_value(self):
        assay_config_with_empty_param_value = self._load_config('assay-empty-characteristic-value.json')
        test_arm_name = next(key for key in assay_config_with_empty_param_value['selectedCells'].keys())
        test_epoch_no = -1  # last epoch, follow-up
        self.assertRaises(
            ValueError, generate_assay_ord_dict_from_config, assay_config_with_empty_param_value,
            test_arm_name, test_epoch_no
        )

    def test_generate_assay_ord_dict_from_config_file_extension(self):
        ds_study_config = self._load_config('crossover-study-human.json')
        marker_panel_assay_plan_config = ds_study_config['design']['assayPlan'][0]
        self.assertEqual(marker_panel_assay_plan_config['name'], 'hematology by marker panel')
        assay_odict = generate_assay_ord_dict_from_config(
            marker_panel_assay_plan_config, arm_name="Arm_0", epoch_no=1
        )
        assay_graph = AssayGraph.generate_assay_plan_from_dict(assay_odict)
        self.assertIsInstance(assay_graph, AssayGraph)
        file_node = next(node for node in assay_graph.nodes if getattr(node, 'type', None) == DATA_FILE)
        self.assertEqual(file_node.name, marker_panel_assay_plan_config['workflow'][-1][0])
        self.assertTrue(file_node.extension, DEFAULT_EXTENSION)

    def test_generate_study_design(self):
        ds_study_config = self._load_config('factorial-sweeteners-study.json')
        ds_design_config = ds_study_config['design']
        design = generate_study_design(ds_study_config)
        self.assertIsInstance(design, StudyDesign)
        self.assertEqual(len(design.study_arms), len(ds_design_config['arms']['selected']))
        for arm in design.study_arms:
            self.assertIsInstance(arm, StudyArm)
            for cell, samp_ass_plan in arm.arm_map.items():
                self.assertIsInstance(cell, StudyCell)
                self.assertIsInstance(samp_ass_plan, SampleAndAssayPlan)
        study = design.generate_isa_study()
        self.assertIsInstance(study, Study)
        self.assertEqual(study.title, ds_study_config['name'])
        self.assertEqual(study.identifier, ds_study_config['_id'])
        self.assertEqual(study.description, ds_study_config['description'])
        self.assertIsInstance(study.design_descriptors[0], OntologyAnnotation)
        self.assertEqual(study.design_descriptors[0].term, ds_design_config['designType']['term'])
        self.assertEqual(study.design_descriptors[0].term_accession, ds_design_config['designType']['iri'])
        counter = 0
        nb_epochs = len(ds_design_config['arms']['selected'][0]['epochs'])
        for sample in study.samples:
            self.assertIsInstance(sample, Sample)
            self.assertTrue(len(sample.factor_values), 3)
            is_treatment = next(comment for comment in sample.comments if comment.name == IS_TREATMENT_EPOCH)
            self.assertIn(is_treatment.value, ('YES', 'NO'))
            sequence_no = next(
                fv for fv in sample.factor_values if fv.factor_name.name == SEQUENCE_ORDER_FACTOR_['name']
            )
            self.assertGreaterEqual(sequence_no.value, 0)
            self.assertLess(sequence_no.value, nb_epochs)
            try:
                agent_fv = next(fv for fv in sample.factor_values if fv.factor_name.name == 'AGENT')
                intensity_fv = next(fv for fv in sample.factor_values if fv.factor_name.name == 'INTENSITY')
                duration_fv = next(fv for fv in sample.factor_values if fv.factor_name.name == 'DURATION')
                self.assertIn(agent_fv.value, ds_design_config['treatmentPlan']['elementParams']['agents'])
                self.assertIn(intensity_fv.value, ds_design_config['treatmentPlan']['elementParams']['intensities'])
                self.assertIn(duration_fv.value, ds_design_config['treatmentPlan']['elementParams']['durations'])
                counter += 1
            except StopIteration:
                continue
        ms_assay = next(
            assay for assay in study.assays if assay.filename.endswith('mass-spectrometry.txt')
        )
        self.assertTrue(
            all(data_file.filename.split('.')[-1] == 'mzML' for data_file in ms_assay.data_files)
        )
        self.assertGreater(counter, 0)      # at least one sample must have factor value annotations
        investigation = Investigation(studies=[study])
        inv_json = json.dumps(
            investigation,
            cls=ISAJSONEncoder,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
        self.assertIsInstance(inv_json, str)
        if SLOW_TESTS:
            data_frames = isatab.dump_tables_to_dataframes(investigation)
            self.assertIsInstance(data_frames, dict)
            self.assertGreater(len(data_frames), 1)

    def test_generate_study_design_observational(self):
        ds_study_config = self._load_config('observational-study-students.json')
        design = generate_study_design(ds_study_config)
        ds_design_config = ds_study_config['design']
        self.assertIsInstance(design, StudyDesign)
        self.assertEqual(len(design.study_arms), len(ds_design_config['arms']['selected']))
        for arm in design.study_arms:
            self.assertIsInstance(arm, StudyArm)
            for cell, samp_ass_plan in arm.arm_map.items():
                self.assertIsInstance(cell, StudyCell)
                self.assertIsInstance(samp_ass_plan, SampleAndAssayPlan)
        study = design.generate_isa_study()
        self.assertIsInstance(study, Study)
        self.assertEqual(study.title, ds_study_config['name'])
        self.assertEqual(study.identifier, ds_study_config['_id'])
        self.assertEqual(study.description, ds_study_config['description'])
        self.assertIsInstance(study.design_descriptors[0], OntologyAnnotation)
        self.assertEqual(study.design_descriptors[0].term, ds_design_config['designType']['term'])
        self.assertEqual(study.design_descriptors[0].term_accession, ds_design_config['designType']['iri'])
        for sample in study.samples:
            self.assertIsInstance(sample, Sample)
        investigation = Investigation(studies=[study])
        inv_json = json.dumps(
            investigation,
            cls=ISAJSONEncoder,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
        self.assertIsInstance(inv_json, str)
        if SLOW_TESTS:
            data_frames = isatab.dump_tables_to_dataframes(investigation)
            self.assertIsInstance(data_frames, dict)
            self.assertGreater(len(data_frames), 1)

    # in this test subject and samples are ontology annotations
    def test_generate_study_design_with_observational_factors_and_ontology_annotations(self):
        ds_study_config = self._load_config('crossover-study-dietary-dog.json')
        design = generate_study_design(ds_study_config)
        ds_design_config = ds_study_config['design']
        self.assertIsInstance(design, StudyDesign)
        for ix, arm in enumerate(design.study_arms):
            self.assertIsInstance(arm, StudyArm)
            self.assertIsInstance(arm.source_type, Characteristic)
            self.assertIsInstance(arm.source_characteristics, set)
            self.assertEqual(len(arm.source_characteristics), len(ds_design_config['observationalFactors']))
            for source_char in arm.source_characteristics:
                self.assertIsInstance(source_char, Characteristic)
                self.assertIsInstance(source_char.category, OntologyAnnotation)
                self.assertIsInstance(source_char.value, OntologyAnnotation)
        investigation = Investigation(studies=[design.generate_isa_study()])
        # two assay types are selected, so we expect to find only two assays in the studies
        self.assertEqual(len(investigation.studies[0].assays), 2)
        if SLOW_TESTS:
            inv_json = json.dumps(
                investigation,
                cls=ISAJSONEncoder,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
            inv_dict = json.loads(inv_json)
            self.assertIsInstance(inv_dict, dict)
            data_frames = isatab.dump_tables_to_dataframes(investigation)
            self.assertIsInstance(data_frames, dict)

    # in this test subject and samples are ontology annotations
    def test_generate_study_design_with_chained_protocols_and_ontology_annotations(self):
        ds_study_config = self._load_config('crossover-study-human.json')
        design = generate_study_design(ds_study_config)
        ds_design_config = ds_study_config['design']
        self.assertIsInstance(design, StudyDesign)
        investigation = Investigation(studies=[design.generate_isa_study()])
        self.assertIsInstance(investigation.studies[0], Study)
        self.assertEqual(len(investigation.studies[0].assays), len(ds_design_config['assayPlan']))
        sequencing_assay = next(
            assay for assay in investigation.studies[0].assays if assay.filename.endswith('nucleic-acid-sequencing.txt')
        )
        self.assertTrue(
            all(data_file.filename.split('.')[-1] == 'raw' for data_file in sequencing_assay.data_files)
        )
        marker_panel_assay = next(
            assay for assay in investigation.studies[0].assays if assay.filename.endswith('marker-panel.txt')
        )
        marker_panel_samples = [
            proc.inputs[0] for proc in marker_panel_assay.process_sequence
            if proc.executes_protocol.name == 'sample preparation'
        ]
        blood_sample = ds_design_config['samplePlan'][0]['sampleType']
        self.assertTrue(
            all(sample.characteristics[0].value.term == blood_sample['term'] for sample in marker_panel_samples)
        )
        self.assertTrue(
            all(sample.characteristics[0].value.term_accession == blood_sample['iri'] for sample in marker_panel_samples)
        )
        self.assertTrue(
            all(data_file.filename.split('.')[-1] == 'raw' for data_file in marker_panel_assay.data_files)
        )
        if SLOW_TESTS:
            json.dumps(
                investigation,
                cls=ISAJSONEncoder,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
            data_frames = isatab.dump_tables_to_dataframes(investigation)
            self.assertIsInstance(data_frames, dict)
            self.assertEqual(len(data_frames), len(ds_design_config['assayPlan']) + 1)
