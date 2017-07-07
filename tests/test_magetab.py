import unittest
from tests.utils import MAGETAB_DATA_DIR
import os
from isatools.magetab import MageTabParser
from isatools.model.v1 import Investigation

""" Unit tests for MAGE-TAB package - only for sanity check, not comprehensive testing """


class WhenCreatingNewParser(unittest.TestCase):

    def setUp(self):
        self.parser = MageTabParser()

    def tearDown(self):
        pass

    def test_ISA_should_have_empty_identifier(self):
        self.assertTrue(self.parser.ISA.identifier == '')

    def test_ISA_should_have_one_study(self):
        self.assertTrue(len(self.parser.ISA.studies) == 1)


class WhenParsingIDF(unittest.TestCase):

    def setUp(self):
        self.parser = MageTabParser()
        self.test_path = os.path.join(MAGETAB_DATA_DIR, 'E-MEXP-31.idf.txt')

    def test_should_parse_idf_without_error(self):
        self.parser.parse_idf(self.test_path)

    def test_should_create_ISA(self):
        self.parser.parse_idf(self.test_path)
        self.assertIsInstance(self.parser.ISA, Investigation)

    def test_should_return_ISA(self):
        self.assertIsInstance(self.parser.parse_idf(self.test_path), Investigation)


class WhenParsedIDF(unittest.TestCase):
    """ Test case using E-MEXP-31.idf.txt """
    def setUp(self):
        self.parser = MageTabParser()
        self.test_path = os.path.join(MAGETAB_DATA_DIR, 'E-MEXP-31.idf.txt')
        self.parser.parse_idf(self.test_path)

    def test_should_load_five_ontology_sources(self):
        self.assertEqual(len(self.parser.ISA.ontology_source_references), 5)

    def test_should_load_one_study(self):
        self.assertEqual(len(self.parser.ISA.studies), 1)

    def test_should_load_three_study_designs(self):
        self.assertEqual(len(self.parser.ISA.studies[-1].design_descriptors), 3)

    def test_should_load_one_study_factor(self):
        self.assertEqual(len(self.parser.ISA.studies[-1].factors), 1)

    def test_should_load_one_person(self):
        self.assertEqual(len(self.parser.ISA.studies[-1].contacts), 1)

    def test_should_load_one_publication(self):
        self.assertEqual(len(self.parser.ISA.studies[-1].publications), 1)

    def test_should_load_six_protocols(self):
        self.assertEqual(len(self.parser.ISA.studies[-1].protocols), 6)

    def test_should_load_one_assay(self):
        self.assertEqual(len(self.parser.ISA.studies[-1].assays), 1)

    def test_should_load_assay_with_transcription_micro(self):
        self.assertEqual(self.parser.ISA.studies[-1].assays[-1].measurement_type.term, "transcription profiling")
        self.assertEqual(self.parser.ISA.studies[-1].assays[-1].technology_type.term, "DNA microarray")
