import unittest
from unittest.mock import patch, mock_open
import sys
from isatools.examples.validateISAjson import main


class TestValidateISAJSON(unittest.TestCase):

    @patch('isatools.examples.validateISAjson.isajson.validate')
    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    @patch('isatools.examples.validateISAjson.os.path.isfile', return_value=True)
    @patch('isatools.examples.validateISAjson.sys.exit')
    def test_valid_file(self, mock_exit, mock_isfile, mock_open_file, mock_validate):
        # Mock validation report
        mock_validate.return_value = {'errors': [], 'warnings': []}

        # Mock command-line arguments
        test_args = ['validateISAjson.py', 'valid_file.json']
        with patch.object(sys, 'argv', test_args):
            main(sys.argv)

        # Assert no errors or warnings
        mock_validate.assert_called_once()
        mock_exit.assert_not_called()

    @patch('isatools.examples.validateISAjson.isajson.validate')
    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    @patch('isatools.examples.validateISAjson.os.path.isfile', return_value=True)
    @patch('isatools.examples.validateISAjson.sys.exit')
    def test_invalid_file(self, mock_exit, mock_isfile, mock_open_file, mock_validate):
        # Mock validation report with errors
        mock_validate.return_value = {'errors': ['Error 1'], 'warnings': []}

        # Mock command-line arguments
        test_args = ['validateISAjson.py', 'invalid_file.json']
        with patch.object(sys, 'argv', test_args):
            main(sys.argv)

        # Assert errors were found
        mock_validate.assert_called_once()
        mock_exit.assert_called_once_with(1)

    @patch('isatools.examples.validateISAjson.os.path.isfile', return_value=False)
    @patch('isatools.examples.validateISAjson.sys.exit')
    def test_file_not_found(self, mock_exit, mock_isfile):
        # Mock command-line arguments
        test_args = ['validateISAjson.py', 'nonexistent_file.json']
        with patch.object(sys, 'argv', test_args):
            main(sys.argv)

        # Assert file was skipped
        mock_isfile.assert_called_once()
        mock_exit.assert_not_called()


if __name__ == '__main__':
    unittest.main()
