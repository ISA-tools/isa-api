__author__ = 'philippe.rocca-serra@oerc.ox.ac.uk'
#--Biocrates2ISA support script:
# a simple script to merge several Biocrates xml files into one.
# why is this necessary? Biocrates export function limits the number of plates meaning that several Biocrates xml files may be necesary to represent
# a complete study.
# input: a bag of Biocrates XML documents . Note: those should be from the same xsd.
# output: a rather large XML document compliant with Biocrates XSD. This file should be used as input to Biocrates2ISA xsl stylesheet.
# Important: Remember to up the memory available to python


from bs4 import BeautifulSoup

import os
import sys, bs4

sys.modules['BeautifulSoup'] = bs4

def merge():

    contacts   = []
    samples    = []
    plate_set  = []
    projects   = []
    metabolites = []

    for i in os.listdir('/Users/Philippe/Documents/git/xslt2isa/biocrates/Biocrates-TUM/input-Biocrates-XML-files/all-biocrates-xml-files'):

        if i.endswith(".xml") :

            f = open('/Users/Philippe/Documents/git/xslt2isa/biocrates/Biocrates-TUM/input-Biocrates-XML-files/all-biocrates-xml-files/'+i)

            # note the "xml" argument: this is to ensure that BeautifulSoup does not lowercase attribute elements (without, the resulting xml trips the xsl)
            soup = BeautifulSoup(open('/Users/Philippe/Documents/git/xslt2isa/biocrates/Biocrates-TUM/input-Biocrates-XML-files/all-biocrates-xml-files/'+i),"xml")


            contacts = contacts + soup.find_all('contact')
            samples = samples + soup.find_all('sample')
            projects = projects + soup.find_all('project')
            plate_set = plate_set + soup.find_all('plate')
            metabolites = metabolites + soup.find_all('metabolite')


    fh = open("/Users/Philippe/Documents/git/xslt2isa/biocrates/Biocrates-TUM/biocrates-merged-output.xml",'w+')
    fh.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>")
    fh.write("<data xmlns=\"http://www.biocrates.com/metstat/result/xml_1.0\" swVersion=\"MetIQ_5.4.8-DB100-Boron-2607-DB100-2607\" concentrationUnit=\"uM\" dateExport=\"2015-10-28T10:37:23.484+01:00\" user=\"labadmin\">")

    #the order in which these objects are written reflect the Biocrates XML structure.
    #known issue: some elements (e.g. contacts may be duplicated but as the objects differ from one attribute value, it is not possible to remove them without further alignment heuristic

    metabolites = list(set(metabolites))
    for element in metabolites:
        fh.write(str(element))

    plate_set = list(set(plate_set))
    for element in plate_set:
        fh.write(str(element))

    projects = list(set(projects))
    for element in projects:
        fh.write(str(element))

    samples = list(set(samples))
    for element in samples:
        fh.write(str(element))

    contacts=list(set(contacts))
    for element in contacts:
        fh.write(str(element.encode('utf-8')))


    fh.write("</data>")
    fh.close()

if __name__ == '__main__':
    merge()



