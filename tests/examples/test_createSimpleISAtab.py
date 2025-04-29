import unittest
from isatools.examples.createSimpleISAtab import create_descriptor


class TestCreateSimpleISATab(unittest.TestCase):

    def test_create_descriptor_returns_valid_isatab(self):
        # Call the function
        result = create_descriptor()

        # Ensure the result is a non-empty string
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_create_descriptor_contains_investigation(self):
        # Call the function
        result = create_descriptor()

        # Check that the ISA-Tab contains the investigation identifier
        self.assertIn("i1", result)
        self.assertIn("My Simple ISA Investigation", result)

    def test_create_descriptor_contains_study(self):
        # Call the function
        result = create_descriptor()

        # Check that the ISA-Tab contains the study identifier and title
        self.assertIn("s1", result)
        self.assertIn("My ISA Study", result)

    def test_create_descriptor_contains_assay(self):
        # Call the function
        result = create_descriptor()

        # Check that the ISA-Tab contains the assay filename
        self.assertIn("a_assay.txt", result)


if __name__ == '__main__':
    unittest.main()
