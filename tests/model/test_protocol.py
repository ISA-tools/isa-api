from unittest import TestCase
from unittest.mock import patch
from isatools.model.protocol import Protocol, load_protocol_types_info
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.protocol_parameter import ProtocolParameter
from isatools.model.comments import Comment

expected_ProtocolParameter_string = ("ProtocolParameter(\n\t"
                                     "parameter_name=test_parameters\n\t"
                                     "comments=0 Comment objects\n)")
expected_repr_string = ("isatools.model.Protocol(name='', protocol_type=isatools.model.OntologyAnnotation("
                        "term='', term_source=None, term_accession='', comments=[]), uri='', version='', "
                        "parameters=[], components=[], comments=[])")


class TestProtocol(TestCase):

    def setUp(self):
        self.protocol = Protocol()

    def test_init(self):
        parameter = ProtocolParameter(parameter_name='test_parameters')
        ontology_annotation = OntologyAnnotation(term='test_components')

        protocol = Protocol(name='test_name', protocol_type='test_protocol_type',
                            description='test_description', uri='test_uri', version='test_version',
                            parameters=[parameter], components=[ontology_annotation])
        self.assertTrue(protocol.name == 'test_name')
        self.assertTrue(protocol.protocol_type.term == 'test_protocol_type')
        self.assertTrue(protocol.description == 'test_description')
        self.assertTrue(protocol.uri == 'test_uri')
        self.assertTrue(protocol.version == 'test_version')
        self.assertTrue(protocol.parameters == [parameter])
        self.assertTrue(protocol.components == [ontology_annotation])

    def test_getters(self):
        self.assertTrue(self.protocol.id == '')
        self.assertTrue(self.protocol.version == '')

    def test_name(self):
        self.assertTrue(self.protocol.name == '')
        self.protocol.name = 'test_name'
        self.assertTrue(self.protocol.name == 'test_name')

        with self.assertRaises(AttributeError) as context:
            self.protocol.name = 1
        self.assertTrue("Protocol.name must be a str or None; got 1:<class 'int'>" in str(context.exception))

        self.protocol.name = None
        self.assertIsNone(self.protocol.name)

    def test_protocol_type(self):
        self.assertIsNotNone(self.protocol.protocol_type)
        self.assertTrue(isinstance(self.protocol.protocol_type, OntologyAnnotation))
        self.assertTrue(self.protocol.protocol_type.term == '')

        with self.assertRaises(AttributeError) as context:
            self.protocol.protocol_type = 1
        self.assertTrue("Protocol.protocol_type must be a OntologyAnnotation, a string or None; "
                        "got 1:<class 'int'>" in str(context.exception))

        self.protocol.protocol_type = None
        self.assertTrue(self.protocol.protocol_type.term == '')
        self.protocol.protocol_type = 'test_protocol_type'
        self.assertTrue(self.protocol.protocol_type.term == 'test_protocol_type')

        ontology_annotation = OntologyAnnotation(term='test_protocol_type')
        self.protocol.protocol_type = ontology_annotation
        self.assertTrue(self.protocol.protocol_type.term == 'test_protocol_type')

    def test_description(self):
        self.assertTrue(self.protocol.description == '')
        self.protocol.description = 'test_description'
        self.assertTrue(self.protocol.description == 'test_description')

        with self.assertRaises(AttributeError) as context:
            self.protocol.description = 1
        self.assertTrue("Protocol.description must be a str or None; got 1:<class 'int'>" in str(context.exception))

        self.protocol.description = None
        self.assertIsNone(self.protocol.description)

    def test_uri(self):
        self.assertTrue(self.protocol.uri == '')
        self.protocol.uri = 'test_uri'
        self.assertTrue(self.protocol.uri == 'test_uri')

        with self.assertRaises(AttributeError) as context:
            self.protocol.uri = 1
        self.assertTrue("Protocol.uri must be a str or None; got 1:<class 'int'>" in str(context.exception))

        self.protocol.uri = None
        self.assertIsNone(self.protocol.uri)

    def test_version(self):
        self.assertTrue(self.protocol.version == '')
        self.protocol.version = 'test_version'
        self.assertTrue(self.protocol.version == 'test_version')

        with self.assertRaises(AttributeError) as context:
            self.protocol.version = 1
        self.assertTrue("Protocol.version must be a str or None; got 1:<class 'int'>" in str(context.exception))

        self.protocol.version = None
        self.assertIsNone(self.protocol.version)

    def test_parameters(self):
        self.assertTrue(self.protocol.parameters == [])
        self.protocol.parameters = ['test_parameters']
        expected_string = ("ProtocolParameter(\n\t"
                           "parameter_name=test_parameters\n\t"
                           "comments=0 Comment objects\n)")
        self.assertTrue(str(self.protocol.parameters[0]) == expected_string)

        with self.assertRaises(AttributeError) as context:
            self.protocol.parameters = 1
        self.assertTrue("Protocol.parameters must be an iterable containing ProtocolParameters"
                        in str(context.exception))

    def test_add_param(self):
        self.assertTrue(self.protocol.parameters == [])
        self.protocol.add_param('test_parameters')
        self.assertTrue(str(self.protocol.parameters[0]) == expected_ProtocolParameter_string)

        with self.assertRaises(AttributeError) as context:
            self.protocol.add_param(1)
        self.assertTrue("Parameter name must be either a string or a ProtocolParameter" in str(context.exception))

        protocol_parameter = ProtocolParameter(parameter_name='test_parameter')
        self.protocol.add_param(protocol_parameter)
        self.assertTrue(self.protocol.parameters[1] == protocol_parameter)

        self.protocol.add_param('test_parameters')
        self.assertTrue(len(self.protocol.parameters) == 2)

    def test_get_param(self):
        self.protocol.add_param('test_parameters')
        self.assertIsNone(self.protocol.get_param(1))

        self.assertTrue(str(self.protocol.get_param('test_parameters')) == expected_ProtocolParameter_string)

    def test_components(self):
        self.assertTrue(self.protocol.components == [])
        self.protocol.components = ['test_components']
        self.assertTrue(self.protocol.components == [])
        ontology_annotation = OntologyAnnotation(term='test_components')
        self.protocol.components = [ontology_annotation]
        self.assertTrue(isinstance(self.protocol.components[0], OntologyAnnotation))
        self.assertTrue(self.protocol.components[0].term == 'test_components')

        with self.assertRaises(AttributeError) as context:
            self.protocol.components = 1
        self.assertTrue("Protocol.components must be iterable containing OntologyAnnotations"
                        in str(context.exception))

    @patch("isatools.model.protocol.pprint")
    def test_show_allowed_protocol_types(self, mock_pprint):
        protocol_types_dict = load_protocol_types_info()
        self.protocol.show_allowed_protocol_types()
        mock_pprint.assert_called_with(protocol_types_dict)

    def test_repr(self):
        self.assertTrue(repr(self.protocol) == expected_repr_string)

    def test_str(self):
        expected_str = ("Protocol(\n\t"
                        "name=\n\t"
                        "protocol_type=\n\t"
                        "uri=\n\t"
                        "version=\n\t"
                        "parameters=0 ProtocolParameter objects\n\t"
                        "components=0 OntologyAnnotation objects\n\t"
                        "comments=0 Comment objects\n)")
        self.assertTrue(str(self.protocol) == expected_str)

    def test_hash(self):
        self.assertTrue(hash(self.protocol) == hash(expected_repr_string))

    def test_equalities(self):
        second_protocol = Protocol(name='test_name', version='1.0')
        third_protocol = Protocol(name='test_name', version='1.0')
        self.assertTrue(second_protocol == third_protocol)
        self.assertTrue(second_protocol != self.protocol)

    def test_to_dict(self):
        expected_dict = {
            '@id': '#protocol/test_id',
            'name': 'test_name', 'version': '1.0', 'description': '', 'uri': '',
            'comments': [{'name': 'test_comment', 'value': ''}],
            'parameters': [
                {
                    'parameterName': {
                        '@id': '#ontology_annotation/pm_id',
                        'annotationValue': 'test_parameter', 'termSource': '', 'termAccession': '', 'comments': []
                    },
                    '@id': 'SET ID'
                 }
            ],
            'protocolType': {
                '@id': '#ontology_annotation/oa_id',
                'annotationValue': 'test_protocol_type',
                'termSource': '',
                'termAccession': '',
                'comments': []},
            'components': []}
        protocol = Protocol(name='test_name', version='1.0',
                            id_='#protocol/test_id',
                            comments=[Comment(name='test_comment')],
                            parameters=[
                                ProtocolParameter(parameter_name=OntologyAnnotation(term='test_parameter', id_='pm_id'))
                            ],
                            protocol_type=OntologyAnnotation(term='test_protocol_type', id_='oa_id'))
        self.assertEqual(protocol.to_dict(), expected_dict)


class TestFunctions(TestCase):

    def test_load_protocol_types_info(self):
        yaml_config = load_protocol_types_info()
        self.assertTrue(isinstance(yaml_config, dict))
        self.assertTrue(len(yaml_config.keys()) == 15)
