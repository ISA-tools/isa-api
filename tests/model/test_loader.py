from os import path
from json import load
from unittest import TestCase

from isatools.model.investigation import Investigation
from isatools.isajson import load as isa_load, loads as isa_loads


class TestCompareLoaders(TestCase):

    def setUp(self) -> None:
        self.here_path = path.dirname(path.realpath(__file__))
        self.use_cases = [
            path.join(self.here_path, '..', 'data', 'json', 'BII-S-3', "BII-S-3.json"),
            path.join(self.here_path, '..', 'data', 'json', 'BII-S-7', "BII-S-7.json")
        ]

    def test_compare_loaders(self):
        for use_case in self.use_cases:
            self.set_investigations(use_case)
            self.assert_cases()

    def set_investigations(self, filepath):
        with open(filepath) as f:
            self.investigation_json = load(f)
        with open(filepath) as f:
            self.old_investigation = isa_load(f)
        with open(filepath) as f:
            self.new_investigation = isa_loads(f)

    def assert_cases(self):
        self.maxDiff = None
        new_investigation = self.new_investigation
        old_investigation = self.old_investigation
        self.assertEqual(old_investigation, new_investigation)
