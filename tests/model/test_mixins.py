from unittest import TestCase
from unittest.mock import patch
from copy import deepcopy
from networkx import DiGraph


from isatools.model.mixins import MetadataMixin, StudyAssayMixin
from isatools.model.publication import Publication
from isatools.model.person import Person
from isatools.model.source import Source
from isatools.model.sample import Sample
from isatools.model.material import Material
from isatools.model.ontology_annotation import OntologyAnnotation
from isatools.model.process import Process
from isatools.model.characteristic import Characteristic
from isatools.model.factor_value import FactorValue


class TestMetadataMixin(TestCase):

    def setUp(self):
        self.metadata_mixin = MetadataMixin()

    def test_init(self):
        self.assertIsInstance(self.metadata_mixin, MetadataMixin)

        publication = Publication(title='Test publication')
        contact = Person(first_name='John', last_name='Doe')
        metadata_mixin = MetadataMixin(
            publications=[publication],
            contacts=[contact]
        )
        self.assertIsInstance(metadata_mixin, MetadataMixin)
        self.assertEqual(metadata_mixin.publications, [publication])
        self.assertEqual(metadata_mixin.contacts, [contact])

    def test_filename(self):
        self.assertEqual(self.metadata_mixin.filename, '')
        self.metadata_mixin.filename = 'test.txt'
        self.assertEqual(self.metadata_mixin.filename, 'test.txt')

        with self.assertRaises(AttributeError) as context:
            self.metadata_mixin.filename = 1
        self.assertEqual(str(context.exception), "MetadataMixin.filename must be a string")

    def test_identifier(self):
        self.assertEqual(self.metadata_mixin.identifier, '')
        self.metadata_mixin.identifier = 'test'
        self.assertEqual(self.metadata_mixin.identifier, 'test')

        with self.assertRaises(AttributeError) as context:
            self.metadata_mixin.identifier = 1
        self.assertEqual(str(context.exception), "MetadataMixin.identifier must be a string")

    def test_title(self):
        self.assertEqual(self.metadata_mixin.title, '')
        self.metadata_mixin.title = 'Test title'
        self.assertEqual(self.metadata_mixin.title, 'Test title')

        with self.assertRaises(AttributeError) as context:
            self.metadata_mixin.title = 1
        self.assertEqual(str(context.exception), "MetadataMixin.title must be a string")

    def test_description(self):
        self.assertEqual(self.metadata_mixin.description, '')
        self.metadata_mixin.description = 'Test description'
        self.assertEqual(self.metadata_mixin.description, 'Test description')

        with self.assertRaises(AttributeError) as context:
            self.metadata_mixin.description = 1
        self.assertEqual(str(context.exception), "MetadataMixin.description must be a string")

    def test_submission_date(self):
        self.assertEqual(self.metadata_mixin.submission_date, '')
        self.metadata_mixin.submission_date = '2017-01-01'
        self.assertEqual(self.metadata_mixin.submission_date, '2017-01-01')

        with self.assertRaises(AttributeError) as context:
            self.metadata_mixin.submission_date = 1
        self.assertEqual(str(context.exception), "MetadataMixin.submission_date must be a string")

    def test_public_release_date(self):
        self.assertEqual(self.metadata_mixin.public_release_date, '')
        self.metadata_mixin.public_release_date = '2017-01-01'
        self.assertEqual(self.metadata_mixin.public_release_date, '2017-01-01')

        with self.assertRaises(AttributeError) as context:
            self.metadata_mixin.public_release_date = 1
        self.assertEqual(str(context.exception), "MetadataMixin.public_release_date must be a string")

    def test_publications(self):
        self.assertEqual(self.metadata_mixin.publications, [])
        publication = Publication(title='Test publication')
        self.metadata_mixin.publications = [publication]
        self.assertEqual(self.metadata_mixin.publications, [publication])

        with self.assertRaises(AttributeError) as context:
            self.metadata_mixin.publications = 1
        self.assertEqual(str(context.exception), "MetadataMixin.publications must be iterable containing Publications")

    def test_contacts(self):
        self.assertEqual(self.metadata_mixin.contacts, [])
        contact = Person(first_name='John', last_name='Doe')
        self.metadata_mixin.contacts = [contact]
        self.assertEqual(self.metadata_mixin.contacts, [contact])

        with self.assertRaises(AttributeError) as context:
            self.metadata_mixin.contacts = 1
        self.assertEqual(str(context.exception), "MetadataMixin.contacts must be iterable containing Person objects")


class TestStudyAssayMixin(TestCase):

    def setUp(self) -> None:
        self.study_assay_mixin = StudyAssayMixin()
        self.source = Source()
        self.sample = Sample()
        self.material = Material()
        self.ontology_annotation = OntologyAnnotation()
        self.process = Process()

    def test_init(self):
        self.assertIsInstance(self.study_assay_mixin, StudyAssayMixin)

        study_assay_mixin = StudyAssayMixin(
            sources=[self.source],
            samples=[self.sample],
            other_material=[self.material],
            characteristic_categories=[self.ontology_annotation],
            units=[self.ontology_annotation],
            process_sequence=[self.process]
        )
        self.assertTrue(study_assay_mixin.sources == [self.source])
        self.assertTrue(study_assay_mixin.samples == [self.sample])
        self.assertTrue(study_assay_mixin.other_material == [self.material])
        self.assertTrue(study_assay_mixin.characteristic_categories == [self.ontology_annotation])
        self.assertTrue(study_assay_mixin.units == [self.ontology_annotation])
        self.assertTrue(study_assay_mixin.process_sequence == [self.process])

    def test_filename(self):
        self.assertEqual(self.study_assay_mixin.filename, '')
        self.study_assay_mixin.filename = 'Test name'
        self.assertEqual(self.study_assay_mixin.filename, 'Test name')

        with self.assertRaises(AttributeError) as context:
            self.study_assay_mixin.filename = 1
        self.assertEqual(str(context.exception), "StudyAssayMixin.filename must be a str or None; got 1:<class 'int'>")

    def test_units(self):
        self.assertEqual(self.study_assay_mixin.units, [])
        self.study_assay_mixin.units = [self.ontology_annotation]
        self.assertEqual(self.study_assay_mixin.units, [self.ontology_annotation])

        with self.assertRaises(AttributeError) as context:
            self.study_assay_mixin.units = 1
        self.assertEqual(str(context.exception),
                         "StudyAssayMixin.units must be iterable containing OntologyAnnotations")

    def test_sources(self):
        self.assertEqual(self.study_assay_mixin.sources, [])
        self.study_assay_mixin.sources = [self.source]
        self.assertEqual(self.study_assay_mixin.sources, [self.source])

        with self.assertRaises(AttributeError) as context:
            self.study_assay_mixin.sources = 1
        self.assertEqual(str(context.exception), "StudyAssayMixin.sources must be iterable containing Sources")

    def test_add_source(self):
        source = Source(name='Test source')
        self.study_assay_mixin.add_source('Test source')
        self.assertTrue(self.study_assay_mixin.sources == [source])

    def test_yield_source(self):
        source = Source(name='Test source')
        self.study_assay_mixin.add_source('Test source')
        self.assertTrue(list(self.study_assay_mixin.yield_sources('Test source')) == [source])
        self.assertTrue(list(self.study_assay_mixin.yield_sources()) == [source])

    def test_get_source(self):
        source = Source(name='Test source')
        self.study_assay_mixin.add_source('Test source')
        self.assertTrue(self.study_assay_mixin.get_source('Test source'), source)
        self.assertIsNone(self.study_assay_mixin.get_source('Not a source'))

    def test_yield_sources_by_characteristic(self):
        characteristic = Characteristic(category='test')
        source = Source(name='Test', characteristics=[characteristic])
        self.study_assay_mixin.add_source(name='Test', characteristics=[characteristic])
        self.assertTrue(list(self.study_assay_mixin.yield_sources_by_characteristic(characteristic)), [source])
        self.assertTrue(list(self.study_assay_mixin.yield_sources_by_characteristic()) == [source])

    def test_get_source_by_characteristic(self):
        characteristic = Characteristic(category='test')
        source = Source(name='Test', characteristics=[characteristic])
        self.study_assay_mixin.add_source(name='Test', characteristics=[characteristic])
        self.assertTrue(self.study_assay_mixin.get_source_by_characteristic(characteristic), source)
        self.assertIsNone(self.study_assay_mixin.get_source_by_characteristic('Not a characteristic'))

    def test_get_source_names(self):
        self.study_assay_mixin.add_source('Test source')
        self.assertTrue(self.study_assay_mixin.get_source_names(), ['Test source'])

    def test_samples(self):
        self.assertEqual(self.study_assay_mixin.samples, [])
        self.study_assay_mixin.samples = [self.sample]
        self.assertEqual(self.study_assay_mixin.samples, [self.sample])

        with self.assertRaises(AttributeError) as context:
            self.study_assay_mixin.samples = 1
        self.assertEqual(str(context.exception), "StudyAssayMixin.samples must be iterable containing Samples")

    def test_add_sample(self):
        self.study_assay_mixin.add_sample('Test sample')
        self.assertTrue(self.study_assay_mixin.samples == [Sample(name='Test sample')])

    def test_yield_samples(self):
        sample = Sample(name='Test sample')
        self.study_assay_mixin.add_sample('Test sample')
        self.assertTrue(list(self.study_assay_mixin.yield_samples('Test sample')) == [sample])
        self.assertTrue(list(self.study_assay_mixin.yield_samples()) == [sample])

    def test_get_sample(self):
        self.study_assay_mixin.add_sample('Test sample')
        self.assertTrue(self.study_assay_mixin.get_sample('Test sample'), Sample(name='Test sample'))
        self.assertIsNone(self.study_assay_mixin.get_sample('Not a sample'))

    def test_yield_samples_by_characteristic(self):
        characteristic = Characteristic(category='test')
        sample = Sample(name='Test', characteristics=[characteristic])
        self.study_assay_mixin.add_sample(name='Test', characteristics=[characteristic])
        self.assertTrue(list(self.study_assay_mixin.yield_samples_by_characteristic(characteristic)), [sample])
        self.assertTrue(list(self.study_assay_mixin.yield_samples_by_characteristic()) == [sample])

    def test_get_sample_by_characteristic(self):
        characteristic = Characteristic(category='test')
        sample = Sample(name='Test', characteristics=[characteristic])
        self.study_assay_mixin.add_sample(name='Test', characteristics=[characteristic])
        self.assertTrue(self.study_assay_mixin.get_sample_by_characteristic(characteristic), sample)
        self.assertIsNone(self.study_assay_mixin.get_sample_by_characteristic('Not a characteristic'))

    def test_yield_samples_by_factor_value(self):
        factor_value = FactorValue(value='Test')
        sample = Sample(name='Test', factor_values=[factor_value])
        self.study_assay_mixin.add_sample(name='Test', factor_values=[factor_value])
        self.assertTrue(list(self.study_assay_mixin.yield_samples_by_factor_value(factor_value)), [sample])
        self.assertTrue(list(self.study_assay_mixin.yield_samples_by_factor_value()) == [sample])

    def test_get_sample_by_factor_value(self):
        factor_value = FactorValue(value='Test')
        sample = Sample(name='Test', factor_values=[factor_value])
        self.study_assay_mixin.add_sample(name='Test', factor_values=[factor_value])
        self.assertTrue(self.study_assay_mixin.get_sample_by_factor_value(factor_value), sample)
        self.assertIsNone(self.study_assay_mixin.get_sample_by_factor_value('Not a factor value'))

    def test_get_sample_names(self):
        self.study_assay_mixin.add_sample('Test sample')
        self.assertTrue(self.study_assay_mixin.get_sample_names(), ['Test sample'])

    def test_other_material(self):
        self.assertEqual(self.study_assay_mixin.other_material, [])
        self.study_assay_mixin.other_material = [self.material]
        self.assertEqual(self.study_assay_mixin.other_material, [self.material])

        with self.assertRaises(AttributeError) as context:
            self.study_assay_mixin.other_material = 1
        self.assertEqual(str(context.exception),
                         "StudyAssayMixin.other_material must be iterable containing Materials")

    def test_yield_materials_by_characteristic(self):
        characteristic = Characteristic(category='test')
        material = Material(name='Test', characteristics=[characteristic])
        self.study_assay_mixin.other_material = [material]
        self.assertTrue(list(self.study_assay_mixin.yield_materials_by_characteristic(characteristic)), [material])
        self.assertTrue(list(self.study_assay_mixin.yield_materials_by_characteristic()) == [material])

    def test_get_material_by_characteristic(self):
        characteristic = Characteristic(category='test')
        material = Material(name='Test', characteristics=[characteristic])
        self.study_assay_mixin.other_material = [material]
        self.assertTrue(self.study_assay_mixin.get_material_by_characteristic(characteristic), material)
        self.assertIsNone(self.study_assay_mixin.get_material_by_characteristic('Not a characteristic'))

    @patch('isatools.model.mixins.warn')
    def test_materials(self, mock_warn):
        self.assertEqual(self.study_assay_mixin.materials, {'other_material': [], 'samples': [], 'sources': []})
        mock_warn.assert_called_with("the `materials` dict property is being deprecated in favour of `sources`, "
                                     "`samples`, and `other_material` properties.", DeprecationWarning)

    def test_process_sequence(self):
        self.assertTrue(self.study_assay_mixin.process_sequence == [])
        process = Process(name='Test process')
        self.study_assay_mixin.process_sequence = [process]
        self.assertTrue(self.study_assay_mixin.process_sequence == [process])

        with self.assertRaises(AttributeError) as context:
            self.study_assay_mixin.process_sequence = 1
        self.assertEqual(str(context.exception),
                         "StudyAssayMixin.process_sequence must be iterable containing Processes")

    def test_characteristic_categories(self):
        ontology_annotations = OntologyAnnotation(term='Test term')
        self.assertEqual(self.study_assay_mixin.characteristic_categories, [])
        self.study_assay_mixin.characteristic_categories = [ontology_annotations]
        self.assertEqual(self.study_assay_mixin.characteristic_categories, [ontology_annotations])
        self.study_assay_mixin.characteristic_categories = ['test']
        self.assertEqual(self.study_assay_mixin.characteristic_categories, [ontology_annotations])

        with self.assertRaises(AttributeError) as context:
            self.study_assay_mixin.characteristic_categories = 1
        self.assertEqual(str(context.exception),
                         "StudyAssayMixin.characteristic_categories must be iterable containing OntologyAnnotation")

    def test_graph(self):
        self.assertIsNone(self.study_assay_mixin.graph)
        self.study_assay_mixin.process_sequence = [Process(name='Test process')]
        self.assertIsInstance(self.study_assay_mixin.graph, DiGraph)

        with self.assertRaises(AttributeError) as context:
            self.study_assay_mixin.graph = 1
        self.assertEqual(str(context.exception), "StudyAssayMixin.graph is not settable")

    def test_shuffle_samples(self):
        samples = [
            Sample(name="Sample1"),
            Sample(name="Sample2"),
            Sample(name="Sample3"),
            Sample(name="Sample4"),
            Sample(name="Sample5"),
            Sample(name="Sample6"),
            Sample(name="Sample7")
        ]
        original_input = deepcopy(samples)
        self.study_assay_mixin.samples = samples
        self.study_assay_mixin.shuffle_materials('samples')
        self.assertNotEqual(original_input, self.study_assay_mixin.samples)

    def test_shuffle_other_material(self):
        other_materials = [
            Material(name="Material1", type_="Extract Name"),
            Material(name="Material2", type_="Extract Name"),
            Material(name="Material3", type_="Extract Name"),
            Material(name="Material4", type_="Extract Name"),
            Material(name="Material5", type_="Extract Name"),
            Material(name="Material6", type_="Labeled Extract Name"),
            Material(name="Material7", type_="Labeled Extract Name"),
            Material(name="Material8", type_="Labeled Extract Name"),
            Material(name="Material9", type_="Labeled Extract Name"),
            Material(name="Material10", type_="Labeled Extract Name"),
        ]
        original_input = deepcopy(other_materials)
        self.study_assay_mixin.other_material = other_materials
        self.study_assay_mixin.shuffle_materials('Extract Name')
        self.assertNotEqual(self.study_assay_mixin.other_material, original_input)

    def test_shuffle_error(self):
        with self.assertRaises(ValueError) as context:
            self.study_assay_mixin.shuffle_materials('foo')
            self.assertTrue('foo should be in samples, sources, Extract Name, Labeled Extract Name'
                            in context.exception)

    def test_shuffle_with_existing_randomized(self):
        ontology_annotation = OntologyAnnotation(term='randomized extraction order')
        samples = [
            Sample(name="Sample1", characteristics=[Characteristic(category=ontology_annotation, value='abc')]),
            Sample(name="Sample2"),
            Sample(name="Sample3"),
            Sample(name="Sample4"),
            Sample(name="Sample5"),
            Sample(name="Sample6", characteristics=[Characteristic(category=ontology_annotation, value='def')]),
            Sample(name="Sample7")
        ]
        original_input = deepcopy(samples)
        self.study_assay_mixin.samples = samples
        self.study_assay_mixin.shuffle_materials('samples')
        self.assertNotEqual(original_input, self.study_assay_mixin.samples)
        self.study_assay_mixin.shuffle_materials('samples')
        self.assertNotEqual(original_input, self.study_assay_mixin.samples)

    def test_categories_to_dict(self):
        characteristic = OntologyAnnotation(term='Test term', id_='test_id')
        characteristic2 = OntologyAnnotation(term='Test term2', id_='#ontology_annotation/test_id2')
        self.study_assay_mixin.characteristic_categories = [characteristic, characteristic2]
        expected_categories = [
            {
                '@id': '#characteristic_category/test_id',
                'characteristicType': {
                    '@id': 'test_id',
                    'termSource': '',
                    'termAccession': '',
                    'annotationValue': 'Test term',
                    'comments': []
                }
            },
            {
                '@id': '#characteristic_category/test_id2',
                'characteristicType': {
                    '@id': '#ontology_annotation/test_id2',
                    'termSource': '',
                    'termAccession': '',
                    'annotationValue': 'Test term2',
                    'comments': []
                }
            }
        ]
        self.assertEqual(self.study_assay_mixin.categories_to_dict(), expected_categories)
