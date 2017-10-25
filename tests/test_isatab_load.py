"""Tests on isatab.py package"""
from __future__ import absolute_import
import io
from isatools import isatab
from isatools.model import *
import unittest


class InvestigationParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = isatab.InvestigationParser()
        self.ontology_source_ref_section = \
            u'ONTOLOGY SOURCE REFERENCE\n' \
            u'Term Source Name\t"A"\t"B"\t"C"\t"D"\n' \
            u'Term Source File\t"f1"\t"f2"\t"f3"\t"f4"\n' \
            u'Term Source Version\t"1"\t"2"\t"3"\t"4"\n' \
            u'Term Source Description\t"d1"\t"d2"\t"d3"\t"d4"'

        self.os1 = OntologySource('A', 'f1', '1', 'd1')
        self.os2 = OntologySource('B', 'f2', '2', 'd2')
        self.os3 = OntologySource('C', 'f3', '3', 'd3')
        self.os4 = OntologySource('D', 'f4', '4', 'd4')

        self.investigation_section = \
            u'INVESTIGATION\n' \
            u'Investigation Identifier\t"ID"\n' \
            u'Investigation Title\t"T"\n' \
            u'Investigation Description\t"D"\n' \
            u'Investigation Submission Date\t"2017-10-24"\n' \
            u'Investigation Public Release Date\t"2017-10-25"'
        self.i = Investigation(identifier='ID', title='T', description='D',
                               submission_date='2017-10-24',
                               public_release_date='2017-10-25')

        self.investigation_publications_section = \
            u'INVESTIGATION PUBLICATIONS\n' \
            u'Investigation PubMed ID\t"0"\n' \
            u'Investigation Publication DOI\t"doi"\n' \
            u'Investigation Publication Author List\t"AL"\n' \
            u'Investigation Publication Title\t"T"\n' \
            u'Investigation Publication Status\t"S"\n' \
            u'Investigation Publication Status Term Accession Number\t"acc"\n' \
            u'Investigation Publication Status Term Source REF\t"src"'
        self.publication = Publication('0', 'doi', 'AL', 'T',
                                       status=OntologyAnnotation('S', 'acc',
                                                                 'src'))

    def test_parse_ontology_source_reference(self):
        self.parser.parse(io.StringIO(self.ontology_source_ref_section))
        self.assertIn(self.os1, self.parser.isa.ontology_source_references)
        self.assertIn(self.os2, self.parser.isa.ontology_source_references)
        self.assertIn(self.os3, self.parser.isa.ontology_source_references)
        self.assertIn(self.os4, self.parser.isa.ontology_source_references)

    def test_parse_investigation_section(self):
        self.parser.parse(io.StringIO(self.investigation_section))
        self.assertEqual(self.i, self.parser.isa)

    def test_parse_investigation_publications_section(self):
        self.parser.parse(io.StringIO(self.investigation_publications_section))
        self.assertIn(self.publication, self.parser.isa.publications)