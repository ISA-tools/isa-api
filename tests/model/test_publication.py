from unittest import TestCase

from isatools.model.publication import Publication
from isatools.model.ontology_annotation import OntologyAnnotation


expected_repr = ("isatools.model.Publication(pubmed_id='', doi='', author_list='', "
                 "title='', status=None, comments=[])")


class TestPublication(TestCase):

    def setUp(self):
        self.publication = Publication()

    def test_pubmed(self):
        self.assertTrue(self.publication.pubmed_id == '')
        self.publication.pubmed_id = "12345"
        self.assertEqual(self.publication.pubmed_id, "12345")

        with self.assertRaises(AttributeError) as context:
            self.publication.pubmed_id = 1
        self.assertTrue("Publication.pubmed_id must be a str or None; got 1:<class 'int'>" in str(context.exception))

    def test_doi(self):
        self.assertTrue(self.publication.doi == '')
        self.publication.doi = "12345"
        self.assertEqual(self.publication.doi, "12345")

        with self.assertRaises(AttributeError) as context:
            self.publication.doi = 1
        self.assertTrue("Publication.doi must be a str or None; got 1:<class 'int'>" in str(context.exception))

    def test_author_list(self):
        self.assertTrue(self.publication.author_list == '')
        self.publication.author_list = "12345"
        self.assertEqual(self.publication.author_list, "12345")

        with self.assertRaises(AttributeError) as context:
            self.publication.author_list = 1
        self.assertTrue("Publication.author_list must be a str or None; got 1:<class 'int'>" in str(context.exception))

    def test_title(self):
        self.assertTrue(self.publication.title == '')
        self.publication.title = "12345"
        self.assertEqual(self.publication.title, "12345")

        with self.assertRaises(AttributeError) as context:
            self.publication.title = 1
        self.assertTrue("Publication.title must be a str or None; got 1:<class 'int'>" in str(context.exception))

    def test_status(self):
        self.assertIsNone(self.publication.status)
        ontology_annotation = OntologyAnnotation(term="12345")
        self.publication.status = ontology_annotation
        self.assertEqual(self.publication.status, ontology_annotation)

        with self.assertRaises(AttributeError) as context:
            self.publication.status = 1
        self.assertTrue("Publication.status must be a OntologyAnnotation or "
                        "None; got 1:<class 'int'>" in str(context.exception))

    def test_repr(self):
        self.assertTrue(repr(self.publication) == expected_repr)

    def test_str(self):
        expected_str = ("Publication(\n\t"
                        "pubmed_id=\n\t"
                        "doi=\n\t"
                        "author_list=\n\t"
                        "title=\n\t"
                        "status=\n\t"
                        "comments=0 Comment objects\n)")
        self.assertTrue(str(self.publication) == expected_str)

    def test_hash(self):
        self.assertTrue(hash(self.publication) == hash(expected_repr))

    def test_equalities(self):
        second_publication = Publication(doi='123', pubmed_id='123', author_list='123', title='123', status=None)
        third_publication = Publication(doi='123', pubmed_id='123', author_list='123', title='123', status=None)
        self.assertTrue(second_publication == third_publication)
        self.assertTrue(second_publication != self.publication)
