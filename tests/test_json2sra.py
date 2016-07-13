from unittest import TestCase
import os
import shutil
from isatools.convert import json2sra
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class JsonToSraTest(TestCase):

    def setUp(self):
        self._dir = os.path.join(os.path.dirname(__file__), "data")
        self._config_dir = os.path.join(self._dir, "Configurations/isaconfig-default_v2015-07-02")
        self._tmp = os.path.join(self._dir, './tmp/')
        if not os.path.exists(self._tmp):
            os.mkdir(self._tmp)

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_json_to_sra_bii_s_3(self):
        work_dir = os.path.join(self._tmp, 'sra', 'BII-S-3')
        json2sra.convert(open(os.path.join(self._dir, 'BII-S-3', 'BII-S-3.json')), self._tmp, self._config_dir)
        self.assertTrue(os.path.exists(os.path.join(self._tmp, 'sra')))

        # SRA should always produce experiment_set.xml, run_set.xml, sample_set.xml study.xml and submission.xml
        expected_sra_path = os.path.join(self._tmp, 'sra', 'BII-S-3')
        expected_file_set = {'experiment_set.xml', 'run_set.xml', 'sample_set.xml', 'study.xml', 'submission.xml'}
        if os.path.exists(expected_sra_path):
            sra_output_files_list = set(os.listdir(expected_sra_path))
            extra_files_found = sra_output_files_list - expected_file_set
            if len(extra_files_found) > 0:
                self.fail("Unexpected file found in SRA output: " + str(extra_files_found))
            expected_files_missing = expected_file_set - sra_output_files_list
            if len(expected_files_missing) > 0:
                self.fail("Unexpected file found in SRA output: " + str(expected_files_missing))
            # Now try load the SRA output in test and compare against the expected output in test data directory
            from lxml import objectify, etree

            # compare experiment_set.xml
            test_experiment_set_file = open(os.path.join(expected_sra_path, 'experiment_set.xml'), 'rb')
            logger.info("Opening: " + test_experiment_set_file.name)
            test_experiment_set_xml_obj = objectify.fromstring(test_experiment_set_file.read())
            expected_experiment_set_file = open(os.path.join(work_dir, 'experiment_set.xml'), 'rb')
            logger.info("Opening: " + expected_experiment_set_file.name)
            expected_experiment_set_xml_obj = objectify.fromstring(expected_experiment_set_file.read())
            logger.info("Comparing output of SRA conversion to expected test data...")
            self.assertEqual(etree.tostring(test_experiment_set_xml_obj),
                             etree.tostring(expected_experiment_set_xml_obj))

            # compare run_set.xml
            test_run_set_file = open(os.path.join(expected_sra_path, 'run_set.xml'), 'rb')
            logger.info("Opening: " + test_run_set_file.name)
            test_run_set_xml_obj = objectify.fromstring(test_run_set_file.read())
            expected_run_set_file = open(os.path.join(work_dir, 'run_set.xml'), 'rb')
            logger.info("Opening: " + expected_run_set_file.name)
            expected_run_set_xml_obj = objectify.fromstring(expected_run_set_file.read())
            logger.info("Comparing output of SRA conversion to expected test data...")
            self.assertEqual(etree.tostring(test_run_set_xml_obj), etree.tostring(expected_run_set_xml_obj))

            # compare sample_set.xml
            test_sample_set_file = open(os.path.join(expected_sra_path, 'sample_set.xml'), 'rb')
            logger.info("Opening: " + test_sample_set_file.name)
            test_sample_set_xml_obj = objectify.fromstring(test_sample_set_file.read())
            expected_sample_set_file = open(os.path.join(work_dir, 'sample_set.xml'), 'rb')
            logger.info("Opening: " + expected_sample_set_file.name)
            expected_sample_set_xml_obj = objectify.fromstring(expected_sample_set_file.read())
            logger.info("Comparing output of SRA conversion to expected test data...")
            self.assertEqual(etree.tostring(test_sample_set_xml_obj), etree.tostring(expected_sample_set_xml_obj))

            # compare study.xml
            test_study_file = open(os.path.join(expected_sra_path, 'study.xml'), 'rb')
            logger.info("Opening: " + test_study_file.name)
            test_study_xml_obj = objectify.fromstring(test_study_file.read())
            expected_study_file = open(os.path.join(work_dir, 'study.xml'), 'rb')
            logger.info("Opening: " + expected_study_file.name)
            expected_study_xml_obj = objectify.fromstring(expected_study_file.read())
            logger.info("Comparing output of SRA conversion to expected test data...")
            self.assertEqual(etree.tostring(test_study_xml_obj), etree.tostring(expected_study_xml_obj))

            # compare submission.xml
            test_submission_file = open(os.path.join(expected_sra_path, 'submission.xml'), 'rb')
            logger.info("Opening: " + test_submission_file.name)
            test_submission_xml_obj = objectify.fromstring(test_submission_file.read())
            expected_submission_file = open(os.path.join(work_dir, 'submission.xml'), 'rb')
            logger.info("Opening: " + expected_submission_file.name)
            expected_submission_xml_obj = objectify.fromstring(expected_submission_file.read())
            logger.info("Comparing output of SRA conversion to expected test data...")
            self.assertEqual(etree.tostring(test_submission_xml_obj), etree.tostring(expected_submission_xml_obj))

    def test_json_to_sra_bii_s_7(self):
        work_dir = os.path.join(self._tmp, 'sra', 'BII-S-7')
        json2sra.convert(open(os.path.join(self._dir, 'BII-S-7/BII-S-7.json')), self._tmp, self._config_dir)
        self.assertTrue(os.path.exists(os.path.join(self._tmp, 'sra')))

        # SRA should always produce experiment_set.xml, run_set.xml, sample_set.xml study.xml and submission.xml
        expected_sra_path = os.path.join(self._tmp, 'sra', 'BII-S-7')
        expected_file_set = {'experiment_set.xml', 'run_set.xml', 'sample_set.xml', 'study.xml', 'submission.xml'}
        if os.path.exists(expected_sra_path):
            sra_output_files_list = set(os.listdir(expected_sra_path))
            extra_files_found = sra_output_files_list - expected_file_set
            if len(extra_files_found) > 0:
                self.fail("Unexpected file found in SRA output: " + str(extra_files_found))
            expected_files_missing = expected_file_set - sra_output_files_list
            if len(expected_files_missing) > 0:
                self.fail("Unexpected file found in SRA output: " + str(expected_files_missing))
            # Now try load the SRA output in test and compare against the expected output in test data directory
            from lxml import objectify, etree

            # compare experiment_set.xml
            test_experiment_set_file = open(os.path.join(expected_sra_path, 'experiment_set.xml'), 'rb')
            logger.info("Opening: " + test_experiment_set_file.name)
            test_experiment_set_xml_obj = objectify.fromstring(test_experiment_set_file.read())
            expected_experiment_set_file = open(os.path.join(work_dir, 'experiment_set.xml'), 'rb')
            logger.info("Opening: " + expected_experiment_set_file.name)
            expected_experiment_set_xml_obj = objectify.fromstring(expected_experiment_set_file.read())
            logger.info("Comparing output of SRA conversion to expected test data...")
            self.assertEqual(etree.tostring(test_experiment_set_xml_obj),
                             etree.tostring(expected_experiment_set_xml_obj))

            # compare run_set.xml
            test_run_set_file = open(os.path.join(expected_sra_path, 'run_set.xml'), 'rb')
            logger.info("Opening: " + test_run_set_file.name)
            test_run_set_xml_obj = objectify.fromstring(test_run_set_file.read())
            expected_run_set_file = open(os.path.join(work_dir, 'run_set.xml'), 'rb')
            logger.info("Opening: " + expected_run_set_file.name)
            expected_run_set_xml_obj = objectify.fromstring(expected_run_set_file.read())
            logger.info("Comparing output of SRA conversion to expected test data...")
            self.assertEqual(etree.tostring(test_run_set_xml_obj), etree.tostring(expected_run_set_xml_obj))

            # compare sample_set.xml
            test_sample_set_file = open(os.path.join(expected_sra_path, 'sample_set.xml'), 'rb')
            logger.info("Opening: " + test_sample_set_file.name)
            test_sample_set_xml_obj = objectify.fromstring(test_sample_set_file.read())
            expected_sample_set_file = open(os.path.join(work_dir, 'sample_set.xml'), 'rb')
            logger.info("Opening: " + expected_sample_set_file.name)
            expected_sample_set_xml_obj = objectify.fromstring(expected_sample_set_file.read())
            logger.info("Comparing output of SRA conversion to expected test data...")
            self.assertEqual(etree.tostring(test_sample_set_xml_obj), etree.tostring(expected_sample_set_xml_obj))

            # compare study.xml
            test_study_file = open(os.path.join(expected_sra_path, 'study.xml'), 'rb')
            logger.info("Opening: " + test_study_file.name)
            test_study_xml_obj = objectify.fromstring(test_study_file.read())
            expected_study_file = open(os.path.join(work_dir, 'study.xml'), 'rb')
            logger.info("Opening: " + expected_study_file.name)
            expected_study_xml_obj = objectify.fromstring(expected_study_file.read())
            logger.info("Comparing output of SRA conversion to expected test data...")
            self.assertEqual(etree.tostring(test_study_xml_obj), etree.tostring(expected_study_xml_obj))

            # compare submission.xml
            test_submission_file = open(os.path.join(expected_sra_path, 'submission.xml'), 'rb')
            logger.info("Opening: " + test_submission_file.name)
            test_submission_xml_obj = objectify.fromstring(test_submission_file.read())
            expected_submission_file = open(os.path.join(work_dir, 'submission.xml'), 'rb')
            logger.info("Opening: " + expected_submission_file.name)
            expected_submission_xml_obj = objectify.fromstring(expected_submission_file.read())
            logger.info("Comparing output of SRA conversion to expected test data...")
            self.assertEqual(etree.tostring(test_submission_xml_obj), etree.tostring(expected_submission_xml_obj))