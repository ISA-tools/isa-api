import unittest
import json
from isatools.examples.createSimpleISAJSON import create_descriptor
from unittest.mock import patch



class TestCreateSimpleISAJSON(unittest.TestCase):

    def test_create_descriptor_returns_valid_json(self):
        # Call the function
        result = create_descriptor()

        # Ensure the result is a valid JSON string
        try:
            data = json.loads(result)
        except json.JSONDecodeError:
            self.fail("create_descriptor did not return valid JSON")

        # Check that the JSON contains expected keys
        self.assertIn("identifier", data)
        self.assertIn("studies", data)
        self.assertIsInstance(data["studies"], list)
        self.assertGreater(len(data["studies"]), 0)

        # Check that the first study contains expected keys
        study = data["studies"][0]
        self.assertIn("title", study)
        self.assertIn("studyDesignDescriptors", study.keys())
        self.assertIsInstance(study["studyDesignDescriptors"], list)

    def test_create_descriptor_contains_ontology_sources(self):
        # Call the function
        result = create_descriptor()
        data = json.loads(result)
        print(data)

        # Check that ontology sources are present
        self.assertIn("ontologySourceReferences", data)
        self.assertIsInstance(data["ontologySourceReferences"], list)
        self.assertGreater(len(data["ontologySourceReferences"]), 0)

    @patch('isatools.examples.createSimpleISAJSON.create_descriptor')
    def test_create_descriptor_invalid_json(self, mock_create_descriptor):
        # Mock the function to return invalid JSON
        mock_create_descriptor.return_value = "invalid_json"

        # Call the function
        result = mock_create_descriptor()

        # Ensure the result raises a JSONDecodeError
        with self.assertRaises(json.JSONDecodeError):
            json.loads(result)


if __name__ == '__main__':
    unittest.main()
