import unittest
from isatools.model.v1 import OntologySource, OntologyAnnotation, StudyFactor, FactorValue


class TestSimpleExamples(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_construct_investigation_object(self):
        try:
            from isatools.model.v1 import Investigation
        except ImportError:
            self.fail("Could not import Investigation class")
        I = Investigation()
        self.assertIsInstance(I.identifier, str)
        self.assertIsInstance(I.title, str)
        self.assertIsInstance(I.description, str)
        self.assertIsInstance(I.submission_date, str)  # todo: check if ISO8601
        self.assertIsInstance(I.public_release_date, str)  # todo: check if ISO8601

    def test_batch_create_materials(self):
        try:
            from isatools.model.v1 import Source
        except ImportError:
            self.fail("Could not import Source class")
        source = Source(name='source_material')

        try:
            from isatools.model.v1 import Sample
        except ImportError:
            self.fail("Could not import Sample class")
        prototype_sample = Sample(name='sample_material', derives_from=source)

        try:
            from isatools.model.v1 import batch_create_materials
        except ImportError:
            self.fail("Could not import batch_create_materials function")

        batch = batch_create_materials(prototype_sample, n=3)
        self.assertEqual(len(batch), 3)
        for material in batch:
            self.assertIsInstance(material, Sample)
            self.assertEqual(material.derives_from, source)
        self.assertSetEqual(set([m.name for m in batch]), {'sample_material-0', 'sample_material-1',
                                                           'sample_material-2'})


class TestOntologySource(unittest.TestCase):

    def setUp(self):
        pass

    def test_repr(self):
        ontology_source = OntologySource(name='some ontology', file='ontology_file.txt')
        self.assertEqual(repr(ontology_source), 'OntologySource(name=some ontology, file=ontology_file.txt)')

class TestOntologyAnnotation(unittest.TestCase):

    def setUp(self):
        pass

    def test_repr(self):
        ontology_source = OntologySource(name='some ontology', file='ontology_file.txt')
        ontology_annotation = OntologyAnnotation(term='thing', term_source=ontology_source, term_accession='http://this.is.a.uri.org')
        self.assertEqual(repr(ontology_annotation), 'OntologyAnnotation(term=thing, '
                                                    'term_source=OntologySource(name=some ontology, '
                                                    'file=ontology_file.txt), '
                                                    'term_accession=http://this.is.a.uri.org)')

class TestStudyFactor(unittest.TestCase):

    def setUp(self):
        pass

    def test_study_factor_repr(self):
        study_factor = StudyFactor(name='Duration', factor_type='time')
        self.assertEqual(repr(study_factor), 'StudyFactor(name=Duration)')

    def test_study_factor_hash(self):
        name = 'Duration'
        factor_type = 'time'
        study_factor = StudyFactor(name=name, factor_type=factor_type)
        self.assertEqual(hash(study_factor), hash(repr(study_factor)))

    def test_study_factor_eq(self):
        name = 'Duration'
        study_factor_1 = StudyFactor(name=name, factor_type='time')
        study_factor_2 = StudyFactor(name=name, factor_type='duration')
        self.assertEqual(study_factor_1, study_factor_2, 'The two tests pass the equality test')

    def test_study_factor_ne(self):
        study_factor_1 = StudyFactor(name='Duration', factor_type='time')
        study_factor_2 = StudyFactor(name='Time', factor_type='time')
        self.assertNotEqual(study_factor_1, study_factor_2, 'The two tests pass the equality test')


