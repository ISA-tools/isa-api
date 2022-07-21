from unittest import TestCase

from isatools.model.protocol_parameter import ProtocolParameter
from isatools.model.ontology_annotation import OntologyAnnotation


protocol_parameter = ProtocolParameter()


class TestProtocolParameter(TestCase):

    def test_parameter_name(self):
        protocol_parameter.parameter_name = None
        self.assertTrue(protocol_parameter.parameter_name is None)

        protocol_parameter.parameter_name = 'test_parameter_name'
        self.assertEqual(protocol_parameter.parameter_name.term, 'test_parameter_name')
        self.assertTrue(isinstance(protocol_parameter.parameter_name, OntologyAnnotation))

        expected_error = ("ProtocolParameter.parameter_name must be either a string or an OntologyAnnotation "
                          "or None; got 1:<class 'int'>")
        with self.assertRaises(AttributeError) as context:
            protocol_parameter.parameter_name = 1
        self.assertEqual(str(context.exception), expected_error)

    def test_repr(self):
        protocol_parameter.parameter_name = 'test_parameter_name'
        param_name = ("isatools.model.OntologyAnnotation("
                      "term='test_parameter_name', "
                      "term_source=None, "
                      "term_accession='', "
                      "comments=[])")
        expected_str = "isatools.model.ProtocolParameter(parameter_name={0}, comments=[])".format(param_name)
        self.assertEqual(protocol_parameter.__repr__(), expected_str)
        self.assertTrue(hash(protocol_parameter) == hash(expected_str))

    def test_str(self):
        protocol_parameter.parameter_name = 'test_parameter_name'
        expected_str = ("ProtocolParameter(\n\t"
                        "parameter_name=test_parameter_name\n\t"
                        "comments=0 Comment objects\n)")
        self.assertEqual(str(protocol_parameter), expected_str)

    def test_equality(self):
        protocol_parameter.parameter_name = 'test_parameter_name'
        another_protocol_parameter = ProtocolParameter(id_="1", parameter_name='another_parameter_name')
        self.assertTrue(protocol_parameter != another_protocol_parameter)
        self.assertFalse(protocol_parameter == another_protocol_parameter)
        self.assertEqual(protocol_parameter, ProtocolParameter(parameter_name='test_parameter_name'))

    def test_dict(self):
        expected_dict = {
            "@id": "my_id",
            "parameterName": {
                '@id': 'parameterName_id',
                'annotationValue': 'parameterName',
                'termSource': '',
                'termAccession': '',
                'comments': []
            }
        }
        another_protocol_parameter = ProtocolParameter(
            id_="my_id", parameter_name=OntologyAnnotation(id_="parameterName_id", term='parameterName')
        )
        self.assertEqual(another_protocol_parameter.to_dict(), expected_dict)
        another_protocol_parameter.from_dict(expected_dict)
        self.assertEqual(another_protocol_parameter.to_dict(), expected_dict)
