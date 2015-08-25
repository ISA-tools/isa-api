__author__ = 'agbeltran'

import os
from os import listdir
from api.io.isatab2cedar import ISATab2CEDAR
from os.path import join

folder = "./datasets/ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/"
path = os.path.abspath(folder)
directories = [ f for f in listdir(path) ]

for directory in directories:
    print "Converting ", directory, " ..."
    isa2cedar = ISATab2CEDAR()
    isa2cedar.createCEDARjson(join(path,directory), "./datasets/output", False)
    print "\t... done"

