"""Tests on isatools.model classes"""
from __future__ import absolute_import
import datetime
import unittest

from isatools.model import Investigation


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

