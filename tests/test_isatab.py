"""Tests on isatab.py package"""
from __future__ import absolute_import
import unittest
import os
import pandas as pd
import shutil
import tempfile
from io import StringIO
import io

from isatools import isatab
from isatools.isatab import ProcessSequenceFactory
from isatools.model import *
from isatools.tests.utils import assert_tab_content_equal
from isatools.tests import utils


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise IOError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestIsaTabLoad(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab_load_issue200(self):
        with open(os.path.join(self._tab_data_dir, 'issue200', 'i_Investigation.txt')) as fp:
            ISA = isatab.load(fp)
            self.assertEqual(len(ISA.studies[0].assays[0].samples), 7)
            self.assertEqual(len(ISA.studies[0].assays[0].other_material), 7)
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
        with io.open(os.path.join(self._tab_data_dir, 'sdata201414-isa1', 'i_Investigation.txt'), encoding='utf-8') as fp:
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

            self.assertEqual(len(study_bii_s_1.sources), 18)  # 18 sources in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_1.samples), 164)  # 164 study samples in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_1.process_sequence), 18)  # 18 study processes in s_BII-S-1.txt

            self.assertListEqual([a.filename for a in study_bii_s_1.assays], ['a_proteome.txt', 'a_metabolome.txt', 'a_transcriptome.txt'])  # 2 assays in s_BII-S-1.txt

            assay_proteome = [a for a in study_bii_s_1.assays if a.filename == 'a_proteome.txt'][0]

            self.assertEqual(len(assay_proteome.samples), 8)  # 8 assay samples in a_proteome.txt
            self.assertEqual(len(assay_proteome.other_material), 19)  # 19 other materials in a_proteome.txt

            self.assertEqual(len(assay_proteome.data_files), 7)  # 7 data files  in a_proteome.txt

            self.assertEqual(len(assay_proteome.process_sequence), 25)  # 25 processes in in a_proteome.txt

            assay_metabolome = [a for a in study_bii_s_1.assays if a.filename == 'a_metabolome.txt'][0]

            self.assertEqual(len(assay_metabolome.samples), 92)  # 92 assay samples in a_metabolome.txt
            self.assertEqual(len(assay_metabolome.other_material), 92)  # 92 other materials in a_metabolome.txt
            self.assertEqual(len(assay_metabolome.data_files), 111)  # 111 data files  in a_metabolome.txt
            self.assertEqual(len(assay_metabolome.process_sequence), 203)  # 203 processes in in a_metabolome.txt

            assay_transcriptome = [a for a in study_bii_s_1.assays if a.filename == 'a_transcriptome.txt'][0]

            self.assertEqual(len(assay_transcriptome.samples), 48)  # 48 assay samples in a_transcriptome.txt
            self.assertEqual(len(assay_transcriptome.other_material), 96)  # 96 other materials in a_transcriptome.txt
            self.assertEqual(len(assay_transcriptome.data_files), 49)  # 49 data files  in a_transcriptome.txt
            self.assertEqual(len(assay_transcriptome.process_sequence), 193)  # 193 processes in in a_transcriptome.txt

            study_bii_s_2 = [s for s in ISA.studies if s.filename == 's_BII-S-2.txt'][0]

            self.assertEqual(len(study_bii_s_2.sources), 1)  # 1 sources in s_BII-S-2.txt
            self.assertEqual(len(study_bii_s_2.samples), 2)  # 2 study samples in s_BII-S-2.txt
            self.assertEqual(len(study_bii_s_2.process_sequence), 1)  # 1 study processes in s_BII-S-2.txt

            self.assertEqual(len(study_bii_s_2.assays), 1)  # 1 assays in s_BII-S-2.txt
            self.assertListEqual([a.filename for a in study_bii_s_2.assays], ['a_microarray.txt'])  # 1 assays in s_BII-S-2.txt

            assay_microarray = [a for a in study_bii_s_2.assays if a.filename == 'a_microarray.txt'][0]

            self.assertEqual(len(assay_microarray.samples), 2)  # 2 assay samples in a_microarray.txt
            self.assertEqual(len(assay_microarray.other_material), 28)  # 28 other materials in a_microarray.txt
            self.assertEqual(len(assay_microarray.data_files), 15)  # 15 data files  in a_microarray.txt
            self.assertEqual(len(assay_microarray.process_sequence), 45)  # 45 processes in in a_microarray.txt

    def test_isatab_load_bii_s_3(self):
        with open(os.path.join(self._tab_data_dir, 'BII-S-3', 'i_gilbert.txt')) as fp:
            ISA = isatab.load(fp)

            self.assertListEqual([s.filename for s in ISA.studies], ['s_BII-S-3.txt'])  # 1 studies in i_gilbert.txt

            study_bii_s_3 = [s for s in ISA.studies if s.filename == 's_BII-S-3.txt'][0]

            self.assertEqual(len(study_bii_s_3.sources), 4)  # 4 sources in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_3.samples), 4)  # 4 study samples in s_BII-S-1.txt
            self.assertEqual(len(study_bii_s_3.process_sequence), 4)  # 4 study processes in s_BII-S-1.txt

            self.assertListEqual([a.filename for a in study_bii_s_3.assays], ['a_gilbert-assay-Gx.txt', 'a_gilbert-assay-Tx.txt'])  # 2 assays in s_BII-S-1.txt

            assay_gx = [a for a in study_bii_s_3.assays if a.filename == 'a_gilbert-assay-Gx.txt'][0]

            self.assertEqual(len(assay_gx.samples), 4)  # 4 assay samples in a_gilbert-assay-Gx.txt
            self.assertEqual(len(assay_gx.other_material), 4)  # 4 other materials in a_gilbert-assay-Gx.txt
            self.assertEqual(len(assay_gx.data_files), 6)  # 6 data files  in a_gilbert-assay-Gx.txt
            self.assertEqual(len(assay_gx.process_sequence), 18)  # 18 processes in in a_gilbert-assay-Gx.txt

            assay_tx = [a for a in study_bii_s_3.assays if a.filename == 'a_gilbert-assay-Tx.txt'][0]

            self.assertEqual(len(assay_tx.samples), 4)  # 4 assay samples in a_gilbert-assay-Tx.txt
            self.assertEqual(len(assay_tx.other_material), 4)  # 4 other materials in a_gilbert-assay-Tx.txt
            self.assertEqual(len(assay_tx.data_files), 24)  # 24 data files  in a_gilbert-assay-Tx.txt
            self.assertEqual(len(assay_tx.process_sequence), 36)  # 36 processes in in a_gilbert-assay-Tx.txt

    def test_isatab_load_bii_s_7(self):
        with open(os.path.join(self._tab_data_dir, 'BII-S-7', 'i_matteo.txt')) as fp:
            ISA = isatab.load(fp)

            self.assertListEqual([s.filename for s in ISA.studies], ['s_BII-S-7.txt'])  # 1 studies in i_gilbert.txt

            study_bii_s_7 = [s for s in ISA.studies if s.filename == 's_BII-S-7.txt'][0]

            self.assertEqual(len(study_bii_s_7.sources), 29)  # 29 sources in s_BII-S-7.txt
            self.assertEqual(len(study_bii_s_7.samples), 29)  # 29 study samples in s_BII-S-7.txt
            self.assertEqual(len(study_bii_s_7.process_sequence), 29)  # 29 study processes in s_BII-S-7.txt

            self.assertListEqual([a.filename for a in study_bii_s_7.assays], ['a_matteo-assay-Gx.txt'])  # 1 assays in s_BII-S-1.txt

            assay_gx = [a for a in study_bii_s_7.assays if a.filename == 'a_matteo-assay-Gx.txt'][0]

            self.assertEqual(len(assay_gx.samples), 29)  # 29 assay samples in a_matteo-assay-Gx.txt
            self.assertEqual(len(assay_gx.other_material), 29)  # 29 other materials in a_matteo-assay-Gx.txt
            self.assertEqual(len(assay_gx.data_files), 29)  # 29 data files  in a_matteo-assay-Gx.txt
            self.assertEqual(len(assay_gx.process_sequence), 116)  # 116 processes in in a_matteo-assay-Gx.txt


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
        with open(os.path.join(self._tab_data_dir, 'MTBLS30', 'i_Investigation.txt'), 'rU') as fp:
            ISA = isatab.load(fp)
            self.assertEqual(len(ISA.studies[0].assays[0].data_files), 1)
            self.assertEqual(len(ISA.studies[0].assays[1].data_files), 1)

    def test_isatab_load_issue210_on_Sacurine(self):
        with open(os.path.join(self._tab_data_dir, 'MTBLS404', 'i_sacurine.txt'), 'rU') as fp:
            ISA = isatab.load(fp)
            self.assertEqual(len([x for x in ISA.studies[0].assays[0].other_material
                                  if x.type == "Labeled Extract Name"]), 0)
