__author__ = 'agbeltran'

import os
from os import listdir
from isatools.convert.isatab2cedar import ISATab2CEDAR
from os.path import join
import unittest

class ISAtab2CEDARTest(unittest.TestCase):
      def setUp(self):
        """set up directories etc"""
        print("Path at terminal when executing this file")
        print(os.getcwd() + "\n")
        self.pathToSchemas = os.path.abspath("../isatools/schemas/cedar")
        print "path to schemas-->", self.pathToSchemas
        self.isa2cedar = ISATab2CEDAR()


        def test_metabolights_conversion(self):
            self.folder = "./datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/"
            self.path = os.path.abspath(self.folder)
            self.directories = [ f for f in listdir(self.path) ]

            for directory in self.directories:
                print "Converting ", directory, " ..."
                self.isa2cedar.createCEDARjson(self.pathToSchemas, join(self.path,directory), "./datasets/metabolights", False)
            print "\t... done"

