from unittest import TestCase
from isatools.model.ontology_source import OntologySource
from isatools.model.comments import Commentable, Comment


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

    def test_validate_field(self):
        with self.assertRaises(AttributeError) as context:
            self.ontology_source.validate_field(1, 'name')
        self.assertTrue("OntologySource.name must be a str; got 1:<class 'int'>" in str(context.exception))
        self.assertIsNone(self.ontology_source.validate_field('test_name', 'name'))

    def test_to_dict(self):
        ontology_source = OntologySource(name='name1',
                                         version='version1',
                                         file='file1',
                                         description='description1',
                                         comments=[Comment(name='commentA', value='valueA')])
        expected_dict = {
            'name': 'name1',
            'version': 'version1',
            'comments': [{'name': 'commentA', 'value': 'valueA'}],
            'file': 'file1',
            'description': 'description1'
        }
        self.assertEqual(ontology_source.to_dict(), expected_dict)
