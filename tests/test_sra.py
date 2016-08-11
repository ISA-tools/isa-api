from unittest import TestCase
from isatools import isajson, sra
from lxml import etree
import os
import shutil
from tests import utils
import tempfile


class TestNewSraExport(TestCase):

    # TODO: Need to write XML comparisons, not just count the tags

    def setUp(self):

        self._json_data_dir = utils.JSON_DATA_DIR
        self._sra_data_dir = utils.SRA_DATA_DIR
        self._tmp_dir = tempfile.mkdtemp()

        study_id = 'BII-S-7'
        self._inv_obj = isajson.load(open(os.path.join(self._json_data_dir, study_id, study_id + '.json')))
        self._study_sra_data_dir = os.path.join(self._sra_data_dir, study_id)
        self._expected_submission_xml_obj = etree.fromstring(open(os.path.join(self._study_sra_data_dir, 'submission.xml'), 'rb').read())
        self._expected_project_set_xml_obj = etree.fromstring(open(os.path.join(self._study_sra_data_dir, 'project_set.xml'),
                                                                 'rb').read())
        self._expected_sample_set_xml_obj = etree.fromstring(open(os.path.join(self._study_sra_data_dir, 'sample_set.xml'),
                                                                 'rb').read())
        self._expected_exp_set_xml_obj = etree.fromstring(open(os.path.join(self._study_sra_data_dir, 'experiment_set.xml'),
                                                                  'rb').read())
        self._expected_run_set_xml_obj = etree.fromstring(open(os.path.join(self._study_sra_data_dir, 'run_set.xml'),
                                                               'rb').read())

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
        shutil.rmtree(self._tmp_dir)

    def test_sra_export(self):
        sra.export(self._inv_obj, self._tmp_dir)
        actual_submission_xml_obj = etree.fromstring(open(os.path.join(self._tmp_dir, 'submission.xml'), 'rb').read())
        # count tags
        self.assertEqual(self._expected_submission_xml_obj.xpath('count(//SUBMISSION)'),
                         actual_submission_xml_obj.xpath('count(//SUBMISSION)'))
        self.assertEqual(self._expected_submission_xml_obj.xpath('count(//CONTACTS)'),
                         actual_submission_xml_obj.xpath('count(//CONTACTS)'))
        self.assertEqual(self._expected_submission_xml_obj.xpath('count(//CONTACT)'),
                         actual_submission_xml_obj.xpath('count(//CONTACT)'))
        self.assertEqual(self._expected_submission_xml_obj.xpath('count(//ACTIONS)'),
                         actual_submission_xml_obj.xpath('count(//ACTIONS)'))
        self.assertEqual(self._expected_submission_xml_obj.xpath('count(//ACTION)'),
                         actual_submission_xml_obj.xpath('count(//ACTION)'))
        self.assertEqual(self._expected_submission_xml_obj.xpath('count(//ADD)'),
                         actual_submission_xml_obj.xpath('count(//ADD)'))

        actual_sample_set_xml_obj = etree.fromstring(open(os.path.join(self._tmp_dir, 'sample_set.xml'), 'rb').read())
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//SAMPLE_SET)'),
                         actual_sample_set_xml_obj.xpath('count(//SAMPLE_SET)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//SAMPLE)'),
                         actual_sample_set_xml_obj.xpath('count(//SAMPLE)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//TITLE)'),
                         actual_sample_set_xml_obj.xpath('count(//TITLE)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//SAMPLE_NAME)'),
                         actual_sample_set_xml_obj.xpath('count(//SAMPLE_NAME)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//TAXON_ID)'),
                         actual_sample_set_xml_obj.xpath('count(//TAXON_ID)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//SCIENTIFIC_NAME)'),
                         actual_sample_set_xml_obj.xpath('count(//SCIENTIFIC_NAME)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//SAMPLE_ATTRIBUTES)'),
                         actual_sample_set_xml_obj.xpath('count(//SAMPLE_ATTRIBUTES)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//SAMPLE_ATTRIBUTE)'),
                         actual_sample_set_xml_obj.xpath('count(//SAMPLE_ATTRIBUTE)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//TAG)'),
                         actual_sample_set_xml_obj.xpath('count(//TAG)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//VALUE)'),
                         actual_sample_set_xml_obj.xpath('count(//VALUE)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//UNITS)'),
                         actual_sample_set_xml_obj.xpath('count(//UNITS)'))

        actual_exp_set_xml_obj = etree.fromstring(open(os.path.join(self._tmp_dir, 'experiment_set.xml'), 'rb').read())
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//EXPERIMENT_SET)'),
                         actual_exp_set_xml_obj.xpath('count(//EXPERIMENT_SET)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//EXPERIMENT)'),
                         actual_exp_set_xml_obj.xpath('count(//EXPERIMENT)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//TITLE)'),
                         actual_exp_set_xml_obj.xpath('count(//TITLE)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//STUDY_REF)'),
                         actual_exp_set_xml_obj.xpath('count(//STUDY_REF)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//DESIGN)'),
                         actual_exp_set_xml_obj.xpath('count(//DESIGN)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//DESIGN_DESCRIPTION)'),
                         actual_exp_set_xml_obj.xpath('count(//DESIGN_DESCRIPTION)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//SAMPLE_DESCRIPTOR)'),
                         actual_exp_set_xml_obj.xpath('count(//SAMPLE_DESCRIPTOR)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LIBRARY_DESCRIPTOR)'),
                         actual_exp_set_xml_obj.xpath('count(//LIBRARY_DESCRIPTOR)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LIBRARY_NAME)'),
                         actual_exp_set_xml_obj.xpath('count(//LIBRARY_NAME)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LIBRARY_STRATEGY)'),
                         actual_exp_set_xml_obj.xpath('count(//LIBRARY_STRATEGY)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LIBRARY_SOURCE)'),
                         actual_exp_set_xml_obj.xpath('count(//LIBRARY_SOURCE)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LIBRARY_SELECTION)'),
                         actual_exp_set_xml_obj.xpath('count(//LIBRARY_SELECTION)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LIBRARY_LAYOUT)'),
                         actual_exp_set_xml_obj.xpath('count(//LIBRARY_LAYOUT)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//SINGLE)'),
                         actual_exp_set_xml_obj.xpath('count(//SINGLE)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//TARGETED_LOCI)'),
                         actual_exp_set_xml_obj.xpath('count(//TARGETED_LOCI)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LOCUS)'),
                         actual_exp_set_xml_obj.xpath('count(//LOCUS)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//POOLING_STRATEGY)'),
                         actual_exp_set_xml_obj.xpath('count(//POOLING_STRATEGY)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LIBRARY_CONSTRUCTION_PROTOCOL)'),
                         actual_exp_set_xml_obj.xpath('count(//LIBRARY_CONSTRUCTION_PROTOCOL)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//SPOT_DESCRIPTOR)'),
                         actual_exp_set_xml_obj.xpath('count(//SPOT_DESCRIPTOR)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//SPOT_DECODE_SPEC)'),
                         actual_exp_set_xml_obj.xpath('count(//SPOT_DECODE_SPEC)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//READ_SPEC)'),
                         actual_exp_set_xml_obj.xpath('count(//READ_SPEC)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//READ_INDEX)'),
                         actual_exp_set_xml_obj.xpath('count(//READ_INDEX)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//READ_CLASS)'),
                         actual_exp_set_xml_obj.xpath('count(//READ_CLASS)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//READ_TYPE)'),
                         actual_exp_set_xml_obj.xpath('count(//READ_TYPE)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//BASE_COORD)'),
                         actual_exp_set_xml_obj.xpath('count(//BASE_COORD)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//READ_INDEX)'),
                         actual_exp_set_xml_obj.xpath('count(//READ_INDEX)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//EXPECTED_BASECALL_TABLE)'),
                         actual_exp_set_xml_obj.xpath('count(//EXPECTED_BASECALL_TABLE)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//BASECALL)'),
                         actual_exp_set_xml_obj.xpath('count(//BASECALL)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//RELATIVE_ORDER)'),
                         actual_exp_set_xml_obj.xpath('count(//RELATIVE_ORDER)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//PLATFORM)'),
                         actual_exp_set_xml_obj.xpath('count(//PLATFORM)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LS454)'),
                         actual_exp_set_xml_obj.xpath('count(//LS454)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//INSTRUMENT_MODEL)'),
                         actual_exp_set_xml_obj.xpath('count(//INSTRUMENT_MODEL)'))

        actual_run_set_xml_obj = etree.fromstring(open(os.path.join(self._tmp_dir, 'run_set.xml'), 'rb').read())
        self.assertEqual(self._expected_run_set_xml_obj.xpath('count(//RUN_SET)'),
                         actual_run_set_xml_obj.xpath('count(//RUN_SET)'))
        self.assertEqual(self._expected_run_set_xml_obj.xpath('count(//RUN)'),
                         actual_run_set_xml_obj.xpath('count(//RUN)'))
        self.assertEqual(self._expected_run_set_xml_obj.xpath('count(//EXPERIMENT_REF)'),
                         actual_run_set_xml_obj.xpath('count(//EXPERIMENT_REF)'))
        self.assertEqual(self._expected_run_set_xml_obj.xpath('count(//DATA_BLOCK)'),
                         actual_run_set_xml_obj.xpath('count(//DATA_BLOCK)'))
        self.assertEqual(self._expected_run_set_xml_obj.xpath('count(//FILES)'),
                         actual_run_set_xml_obj.xpath('count(//FILES)'))
        self.assertEqual(self._expected_run_set_xml_obj.xpath('count(//FILE)'),
                         actual_run_set_xml_obj.xpath('count(//FILE)'))

        actual_project_set_xml_obj = etree.fromstring(open(os.path.join(self._tmp_dir, 'project_set.xml'), 'rb').read())
        # TODO Need to create an expected project_set.xml to compare actual project_set.xml
