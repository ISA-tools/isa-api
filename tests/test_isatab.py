import unittest
import os
import shutil
from tests.utils import assert_tab_content_equal
from isatools.model.v1 import *
from tests import utils
import tempfile
from isatools import isatab
from isatools.isatab import ProcessSequenceFactory
from io import StringIO
import pandas as pd


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestIsaMerge(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_merge_bii_s_1_with_a_proteome(self):
        isatab.merge_study_with_assay_tables(os.path.join(self._tab_data_dir, 'BII-I-1', 's_BII-S-1.txt'),
                                             os.path.join(self._tab_data_dir, 'BII-I-1', 'a_proteome.txt'),
                                             os.path.join(self._tmp_dir, 'merged.txt'))
        merged_DF = isatab.read_tfile(os.path.join(self._tmp_dir, 'merged.txt'))
        # num rows expected is max of input DFs
        self.assertEqual(merged_DF.shape[0], 18)
        # num columns expected is sum of input DFs, minus index column
        self.assertEqual(merged_DF.shape[1], 43)

    def test_merge_bii_s_1_with_a_metabolome(self):
        isatab.merge_study_with_assay_tables(os.path.join(self._tab_data_dir, 'BII-I-1', 's_BII-S-1.txt'),
                                             os.path.join(self._tab_data_dir, 'BII-I-1', 'a_metabolome.txt'),
                                             os.path.join(self._tmp_dir, 'merged.txt'))
        merged_DF = isatab.read_tfile(os.path.join(self._tmp_dir, 'merged.txt'))
        self.assertEqual(merged_DF.shape[0], 111)
        self.assertEqual(merged_DF.shape[1], 41)

    def test_merge_bii_s_1_with_a_transcriptome(self):
        isatab.merge_study_with_assay_tables(os.path.join(self._tab_data_dir, 'BII-I-1', 's_BII-S-1.txt'),
                                             os.path.join(self._tab_data_dir, 'BII-I-1', 'a_transcriptome.txt'),
                                             os.path.join(self._tmp_dir, 'merged.txt'))
        merged_DF = isatab.read_tfile(os.path.join(self._tmp_dir, 'merged.txt'))
        self.assertEqual(merged_DF.shape[0], 48)
        self.assertEqual(merged_DF.shape[1], 40)

    def test_merge_bii_s_2_with_a_microarray(self):
        isatab.merge_study_with_assay_tables(os.path.join(self._tab_data_dir, 'BII-I-1', 's_BII-S-2.txt'),
                                             os.path.join(self._tab_data_dir, 'BII-I-1', 'a_microarray.txt'),
                                             os.path.join(self._tmp_dir, 'merged.txt'))
        merged_DF = isatab.read_tfile(os.path.join(self._tmp_dir, 'merged.txt'))
        self.assertEqual(merged_DF.shape[0], 14)
        self.assertEqual(merged_DF.shape[1], 43)

    def test_merge_bii_s_1_with_a_microarray(self):
        isatab.merge_study_with_assay_tables(os.path.join(self._tab_data_dir, 'BII-I-1', 's_BII-S-1.txt'),
                                             os.path.join(self._tab_data_dir, 'BII-I-1', 'a_microarray.txt'),
                                             os.path.join(self._tmp_dir, 'merged.txt'))
        merged_DF = isatab.read_tfile(os.path.join(self._tmp_dir, 'merged.txt'))
        self.assertEqual(merged_DF.shape[0], 0)  # tests no matching samples
        self.assertEqual(merged_DF.shape[1], 47)  # still prints out joined header though


class TestIsaTabDump(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
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
        i.studies = [s]
        isatab.dump(i, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 's_pool.txt')) as actual_file, \
                open(os.path.join(self._tab_data_dir, 'TEST-ISA-source-split',
                                  's_TEST-Template1-Splitting.txt')) as expected_file:
            self.assertTrue(assert_tab_content_equal(actual_file, expected_file))

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
        i.studies = [s]
        isatab.dump(i, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 's_pool.txt')) as actual_file, \
                open(os.path.join(self._tab_data_dir, 'TEST-ISA-sample-pool',
                                  's_TEST-Template3-Splitting.txt')) as expected_file:
            self.assertTrue(assert_tab_content_equal(actual_file, expected_file))
            self.assertIsInstance(isatab.dumps(i), str)

    def test_isatab_dump_source_sample_sample(self):
        # Validates issue fix for #191
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

        sample_collection_process2 = Process(executes_protocol=sample_collection_protocol)
        sample2 = Sample(name='sample2')

        sample_collection_process.inputs = [source1, source2, source3, source4]
        sample_collection_process.outputs = [sample1]
        sample_collection_process2.inputs = [sample1]
        sample_collection_process2.outputs = [sample2]
        s.process_sequence = [sample_collection_process, sample_collection_process2]
        i.studies = [s]
        isatab.dump(i, self._tmp_dir)
        with open(os.path.join(self._tmp_dir, 's_pool.txt')) as actual_file, \
                open(os.path.join(self._tab_data_dir, 'TEST-ISA-sample-pool-sample-chain',
                                  's_TEST-Template3-Splitting.txt')) as expected_file:
            self.assertTrue(assert_tab_content_equal(actual_file, expected_file))
            self.assertIsInstance(isatab.dumps(i), str)


class TestIsaTabLoad(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab_load_issue200(self):
        with open(os.path.join(self._tab_data_dir, 'issue200', 'i_Investigation.txt')) as fp:
            ISA = isatab.load(fp)
            self.assertEqual(len(ISA.studies[0].assays[0].materials['samples']), 7)
            self.assertEqual(len(ISA.studies[0].assays[0].materials['other_material']), 7)
            self.assertEqual(len(ISA.studies[0].assays[0].data_files), 2)
            self.assertEqual(len(ISA.studies[0].assays[0].process_sequence), 11)

    # def test_isatab_load_issue201(self):  # issue now not relevant due to changes in parser
    #     with open(os.path.join(self._tab_data_dir, 'sdata201411-isa1-parsererror', 'i_Investigation.txt')) as fp:
    #         try:
    #             self.assertRaises(isatab.load(fp, skip_load_tables=True), IOError)
    #         except Exception as ex:  # This now doesn't fail as section loader is now more resilient
    #             self.assertIsInstance(ex, IOError)
    #             self.assertIn("There was a problem parsing the investigation section:", str(ex))

    def test_isatab_load_sdata201414_isa1(self):
        with open(os.path.join(self._tab_data_dir, 'sdata201414-isa1', 'i_Investigation.txt')) as fp:
            ISA = isatab.load(fp)
            self.assertEqual(len(ISA.ontology_source_references), 5)  # 5 ontology sources in investigation
            self.assertListEqual([s.filename for s in ISA.studies], ['s_chambers.txt'])  # 1 study in i_investigation.txt
            self.assertEqual(len(ISA.studies[0].comments), 9)  # 9 comments in study
            self.assertEqual(len(ISA.studies[0].design_descriptors), 3)  # 3 design descriptors in study
            self.assertEqual(len(ISA.studies[0].publications), 0)  # 0 publications in study
            self.assertEqual(len(ISA.studies[0].factors), 2)  # 2 factors in study
            self.assertEqual(len(ISA.studies[0].protocols), 5)  # 5 protocols in study
            self.assertEqual(len(ISA.studies[0].contacts), 2)  # 2 contacts in study
            self.assertEqual(len(ISA.studies[0].contacts[0].comments), 5)  # 5 comments in contact
            self.assertEqual(len(ISA.studies[0].contacts[1].comments), 5)  # 5 comments in contact
            self.assertListEqual([a.filename for a in ISA.studies[0].assays], ['a_chambers.txt'])  # 1 assays in s_chambers.txt

    def test_isatab_load_bii_i_1(self):
        with open(os.path.join(self._tab_data_dir, 'BII-I-1', 'i_investigation.txt')) as fp:
            ISA = isatab.load(fp)

            self.assertListEqual([s.filename for s in ISA.studies], ['s_BII-S-1.txt', 's_BII-S-2.txt'])  # 2 studies in i_investigation.txt

            study_bii_s_1 = [s for s in ISA.studies if s.filename == 's_BII-S-1.txt'][0]

            self.assertEqual(len(study_bii_s_1.materials['sources']), 18)  # 18 sources in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_1.materials['samples']), 164)  # 164 study samples in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_1.process_sequence), 18)  # 18 study processes in s_BII-S-1.txt

            self.assertListEqual([a.filename for a in study_bii_s_1.assays], ['a_proteome.txt', 'a_metabolome.txt', 'a_transcriptome.txt'])  # 2 assays in s_BII-S-1.txt

            assay_proteome = [a for a in study_bii_s_1.assays if a.filename == 'a_proteome.txt'][0]

            self.assertEqual(len(assay_proteome.materials['samples']), 8)  # 8 assay samples in a_proteome.txt
            self.assertEqual(len(assay_proteome.materials['other_material']), 19)  # 19 other materials in a_proteome.txt

            self.assertEqual(len(assay_proteome.data_files), 7)  # 7 data files  in a_proteome.txt

            self.assertEqual(len(assay_proteome.process_sequence), 25)  # 25 processes in in a_proteome.txt

            assay_metabolome = [a for a in study_bii_s_1.assays if a.filename == 'a_metabolome.txt'][0]

            self.assertEqual(len(assay_metabolome.materials['samples']), 92)  # 92 assay samples in a_metabolome.txt
            self.assertEqual(len(assay_metabolome.materials['other_material']), 92)  # 92 other materials in a_metabolome.txt
            self.assertEqual(len(assay_metabolome.data_files), 111)  # 111 data files  in a_metabolome.txt
            self.assertEqual(len(assay_metabolome.process_sequence), 203)  # 203 processes in in a_metabolome.txt

            assay_transcriptome = [a for a in study_bii_s_1.assays if a.filename == 'a_transcriptome.txt'][0]

            self.assertEqual(len(assay_transcriptome.materials['samples']), 48)  # 48 assay samples in a_transcriptome.txt
            self.assertEqual(len(assay_transcriptome.materials['other_material']), 96)  # 96 other materials in a_transcriptome.txt
            self.assertEqual(len(assay_transcriptome.data_files), 49)  # 49 data files  in a_transcriptome.txt
            self.assertEqual(len(assay_transcriptome.process_sequence), 193)  # 193 processes in in a_transcriptome.txt

            study_bii_s_2 = [s for s in ISA.studies if s.filename == 's_BII-S-2.txt'][0]

            self.assertEqual(len(study_bii_s_2.materials['sources']), 1)  # 1 sources in s_BII-S-2.txt
            self.assertEqual(len(study_bii_s_2.materials['samples']), 2)  # 2 study samples in s_BII-S-2.txt
            self.assertEqual(len(study_bii_s_2.process_sequence), 1)  # 1 study processes in s_BII-S-2.txt

            self.assertEqual(len(study_bii_s_2.assays), 1)  # 1 assays in s_BII-S-2.txt
            self.assertListEqual([a.filename for a in study_bii_s_2.assays], ['a_microarray.txt'])  # 1 assays in s_BII-S-2.txt

            assay_microarray = [a for a in study_bii_s_2.assays if a.filename == 'a_microarray.txt'][0]

            self.assertEqual(len(assay_microarray.materials['samples']), 2)  # 2 assay samples in a_microarray.txt
            self.assertEqual(len(assay_microarray.materials['other_material']), 28)  # 28 other materials in a_microarray.txt
            self.assertEqual(len(assay_microarray.data_files), 15)  # 15 data files  in a_microarray.txt
            self.assertEqual(len(assay_microarray.process_sequence), 45)  # 45 processes in in a_microarray.txt

    def test_isatab_load_bii_s_3(self):
        with open(os.path.join(self._tab_data_dir, 'BII-S-3', 'i_gilbert.txt')) as fp:
            ISA = isatab.load(fp)

            self.assertListEqual([s.filename for s in ISA.studies], ['s_BII-S-3.txt'])  # 1 studies in i_gilbert.txt

            study_bii_s_3 = [s for s in ISA.studies if s.filename == 's_BII-S-3.txt'][0]

            self.assertEqual(len(study_bii_s_3.materials['sources']), 4)  # 4 sources in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_3.materials['samples']), 4)  # 4 study samples in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_3.process_sequence), 4)  # 4 study processes in s_BII-S-1.txt

            self.assertListEqual([a.filename for a in study_bii_s_3.assays], ['a_gilbert-assay-Gx.txt', 'a_gilbert-assay-Tx.txt'])  # 2 assays in s_BII-S-1.txt

            assay_gx = [a for a in study_bii_s_3.assays if a.filename == 'a_gilbert-assay-Gx.txt'][0]

            self.assertEqual(len(assay_gx.materials['samples']), 4)  # 4 assay samples in a_gilbert-assay-Gx.txt
            self.assertEqual(len(assay_gx.materials['other_material']), 4)  # 4 other materials in a_gilbert-assay-Gx.txt
            self.assertEqual(len(assay_gx.data_files), 6)  # 6 data files  in a_gilbert-assay-Gx.txt
            self.assertEqual(len(assay_gx.process_sequence), 18)  # 18 processes in in a_gilbert-assay-Gx.txt

            assay_tx = [a for a in study_bii_s_3.assays if a.filename == 'a_gilbert-assay-Tx.txt'][0]

            self.assertEqual(len(assay_tx.materials['samples']), 4)  # 4 assay samples in a_gilbert-assay-Tx.txt
            self.assertEqual(len(assay_tx.materials['other_material']), 4)  # 4 other materials in a_gilbert-assay-Tx.txt
            self.assertEqual(len(assay_tx.data_files), 24)  # 24 data files  in a_gilbert-assay-Tx.txt
            self.assertEqual(len(assay_tx.process_sequence), 36)  # 36 processes in in a_gilbert-assay-Tx.txt

    def test_isatab_load_bii_s_7(self):
        with open(os.path.join(self._tab_data_dir, 'BII-S-7', 'i_matteo.txt')) as fp:
            ISA = isatab.load(fp)

            self.assertListEqual([s.filename for s in ISA.studies], ['s_BII-S-7.txt'])  # 1 studies in i_gilbert.txt

            study_bii_s_7 = [s for s in ISA.studies if s.filename == 's_BII-S-7.txt'][0]

            self.assertEqual(len(study_bii_s_7.materials['sources']), 29)  # 29 sources in s_BII-S-7.txt
            self.assertEqual(len(study_bii_s_7.materials['samples']), 29)  # 29 study samples in s_BII-S-7.txt
            self.assertEqual(len(study_bii_s_7.process_sequence), 29)  # 29 study processes in s_BII-S-7.txt

            self.assertListEqual([a.filename for a in study_bii_s_7.assays], ['a_matteo-assay-Gx.txt'])  # 1 assays in s_BII-S-1.txt

            assay_gx = [a for a in study_bii_s_7.assays if a.filename == 'a_matteo-assay-Gx.txt'][0]

            self.assertEqual(len(assay_gx.materials['samples']), 29)  # 29 assay samples in a_matteo-assay-Gx.txt
            self.assertEqual(len(assay_gx.materials['other_material']), 29)  # 29 other materials in a_matteo-assay-Gx.txt
            self.assertEqual(len(assay_gx.data_files), 29)  # 29 data files  in a_matteo-assay-Gx.txt
            self.assertEqual(len(assay_gx.process_sequence), 116)  # 116 processes in in a_matteo-assay-Gx.txt


class UnitTestIsaTabDump(unittest.TestCase):
    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_source_protocol_ref_sample(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='sample collection')]
        )
        source1 = Source(name='source1')
        sample1 = Sample(name='sample1')
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1]
        s.process_sequence = [sample_collection_process]
        i.studies = [s]
        expected = """Source Name	Protocol REF	Sample Name
source1	sample collection	sample1"""
        self.assertIn(expected, isatab.dumps(i))

    def test_source_protocol_ref_sample_x2(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='sample collection')]
        )
        source1 = Source(name='source1')
        sample1 = Sample(name='sample1')
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1]
        source2 = Source(name='source2')
        sample2 = Sample(name='sample2')
        sample_collection_process2 = Process(executes_protocol=s.protocols[0])
        sample_collection_process2.inputs = [source2]
        sample_collection_process2.outputs = [sample2]
        s.process_sequence = [sample_collection_process, sample_collection_process2]
        i.studies = [s]

        expected_line1 = """Source Name	Protocol REF	Sample Name"""
        expected_line2 = """source1	sample collection	sample1"""
        expected_line3 = """source2	sample collection	sample2"""
        dumps_out = isatab.dumps(i)

        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)

    def test_source_protocol_ref_sample_split(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='sample collection')]
        )
        source1 = Source(name='source1')
        sample1 = Sample(name='sample1')
        sample2 = Sample(name='sample2')
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1, sample2]
        s.process_sequence = [sample_collection_process]
        i.studies = [s]

        expected_line1 = """Source Name	Protocol REF	Sample Name"""
        expected_line2 = """source1	sample collection	sample1"""
        expected_line3 = """source1	sample collection	sample2"""
        dumps_out = isatab.dumps(i)

        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)

    def test_source_protocol_ref_sample_pool(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='sample collection')]
        )
        source1 = Source(name='source1')
        source2 = Source(name='source2')
        sample1 = Sample(name='sample1')
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        sample_collection_process.inputs = [source1, source2]
        sample_collection_process.outputs = [sample1]
        s.process_sequence = [sample_collection_process]
        i.studies = [s]

        expected_line1 = """Source Name	Protocol REF	Sample Name"""
        expected_line2 = """source1	sample collection	sample1"""
        expected_line3 = """source2	sample collection	sample1"""
        dumps_out = isatab.dumps(i)

        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)

    def test_source_protocol_ref_sample_with_characteristics(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='sample collection')]
        )
        reference_descriptor_category = OntologyAnnotation(term='reference descriptor')
        organism_part_category = OntologyAnnotation(term='organism part')
        source1 = Source(name='source1')
        source1.characteristics = [Characteristic(category=reference_descriptor_category, value='not applicable')]
        sample1 = Sample(name='sample1')
        sample1.characteristics = [
            Characteristic(category=organism_part_category, value=OntologyAnnotation(term='liver'))]
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1]
        s.process_sequence = [sample_collection_process]
        i.studies = [s]
        expected = """Source Name	Characteristics[reference descriptor]	Protocol REF	Sample Name	Characteristics[organism part]
source1	not applicable	sample collection	sample1	liver"""
        self.assertIn(expected, isatab.dumps(i))

    def test_source_protocol_ref_sample_with_parameter_values(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[
                Protocol(name='sample collection',
                         parameters=[ProtocolParameter(parameter_name=OntologyAnnotation(term='temperature'))])
            ]
        )
        source1 = Source(name='source1')
        sample1 = Sample(name='sample1')
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        sample_collection_process.parameter_values = [ParameterValue(category=s.protocols[0].parameters[0], value=10)]
        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1]
        s.process_sequence = [sample_collection_process]
        i.studies = [s]
        expected = """Source Name	Protocol REF	Parameter Value[temperature]	Sample Name
source1	sample collection	10	sample1"""
        self.assertIn(expected, isatab.dumps(i))

    def test_source_protocol_ref_sample_with_factor_values(self):
        i = Investigation()
        s = Study(filename='s_test.txt',
                  protocols=[Protocol(name='sample collection')],
                  factors=[StudyFactor(name='study group')])
        source1 = Source(name='source1')
        sample1 = Sample(name='sample1')
        sample1.factor_values = [FactorValue(factor_name=s.factors[0], value="Study group 1")]
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1]
        s.process_sequence = [sample_collection_process]
        i.studies = [s]
        expected = """Source Name	Protocol REF	Sample Name	Factor Value[study group]
source1	sample collection	sample1	Study group 1"""
        self.assertIn(expected, isatab.dumps(i))

    def test_source_protocol_ref_protocol_ref_sample(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='sample collection'), Protocol(name='aliquoting')]
        )
        source1 = Source(name='source1')
        aliquot1 = Sample(name='aliquot1')
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        aliquoting_process = Process(executes_protocol=s.protocols[1])
        sample_collection_process.inputs = [source1]
        aliquoting_process.outputs = [aliquot1]
        plink(sample_collection_process, aliquoting_process)
        s.process_sequence = [sample_collection_process, aliquoting_process]
        i.studies = [s]
        expected = """Source Name	Protocol REF	Protocol REF	Sample Name
source1	sample collection	aliquoting	aliquot1"""
        self.assertIn(expected, isatab.dumps(i))

    def test_source_protocol_ref_sample_protocol_ref_sample(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='sample collection'), Protocol(name='aliquoting')]
        )
        source1 = Source(name='source1')
        sample1 = Sample(name='sample1')
        aliquot1 = Sample(name='aliquot1')
        sample_collection_process = Process(executes_protocol=s.protocols[0])
        aliquoting_process = Process(executes_protocol=s.protocols[1])
        sample_collection_process.inputs = [source1]
        sample_collection_process.outputs = [sample1]
        aliquoting_process.inputs = [sample1]
        aliquoting_process.outputs = [aliquot1]
        plink(sample_collection_process, aliquoting_process)
        s.process_sequence = [sample_collection_process, aliquoting_process]
        i.studies = [s]
        expected = """Source Name	Protocol REF	Sample Name	Protocol REF	Sample Name
source1	sample collection	sample1	aliquoting	aliquot1"""
        self.assertIn(expected, isatab.dumps(i))

    def test_sample_protocol_ref_material_protocol_ref_data(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='extraction'), Protocol(name='scanning')]
        )
        sample1 = Sample(name='sample1')
        extract1 = Material(name='extract1', type_='Extract Name')
        data1 = DataFile(filename='datafile.raw', label='Raw Data File')
        extraction_process = Process(executes_protocol=s.protocols[0])
        scanning_process = Process(executes_protocol=s.protocols[1])
        extraction_process.inputs = [sample1]
        extraction_process.outputs = [extract1]
        scanning_process.inputs = [extract1]
        scanning_process.outputs = [data1]
        plink(extraction_process, scanning_process)
        a = Assay(filename='a_test.txt')
        a.process_sequence = [extraction_process, scanning_process]
        s.assays = [a]
        i.studies = [s]
        expected = """Sample Name	Protocol REF	Extract Name	Protocol REF	Raw Data File
sample1	extraction	extract1	scanning	datafile.raw"""
        self.assertIn(expected, isatab.dumps(i))

    def test_sample_protocol_ref_material_protocol_ref_data_x2(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='extraction'), Protocol(name='scanning')]
        )
        sample1 = Sample(name='sample1')
        extract1 = Material(name='extract1', type_='Extract Name')
        data1 = DataFile(filename='datafile1.raw', label='Raw Data File')
        extraction_process1 = Process(executes_protocol=s.protocols[0])
        scanning_process1 = Process(executes_protocol=s.protocols[1])
        extraction_process1.inputs = [sample1]
        extraction_process1.outputs = [extract1]
        scanning_process1.inputs = [extract1]
        scanning_process1.outputs = [data1]
        plink(extraction_process1, scanning_process1)

        sample2 = Sample(name='sample2')
        extract2 = Material(name='extract2', type_='Extract Name')
        data2 = DataFile(filename='datafile2.raw', label='Raw Data File')
        extraction_process2 = Process(executes_protocol=s.protocols[0])
        scanning_process2 = Process(executes_protocol=s.protocols[1])
        extraction_process2.inputs = [sample2]
        extraction_process2.outputs = [extract2]
        scanning_process2.inputs = [extract2]
        scanning_process2.outputs = [data2]
        plink(extraction_process2, scanning_process2)

        a = Assay(filename='a_test.txt')
        a.process_sequence = [scanning_process1, extraction_process1, scanning_process2, extraction_process2]
        s.assays = [a]
        i.studies = [s]

        expected_line1 = """Sample Name	Protocol REF	Extract Name	Protocol REF	Raw Data File"""
        expected_line2 = """sample1	extraction	extract1	scanning	datafile1.raw"""
        expected_line3 = """sample2	extraction	extract2	scanning	datafile2.raw"""
        dumps_out = isatab.dumps(i)

        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)

    def test_sample_split_protocol_ref_material_protocol_ref_data(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='extraction'), Protocol(name='scanning')]
        )
        sample1 = Sample(name='sample1')
        extract1 = Material(name='extract1', type_='Extract Name')
        extract2 = Material(name='extract2', type_='Extract Name')
        data1 = DataFile(filename='datafile1.raw', label='Raw Data File')
        data2 = DataFile(filename='datafile2.raw', label='Raw Data File')

        extraction_process1 = Process(executes_protocol=s.protocols[0])
        extraction_process1.inputs = [sample1]
        extraction_process1.outputs = [extract1, extract2]

        scanning_process1 = Process(executes_protocol=s.protocols[1])
        scanning_process1.inputs = [extract1]
        scanning_process1.outputs = [data1]

        scanning_process2 = Process(executes_protocol=s.protocols[1])
        scanning_process2.inputs = [extract2]
        scanning_process2.outputs = [data2]
        plink(extraction_process1, scanning_process1)
        plink(extraction_process1, scanning_process2)

        a = Assay(filename='a_test.txt')
        a.process_sequence = [scanning_process1, extraction_process1, scanning_process2]
        s.assays = [a]
        i.studies = [s]
        expected_line1 = """Sample Name	Protocol REF	Extract Name	Protocol REF	Raw Data File"""
        expected_line2 = """sample1	extraction	extract1	scanning	datafile1.raw"""
        expected_line3 = """sample1	extraction	extract2	scanning	datafile2.raw"""
        dumps_out = isatab.dumps(i)
        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)

    def test_sample_protocol_ref_material_protocol_split_ref_data(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='extraction'), Protocol(name='scanning')]
        )
        sample1 = Sample(name='sample1')
        extract1 = Material(name='extract1', type_='Extract Name')
        data1 = DataFile(filename='datafile1.raw', label='Raw Data File')
        data2 = DataFile(filename='datafile2.raw', label='Raw Data File')

        extraction_process1 = Process(executes_protocol=s.protocols[0])
        extraction_process1.inputs = [sample1]
        extraction_process1.outputs = [extract1]

        scanning_process1 = Process(executes_protocol=s.protocols[1])
        scanning_process1.inputs = [extract1]
        scanning_process1.outputs = [data1]

        scanning_process2 = Process(executes_protocol=s.protocols[1])
        scanning_process2.inputs = [extract1]
        scanning_process2.outputs = [data2]

        plink(extraction_process1, scanning_process1)
        plink(extraction_process1, scanning_process2)

        a = Assay(filename='a_test.txt')
        a.process_sequence = [extraction_process1, scanning_process1, scanning_process2]
        s.assays = [a]
        i.studies = [s]

        expected_line1 = """Sample Name	Protocol REF	Extract Name	Protocol REF	Raw Data File"""
        expected_line2 = """sample1	extraction	extract1	scanning	datafile1.raw"""
        expected_line3 = """sample1	extraction	extract1	scanning	datafile2.raw"""
        dumps_out = isatab.dumps(i)

        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)

    def test_sample_pool_protocol_ref_material_protocol_ref_data(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='extraction'), Protocol(name='scanning')]
        )
        sample1 = Sample(name='sample1')
        sample2 = Sample(name='sample2')
        extract1 = Material(name='extract1', type_='Extract Name')
        data1 = DataFile(filename='datafile1.raw', label='Raw Data File')
        extraction_process1 = Process(executes_protocol=s.protocols[0])
        scanning_process1 = Process(executes_protocol=s.protocols[1])
        extraction_process1.inputs = [sample1, sample2]
        extraction_process1.outputs = [extract1]

        scanning_process1.inputs = [extract1]
        scanning_process1.outputs = [data1]
        plink(extraction_process1, scanning_process1)

        a = Assay(filename='a_test.txt')
        a.process_sequence = [extraction_process1, scanning_process1]
        s.assays = [a]
        i.studies = [s]

        expected_line1 = """Sample Name	Protocol REF	Extract Name	Protocol REF	Raw Data File"""
        expected_line2 = """sample1	extraction	extract1	scanning	datafile1.raw"""
        expected_line3 = """sample2	extraction	extract1	scanning	datafile1.raw"""
        dumps_out = isatab.dumps(i)

        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)

    def test_sample_protocol_ref_material_pool_protocol_ref_data(self):
        i = Investigation()
        s = Study(
            filename='s_test.txt',
            protocols=[Protocol(name='extraction'), Protocol(name='scanning')]
        )
        sample1 = Sample(name='sample1')
        sample2 = Sample(name='sample2')
        extract1 = Material(name='extract1', type_='Extract Name')
        extract2 = Material(name='extract2', type_='Extract Name')
        data1 = DataFile(filename='datafile1.raw', label='Raw Data File')

        extraction_process1 = Process(executes_protocol=s.protocols[0])
        extraction_process1.inputs = [sample1]
        extraction_process1.outputs = [extract1]

        extraction_process2 = Process(executes_protocol=s.protocols[0])
        extraction_process2.inputs = [sample2]
        extraction_process2.outputs = [extract2]

        scanning_process1 = Process(executes_protocol=s.protocols[1])
        scanning_process1.inputs = [extract1, extract2]
        scanning_process1.outputs = [data1]
        plink(extraction_process1, scanning_process1)
        plink(extraction_process2, scanning_process1)

        a = Assay(filename='a_test.txt')
        a.process_sequence = [extraction_process1, extraction_process2, scanning_process1]
        s.assays = [a]
        i.studies = [s]

        expected_line1 = """Sample Name	Protocol REF	Extract Name	Protocol REF	Raw Data File"""
        expected_line2 = """sample1	extraction	extract1	scanning	datafile1.raw"""
        expected_line3 = """sample2	extraction	extract2	scanning	datafile1.raw"""
        dumps_out = isatab.dumps(i)

        self.assertIn(expected_line1, dumps_out)
        self.assertIn(expected_line2, dumps_out)
        self.assertIn(expected_line3, dumps_out)


class UnitTestIsaTabLoad(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_source_protocol_ref_sample(self):
        factory = ProcessSequenceFactory(study_protocols=[Protocol(name="sample collection")])
        table_to_load = """Source Name	Protocol REF	Sample Name
source1	sample collection	sample1"""
        DF = pd.read_csv(StringIO(table_to_load), sep='\t')
        DF.isatab_header = ["Source Name", "Protocol REF", "Sample Name"]
        so, sa, om, d, pr, _, __ = factory.create_from_df(DF)
        self.assertEqual(len(so), 1)
        self.assertEqual(len(sa), 1)
        self.assertEqual(len(om), 0)
        self.assertEqual(len(d), 0)
        self.assertEqual(len(pr), 1)

    def test_source_protocol_ref_sample_x2(self):
        factory = ProcessSequenceFactory(study_protocols=[Protocol(name="sample collection")])
        table_to_load = """Source Name	Protocol REF	Sample Name
source1	sample collection	sample1
source2	sample collection	sample2"""
        DF = pd.read_csv(StringIO(table_to_load), sep='\t')
        DF.isatab_header = ["Source Name", "Protocol REF", "Sample Name"]
        so, sa, om, d, pr, _, __ = factory.create_from_df(DF)
        self.assertEqual(len(so), 2)
        self.assertEqual(len(sa), 2)
        self.assertEqual(len(om), 0)
        self.assertEqual(len(d), 0)
        self.assertEqual(len(pr), 2)

    def test_source_protocol_ref_split_sample(self):
        factory = ProcessSequenceFactory(study_protocols=[Protocol(name="sample collection")])
        table_to_load = """Source Name	Protocol REF	Sample Name
source1	sample collection	sample1
source1	sample collection	sample2"""
        DF = pd.read_csv(StringIO(table_to_load), sep='\t')
        DF.isatab_header = ["Source Name", "Protocol REF", "Sample Name"]
        so, sa, om, d, pr, _, __ = factory.create_from_df(DF)
        self.assertEqual(len(so), 1)
        self.assertEqual(len(sa), 2)
        self.assertEqual(len(om), 0)
        self.assertEqual(len(d), 0)
        self.assertEqual(len(pr), 1)

    def test_source_protocol_ref_pool_sample(self):
        factory = ProcessSequenceFactory(study_protocols=[Protocol(name="sample collection")])
        table_to_load = """Source Name	Protocol REF	Sample Name
source1	sample collection	sample1
source2	sample collection	sample1"""
        DF = pd.read_csv(StringIO(table_to_load), sep='\t')
        DF.isatab_header = ["Source Name", "Protocol REF", "Sample Name"]
        so, sa, om, d, pr, _, __ = factory.create_from_df(DF)
        self.assertEqual(len(so), 2)
        self.assertEqual(len(sa), 1)
        self.assertEqual(len(om), 0)
        self.assertEqual(len(d), 0)
        self.assertEqual(len(pr), 1)

    def test_sample_protocol_ref_split_extract_protocol_ref_data(self):
        factory = ProcessSequenceFactory(
            study_samples=[Sample(name="sample1")],
            study_protocols=[Protocol(name="extraction"), Protocol(name="scanning")])
        table_to_load = """Sample Name	Protocol REF	Extract Name	Protocol REF	Raw Data File
sample1	extraction	e1	scanning	d1
sample1	extraction	e2	scanning	d2"""
        DF = pd.read_csv(StringIO(table_to_load), sep='\t')
        DF.isatab_header = ["Source Name", "Protocol REF", "Extract Name", "Protocol REF", "Raw Data File"]
        so, sa, om, d, pr, _, __ = factory.create_from_df(DF)
        self.assertEqual(len(so), 0)
        self.assertEqual(len(sa), 1)
        self.assertEqual(len(om), 2)
        self.assertEqual(len(d), 2)
        self.assertEqual(len(pr), 3)

    def test_isatab_load_issue210_on_MTBLS30(self):
        with open(os.path.join(self._tab_data_dir, 'MTBLS30', 'i_Investigation.txt')) as fp:
            ISA = isatab.load(fp)
            self.assertEqual(len(ISA.studies[0].assays[0].data_files), 1)
            self.assertEqual(len(ISA.studies[0].assays[1].data_files), 1)

    def test_isatab_load_issue210_on_Sacurine(self):
        with open(os.path.join(self._tab_data_dir, 'MTBLS404', 'i_sacurine.txt')) as fp:
            ISA = isatab.load(fp)
            self.assertEqual(len([x for x in ISA.studies[0].assays[0].materials['other_material']
                                  if x.type == "Labeled Extract Name"]), 0)

