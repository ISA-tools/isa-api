from unittest import TestCase
from isatools.model.source import Source
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.characteristic import Characteristic

expected_repr = "isatools.model.Source(name='', characteristics=[], comments=[])"


class TestSource(TestCase):

    def setUp(self):
        self.source = Source()

    def test_getters(self):
        self.assertTrue(self.source.name == '')
        self.assertTrue(self.source.id == '')

    def test_name(self):
        self.assertTrue(self.source.name == '')
        self.source.name = 'test_name'
        self.assertTrue(self.source.name == 'test_name')

        with self.assertRaises(AttributeError) as context:
            self.source.name = 1
        self.assertTrue("Source.name must be a str or None; got 1:<class 'int'>" in str(context.exception))

        self.source.name = None
        self.assertIsNone(self.source.name)

    def test_characteristics(self):
        self.assertTrue(self.source.characteristics == [])
        self.source.characteristics = [Characteristic(category=OntologyAnnotation(term='test_term',
                                                                                  term_source="test_term_source",
                                                                                  term_accession="test_term_accession"),
                                                      value='',
                                                      unit=''
                                                      )]

        test_characteristics = [Characteristic(category=OntologyAnnotation(term='test_term',
                                                                           term_source="test_term_source",
                                                                           term_accession="test_term_accession"),
                                               value='',
                                               unit=''
                                               )]

        self.assertTrue(self.source.characteristics == test_characteristics)

        expected_string = ("Characteristic(\n\t"
                           "category=test_term\n\t"
                           "value=\n\t"
                           "unit=\n\t"
                           "comments=0 Comment objects\n"
                           ")")

        self.assertTrue(str(self.source.characteristics[0]) == expected_string)

        with self.assertRaises(AttributeError) as context:
            self.source.characteristics = 1
        self.assertTrue("Source.characteristics must be iterable containing" in str(context.exception))

    def test_repr(self):
        self.assertTrue(repr(self.source) == expected_repr)

    def test_str(self):
        expected_str = ("Source(\n\t"
                        "name=\n\t"
                        "characteristics=0 Characteristic objects\n\t"
                        "comments=0 Comment objects\n)")
        self.assertTrue(str(self.source) == expected_str)

    def test_hash(self):
        self.assertTrue(hash(self.source) == hash(expected_repr))

    def test_equalities(self):
        source_a = Source(name='sars-cov2', characteristics=None)
        source_b = Source(name='sars-cov2', characteristics=None)
        self.assertTrue(source_a == source_b)
        self.assertTrue(source_a != self.source)
