import unittest
import os
from performances.isajson import (
    profile_json_load,
    profile_json_dump,
    profile_validate,
    profile_isajson
)
from performances.defaults import DEFAULT_JSON_INPUT, OUTPUT_PATH


class TestISAJsonPerformance(unittest.TestCase):

    def setUp(self):
        # Ensure the output directory exists
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)

    def test_profile_json_load(self):
        # Test the profile_json_load function
        output_file = os.path.join(OUTPUT_PATH, 'isajson_load')
        profile_json_load(DEFAULT_JSON_INPUT, OUTPUT_PATH)
        self.assertTrue(os.path.exists(output_file))

    def test_profile_json_dump(self):
        # Test the profile_json_dump function
        output_file = os.path.join(OUTPUT_PATH, 'isajson_dump')
        profile_json_dump(DEFAULT_JSON_INPUT, OUTPUT_PATH)
        self.assertTrue(os.path.exists(output_file))

    def test_profile_validate(self):
        # Test the profile_validate function
        output_file = os.path.join(OUTPUT_PATH, 'isajson_validate')
        profile_validate(DEFAULT_JSON_INPUT, OUTPUT_PATH)
        self.assertTrue(os.path.exists(output_file))

    def test_profile_isajson(self):
        # Test the profile_isajson function
        load_output = os.path.join(OUTPUT_PATH, 'isajson_load')
        dump_output = os.path.join(OUTPUT_PATH, 'isajson_dump')
        validate_output = os.path.join(OUTPUT_PATH, 'isajson_validate')
        profile_isajson(DEFAULT_JSON_INPUT, OUTPUT_PATH)
        self.assertTrue(os.path.exists(load_output))
        self.assertTrue(os.path.exists(dump_output))
        self.assertTrue(os.path.exists(validate_output))

    def tearDown(self):
        # Clean up the output directory after tests
        for file in os.listdir(OUTPUT_PATH):
            file_path = os.path.join(OUTPUT_PATH, file)
            if os.path.isfile(file_path):
                os.remove(file_path)


if __name__ == '__main__':
    unittest.main()