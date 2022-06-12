from unittest import TestCase

from isatools.model.parameter_value import ParameterValue
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.protocol_parameter import ProtocolParameter
from isatools.model.loader_indexes import loader_states as indexes

expected_repr = 'isatools.model.ParameterValue(category=None, value=None, unit=None, comments=[])'


class TestParameterValue(TestCase):

    def setUp(self):
        self.parameter = ParameterValue()

    def test_init(self):
        # Unit but no value should raise an error
        with self.assertRaises(ValueError) as context:
            ParameterValue(unit=OntologyAnnotation())
        self.assertEqual(str(context.exception),
                         "ParameterValue value mus be quantitative (i.e. numeric) if a unit is supplied")

    def test_category(self):
        self.assertIsNone(self.parameter.category)
        self.parameter.category = ProtocolParameter(parameter_name='test')
        self.assertIsInstance(self.parameter.category, ProtocolParameter)
        self.assertTrue(isinstance(self.parameter.category.parameter_name, OntologyAnnotation))
        self.assertTrue(self.parameter.category.parameter_name.term == 'test')

        with self.assertRaises(AttributeError) as context:
            self.parameter.category = 'test'
        self.assertEqual(str(context.exception),
                         "ParameterValue.category must be a ProtocolParameter or None; got test:<class 'str'>")

    def test_value(self):
        self.assertIsNone(self.parameter.value)
        self.parameter.value = 123
        self.assertIsInstance(self.parameter.value, int)

        expected_error = ("ParameterValue.value must be a string, numeric, an OntologyAnnotation, or None; "
                          "got {'test': 'test'}:<class 'dict'>")
        with self.assertRaises(AttributeError) as context:
            self.parameter.value = {'test': 'test'}
        self.assertEqual(str(context.exception), expected_error)

    def test_unit(self):
        self.assertIsNone(self.parameter.unit)
        self.parameter.unit = OntologyAnnotation(term='test')
        self.assertIsInstance(self.parameter.unit, OntologyAnnotation)
        self.assertTrue(self.parameter.unit.term == 'test')

        with self.assertRaises(AttributeError) as context:
            self.parameter.unit = 'test'
        self.assertEqual(str(context.exception),
                         "ParameterValue.unit must be a OntologyAnnotation, or None; got test:<class 'str'>")

    def test_repr(self):
        self.assertEqual(repr(self.parameter), expected_repr)

    def test_str(self):
        expected_str = ("ParameterValue(\n\t"
                        "category=\n\t"
                        "value=None\n\t"
                        "unit=\n\t"
                        "comments=0 Comment objects\n)")
        self.assertEqual(str(self.parameter), expected_str)

    def test_hash(self):
        self.assertEqual(hash(self.parameter), hash(expected_repr))

    def test_equalities(self):
        second_parameter = ParameterValue(category=ProtocolParameter(parameter_name=OntologyAnnotation(term='test')))
        third_parameter = ParameterValue(category=ProtocolParameter(parameter_name=OntologyAnnotation(term='test')))
        self.assertTrue(second_parameter == third_parameter)
        self.assertTrue(second_parameter != self.parameter)

    def test_from_dict(self):
        expected_dict = {
            'comments': [],
            'category': {"@id": 'mycat'},
            'value': {
                '@id': "valueID"
            },
        }
        indexes.characteristic_categories = {
            'mycat': ProtocolParameter(id_='mycat', parameter_name=OntologyAnnotation(id_='valueID'))
        }
        parameter_value = ParameterValue()
        parameter_value.from_dict(expected_dict)
        self.assertEqual(parameter_value.category, indexes.get_characteristic_category('mycat'))

        expected_dict['value'] = 123
        expected_dict['unit'] = {"@id": 'myUnit'}
        indexes.units = {
            'myUnit': OntologyAnnotation(id_='myUnit')
        }
        parameter_value.from_dict(expected_dict)
        self.assertEqual(parameter_value.category, indexes.get_characteristic_category('mycat'))

