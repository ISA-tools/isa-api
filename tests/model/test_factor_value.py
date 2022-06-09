from unittest import TestCase
from unittest.mock import patch

from isatools.model.factor_value import FactorValue, StudyFactor
from isatools.model.ontology_annotation import OntologyAnnotation


class TestStudyFactor(TestCase):

    def setUp(self):
        self.study_factor = StudyFactor(id_='id')

    def test_init(self):
        self.assertEqual(self.study_factor.id, 'id')
        study_factor = StudyFactor(id_='id', name='name', factor_type='term')
        self.assertTrue(study_factor.id == 'id')
        self.assertTrue(study_factor.name == 'name')
        self.assertTrue(study_factor.factor_type == 'term')

    def test_name(self):
        self.assertTrue(self.study_factor.name == '')
        self.study_factor.name = 'name'
        self.assertTrue(self.study_factor.name == 'name')

        with self.assertRaises(AttributeError) as context:
            self.study_factor.name = 1
        self.assertTrue("StudyFactor.name must be a str or None; got 1:<class 'int'>" in str(context.exception))

    def test_factor_type(self):
        self.assertTrue(self.study_factor.factor_type.term == '')
        self.assertTrue(isinstance(self.study_factor.factor_type, OntologyAnnotation))
        self.study_factor.factor_type = OntologyAnnotation(term='term')
        self.assertTrue(self.study_factor.factor_type.term == 'term')

        with self.assertRaises(AttributeError) as context:
            self.study_factor.factor_type = 1
        self.assertTrue("StudyFactor.factor_type must be a OntologyAnnotation or None; got 1:<class 'int'>"
                        in str(context.exception))

    def test_repr(self):
        expected_repr = ("isatools.model.StudyFactor(name='', factor_type=isatools.model.OntologyAnnotation(term='', "
                         "term_source=None, term_accession='', comments=[]), comments=[])")
        self.assertTrue(repr(self.study_factor) == expected_repr)
        self.assertTrue(hash(self.study_factor) == hash(expected_repr))

    def test_str(self):
        expected_str = ("StudyFactor(\n\t"
                        "name=\n\t"
                        "factor_type=\n\t"
                        "comments=0 Comment objects\n)")
        self.assertEqual(str(self.study_factor), expected_str)

    def test_equalities(self):
        second_study_factor = StudyFactor(id_='id', name='name', factor_type='term')
        third_study_factor = StudyFactor(id_='id', name='name', factor_type='term')
        self.assertTrue(second_study_factor == third_study_factor)
        self.assertTrue(second_study_factor != self.study_factor)

    def test_dict(self):
        factor_type = OntologyAnnotation(term='term', id_='factor_type_id')
        study_factor = StudyFactor(id_='study_factor_id', name='name', factor_type=factor_type)
        expected_dict = {
            '@id': 'study_factor_id', 'factorName': 'name',
            'factorType': {
                '@id': 'factor_type_id',
                'annotationValue': 'term',
                'termSource': '',
                'termAccession': '',
                'comments': []
            },
            'comments': []
        }
        self.assertEqual(study_factor.to_dict(), expected_dict)
        study_factor = StudyFactor()
        study_factor.from_dict(expected_dict)
        self.assertEqual(study_factor.to_dict(), expected_dict)


class TestFactorValue(TestCase):

    def setUp(self):
        self.factor_value = FactorValue(factor_name=StudyFactor(name='Control'),
                                        value=12,
                                        unit=OntologyAnnotation(term='mg'))

    def test_factor_name(self):
        self.assertTrue(isinstance(self.factor_value.factor_name, StudyFactor))
        self.assertEqual(self.factor_value.factor_name.name, 'Control')

        with self.assertRaises(AttributeError) as context:
            self.factor_value.factor_name = 1
        self.assertTrue("FactorValue.factor_name must be a StudyFactor or None; got 1:<class 'int'>"
                        in str(context.exception))

    def test_value(self):
        self.assertEqual(self.factor_value.value, 12)
        self.factor_value.value = 13
        self.assertEqual(self.factor_value.value, 13)

        with self.assertRaises(AttributeError) as context:
            self.factor_value.value = {}
        self.assertTrue("FactorValue.value must be a string, numeric, an OntologyAnnotation, or None; "
                        "got {}:<class 'dict'>" in str(context.exception))

    def test_unit(self):
        self.assertTrue(isinstance(self.factor_value.unit, OntologyAnnotation))
        self.assertEqual(self.factor_value.unit.term, 'mg')

        with self.assertRaises(AttributeError) as context:
            self.factor_value.unit = 1
        self.assertTrue("FactorValue.unit must be an OntologyAnnotation, o string, or None; got 1:<class 'int'>"
                        in str(context.exception))

    def test_repr(self):
        factor_name_str = ("isatools.model.StudyFactor(name='Control', factor_type=isatools.model.OntologyAnnotation("
                           "term='', term_source=None, term_accession='', comments=[]), comments=[])")
        unit_str = "isatools.model.OntologyAnnotation(term='mg', term_source=None, term_accession='', comments=[])"
        expected_str = "isatools.model.FactorValue(factor_name={0}, value=12, unit={1})".format(factor_name_str,
                                                                                                unit_str)
        self.assertEqual(repr(self.factor_value), expected_str)
        self.assertEqual(hash(self.factor_value), hash(expected_str))

    def test_str(self):
        expected_str = ("FactorValue(\n\t"
                        "factor_name=Control\n\t"
                        "value=12\n\t"
                        "unit=mg\n)")
        self.assertEqual(str(self.factor_value), expected_str)

    def test_equalities(self):
        second_factor_value = FactorValue(factor_name=StudyFactor(name='Control'),
                                          value=12,
                                          unit=OntologyAnnotation(term='mg'))
        third_factor_value = FactorValue(factor_name=StudyFactor(name='Control'),
                                         value=13,
                                         unit=OntologyAnnotation(term='mg'))
        self.assertTrue(second_factor_value != third_factor_value)
        self.assertTrue(second_factor_value == self.factor_value)

    @patch('isatools.model.factor_value.uuid4', return_value='test_uuid')
    def test_to_dict(self, mock_uuid):
        first_factor_value = FactorValue(factor_name=StudyFactor(name='test_factor_name', id_="#factor/0"),
                                         value=OntologyAnnotation(term='test_value', id_="#factor_value/0"),
                                         unit=OntologyAnnotation(term='test_unit', id_="#unit/0"))
        second_factor_value = FactorValue(factor_name=StudyFactor(name='factor_name1', id_="#factor/1"),
                                          unit="unit1")
        expected_dict = {
            'category': {'@id': '#factor/0'},
            'value': {
                '@id': '#factor_value/0',
                'annotationValue': 'test_value',
                'termSource': '',
                'termAccession': '',
                'comments': []},
            'unit': {'@id': '#unit/0'}
        }
        self.assertEqual(first_factor_value.to_dict(), expected_dict)

        expected_dict = {
            'category': {'@id': '#factor/1'},
            'value': '',
            'unit': {'@id': '#unit/' + mock_uuid.return_value}
        }
        self.assertEqual(second_factor_value.to_dict(), expected_dict)

    def test_from_dict(self):
        expected_dict = {
            'category': {'@id': 'factor0'},
            'value': {
                '@id': 'factor_value0',
                'annotationValue': 'test_value',
                'termSource': '',
                'termAccession': '',
                'comments': []},
            'unit': {'@id': '#unit/0'}
        }
        factors_index = {
            'factor0'
        }
        pass
