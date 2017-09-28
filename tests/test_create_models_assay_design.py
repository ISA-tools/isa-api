"""Tests on Assay planning model objects in isatools.create.models"""
import unittest

from isatools.create.models import AssayType, AssayTopologyModifiers
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
        self.assertEqual('AssayType(measurement_type=isatools.model.OntologyAnnotation('
                         'term="{0}", term_source=None, term_accession="", '
                         'comments=[]), '
                         'technology_type=isatools.model.OntologyAnnotation(term="{1}", '
                         'term_source=None, term_accession="", comments=[]), '
                         'topology_modifiers=None)'
                         .format(MEASUREMENT_TYPE_TRANSCRIPTION_PROFILING,
                                 TECHNOLOGY_TYPE_DNA_MICROARRAY),
                         repr(self.assay_type))

        self.assertEqual('AssayType(measurement_type=isatools.model.OntologyAnnotation('
                         'term="{0}", term_source=None, term_accession="", '
                         'comments=[]), technology_type=isatools.model.OntologyAnnotation('
                         'term="{1}", term_source=None, term_accession="", '
                         'comments=[]), topology_modifiers=None)'.format(
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
        self.assertNotEqual(hash(expected_other_assay_type), hash(self.assay_type))
        self.assertNotEqual(expected_other_assay_type, self.assay_type_with_oa)
        self.assertNotEqual(hash(expected_other_assay_type),
                            hash(self.assay_type_with_oa))


class AssayTopologyModifiersTest(unittest.TestCase):

    def setUp(self):
        self.assay_topology_modifiers_default = AssayTopologyModifiers()
        self.assay_topology_modifiers = AssayTopologyModifiers(
            distinct_libraries=1,
            array_designs={'design1', 'design2'},
            injection_modes={'GC', 'LC'},
            acquisition_modes={'mode1', 'mode2'},
            pulse_sequences={'TOCSY', 'NOCSY'},
            technical_replicates=6,
            instruments={'Agilent QTOF'},
            chromatography_instruments={'Agilent 12345F'}
        )

    def test_repr(self):
        self.assertEqual('AssayTopologyModifiers('
                         'distinct_libraries=0, '
                         'array_designs=[], '
                         'injection_modes=[], '
                         'acquisition_modes=[], '
                         'pulse_sequences=[], '
                         'technical_replicates=1, '
                         'instruments=[], '
                         'chromatography_instruments=[])',
                         repr(self.assay_topology_modifiers_default))
        self.assertEqual("AssayTopologyModifiers("
                         "distinct_libraries=1, "
                         "array_designs=['design1', 'design2'], "
                         "injection_modes=['GC', 'LC'], "
                         "acquisition_modes=['mode1', 'mode2'], "
                         "pulse_sequences=['NOCSY', 'TOCSY'], "
                         "technical_replicates=6, "
                         "instruments=['Agilent QTOF'], "
                         "chromatography_instruments=['Agilent 12345F'])",
                         repr(self.assay_topology_modifiers))

    def test_eq(self):
        expected_assay_topology_modifiers_default = AssayTopologyModifiers()
        expected_assay_topology_modifiers = AssayTopologyModifiers(
            distinct_libraries=1,
            array_designs={'design1', 'design2'},
            injection_modes={'GC', 'LC'},
            acquisition_modes={'mode1', 'mode2'},
            pulse_sequences={'TOCSY', 'NOCSY'},
            technical_replicates=6,
            instruments={'Agilent QTOF'},
            chromatography_instruments={'Agilent 12345F'}
        )
        self.assertEqual(expected_assay_topology_modifiers_default,
                         self.assay_topology_modifiers_default)
        self.assertEqual(hash(expected_assay_topology_modifiers),
                         hash(self.assay_topology_modifiers))

    def test_ne(self):
        expected_assay_topology_modifiers_default = AssayTopologyModifiers()
        expected_assay_topology_modifiers = AssayTopologyModifiers(
            distinct_libraries=1,
            array_designs={'design1', 'design2'},
            injection_modes={'GC', 'LC'},
            acquisition_modes={'mode1', 'mode2'},
            pulse_sequences={'TOCSY', 'NOCSY'},
            technical_replicates=6,
            instruments={'Agilent QTOF'},
            chromatography_instruments={'Agilent 12345F'}
        )
        self.assertNotEqual(expected_assay_topology_modifiers,
                            self.assay_topology_modifiers_default)
        self.assertNotEqual(hash(expected_assay_topology_modifiers_default),
                            hash(self.assay_topology_modifiers))
