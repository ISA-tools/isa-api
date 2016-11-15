from bs4 import BeautifulSoup
from collections import defaultdict
import subprocess
import os
import re
from io import BytesIO, StringIO
from zipfile import ZipFile
from shutil import rmtree
import logging
import pdb
import glob
import uuid
import os
import sys
import bs4


sys.modules['BeautifulSoup'] = bs4

__author__ = 'philippe.rocca-serra@oerc.ox.ac.uk'
__author__ = 'massi@oerc.ox.ac.uk'
__author__ = 'alfie'

DESTINATION_DIR = 'output'
DEFAULT_SAXON_DIR = os.path.join(os.path.expanduser('~'), 'Applications', 'SaxonHE')
DEFAULT_SAXON_EXECUTABLE = os.path.join(DEFAULT_SAXON_DIR, 'saxon9he.jar')
BIOCRATES_DIR = os.path.join(os.path.dirname(__file__), 'resources', 'biocrates')
INPUT_FILE = os.path.join(BIOCRATES_DIR, 'biocrates-shorter-testfile.xml')
BIOCRATES_META_XSL_FILE = os.path.join(BIOCRATES_DIR, 'ISA-Team-Biocrates2ISATAB-refactor.xsl')
BIOCRATES_DATA_XSL_FILE = os.path.join(BIOCRATES_DIR, 'ISA-Team-Biocrates2MAF.xsl')

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def zipdir(path, zip_file):
    """utility function to zip a whole directory"""
    # zip_file is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_file.write(os.path.join(root, file))


def merge_biocrates_files(input_dir):
    """ --Biocrates2ISA support script:
    a simple script to merge several Biocrates xml files into one.
    Invoke this method before running a conversion from Biocrates to ISA-Tab if and only if the Biocrates study comes
    in more than one file
    why is this necessary? Biocrates export function limits the number of plates meaning that several xml files
    may be necessary to represent
    a complete study.
    input: a bag of Biocrates XML documents . Note: those should be from the same xsd.
    output: a rather large XML document compliant with Biocrates XSD. This file should be used as input to Biocrates2ISA
    xsl stylesheet.
    Important: Remember to up the memory available to python """

    contacts = []
    samples = []
    plate_set = []
    projects = []
    metabolites = []

    for i in glob.iglob(os.path.join(input_dir, '*.xml')):

        # f = open('/Users/Philippe/Documents/git/biocrates/Biocrates-TUM/input-Biocrates-XML-files/'
        #          'all-biocrates-xml-files/'+i)

        # note the "xml" argument: this is to ensure that BeautifulSoup does not lowercase attribute elements
        # (without, the resulting xml trips the xsl)
        # soup = BeautifulSoup(open('/Users/Philippe/Documents/git/biocrates-DATA/Biocrates-TUM/input-Biocrates'
        #                           '-XML-files/all-biocrates-xml-files/'+i), "xml")

        soup = BeautifulSoup(open(i), "xml")

        contacts = contacts + soup.find_all('contact')
        samples = samples + soup.find_all('sample')
        projects = projects + soup.find_all('project')
        plate_set = plate_set + soup.find_all('plate')
        metabolites = metabolites + soup.find_all('metabolite')

    # fh = open("/Users/Philippe/Documents/git/biocrates-DATA/Biocrates-TUM/biocrates-merged-output.xml",  'w+')
    fh = open("biocrates-merged-output.xml",  'w+')
    fh.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>")
    fh.write("<data xmlns=\"http://www.biocrates.com/metstat/result/xml_1.0\" swVersion=\"MetIQ_5.4.8-DB100-Boron-2607"
             "-DB100-2607\" "
             "concentrationUnit=\"uM\" dateExport=\"2015-10-28T10:37:23.484+01:00\" user=\"labadmin\">")

    # the order in which these objects are written reflect the Biocrates XML structure.
    # known issue: some elements (e.g. contacts may be duplicated but as the objects differ from one attribute value,
    # it is not possible to remove them without further alignment heuristic

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

    contacts = list(set(contacts))
    for element in contacts:
        fh.write(str(element.encode('utf-8')))

    fh.write("</data>")
    fh.close()

    return fh


def biocrates_to_isatab_convert(biocrates_filename, saxon_jar_path=DEFAULT_SAXON_EXECUTABLE):
    """
    Given a directory containing one or more biocrates xml filename, the method convert it to ISA-tab using an XSL 2.0
    transformation.
    If the directory contains more than one biocrates xml file corresponding to one same study, a method is called
    to merge the xml documents together prior to the transformation
    The XSLT is invoked using an executable script.

    Notice: this method depend on SAXON XSLT Processor

    Parameters:
         :param biocrates_filename (str or list) - if a string must contain only comma separated valid SRA accession
         numbers
         :param saxon_jar_path str - if provided, must be a valid path pointing to SAXON Java JAR file. Otherwise, the
                                     default Saxon HE JAR will be used, if installed

    # merged = merge_biocrates_files("/path/to/bag/of/biocrates-DATA/input-Biocrates-XML-files/")
    # biocrates_to_isatab_convert('biocrates-merged-output.xml', saxon_jar_path="/path/to/saxon9-he-processor/saxon9he.jar")

    Returns:zp
        :returns io.BytesIO if at least one of the SRA instances has been successfully converted
                 (NOTE: should I return StringIO instead?)
    """
    res = None
    dir_name = uuid.uuid4().hex
    buffer = BytesIO()

    destination_dir = os.path.abspath(dir_name)
    print('Destination dir is: ' + destination_dir)
    logger.info('Destination dir is: ' + destination_dir)

    if os.path.exists(destination_dir):
        logger.debug('Removing dir' + destination_dir)
        print('Removing dir' + destination_dir)
        rmtree(destination_dir)

    try:
        res = subprocess.call(['java', '-jar', saxon_jar_path, INPUT_FILE, BIOCRATES_META_XSL_FILE,
                                   'biocrates_filename='+biocrates_filename, 'outputdir='+destination_dir])

        logger.info('Subprocess Saxon exited with code: %d', res)

    except subprocess.CalledProcessError as err:
        logger.error("isatools.convert.biocrates2isatab: CalledProcessError caught ", err.returncode)

    with ZipFile(buffer, 'w') as zip_file:
        # use relative dir_name to avoid absolute path on file names
        zipdir(dir_name, zip_file)
        print(zip_file.namelist())

    # clean up the target directory after the ZIP file has been closed
    # rmtree(destination_dir)

    buffer.seek(0)
    return buffer



__author__ = 'alfie'


def generatePolarityAttrsDict(plate, polarity, myAttrs, myMetabolites, mydict):
    usedop = plate.get('usedop')
    platebarcode = plate.get('platebarcode')
    injection = plate.find_all('injection', {'polarity': polarity})
    if len(injection) > 0:
        for pi in injection:
            myAttrList = []
            myMetabolitesList = []
            for p in pi.find_all('measure'):
                myrdfname = p.find_parent('injection').get('rawdatafilename').split('.')[0]
                for attr, value in p.attrs.iteritems():
                    if attr != 'metabolite':
                        mydict[p.get('metabolite') + '-' + myrdfname + '-' + attr + '-' + polarity.lower() + '-' + usedop + '-' + platebarcode] = value
                        if attr not in myAttrList:
                            myAttrList.append(attr)
                myMblite = p.get('metabolite')
                if myMblite not in myMetabolitesList:
                    myMetabolitesList.append(myMblite)
            # it is assume that the rawdatafilename is unique in each of the plate grouping and polarity
            myAttrs[pi.get('rawdatafilename').split('.')[0]] = myAttrList
        myMetabolites[usedop + '-' + platebarcode + '-' + polarity.lower()] = myMetabolitesList
    return myAttrs, mydict


def generateAttrsDict(plate):
    # using dictionaries of lists
    posAttrs = defaultdict(list)
    negAttrs = defaultdict(list)
    posMetabolites = defaultdict(list)
    negMetabolites = defaultdict(list)
    mydict = {}
    posAttrs, mydict = generatePolarityAttrsDict(plate, 'POSITIVE', posAttrs, posMetabolites, mydict)
    negAttrs, mydict = generatePolarityAttrsDict(plate, 'NEGATIVE', negAttrs, negMetabolites, mydict)
    return posAttrs, negAttrs, posMetabolites, negMetabolites, mydict


def writeOutToFile(plate, polarity, usedop, platebarcode, output_dir, uniqueAttrs, uniqueMetaboliteIdentifiers, mydict):
    pos_injection = plate.find_all('injection', {'polarity': polarity})
    if len(pos_injection) > 0:
        filename = usedop + '-' + platebarcode + '-' + polarity.lower() + '-maf.txt'
        print(filename)
        with open(os.path.join(output_dir, filename), 'w') as file_handler:
            # writing out the header
            file_handler.write('Sample ID')
            for ua in uniqueAttrs:
                for myattr in uniqueAttrs[ua]:
                    file_handler.write('\t' + ua + '[' + myattr + ']')
            # now the rest of the rows
            for myMetabolite in uniqueMetaboliteIdentifiers[usedop + '-' + platebarcode + '-' + polarity.lower()]:
                file_handler.write('\n' + myMetabolite)
                for ua in uniqueAttrs:
                    for myattr in uniqueAttrs[ua]:
                        mykey = myMetabolite + '-' + ua + '-' + myattr + '-' + polarity.lower() + '-' + usedop + '-' + platebarcode
                        if mykey in mydict:
                            file_handler.write('\t' + mydict[mykey])
                        else:
                            file_handler.write('\t')
        file_handler.close()


def parseSample(file):
    folder_name = 'output'
    output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), folder_name)

    # create the output directory if it does not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file = sys.argv[1]
    # open and read up the file
    handler = open(file).read()
    soup = BeautifulSoup(handler)

    # get all the plates
    plates = soup.find_all('plate')
    for plate in plates:
        usedop = plate.get('usedop')
        platebarcode = plate.get('platebarcode')
        # extracting the the distinct column labels, metabolites, and rawdatafilename
        # collect the data into a dictionary
        posAttrs, negAttrs, posMetabolites, negMetabolites, mydict = generateAttrsDict(plate)
        # and start creating the sample tab files
        writeOutToFile(plate, 'POSITIVE', usedop, platebarcode, output_dir, posAttrs, posMetabolites, mydict)
        writeOutToFile(plate, 'NEGATIVE', usedop, platebarcode, output_dir, negAttrs, negMetabolites, mydict)


# if __name__ == "__main__":
#     parseSample(sys.argv[1])
# uncomment to run test
# merged = merge_biocrates_files("/Users/Philippe/Documents/git/biocrates-DATA/Biocrates-TUM/input-Biocrates-XML-files/all-biocrates-xml-files/")
# biocrates_to_isatab_convert('biocrates-merged-output.xml', saxon_jar_path="/Applications/IntelliJ IDEA 13.app/plugins/xslt-debugger/lib/rt/saxon9he.jar")
