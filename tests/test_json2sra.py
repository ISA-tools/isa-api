from unittest import TestCase
import os
import shutil
from isatools.convert import json2sra
from lxml import etree


class TestJsonToSra(TestCase):

    def setUp(self):
        self._sra_data_dir = os.path.join(os.path.dirname(__file__), 'data', 'sra')
        self._sra_configs_dir = os.path.join(os.path.dirname(__file__), 'data', 'configs', 'xml', 'i'
                                                                                                  'saconfig-default_v2015-07-02')
        self._json_data_dir = os.path.join(os.path.dirname(__file__), 'data', 'json')
        self._tmp_dir = os.path.join(os.path.join(os.path.dirname(__file__), './tmp/'))

        if not os.path.exists(self._tmp_dir):
            os.mkdir(self._tmp_dir)

        self._expected_submission_xml_biis3 = etree.fromstring(open(os.path.join(self._sra_data_dir, 'BII-S-3', 'submission.xml'), 'rb').read())
        self._expected_study_xml_biis3 = etree.fromstring(open(os.path.join(self._sra_data_dir, 'BII-S-3', 'study.xml'), 'rb').read())
        self._expected_sample_set_xml_biis3 = etree.fromstring(open(os.path.join(self._sra_data_dir, 'BII-S-3', 'sample_set.xml'), 'rb').read())
        self._expected_experiment_set_xml_biis3 = etree.fromstring(open(os.path.join(self._sra_data_dir, 'BII-S-3', 'experiment_set.xml'), 'rb').read())
        self._expected_run_set_xml_biis3 = etree.fromstring(open(os.path.join(self._sra_data_dir, 'BII-S-3', 'run_set.xml'), 'rb').read())

        self._expected_submission_xml_biis7 = etree.fromstring(open(os.path.join(self._sra_data_dir, 'BII-S-7', 'submission.xml'), 'rb').read())
        self._expected_study_xml_biis7 = etree.fromstring(open(os.path.join(self._sra_data_dir, 'BII-S-7', 'study.xml'), 'rb').read())
        self._expected_sample_set_xml_biis7 = etree.fromstring(open(os.path.join(self._sra_data_dir, 'BII-S-7', 'sample_set.xml'), 'rb').read())
        self._expected_experiment_set_xml_biis7 = etree.fromstring(open(os.path.join(self._sra_data_dir, 'BII-S-7', 'experiment_set.xml'), 'rb').read())
        self._expected_run_set_xml_biis7 = etree.fromstring(open(os.path.join(self._sra_data_dir, 'BII-S-7', 'run_set.xml'), 'rb').read())

        self._sra_default_config = {
            "broker_name": "",
            "center_name": "OXFORD",
            "center_project_name": "OXFORD",
            "lab_name": "Oxford e-Research Centre",
            "submission_action": "ADD",
            "funding_agency": "None",
            "grant_number": "None",
            "inform_on_status_name": "Philippe Rocca-Serra",
            "inform_on_status_email": "proccaserra@gmail.com",
            "inform_on_error_name:": "Philippe Rocca-Serra",
            "inform_on_error_email": "proccaserra@gmail.com"
        }

    def tearDown(self):
        shutil.rmtree(self._tmp_dir, ignore_errors=True)
        # pass

    def test_sra_dump_dir_exists(self):
        json2sra.convert(open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')), self._tmp_dir,
                         self._sra_configs_dir)
        self.assertTrue(os.path.exists(os.path.join(self._tmp_dir, 'sra')))

    def test_sra_dump_file_set(self):
        json2sra.convert(open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')), self._tmp_dir,
                         self._sra_configs_dir)
        # SRA should always produce experiment_set.xml, run_set.xml, sample_set.xml study.xml and submission.xml
        expected_sra_path = os.path.join(self._tmp_dir, 'sra', 'BII-S-3')
        expected_file_set = {'experiment_set.xml', 'run_set.xml', 'sample_set.xml', 'study.xml', 'submission.xml'}
        if os.path.exists(expected_sra_path):
            actual_file_set = set(os.listdir(expected_sra_path))
            extra_files_found = actual_file_set - expected_file_set
            if len(extra_files_found) > 0:
                self.fail("Unexpected file found in SRA output: " + str(extra_files_found))
            expected_files_missing = expected_file_set - actual_file_set
            if len(expected_files_missing) > 0:
                self.fail("Unexpected file found in SRA output: " + str(expected_files_missing))
        
    def test_sra_dump_submission_xml_biis3(self):
        json2sra.convert(open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')), self._tmp_dir, self._sra_configs_dir)
        # Now try load the SRA output in test and compare against the expected output in test data directory
        submission_xml = open(os.path.join(self._tmp_dir, 'sra', 'BII-S-3', 'submission.xml'), 'rb').read()
        actual_submission_xml_biis3 = etree.fromstring(submission_xml)
        # count tags
        self.assertEqual(self._expected_submission_xml_biis3.xpath('count(//SUBMISSION)'), actual_submission_xml_biis3.xpath('count(//SUBMISSION)'))
        self.assertEqual(self._expected_submission_xml_biis3.xpath('count(//CONTACTS)'), actual_submission_xml_biis3.xpath('count(//CONTACTS)'))
        self.assertEqual(self._expected_submission_xml_biis3.xpath('count(//CONTACT)'), actual_submission_xml_biis3.xpath('count(//CONTACT)'))
        self.assertEqual(self._expected_submission_xml_biis3.xpath('count(//ACTIONS)'), actual_submission_xml_biis3.xpath('count(//ACTIONS)'))
        self.assertEqual(self._expected_submission_xml_biis3.xpath('count(//ACTION)'), actual_submission_xml_biis3.xpath('count(//ACTION)'))
        self.assertEqual(self._expected_submission_xml_biis3.xpath('count(//ADD)'), actual_submission_xml_biis3.xpath('count(//ADD)'))
        
    def test_sra_dump_study_xml_biis3(self):
        json2sra.convert(open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')), self._tmp_dir,
                         self._sra_configs_dir)
        # Now try load the SRA output in test and compare against the expected output in test data directory
        study_xml = open(os.path.join(self._tmp_dir, 'sra', 'BII-S-3', 'study.xml'), 'rb').read()
        actual_study_xml_biis3 = etree.fromstring(study_xml)
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//STUDY)'),
                         actual_study_xml_biis3.xpath('count(//STUDY)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//DESCRIPTOR)'),
                         actual_study_xml_biis3.xpath('count(//DESCRIPTOR)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//CENTER_NAME)'),
                         actual_study_xml_biis3.xpath('count(//CENTER_NAME)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//CENTER_PROJECT_NAME)'),
                         actual_study_xml_biis3.xpath('count(//CENTER_PROJECT_NAME)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//STUDY_TITLE)'),
                         actual_study_xml_biis3.xpath('count(//STUDY_TITLE)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//STUDY_DESCRIPTION)'),
                         actual_study_xml_biis3.xpath('count(//STUDY_DESCRIPTION)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//STUDY_TYPE)'),
                         actual_study_xml_biis3.xpath('count(//STUDY_TYPE)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//STUDY_LINKS)'),
                         actual_study_xml_biis3.xpath('count(//STUDY_LINKS)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//STUDY_LINK)'),
                         actual_study_xml_biis3.xpath('count(//STUDY_LINK)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//ENTREZ_LINK)'),
                         actual_study_xml_biis3.xpath('count(//ENTREZ_LINK)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//DB)'), actual_study_xml_biis3.xpath('count(//DB)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//ID)'), actual_study_xml_biis3.xpath('count(//ID)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//STUDY_ATTRIBUTES)'),
                         actual_study_xml_biis3.xpath('count(//STUDY_ATTRIBUTES)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//STUDY_ATTRIBUTE)'),
                         actual_study_xml_biis3.xpath('count(//STUDY_ATTRIBUTE)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//TAG)'), actual_study_xml_biis3.xpath('count(//TAG)'))
        self.assertEqual(self._expected_study_xml_biis3.xpath('count(//VALUE)'),
                         actual_study_xml_biis3.xpath('count(//VALUE)'))

    def test_sra_dump_sample_set_xml_biis3(self):
        json2sra.convert(open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')), self._tmp_dir,
                         self._sra_configs_dir)
        # Now try load the SRA output in test and compare against the expected output in test data directory
        sample_set_xml = open(os.path.join(self._tmp_dir, 'sra', 'BII-S-3', 'sample_set.xml'), 'rb').read()
        actual_sample_set_xml_biis3 = etree.fromstring(sample_set_xml)
        self.assertEqual(self._expected_sample_set_xml_biis3.xpath('count(//SAMPLE_SET)'),
                         actual_sample_set_xml_biis3.xpath('count(//SAMPLE_SET)'))
        self.assertEqual(self._expected_sample_set_xml_biis3.xpath('count(//SAMPLE)'),
                         actual_sample_set_xml_biis3.xpath('count(//SAMPLE)'))
        self.assertEqual(self._expected_sample_set_xml_biis3.xpath('count(//TITLE)'),
                         actual_sample_set_xml_biis3.xpath('count(//TITLE)'))
        self.assertEqual(self._expected_sample_set_xml_biis3.xpath('count(//SAMPLE_NAME)'),
                         actual_sample_set_xml_biis3.xpath('count(//SAMPLE_NAME)'))
        self.assertEqual(self._expected_sample_set_xml_biis3.xpath('count(//TAXON_ID)'),
                         actual_sample_set_xml_biis3.xpath('count(//TAXON_ID)'))
        self.assertEqual(self._expected_sample_set_xml_biis3.xpath('count(//SCIENTIFIC_NAME)'),
                         actual_sample_set_xml_biis3.xpath('count(//SCIENTIFIC_NAME)'))
        self.assertEqual(self._expected_sample_set_xml_biis3.xpath('count(//SAMPLE_ATTRIBUTES)'),
                         actual_sample_set_xml_biis3.xpath('count(//SAMPLE_ATTRIBUTES)'))
        self.assertEqual(self._expected_sample_set_xml_biis3.xpath('count(//SAMPLE_ATTRIBUTE)'),
                         actual_sample_set_xml_biis3.xpath('count(//SAMPLE_ATTRIBUTE)'))
        self.assertEqual(self._expected_sample_set_xml_biis3.xpath('count(//TAG)'),
                         actual_sample_set_xml_biis3.xpath('count(//TAG)'))
        self.assertEqual(self._expected_sample_set_xml_biis3.xpath('count(//VALUE)'),
                         actual_sample_set_xml_biis3.xpath('count(//VALUE)'))
        self.assertEqual(self._expected_sample_set_xml_biis3.xpath('count(//UNITS)'),
                         actual_sample_set_xml_biis3.xpath('count(//UNITS)'))

    def test_sra_dump_experiment_set_xml_biis3(self):
        json2sra.convert(open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')), self._tmp_dir,
                         self._sra_configs_dir)
        # Now try load the SRA output in test and compare against the expected output in test data directory
        experiment_set_xml = open(os.path.join(self._tmp_dir, 'sra', 'BII-S-3', 'experiment_set.xml'), 'rb').read()
        actual_experiment_set_xml_biis3 = etree.fromstring(experiment_set_xml)
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//EXPERIMENT_SET)'),
                         actual_experiment_set_xml_biis3.xpath('count(//EXPERIMENT_SET)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//EXPERIMENT)'),
                         actual_experiment_set_xml_biis3.xpath('count(//EXPERIMENT)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//TITLE)'),
                         actual_experiment_set_xml_biis3.xpath('count(//TITLE)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//STUDY_REF)'),
                         actual_experiment_set_xml_biis3.xpath('count(//STUDY_REF)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//DESIGN)'),
                         actual_experiment_set_xml_biis3.xpath('count(//DESIGN)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//DESIGN_DESCRIPTION)'),
                         actual_experiment_set_xml_biis3.xpath('count(//DESIGN_DESCRIPTION)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//SAMPLE_DESCRIPTOR)'),
                         actual_experiment_set_xml_biis3.xpath('count(//SAMPLE_DESCRIPTOR)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//LIBRARY_DESCRIPTOR)'),
                         actual_experiment_set_xml_biis3.xpath('count(//LIBRARY_DESCRIPTOR)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//LIBRARY_NAME)'),
                         actual_experiment_set_xml_biis3.xpath('count(//LIBRARY_NAME)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//LIBRARY_STRATEGY)'),
                         actual_experiment_set_xml_biis3.xpath('count(//LIBRARY_STRATEGY)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//LIBRARY_SOURCE)'),
                         actual_experiment_set_xml_biis3.xpath('count(//LIBRARY_SOURCE)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//LIBRARY_SELECTION)'),
                         actual_experiment_set_xml_biis3.xpath('count(//LIBRARY_SELECTION)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//LIBRARY_LAYOUT)'),
                         actual_experiment_set_xml_biis3.xpath('count(//LIBRARY_LAYOUT)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//SINGLE)'),
                         actual_experiment_set_xml_biis3.xpath('count(//SINGLE)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//TARGETED_LOCI)'),
                         actual_experiment_set_xml_biis3.xpath('count(//TARGETED_LOCI)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//LOCUS)'),
                         actual_experiment_set_xml_biis3.xpath('count(//LOCUS)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//POOLING_STRATEGY)'),
                         actual_experiment_set_xml_biis3.xpath('count(//POOLING_STRATEGY)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//LIBRARY_CONSTRUCTION_PROTOCOL)'),
                         actual_experiment_set_xml_biis3.xpath('count(//LIBRARY_CONSTRUCTION_PROTOCOL)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//SPOT_DESCRIPTOR)'),
                         actual_experiment_set_xml_biis3.xpath('count(//SPOT_DESCRIPTOR)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//SPOT_DECODE_SPEC)'),
                         actual_experiment_set_xml_biis3.xpath('count(//SPOT_DECODE_SPEC)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//READ_SPEC)'),
                         actual_experiment_set_xml_biis3.xpath('count(//READ_SPEC)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//READ_INDEX)'),
                         actual_experiment_set_xml_biis3.xpath('count(//READ_INDEX)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//READ_CLASS)'),
                         actual_experiment_set_xml_biis3.xpath('count(//READ_CLASS)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//READ_TYPE)'),
                         actual_experiment_set_xml_biis3.xpath('count(//READ_TYPE)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//BASE_COORD)'),
                         actual_experiment_set_xml_biis3.xpath('count(//BASE_COORD)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//READ_INDEX)'),
                         actual_experiment_set_xml_biis3.xpath('count(//READ_INDEX)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//EXPECTED_BASECALL_TABLE)'),
                         actual_experiment_set_xml_biis3.xpath('count(//EXPECTED_BASECALL_TABLE)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//BASECALL)'),
                         actual_experiment_set_xml_biis3.xpath('count(//BASECALL)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//RELATIVE_ORDER)'),
                         actual_experiment_set_xml_biis3.xpath('count(//RELATIVE_ORDER)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//PLATFORM)'),
                         actual_experiment_set_xml_biis3.xpath('count(//PLATFORM)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//LS454)'),
                         actual_experiment_set_xml_biis3.xpath('count(//LS454)'))
        self.assertEqual(self._expected_experiment_set_xml_biis3.xpath('count(//INSTRUMENT_MODEL)'),
                         actual_experiment_set_xml_biis3.xpath('count(//INSTRUMENT_MODEL)'))

    def test_sra_dump_run_set_xml_biis3(self):
        json2sra.convert(open(os.path.join(self._json_data_dir, 'BII-S-3', 'BII-S-3.json')), self._tmp_dir,
                         self._sra_configs_dir)
        # Now try load the SRA output in test and compare against the expected output in test data directory
        run_set_xml = open(os.path.join(self._tmp_dir, 'sra', 'BII-S-3', 'run_set.xml'), 'rb').read()
        actual_run_set_xml_biis3 = etree.fromstring(run_set_xml)
        self.assertEqual(self._expected_run_set_xml_biis3.xpath('count(//RUN_SET)'),
                         actual_run_set_xml_biis3.xpath('count(//RUN_SET)'))
        self.assertEqual(self._expected_run_set_xml_biis3.xpath('count(//RUN)'),
                         actual_run_set_xml_biis3.xpath('count(//RUN)'))
        self.assertEqual(self._expected_run_set_xml_biis3.xpath('count(//EXPERIMENT_REF)'),
                         actual_run_set_xml_biis3.xpath('count(//EXPERIMENT_REF)'))
        self.assertEqual(self._expected_run_set_xml_biis3.xpath('count(//DATA_BLOCK)'),
                         actual_run_set_xml_biis3.xpath('count(//DATA_BLOCK)'))
        self.assertEqual(self._expected_run_set_xml_biis3.xpath('count(//FILES)'),
                         actual_run_set_xml_biis3.xpath('count(//FILES)'))
        self.assertEqual(self._expected_run_set_xml_biis3.xpath('count(//FILE)'),
                         actual_run_set_xml_biis3.xpath('count(//FILE)'))

    def test_sra_dump_submission_xml_biis7(self):
        json2sra.convert(open(os.path.join(self._json_data_dir, 'BII-S-7', 'BII-S-7.json')), self._tmp_dir,
                         self._sra_configs_dir)
        # Now try load the SRA output in test and compare against the expected output in test data directory
        submission_xml = open(os.path.join(self._tmp_dir, 'sra', 'BII-S-7', 'submission.xml'), 'rb').read()
        actual_submission_xml_biis7 = etree.fromstring(submission_xml)
        # count tags
        self.assertEqual(self._expected_submission_xml_biis7.xpath('count(//SUBMISSION)'),
                         actual_submission_xml_biis7.xpath('count(//SUBMISSION)'))
        self.assertEqual(self._expected_submission_xml_biis7.xpath('count(//CONTACTS)'),
                         actual_submission_xml_biis7.xpath('count(//CONTACTS)'))
        self.assertEqual(self._expected_submission_xml_biis7.xpath('count(//CONTACT)'),
                         actual_submission_xml_biis7.xpath('count(//CONTACT)'))
        self.assertEqual(self._expected_submission_xml_biis7.xpath('count(//ACTIONS)'),
                         actual_submission_xml_biis7.xpath('count(//ACTIONS)'))
        self.assertEqual(self._expected_submission_xml_biis7.xpath('count(//ACTION)'),
                         actual_submission_xml_biis7.xpath('count(//ACTION)'))
        self.assertEqual(self._expected_submission_xml_biis7.xpath('count(//ADD)'),
                         actual_submission_xml_biis7.xpath('count(//ADD)'))

    def test_sra_dump_study_xml_biis7(self):
        json2sra.convert(open(os.path.join(self._json_data_dir, 'BII-S-7', 'BII-S-7.json')), self._tmp_dir,
                         self._sra_configs_dir)
        # Now try load the SRA output in test and compare against the expected output in test data directory
        study_xml = open(os.path.join(self._tmp_dir, 'sra', 'BII-S-7', 'study.xml'), 'rb').read()
        actual_study_xml_biis7 = etree.fromstring(study_xml)
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//STUDY)'),
                         actual_study_xml_biis7.xpath('count(//STUDY)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//DESCRIPTOR)'),
                         actual_study_xml_biis7.xpath('count(//DESCRIPTOR)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//CENTER_NAME)'),
                         actual_study_xml_biis7.xpath('count(//CENTER_NAME)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//CENTER_PROJECT_NAME)'),
                         actual_study_xml_biis7.xpath('count(//CENTER_PROJECT_NAME)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//STUDY_TITLE)'),
                         actual_study_xml_biis7.xpath('count(//STUDY_TITLE)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//STUDY_DESCRIPTION)'),
                         actual_study_xml_biis7.xpath('count(//STUDY_DESCRIPTION)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//STUDY_TYPE)'),
                         actual_study_xml_biis7.xpath('count(//STUDY_TYPE)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//STUDY_LINKS)'),
                         actual_study_xml_biis7.xpath('count(//STUDY_LINKS)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//STUDY_LINK)'),
                         actual_study_xml_biis7.xpath('count(//STUDY_LINK)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//ENTREZ_LINK)'),
                         actual_study_xml_biis7.xpath('count(//ENTREZ_LINK)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//DB)'),
                         actual_study_xml_biis7.xpath('count(//DB)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//ID)'),
                         actual_study_xml_biis7.xpath('count(//ID)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//STUDY_ATTRIBUTES)'),
                         actual_study_xml_biis7.xpath('count(//STUDY_ATTRIBUTES)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//STUDY_ATTRIBUTE)'),
                         actual_study_xml_biis7.xpath('count(//STUDY_ATTRIBUTE)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//TAG)'),
                         actual_study_xml_biis7.xpath('count(//TAG)'))
        self.assertEqual(self._expected_study_xml_biis7.xpath('count(//VALUE)'),
                         actual_study_xml_biis7.xpath('count(//VALUE)'))

    def test_sra_dump_sample_set_xml_biis7(self):
        json2sra.convert(open(os.path.join(self._json_data_dir, 'BII-S-7', 'BII-S-7.json')), self._tmp_dir,
                         self._sra_configs_dir)
        # Now try load the SRA output in test and compare against the expected output in test data directory
        sample_set_xml = open(os.path.join(self._tmp_dir, 'sra', 'BII-S-7', 'sample_set.xml'), 'rb').read()
        actual_sample_set_xml_biis7 = etree.fromstring(sample_set_xml)
        self.assertEqual(self._expected_sample_set_xml_biis7.xpath('count(//SAMPLE_SET)'),
                         actual_sample_set_xml_biis7.xpath('count(//SAMPLE_SET)'))
        self.assertEqual(self._expected_sample_set_xml_biis7.xpath('count(//SAMPLE)'),
                         actual_sample_set_xml_biis7.xpath('count(//SAMPLE)'))
        self.assertEqual(self._expected_sample_set_xml_biis7.xpath('count(//TITLE)'),
                         actual_sample_set_xml_biis7.xpath('count(//TITLE)'))
        self.assertEqual(self._expected_sample_set_xml_biis7.xpath('count(//SAMPLE_NAME)'),
                         actual_sample_set_xml_biis7.xpath('count(//SAMPLE_NAME)'))
        self.assertEqual(self._expected_sample_set_xml_biis7.xpath('count(//TAXON_ID)'),
                         actual_sample_set_xml_biis7.xpath('count(//TAXON_ID)'))
        self.assertEqual(self._expected_sample_set_xml_biis7.xpath('count(//SCIENTIFIC_NAME)'),
                         actual_sample_set_xml_biis7.xpath('count(//SCIENTIFIC_NAME)'))
        self.assertEqual(self._expected_sample_set_xml_biis7.xpath('count(//SAMPLE_ATTRIBUTES)'),
                         actual_sample_set_xml_biis7.xpath('count(//SAMPLE_ATTRIBUTES)'))
        self.assertEqual(self._expected_sample_set_xml_biis7.xpath('count(//SAMPLE_ATTRIBUTE)'),
                         actual_sample_set_xml_biis7.xpath('count(//SAMPLE_ATTRIBUTE)'))
        self.assertEqual(self._expected_sample_set_xml_biis7.xpath('count(//TAG)'),
                         actual_sample_set_xml_biis7.xpath('count(//TAG)'))
        self.assertEqual(self._expected_sample_set_xml_biis7.xpath('count(//VALUE)'),
                         actual_sample_set_xml_biis7.xpath('count(//VALUE)'))
        self.assertEqual(self._expected_sample_set_xml_biis7.xpath('count(//UNITS)'),
                         actual_sample_set_xml_biis7.xpath('count(//UNITS)'))

    def test_sra_dump_experiment_set_xml_biis7(self):
        json2sra.convert(open(os.path.join(self._json_data_dir, 'BII-S-7', 'BII-S-7.json')), self._tmp_dir,
                         self._sra_configs_dir)
        # Now try load the SRA output in test and compare against the expected output in test data directory
        experiment_set_xml = open(os.path.join(self._tmp_dir, 'sra', 'BII-S-7', 'experiment_set.xml'), 'rb').read()
        actual_experiment_set_xml_biis7 = etree.fromstring(experiment_set_xml)
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//EXPERIMENT_SET)'),
                         actual_experiment_set_xml_biis7.xpath('count(//EXPERIMENT_SET)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//EXPERIMENT)'),
                         actual_experiment_set_xml_biis7.xpath('count(//EXPERIMENT)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//TITLE)'),
                         actual_experiment_set_xml_biis7.xpath('count(//TITLE)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//STUDY_REF)'),
                         actual_experiment_set_xml_biis7.xpath('count(//STUDY_REF)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//DESIGN)'),
                         actual_experiment_set_xml_biis7.xpath('count(//DESIGN)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//DESIGN_DESCRIPTION)'),
                         actual_experiment_set_xml_biis7.xpath('count(//DESIGN_DESCRIPTION)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//SAMPLE_DESCRIPTOR)'),
                         actual_experiment_set_xml_biis7.xpath('count(//SAMPLE_DESCRIPTOR)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//LIBRARY_DESCRIPTOR)'),
                         actual_experiment_set_xml_biis7.xpath('count(//LIBRARY_DESCRIPTOR)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//LIBRARY_NAME)'),
                         actual_experiment_set_xml_biis7.xpath('count(//LIBRARY_NAME)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//LIBRARY_STRATEGY)'),
                         actual_experiment_set_xml_biis7.xpath('count(//LIBRARY_STRATEGY)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//LIBRARY_SOURCE)'),
                         actual_experiment_set_xml_biis7.xpath('count(//LIBRARY_SOURCE)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//LIBRARY_SELECTION)'),
                         actual_experiment_set_xml_biis7.xpath('count(//LIBRARY_SELECTION)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//LIBRARY_LAYOUT)'),
                         actual_experiment_set_xml_biis7.xpath('count(//LIBRARY_LAYOUT)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//SINGLE)'),
                         actual_experiment_set_xml_biis7.xpath('count(//SINGLE)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//TARGETED_LOCI)'),
                         actual_experiment_set_xml_biis7.xpath('count(//TARGETED_LOCI)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//LOCUS)'),
                         actual_experiment_set_xml_biis7.xpath('count(//LOCUS)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//POOLING_STRATEGY)'),
                         actual_experiment_set_xml_biis7.xpath('count(//POOLING_STRATEGY)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//LIBRARY_CONSTRUCTION_PROTOCOL)'),
                         actual_experiment_set_xml_biis7.xpath('count(//LIBRARY_CONSTRUCTION_PROTOCOL)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//SPOT_DESCRIPTOR)'),
                         actual_experiment_set_xml_biis7.xpath('count(//SPOT_DESCRIPTOR)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//SPOT_DECODE_SPEC)'),
                         actual_experiment_set_xml_biis7.xpath('count(//SPOT_DECODE_SPEC)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//READ_SPEC)'),
                         actual_experiment_set_xml_biis7.xpath('count(//READ_SPEC)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//READ_INDEX)'),
                         actual_experiment_set_xml_biis7.xpath('count(//READ_INDEX)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//READ_CLASS)'),
                         actual_experiment_set_xml_biis7.xpath('count(//READ_CLASS)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//READ_TYPE)'),
                         actual_experiment_set_xml_biis7.xpath('count(//READ_TYPE)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//BASE_COORD)'),
                         actual_experiment_set_xml_biis7.xpath('count(//BASE_COORD)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//READ_INDEX)'),
                         actual_experiment_set_xml_biis7.xpath('count(//READ_INDEX)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//EXPECTED_BASECALL_TABLE)'),
                         actual_experiment_set_xml_biis7.xpath('count(//EXPECTED_BASECALL_TABLE)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//BASECALL)'),
                         actual_experiment_set_xml_biis7.xpath('count(//BASECALL)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//RELATIVE_ORDER)'),
                         actual_experiment_set_xml_biis7.xpath('count(//RELATIVE_ORDER)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//PLATFORM)'),
                         actual_experiment_set_xml_biis7.xpath('count(//PLATFORM)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//LS454)'),
                         actual_experiment_set_xml_biis7.xpath('count(//LS454)'))
        self.assertEqual(self._expected_experiment_set_xml_biis7.xpath('count(//INSTRUMENT_MODEL)'),
                         actual_experiment_set_xml_biis7.xpath('count(//INSTRUMENT_MODEL)'))

    def test_sra_dump_run_set_xml_biis7(self):
        json2sra.convert(open(os.path.join(self._json_data_dir, 'BII-S-7', 'BII-S-7.json')), self._tmp_dir,
                         self._sra_configs_dir)
        # Now try load the SRA output in test and compare against the expected output in test data directory
        run_set_xml = open(os.path.join(self._tmp_dir, 'sra', 'BII-S-7', 'run_set.xml'), 'rb').read()
        actual_run_set_xml_biis7 = etree.fromstring(run_set_xml)
        self.assertEqual(self._expected_run_set_xml_biis7.xpath('count(//RUN_SET)'),
                         actual_run_set_xml_biis7.xpath('count(//RUN_SET)'))
        self.assertEqual(self._expected_run_set_xml_biis7.xpath('count(//RUN)'),
                         actual_run_set_xml_biis7.xpath('count(//RUN)'))
        self.assertEqual(self._expected_run_set_xml_biis7.xpath('count(//EXPERIMENT_REF)'),
                         actual_run_set_xml_biis7.xpath('count(//EXPERIMENT_REF)'))
        self.assertEqual(self._expected_run_set_xml_biis7.xpath('count(//DATA_BLOCK)'),
                         actual_run_set_xml_biis7.xpath('count(//DATA_BLOCK)'))
        self.assertEqual(self._expected_run_set_xml_biis7.xpath('count(//FILES)'),
                         actual_run_set_xml_biis7.xpath('count(//FILES)'))
        self.assertEqual(self._expected_run_set_xml_biis7.xpath('count(//FILE)'),
                         actual_run_set_xml_biis7.xpath('count(//FILE)'))
