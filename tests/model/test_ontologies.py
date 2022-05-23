from unittest import TestCase
from unittest.mock import patch

from isatools.model import OntologySource, OntologyAnnotation, Commentable


class TestOntologySource(TestCase):

    def setUp(self):
        self.ontology_source = OntologySource(name='test_name',
                                              file='test_file',
                                              version='test_version',
                                              description='test_description')

    def test_instance(self):
        self.assertTrue(isinstance(self.ontology_source, OntologySource))
        self.assertTrue(isinstance(self.ontology_source, Commentable))

    def test_properties(self):
        self.assertTrue(self.ontology_source.name == 'test_name')
        self.assertTrue(self.ontology_source.file == 'test_file')
        self.assertTrue(self.ontology_source.version == 'test_version')
        self.assertTrue(self.ontology_source.description == 'test_description')

    def test_setters(self):
        self.ontology_source.name = 'new_name'
        self.assertTrue(self.ontology_source.name == 'new_name')
        with self.assertRaises(AttributeError) as context:
            self.ontology_source.name = 1
        self.assertTrue("OntologySource.name must be a str; got 1:<class 'int'>" in str(context.exception))

        self.ontology_source.file = 'new_file'
        self.assertTrue(self.ontology_source.file == 'new_file')
        with self.assertRaises(AttributeError) as context:
            self.ontology_source.file = 1
        self.assertTrue("OntologySource.file must be a str; got 1:<class 'int'>" in str(context.exception))

        self.ontology_source.version = 'new_version'
        self.assertTrue(self.ontology_source.version == 'new_version')
        with self.assertRaises(AttributeError) as context:
            self.ontology_source.version = 1
        self.assertTrue("OntologySource.version must be a str; got 1:<class 'int'>" in str(context.exception))

        self.ontology_source.description = 'new_description'
        self.assertTrue(self.ontology_source.description == 'new_description')
        with self.assertRaises(AttributeError) as context:
            self.ontology_source.description = 1
        self.assertTrue("OntologySource.description must be a str; got 1:<class 'int'>" in str(context.exception))

        self.ontology_source = OntologySource(name='test_name',
                                              file='test_file',
                                              version='test_version',
                                              description='test_description')

    def test_builtins(self):
        expected_str_template = ("isatools.model.OntologySource(name='test_name', "
                                 "file='test_file', "
                                 "version='test_version', "
                                 "description='test_description', "
                                 "comments={comments})")
        expected_str = expected_str_template.format(comments=[])
        self.assertTrue(self.ontology_source.__repr__() == expected_str)
        expected_output_template = ("OntologySource(\n\t"
                                    "name=test_name\n\t"
                                    "file=test_file\n\t"
                                    "version=test_version\n\t"
                                    "description=test_description\n\t"
                                    "comments={num} Comment objects\n)")
        expected_output = expected_output_template.format(num=0)
        self.assertTrue(self.ontology_source.__str__() == expected_output)
        self.assertTrue(self.ontology_source.__hash__() == hash(expected_str))
        self.ontology_source.add_comment(name='test_name', value_='test_value')
        expected_output = expected_output_template.format(num=1)
        self.assertTrue(self.ontology_source.__str__() == expected_output)

        new_ontology_source = OntologySource(name='test_name')
        self.assertFalse(self.ontology_source == new_ontology_source)
        self.assertTrue(self.ontology_source != new_ontology_source)


class TestOntologyAnnotation(TestCase):

    def setUp(self):
        self.ontology_annotation = OntologyAnnotation(term='test_term',
                                                      term_source='test_term_source',
                                                      term_accession='test_term_accession')

    def test_instance(self):
        self.assertTrue(isinstance(self.ontology_annotation, OntologyAnnotation))
        self.assertTrue(isinstance(self.ontology_annotation, Commentable))

    @patch('isatools.model.ontologies.uuid4', return_value="i am a mocked UUID")
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
            self.ontology_annotation.term_source = 1
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
