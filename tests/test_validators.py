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


class ValidateIsaTabTest(TestCase):

    def setUp(self):
        self._dir = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def test_invalid_tab_load(self):
        with self.assertRaises(ValueError):
            isatab.validatei(open(os.path.join(self._dir, 'data', 'tab', 'invalid_i', 'i_01.txt')))
        with self.assertRaises(ValueError):
            isatab.validatei(open(os.path.join(self._dir, 'data', 'tab', 'invalid_i', 'i_02.txt')))

