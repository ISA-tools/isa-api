__author__ = 'agbeltran'

import os
from os import listdir
from isatools.convert.isatab2cedar import ISATab2CEDAR
from os.path import join
import unittest

class ISAtab2CEDARTest(unittest.TestCase):
      def setUp(self):
        """set up directories etc"""
        self.isa2cedar = ISATab2CEDAR()

      def test_bii_i_1_conversion(self):
        self.test_data = "./data/BII-I-1"
        self.isa2cedar.createCEDARjson(self.test_data, "./datasets", False)

      def test_metabolights_conversion(self):
        self.folder = "./datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/"
        self.path = os.path.abspath(self.folder)
        self.directories = [ f for f in listdir(self.path) ]

        for directory in self.directories:
            print "Converting ", directory, " ..."
            self.isa2cedar.createCEDARjson(join(self.path,directory), "./datasets/metabolights", False)
        print "\t... done"

