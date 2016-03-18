from unittest import TestCase
from isatools import isajson
from isatools import isatab
import os
from isatools.isatab import ValidationError
from logging import INFO


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
        self.reporting_level = INFO

    def tearDown(self):
        pass

    def test_i_no_content(self):
        with self.assertRaises(ValidationError):
            isatab.validatei(fp=open(os.path.join(self._dir, 'data', 'tab', 'invalid_i', 'i_01.txt')),
                             reporting_level=self.reporting_level)

    def test_i_no_required_labels(self):
        with self.assertRaises(ValidationError):
            isatab.validatei(fp=open(os.path.join(self._dir, 'data', 'tab', 'invalid_i', 'i_02.txt')),
                             reporting_level=self.reporting_level)

    def test_i_valid_labels(self):
        isatab.validatei(fp=open(os.path.join(self._dir, 'data', 'tab', 'valid_i', 'i_01.txt')),
                         reporting_level=self.reporting_level)

    def test_i_content(self):
        isatab.validatei(fp=open(os.path.join(self._dir, 'data', 'tab', 'invalid_i', 'i_03.txt')),
                         reporting_level=self.reporting_level)
