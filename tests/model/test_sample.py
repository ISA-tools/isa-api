from unittest import TestCase

from isatools.model.sample import Sample
from isatools.model.factor_value import FactorValue, StudyFactor
from isatools.model.characteristic import Characteristic
from isatools.model.source import Source


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
