import os
from os import listdir
from isatools.convert.isatab2cedar import ISATab2CEDAR
from unittest import TestCase


class ISAtab2CEDARTest(TestCase):
    def setUp(self):
        """set up directories etc"""
        self._data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_bii_i_1_conversion(self):
        self.isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        self.test_data = os.path.join(self._data_dir, "BII-I-1")
        self.isa2cedar.createCEDARjson(self.test_data, self._data_dir, True)

    def test_isa_charac_param_factor(self):
        self.isa2cedar = ISATab2CEDAR("http://www.isa-tools.org/")
        self.test_data = os.path.join(self._data_dir, "TEST-ISA-charax-param-factor")
        self.isa2cedar.createCEDARjson(self.test_data, self._data_dir, True)

    def test_metabolights_conversion(self):
        self.isa2cedar = ISATab2CEDAR("http://www.ebi.ac.uk/metabolights/")
        self.folder = os.path.join(self._data_dir, "metabolights")
        self.path = os.path.abspath(self.folder)

        # find all subdirectories in self.path directory
        self.directories = next(os.walk(self.path))[1]

        for directory in self.directories:
            print("Converting ", directory, " ...")
            self.isa2cedar.createCEDARjson(os.path.join(self.path, directory),
                                           os.path.join(self._data_dir, "metabolights"), False)
        print("\t... done")


