from unittest import TestCase
from unittest.mock import patch

from isatools.model.sample import Sample
from isatools.model.factor_value import FactorValue, StudyFactor
from isatools.model.characteristic import Characteristic
from isatools.model.source import Source
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.loader_indexes import loader_states as indexes


class TestSample(TestCase):

    def setUp(self):
        self.sample = Sample()

    def test_init(self):
        factor_value = FactorValue()
        characteristic = Characteristic()
        source = Source()

        sample = Sample(name="sample1",
                        factor_values=[factor_value],
                        characteristics=[characteristic],
                        derives_from=[source])
        self.assertEqual(sample.name, "sample1")
        self.assertEqual(sample.factor_values, [factor_value])
        self.assertEqual(sample.characteristics, [characteristic])
        self.assertEqual(sample.derives_from, [source])

    def test_name(self):
        self.assertTrue(self.sample.name == '')
        self.sample.name = 'test_name'
        self.assertTrue(self.sample.name == 'test_name')

        with self.assertRaises(AttributeError) as context:
            self.sample.name = 1
        self.assertTrue("Sample.name must be a str or None; got 1:<class 'int'>" in str(context.exception))

    def test_factor_value(self):
        self.assertTrue(self.sample.factor_values == [])
        factor_value = FactorValue(factor_name=StudyFactor(name='test_factor_name'))
        self.sample.factor_values = [factor_value]
        self.assertTrue(self.sample.factor_values == [factor_value])
        self.sample.factor_values = [1, 2, 3]
        self.assertTrue(self.sample.factor_values == [factor_value])

        with self.assertRaises(AttributeError) as context:
            self.sample.factor_values = 1
        self.assertTrue("Sample.factor_values must be iterable containing FactorValues" in str(context.exception))

    def test_characteristics(self):
        self.assertTrue(self.sample.characteristics == [])
        characteristic = Characteristic(category='test_factor_name')
        self.sample.characteristics = [characteristic]
        self.assertTrue(self.sample.characteristics == [characteristic])
        self.sample.characteristics = [1]
        self.assertTrue(self.sample.characteristics == [characteristic])

        with self.assertRaises(AttributeError) as context:
            self.sample.characteristics = 1
        self.assertTrue("Sample.characteristics must be iterable containing Characteristics" in str(context.exception))

    def test_has_char(self):
        characteristic = Characteristic(category='test_factor_name')
        self.sample.characteristics = [characteristic]
        self.assertTrue(self.sample.has_char('test_factor_name'))
        self.assertTrue(self.sample.has_char(characteristic))
        self.assertFalse(self.sample.has_char('test_factor_name2'))
        self.assertFalse(self.sample.has_char(1))

    def test_get_char(self):
        first_characteristic = Characteristic(category='test_factor_name')
        second_characteristic = Characteristic(category='test_factor_name2')
        self.sample.characteristics = [first_characteristic, second_characteristic]
        self.assertTrue(self.sample.get_char('test_factor_name') == first_characteristic)
        self.assertIsNone(self.sample.get_char('test_factor_name3'))

    def test_derives_from(self):
        self.assertTrue(self.sample.derives_from == [])
        source = Source()
        self.sample.derives_from = [source]
        self.assertTrue(self.sample.derives_from == [source])
        self.sample.derives_from = [1, 2]
        self.assertTrue(self.sample.derives_from == [source])

        with self.assertRaises(AttributeError) as context:
            self.sample.derives_from = 1
        self.assertTrue("Sample.derives_from must be iterable containing Sources" in str(context.exception))

    def test_repr(self):
        expected_str = ("isatools.model.Sample(name='', characteristics=[], factor_values=[],"
                        " derives_from=[], comments=[])")
        self.assertTrue(repr(self.sample) == expected_str)
        self.assertTrue(hash(self.sample) == hash(expected_str))

    def test_str(self):
        expected_str = ("Sample(\n\t"
                        "name=\n\t"
                        "characteristics=0 Characteristic objects\n\t"
                        "factor_values=0 FactorValue objects\n\t"
                        "derives_from=0 Source objects\n\t"
                        "comments=0 Comment objects\n)")
        self.assertTrue((str(self.sample) == expected_str))

    def test_equalities(self):
        first_sample = Sample(name="sample1")
        second_sample = Sample(name="sample1")
        self.assertEqual(first_sample, second_sample)
        self.assertNotEqual(first_sample, self.sample)

    @patch('isatools.model.factor_value.uuid4', return_value='test_uuid')
    def test_to_dict(self, mock_uuid):
        self.sample.name = 'test_name'
        self.sample.id = 'test_id'
        expected_dict = {
            '@id': 'test_id', 'name': 'test_name',
            'characteristics': [], 'factorValues': [], 'derivesFrom': [], 'comments': []
        }
        self.assertEqual(self.sample.to_dict(), expected_dict)
        category = OntologyAnnotation(term='test_category', id_="#characteristics/0")
        unit = OntologyAnnotation(term='test_unit', id_="#unit/0")
        characteristic = Characteristic(category=category, unit=unit)
        self.sample.characteristics = [characteristic]
        expected_dict['characteristics'] = [
            {
                'category': {'@id': '#characteristics/0'},
                'value': None,
                'unit': {'@id': '#unit/0'},
                'comments': []
            }
        ]
        self.assertEqual(self.sample.to_dict(), expected_dict)

        first_factor_value = FactorValue(factor_name=StudyFactor(name='test_factor_name', id_="#factor/0"),
                                         value=OntologyAnnotation(term='test_value', id_="#factor_value/0"),
                                         unit=OntologyAnnotation(term='test_unit', id_="#unit/0"))
        second_factor_value = FactorValue(factor_name=StudyFactor(name='factor_name1', id_="#factor/1"),
                                          unit="unit1")
        self.sample.factor_values = [first_factor_value, second_factor_value]
        expected_dict['factorValues'] = [
            {
                'category': {'@id': '#factor/0'},
                'value': {
                    '@id': '#factor_value/0',
                    'annotationValue': 'test_value',
                    'termSource': '',
                    'termAccession': '',
                    'comments': []},
                'unit': {'@id': '#unit/0'}
            },
            {
                'category': {'@id': '#factor/1'},
                'value': '',
                'unit': {'@id': '#unit/' + mock_uuid.return_value}
            }
        ]
        self.assertEqual(self.sample.to_dict(), expected_dict)

        self.sample.derives_from = [Source(name='source0', id_="#source/0"),
                                    Source(name='source1', id_="#source/1")]
        expected_dict['derivesFrom'] = [{'@id': '#source/0'}, {'@id': '#source/1'}]
        self.assertEqual(self.sample.to_dict(), expected_dict)

    def test_from_dict(self):
        expected_dict = {
            "@id": "sampleID",
            "name": "sample name",
            "characteristics": [],
            "factorValues": [],
            'comments': [],
            'derivesFrom': []
        }
        sample = Sample()
        sample.from_dict(expected_dict)
        self.assertEqual(sample.to_dict(), expected_dict)

        indexes.characteristic_categories = {"cat_id": OntologyAnnotation(term='my_cat', id_='cat_id')}
        expected_dict['characteristics'] = [
            {
                "category": {'@id': 'cat_id'},
                "comments": [],
                'value': 'val'
            }
        ]
        sample.from_dict(expected_dict)
        self.assertEqual(sample.to_dict(), expected_dict)
        self.assertEqual(sample.characteristics[0].category, indexes.get_characteristic_category('cat_id'))

        # indexes.reset_store()
        factor_type = OntologyAnnotation(id_='factorTypeID')
        indexes.factors = {'factor0': StudyFactor(id_='factor0', factor_type=factor_type)}
        expected_dict['factorValues'] = [
            {
                'category': {'@id': 'factor0'},
                'value': ''
            }
        ]
        sample.from_dict(expected_dict)
        self.assertEqual(sample.to_dict()['factorValues'], expected_dict['factorValues'])
        self.assertIn(sample.factor_values[0].to_dict(), expected_dict['factorValues'])

        indexes.sources = {
            "my_source": Source(id_="my_source")
        }
        expected_dict['derivesFrom'] = [{"@id": "my_source"}]
        sample.from_dict(expected_dict)
        self.assertEqual(indexes.get_source("my_source"), sample.derives_from[0])