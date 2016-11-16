# coding: utf-8
import unittest
import os
import sys
import shutil
import tempfile
import functools
import six

from isatools import isatab
from isatools.model.v1 import *
from tests import utils

# This will remove the "'U' flag is deprecated" DeprecationWarning in Python3
open = functools.partial(open, mode='r') if six.PY3 else functools.partial(open, mode='rbU')

#  Manually testing object model to write to isatab, study file-out only to check if model and writer function correctly
#  Currently only tests source-split and sample pooling, at study level


class TestIsaTab(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._tab_data_dir = utils.TAB_DATA_DIR

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab_bad_i_file_name(self):
        with self.assertRaises(NameError):
            isatab.dump(Investigation(), self._tmp_dir, i_file_name='investigation.txt')

    def test_isatab_dump_source_sample_split(self):
        i = Investigation()
        uberon = OntologySource(name='UBERON',
                                description="Uber Anatomy Ontology",
                                version='216',
                                file='http://data.bioontology.org/ontologies/UBERON')
        ncbitaxon = OntologySource(name='NCBITAXON',
                                   description="National Center for Biotechnology Information (NCBI) Organismal Classification",
                                   version='2',
                                   file='http://data.bioontology.org/ontologies/NCBITAXON')
        i.ontology_source_references.append(uberon)
        i.ontology_source_references.append(ncbitaxon)

        s = Study(filename='s_pool.txt')

        sample_collection_protocol = Protocol(
            name='sample collection',
            protocol_type=OntologyAnnotation(term='sample collection')
        )
        s.protocols.append(sample_collection_protocol)

        reference_descriptor_category = OntologyAnnotation(term='reference descriptor')
        material_type_category = OntologyAnnotation(term='material type')
        organism_category = OntologyAnnotation(term='organism')

        source1 = Source(name='source1')
        source1.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(term='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        sample1 = Sample(name='sample1')
        organism_part = OntologyAnnotation(term='organism part')
        sample1.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            term='liver',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0002107',
        )))

        sample2 = Sample(name='sample2')
        sample2.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            term='heart',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000948',
        )))

        sample3 = Sample(name='sample3')
        sample3.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            term='blood',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000178',
        )))

        sample4 = Sample(name='sample4')
        sample4.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            term='blood',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0000178',
        )))

        sample_collection_process = Process(executes_protocol=sample_collection_protocol)

        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1, sample2, sample3, sample4]
        s.process_sequence = [sample_collection_process]
        # from isatools.model.v1 import _build_assay_graph
        # s.graph = _build_assay_graph(s.process_sequence)
        i.studies = [s]
        isatab.dump(i, self._tmp_dir)

        with open(os.path.join(self._tab_data_dir, 'TEST-ISA-source-split','s_TEST-Template1-Splitting.txt')) as src_file:
            with open(os.path.join(self._tmp_dir, 's_pool.txt')) as dumped_file:
                self.assertTrue(utils.assert_tab_content_equal(src_file, dumped_file))
        # self.assertTrue(assert_tab_content_equal(open(os.path.join(self._tmp_dir, 's_pool.txt')),
        #                                          open(os.path.join(self._tab_data_dir, 'TEST-ISA-source-split',
        #                                                            's_TEST-Template1-Splitting.txt'))))

    def test_isatab_dump_source_sample_pool(self):
        i = Investigation()
        uberon = OntologySource(name='UBERON')
        ncbitaxon = OntologySource(name='NCBITAXON')
        i.ontology_source_references.append(uberon)
        i.ontology_source_references.append(ncbitaxon)

        s = Study(filename='s_pool.txt')
        sample_collection_protocol = Protocol(
            name='sample collection',
            protocol_type=OntologyAnnotation(term='sample collection')
        )
        s.protocols.append(sample_collection_protocol)

        reference_descriptor_category = OntologyAnnotation(term='reference descriptor')
        material_type_category = OntologyAnnotation(term='material type')
        organism_category = OntologyAnnotation(term='organism')

        source1 = Source(name='source1')
        source1.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(term='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source2 = Source(name='source2')
        source2.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(term='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source3 = Source(name='source3')
        source3.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(term='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        source4 = Source(name='source4')
        source4.characteristics = [
            Characteristic(category=reference_descriptor_category, value='not applicable'),
            Characteristic(category=material_type_category, value='specimen'),
            Characteristic(category=organism_category,
                           value=OntologyAnnotation(term='Human', term_source=ncbitaxon,
                                                    term_accession='http://purl.bioontology.org/ontology/STY/T016')),
        ]

        sample1 = Sample(name='sample1')
        organism_part = OntologyAnnotation(term='organism part')
        sample1.characteristics.append(Characteristic(category=organism_part, value=OntologyAnnotation(
            term='liver',
            term_source=uberon,
            term_accession='http://purl.obolibrary.org/obo/UBERON_0002107',
        )))

        sample_collection_process = Process(executes_protocol=sample_collection_protocol)

        sample_collection_process.inputs = [source1, source2, source3, source4]
        sample_collection_process.outputs = [sample1]
        s.process_sequence = [sample_collection_process]
        # from isatools.model.v1 import _build_assay_graph
        # s.graph = _build_assay_graph(s.process_sequence)
        i.studies = [s]
        isatab.dump(i, self._tmp_dir)

        with open(os.path.join(self._tmp_dir, 's_pool.txt')) as dumped_file:
            with open(os.path.join(self._tab_data_dir, 'TEST-ISA-sample-pool',\
                                            's_TEST-Template3-Splitting.txt')) as template_file:
                self.assertTrue(utils.assert_tab_content_equal(dumped_file, template_file))
                self.assertIsInstance(isatab.dumps(i), six.text_type)

    def test_batch_create_materials(self):
        source = Source(name='source_material')
        prototype_sample = Sample(name='sample_material', derives_from=source)
        batch = batch_create_materials(prototype_sample, n=3)
        self.assertEqual(len(batch), 3)
        for material in batch:
            self.assertIsInstance(material, Sample)
            self.assertEqual(material.derives_from, source)
        self.assertSetEqual({m.name for m in batch}, {'sample_material-0', 'sample_material-1',
                                                           'sample_material-2'})

