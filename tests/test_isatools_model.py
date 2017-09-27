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
    ontology_source_references=[]
    publications=[]
    contacts=[]
    studies=[]
    comments=[]
)""", str(self.investigation_default))

        self.assertEqual("""Investigation(
    identifier=id
    filename=file
    title=T
    submission_date=2017-01-01 00:00:00
    public_release_date=2017-01-01 00:00:00
    ontology_source_references=[]
    publications=[]
    contacts=[]
    studies=[]
    comments=[]
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
        self.assertNotEqual(hash(expected_other_investigation), hash(self.investigation))
