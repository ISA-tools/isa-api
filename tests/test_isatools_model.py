"""Tests on isatools.model classes"""
from __future__ import absolute_import
import datetime
import unittest
from copy import deepcopy


from isatools.model import (
     Investigation, OntologyAnnotation, Study, Characteristic,
     Assay, Sample,  Material
)


class InvestigationTest(unittest.TestCase):

    def setUp(self):
        self.investigation_default = Investigation()
        self.investigation = Investigation(
            identifier='id', filename='file', title='T',
            submission_date=datetime.datetime(day=1, month=1, year=2017),
            public_release_date=datetime.datetime(day=1, month=1, year=2017))

    def test_repr(self):
        self.assertEqual("isatools.model.Investigation(identifier='', "
                         "filename='', title='', submission_date='', "
                         "public_release_date='', "
                         "ontology_source_references=[], publications=[], "
                         "contacts=[], studies=[], comments=[])",
                         repr(self.investigation_default))
        self.assertEqual("isatools.model.Investigation(identifier='id', "
                         "filename='file', title='T', "
                         "submission_date='2017-01-01 00:00:00', "
                         "public_release_date='2017-01-01 00:00:00', "
                         "ontology_source_references=[], publications=[], "
                         "contacts=[], studies=[], comments=[])",
                         repr(self.investigation))

    def test_str(self):
        self.assertEqual("""Investigation(
    identifier=
    filename=
    title=
    submission_date=
    public_release_date=
    ontology_source_references=0 OntologySources
    publications=0 Publication objects
    contacts=0 Person objects
    studies=0 Study objects
    comments=0 Comment objects
)""", str(self.investigation_default))

        self.assertEqual("""Investigation(
    identifier=id
    filename=file
    title=T
    submission_date=2017-01-01 00:00:00
    public_release_date=2017-01-01 00:00:00
    ontology_source_references=0 OntologySources
    publications=0 Publication objects
    contacts=0 Person objects
    studies=0 Study objects
    comments=0 Comment objects
)""", str(self.investigation))

    def test_eq(self):
        expected_investigation = Investigation(
            identifier='id', filename='file', title='T',
            submission_date=datetime.datetime(day=1, month=1, year=2017),
            public_release_date=datetime.datetime(day=1, month=1, year=2017))
        self.assertEqual(expected_investigation, self.investigation)
        self.assertEqual(hash(expected_investigation), hash(self.investigation))

    def test_ne(self):
        expected_other_investigation = Investigation(
            identifier='id2', filename='file2', title='T2',
            submission_date=datetime.datetime(day=2, month=1, year=2017),
            public_release_date=datetime.datetime(day=2, month=1, year=2017))
        self.assertNotEqual(expected_other_investigation, self.investigation)
        self.assertNotEqual(
            hash(expected_other_investigation), hash(self.investigation))


class StudyTest(unittest.TestCase):

    def setUp(self):
        self.study_default = Study()
        self.study = Study(
            filename='file', identifier='0', title='T', description='D',
            submission_date=datetime.datetime(day=1, month=1, year=2017),
            public_release_date=datetime.datetime(day=1, month=1, year=2017))

    def test_repr(self):
        self.assertEqual("isatools.model.Study(filename='', "
                         "identifier='', title='', description='', "
                         "submission_date='', public_release_date='', "
                         "contacts=[], design_descriptors=[], publications=[], "
                         "factors=[], protocols=[], assays=[], sources=[], "
                         "samples=[], process_sequence=[], other_material=[], "
                         "characteristic_categories=[], comments=[], units=[])",
                         repr(self.study_default))
        self.assertEqual("isatools.model.Study(filename='file', "
                         "identifier='0', title='T', description='D', "
                         "submission_date='2017-01-01 00:00:00', "
                         "public_release_date='2017-01-01 00:00:00', "
                         "contacts=[], design_descriptors=[], publications=[], "
                         "factors=[], protocols=[], assays=[], sources=[], "
                         "samples=[], process_sequence=[], other_material=[], "
                         "characteristic_categories=[], comments=[], units=[])",
                         repr(self.study))

    def test_str(self):
        self.assertEqual("""Study(
    identifier=
    filename=
    title=
    description=
    submission_date=
    public_release_date=
    contacts=0 Person objects
    design_descriptors=0 OntologyAnnotation objects
    publications=0 Publication objects
    factors=0 StudyFactor objects
    protocols=0 Protocol objects
    assays=0 Assay objects
    sources=0 Source objects
    samples=0 Sample objects
    process_sequence=0 Process objects
    other_material=0 Material objects
    characteristic_categories=0 OntologyAnnots
    comments=0 Comment objects
    units=0 Unit objects
)""", str(self.study_default))

        self.assertEqual("""Study(
    identifier=0
    filename=file
    title=T
    description=D
    submission_date=2017-01-01 00:00:00
    public_release_date=2017-01-01 00:00:00
    contacts=0 Person objects
    design_descriptors=0 OntologyAnnotation objects
    publications=0 Publication objects
    factors=0 StudyFactor objects
    protocols=0 Protocol objects
    assays=0 Assay objects
    sources=0 Source objects
    samples=0 Sample objects
    process_sequence=0 Process objects
    other_material=0 Material objects
    characteristic_categories=0 OntologyAnnots
    comments=0 Comment objects
    units=0 Unit objects
)""", str(self.study))

    def test_eq(self):
        expected_study = Study(
            filename='file', identifier='0', title='T', description='D',
            submission_date=datetime.datetime(day=1, month=1, year=2017),
            public_release_date=datetime.datetime(day=1, month=1, year=2017),
            contacts=[], design_descriptors=[], publications=[], factors=[],
            protocols=[], assays=[], sources=[], samples=[],
            process_sequence=[], other_material=[],
            characteristic_categories=[], comments=[], units=[])
        self.assertEqual(expected_study, self.study)
        self.assertEqual(hash(expected_study),  hash(self.study))

    def test_ne(self):
        expected_other_study = Study(
            filename='file2', identifier='1', title='T2', description='D2',
            submission_date=datetime.datetime(day=2, month=1, year=2017),
            public_release_date=datetime.datetime(day=2, month=1, year=2017),
            contacts=[], design_descriptors=[], publications=[], factors=[],
            protocols=[], assays=[], sources=[], samples=[],
            process_sequence=[], other_material=[],
            characteristic_categories=[], comments=[], units=[])
        self.assertNotEqual(expected_other_study, self.study)
        self.assertNotEqual(hash(expected_other_study), hash(self.study))

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
        self.study.samples = samples
        self.study.shuffle_materials('samples')
        self.assertNotEqual(original_input, self.study.samples)

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
        self.study.other_material = other_materials
        self.study.shuffle_materials('Extract Name')
        self.assertNotEqual(self.study.other_material, original_input)

    def test_shuffle_error(self):
        with self.assertRaises(ValueError) as context:
            self.study.shuffle_materials('foo')
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
        self.study.samples = samples
        self.study.shuffle_materials('samples')
        self.assertNotEqual(original_input, self.study.samples)


class AssayTest(unittest.TestCase):

    def setUp(self):
        self.assay_default = Assay()
        self.assay = Assay(measurement_type=OntologyAnnotation(term='MT'),
                           technology_type=OntologyAnnotation(term='TT'),
                           technology_platform='TP', filename='file')

    def test_repr(self):
        self.assertEqual("isatools.model.Assay(measurement_type="
                         "isatools.model.OntologyAnnotation(term='', "
                         "term_source=None, term_accession='', comments=[]), "
                         "technology_type=isatools.model.OntologyAnnotation("
                         "term='', term_source=None, term_accession='', "
                         "comments=[]), technology_platform='', filename='', "
                         "data_files=[], samples=[], process_sequence=[], "
                         "other_material=[], characteristic_categories=[], "
                         "comments=[], units=[])",
                         repr(self.assay_default))
        self.assertEqual("isatools.model.Assay(measurement_type="
                         "isatools.model.OntologyAnnotation(term='MT', "
                         "term_source=None, term_accession='', comments=[]), "
                         "technology_type=isatools.model.OntologyAnnotation("
                         "term='TT', term_source=None, term_accession='', "
                         "comments=[]), technology_platform='TP', "
                         "filename='file', data_files=[], samples=[], "
                         "process_sequence=[], other_material=[], "
                         "characteristic_categories=[], comments=[], units=[])",
                         repr(self.assay))

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
)""", str(self.assay_default))

        self.assertEqual("""Assay(
    measurement_type=MT
    technology_type=TT
    technology_platform=TP
    filename=file
    data_files=0 DataFile objects
    samples=0 Sample objects
    process_sequence=0 Process objects
    other_material=0 Material objects
    characteristic_categories=0 OntologyAnnots
    comments=0 Comment objects
    units=0 Unit objects
)""", str(self.assay))

    def test_eq(self):
        expected_assay = Assay(measurement_type=OntologyAnnotation(term='MT'),
                               technology_type=OntologyAnnotation(term='TT'),
                               technology_platform='TP', filename='file')
        self.assertEqual(expected_assay, self.assay)
        self.assertEqual(hash(expected_assay),  hash(self.assay))

    def test_ne(self):
        expected_other_assay = Assay(
            measurement_type=OntologyAnnotation(term='MT2'),
            technology_type=OntologyAnnotation(term='TT2'),
            technology_platform='TP2', filename='file2')
        self.assertNotEqual(expected_other_assay, self.assay)
        self.assertNotEqual(hash(expected_other_assay), hash(self.assay))

