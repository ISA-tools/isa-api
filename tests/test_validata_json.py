__author__ = 'agbeltran'

import unittest
from isatools.validate.validate_json import validateJsonAgainstSchemas

class ValidateJsonTest(unittest.TestCase):

      def test_cedar_example(self):
        validateJsonAgainstSchemas("../isatools/schemas/cedar/InvestigationSchema.json","../isatools/schemas/cedar/InvestigationExampleInstances.json")

      def test_cedar_bii_i_1(self):
        validateJsonAgainstSchemas("../isatools/schemas/cedar/InvestigationSchema.json","./datassets/BII-S-1.json")