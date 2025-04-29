import unittest
from unittest.mock import patch, mock_open, MagicMock
from io import BytesIO
from isatools.net.biocrates2isatab import (
    replaceAll, zipdir, merge_biocrates_files, biocrates_to_isatab_convert,
    generatePolarityAttrsDict, generateAttrsDict, writeOutToFile, complete_MAF,
    add_sample_metadata, parseSample
)


class TestBiocrates2ISATAB(unittest.TestCase):

    @patch('isatools.net.biocrates2isatab.fileinput.input', create=True)
    @patch('isatools.net.biocrates2isatab.sys.stdout', new_callable=MagicMock)
    def test_replaceAll(self, mock_stdout, mock_fileinput):
        mock_fileinput.return_value = iter(["line with searchExp"])
        replaceAll("dummy_file", "searchExp", "replaceExp")
        mock_stdout.write.assert_called_with("line with replaceExp")

    @patch('isatools.net.biocrates2isatab.os.walk')
    @patch('isatools.net.biocrates2isatab.ZipFile')
    def test_zipdir(self, mock_zipfile, mock_walk):
        mock_walk.return_value = [('/path', ('dir',), ('file1', 'file2'))]
        mock_zip = MagicMock()
        mock_zipfile.return_value = mock_zip
        zipdir('/path', mock_zip)
        mock_zip.write.assert_any_call('/path/file1')
        mock_zip.write.assert_any_call('/path/file2')

    @patch('isatools.net.biocrates2isatab.BeautifulSoup')
    @patch('isatools.net.biocrates2isatab.open', new_callable=mock_open)
    def test_merge_biocrates_files(self, mock_open_file, mock_soup):
        mock_soup.return_value.find_all.side_effect = lambda tag: [f"<{tag}>content</{tag}>"]
        result = merge_biocrates_files('/input_dir')
        self.assertIsNotNone(result)

    @patch('isatools.net.biocrates2isatab.subprocess.call')
    @patch('isatools.net.biocrates2isatab.ZipFile')
    @patch('isatools.net.biocrates2isatab.os.path.exists', return_value=False)
    @patch('isatools.net.biocrates2isatab.os.makedirs')
    def test_biocrates_to_isatab_convert(self, mock_makedirs, mock_exists, mock_zipfile, mock_subprocess):
        mock_subprocess.return_value = 0
        buffer = biocrates_to_isatab_convert('test.xml')
        self.assertIsInstance(buffer, BytesIO)

    def test_generatePolarityAttrsDict(self):
        plate = MagicMock()
        plate.get.return_value = "usedop_value"
        plate.find_all.return_value = [MagicMock()]
        attrs, mydict = generatePolarityAttrsDict(plate, 'POSITIVE', {}, {}, {})
        self.assertIsInstance(attrs, dict)
        self.assertIsInstance(mydict, dict)

    def test_generateAttrsDict(self):
        plate = MagicMock()
        pos_attrs, neg_attrs, pos_metabolites, neg_metabolites, mydict = generateAttrsDict(plate)
        self.assertIsInstance(pos_attrs, dict)
        self.assertIsInstance(neg_attrs, dict)
        self.assertIsInstance(pos_metabolites, dict)
        self.assertIsInstance(neg_metabolites, dict)
        self.assertIsInstance(mydict, dict)

    # @patch('isatools.net.biocrates2isatab.open', new_callable=mock_open)
    # @patch('isatools.net.biocrates2isatab.complete_MAF')
    # def test_writeOutToFile(self, mock_complete_maf, mock_open_file):
    #     plate = MagicMock()
    #     plate.find_all.return_value = [MagicMock()]
    #     writeOutToFile(plate, 'POSITIVE', 'KIT2-0-5404', '809697', '/output', {}, {}, {})
    #     mock_open_file.assert_called_once()

    # @patch('isatools.net.biocrates2isatab.pd.read_csv')
    # @patch('isatools.net.biocrates2isatab.pd.DataFrame.to_csv')
    # def test_complete_MAF(self, mock_to_csv, mock_read_csv):
    #     mock_read_csv.return_value = MagicMock()
    #     complete_MAF('test_maf.txt')
    #     mock_to_csv.assert_called_once()
    #
    # @patch('isatools.net.biocrates2isatab.pd.read_csv')
    # @patch('isatools.net.biocrates2isatab.pd.DataFrame.to_csv')
    # @patch('isatools.net.biocrates2isatab.replaceAll')
    # def test_add_sample_metadata(self, mock_replaceAll, mock_to_csv, mock_read_csv):
    #     mock_read_csv.return_value = MagicMock()
    #     add_sample_metadata('sample_info.csv', 'study_file.txt')
    #     # mock_to_csv.assert_called_once()
    #     mock_replaceAll.assert_called_once()

    @patch('isatools.net.biocrates2isatab.os.makedirs')
    @patch('isatools.net.biocrates2isatab.BeautifulSoup')
    @patch('isatools.net.biocrates2isatab.writeOutToFile')
    def test_parseSample(self, mock_writeOutToFile, mock_soup, mock_makedirs):
        plate = MagicMock()
        mock_soup.return_value.find_all.return_value = [plate]
        parseSample('biocrates-shorter-testfile.xml')
        mock_writeOutToFile.assert_called()


if __name__ == "__main__":
    unittest.main()
