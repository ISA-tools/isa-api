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