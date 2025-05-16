import unittest
import os
from performances.isatab import profile_validation, profile_loader, profile_isatab
from performances.defaults import DEFAULT_TAB_INPUT, OUTPUT_PATH

class TestISATabPerformance(unittest.TestCase):

    def setUp(self):
        # Ensure the output directory exists
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)

    def test_profile_validation(self):
        # Test the profile_validation function
        output_file = os.path.join(OUTPUT_PATH, 'isatab_validation')
        profile_validation(DEFAULT_TAB_INPUT, OUTPUT_PATH)
        self.assertTrue(os.path.exists(output_file))

    def test_profile_loader(self):
        # Test the profile_loader function
        output_file = os.path.join(OUTPUT_PATH, 'isatab_load')
        profile_loader(DEFAULT_TAB_INPUT, OUTPUT_PATH)
        self.assertTrue(os.path.exists(output_file))

    def test_profile_isatab(self):
        # Test the profile_isatab function
        validation_output = os.path.join(OUTPUT_PATH, 'isatab_validation')
        loader_output = os.path.join(OUTPUT_PATH, 'isatab_load')
        profile_isatab(DEFAULT_TAB_INPUT, OUTPUT_PATH)
        self.assertTrue(os.path.exists(validation_output))
        self.assertTrue(os.path.exists(loader_output))

    def tearDown(self):
        # Clean up the output directory after tests
        for file in os.listdir(OUTPUT_PATH):
            file_path = os.path.join(OUTPUT_PATH, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

if __name__ == '__main__':
    unittest.main()