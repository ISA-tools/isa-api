from isatools.create.connectors import assay_template_to_ordered_dict, assay_ordered_dict_to_template, \
    generate_study_design_from_config, generate_study_design_from_datascriptor_config

import unittest
import os
import json

from isatools.create.models import StudyDesign, StudyArm, StudyCell, SampleAndAssayPlan, Study, Investigation
from isatools.isajson import ISAJSONEncoder
from tests.create_sample_assay_plan_odicts import ms_assay_dict, annotated_ms_assay_dict


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

    # FIXME I suspect this is superseded as I changed the underlying model (double check)
    # At the very least it has to be renamed
    def test_generate_isa_study_design_from_datascriptor_model_simple(self):
        ds_design_config_file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), 'data', 'json', 'create', 'datascriptor', 'study-design-with-two-arms.json'
            )
        )
        with open(ds_design_config_file_path) as json_fp:
            ds_design_config = json.load(json_fp)
        # the first assay template is Metabolite Profiling - Mass Spec
        ds_design_config['events'][-2]['template'] = self.met_prof_jsons[0]
        # the second assay template is Metabolite Profiling - NMR
        ds_design_config['events'][-1]['template'] = self.met_prof_jsons[2]
        design = generate_study_design_from_config(ds_design_config)
        self.assertIsInstance(design, StudyDesign)
        self.assertEqual(len(design.study_arms), len(ds_design_config['arms']))
        for arm in design.study_arms:
            self.assertIsInstance(arm, StudyArm)
            for cell, samp_ass_plan in arm.arm_map.items():
                self.assertIsInstance(cell, StudyCell)
                self.assertIsInstance(samp_ass_plan, SampleAndAssayPlan)
        study = design.generate_isa_study()
        self.assertIsInstance(study, Study)
        investigation = Investigation(studies=[study])
        inv_json = json.dumps(
            investigation,
            cls=ISAJSONEncoder,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
        self.assertIsInstance(inv_json, str)

    def test_generate_study_design_from_datascriptor_config(self):
        ds_design_config_file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), 'data', 'json', 'create', 'datascriptor',
                'study-design-3-repeated-treatment.json'
            )
        )
        with open(ds_design_config_file_path) as json_fp:
            ds_design_config = json.load(json_fp)
        design = generate_study_design_from_datascriptor_config(ds_design_config)
        self.assertIsInstance(design, StudyDesign)
        self.assertEqual(len(design.study_arms), len(ds_design_config['selectedArms']))
        for arm in design.study_arms:
            self.assertIsInstance(arm, StudyArm)
            for cell, samp_ass_plan in arm.arm_map.items():
                self.assertIsInstance(cell, StudyCell)
                self.assertIsInstance(samp_ass_plan, SampleAndAssayPlan)
        study = design.generate_isa_study()
        self.assertIsInstance(study, Study)
        investigation = Investigation(studies=[study])
        inv_json = json.dumps(
            investigation,
            cls=ISAJSONEncoder,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
        self.assertIsInstance(inv_json, str)
