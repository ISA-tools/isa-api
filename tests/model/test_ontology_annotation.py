from unittest import TestCase
from unittest.mock import patch

from isatools.model import OntologySource, OntologyAnnotation, Commentable


class TestOntologyAnnotation(TestCase):

    def setUp(self):
        self.ontology_annotation = OntologyAnnotation(term='test_term',
                                                      term_source='test_term_source',
                                                      term_accession='test_term_accession')

    def test_instance(self):
        self.assertTrue(isinstance(self.ontology_annotation, OntologyAnnotation))
        self.assertTrue(isinstance(self.ontology_annotation, Commentable))

    @patch('isatools.model.ontology_annotation.uuid4', return_value="i am a mocked UUID")
    def test_properties(self, mock_uuid):
        self.assertTrue(self.ontology_annotation.term == 'test_term')
        self.assertTrue(self.ontology_annotation.term_source == 'test_term_source')
        self.assertTrue(self.ontology_annotation.term_accession == 'test_term_accession')
        ontology_annotation_with_id = OntologyAnnotation(id_='I am NOT an uuid')
        self.assertTrue(ontology_annotation_with_id.id == 'I am NOT an uuid')
        ontology_annotation_mocked_id = OntologyAnnotation(term='test_term')
        self.assertTrue(ontology_annotation_mocked_id.id == "i am a mocked UUID")

    def test_setters(self):
        self.ontology_annotation.term = None
        self.assertIsNone(self.ontology_annotation.term)
        with self.assertRaises(AttributeError) as context:
            self.ontology_annotation.term = 1
        self.assertTrue("OntologyAnnotation.term must be a str or None; got 1:<class 'int'>" in str(context.exception))

        self.ontology_annotation.term_source = None
        self.assertIsNone(self.ontology_annotation.term_source)
        self.ontology_annotation.term_source = OntologySource(name='test_source_name')
        self.assertTrue(isinstance(self.ontology_annotation.term_source, OntologySource))
        self.assertTrue(self.ontology_annotation.term_source.name == 'test_source_name')
        with self.assertRaises(AttributeError) as context:
            self.ontology_annotation.term_source = "term-source"
        self.assertTrue("OntologyAnnotation.term_source must be a OntologySource or None; got term-source:<class 'str'>"
                        in str(context.exception))

        self.ontology_annotation.term_accession = None
        self.assertIsNone(self.ontology_annotation.term_accession)
        with self.assertRaises(AttributeError) as context:
            self.ontology_annotation.term_accession = 1
        self.assertTrue("OntologyAnnotation.term_accession must be a str or None" in str(context.exception))

    def test_builtins(self):
        expected_str = ("isatools.model.OntologyAnnotation(term='test_term', "
                        "term_source='test_term_source', "
                        "term_accession='test_term_accession', "
                        "comments=[])")
        expected_hash = hash(expected_str)
        self.assertTrue(self.ontology_annotation.__repr__() == expected_str)
        self.assertTrue(self.ontology_annotation.__hash__() == expected_hash)

        expected_str = ("OntologyAnnotation(\n\t"
                        "term=test_term\n\t"
                        "term_source=test_term_source\n\t"
                        "term_accession=test_term_accession\n\t"
                        "comments=0 Comment objects\n)")
        self.assertTrue(self.ontology_annotation.__str__() == expected_str)
        self.ontology_annotation.term_source = OntologySource(name='anotherSourceName')
        expected_str = ("OntologyAnnotation(\n\t"
                        "term=test_term\n\t"
                        "term_source=anotherSourceName\n\t"
                        "term_accession=test_term_accession\n\t"
                        "comments=0 Comment objects\n)")
        self.assertTrue(self.ontology_annotation.__str__() == expected_str)

        self.assertTrue(self.ontology_annotation != 123)
        self.assertFalse(self.ontology_annotation == 123)
