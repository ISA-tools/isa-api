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