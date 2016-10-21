# coding: utf-8
import os
import unittest
from six import BytesIO
from zipfile import ZipFile
import shutil
from lxml import etree
import tempfile

from isatools.convert import isatab2sra
from tests import utils


class TestIsaTab2Sra(unittest.TestCase):

    def setUp(self):
        self._tab_data_dir = utils.TAB_DATA_DIR
        self._sra_data_dir = utils.SRA_DATA_DIR
        self._sra_config_dir = utils.SRA2016_XML_CONFIGS_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

        self._biis3_dir = os.path.join(self._tab_data_dir, 'BII-S-3')
        self._biis7_dir = os.path.join(self._tab_data_dir, 'BII-S-7')

        # self._expected_submission_xml_biis3 = etree.fromstring(
        #     open(os.path.join(self._sra_data_dir, 'BII-S-3', 'submission.xml'), 'rb').read())
        self._expected_submission_xml_biis3 = etree.parse(
            os.path.join(self._sra_data_dir, 'BII-S-3', 'submission.xml')
        )
        # self._expected_project_set_xml_biis3 = etree.fromstring(
        #     open(os.path.join(self._sra_data_dir, 'BII-S-3', 'project_set.xml'), 'rb').read())
        self._expected_project_set_xml_biis3 = etree.parse(
            os.path.join(self._sra_data_dir, 'BII-S-3', 'project_set.xml')
        )
        # self._expected_sample_set_xml_biis3 = etree.fromstring(
        #     open(os.path.join(self._sra_data_dir, 'BII-S-3', 'sample_set.xml'), 'rb').read())
        self._expected_sample_set_xml_biis3 = etree.parse(
            os.path.join(self._sra_data_dir, 'BII-S-3', 'sample_set.xml')
        )
        # self._expected_experiment_set_xml_biis3 = etree.fromstring(
        #     open(os.path.join(self._sra_data_dir, 'BII-S-3', 'experiment_set.xml'), 'rb').read())
        self._expected_experiment_set_xml_biis3 = etree.parse(
            os.path.join(self._sra_data_dir, 'BII-S-3', 'experiment_set.xml')
        )
        # self._expected_run_set_xml_biis3 = etree.fromstring(
        #     open(os.path.join(self._sra_data_dir, 'BII-S-3', 'run_set.xml'), 'rb').read())
        self._expected_run_set_xml_biis3 = etree.parse(
            os.path.join(self._sra_data_dir, 'BII-S-3', 'run_set.xml')
        )
        # self._expected_submission_xml_biis7 = etree.fromstring(
        #     open(os.path.join(self._sra_data_dir, 'BII-S-7', 'submission.xml'), 'rb').read())
        self._expected_submission_xml_biis7 = etree.parse(
            os.path.join(self._sra_data_dir, 'BII-S-7', 'submission.xml')
        )
        # self._expected_project_set_xml_biis7 = etree.fromstring(
        #     open(os.path.join(self._sra_data_dir, 'BII-S-7', 'project_set.xml'), 'rb').read())
        self._expected_project_set_xml_biis7 = etree.parse(
            os.path.join(self._sra_data_dir, 'BII-S-7', 'project_set.xml')
        )
        # self._expected_sample_set_xml_biis7 = etree.fromstring(
        #     open(os.path.join(self._sra_data_dir, 'BII-S-7', 'sample_set.xml'), 'rb').read())
        self._expected_sample_set_xml_biis7 = etree.parse(
            os.path.join(self._sra_data_dir, 'BII-S-7', 'sample_set.xml')
        )
        # self._expected_experiment_set_xml_biis7 = etree.fromstring(
        #     open(os.path.join(self._sra_data_dir, 'BII-S-7', 'experiment_set.xml'), 'rb').read())
        self._expected_experiment_set_xml_biis7 = etree.parse(
            os.path.join(self._sra_data_dir, 'BII-S-7', 'experiment_set.xml')
        )
        # self._expected_run_set_xml_biis7 = etree.fromstring(
        #     open(os.path.join(self._sra_data_dir, 'BII-S-7', 'run_set.xml'), 'rb').read())
        self._expected_run_set_xml_biis7 = etree.parse(
            os.path.join(self._sra_data_dir, 'BII-S-7', 'run_set.xml')
        )

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab2sra_zip_return(self):
        b = isatab2sra.convert(self._biis3_dir, self._tmp_dir, validate_first=False)
        self.assertIsInstance(b, BytesIO)
        with ZipFile(b) as zip_file:
            self.assertEqual(len(zip_file.namelist()), 5)

    def test_isatab2sra_dump_submission_xml_biis3(self):
        isatab2sra.convert(self._biis3_dir, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 'submission.xml'), 'rb') as xml_file:
            submission_xml = xml_file.read()
        actual_submission_xml_biis3 = etree.fromstring(submission_xml)
        self.assertTrue(utils.assert_xml_equal(self._expected_submission_xml_biis3, actual_submission_xml_biis3))

    def test_isatab2sra_dump_project_set_xml_biis3(self):
        isatab2sra.convert(self._biis3_dir, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 'project_set.xml'), 'rb') as xml_file:
            project_set_xml = xml_file.read()
        actual_project_set_xml_biis3 = etree.fromstring(project_set_xml)
        self.assertTrue(utils.assert_xml_equal(self._expected_project_set_xml_biis3, actual_project_set_xml_biis3))

    def test_isatab2sra_dump_sample_set_xml_biis3(self):
        isatab2sra.convert(self._biis3_dir, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 'sample_set.xml'), 'rb') as xml_file:
            sample_set_xml = xml_file.read()
        actual_sample_set_xml_biis3 = etree.fromstring(sample_set_xml)
        self.assertTrue(utils.assert_xml_equal(self._expected_sample_set_xml_biis3, actual_sample_set_xml_biis3))

    def test_iatab2sra_dump_experiment_set_xml_biis3(self):
        isatab2sra.convert(self._biis3_dir, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 'experiment_set.xml'), 'rb') as xml_file:
            experiment_set_xml = xml_file.read()
        actual_experiment_set_xml_biis3 = etree.fromstring(experiment_set_xml)
        self.assertTrue(utils.assert_xml_equal(self._expected_experiment_set_xml_biis3, actual_experiment_set_xml_biis3))

    def test_isatab2sra_dump_run_set_xml_biis3(self):
        isatab2sra.convert(self._biis3_dir, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 'run_set.xml'), 'rb') as xml_file:
            run_set_xml = xml_file.read()
        actual_run_set_xml_biis3 = etree.fromstring(run_set_xml)
        self.assertTrue(utils.assert_xml_equal(self._expected_run_set_xml_biis3, actual_run_set_xml_biis3))

    def test_isatab2sra_dump_submission_xml_biis7(self):
        isatab2sra.convert(self._biis3_dir, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 'submission.xml'), 'rb') as xml_file:
            submission_xml = xml_file.read()
        actual_submission_xml_biis7 = etree.fromstring(submission_xml)
        self.assertTrue(utils.assert_xml_equal(self._expected_submission_xml_biis7, actual_submission_xml_biis7))

    def test_isatab2sra_dump_project_set_xml_biis7(self):
        isatab2sra.convert(self._biis7_dir, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 'project_set.xml'), 'rb') as xml_file:
            project_set_xml = xml_file.read()
        actual_project_set_xml_biis7 = etree.fromstring(project_set_xml)
        self.assertTrue(utils.assert_xml_equal(self._expected_project_set_xml_biis7, actual_project_set_xml_biis7))

    def test_isatab2sra_dump_sample_set_xml_biis7(self):
        isatab2sra.convert(self._biis7_dir, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 'sample_set.xml'), 'rb') as xml_file:
            sample_set_xml = xml_file.read()
        actual_sample_set_xml_biis7 = etree.fromstring(sample_set_xml)
        self.assertTrue(utils.assert_xml_equal(self._expected_sample_set_xml_biis7, actual_sample_set_xml_biis7))

    def test_isatab2sra_dump_experiment_set_xml_biis7(self):
        isatab2sra.convert(self._biis7_dir, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 'experiment_set.xml'), 'rb') as xml_file:
            experiment_set_xml = xml_file.read()
        actual_experiment_set_xml_biis7 = etree.fromstring(experiment_set_xml)
        self.assertTrue(utils.assert_xml_equal(self._expected_experiment_set_xml_biis7, actual_experiment_set_xml_biis7))

    def test_isatab2sra_dump_run_set_xml_biis7(self):
        isatab2sra.convert(self._biis7_dir, self._tmp_dir, validate_first=False)
        with open(os.path.join(self._tmp_dir, 'run_set.xml'), 'rb') as xml_file:
            run_set_xml = xml_file.read()
        actual_run_set_xml_biis7 = etree.fromstring(run_set_xml)
        self.assertTrue(utils.assert_xml_equal(self._expected_run_set_xml_biis7, actual_run_set_xml_biis7))
