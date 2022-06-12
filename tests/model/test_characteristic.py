from unittest import TestCase
from unittest.mock import patch

from isatools.model.characteristic import Characteristic
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.loader_indexes import loader_states as indexes

class TestCharacteristic(TestCase):

    def setUp(self):
        self.characteristic = Characteristic(category='test_category', value='test_value', unit='test_unit')

    def test_constructor(self):
        characteristic = Characteristic(value='test_value', unit='test_unit')
        self.assertIsNone(characteristic.category)
        self.assertTrue(isinstance(self.characteristic.category, OntologyAnnotation))

    def test_category(self):
        self.characteristic.category = 'test_category'
        self.assertEqual(self.characteristic.category.term, 'test_category')
        annotation = OntologyAnnotation(term='another_category')
        self.characteristic.category = annotation
        self.assertEqual(self.characteristic.category.term, 'another_category')
        expected_error = ("Characteristic.category must be either a string ot an OntologyAnnotation, or None; "
                          "got 1:<class 'int'>")
        with self.assertRaises(AttributeError) as context:
            self.characteristic.category = 1
        self.assertEqual(str(context.exception), expected_error)

    def test_value(self):
        self.characteristic.value = 'test_value'
        self.assertEqual(self.characteristic.value, 'test_value')
        expected_error = ("Characteristic.value must be a string, numeric, an OntologyAnnotation, or None; "
                          "got ():<class 'tuple'>")
        with self.assertRaises(AttributeError) as context:
            self.characteristic.value = ()
        self.assertEqual(str(context.exception), expected_error)

    def test_unit(self):
        self.characteristic.unit = 'test_unit'
        self.assertEqual(self.characteristic.unit, 'test_unit')
        expected_error = ("Characteristic.unit must be either a string ot an OntologyAnnotation, or None; "
                          "got 1:<class 'int'>")
        with self.assertRaises(AttributeError) as context:
            self.characteristic.unit = 1
        self.assertEqual(str(context.exception), expected_error)

    def test_str(self):
        expected_str = ("isatools.model.Characteristic("
                        "category=isatools.model.OntologyAnnotation(term='test_category', "
                        "term_source=None, term_accession='', comments=[]), "
                        "value='test_value', unit='test_unit', comments=[])")
        self.assertEqual(self.characteristic.__repr__(), expected_str)
        self.assertTrue(hash(self.characteristic) == hash(expected_str))

    def test_repr(self):
        expected_str = ("Characteristic(\n\t"
                        "category=test_category\n\t"
                        "value=test_value\n\t"
                        "unit=test_unit\n\t"
                        "comments=0 Comment objects\n)")
        self.assertTrue(str(self.characteristic) == expected_str)

        self.characteristic.value = "another_value"
        self.characteristic.unit = "another_unit"
        expected_str = ("Characteristic(\n\t"
                        "category=test_category\n\t"
                        "value=another_value\n\t"
                        "unit=another_unit\n\t"
                        "comments=0 Comment objects\n)")
        self.assertTrue(str(self.characteristic) == expected_str)

        self.characteristic.value = None
        self.characteristic.unit = None
        expected_str = ("Characteristic(\n\t"
                        "category=test_category\n\t"
                        "value=\n\t"
                        "unit=\n\t"
                        "comments=0 Comment objects\n)")
        self.assertTrue(str(self.characteristic) == expected_str)

    def test_comparators(self):
        second_characteristic = Characteristic(category='_category', value='_value', unit='_unit')
        third_characteristic = Characteristic(category='test_category', value='test_value', unit='test_unit')
        self.assertTrue(self.characteristic == third_characteristic)
        self.assertTrue(self.characteristic != second_characteristic)

    @patch('isatools.model.characteristic.uuid4', return_value='A random string')
    def test_to_dict(self, mock_uuid4):
        category = OntologyAnnotation(id_="#ontology_annotation/characteristic_category_1")
        unit = OntologyAnnotation(id_="#ontology_annotation/characteristic_unit_1")
        characteristic = Characteristic(value=12, unit='test_unit')

        expected_dict = {
            'category': '',
            'value': 12,
            'unit': {'@id': '#unit/' + mock_uuid4.return_value},
            'comments': []
        }
        self.assertEqual(characteristic.to_dict(), expected_dict)
        characteristic.unit = unit
        characteristic.category = category
        expected_dict['unit'] = {'@id': '#unit/characteristic_unit_1'}
        expected_dict['category'] = {'@id': '#characteristic_category/characteristic_category_1'}
        self.assertEqual(characteristic.to_dict(), expected_dict)

    def test_from_dict(self):
        input_dict = {
            'category': '',
            'comments': [],
            'value': {}
        }
        characteristic = Characteristic()
        expected_error = ("Can't create value as annotation: 'annotationValue' "
                          "object: {'category': '', 'comments': [], 'value': {}}")
        with self.assertRaises(IOError) as context:
            characteristic.from_dict(input_dict)
        self.assertEqual(expected_error, str(context.exception))

        category = OntologyAnnotation(id_="cat")
        input_dict = {
            'category': category,
            'comments': [],
            'value': {
                '@id': 'test_id',
                'annotationValue': 123,
                'termSource': '',
                'termAccession': '',
                'comments': []
            }
        }
        characteristic.from_dict(input_dict)
        self.assertIsInstance(characteristic.category, OntologyAnnotation)
        self.assertEqual(characteristic.value.term, "123")
        self.assertEqual(characteristic.category.id, 'cat')

        input_dict = {'category': category, 'value': 123, 'comments': []}
        characteristic.from_dict(input_dict)
        self.assertIsNone(characteristic.unit)
        units_index = {"unit1": OntologyAnnotation(term='my unit')}
        input_dict['unit'] = {"@id": 'unit1'}

        indexes.units = units_index
        characteristic.from_dict(input_dict)
        self.assertEqual(characteristic.unit, units_index['unit1'])

        input_dict['value'] = []
        with self.assertRaises(IOError) as context:
            characteristic.from_dict(input_dict)
        self.assertEqual("Unexpected type in characteristic value", str(context.exception))

        input_dict = {'category': category, 'value': '123', 'comments': []}
        characteristic.from_dict(input_dict)
        self.assertEqual(characteristic.value, "123")
        indexes.reset_store()



