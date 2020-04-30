from isatools.create.connectors import assay_template_convert_json_to_ordered_dict, \
    assay_template_convert_ordered_dict_to_json

import unittest
import os
import json

from tests.create_sample_assay_plan_odicts import ms_assay_dict, annotated_ms_assay_dict


class TestMappings(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.mp_ms_jsons = []
        filenames = ('metabolite-profiling-ms.json', 'metabolite-profiling-ms-annotated.json')
        for filename in filenames:
            file_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    'data', 'json', 'create', 'templates',
                    filename
                )
            )
            with open(file_path) as json_fp:
                self.mp_ms_jsons.append(json.load(json_fp))

    def test_assay_template_convert_json_to_ordered_dict_met_prof_mass_spec(self):
        actual_odict_mp_ms = assay_template_convert_json_to_ordered_dict(self.mp_ms_jsons[0])
        self.assertEqual(actual_odict_mp_ms, ms_assay_dict)

    def test_assay_template_convert_json_to_ordered_dict_met_prof_mass_spec_annotated(self):
        actual_annotated_odict_mp_ms = assay_template_convert_json_to_ordered_dict(self.mp_ms_jsons[1])
        self.assertEqual(actual_annotated_odict_mp_ms, annotated_ms_assay_dict)

    def test_assay_template_convert_ordered_dict_to_json_met_prof_mass_spec(self):
        actual_json_mp_ms = assay_template_convert_ordered_dict_to_json(ms_assay_dict)
        self.assertEqual(actual_json_mp_ms, self.mp_ms_jsons[0])

    def test_assay_template_convert_ordered_dict_to_json_met_prof_mass_spec_annotated(self):
        actual_annotated_json_mp_ms = assay_template_convert_ordered_dict_to_json(annotated_ms_assay_dict)
        self.assertEqual(actual_annotated_json_mp_ms, {
            key: value for key, value in self.mp_ms_jsons[1].items() if key not in ['@context']
        })

    def test_generate_isa_study_design_from_datascriptor_model(self):
        # TODO load Datascriptor model and test it here
        self.assertFalse(True)

