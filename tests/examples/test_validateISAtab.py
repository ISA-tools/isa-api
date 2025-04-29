import unittest
from unittest.mock import patch, mock_open
import sys
from isatools.examples.validateISAtab import main


class TestValidateISATab(unittest.TestCase):

    @patch('isatools.examples.validateISAtab.isatab.validate')
    @patch('builtins.open', new_callable=mock_open, read_data='Sample ISA-Tab content')
    @patch('isatools.examples.validateISAtab.os.path.isfile', return_value=True)
    @patch('isatools.examples.validateISAtab.sys.exit')
    def test_valid_file(self, mock_exit, mock_isfile, mock_open_file, mock_validate):
        # Mock validation report
        mock_validate.return_value = {'errors': [], 'warnings': []}

        # Mock command-line arguments
        test_args = ['validateISAtab.py', 'valid_file.txt']
        with patch.object(sys, 'argv', test_args):
            main(sys.argv)

        # Assert no errors or warnings
        mock_validate.assert_called_once()
        mock_exit.assert_not_called()

    @patch('isatools.examples.validateISAtab.isatab.validate')
    @patch('builtins.open', new_callable=mock_open, read_data='Sample ISA-Tab content')
    @patch('isatools.examples.validateISAtab.os.path.isfile', return_value=True)
    @patch('isatools.examples.validateISAtab.sys.exit')
    def test_invalid_file(self, mock_exit, mock_open, mock_isfile, mock_validate):
        # Mock validation report with errors
        mock_validate.return_value = {'errors': ['Error 1'], 'warnings': []}

        # Mock command-line arguments
        test_args = ['validateISAtab.py', 'invalid_file.txt']
        with patch.object(sys, 'argv', test_args):
            main(sys.argv)

        # Assert errors were found
        mock_validate.assert_called_once()
        mock_exit.assert_called_once_with(1)

    # @patch('isatools.examples.validateISAtab.isatab.validate')
    @patch('isatools.examples.validateISAtab.os.path.isfile', return_value=False)
    @patch('isatools.examples.validateISAtab.sys.exit')
    def test_file_not_found(self, mock_isfile, mock_exit):
        # Mock command-line arguments
        test_args = ['validateISAtab.py', 1]
        with patch.object(sys, 'argv', test_args):
            main(sys.argv)

        # Assert file was skipped
        # mock_isfile.assert_called_once()
        mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
