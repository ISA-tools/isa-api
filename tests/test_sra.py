from unittest import TestCase
from isatools import isajson, sra
from lxml import etree
import logging
import os

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class SraExporterTests(TestCase):

    def setUp(self):
        self._dir = os.path.join(os.path.dirname(__file__), 'data', 'BII-S-7')
        self._inv_obj = isajson.load(open(os.path.join(self._dir, 'BII-S-7.json')))
        self._expected_submission_xml_obj = etree.fromstring(open(os.path.join(self._dir,
                                                                                'sra', 'submission.xml'), 'rb').read())
        self._expected_study_xml_obj = etree.fromstring(open(os.path.join(self._dir, 'sra', 'study.xml'),
                                                                 'rb').read())
        self._expected_sample_set_xml_obj = etree.fromstring(open(os.path.join(self._dir, 'sra', 'sample_set.xml'),
                                                                 'rb').read())
        self._expected_exp_set_xml_obj = etree.fromstring(open(os.path.join(self._dir, 'sra', 'experiment_set.xml'),
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

    def test_dump_submission_xml(self):
        submission_xml = sra._write_submission_xml(self._inv_obj, self._sra_default_config)
        actual_submission_xml_obj = etree.fromstring(submission_xml)
        # count tags
        self.assertEqual(self._expected_submission_xml_obj.xpath('count(//SUBMISSION)'), actual_submission_xml_obj.xpath('count(//SUBMISSION)'))
        self.assertEqual(self._expected_submission_xml_obj.xpath('count(//CONTACTS)'), actual_submission_xml_obj.xpath('count(//CONTACTS)'))
        self.assertEqual(self._expected_submission_xml_obj.xpath('count(//CONTACT)'), actual_submission_xml_obj.xpath('count(//CONTACT)'))
        self.assertEqual(self._expected_submission_xml_obj.xpath('count(//ACTIONS)'), actual_submission_xml_obj.xpath('count(//ACTIONS)'))
        self.assertEqual(self._expected_submission_xml_obj.xpath('count(//ACTION)'), actual_submission_xml_obj.xpath('count(//ACTION)'))
        self.assertEqual(self._expected_submission_xml_obj.xpath('count(//ADD)'), actual_submission_xml_obj.xpath('count(//ADD)'))

    def test_dump_study_xml(self):
        study_xml = sra._write_study_xml(self._inv_obj, self._sra_default_config)
        actual_study_xml_obj = etree.fromstring(study_xml)
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//STUDY)'), actual_study_xml_obj.xpath('count(//STUDY)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//DESCRIPTOR)'), actual_study_xml_obj.xpath('count(//DESCRIPTOR)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//CENTER_NAME)'), actual_study_xml_obj.xpath('count(//CENTER_NAME)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//CENTER_PROJECT_NAME)'), actual_study_xml_obj.xpath('count(//CENTER_PROJECT_NAME)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//STUDY_TITLE)'), actual_study_xml_obj.xpath('count(//STUDY_TITLE)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//STUDY_DESCRIPTION)'), actual_study_xml_obj.xpath('count(//STUDY_DESCRIPTION)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//STUDY_TYPE)'), actual_study_xml_obj.xpath('count(//STUDY_TYPE)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//STUDY_LINKS)'), actual_study_xml_obj.xpath('count(//STUDY_LINKS)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//STUDY_LINK)'), actual_study_xml_obj.xpath('count(//STUDY_LINK)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//ENTREZ_LINK)'), actual_study_xml_obj.xpath('count(//ENTREZ_LINK)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//DB)'), actual_study_xml_obj.xpath('count(//DB)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//ID)'), actual_study_xml_obj.xpath('count(//ID)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//STUDY_ATTRIBUTES)'), actual_study_xml_obj.xpath('count(//STUDY_ATTRIBUTES)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//STUDY_ATTRIBUTE)'), actual_study_xml_obj.xpath('count(//STUDY_ATTRIBUTE)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//TAG)'), actual_study_xml_obj.xpath('count(//TAG)'))
        self.assertEqual(self._expected_study_xml_obj.xpath('count(//VALUE)'), actual_study_xml_obj.xpath('count(//VALUE)'))

    def test_dump_sample_set_xml(self):
        sample_set_xml = sra._write_sample_set_xml(self._inv_obj, self._sra_default_config)
        actual_sample_set_xml_obj = etree.fromstring(sample_set_xml)
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//SAMPLE_SET)'), actual_sample_set_xml_obj.xpath('count(//SAMPLE_SET)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//SAMPLE)'), actual_sample_set_xml_obj.xpath('count(//SAMPLE)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//TITLE)'), actual_sample_set_xml_obj.xpath('count(//TITLE)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//SAMPLE_NAME)'), actual_sample_set_xml_obj.xpath('count(//SAMPLE_NAME)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//TAXON_ID)'), actual_sample_set_xml_obj.xpath('count(//TAXON_ID)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//SCIENTIFIC_NAME)'), actual_sample_set_xml_obj.xpath('count(//SCIENTIFIC_NAME)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//SAMPLE_ATTRIBUTES)'), actual_sample_set_xml_obj.xpath('count(//SAMPLE_ATTRIBUTES)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//SAMPLE_ATTRIBUTE)'), actual_sample_set_xml_obj.xpath('count(//SAMPLE_ATTRIBUTE)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//TAG)'), actual_sample_set_xml_obj.xpath('count(//TAG)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//VALUE)'), actual_sample_set_xml_obj.xpath('count(//VALUE)'))
        self.assertEqual(self._expected_sample_set_xml_obj.xpath('count(//UNITS)'), actual_sample_set_xml_obj.xpath('count(//UNITS)'))

    def test_dump_exp_set_xml(self):
        exp_set_xml = sra._write_experiment_set_xml(self._inv_obj, self._sra_default_config)
        actual_exp_set_xml_obj = etree.fromstring(exp_set_xml)
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//EXPERIMENT_SET)'), actual_exp_set_xml_obj.xpath('count(//EXPERIMENT_SET)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//EXPERIMENT)'), actual_exp_set_xml_obj.xpath('count(//EXPERIMENT)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//TITLE)'), actual_exp_set_xml_obj.xpath('count(//TITLE)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//STUDY_REF)'), actual_exp_set_xml_obj.xpath('count(//STUDY_REF)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//DESIGN)'), actual_exp_set_xml_obj.xpath('count(//DESIGN)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//DESIGN_DESCRIPTION)'), actual_exp_set_xml_obj.xpath('count(//DESIGN_DESCRIPTION)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//SAMPLE_DESCRIPTOR)'), actual_exp_set_xml_obj.xpath('count(//SAMPLE_DESCRIPTOR)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LIBRARY_DESCRIPTOR)'), actual_exp_set_xml_obj.xpath('count(//LIBRARY_DESCRIPTOR)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LIBRARY_NAME)'), actual_exp_set_xml_obj.xpath('count(//LIBRARY_NAME)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LIBRARY_STRATEGY)'), actual_exp_set_xml_obj.xpath('count(//LIBRARY_STRATEGY)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LIBRARY_SOURCE)'), actual_exp_set_xml_obj.xpath('count(//LIBRARY_SOURCE)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LIBRARY_SELECTION)'), actual_exp_set_xml_obj.xpath('count(//LIBRARY_SELECTION)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LIBRARY_LAYOUT)'), actual_exp_set_xml_obj.xpath('count(//LIBRARY_LAYOUT)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//SINGLE)'), actual_exp_set_xml_obj.xpath('count(//SINGLE)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//TARGETED_LOCI)'), actual_exp_set_xml_obj.xpath('count(//TARGETED_LOCI)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LOCUS)'), actual_exp_set_xml_obj.xpath('count(//LOCUS)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//POOLING_STRATEGY)'), actual_exp_set_xml_obj.xpath('count(//POOLING_STRATEGY)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LIBRARY_CONSTRUCTION_PROTOCOL)'), actual_exp_set_xml_obj.xpath('count(//LIBRARY_CONSTRUCTION_PROTOCOL)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//SPOT_DESCRIPTOR)'), actual_exp_set_xml_obj.xpath('count(//SPOT_DESCRIPTOR)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//SPOT_DECODE_SPEC)'), actual_exp_set_xml_obj.xpath('count(//SPOT_DECODE_SPEC)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//READ_SPEC)'), actual_exp_set_xml_obj.xpath('count(//READ_SPEC)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//READ_INDEX)'), actual_exp_set_xml_obj.xpath('count(//READ_INDEX)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//READ_CLASS)'), actual_exp_set_xml_obj.xpath('count(//READ_CLASS)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//READ_TYPE)'), actual_exp_set_xml_obj.xpath('count(//READ_TYPE)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//BASE_COORD)'), actual_exp_set_xml_obj.xpath('count(//BASE_COORD)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//READ_INDEX)'), actual_exp_set_xml_obj.xpath('count(//READ_INDEX)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//EXPECTED_BASECALL_TABLE)'), actual_exp_set_xml_obj.xpath('count(//EXPECTED_BASECALL_TABLE)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//BASECALL)'), actual_exp_set_xml_obj.xpath('count(//BASECALL)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//RELATIVE_ORDER)'), actual_exp_set_xml_obj.xpath('count(//RELATIVE_ORDER)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//PLATFORM)'), actual_exp_set_xml_obj.xpath('count(//PLATFORM)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//LS454)'), actual_exp_set_xml_obj.xpath('count(//LS454)'))
        self.assertEqual(self._expected_exp_set_xml_obj.xpath('count(//INSTRUMENT_MODEL)'), actual_exp_set_xml_obj.xpath('count(//INSTRUMENT_MODEL)'))

