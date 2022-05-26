from unittest import TestCase

from isatools.model.protocol_component import ProtocolComponent
from isatools.model.ontology_annotation import OntologyAnnotation


class TestProtocolComponent(TestCase):

    def setUp(self):
        self.protocol_component = ProtocolComponent()

    def test_init(self):
        ontology_annotation = OntologyAnnotation(term='term')
        protocol_component = ProtocolComponent(component_type=ontology_annotation)
        self.assertEqual(protocol_component.component_type, ontology_annotation)

    def test_name(self):
        self.assertEqual(self.protocol_component.name, '')
        self.protocol_component.name = 'name'
        self.assertEqual(self.protocol_component.name, 'name')

        with self.assertRaises(AttributeError) as context:
            self.protocol_component.name = 1
        self.assertEqual(str(context.exception), "ProtocolComponent.name must be a str or None; got 1:<class 'int'>")

    def test_component_type(self):
        self.assertIsInstance(self.protocol_component.component_type, OntologyAnnotation)
        ontology_annotation = OntologyAnnotation(term='term')
        self.protocol_component.component_type = ontology_annotation
        self.assertEqual(self.protocol_component.component_type, ontology_annotation)

        with self.assertRaises(AttributeError) as context:
            self.protocol_component.component_type = 1
        self.assertEqual(str(context.exception),
                         "ProtocolComponent.component_type must be a OntologyAnnotation, or None; got 1:<class 'int'>")

    def test_repr(self):
        expected_str = ("isatools.model.ProtocolComponent(name='', category=isatools.model.OntologyAnnotation(term='', "
                        "term_source=None, term_accession='', comments=[]), comments=[])")
        self.assertEqual(repr(self.protocol_component), expected_str)
        self.assertEqual(hash(self.protocol_component), hash(expected_str))

    def test_str(self):
        expected_str = """ProtocolComponent(
    name=
    category=
    comments=0 Comment objects
)"""
        self.assertEqual(str(self.protocol_component), expected_str)

    def test_equalities(self):
        first_protocol_component = ProtocolComponent(name='name1')
        second_protocol_component = ProtocolComponent(name='name1')
        third_protocol_component = ProtocolComponent(name='name2')
        self.assertEqual(first_protocol_component, second_protocol_component)
        self.assertNotEqual(first_protocol_component, third_protocol_component)
