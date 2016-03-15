from unittest import TestCase
from isatools import isajson
from isatools import isatab
import os


class ValidateIsaJsonTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def test_invalid_json_load(self):
        with self.assertRaises(ValueError):
            isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'invalid.json')))

    def test_isa_json_load(self):
        isajson.validate(open(os.path.join(self._dir, 'data', 'json', 'minimal_syntax.json')))


class ValidateIsaTabTest:

    def setUp(self):
        pass

    def tearDown(self):
        pass