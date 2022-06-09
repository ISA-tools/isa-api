from unittest import TestCase
from isatools.model.source import Source
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.characteristic import Characteristic
from isatools.model.comments import Comment
from isatools.model.loader_indexes import loader_states as indexes

expected_repr = "isatools.model.Source(name='', characteristics=[], comments=[])"


class TestSource(TestCase):

    def setUp(self):
        self.source = Source(id_='test_id')
        self.ontology_annotation = OntologyAnnotation(term='test_term')

    def test_init(self):
        characteristic = Characteristic(category=self.ontology_annotation)
        source = Source(name='sars-cov2', characteristics=[characteristic])
        self.assertTrue(source.name == 'sars-cov2')
        self.assertTrue(source.characteristics == [characteristic])

    def test_getters(self):
        self.assertTrue(self.source.name == '')
        self.assertTrue(self.source.id == 'test_id')

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
        self.source.characteristics = [Characteristic(category=self.ontology_annotation, value='', unit='')]

        self.assertTrue(self.source.characteristics[0].value == '')
        self.assertTrue(self.source.characteristics[0].unit == '')
        self.assertTrue(self.source.characteristics[0].category == self.ontology_annotation)

        with self.assertRaises(AttributeError) as context:
            self.source.characteristics = 1
        self.assertTrue("Source.characteristics must be iterable containing" in str(context.exception))

    def test_has_char(self):
        characteristic = Characteristic(category=self.ontology_annotation)
        self.source.characteristics = [characteristic]
        self.assertTrue(self.source.has_char('test_term'))
        self.assertTrue(self.source.has_char(characteristic))
        self.assertFalse(self.source.has_char('test_term_2'))
        self.assertFalse(self.source.has_char(1))

    def test_get_char(self):
        first_characteristic = Characteristic(category=self.ontology_annotation)
        second_characteristic = Characteristic(category=OntologyAnnotation(term='test_term_2'))
        self.source.characteristics = [first_characteristic, second_characteristic]
        self.assertTrue(self.source.get_char('test_term'), [first_characteristic])
        self.assertIsNone(self.source.get_char('foo'))

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

    def test_to_dict(self):
        self.source.id = 'test_id'
        self.source.comments = [Comment(name='test_comment')]
        expected_dict = {
            '@id': "test_id",
            'name': '',
            'characteristics': [],
            'comments': [{'name': 'test_comment', 'value': ''}]
        }
        self.assertEqual(self.source.to_dict(), expected_dict)

        ontology_annotation = OntologyAnnotation(term='test_term', id_='test_id')
        self.source.characteristics = [Characteristic(category=ontology_annotation)]
        expected_dict['characteristics'] = [
            {
                'category': {'@id': 'test_id'},
                'comments': [],
                'value': None
            }
        ]
        self.assertEqual(self.source.to_dict(), expected_dict)

    def test_from_dict(self):
        expected_dict = {
            "@id": "source_id",
            "name": "source name",
            "comments": [],
            "characteristics": []
        }
        source = Source()
        source.from_dict(expected_dict)
        self.assertEqual(source.to_dict(), expected_dict)

        expected_dict["characteristics"] = [
            {
                "category": {'@id': 'category_id'},
                "comments": [],
                "value": "123",
                'unit': ''
            }
        ]
        characteristics_index = {
            'category_id': OntologyAnnotation(term='my category', id_='my_cat_id')
        }
        indexes.characteristic_categories = characteristics_index
        source.from_dict(expected_dict)
        expected_characteristics = [
           {
               'category': {'@id': 'my_cat_id'},
               'value': '123',
               'comments': []
           }
        ]
        self.assertIsInstance(source.characteristics[0], Characteristic)
        self.assertEqual(source.to_dict()['characteristics'], expected_characteristics)