"""Tests on Assay planning model objects in isatools.create.models"""
import unittest

from isatools.create.models import *
from isatools.model import OntologyAnnotation

MEASUREMENT_TYPE_TRANSCRIPTION_PROFILING = 'transcription profiling'
TECHNOLOGY_TYPE_DNA_MICROARRAY = 'DNA microarray'
TECHNOLOGY_TYPE_DNA_SEQUENCING = 'nucleic acid sequencing'


class AssayTypeTest(unittest.TestCase):

    def setUp(self):
        self.assay_type = AssayType(
            measurement_type=MEASUREMENT_TYPE_TRANSCRIPTION_PROFILING,
            technology_type=TECHNOLOGY_TYPE_DNA_MICROARRAY
        )
        self.assay_type_with_oa = AssayType(
            measurement_type=OntologyAnnotation(
                term=MEASUREMENT_TYPE_TRANSCRIPTION_PROFILING),
            technology_type=OntologyAnnotation(
                term=TECHNOLOGY_TYPE_DNA_MICROARRAY)
        )

    def test_repr(self):
        self.assertEqual("AssayType(measurement_type="
                         "isatools.model.OntologyAnnotation("
                         "term='{0}', term_source=None, term_accession='', "
                         "comments=[]), "
                         "technology_type=i"
                         "satools.model.OntologyAnnotation(term='{1}', "
                         "term_source=None, term_accession='', comments=[]), "
                         "topology_modifiers=None)"
                         .format(MEASUREMENT_TYPE_TRANSCRIPTION_PROFILING,
                                 TECHNOLOGY_TYPE_DNA_MICROARRAY),
                         repr(self.assay_type))

        self.assertEqual("AssayType(measurement_type="
                         "isatools.model.OntologyAnnotation("
                         "term='{0}', term_source=None, term_accession='', "
                         "comments=[]), technology_type="
                         "isatools.model.OntologyAnnotation("
                         "term='{1}', term_source=None, term_accession='', "
                         "comments=[]), topology_modifiers=None)".format(
                          MEASUREMENT_TYPE_TRANSCRIPTION_PROFILING,
                          TECHNOLOGY_TYPE_DNA_MICROARRAY), repr(
                          self.assay_type_with_oa))

    def test_eq(self):
        expected_assay_type = AssayType(
            measurement_type=MEASUREMENT_TYPE_TRANSCRIPTION_PROFILING,
            technology_type=TECHNOLOGY_TYPE_DNA_MICROARRAY
        )
        self.assertEqual(expected_assay_type, self.assay_type)
        self.assertEqual(hash(expected_assay_type), hash(self.assay_type))
        self.assertEqual(expected_assay_type, self.assay_type_with_oa)
        self.assertEqual(hash(expected_assay_type),
                         hash(self.assay_type_with_oa))

    def test_ne(self):
        expected_other_assay_type = AssayType(
            measurement_type=MEASUREMENT_TYPE_TRANSCRIPTION_PROFILING,
            technology_type=TECHNOLOGY_TYPE_DNA_SEQUENCING
        )
        self.assertNotEqual(expected_other_assay_type, self.assay_type)
        self.assertNotEqual(
            hash(expected_other_assay_type), hash(self.assay_type))
        self.assertNotEqual(expected_other_assay_type, self.assay_type_with_oa)
        self.assertNotEqual(hash(expected_other_assay_type),
                            hash(self.assay_type_with_oa))


class AssayTopologyModifiersTest(unittest.TestCase):

    def setUp(self):
        self.dna_micro_assay_topology_modifiers_default = \
            DNAMicroAssayTopologyModifiers()
        self.dna_micro_assay_topology_modifiers = \
            DNAMicroAssayTopologyModifiers(
                array_designs={'design1', 'design2'},
                technical_replicates=6,
            )
        self.dna_seq_assay_topology_modifiers_default = \
            DNASeqAssayTopologyModifiers()
        self.dna_seq_assay_topology_modifiers = DNASeqAssayTopologyModifiers(
            distinct_libraries=1,
            technical_replicates=6,
            instruments={'Agilent QTOF'}
        )
        self.ms_assay_topology_modifiers_default = MSAssayTopologyModifiers()
        self.ms_assay_topology_modifiers = MSAssayTopologyModifiers(
            injection_modes={'GC', 'LC'},
            acquisition_modes={'mode1', 'mode2'},
            technical_replicates=6,
            instruments={'Agilent QTOF'},
            chromatography_instruments={'Agilent 12345F'}
        )
        self.nmr_assay_topology_modifiers_default = NMRAssayTopologyModifiers()
        self.nmr_assay_topology_modifiers = NMRAssayTopologyModifiers(
            injection_modes={'GC', 'LC'},
            acquisition_modes={'mode1', 'mode2'},
            pulse_sequences={'TOCSY', 'NOCSY'},
            technical_replicates=6,
            instruments={'Agilent QTOF'}
        )

    def test_dna_micro_repr(self):
        self.assertEqual('DNAMicroAssayTopologyModifiers('
                         'technical_replicates=1, '
                         'array_designs=[])',
                         repr(self.dna_micro_assay_topology_modifiers_default))
        self.assertEqual("DNAMicroAssayTopologyModifiers("
                         "technical_replicates=6, "
                         "array_designs=['design1', 'design2'])",
                         repr(self.dna_micro_assay_topology_modifiers))

    def test_dna_micro_eq(self):
        expected_assay_topology_modifiers_default = \
            DNAMicroAssayTopologyModifiers()
        expected_assay_topology_modifiers = DNAMicroAssayTopologyModifiers(
            array_designs={'design1', 'design2'},
            technical_replicates=6
        )
        self.assertEqual(expected_assay_topology_modifiers_default,
                         self.dna_micro_assay_topology_modifiers_default)
        self.assertEqual(hash(expected_assay_topology_modifiers),
                         hash(self.dna_micro_assay_topology_modifiers))

    def test_dna_micro_ne(self):
        expected_assay_topology_modifiers_default = \
            DNAMicroAssayTopologyModifiers()
        expected_assay_topology_modifiers = DNAMicroAssayTopologyModifiers(
            array_designs={'design1', 'design2'},
            technical_replicates=6
        )
        self.assertNotEqual(expected_assay_topology_modifiers,
                            self.dna_micro_assay_topology_modifiers_default)
        self.assertNotEqual(hash(expected_assay_topology_modifiers_default),
                            hash(self.dna_micro_assay_topology_modifiers))

    def test_dna_seq_repr(self):
        self.assertEqual('DNASeqAssayTopologyModifiers('
                         'technical_replicates=1, '
                         'instruments=[], '
                         'distinct_libraries=0)',
                         repr(self.dna_seq_assay_topology_modifiers_default))
        self.assertEqual("DNASeqAssayTopologyModifiers("
                         "technical_replicates=6, "
                         "instruments=['Agilent QTOF'], "
                         "distinct_libraries=1)",
                         repr(self.dna_seq_assay_topology_modifiers))

    def test_dna_seq_eq(self):
        expected_assay_topology_modifiers_default = \
            DNASeqAssayTopologyModifiers()
        expected_assay_topology_modifiers = DNASeqAssayTopologyModifiers(
            distinct_libraries=1,
            technical_replicates=6,
            instruments={'Agilent QTOF'}
        )
        self.assertEqual(expected_assay_topology_modifiers_default,
                         self.dna_seq_assay_topology_modifiers_default)
        self.assertEqual(hash(expected_assay_topology_modifiers),
                         hash(self.dna_seq_assay_topology_modifiers))

    def test_dna_seq_ne(self):
        expected_assay_topology_modifiers_default = \
            DNASeqAssayTopologyModifiers()
        expected_assay_topology_modifiers = DNASeqAssayTopologyModifiers(
            distinct_libraries=1,
            technical_replicates=6,
            instruments = {'Agilent QTOF'}
        )
        self.assertNotEqual(expected_assay_topology_modifiers,
                            self.dna_seq_assay_topology_modifiers_default)
        self.assertNotEqual(hash(expected_assay_topology_modifiers_default),
                            hash(self.dna_seq_assay_topology_modifiers))
        
    def test_ms_repr(self):
        self.assertEqual('MSAssayTopologyModifiers('
                         'technical_replicates=1, '
                         'instruments=[], '
                         'injection_modes=[], '
                         'acquisition_modes=[], '
                         'chromatography_instruments=[])',
                         repr(self.ms_assay_topology_modifiers_default))
        self.assertEqual("MSAssayTopologyModifiers("
                         "technical_replicates=6, "
                         "instruments=['Agilent QTOF'], "
                         "injection_modes=['GC', 'LC'], "
                         "acquisition_modes=['mode1', 'mode2'], "
                         "chromatography_instruments=['Agilent 12345F'])",
                         repr(self.ms_assay_topology_modifiers))

    def test_ms_eq(self):
        expected_assay_topology_modifiers_default = \
            MSAssayTopologyModifiers()
        expected_assay_topology_modifiers = MSAssayTopologyModifiers(
            technical_replicates=6,
            instruments={'Agilent QTOF'},
            injection_modes={'GC', 'LC'}
        )
        self.assertEqual(expected_assay_topology_modifiers_default,
                         self.ms_assay_topology_modifiers_default)
        self.assertEqual(hash(expected_assay_topology_modifiers),
                         hash(self.ms_assay_topology_modifiers))

    def test_ms_ne(self):
        expected_assay_topology_modifiers_default = MSAssayTopologyModifiers()
        expected_assay_topology_modifiers = MSAssayTopologyModifiers(
            technical_replicates=6,
            instruments={'Agilent QTOF'},
            injection_modes={'GC', 'LC'}
        )
        self.assertNotEqual(expected_assay_topology_modifiers,
                            self.ms_assay_topology_modifiers_default)
        self.assertNotEqual(hash(expected_assay_topology_modifiers_default),
                            hash(self.ms_assay_topology_modifiers))
        
    def test_nmr_repr(self):
        self.assertEqual('NMRAssayTopologyModifiers('
                         'acquisition_modes=[], '
                         'pulse_sequences=[], '
                         'technical_replicates=1, '
                         'instruments=[], '
                         'injection_modes=[])',
                         repr(self.nmr_assay_topology_modifiers_default))
        self.assertEqual("NMRAssayTopologyModifiers("
                         "acquisition_modes=['mode1', 'mode2'], "
                         "pulse_sequences=['NOCSY', 'TOCSY'], "
                         "technical_replicates=6, "
                         "instruments=['Agilent QTOF'], "
                         "injection_modes=['mode1', 'mode2'])",
                         repr(self.nmr_assay_topology_modifiers))

    def test_nmr_eq(self):
        expected_assay_topology_modifiers_default = \
            NMRAssayTopologyModifiers()
        expected_assay_topology_modifiers = NMRAssayTopologyModifiers(
            injection_modes={'GC', 'LC'},
            acquisition_modes={'mode1', 'mode2'},
            pulse_sequences={'TOCSY', 'NOCSY'},
            technical_replicates=6,
            instruments={'Agilent QTOF'}
        )
        self.assertEqual(expected_assay_topology_modifiers_default,
                         self.nmr_assay_topology_modifiers_default)
        self.assertEqual(hash(expected_assay_topology_modifiers),
                         hash(self.nmr_assay_topology_modifiers))

    def test_nmr_ne(self):
        expected_assay_topology_modifiers_default = NMRAssayTopologyModifiers()
        expected_assay_topology_modifiers = NMRAssayTopologyModifiers(
            injection_modes={'GC', 'LC'},
            acquisition_modes={'mode1', 'mode2'},
            pulse_sequences={'TOCSY', 'NOCSY'},
            technical_replicates=6,
            instruments={'Agilent QTOF'}
        )
        self.assertNotEqual(expected_assay_topology_modifiers,
                            self.nmr_assay_topology_modifiers_default)
        self.assertNotEqual(hash(expected_assay_topology_modifiers_default),
                            hash(self.nmr_assay_topology_modifiers))