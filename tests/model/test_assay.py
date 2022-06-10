from unittest import TestCase

from isatools.model.assay import Assay
from isatools.model.datafile import DataFile
from isatools.model.ontology_annotation import OntologyAnnotation


class TestAssay(TestCase):

    def setUp(self):
        self.assay = Assay()

    def test_init(self):
        assay = Assay(measurement_type=OntologyAnnotation(term='MT'),
                      technology_type=OntologyAnnotation(term='TT'),
                      technology_platform='TP',
                      filename='file',
                      data_files=[DataFile(filename='file1')])
        self.assertEqual(OntologyAnnotation(term='MT'), assay.measurement_type)
        self.assertEqual(OntologyAnnotation(term='TT'), assay.technology_type)
        self.assertEqual('TP', assay.technology_platform)
        self.assertEqual('file', assay.filename)
        self.assertEqual(1, len(assay.data_files))
        self.assertEqual('file1', assay.data_files[0].filename)

    def test_measurement_type(self):
        self.assertIsInstance(self.assay.measurement_type, OntologyAnnotation)
        self.assertEqual(self.assay.measurement_type.term, '')
        self.assay.measurement_type = OntologyAnnotation(term='MT')
        self.assertEqual(OntologyAnnotation(term='MT'), self.assay.measurement_type)

        with self.assertRaises(AttributeError) as context:
            self.assay.measurement_type = 1
        self.assertTrue("Assay.measurement_type must be a OntologyAnnotation or None; got 1:<class 'int'>"
                        in str(context.exception))

    def test_technology_type(self):
        self.assertIsInstance(self.assay.technology_type, OntologyAnnotation)
        self.assertEqual(self.assay.technology_type.term, '')
        self.assay.technology_type = OntologyAnnotation(term='TT')
        self.assertEqual(OntologyAnnotation(term='TT'), self.assay.technology_type)

        with self.assertRaises(AttributeError) as context:
            self.assay.technology_type = 1
        self.assertTrue("Assay.technology_type must be a OntologyAnnotation or None; got 1:<class 'int'>"
                        in str(context.exception))

    def test_technology_platform(self):
        self.assertEqual('', self.assay.technology_platform)
        self.assay.technology_platform = 'TP'
        self.assertEqual('TP', self.assay.technology_platform)

        with self.assertRaises(AttributeError) as context:
            self.assay.technology_platform = 1
        self.assertTrue("Assay.technology_platform must be a str or None; got 1:<class 'int'>"
                        in str(context.exception))

    def test_data_files(self):
        self.assertEqual(0, len(self.assay.data_files))
        datafile = DataFile()
        self.assay.data_files = [datafile]
        self.assertEqual(self.assay.data_files, [datafile])
        self.assay.data_files = [123]
        self.assertEqual(self.assay.data_files, [datafile])

        with self.assertRaises(AttributeError) as context:
            self.assay.data_files = 1
        self.assertTrue("Assay.data_files must be iterable containing DataFiles"
                        in str(context.exception))

    def test_repr(self):
        expected_str = ("isatools.model.Assay(measurement_type="
                        "isatools.model.OntologyAnnotation(term='', "
                        "term_source=None, term_accession='', comments=[]), "
                        "technology_type=isatools.model.OntologyAnnotation("
                        "term='', term_source=None, term_accession='', "
                        "comments=[]), technology_platform='', filename='', "
                        "data_files=[], samples=[], process_sequence=[], "
                        "other_material=[], characteristic_categories=[], "
                        "comments=[], units=[])")
        self.assertEqual(expected_str, repr(self.assay))
        self.assertEqual(hash(expected_str), hash(self.assay))

    def test_str(self):
        self.assertEqual("""Assay(
    measurement_type=
    technology_type=
    technology_platform=
    filename=
    data_files=0 DataFile objects
    samples=0 Sample objects
    process_sequence=0 Process objects
    other_material=0 Material objects
    characteristic_categories=0 OntologyAnnots
    comments=0 Comment objects
    units=0 Unit objects
)""", str(self.assay))

    def test_equalities(self):
        first_assay = Assay(measurement_type=OntologyAnnotation(term='MT1'))
        second_assay = Assay(measurement_type=OntologyAnnotation(term='MT1'))
        third_assay = Assay(measurement_type=OntologyAnnotation(term='MT2'))
        self.assertTrue(first_assay == second_assay)
        self.assertFalse(first_assay == third_assay)
        self.assertFalse(first_assay != second_assay)
        self.assertTrue(first_assay != third_assay)

    def test_to_dict(self):
        assay = Assay(
            filename='file',
            measurement_type=OntologyAnnotation(term='MT', id_='MT_ID'),
            technology_type=OntologyAnnotation(term='TT', id_='TT_ID')
        )
        expected_dict = {
            'measurementType': {
                '@id': 'MT_ID',
                'annotationValue': 'MT',
                'termSource': '',
                'termAccession': '',
                'comments': []},
            'technologyType': {
                '@id': 'TT_ID',
                'annotationValue': 'TT',
                'termSource': '',
                'termAccession': '',
                'comments': []
            },
            'technologyPlatform': '',
            'filename': 'file',
            'characteristicCategories': [],
            'unitCategories': [],
            'comments': [],
            'materials': {
                'samples': [],
                'otherMaterials': []
            },
            'dataFiles': [],
            'processSequence': []
        }
        self.assertEqual(expected_dict, assay.to_dict())

        assay = Assay()
        assay.from_dict(expected_dict)
        self.assertEqual(assay.to_dict(), expected_dict)

        expected_dict['unitCategories'] = [{
            '@id': 'unit_ID',
            'annotationValue': 'my_unit',
            'termSource': '',
            'termAccession': '',
            'comments': []
        }]
        assay.from_dict(expected_dict)
        self.assertEqual(assay.to_dict(), expected_dict)


























