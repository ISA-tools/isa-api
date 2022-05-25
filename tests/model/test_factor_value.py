from unittest import TestCase

from isatools.model.factor_value import FactorValue, StudyFactor
from isatools.model.ontology_annotation import OntologyAnnotation


class TestStudyFactor(TestCase):

    def setUp(self):
        self.study_factor = StudyFactor()

    def test_init(self):
        self.assertTrue(self.study_factor.id == '')
        self.assertTrue(isinstance(self.study_factor.factor_type, OntologyAnnotation))
        self.assertTrue(self.study_factor.factor_type.term == '')

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


class TestFactorValue(TestCase):

    def setUp(self):
        self.factor_value = FactorValue(factor_name=StudyFactor(name='Control'),
                                        value=12,
                                        unit=OntologyAnnotation(term='mg'))

    def test_init(self):
        self.assertEqual(self.factor_value.factor_name.name, 'Control')
        self.assertEqual(self.factor_value.value, 12)
        self.assertEqual(self.factor_value.unit.term, 'mg')
