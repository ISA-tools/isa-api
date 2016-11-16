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

    @classmethod
    def setUpClass(cls):
        cls._tab_data_dir = utils.TAB_DATA_DIR
        cls._sra_data_dir = utils.SRA_DATA_DIR
        cls._sra_config_dir = utils.SRA2016_XML_CONFIGS_DATA_DIR

        cls._biis3_dir = os.path.join(cls._tab_data_dir, 'BII-S-3')
        cls._biis7_dir = os.path.join(cls._tab_data_dir, 'BII-S-7')

        cls._expected_submission_xml_biis3 = etree.parse(
            os.path.join(cls._sra_data_dir, 'BII-S-3', 'submission.xml')
        )
        cls._expected_project_set_xml_biis3 = etree.parse(
            os.path.join(cls._sra_data_dir, 'BII-S-3', 'project_set.xml')
        )
        cls._expected_sample_set_xml_biis3 = etree.parse(
            os.path.join(cls._sra_data_dir, 'BII-S-3', 'sample_set.xml')
        )
        cls._expected_experiment_set_xml_biis3 = etree.parse(
            os.path.join(cls._sra_data_dir, 'BII-S-3', 'experiment_set.xml')
        )
        cls._expected_run_set_xml_biis3 = etree.parse(
            os.path.join(cls._sra_data_dir, 'BII-S-3', 'run_set.xml')
        )
        cls._expected_submission_xml_biis7 = etree.parse(
            os.path.join(cls._sra_data_dir, 'BII-S-7', 'submission.xml')
        )
        cls._expected_project_set_xml_biis7 = etree.parse(
            os.path.join(cls._sra_data_dir, 'BII-S-7', 'project_set.xml')
        )
        cls._expected_sample_set_xml_biis7 = etree.parse(
            os.path.join(cls._sra_data_dir, 'BII-S-7', 'sample_set.xml')
        )
        cls._expected_experiment_set_xml_biis7 = etree.parse(
            os.path.join(cls._sra_data_dir, 'BII-S-7', 'experiment_set.xml')
        )
        cls._expected_run_set_xml_biis7 = etree.parse(
            os.path.join(cls._sra_data_dir, 'BII-S-7', 'run_set.xml')
        )

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_isatab2sra_zip_return(self):
        b = isatab2sra.convert(self._biis3_dir, self._tmp_dir, validate_first=False)
        self.assertIsInstance(b, BytesIO)
        with ZipFile(b) as zip_file:
            self.assertEqual(len(zip_file.namelist()), 5)

    def test_isatab2sra_dump_submission_xml_biis3(self):
        isatab2sra.convert(self._biis3_dir, self._tmp_dir, validate_first=False)
        actual_submission_xml_biis3 = etree.parse(os.path.join(self._tmp_dir, 'submission.xml'))
        self.assertTrue(utils.assert_xml_equal(self._expected_submission_xml_biis3, actual_submission_xml_biis3))

    def test_isatab2sra_dump_project_set_xml_biis3(self):
        isatab2sra.convert(self._biis3_dir, self._tmp_dir, validate_first=False)
        actual_project_set_xml_biis3 = etree.parse(os.path.join(self._tmp_dir, 'project_set.xml'))
        self.assertTrue(utils.assert_xml_equal(self._expected_project_set_xml_biis3, actual_project_set_xml_biis3))

    def test_isatab2sra_dump_sample_set_xml_biis3(self):
        isatab2sra.convert(self._biis3_dir, self._tmp_dir, validate_first=False)
        actual_sample_set_xml_biis3 = etree.parse(os.path.join(self._tmp_dir, 'sample_set.xml'))
        self.assertTrue(utils.assert_xml_equal(self._expected_sample_set_xml_biis3, actual_sample_set_xml_biis3))

    def test_isatab2sra_dump_experiment_set_xml_biis3(self):
        isatab2sra.convert(self._biis3_dir, self._tmp_dir, validate_first=False)
        actual_experiment_set_xml_biis3 = etree.parse(os.path.join(self._tmp_dir, 'experiment_set.xml'))
        self.assertTrue(utils.assert_xml_equal(self._expected_experiment_set_xml_biis3, actual_experiment_set_xml_biis3))

    def test_isatab2sra_dump_run_set_xml_biis3(self):
        isatab2sra.convert(self._biis3_dir, self._tmp_dir, validate_first=False)
        actual_run_set_xml_biis3 = etree.parse(os.path.join(self._tmp_dir, 'run_set.xml'))
        self.assertTrue(utils.assert_xml_equal(self._expected_run_set_xml_biis3, actual_run_set_xml_biis3))

    def test_isatab2sra_dump_submission_xml_biis7(self):
        sra_settings = {
            "sra_broker": "",
            "sra_center": "OXFORD",
            "sra_project": "OXFORD",
            "sra_lab": "Oxford e-Research Centre",
            "sra_broker_inform_on_status": "proccaserra@gmail.com",
            "sra_broker_inform_on_error": "proccaserra@gmail.com",
            "sra_broker_contact_name": "PRS"
        }
        isatab2sra.convert(self._biis3_dir, self._tmp_dir, sra_settings=sra_settings, validate_first=False)
        actual_submission_xml_biis7 = etree.parse(os.path.join(self._tmp_dir, 'submission.xml'))
        self.assertTrue(utils.assert_xml_equal(self._expected_submission_xml_biis7, actual_submission_xml_biis7))

    def test_isatab2sra_dump_project_set_xml_biis7(self):
        isatab2sra.convert(self._biis7_dir, self._tmp_dir, validate_first=False)
        actual_project_set_xml_biis7 = etree.parse(os.path.join(self._tmp_dir, 'project_set.xml'))
        self.assertTrue(utils.assert_xml_equal(self._expected_project_set_xml_biis7, actual_project_set_xml_biis7))

    def test_isatab2sra_dump_sample_set_xml_biis7(self):
        isatab2sra.convert(self._biis7_dir, self._tmp_dir, validate_first=False)
        actual_sample_set_xml_biis7 = etree.parse(os.path.join(self._tmp_dir, 'sample_set.xml'))
        self.assertTrue(utils.assert_xml_equal(self._expected_sample_set_xml_biis7, actual_sample_set_xml_biis7))

    def test_isatab2sra_dump_experiment_set_xml_biis7(self):
        isatab2sra.convert(self._biis7_dir, self._tmp_dir, validate_first=False)
        actual_experiment_set_xml_biis7 = etree.parse(os.path.join(self._tmp_dir, 'experiment_set.xml'))
        self.assertTrue(utils.assert_xml_equal(self._expected_experiment_set_xml_biis7, actual_experiment_set_xml_biis7))

    def test_isatab2sra_dump_run_set_xml_biis7(self):
        isatab2sra.convert(self._biis7_dir, self._tmp_dir, validate_first=False)
        actual_run_set_xml_biis7 = etree.parse(os.path.join(self._tmp_dir, 'run_set.xml'))
        self.assertTrue(utils.assert_xml_equal(self._expected_run_set_xml_biis7, actual_run_set_xml_biis7))
