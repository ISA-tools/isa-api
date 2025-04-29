import unittest
from unittest.mock import patch
from isatools.model import Investigation
from isatools.examples.modifyInvestigationOnly import modify_investigation


class TestModifyInvestigationOnly(unittest.TestCase):

    @patch('isatools.examples.modifyInvestigationOnly.modify_investigation')
    def test_modify_investigation_updates_title(self, mock_modify_investigation):
        # Create a mock investigation object
        investigation = Investigation(identifier="i1", title="Old Title")

        # Mock the function to modify the investigation title
        mock_modify_investigation.return_value = Investigation(
            identifier="i1", title="New Title"
        )

        # Call the function
        updated_investigation = mock_modify_investigation(investigation)

        # Assert the title was updated
        self.assertEqual(updated_investigation.title, "New Title")

    @patch('isatools.examples.modifyInvestigationOnly.modify_investigation')
    def test_modify_investigation_preserves_identifier(self, mock_modify_investigation):
        # Create an investigation object
        investigation = Investigation(identifier="i1", title="Old Title")

        # Mock the function to modify the investigation title
        mock_modify_investigation.return_value = Investigation(
            identifier="i1", title="New Title"
        )

        # Call the function
        updated_investigation = mock_modify_investigation(investigation)

        # Assert the identifier remains unchanged
        self.assertEqual(updated_investigation.identifier, "i1")



if __name__ == '__main__':
    unittest.main()
