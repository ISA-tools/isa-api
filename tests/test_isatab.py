# coding: utf-8
import unittest
import os
import sys
import shutil
from tests.utils import assert_tab_content_equal
from isatools.model.v1 import *
from tests import utils
import tempfile
from isatools import isatab

from functools import partial
open = partial(open, mode='rU') if sys.version_info[0]==2 else partial(open, mode='r')

#  Manually testing object model to write to isatab, study file-out only to check if model and writer function correctly
#  Currently only tests source-split and sample pooling, at study level


class TestIsaTab(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab_dump_source_sample_split(self):
        i = Investigation()
        uberon = OntologySourceReference(name='UBERON',
                                         description="Uber Anatomy Ontology",
                                         version='216',
                                         file='http://data.bioontology.org/ontologies/UBERON')
        ncbitaxon = OntologySourceReference(name='NCBITAXON',
                                            description="National Center for Biotechnology Information (NCBI) Organismal Classification",
                                            version='2',
                                            file='http://data.bioontology.org/ontologies/NCBITAXON')
        i.ontology_source_references.append(uberon)
        i.ontology_source_references.append(ncbitaxon)

        s = Study(filename='s_pool.txt')

        sample_collection_protocol = Protocol(
            name='sample collection',
            protocol_type=OntologyAnnotation(name='sample collection')
        )
        s.protocols.append(sample_collection_protocol)

        reference_descriptor_category = OntologyAnnotation(name='reference descriptor')
        material_type_category = OntologyAnnotation(name='material type')
        organism_category = OntologyAnnotation(name='organism')

        source1 = Source(name='source1')
        source1.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(name='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        sample1 = Sample(name='sample1')
        organism_part = OntologyAnnotation(name='organism part')
        sample1.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='liver',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0002107',
        )))

        sample2 = Sample(name='sample2')
        sample2.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='heart',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000948',
        )))

        sample3 = Sample(name='sample3')
        sample3.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='blood',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000178',
        )))

        sample4 = Sample(name='sample4')
        sample4.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='blood',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000178',
        )))

        sample_collection_process = Process(executes_protocol=sample_collection_protocol)

        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1, sample2, sample3, sample4]
        s.process_sequence = [sample_collection_process]
        from isatools.model.v1 import _build_assay_graph
        s.graph = _build_assay_graph(s.process_sequence)
        i.studies = [s]
        isatab.dump(i, self._tmp_dir)
        self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 's_pool.txt')),
                                                 open(os.path.join(self._tab_data_dir, 'TEST-ISA-source-split',
                                                                   's_TEST-Template1-Splitting.txt'))))

    def test_isatab_dump_source_sample_pool(self):
        i = Investigation()
        uberon = OntologySourceReference(name='UBERON')
        ncbitaxon = OntologySourceReference(name='NCBITAXON')
        i.ontology_source_references.append(uberon)
        i.ontology_source_references.append(ncbitaxon)

        s = Study(filename='s_pool.txt')
        sample_collection_protocol = Protocol(
            name='sample collection',
            protocol_type=OntologyAnnotation(name='sample collection')
        )
        s.protocols.append(sample_collection_protocol)

        reference_descriptor_category = OntologyAnnotation(name='reference descriptor')
        material_type_category = OntologyAnnotation(name='material type')
        organism_category = OntologyAnnotation(name='organism')

        source1 = Source(name='source1')
        source1.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(name='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source2 = Source(name='source2')
        source2.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(name='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source3 = Source(name='source3')
        source3.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(name='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source4 = Source(name='source4')
        source4.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(name='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        sample1 = Sample(name='sample1')
        organism_part = OntologyAnnotation(name='organism part')
        sample1.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            name='liver',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0002107',
        )))

        sample_collection_process = Process(executes_protocol=sample_collection_protocol)

        sample_collection_process.inputs = [source1, source2, source3, source4]
        sample_collection_process.outputs = [sample1]
        s.process_sequence = [sample_collection_process]
        from isatools.model.v1 import _build_assay_graph
        s.graph = _build_assay_graph(s.process_sequence)
        i.studies = [s]
        isatab.dump(i, self._tmp_dir)
        self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 's_pool.txt')),
                                                 open(os.path.join(self._tab_data_dir, 'TEST-ISA-sample-pool',
                                                                   's_TEST-Template3-Splitting.txt'))))

    def test_isatab_load_utf8_unix_investigation(self):
        """Load investigation encoded in utf-8 with Unix endlines"""
        test_case = "TEST-ISA-utf8-unix"
        with open(os.path.join(self._tab_data_dir, test_case, "i_investigation.txt")) as i:
            try:
                isatab.load2(i)
            except BaseException as e:
                self.fail("Error found when loading ISA TAB: {}".format(e))

    def test_isatab_load_utf8_mac_investigation(self):
        """Load investigation encoded in utf-8 with Mac endlines"""
        test_case = "TEST-ISA-utf8-mac"
        with open(os.path.join(self._tab_data_dir, test_case, "i_investigation.txt")) as i:
            try:
                isatab.load2(i)
            except BaseException as e:
                self.fail("Error found when loading ISA TAB: {}".format(e))

    def test_isatab_load_utf8_dos_investigation(self):
        """Load investigation encoded in utf-8 with DOS/Windows endlines"""
        test_case = "TEST-ISA-utf8-dos"
        with open(os.path.join(self._tab_data_dir, test_case, "i_investigation.txt")) as i:
            try:
                isatab.load2(i)
            except BaseException as e:
                self.fail("Error found when loading ISA TAB: {}".format(e))

    def test_isatab_unexisting_directory(self):
        #try:
        with self.assertRaises(IOError):
            isatab.validate("/unexisting/directory", "/fake/config/dir")

        with self.assertRaises(SystemError):
            with open(os.path.join(self._tab_data_dir, "MTBLS1", "i_investigation.txt")) as i:
                isatab.validate2(i, "/dir/without/config")

