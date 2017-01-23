import unittest
from isatools import isajson
import json
from tests import utils
import os


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError("Could not fine test data directory in {0}. Ensure you have cloned the ISAdatasets "
                                "repository using "
                                "git clone -b tests --single-branch git@github.com:ISA-tools/ISAdatasets {0}"
                                .format(utils.DATA_DIR))


class TestIsaJson(unittest.TestCase):

    def setUp(self):
        self._json_data_dir = utils.JSON_DATA_DIR

    def test_json_load_and_dump_bii_i_1(self):
        # Load into ISA objects
        ISA = isajson.load(open(os.path.join(utils.JSON_DATA_DIR, 'BII-I-1', 'BII-I-1.json')))

        # Dump into ISA JSON from ISA objects
        ISA_J = json.loads(json.dumps(ISA, cls=isajson.ISAJSONEncoder))

        self.assertListEqual([s['filename'] for s in ISA_J['studies']], ['s_BII-S-1.txt', 's_BII-S-2.txt'])  # 2 studies in i_investigation.txt

        study_bii_s_1 = [s for s in ISA_J['studies'] if s['filename'] == 's_BII-S-1.txt'][0]

        self.assertEqual(len(study_bii_s_1['materials']['sources']), 18)  # 18 sources in s_BII-S-1.txt
        self.assertEqual(len(study_bii_s_1['materials']['samples']), 164)  # 164 study samples in s_BII-S-1.txt
        self.assertEqual(len(study_bii_s_1['processSequence']), 18)  # 18 study processes in s_BII-S-1.txt

        self.assertListEqual([a['filename'] for a in study_bii_s_1['assays']], ['a_proteome.txt', 'a_metabolome.txt', 'a_transcriptome.txt'])  # 2 assays in s_BII-S-1.txt

        assay_proteome = [a for a in study_bii_s_1['assays'] if a['filename'] == 'a_proteome.txt'][0]

        self.assertEqual(len(assay_proteome['materials']['samples']), 8)  # 8 assay samples in a_proteome.txt
        self.assertEqual(len(assay_proteome['materials']['otherMaterials']), 19)  # 19 other materials in a_proteome.txt
        self.assertEqual(len(assay_proteome['dataFiles']), 7)  # 7 data files  in a_proteome.txt
        self.assertEqual(len(assay_proteome['processSequence']), 25)  # 25 processes in in a_proteome.txt

        assay_metabolome = [a for a in study_bii_s_1['assays'] if a['filename'] == 'a_metabolome.txt'][0]

        self.assertEqual(len(assay_metabolome['materials']['samples']), 92)  # 92 assay samples in a_metabolome.txt
        self.assertEqual(len(assay_metabolome['materials']['otherMaterials']), 92)  # 92 other materials in a_metabolome.txt
        self.assertEqual(len(assay_metabolome['dataFiles']), 111)  # 111 data files  in a_metabolome.txt
        self.assertEqual(len(assay_metabolome['processSequence']), 203)  # 203 processes in in a_metabolome.txt

        assay_transcriptome = [a for a in study_bii_s_1['assays'] if a['filename'] == 'a_transcriptome.txt'][0]

        self.assertEqual(len(assay_transcriptome['materials']['samples']), 48)  # 48 assay samples in a_transcriptome.txt
        self.assertEqual(len(assay_transcriptome['materials']['otherMaterials']), 96)  # 96 other materials in a_transcriptome.txt
        self.assertEqual(len(assay_transcriptome['dataFiles']), 49)  # 49 data files  in a_transcriptome.txt
        self.assertEqual(len(assay_transcriptome['processSequence']), 193)  # 203 processes in in a_transcriptome.txt

        study_bii_s_2 = [s for s in ISA_J['studies'] if s['filename'] == 's_BII-S-2.txt'][0]

        self.assertEqual(len(study_bii_s_2['materials']['sources']), 1)  # 1 sources in s_BII-S-2.txt
        self.assertEqual(len(study_bii_s_2['materials']['samples']), 2)  # 2 study samples in s_BII-S-2.txt
        self.assertEqual(len(study_bii_s_2['processSequence']), 1)  # 1 study processes in s_BII-S-2.txt

        self.assertEqual(len(study_bii_s_2['assays']), 1)  # 1 assays in s_BII-S-2.txt
        self.assertListEqual([a['filename'] for a in study_bii_s_2['assays']], ['a_microarray.txt'])  # 1 assays in s_BII-S-2.txt
        
        assay_microarray = [a for a in study_bii_s_2['assays'] if a['filename'] == 'a_microarray.txt'][0]

        self.assertEqual(len(assay_microarray['materials']['samples']), 2)  # 2 assay samples in a_microarray.txt
        self.assertEqual(len(assay_microarray['materials']['otherMaterials']), 28)  # 28 other materials in a_microarray.txt
        self.assertEqual(len(assay_microarray['dataFiles']), 15)  # 15 data files  in a_microarray.txt
        self.assertEqual(len(assay_microarray['processSequence']), 45)  # 45 processes in in a_microarray.txt

    def test_json_load_and_dump_bii_s_3(self):
        # Load into ISA objects
        ISA = isajson.load(open(os.path.join(utils.JSON_DATA_DIR, 'BII-S-3', 'BII-S-3.json')))

        # Dump into ISA JSON from ISA objects
        ISA_J = json.loads(json.dumps(ISA, cls=isajson.ISAJSONEncoder))
    
        self.assertListEqual([s['filename'] for s in ISA_J['studies']], ['s_BII-S-3.txt'])  # 1 studies in i_gilbert.txt
    
        study_bii_s_3 = [s for s in ISA_J['studies'] if s['filename'] == 's_BII-S-3.txt'][0]
    
        self.assertEqual(len(study_bii_s_3['materials']['sources']), 4)  # 4 sources in s_BII-S-1.txt
        self.assertEqual(len(study_bii_s_3['materials']['samples']), 4)  # 4 study samples in s_BII-S-1.txt
        self.assertEqual(len(study_bii_s_3['processSequence']), 4)  # 4 study processes in s_BII-S-1.txt

        self.assertListEqual([a['filename'] for a in study_bii_s_3['assays']], ['a_gilbert-assay-Gx.txt', 'a_gilbert-assay-Tx.txt'])  # 2 assays in s_BII-S-1.txt
    
        assay_gx = [a for a in study_bii_s_3['assays'] if a['filename'] == 'a_gilbert-assay-Gx.txt'][0]
    
        self.assertEqual(len(assay_gx['materials']['samples']), 4)  # 4 assay samples in a_gilbert-assay-Gx.txt
        self.assertEqual(len(assay_gx['materials']['otherMaterials']), 4)  # 4 other materials in a_gilbert-assay-Gx.txt
        self.assertEqual(len(assay_gx['dataFiles']), 6)  # 6 data files  in a_gilbert-assay-Gx.txt
        self.assertEqual(len(assay_gx['processSequence']), 18)  # 18 processes in in a_gilbert-assay-Gx.txt

        assay_tx = [a for a in study_bii_s_3['assays'] if a['filename'] == 'a_gilbert-assay-Tx.txt'][0]
    
        self.assertEqual(len(assay_tx['materials']['samples']), 4)  # 4 assay samples in a_gilbert-assay-Tx.txt
        self.assertEqual(len(assay_tx['materials']['otherMaterials']), 4)  # 4 other materials in a_gilbert-assay-Tx.txt
        self.assertEqual(len(assay_tx['dataFiles']), 24)  # 24 data files  in a_gilbert-assay-Tx.txt
        self.assertEqual(len(assay_tx['processSequence']), 36)  # 36 processes in in a_gilbert-assay-Tx.txt

    def test_json_load_and_dump_bii_s_7(self):
        # Load into ISA objects
        ISA = isajson.load(open(os.path.join(utils.JSON_DATA_DIR, 'BII-S-7', 'BII-S-7.json')))

        # Dump into ISA JSON from ISA objects
        ISA_J = json.loads(json.dumps(ISA, cls=isajson.ISAJSONEncoder))
    
        self.assertListEqual([s['filename'] for s in ISA_J['studies']], ['s_BII-S-7.txt'])  # 1 studies in i_gilbert.txt
    
        study_bii_s_7 = [s for s in ISA_J['studies'] if s['filename'] == 's_BII-S-7.txt'][0]
    
        self.assertEqual(len(study_bii_s_7['materials']['sources']), 29)  # 29 sources in s_BII-S-1.txt
        self.assertEqual(len(study_bii_s_7['materials']['samples']), 29)  # 29 study samples in s_BII-S-1.txt
        self.assertEqual(len(study_bii_s_7['processSequence']), 29)  # 29 study processes in s_BII-S-1.txt
    
        self.assertListEqual([a['filename'] for a in study_bii_s_7['assays']], ['a_matteo-assay-Gx.txt'])  # 1 assays in s_BII-S-1.txt
    
        assay_gx = [a for a in study_bii_s_7['assays'] if a['filename'] == 'a_matteo-assay-Gx.txt'][0]
    
        self.assertEqual(len(assay_gx['materials']['samples']), 29)  # 29 assay samples in a_matteo-assay-Gx.txt
        self.assertEqual(len(assay_gx['materials']['otherMaterials']), 29)  # 29 other materials in a_matteo-assay-Gx.txt
        self.assertEqual(len(assay_gx['dataFiles']), 29)  # 29 data files  in a_matteo-assay-Gx.txt
        self.assertEqual(len(assay_gx['processSequence']), 116)  # 116 processes in in a_matteo-assay-Gx.txt
