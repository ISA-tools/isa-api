from unittest import TestCase
from isatools import isajson, sra
from lxml import objectify, etree
import logging
import os

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class SraExporterTests(TestCase):

    def setUp(self):
        self._dir = os.path.join(os.path.dirname(__file__), 'data', 'BII-S-7')
        self._inv_obj = isajson.load(open(os.path.join(self._dir, 'BII-S-7.json')))
        self._expected_run_set_xml_obj = objectify.fromstring(open(os.path.join(self._dir,
                                                                                'srafix', 'submission.xml'), 'rb').read())

    def test_dump_submission_xml(self):
        submission_xml = sra._write_submission_xml(self._inv_obj.studies[0])
        actual_submission_xml_obj = objectify.fromstring(submission_xml)
        self.assertEqual(etree.tostring(self._expected_run_set_xml_obj), etree.tostring(actual_submission_xml_obj))