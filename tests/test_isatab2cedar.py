import os
from os import listdir
from isatools.convert.isatab2cedar import ISATab2CEDAR
from os.path import join
from unittest import TestCase


class ISAtab2CEDARTest(TestCase):
    def setUp(self):
        """set up directories etc"""
        pass

    def test_bii_i_1_conversion(self):
        self.isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        self.test_data = "./data/BII-I-1"
        self.isa2cedar.createCEDARjson(self.test_data, "./data", True)

    def test_metabolights_conversion(self):
        self.isa2cedar = ISATab2CEDAR("http://www.ebi.ac.uk/metabolights/")
        self.folder = "./data/metabolights"
        self.path = os.path.abspath(self.folder)
        self.directories = [ f for f in listdir(self.path) ]

        for directory in self.directories:
            print("Converting ", directory, " ...")
            self.isa2cedar.createCEDARjson(join(self.path,directory), "./data/metabolights", False)
        print("\t... done")


