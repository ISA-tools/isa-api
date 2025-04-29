import unittest
from unittest.mock import patch, MagicMock
from isatools.net import pubmed
from isatools.model import Publication


class TestGetPubmedArticle(unittest.TestCase):

    @patch("Bio.Medline.parse")
    @patch("Bio.Entrez.efetch")
    def test_valid_pubmed_response_with_doi(self, mock_efetch, mock_medline_parse):
        mock_handle = MagicMock()
        mock_efetch.return_value = mock_handle

        mock_medline_parse.return_value = iter([{
            "TI": "Sample Article Title",
            "AU": ["Author A", "Author B"],
            "TA": "Sample Journal",
            "EDAT": "2020/01/01 00:00",
            "LID": "10.1234/exampledoi [doi]",
        }])

        expected = {
            "pubmedid": "123456",
            "title": "Sample Article Title",
            "authors": ["Author A", "Author B"],
            "journal": "Sample Journal",
            "year": "2020",
            "doi": "10.1234/exampledoi",
        }

        result = pubmed.get_pubmed_article("123456")
        self.assertEqual(result, expected)

    @patch("Bio.Medline.parse")
    @patch("Bio.Entrez.efetch")
    def test_pubmed_response_with_aid_doi(self, mock_efetch, mock_medline_parse):
        mock_efetch.return_value = MagicMock()

        mock_medline_parse.return_value = iter([{
            "TI": "Another Title",
            "AU": ["C. Author"],
            "TA": "Another Journal",
            "EDAT": "2019/05/15 00:00",
            "LID": "",
            "AID": ["10.5678/alt-doi [doi]", "SOMEID [pii]"]
        }])

        result = pubmed.get_pubmed_article("654321")

        self.assertEqual(result["pubmedid"], "654321")
        self.assertEqual(result["doi"], "10.5678/alt-doi")
        self.assertEqual(result["title"], "Another Title")
        self.assertEqual(result["authors"], ["C. Author"])
        self.assertEqual(result["journal"], "Another Journal")
        self.assertEqual(result["year"], "2019")

    @patch("Bio.Medline.parse")
    @patch("Bio.Entrez.efetch")
    def test_pubmed_response_no_doi(self, mock_efetch, mock_medline_parse):
        mock_efetch.return_value = MagicMock()

        mock_medline_parse.return_value = iter([{
            "TI": "No DOI Title",
            "AU": [],
            "TA": "Journal X",
            "EDAT": "2018/12/31 00:00",
        }])

        result = pubmed.get_pubmed_article("999999")

        self.assertEqual(result["doi"], "")
        self.assertEqual(result["year"], "2018")
        self.assertEqual(result["title"], "No DOI Title")
        self.assertEqual(result["authors"], [])
        self.assertEqual(result["journal"], "Journal X")

#
# class Comment:
#     def __init__(self, name, value):
#         self.name = name
#         self.value = value


# class Publication:
#     def __init__(self, pubmed_id):
#         self.pubmed_id = pubmed_id
#         self.doi = None
#         self.author_list = None
#         self.title = None
#         self.comments = []


# class TestSetPubmedArticle(unittest.TestCase):
#
#     @patch("pubmed.get_pubmed_article")
#     def test_sets_publication_fields_correctly(self, mock_get_pubmed_article):
#         # Given mock response from PubMed
#         mock_get_pubmed_article.return_value = {
#             "pubmedid": "123456",
#             "title": "Mocked Title",
#             "authors": ["Alice Smith", "Bob Jones"],
#             "journal": "Mock Journal",
#             "year": "2021",
#             "doi": "10.1234/mock.doi"
#         }
#
#         pub = Publication(pubmed_id="123456")
#         pubmed.set_pubmed_article(pub)
#
#         self.assertEqual(pub.doi, "10.1234/mock.doi")
#         self.assertEqual(pub.author_list, "Alice Smith, Bob Jones")
#         self.assertEqual(pub.title, "Mocked Title")
#         self.assertEqual(len(pub.comments), 1)
#         self.assertEqual(pub.comments[0].name, "Journal")
#         self.assertEqual(pub.comments[0].value, "Mock Journal")
#
#     def test_raises_type_error_on_invalid_input(self):
#         with self.assertRaises(TypeError):
#             pubmed.set_pubmed_article("not_a_publication")


if __name__ == "__main__":
    unittest.main()
