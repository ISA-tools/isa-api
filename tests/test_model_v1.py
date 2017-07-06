import unittest
from isatools.model.v1 import OntologySource, OntologyAnnotation, StudyFactor, FactorValue, Characteristic


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


class TestCharacteristic(unittest.TestCase):

    def setUp(self):
        ontology_source = OntologySource(name='some ontology', file='ontology_file.txt')
        self.category = OntologyAnnotation(term='thing', term_source=ontology_source, term_accession='http://some.uri.org')
        self.value = OntologyAnnotation(term='val', term_source=ontology_source, term_accession='http://other.uri.org')
        self.unit = OntologyAnnotation(term='unit', term_source=ontology_source, term_accession='http://unit.uri.org')

    def test_repr(self):
        characteristic = Characteristic(category=self.category, value=self.value)
        self.assertNotEqual(repr(characteristic), 'Characteristic(category={0}, value={1} unit={2})'.format(
            self.category, self.value, None))

    def test_eq(self):
        characteristic = Characteristic(category=self.category, value=self.value)
        same_characteristic = Characteristic(value=self.value, category=self.category)
        self.assertEqual(characteristic, same_characteristic)
        self.assertEqual(hash(characteristic), hash(same_characteristic))

    def test_ne(self):
        characteristic = Characteristic(category=self.category, value=self.value)
        other_characteristic = Characteristic(value=self.value, category=self.category, unit=self.unit)
        self.assertNotEqual(characteristic, other_characteristic)
        self.assertNotEqual(hash(characteristic), hash(other_characteristic))


class TestStudyFactor(unittest.TestCase):

    def setUp(self):
        pass

    def test_repr(self):
        study_factor = StudyFactor(name='Duration', factor_type='time')
        self.assertEqual(repr(study_factor), 'StudyFactor(name=Duration)')

    def test_hash(self):
        name = 'Duration'
        factor_type = 'time'
        study_factor = StudyFactor(name=name, factor_type=factor_type)
        self.assertEqual(hash(study_factor), hash(repr(study_factor)))

    def test_eq(self):
        name = 'Duration'
        study_factor_1 = StudyFactor(name=name, factor_type='time')
        study_factor_2 = StudyFactor(name=name, factor_type='duration')
        self.assertEqual(study_factor_1, study_factor_2, 'The two tests pass the equality test')

    def test_ne(self):
        study_factor_1 = StudyFactor(name='Duration', factor_type='time')
        study_factor_2 = StudyFactor(name='Time', factor_type='time')
        self.assertNotEqual(study_factor_1, study_factor_2, 'The two tests pass the equality test')


class TestFactorValue(unittest.TestCase):

    def setUp(self):
        self.factor_value = FactorValue(factor_name='AGENT', value='agent_orange')

    def test_repr(self):
        self.assertEqual(repr(self.factor_value), 'FactorValue(factor_name=AGENT, value=agent_orange, unit=None)')

    def test_hash(self):
        self.assertEqual(hash(self.factor_value), hash(repr(self.factor_value)))

    def test_eq(self):
        same_factor_value = FactorValue(factor_name='AGENT', value='agent_orange')
        self.assertEqual(self.factor_value, same_factor_value)

    def test_ne(self):
        other_factor_value = FactorValue(factor_name='AGENT', value='Zyklon B')
        self.assertNotEqual(self.factor_value, other_factor_value)
