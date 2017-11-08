"""Tests on isatab.py package"""
from __future__ import absolute_import
import io
from isatools import isatab
from isatools.model import *
import unittest
import os
import sys

# Function for opening correctly a CSV file for csv.reader() for both Python 2 and 3
def utf8_text_file_open(path):
    if sys.version_info[0] < 3: 
        fp = open(path, 'rb')
    else:
        fp = open(path, 'r', newline='', encoding='utf8')
    return fp

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

        self.investigation_section_with_comment_lines = \
            u'# This line is a comment\n' \
            u'INVESTIGATION\n' \
            u'Investigation Identifier\t"ID"\n' \
            u'Investigation Title\t"T"\n' \
            u'# This line is another comment\n' \
            u'Investigation Description\t"D"\n' \
            u'Investigation Submission Date\t"2017-10-24"\n' \
            u'Investigation Public Release Date\t"2017-10-25"'

        self.investigation_publications_section = \
            u'INVESTIGATION PUBLICATIONS\n' \
            u'Investigation PubMed ID\t"0"\t"1"\n' \
            u'Investigation Publication DOI\t"doi1"\t"doi2"\n' \
            u'Investigation Publication Author List\t"AL1"\t"AL2"\n' \
            u'Investigation Publication Title\t"T1"\t"T2"\n' \
            u'Investigation Publication Status\t"S1"\t"S2"\n' \
            u'Investigation Publication Status Term Accession Number\t"acc1"\t"acc2"\n' \
            u'Investigation Publication Status Term Source REF\t"src1"\t"src2"'

        publication_status1 = OntologyAnnotation('S1', 'src1', 'acc1')
        publication_status2 = OntologyAnnotation('S2', 'src2', 'acc2')
        self.publication1 = Publication('0', 'doi1', 'AL1', 'T1',
                                        publication_status1)
        self.publication2 = Publication('1', 'doi2', 'AL2', 'T2',
                                        publication_status2)

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

        publication_status1b = OntologyAnnotation('S1b', 'src1b', 'acc1b')
        publication_status2b = OntologyAnnotation('S2b', 'src2b', 'acc2b')
        self.publication1b = Publication('0b', 'doi1b', 'AL1b', 'T1b',
                                         publication_status1b)
        self.publication2b = Publication('1b', 'doi2b', 'AL2b', 'T2b',
                                         publication_status2b)

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
            '', 'p1b', OntologyAnnotation('pt1b', 'pt1b_src', 'pt1b_acc'),
            'u1b',
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

    def test_parse_and_ignore_comment_lines(self):
        self.parser.parse(
            io.StringIO(self.investigation_section_with_comment_lines))
        self.assertEqual(self.i, self.parser.isa)
        
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
        self._tab_data_dir = os.path.join(
            os.path.dirname(__file__), 'data', 'tab')
        self.parser = isatab.InvestigationParser()

    def tearDown(self):
        pass

    def test_isatab_load_bii_i_1(self):
        with io.open(os.path.join(self._tab_data_dir, 'BII-I-1',
                                  'i_investigation.txt')) as fp:
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
        with io.open(os.path.join(self._tab_data_dir, 'BII-S-3',
                                  'i_gilbert.txt')) as fp:
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
        with io.open(os.path.join(self._tab_data_dir, 'BII-S-7',
                                  'i_matteo.txt')) as fp:
            self.parser.parse(fp)
            isa = self.parser.isa

            self.assertListEqual([s.filename for s in isa.studies], [
                's_BII-S-7.txt'])
            study_bii_s_7 = \
            [s for s in isa.studies if s.filename == 's_BII-S-7.txt'][0]
            self.assertListEqual([a.filename for a in study_bii_s_7.assays],
                                 ['a_matteo-assay-Gx.txt'])

    def test_isatab_load_mtbls30(self):
        with utf8_text_file_open(os.path.join(self._tab_data_dir, 'MTBLS30-2',
                                  'i_Investigation.txt')) as fp:
            self.parser.parse(fp)
            isa = self.parser.isa

            self.assertListEqual([s.filename for s in isa.studies], [
                's_York_SRC_metabolomics.txt'])
            study_bii_s_7 = \
            [s for s in isa.studies if s.filename == 's_York_SRC_metabolomics.txt'][0]
            self.assertListEqual([a.filename for a in study_bii_s_7.assays],
                                 ['a_york_src_GC_mass_spectrometry.txt', 'a_york_src_FIA_mass_spectrometry.txt'])


class StudySampleTableParserUnitTest(unittest.TestCase):

    """Note: does not account for missing Protocol REF preprocessing"""

    def setUp(self):
        self.isa = Investigation()
        self.isa.ontology_source_references = [
            OntologySource('A', 'f1', '1', 'd1'),
            OntologySource('B', 'f2', '2', 'd2')]
        self.parser = isatab.StudySampleTableParser(self.isa)

        self.study_sample_table = \
            u'Source Name\tSample Name\n' \
            u'source1\tsample1\n' \
            u'source2\tsample2'

        self.study_sample_table_with_two_sample_names_columns = \
            u'Source Name\tSample Name\tSample Name\n' \
            u'source1\tsample1\tsample2\n'

        self.study_sample_table_with_numbers_as_ids = \
            u'Source Name\tSample Name\tSample Name\n' \
            u'source1\t1\t2\n'

        self.study_sample_table_with_process = \
            u'Source Name\tProtocol REF\tSample Name\n' \
            u'source1\tsample collection\tsample1\n' \
            u'source2\tsample collection\tsample2'

        self.study_sample_table_with_process_split = \
            u'Source Name\tProtocol REF\tSample Name\n' \
            u'source1\tsample collection\tsample1\n' \
            u'source1\tsample collection\tsample2'

        self.study_sample_table_with_process_pool = \
            u'Source Name\tProtocol REF\tSample Name\n' \
            u'source1\tsample collection\tsample1\n' \
            u'source2\tsample collection\tsample1'

        self.source_list = [Source(name='source1'), Source(name='source2')]
        self.sample_list = [Sample(name='sample1'), Sample(name='sample2')]
        self.sample_list_with_numbers_as_ids = [Sample(name='1'),
                                                Sample(name='2')]

    def test_parse_sources(self):
        self.parser.parse(io.StringIO(self.study_sample_table))
        self.assertListEqual(sorted(self.parser.sources, key=lambda x: repr(x)),
                             sorted(self.source_list, key=lambda x: repr(x)))

    def test_parse_samples(self):
        self.parser.parse(io.StringIO(self.study_sample_table))
        self.assertListEqual(sorted(self.parser.samples, key=lambda x: repr(x)),
                             sorted(self.sample_list, key=lambda x: repr(x)))

    def test_parse_samples_with_two_sample_names_columns(self):
        self.parser.parse(
            io.StringIO(self.study_sample_table_with_two_sample_names_columns))
        self.assertListEqual(sorted(self.parser.samples, key=lambda x: repr(x)),
                             sorted(self.sample_list, key=lambda x: repr(x)))

    def test_parse_samples_with_with_numbers_as_ids(self):
        self.parser.parse(
            io.StringIO(self.study_sample_table_with_numbers_as_ids))
        self.assertListEqual(sorted(self.parser.samples, key=lambda x: repr(x)),
                             sorted(self.sample_list_with_numbers_as_ids,
                                    key=lambda x: repr(x)))

    def test_parse_process_sequence(self):
        self.parser.parse(
            io.StringIO(self.study_sample_table_with_process))
        self.assertEqual(len(self.parser.process_sequence), 2)
        self.assertIn(self.source_list[0],
                      self.parser.process_sequence[0].inputs)
        self.assertIn(self.sample_list[0],
                      self.parser.process_sequence[0].outputs)
        self.assertIn(self.source_list[-1],
                      self.parser.process_sequence[-1].inputs)
        self.assertIn(self.sample_list[-1],
                      self.parser.process_sequence[-1].outputs)

    def test_parse_process_sequence_split(self):
        self.parser.parse(
            io.StringIO(self.study_sample_table_with_process_split))
        self.assertEqual(len(self.parser.process_sequence), 1)
        self.assertIn(self.source_list[0],
                      self.parser.process_sequence[0].inputs)
        self.assertIn(self.sample_list[0],
                      self.parser.process_sequence[0].outputs)
        self.assertIn(self.sample_list[-1],
                      self.parser.process_sequence[0].outputs)

    def test_parse_process_sequence_pool(self):
        self.parser.parse(
            io.StringIO(self.study_sample_table_with_process_pool))
        self.assertEqual(len(self.parser.process_sequence), 1)
        self.assertIn(self.source_list[0],
                      self.parser.process_sequence[0].inputs)
        self.assertIn(self.source_list[-1],
                      self.parser.process_sequence[0].inputs)
        self.assertIn(self.sample_list[0],
                      self.parser.process_sequence[0].outputs)


class StudySampleTableParserIntegrationTest(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = os.path.join(
            os.path.dirname(__file__), 'data', 'tab')

    def tearDown(self):
        pass

    def test_isatab_parse_study_table_bii_s_1(self):
        with io.open(os.path.join(self._tab_data_dir, 'BII-I-1',
                                  'i_investigation.txt')) as fp:
            investigation_parser = isatab.InvestigationParser()
            investigation_parser.parse(fp)

            self.parser = isatab.StudySampleTableParser(
                investigation_parser.isa)
            self.parser.parse(os.path.join(self._tab_data_dir, 'BII-I-1',
                                           investigation_parser.isa.studies[
                                               0].filename))
            self.assertEqual(len(self.parser.sources), 18)
            self.assertEqual(len(self.parser.samples), 164)
            self.assertEqual(len(self.parser.process_sequence), 18)

    def test_isatab_parse_bii_s_2(self):
        with io.open(os.path.join(self._tab_data_dir, 'BII-I-1',
                                  'i_investigation.txt')) as fp:
            investigation_parser = isatab.InvestigationParser()
            investigation_parser.parse(fp)
            self.parser = isatab.StudySampleTableParser(
                investigation_parser.isa)
            self.parser.parse(os.path.join(self._tab_data_dir, 'BII-I-1',
                                           investigation_parser.isa.studies[
                                               1].filename))
            self.assertEqual(len(self.parser.sources), 1)
            self.assertEqual(len(self.parser.samples), 2)
            self.assertEqual(len(self.parser.process_sequence), 1)

    def test_isatab_parse_study_table_bii_s_3(self):
        with io.open(os.path.join(self._tab_data_dir, 'BII-S-3',
                                  'i_gilbert.txt')) as fp:
            investigation_parser = isatab.InvestigationParser()
            investigation_parser.parse(fp)
            self.parser = isatab.StudySampleTableParser(
                investigation_parser.isa)
            self.parser.parse(os.path.join(self._tab_data_dir, 'BII-S-3',
                                           investigation_parser.isa.studies[
                                               -1].filename))
            self.assertEqual(len(self.parser.sources), 4)
            self.assertEqual(len(self.parser.samples), 4)
            self.assertEqual(len(self.parser.process_sequence), 4)

    def test_isatab_load_bii_s_7(self):
        with io.open(os.path.join(self._tab_data_dir, 'BII-S-7',
                                  'i_matteo.txt')) as fp:
            investigation_parser = isatab.InvestigationParser()
            investigation_parser.parse(fp)
            self.parser = isatab.StudySampleTableParser(
                investigation_parser.isa)
            self.parser.parse(os.path.join(self._tab_data_dir, 'BII-S-7',
                                           investigation_parser.isa.studies[
                                               -1].filename))
            self.assertEqual(len(self.parser.sources), 29)
            self.assertEqual(len(self.parser.samples), 29)
            self.assertEqual(len(self.parser.process_sequence), 29)

    def test_isatab_load_mtbls30(self):
        with utf8_text_file_open(os.path.join(self._tab_data_dir, 'MTBLS30-2',
                                  'i_Investigation.txt')) as fp:
            investigation_parser = isatab.InvestigationParser()
            investigation_parser.parse(fp)
            self.parser = isatab.StudySampleTableParser(
                investigation_parser.isa)
            self.parser.parse(os.path.join(self._tab_data_dir, 'MTBLS30-2',
                                           investigation_parser.isa.studies[
                                               -1].filename))
            self.assertEqual(len(self.parser.sources), 5)
            self.assertEqual(len(self.parser.samples), 300)
            self.assertEqual(len(self.parser.process_sequence), 6)

class AssayTableParserUnitTest(unittest.TestCase):

    def setUp(self):
        self.isa = Investigation()
        self.isa.ontology_source_references = [
            OntologySource('A', 'f1', '1', 'd1'),
            OntologySource('B', 'f2', '2', 'd2')]
        self.parser = isatab.AssayTableParser(self.isa)

        self.assay_table = \
            u'Sample Name\tExtract Name\tLabeled Extract Name\tRaw Data File\n' \
            u'sample1\textract1\t\tfile1.txt\n' \
            u'sample2\t\tlabeled1\tfile2.txt'

        self.assay_table_with_process = \
            u'Sample Name\tProtocol REF\tExtract Name\tProtocol REF\tLabeled Extract Name\tProtocol REF\tRaw Data File\n' \
            u'sample1\tsample extraction\textract1\tlabeling\tlabeled1\tscanning\tfile1.txt\n' \
            u'sample2\tsample extraction\textract1\tlabeling\tlabeled1\tscanning\tfile2.txt'

        self.sample_list = [Sample(name='sample1'), Sample(name='sample2')]
        self.data_file_list = [
            DataFile(filename='file2.txt', label='Raw Data File'),
            DataFile(filename='file1.txt', label='Raw Data File')
        ]
        self.other_material_list = [LabeledExtract(name='labeled1'),
                                    Extract(name='extract1')]

    def test_parse_samples(self):
        self.parser.parse(io.StringIO(self.assay_table))
        self.assertListEqual(sorted(self.parser.samples, key=lambda x: repr(x)),
                             sorted(self.sample_list, key=lambda x: repr(x)))

    def test_parse_data_files(self):
        self.parser.parse(io.StringIO(self.assay_table))
        self.assertListEqual(
            sorted(self.parser.data_files, key=lambda x: repr(x)),
            sorted(self.data_file_list, key=lambda x: repr(x)))

    def test_parse_other_material(self):
        self.parser.parse(io.StringIO(self.assay_table))
        self.assertListEqual(
            sorted(self.parser.other_material, key=lambda x: repr(x)),
            sorted(self.other_material_list, key=lambda x: repr(x)))

    def test_parse_process_sequence(self):
        self.parser.parse(
            io.StringIO(self.assay_table_with_process))
        self.assertEqual(len(self.parser.process_sequence), 3)


class AssayTableParserIntegrationTest(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = os.path.join(
            os.path.dirname(__file__), 'data', 'tab')

    def tearDown(self):
        pass

    def test_isatab_parse_assay_table_bii_s_1_metabolome(self):
        with io.open(os.path.join(self._tab_data_dir, 'BII-I-1',
                                  'i_investigation.txt')) as fp:
            investigation_parser = isatab.InvestigationParser()
            investigation_parser.parse(fp)

            self.parser = isatab.AssayTableParser(
                investigation_parser.isa)
            self.parser.parse(os.path.join(self._tab_data_dir, 'BII-I-1',
                                           'a_metabolome.txt'))
            self.assertEqual(len(self.parser.samples), 92)
            self.assertEqual(len(self.parser.data_files), 111)
            self.assertEqual(len(self.parser.other_material), 92)
            self.assertEqual(len(self.parser.process_sequence), 92)

    def test_isatab_parse_bii_s_1_microarray(self):
        with io.open(os.path.join(self._tab_data_dir, 'BII-I-1',
                                  'i_investigation.txt')) as fp:
            investigation_parser = isatab.InvestigationParser()
            investigation_parser.parse(fp)
            self.parser = isatab.AssayTableParser(
                investigation_parser.isa)
            self.parser.parse(os.path.join(self._tab_data_dir, 'BII-I-1',
                                           'a_microarray.txt'))
            self.assertEqual(len(self.parser.samples), 2)
            self.assertEqual(len(self.parser.data_files), 15)
            self.assertEqual(len(self.parser.other_material), 28)
            self.assertEqual(len(self.parser.process_sequence), 30)

    def test_isatab_parse_bii_s_1_proteome(self):
        with io.open(os.path.join(self._tab_data_dir, 'BII-I-1',
                                  'i_investigation.txt')) as fp:
            investigation_parser = isatab.InvestigationParser()
            investigation_parser.parse(fp)
            self.parser = isatab.AssayTableParser(
                investigation_parser.isa)
            self.parser.parse(os.path.join(self._tab_data_dir, 'BII-I-1',
                                           'a_proteome.txt'))
            self.assertEqual(len(self.parser.samples), 8)
            self.assertEqual(len(self.parser.data_files), 7)
            self.assertEqual(len(self.parser.other_material), 19)
            self.assertEqual(len(self.parser.process_sequence), 16)

    def test_isatab_parse_bii_s_2_trascriptome(self):
        with io.open(os.path.join(self._tab_data_dir, 'BII-I-1',
                                  'i_investigation.txt')) as fp:
            investigation_parser = isatab.InvestigationParser()
            investigation_parser.parse(fp)
            self.parser = isatab.AssayTableParser(
                investigation_parser.isa)
            self.parser.parse(os.path.join(self._tab_data_dir, 'BII-I-1',
                                           'a_transcriptome.txt'))
            self.assertEqual(len(self.parser.samples), 48)
            self.assertEqual(len(self.parser.data_files), 49)
            self.assertEqual(len(self.parser.other_material), 96)
            self.assertEqual(len(self.parser.process_sequence), 144)

    def test_isatab_parse_bii_s_3_Gx(self):
        with io.open(os.path.join(self._tab_data_dir, 'BII-S-3',
                               'i_gilbert.txt')) as fp:
            investigation_parser = isatab.InvestigationParser()
            investigation_parser.parse(fp)
            self.parser = isatab.AssayTableParser(
                investigation_parser.isa)
            self.parser.parse(os.path.join(self._tab_data_dir, 'BII-S-3',
                                           'a_gilbert-assay-Gx.txt'))
            self.assertEqual(len(self.parser.samples), 4)
            self.assertEqual(len(self.parser.data_files), 6)
            self.assertEqual(len(self.parser.other_material), 4)
            self.assertEqual(len(self.parser.process_sequence), 16)

    def test_isatab_parse_bii_s_3_Tx(self):
        with io.open(os.path.join(self._tab_data_dir, 'BII-S-3',
                               'i_gilbert.txt')) as fp:
            investigation_parser = isatab.InvestigationParser()
            investigation_parser.parse(fp)
            self.parser = isatab.AssayTableParser(
                investigation_parser.isa)
            self.parser.parse(os.path.join(self._tab_data_dir, 'BII-S-3',
                                           'a_gilbert-assay-Tx.txt'))
            self.assertEqual(len(self.parser.samples), 4)
            self.assertEqual(len(self.parser.data_files), 24)
            self.assertEqual(len(self.parser.other_material), 4)
            self.assertEqual(len(self.parser.process_sequence), 16)

    def test_isatab_parse_bii_s_7_Gx(self):
        with io.open(os.path.join(self._tab_data_dir, 'BII-S-7',
                                 'i_matteo.txt')) as fp:
            investigation_parser = isatab.InvestigationParser()
            investigation_parser.parse(fp)
            self.parser = isatab.AssayTableParser(
                investigation_parser.isa)
            self.parser.parse(os.path.join(self._tab_data_dir, 'BII-S-7',
                                           'a_matteo-assay-Gx.txt'))
            self.assertEqual(len(self.parser.samples), 29)
            self.assertEqual(len(self.parser.data_files), 29)
            self.assertEqual(len(self.parser.other_material), 29)
            self.assertEqual(len(self.parser.process_sequence), 116)

class ParserIntegrationTest(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = os.path.join(
            os.path.dirname(__file__), 'data', 'tab')
        self.parser = isatab.Parser()

    def test_parser_with_bii_i_1(self):
        with io.open(os.path.join(self._tab_data_dir, 'BII-I-1',
                                  'i_investigation.txt')) as fp:
            self.parser.parse(fp)
            self.assertEqual(len(self.parser.isa.ontology_source_references), 7)
            self.assertEqual(len(self.parser.isa.contacts), 3)
            self.assertEqual(len(self.parser.isa.publications), 1)
            self.assertEqual(len(self.parser.isa.comments), 2)
            self.assertEqual(len(self.parser.isa.studies), 2)

            self.assertEqual(
                len(self.parser.isa.studies[0].design_descriptors), 1)
            self.assertEqual(len(self.parser.isa.studies[0].publications), 1)
            self.assertEqual(len(self.parser.isa.studies[0].contacts), 3)
            self.assertEqual(len(self.parser.isa.studies[0].factors), 2)
            self.assertEqual(len(self.parser.isa.studies[0].assays), 3)
            self.assertEqual(len(self.parser.isa.studies[0].protocols), 7)

            self.assertEqual(len(self.parser.isa.studies[0].sources), 18)
            self.assertEqual(len(self.parser.isa.studies[0].samples), 164)
            self.assertEqual(len(self.parser.isa.studies[0].process_sequence), 18)

            self.assertEqual(
                len(self.parser.isa.studies[0].assays[0].samples), 8)
            self.assertEqual(
                len(self.parser.isa.studies[0].assays[0].data_files), 7)
            self.assertEqual(
                len(self.parser.isa.studies[0].assays[0].other_material), 19)
            self.assertEqual(
                len(self.parser.isa.studies[0].assays[0].process_sequence), 16)
            self.assertEqual(
                len(self.parser.isa.studies[0].assays[1].samples), 92)
            self.assertEqual(
                len(self.parser.isa.studies[0].assays[1].data_files), 111)
            self.assertEqual(
                len(self.parser.isa.studies[0].assays[1].other_material), 92)
            self.assertEqual(
                len(self.parser.isa.studies[0].assays[1].process_sequence), 92)

            self.assertEqual(
                len(self.parser.isa.studies[0].assays[2].samples), 48)
            self.assertEqual(
                len(self.parser.isa.studies[0].assays[2].data_files), 49)
            self.assertEqual(
                len(self.parser.isa.studies[0].assays[2].other_material), 96)
            self.assertEqual(
                len(self.parser.isa.studies[0].assays[2].process_sequence), 144)

            self.assertEqual(
                len(self.parser.isa.studies[1].design_descriptors), 1)
            self.assertEqual(len(self.parser.isa.studies[1].publications), 1)
            self.assertEqual(len(self.parser.isa.studies[1].contacts), 3)
            self.assertEqual(len(self.parser.isa.studies[1].factors), 3)
            self.assertEqual(len(self.parser.isa.studies[1].assays), 1)
            self.assertEqual(len(self.parser.isa.studies[1].protocols), 4)

            self.assertEqual(len(self.parser.isa.studies[1].sources), 1)
            self.assertEqual(len(self.parser.isa.studies[1].samples), 2)
            self.assertEqual(len(self.parser.isa.studies[1].process_sequence), 1)

            self.assertEqual(
                len(self.parser.isa.studies[1].assays[-1].samples), 2)
            self.assertEqual(
                len(self.parser.isa.studies[1].assays[-1].data_files), 15)
            self.assertEqual(
                len(self.parser.isa.studies[1].assays[-1].other_material), 28)
            self.assertEqual(
                len(self.parser.isa.studies[1].assays[-1].process_sequence), 30)
