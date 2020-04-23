from isatools.create.connectors import assay_template_convert_json_to_ordered_dict, \
    assay_template_convert_ordered_dict_to_json

import unittest
import os
import json

from tests.test_create_models_study_design import ms_assay_dict


class TestMappings(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), 'data', 'json', 'create', 'templates', 'metabolite-profiling-ms.json'
            )
        )
        with open(file_path) as json_fp:
            self.json_mp_ms = json.load(json_fp)

    def test_assay_template_convert_json_to_ordered_dict_met_prof_mass_spec(self):
        actual_odict_mp_ms = assay_template_convert_json_to_ordered_dict(self.json_mp_ms)
        self.assertEqual(actual_odict_mp_ms, ms_assay_dict)

    def test_assay_template_convert_ordered_dict_to_json_met_prof_mass_spec(self):
        actual_json_mp_ms = assay_template_convert_ordered_dict_to_json(ms_assay_dict)
        self.assertEqual(actual_json_mp_ms, self.json_mp_ms)