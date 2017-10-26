"""Tests on isatab.py package"""
from __future__ import absolute_import
import io
from isatools import isatab
from isatools.model import *
import unittest
import tempfile
import os


class InvestigationParserUnitTests(unittest.TestCase):

    def setUp(self):
        self.parser = isatab.InvestigationParser()
        self.ontology_source_ref_section = \
            u'ONTOLOGY SOURCE REFERENCE\n' \
            u'Term Source Name\t"A"\t"B"\n' \
            u'Term Source File\t"f1"\t"f2"\n' \
            u'Term Source Version\t"1"\t"2"\n' \
            u'Term Source Description\t"d1"\t"d2"'

        self.os1 = OntologySource('A', 'f1', '1', 'd1')
        self.os2 = OntologySource('B', 'f2', '2', 'd2')

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
            u'Investigation PubMed ID\t"0"\t"1"\n' \
            u'Investigation Publication DOI\t"doi1"\t"doi2"\n' \
            u'Investigation Publication Author List\t"AL1"\t"AL2"\n' \
            u'Investigation Publication Title\t"T1"\t"T2"\n' \
            u'Investigation Publication Status\t"S1"\t"S2"\n' \
            u'Investigation Publication Status Term Accession Number\t"acc1"\t"acc2"\n' \
            u'Investigation Publication Status Term Source REF\t"src1"\t"src2"'
        
        self.publication1 = Publication('0', 'doi1', 'AL1', 'T1',)
        self.publication2 = Publication('1', 'doi2', 'AL2', 'T2', )

        self.study_publications_section = \
            u'STUDY\n' \
            u'STUDY PUBLICATIONS\n' \
            u'Study PubMed ID\t"0"\n' \
            u'Study Publication DOI\t"doi1"\n' \
            u'Study Publication Author List\t"AL1"\n' \
            u'Study Publication Title\t"T1"\n' \
            u'Study Publication Status\t"S1"\n' \
            u'Study Publication Status Term Accession Number\t"acc1"\n' \
            u'Study Publication Status Term Source REF\t"src1"\n' \
            u'STUDY\n' \
            u'STUDY PUBLICATIONS\n' \
            u'Study PubMed ID\t"0b"\t"1b"\n' \
            u'Study Publication DOI\t"doi1b"\t"doi2b"\n' \
            u'Study Publication Author List\t"AL1b"\t"AL2b"\n' \
            u'Study Publication Title\t"T1b"\t"T2b"\n' \
            u'Study Publication Status\t"S1b"\t"S2b"\n' \
            u'Study Publication Status Term Accession Number\t"acc1b"\t"acc2b"\n' \
            u'Study Publication Status Term Source REF\t"src1b"\t"src2b"'

        self.publication1b = Publication('0b', 'doi1b', 'AL1b', 'T1b', )
        self.publication2b = Publication('1b', 'doi2b', 'AL2b', 'T2b', )

        self.investigation_contacts_section = \
            u'INVESTIGATION CONTACTS\n' \
            u'Investigation Person Last Name\t"ln1"\t"ln2"\n' \
            u'Investigation Person First Name\t"fn1"\t"fn2"\n' \
            u'Investigation Person Mid Initials\t"mi1"\t"mi2"\n' \
            u'Investigation Person Email\t"e1"\t"e2"\n' \
            u'Investigation Person Phone\t"ph1"\t"ph2"\n' \
            u'Investigation Person Fax\t"fax1"\t"fax2"\n' \
            u'Investigation Person Address\t"ad1"\t"ad2"\n' \
            u'Investigation Person Affiliation\t"af1"\t"af2"\n' \
            u'Investigation Person Roles\t"r1"\t"r2"\n' \
            u'Investigation Person Roles Term Accession Number\t"r_acc1"\t"r_acc2"\n' \
            u'Investigation Person Roles Term Source REF\t"r_src1"\t"r_src2"'
        
        self.study_contacts_section = \
            u'STUDY\n'\
            u'STUDY CONTACTS\n' \
            u'Study Person Last Name\t"ln1"\t"ln2"\n' \
            u'Study Person First Name\t"fn1"\t"fn2"\n' \
            u'Study Person Mid Initials\t"mi1"\t"mi2"\n' \
            u'Study Person Email\t"e1"\t"e2"\n' \
            u'Study Person Phone\t"ph1"\t"ph2"\n' \
            u'Study Person Fax\t"fax1"\t"fax2"\n' \
            u'Study Person Address\t"ad1"\t"ad2"\n' \
            u'Study Person Affiliation\t"af1"\t"af2"\n' \
            u'Study Person Roles\t"r1"\t"r2"\n' \
            u'Study Person Roles Term Accession Number\t"r_acc1"\t"r_acc2"\n' \
            u'Study Person Roles Term Source REF\t"r_src1"\t"r_src2"\n' \
            u'STUDY\n' \
            u'STUDY CONTACTS\n' \
            u'Study Person Last Name\t"ln1b"\t"ln2b"\n' \
            u'Study Person First Name\t"fn1b"\t"fn2b"\n' \
            u'Study Person Mid Initials\t"mi1b"\t"mi2b"\n' \
            u'Study Person Email\t"e1b"\t"e2b"\n' \
            u'Study Person Phone\t"ph1b"\t"ph2b"\n' \
            u'Study Person Fax\t"fax1b"\t"fax2b"\n' \
            u'Study Person Address\t"ad1b"\t"ad2b"\n' \
            u'Study Person Affiliation\t"af1b"\t"af2b"\n' \
            u'Study Person Roles\t"r1b"\t"r2b"\n' \
            u'Study Person Roles Term Accession Number\t"r_acc1b"\t"r_acc2b"\n' \
            u'Study Person Roles Term Source REF\t"r_src1b"\t"r_src2b"'

        role1 = OntologyAnnotation('r1', 'r_src1', 'r_acc1')
        role2 = OntologyAnnotation('r2', 'r_src2', 'r_acc2')
        self.person1 = Person('ln1', 'fn1', 'mi1', 'e1', 'ph1', 'fax1', 'ad1',
                              'af1', [role1])
        self.person2 = Person('ln2', 'fn2', 'mi2', 'e2', 'ph2', 'fax2', 'ad2', 
                              'af2', [role2])
        role1b = OntologyAnnotation('r1b', 'r_src1b', 'r_acc1b')
        role2b = OntologyAnnotation('r2b', 'r_src2b', 'r_acc2b')
        self.person1b = Person('ln1b', 'fn1b', 'mi1b', 'e1b', 'ph1b', 'fax1b', 
                               'ad1b', 'af1b', [role1b])
        self.person2b = Person('ln2b', 'fn2b', 'mi2b', 'e2b', 'ph2b', 'fax2b', 
                               'ad2b', 'af2b', [role2b])

        self.study_section = \
            u'STUDY\n' \
            u'Study Identifier\t"ID"\n' \
            u'Study Title\t"T"\n' \
            u'Study Description\t"D"\n' \
            u'Study Submission Date\t"2017-10-24"\n' \
            u'Study Public Release Date\t"2017-10-25"\n' \
            u'Study File Name\t"f"'

        self.s = Study(identifier='ID', title='T', description='D',
                               submission_date='2017-10-24',
                               public_release_date='2017-10-25', filename='f')

        self.study_design_descriptors_section = \
            u'STUDY\n' \
            u'STUDY DESIGN DESCRIPTORS\n' \
            u'Study Design Type\t"d1"\t"d2"\n' \
            u'Study Design Type Term Accession Number\t"acc1"\t"acc2"\n' \
            u'Study Design Type Term Source REF\t"src1"\t"src2"'

        self.study_design = [
            OntologyAnnotation('d1', 'src1', 'acc1'),
            OntologyAnnotation('d2', 'src2', 'acc2')
        ]

        self.study_factors_section = \
            u'STUDY\n' \
            u'STUDY FACTORS\n' \
            u'Study Factor Name\t"f1"\t"f2"\n' \
            u'Study Factor Type\t"t1"\t"t2"\n' \
            u'Study Factor Type Term Accession Number\t"acc1"\t"acc2"\n' \
            u'Study Factor Type Term Source REF\t"src1"\t"src2"'

        self.study_factors = [
            StudyFactor(name='f1',
                        factor_type=OntologyAnnotation('t1', 'src1', 'acc1')),
            StudyFactor(name='f2',
                        factor_type=OntologyAnnotation('t2', 'src2', 'acc2'))
        ]
        
        self.study_assays_section = \
            u'STUDY\n' \
            u'STUDY ASSAYS\n' \
            u'Study Assay Measurement Type\t"mt1"\t"mt2"\n' \
            u'Study Assay Measurement Type Term Accession Number\t"mt_acc1"\t"mt_acc2"\n' \
            u'Study Assay Measurement Type Term Source REF\t"mt_src1"\t"mt_src2"\n' \
            u'Study Assay Technology Type\t"tt1"\t"tt2"\n' \
            u'Study Assay Technology Type Term Accession Number\t"tt_acc1"\t"tt_acc2"\n' \
            u'Study Assay Technology Type Term Source REF\t"tt_src1"\t"tt_src2"\n' \
            u'Study Assay Technology Platform\t"tp1"\t"tp2"\n' \
            u'Study Assay File Name\t"f1"\t"f2"'
        
        self.study_assay1 = Assay(
            measurement_type=OntologyAnnotation('mt1', 'mt_src1', 'mt_acc1'),
            technology_type=OntologyAnnotation('tt1', 'tt_src1', 'tt_acc1'),
            technology_platform='tp1', filename='f1'
        )
        self.study_assay2 = Assay(
            measurement_type=OntologyAnnotation('mt2', 'mt_src2', 'mt_acc2'),
            technology_type=OntologyAnnotation('tt2', 'tt_src2', 'tt_acc2'),
            technology_platform='tp2', filename='f2'
        )

        self.study_protocols_section = \
            u'STUDY\n' \
            u'STUDY PROTOCOLS\n' \
            u'Study Protocol Name\t"p1"\t"p2"\n' \
            u'Study Protocol Type\t"pt1"\t"pt2"\n' \
            u'Study Protocol Type Term Accession Number\t"pt1_acc"\t"pt2_acc"\n' \
            u'Study Protocol Type Term Source REF\t"pt1_src"\t"pt2_src"\n' \
            u'Study Protocol Description\t"d1"\t"d2"\n' \
            u'Study Protocol URI\t"u1"\t"u2"\n' \
            u'Study Protocol Version\t"v1"\t"v2"\n' \
            u'Study Protocol Parameters Name\t"ppn1a;ppn1b"\t"ppn2"\n' \
            u'Study Protocol Parameters Name Term Accession Number\t"ppn1a_acc;ppn1b_acc"\t"ppn2_acc"\n' \
            u'Study Protocol Parameters Name Term Source REF\t"ppn1a_src;ppn1b_src"\t"ppn2_src"\n' \
            u'Study Protocol Components Name\t"cn1a;cn1b"\t"cn2"\n' \
            u'Study Protocol Components Type\t"ct1a;ct1b"\t"ct2"\n' \
            u'Study Protocol Components Type Term Accession Number\t"ct1a_acc;ct1b_acc"\t"ct2_acc"\n' \
            u'Study Protocol Components Type Term Source REF\t"ct1a_src;ct1b_src"\t"ct2_src"\n' \
            u'STUDY\n' \
            u'STUDY PROTOCOLS\n' \
            u'Study Protocol Name\t"p1b"\n' \
            u'Study Protocol Type\t"pt1b"\n' \
            u'Study Protocol Type Term Accession Number\t"pt1b_acc"\n' \
            u'Study Protocol Type Term Source REF\t"pt1b_src"\n' \
            u'Study Protocol Description\t"d1b"\n' \
            u'Study Protocol URI\t"u1b"\n' \
            u'Study Protocol Version\t"v1b"\n' \
            u'Study Protocol Parameters Name\t"ppn1b"\n' \
            u'Study Protocol Parameters Name Term Accession Number\t"ppn1b_acc"\n' \
            u'Study Protocol Parameters Name Term Source REF\t"ppn1b_src"\n' \
            u'Study Protocol Components Name\t"cn1b"\n' \
            u'Study Protocol Components Type\t"ct1b"\n' \
            u'Study Protocol Components Type Term Accession Number\t"ct1b_acc"\n' \
            u'Study Protocol Components Type Term Source REF\t"ct1b_src"'

        self.study_protocol1 = Protocol(
            '', 'p1', OntologyAnnotation('pt1', 'pt1_src', 'pt1_acc'), 'u1',
            'd1', 'v1', [
                ProtocolParameter(
                    parameter_name=OntologyAnnotation('ppn1a', 'ppn1a_src',
                                                      'ppn1a_acc')),
                ProtocolParameter(
                    parameter_name=OntologyAnnotation('ppn1b', 'ppn1b_src',
                                                      'ppn1b_acc'))
            ], [
                ProtocolComponent(
                    name='cn1a',
                    component_type=OntologyAnnotation('ct1a', 'ct1a_src',
                                                      'ct1a_acc')),
                ProtocolComponent(
                    name='cn1b',
                    component_type=OntologyAnnotation('ct1b', 'ct1b_src',
                                                      'ct1b_acc'))
            ])
        self.study_protocol2 = Protocol(
            '', 'p2', OntologyAnnotation('pt2', 'pt2_src', 'pt2_acc'), 'u2',
            'd2', 'v2', [
                ProtocolParameter(
                    parameter_name=OntologyAnnotation('ppn2', 'ppn2_src',
                                                      'ppn2_acc'))
            ], [
                ProtocolComponent(
                    name='cn2',
                    component_type=OntologyAnnotation('ct2', 'ct2_src',
                                                      'ct2_acc'))
            ])
        self.study_protocol1b = Protocol(
            '', 'p1b', OntologyAnnotation('pt1b', 'pt1b_src', 'pt1b_acc'), 'u1b',
            'd1b', 'v1b', [
                ProtocolParameter(
                    parameter_name=OntologyAnnotation('ppn1b', 'ppn1b_src',
                                                      'ppn1b_acc'))
            ], [
                ProtocolComponent(
                    name='cn1b',
                    component_type=OntologyAnnotation('ct1b', 'ct1b_src',
                                                      'ct1b_acc'))
            ])
        
    def test_parse_ontology_source_reference(self):
        self.parser.parse(io.StringIO(self.ontology_source_ref_section))
        self.assertIn(self.os1, self.parser.isa.ontology_source_references)
        self.assertIn(self.os2, self.parser.isa.ontology_source_references)

    def test_parse_investigation_section(self):
        self.parser.parse(io.StringIO(self.investigation_section))
        self.assertEqual(self.i, self.parser.isa)

    def test_parse_investigation_publications_section(self):
        self.parser.parse(io.StringIO(self.investigation_publications_section))
        self.assertIn(self.publication1, self.parser.isa.publications)

    def test_parse_study_publications_section(self):
        self.parser.parse(io.StringIO(self.study_publications_section))
        self.assertIn(self.publication1b,
                      self.parser.isa.studies[-1].publications)
        self.assertIn(self.publication2b,
                      self.parser.isa.studies[-1].publications)
        
    def test_parse_investigation_contacts_section(self):
        self.parser.parse(io.StringIO(self.investigation_contacts_section))
        self.assertIn(self.person1, self.parser.isa.contacts)

    def test_parse_study_contacts_section(self):
        self.parser.parse(io.StringIO(self.study_contacts_section))
        self.assertIn(self.person1b,
                      self.parser.isa.studies[-1].contacts)
        self.assertIn(self.person2b,
                      self.parser.isa.studies[-1].contacts)

    def test_parse_study_section(self):
        self.parser.parse(io.StringIO(self.study_section))
        self.assertEqual(self.s, self.parser.isa.studies[-1])

    def test_parse_study_design_descriptors_section(self):
        self.parser.parse(io.StringIO(self.study_design_descriptors_section))
        self.assertEqual(self.study_design,
                         self.parser.isa.studies[-1].design_descriptors)

    def test_parse_study_factors_section(self):
        self.parser.parse(io.StringIO(self.study_factors_section))
        self.assertEqual(self.study_factors,
                         self.parser.isa.studies[-1].factors)

    def test_parse_study_assays_section(self):
        self.parser.parse(io.StringIO(self.study_assays_section))
        self.assertIn(self.study_assay1, self.parser.isa.studies[-1].assays)
        self.assertIn(self.study_assay2, self.parser.isa.studies[-1].assays)

    def test_parse_study_protocols_section(self):
        self.parser.parse(io.StringIO(self.study_protocols_section))
        self.assertIn(self.study_protocol1,
                      self.parser.isa.studies[0].protocols)
        self.assertIn(self.study_protocol2,
                      self.parser.isa.studies[0].protocols)
        self.assertIn(self.study_protocol1b,
                      self.parser.isa.studies[1].protocols)


class InvestigationParserIntegrationTests(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = os.path.join(os.path.dirname(__file__), 'data',
                                          'tab')
        self.parser = isatab.InvestigationParser()

    def tearDown(self):
        # os.rmdir(self._tmp_dir)
        pass

    def test_isatab_load_bii_i_1(self):
        with open(os.path.join(self._tab_data_dir, 'BII-I-1', 'i_investigation.txt')) as fp:
            self.parser.parse(fp)
            isa = self.parser.isa

            self.assertListEqual([s.filename for s in isa.studies],
                                 ['s_BII-S-1.txt',
                                  's_BII-S-2.txt'])
            study_bii_s_1 = \
            [s for s in isa.studies if s.filename == 's_BII-S-1.txt'][0]
            self.assertListEqual([a.filename for a in study_bii_s_1.assays],
                                 ['a_proteome.txt', 'a_metabolome.txt',
                                  'a_transcriptome.txt'])
            study_bii_s_2 = \
            [s for s in isa.studies if s.filename == 's_BII-S-2.txt'][0]
            self.assertListEqual([a.filename for a in study_bii_s_2.assays],
                                 ['a_microarray.txt'])

    def test_isatab_load_bii_s_3(self):
        with open(os.path.join(self._tab_data_dir, 'BII-S-3', 'i_gilbert.txt')) as fp:
            self.parser.parse(fp)
            isa = self.parser.isa

            self.assertListEqual([s.filename for s in isa.studies],
                                 ['s_BII-S-3.txt'])
            study_bii_s_3 = \
            [s for s in isa.studies if s.filename == 's_BII-S-3.txt'][0]
            self.assertListEqual([a.filename for a in study_bii_s_3.assays],
                                 ['a_gilbert-assay-Gx.txt',
                                  'a_gilbert-assay-Tx.txt'])

    def test_isatab_load_bii_s_7(self):
        with open(os.path.join(self._tab_data_dir, 'BII-S-7', 'i_matteo.txt'), 'rU') as fp:
            self.parser.parse(fp)
            isa = self.parser.isa

            self.assertListEqual([s.filename for s in isa.studies], [
                's_BII-S-7.txt'])
            study_bii_s_7 = \
            [s for s in isa.studies if s.filename == 's_BII-S-7.txt'][0]
            self.assertListEqual([a.filename for a in study_bii_s_7.assays],
                                 ['a_matteo-assay-Gx.txt'])
