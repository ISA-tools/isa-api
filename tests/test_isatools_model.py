"""Tests on isatools.model classes"""
from __future__ import absolute_import
import datetime
import unittest

from isatools.model import *


class CommentTest(unittest.TestCase):

    def setUp(self):
        self.comment_default = Comment()
        self.comment = Comment(name='N', value='V')

    def test_repr(self):
        self.assertEqual('isatools.model.Comment(name="", value="")',
                         repr(self.comment_default))
        self.assertEqual('isatools.model.Comment(name="N", value="V")',
                         repr(self.comment))

    def test_str(self):
        self.assertEqual('Comment[]\t',
                         str(self.comment_default))
        self.assertEqual('Comment[N]\tV',
                         str(self.comment))

    def test_eq(self):
        expected_comment = Comment(name='N', value='V')

        self.assertEqual(expected_comment, self.comment)
        self.assertEqual(hash(expected_comment), hash(self.comment))

    def test_ne(self):
        expected_other_comment = Comment(name='V', value='N')

        self.assertNotEqual(expected_other_comment, self.comment)
        self.assertNotEqual(hash(expected_other_comment), hash(self.comment))

    def test_raises_ISAModelAttributeError(self):
        try:
            self.comment_default.name = 0
        except ISAModelAttributeError:
            pass
        except Exception:
            self.fail('ISAModelAttributeError not raised')

        try:
            self.comment_default.value = 0
        except ISAModelAttributeError:
            pass
        except Exception:
            self.fail('ISAModelAttributeError not raised')


class InvestigationTest(unittest.TestCase):

    def setUp(self):
        self.investigation_default = Investigation()
        self.investigation = Investigation(
            identifier='id', filename='file', title='T',
            submission_date=datetime.datetime(day=1, month=1, year=2017),
            public_release_date=datetime.datetime(day=1, month=1, year=2017))

    def test_repr(self):
        self.assertEqual('isatools.model.Investigation(identifier="", '
                         'filename="", title="", submission_date="", '
                         'public_release_date="", '
                         'ontology_source_references=[], publications=[], '
                         'contacts=[], studies=[], comments=[])',
                         repr(self.investigation_default))
        self.assertEqual('isatools.model.Investigation(identifier="id", '
                         'filename="file", title="T", '
                         'submission_date="2017-01-01 00:00:00", '
                         'public_release_date="2017-01-01 00:00:00", '
                         'ontology_source_references=[], publications=[], '
                         'contacts=[], studies=[], comments=[])',
                         repr(self.investigation))

    def test_str(self):
        self.assertEqual("""Investigation(
    identifier=
    filename=
    title=
    submission_date=
    public_release_date=
    ontology_source_references=0 OntologySource objects
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
    ontology_source_references=0 OntologySource objects
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


class OntologySourceTest(unittest.TestCase):

    def setUp(self):
        self.ontology_source_default = OntologySource(name='N')
        self.ontology_source = OntologySource(name='N', file='F', version='V',
                                              description='D')

    def test_repr(self):
        self.assertEqual('isatools.model.OntologySource(name="N", file="", '
                         'version="", description="", comments=[])',
                         repr(self.ontology_source_default))
        self.assertEqual('isatools.model.OntologySource(name="N", file="F", '
                         'version="V", description="D", comments=[])',
                         repr(self.ontology_source))

    def test_str(self):
        self.assertEqual("""OntologySource(
    name=N
    file=
    version=
    description=
    comments=0 Comment objects
)""", str(self.ontology_source_default))

        self.assertEqual("""OntologySource(
    name=N
    file=F
    version=V
    description=D
    comments=0 Comment objects
)""", str(self.ontology_source))

    def test_eq(self):
        expected_ontology_source = OntologySource(
            name='N', file='F', version='V', description='D', comments=[])
        self.assertEqual(expected_ontology_source, self.ontology_source)
        self.assertEqual(
            hash(expected_ontology_source),  hash(self.ontology_source))

    def test_ne(self):
        expected_other_ontology_source = OntologySource(
            name='N2', file='F2', version='V2', description='D2', comments=[])
        self.assertNotEqual(
            expected_other_ontology_source, self.ontology_source)
        self.assertNotEqual(
            hash(expected_other_ontology_source), hash(self.ontology_source))


class OntologyAnnotationTest(unittest.TestCase):

    def setUp(self):
        self.ontology_annotation_default = OntologyAnnotation()
        self.ontology_annotation = OntologyAnnotation(
            term='T', term_source=OntologySource('N'), term_accession='A')

    def test_repr(self):
        self.assertEqual('isatools.model.OntologyAnnotation(term="", '
                         'term_source=None, term_accession="", comments=[])',
                         repr(self.ontology_annotation_default))
        self.assertEqual('isatools.model.OntologyAnnotation(term="T", '
                         'term_source=isatools.model.OntologySource('
                         'name="N", file="", version="", description="", '
                         'comments=[]), term_accession="A", comments=[])',
                         repr(self.ontology_annotation))

    def test_str(self):
        self.assertEqual("""OntologyAnnotation(
    term=
    term_source=
    term_accession=
    comments=0 Comment objects
)""", str(self.ontology_annotation_default))

        self.assertEqual("""OntologyAnnotation(
    term=T
    term_source=N
    term_accession=A
    comments=0 Comment objects
)""", str(self.ontology_annotation))

    def test_eq(self):
        expected_ontology_annotation = OntologyAnnotation(
            term='T', term_source=OntologySource(name='N'), term_accession='A')
        self.assertEqual(expected_ontology_annotation, self.ontology_annotation)
        self.assertEqual(
            hash(expected_ontology_annotation),  hash(self.ontology_annotation))

    def test_ne(self):
        expected_other_ontology_annotation = OntologyAnnotation(
            term='T2', term_source=OntologySource(name='N2'),
            term_accession='A2')
        self.assertNotEqual(expected_other_ontology_annotation, self.ontology_annotation)
        self.assertNotEqual(
            hash(expected_other_ontology_annotation), hash(self.ontology_annotation))


class PublicationTest(unittest.TestCase):

    def setUp(self):
        self.publication_default = Publication()
        self.publication = Publication(
            pubmed_id='1', doi='10', author_list='A. Author', title='T',
            status=OntologyAnnotation(term='S'))

    def test_repr(self):
        self.assertEqual('isatools.model.Publication(pubmed_id="", '
                         'doi="", author_list="", title="", status=None, '
                         'comments=[])',
                         repr(self.publication_default))
        self.assertEqual('isatools.model.Publication(pubmed_id="1", '
                         'doi="10", author_list="A. Author", title="T", '
                         'status=isatools.model.OntologyAnnotation(term="S", '
                         'term_source=None, term_accession="", comments=[]), '
                         'comments=[])',
                         repr(self.publication))

    def test_str(self):
        self.assertEqual("""Publication(
    pubmed_id=
    doi=
    author_list=
    title=
    status=
    comments=0 Comment objects
)""", str(self.publication_default))

        self.assertEqual("""Publication(
    pubmed_id=1
    doi=10
    author_list=A. Author
    title=T
    status=S
    comments=0 Comment objects
)""", str(self.publication))

    def test_eq(self):
        expected_publication = Publication(
            pubmed_id='1', doi='10', author_list='A. Author', title='T', 
            status=OntologyAnnotation(term='S'))
        self.assertEqual(expected_publication, self.publication)
        self.assertEqual(
            hash(expected_publication),  hash(self.publication))

    def test_ne(self):
        expected_other_publication = Publication(
            pubmed_id='2', doi='20', author_list='B. Author', title='T2',
            status=OntologyAnnotation(term='S2'))
        self.assertNotEqual(expected_other_publication, self.publication)
        self.assertNotEqual(
            hash(expected_other_publication), hash(self.publication))


class PersonTest(unittest.TestCase):

    def setUp(self):
        self.person_default = Person()
        self.person = Person(last_name='L', first_name='F', mid_initials='M',
                             email='a@b.com', phone='0', fax='1', address='A',
                             affiliation='Af',
                             roles=[OntologyAnnotation(term='R')])

    def test_repr(self):
        self.assertEqual('isatools.model.Person(last_name="", first_name="", '
                         'mid_initials="", email="", phone="", fax="", '
                         'address="", affiliation="", roles=[], comments=[])',
                         repr(self.person_default))
        self.assertEqual('isatools.model.Person(last_name="L", first_name="F", '
                         'mid_initials="M", email="a@b.com", phone="0", '
                         'fax="1", address="A", affiliation="Af", '
                         'roles=[isatools.model.OntologyAnnotation(term="R", '
                         'term_source=None, term_accession="", comments=[])], '
                         'comments=[])',
                         repr(self.person))

    def test_str(self):
        self.assertEqual("""Person(
    last_name=
    first_name=
    mid_initials=
    email=
    phone=
    fax=
    address=
    roles=0 OntologyAnnotation objects
    comments=0 Comment objects
)""", str(self.person_default))

        self.assertEqual("""Person(
    last_name=L
    first_name=F
    mid_initials=M
    email=a@b.com
    phone=0
    fax=1
    address=A
    roles=1 OntologyAnnotation objects
    comments=0 Comment objects
)""", str(self.person))

    def test_eq(self):
        expected_person = Person(last_name='L', first_name='F', 
                                 mid_initials='M', email='a@b.com', phone='0', 
                                 fax='1', address='A', affiliation='Af', 
                                 roles=[OntologyAnnotation(
                                     term='R', term_source=None, 
                                     term_accession='', comments=[])], 
                                 comments=[])
        self.assertEqual(expected_person, self.person)
        self.assertEqual(hash(expected_person),  hash(self.person))

    def test_ne(self):
        expected_other_person = Person(last_name='F', first_name='L',
                                 mid_initials='M2', email='c@d.com', phone='1',
                                 fax='2', address='A2', affiliation='Af2',
                                 roles=[OntologyAnnotation(
                                     term='R2', term_source=None,
                                     term_accession='', comments=[])],
                                 comments=[])
        self.assertNotEqual(expected_other_person, self.person)
        self.assertNotEqual(
            hash(expected_other_person), hash(self.person))


class StudyTest(unittest.TestCase):

    def setUp(self):
        self.study_default = Study()
        self.study = Study(
            filename='file', identifier='0', title='T', description='D',
            submission_date=datetime.datetime(day=1, month=1, year=2017),
            public_release_date=datetime.datetime(day=1, month=1, year=2017))

    def test_repr(self):
        self.assertEqual('isatools.model.Study(filename="", '
                         'identifier="", title="", description="", '
                         'submission_date="", public_release_date="", '
                         'contacts=[], design_descriptors=[], publications=[], '
                         'factors=[], protocols=[], assays=[], sources=[], '
                         'samples=[], process_sequence=[], other_material=[], '
                         'characteristic_categories=[], comments=[], units=[])',
                         repr(self.study_default))
        self.assertEqual('isatools.model.Study(filename="file", '
                         'identifier="0", title="T", description="D", '
                         'submission_date="2017-01-01 00:00:00", '
                         'public_release_date="2017-01-01 00:00:00", '
                         'contacts=[], design_descriptors=[], publications=[], '
                         'factors=[], protocols=[], assays=[], sources=[], '
                         'samples=[], process_sequence=[], other_material=[], '
                         'characteristic_categories=[], comments=[], units=[])',
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
    characteristic_categories=0 Characteristic objects
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
    characteristic_categories=0 Characteristic objects
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


class StudyFactorTest(unittest.TestCase):

    def setUp(self):
        self.factor_default = StudyFactor()
        self.factor = StudyFactor(name='N', factor_type=OntologyAnnotation('T'))

    def test_repr(self):
        self.assertEqual('isatools.model.StudyFactor(name="", '
                         'factor_type=isatools.model.OntologyAnnotation('
                         'term="", term_source=None, term_accession="", '
                         'comments=[]), comments=[])',
                         repr(self.factor_default))
        self.assertEqual('isatools.model.StudyFactor(name="N", '
                         'factor_type=isatools.model.OntologyAnnotation('
                         'term="T", term_source=None, term_accession="", '
                         'comments=[]), comments=[])',
                         repr(self.factor))

    def test_str(self):
        self.assertEqual("""StudyFactor(
    name=
    factor_type=
    comments=0 Comment objects
)""", str(self.factor_default))

        self.assertEqual("""StudyFactor(
    name=N
    factor_type=T
    comments=0 Comment objects
)""", str(self.factor))

    def test_eq(self):
        expected_factor = StudyFactor(
            name='N', factor_type=OntologyAnnotation(term='T'))
        self.assertEqual(expected_factor, self.factor)
        self.assertEqual(hash(expected_factor),  hash(self.factor))

    def test_ne(self):
        expected_other_factor = StudyFactor(
            name='N2', factor_type=OntologyAnnotation(term='T2'))
        self.assertNotEqual(expected_other_factor, self.factor)
        self.assertNotEqual(hash(expected_other_factor), hash(self.factor))


class CharacteristicTest(unittest.TestCase):

    def setUp(self):
        self.characteristic_default = Characteristic()
        self.characteristic = Characteristic(
            category=OntologyAnnotation(term='C'), value=0,
            unit=OntologyAnnotation(term='U') )

    def test_repr(self):
        self.assertEqual('isatools.model.Characteristic('
                         'category=isatools.model.OntologyAnnotation('
                         'term="", term_source=None, term_accession="", '
                         'comments=[]), '
                         'value=isatools.model.OntologyAnnotation('
                         'term="", term_source=None, term_accession="", '
                         'comments=[]), unit=None, comments=[])',
                         repr(self.characteristic_default))
        self.assertEqual('isatools.model.Characteristic('
                         'category=isatools.model.OntologyAnnotation('
                         'term="C", term_source=None, term_accession="", '
                         'comments=[]), value=0, '
                         'unit=isatools.model.OntologyAnnotation(term="U", '
                         'term_source=None, term_accession="", comments=[]), '
                         'comments=[])', repr(self.characteristic))

    def test_str(self):
        self.assertEqual("""Characteristic(
    category=
    value=
    unit=
    comments=0 Comment objects
)""", str(self.characteristic_default))

        self.assertEqual("""Characteristic(
    category=C
    value=0
    unit=U
    comments=0 Comment objects
)""", str(self.characteristic))

    def test_eq(self):
        expected_characteristic = Characteristic(
            category=OntologyAnnotation(term='C'), value=0,
            unit=OntologyAnnotation(term='U'))
        self.assertEqual(expected_characteristic, self.characteristic)
        self.assertEqual(
            hash(expected_characteristic), hash(self.characteristic))

    def test_ne(self):
        expected_other_characteristic = Characteristic(
            category=OntologyAnnotation(term='C2'), value=1,
            unit=OntologyAnnotation(term='U2'))
        self.assertNotEqual(expected_other_characteristic, self.characteristic)
        self.assertNotEqual(
            hash(expected_other_characteristic), hash(self.characteristic))