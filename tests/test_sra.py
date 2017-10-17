"""Tests for exporting from ISA to SRA XML 1.5"""
import unittest
import os
import shutil
import tempfile
from lxml import etree

from isatools.tests import utils

from isatools import isajson
from isatools import sra


def setUpModule():
    if not os.path.exists(utils.DATA_DIR):
        raise FileNotFoundError(
            "Could not fine test data directory in {0}. Ensure you have cloned "
            "the ISAdatasets repository using "
            "git clone -b tests --single-branch "
            "git@github.com:ISA-tools/ISAdatasets {0}".format(utils.DATA_DIR))


class TestSraExport(unittest.TestCase):

    # TODO: Isolate testing SRA writer (don't rely on ISA JSON loader)

    def setUp(self):

        self._json_data_dir = utils.JSON_DATA_DIR
        self._sra_data_dir = utils.SRA_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

        study_id = 'BII-S-7'
        study_id_paired = 'BII-S-7'
        with open(os.path.join(self._json_data_dir, study_id,
                               study_id + '.json')) as json_fp:
            self._inv_obj = isajson.load(json_fp)

        with open(os.path.join(self._json_data_dir, study_id_paired,
                               study_id + '.json')) as json_fp:
            self._inv_obj = isajson.load(json_fp)

        self._study_sra_data_dir = os.path.join(self._sra_data_dir, study_id)
        with open(os.path.join(self._study_sra_data_dir, 'submission.xml'),
                  'rb') as sub_fp:
            self._expected_submission_xml_obj = etree.fromstring(sub_fp.read())
        with open(os.path.join(self._study_sra_data_dir, 'project_set.xml'),
                  'rb') as ps_fp:
            self._expected_project_set_xml_obj = etree.fromstring(ps_fp.read())
        with open(os.path.join(self._study_sra_data_dir, 'sample_set.xml'),
                  'rb') as ss_fp:
            self._expected_sample_set_xml_obj = etree.fromstring(ss_fp.read())
        with open(os.path.join(self._study_sra_data_dir, 'experiment_set.xml'),
                  'rb') as es_fp:
            self._expected_exp_set_xml_obj = etree.fromstring(es_fp.read())
        with open(os.path.join(self._study_sra_data_dir, 'run_set.xml'),
                  'rb') as rs_fp:
            self._expected_run_set_xml_obj = etree.fromstring(rs_fp.read())

        self._paired_study_sra_data_dir = os.path.join(
            self._sra_data_dir, study_id_paired)
        with open(os.path.join(
                self._paired_study_sra_data_dir, 'submission.xml'),
                'rb') as sub_fp:
            self._expected_submission_xml_obj_paired = etree.fromstring(
                sub_fp.read())
        with open(os.path.join(
                self._paired_study_sra_data_dir, 'project_set.xml'),
                'rb') as ps_fp:
            self._expected_project_set_xml_obj_paired = etree.fromstring(
                ps_fp.read())
        with open(os.path.join(
                self._paired_study_sra_data_dir, 'sample_set.xml'),
                'rb') as ss_fp:
            self._expected_sample_set_xml_obj_paired = etree.fromstring(
                ss_fp.read())
        with open(os.path.join(
                self._paired_study_sra_data_dir, 'experiment_set.xml'),
                'rb') as es_fp:
            self._expected_exp_set_xml_obj_paired = etree.fromstring(
                es_fp.read())
        with open(os.path.join(
                self._paired_study_sra_data_dir, 'run_set.xml'), 'rb') as rs_fp:
            self._expected_run_set_xml_obj_paired = etree.fromstring(
                rs_fp.read())

        self._sra_default_config = {
            "sra_broker": "",
            "sra_center": "OXFORD",
            "sra_project": "OXFORD",
            "sra_lab": "Oxford e-Research Centre",
            "sra_broker_inform_on_status": "proccaserra@gmail.com",
            "sra_broker_inform_on_error": "proccaserra@gmail.com",
            "sra_broker_contact_name": "PRS"
        }

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_sra_export_submission_xml(self):
        sra.export(self._inv_obj, self._tmp_dir,
                   sra_settings=self._sra_default_config)
        with open(os.path.join(self._tmp_dir, 'submission.xml'),
                  'rb') as out_fp:
            actual_submission_xml_obj = etree.fromstring(out_fp.read())
            self.assertTrue(
                utils.assert_xml_equal(self._expected_submission_xml_obj,
                                       actual_submission_xml_obj))

    def test_sra_export_sample_set_xml(self):
        sra.export(self._inv_obj, self._tmp_dir,
                   sra_settings=self._sra_default_config)
        with open(os.path.join(self._tmp_dir, 'sample_set.xml'),
                  'rb') as out_fp:
            actual_sample_set_xml_obj = etree.fromstring(out_fp.read())
            self.assertTrue(
                utils.assert_xml_equal(self._expected_sample_set_xml_obj,
                                       actual_sample_set_xml_obj))

    def test_sra_export_experiment_set_xml(self):
        sra.export(self._inv_obj, self._tmp_dir,
                   sra_settings=self._sra_default_config)
        with open(os.path.join(self._tmp_dir, 'experiment_set.xml'),
                  'rb') as out_fp:
            actual_exp_set_xml_obj = etree.fromstring(out_fp.read())
            self.assertTrue(
                utils.assert_xml_equal(self._expected_exp_set_xml_obj,
                                       actual_exp_set_xml_obj))

    def test_sra_export_run_set_xml(self):
        sra.export(self._inv_obj, self._tmp_dir,
                   sra_settings=self._sra_default_config)
        with open(os.path.join(self._tmp_dir, 'run_set.xml'), 'rb') as out_fp:
            actual_run_set_xml_obj = etree.fromstring(out_fp.read())
            self.assertTrue(
                utils.assert_xml_equal(self._expected_run_set_xml_obj,
                                       actual_run_set_xml_obj))

    def test_sra_export_project_set_xml(self):
        sra.export(self._inv_obj, self._tmp_dir,
                   sra_settings=self._sra_default_config)
        with open(os.path.join(self._tmp_dir, 'project_set.xml'),
                  'rb') as out_fp:
            actual_project_set_xml_obj = etree.fromstring(out_fp.read())
            self.assertTrue(
                utils.assert_xml_equal(self._expected_project_set_xml_obj,
                                       actual_project_set_xml_obj))

    def test_create_datafile_hashes_success(self):
        datafilehashes = sra.create_datafile_hashes(
            os.path.join(utils.TAB_DATA_DIR, 'BII-S-7'), ['1EU.sff'])
        self.assertEqual(datafilehashes['1EU.sff'],
                         'd41d8cd98f00b204e9800998ecf8427e')  # empty file hash

    def test_create_datafile_hashes_fail(self):
        with self.assertRaises(FileNotFoundError):
            sra.create_datafile_hashes(
                os.path.join(utils.TAB_DATA_DIR, 'BII-S-7'), ['1EU'])

    def test_spot_descriptor_injection(self):
        sra.export(self._inv_obj, self._tmp_dir,
                   sra_settings=self._sra_default_config)
        with open(os.path.join(self._tmp_dir, 'experiment_set.xml'),
                  'rb') as out_fp:
            self.assertTrue('<SPOT_DESCRIPTOR>' in str(out_fp.read()))


    def test_sra_paired_export_submission_xml(self):
        sra.export(self._inv_obj, self._tmp_dir,
                   sra_settings=self._sra_default_config)
        with open(os.path.join(self._tmp_dir, 'submission.xml'),
                  'rb') as out_fp:
            actual_submission_xml_obj = etree.fromstring(out_fp.read())
            self.assertTrue(
                utils.assert_xml_equal(self._expected_submission_xml_obj,
                                       actual_submission_xml_obj))

    def test_sra_paired_export_sample_set_xml(self):
        sra.export(self._inv_obj, self._tmp_dir,
                   sra_settings=self._sra_default_config)
        with open(os.path.join(self._tmp_dir, 'sample_set.xml'),
                  'rb') as out_fp:
            actual_sample_set_xml_obj = etree.fromstring(out_fp.read())
            self.assertTrue(
                utils.assert_xml_equal(self._expected_sample_set_xml_obj,
                                       actual_sample_set_xml_obj))

    def test_sra_paired_export_experiment_set_xml(self):
        sra.export(self._inv_obj, self._tmp_dir,
                   sra_settings=self._sra_default_config)
        with open(os.path.join(self._tmp_dir, 'experiment_set.xml'),
                  'rb') as out_fp:
            actual_exp_set_xml_obj = etree.fromstring(out_fp.read())
            self.assertTrue(
                utils.assert_xml_equal(self._expected_exp_set_xml_obj,
                                       actual_exp_set_xml_obj))

    def test_sra_paired_export_run_set_xml(self):
        sra.export(self._inv_obj, self._tmp_dir,
                   sra_settings=self._sra_default_config)
        with open(os.path.join(self._tmp_dir, 'run_set.xml'), 'rb') as out_fp:
            actual_run_set_xml_obj = etree.fromstring(out_fp.read())
            self.assertTrue(
                utils.assert_xml_equal(self._expected_run_set_xml_obj,
                                       actual_run_set_xml_obj))

    def test_sra_paired_export_project_set_xml(self):
        sra.export(self._inv_obj, self._tmp_dir,
                   sra_settings=self._sra_default_config)
        with open(os.path.join(self._tmp_dir, 'project_set.xml'),
                  'rb') as out_fp:
            actual_project_set_xml_obj = etree.fromstring(out_fp.read())
            self.assertTrue(
                utils.assert_xml_equal(self._expected_project_set_xml_obj,
                                       actual_project_set_xml_obj))