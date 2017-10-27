"""Tests on isajson.py package"""
from __future__ import absolute_import
import json
import unittest
import os

from isatools import isajson


class TestIsaJson(unittest.TestCase):

    def setUp(self):
        self._json_data_dir = os.path.join(os.path.dirname(__file__), 'data',
                                           'json')

    def test_json_load_and_dump_bii_i_1(self):
        with open(os.path.join(self._json_data_dir, 'BII-I-1',
                               'BII-I-1.json')) as isajson_fp:
            ISA = isajson.load(isajson_fp)
            ISA_J = json.loads(json.dumps(ISA, cls=isajson.ISAJSONEncoder))
            self.assertListEqual([s['filename'] for s in ISA_J['studies']],
                                 ['s_BII-S-1.txt', 's_BII-S-2.txt'])
            study_bii_s_1 = \
            [s for s in ISA_J['studies'] if s['filename'] == 's_BII-S-1.txt'][0]
            self.assertEqual(len(study_bii_s_1['materials']['sources']), 18)
            self.assertEqual(len(study_bii_s_1['materials']['samples']), 164)
            self.assertEqual(len(study_bii_s_1['processSequence']), 18)
            self.assertListEqual(
                [a['filename'] for a in study_bii_s_1['assays']],
                ['a_proteome.txt', 'a_metabolome.txt',
                 'a_transcriptome.txt'])
            assay_proteome = [a for a in study_bii_s_1['assays'] if
                              a['filename'] == 'a_proteome.txt'][0]

            self.assertEqual(len(assay_proteome['materials']['samples']), 8)
            self.assertEqual(len(assay_proteome['materials']['otherMaterials']),
                             19)
            self.assertEqual(len(assay_proteome['dataFiles']), 7)
            self.assertEqual(len(assay_proteome['processSequence']), 25)

            assay_metabolome = [a for a in study_bii_s_1['assays'] if
                                a['filename'] == 'a_metabolome.txt'][0]
            self.assertEqual(len(assay_metabolome['materials']['samples']), 92)
            self.assertEqual(
                len(assay_metabolome['materials']['otherMaterials']), 92)
            self.assertEqual(len(assay_metabolome['dataFiles']), 111)
            self.assertEqual(len(assay_metabolome['processSequence']), 203)

            assay_transcriptome = [a for a in study_bii_s_1['assays'] if
                                   a['filename'] == 'a_transcriptome.txt'][0]
            self.assertEqual(len(assay_transcriptome['materials']['samples']),
                             48)
            self.assertEqual(
                len(assay_transcriptome['materials']['otherMaterials']), 96)
            self.assertEqual(len(assay_transcriptome['dataFiles']), 49)
            self.assertEqual(len(assay_transcriptome['processSequence']), 193)
            study_bii_s_2 = \
            [s for s in ISA_J['studies'] if s['filename'] == 's_BII-S-2.txt'][0]
            self.assertEqual(len(study_bii_s_2['materials']['sources']), 1)
            self.assertEqual(len(study_bii_s_2['materials']['samples']), 2)
            self.assertEqual(len(study_bii_s_2['processSequence']), 1)
            self.assertEqual(len(study_bii_s_2['assays']), 1)
            self.assertListEqual(
                [a['filename'] for a in study_bii_s_2['assays']],
                ['a_microarray.txt'])
            assay_microarray = [a for a in study_bii_s_2['assays'] if
                                a['filename'] == 'a_microarray.txt'][0]

            self.assertEqual(len(assay_microarray['materials']['samples']), 2)
            self.assertEqual(
                len(assay_microarray['materials']['otherMaterials']), 28)
            self.assertEqual(len(assay_microarray['dataFiles']), 15)
            self.assertEqual(len(assay_microarray['processSequence']), 45)

    def test_json_load_and_dump_bii_s_3(self):
        with open(os.path.join(self._json_data_dir, 'BII-S-3',
                               'BII-S-3.json')) as isajson_fp:
            ISA = isajson.load(isajson_fp)
            ISA_J = json.loads(json.dumps(ISA, cls=isajson.ISAJSONEncoder))
            self.assertListEqual([s['filename'] for s in ISA_J['studies']],
                                 ['s_BII-S-3.txt'])
            study_bii_s_3 = \
            [s for s in ISA_J['studies'] if s['filename'] == 's_BII-S-3.txt'][0]
            self.assertEqual(len(study_bii_s_3['materials']['sources']), 4)
            self.assertEqual(len(study_bii_s_3['materials']['samples']), 4)
            self.assertEqual(len(study_bii_s_3['processSequence']), 4)
            self.assertListEqual(
                [a['filename'] for a in study_bii_s_3['assays']],
                ['a_gilbert-assay-Gx.txt', 'a_gilbert-assay-Tx.txt'])
            assay_gx = [a for a in study_bii_s_3['assays'] if
                        a['filename'] == 'a_gilbert-assay-Gx.txt'][0]
            self.assertEqual(len(assay_gx['materials']['samples']), 4)
            self.assertEqual(len(assay_gx['materials']['otherMaterials']), 4)
            self.assertEqual(len(assay_gx['dataFiles']), 6)
            self.assertEqual(len(assay_gx['processSequence']), 18)
            assay_tx = [a for a in study_bii_s_3['assays'] if
                        a['filename'] == 'a_gilbert-assay-Tx.txt'][0]
            self.assertEqual(len(assay_tx['materials']['samples']), 4)
            self.assertEqual(len(assay_tx['materials']['otherMaterials']), 4)
            self.assertEqual(len(assay_tx['dataFiles']), 24)
            self.assertEqual(len(assay_tx['processSequence']), 36)

    def test_json_load_and_dump_bii_s_7(self):
        # Load into ISA objects
        with open(os.path.join(self._json_data_dir, 'BII-S-7',
                               'BII-S-7.json')) as isajson_fp:
            ISA = isajson.load(isajson_fp)
            ISA_J = json.loads(json.dumps(ISA, cls=isajson.ISAJSONEncoder))
            self.assertListEqual([s['filename'] for s in ISA_J['studies']],
                                 ['s_BII-S-7.txt'])
            study_bii_s_7 = \
            [s for s in ISA_J['studies'] if s['filename'] == 's_BII-S-7.txt'][0]
            self.assertEqual(len(study_bii_s_7['materials']['sources']), 29)
            self.assertEqual(len(study_bii_s_7['materials']['samples']), 29)
            self.assertEqual(len(study_bii_s_7['processSequence']), 29)
            self.assertListEqual(
                [a['filename'] for a in study_bii_s_7['assays']],
                ['a_matteo-assay-Gx.txt'])
            assay_gx = [a for a in study_bii_s_7['assays'] if
                        a['filename'] == 'a_matteo-assay-Gx.txt'][0]
            self.assertEqual(len(assay_gx['materials']['samples']), 29)
            self.assertEqual(len(assay_gx['materials']['otherMaterials']), 29)
            self.assertEqual(len(assay_gx['dataFiles']), 29)
            self.assertEqual(len(assay_gx['processSequence']), 116)