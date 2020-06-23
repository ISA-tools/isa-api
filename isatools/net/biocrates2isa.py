# -*- coding: utf-8 -*-
"""Functions for importing from BioCrates"""
from time import time
import os

# -- TESTING FOR distribution and light-weight parallel DataFrame implementation
# os.environ["MODIN_ENGINE"] = "ray"
# os.environ["MODIN_CPUS"] = "4"
# import ray
# ray.init(num_cpus=1)
# import modin.pandas as pd
# -- END OF ---------------

import pandas as pd

import glob
import logging

import subprocess
import sys
import uuid

import fileinput

from collections import defaultdict
from io import BytesIO
from shutil import rmtree
from zipfile import ZipFile

import bs4
from bs4 import BeautifulSoup


sys.modules['BeautifulSoup'] = bs4

__author__ = ['philippe.rocca-serra@oerc.ox.ac.uk',
              'massi@oerc.ox.ac.uk',
              'alfie']


DEFAULT_SAXON_EXECUTABLE = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)), 'resources', 'saxon9', 'saxon9he.jar')

# print(DEFAULT_SAXON_EXECUTABLE)

BIOCRATES_DIR = os.path.join(os.path.dirname(__file__), 'resources',
                             'biocrates')

BIOCRATES_META_XSL_FILE = os.path.join(
    BIOCRATES_DIR, 'ISA-Team-Biocrates2ISATAB-refactor-no-quotes.xsl')

BIOCRATES_DATA_XSL_FILE = os.path.join(
    BIOCRATES_DIR, 'ISA-Team-Biocrates2MAF.xsl')

SAMPLE_METADATA_INPUT_DIR = 'resources/biocrates/input-test/'

DESTINATION_DIR = 'biocrates-in-isa'

logger = logging.getLogger('isatools')


def replaceAll(file, searchExp, replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp, replaceExp)
        sys.stdout.write(line)


def zipdir(path, zip_file):
    """utility function to zip a whole directory"""
    # zip_file is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_file.write(os.path.join(root, file))


def merge_biocrates_files(input_dir):
    """ --Biocrates2ISA support script:
    a simple script to merge several Biocrates xml files into one.
    Invoke this method before running a conversion from Biocrates to ISA-Tab
    if and only if the Biocrates study comes in more than one file why is
    this necessary? Biocrates export function limits the number of plates
    meaning that several xml files may be necessary to represent a complete
    study.
    input: a bag of Biocrates XML documents . Note: those should be from the
    same xsd.
    output: a rather large XML document compliant with Biocrates XSD. This
    file should be used as input to Biocrates2ISA xsl stylesheet.
    Important: Remember to up the memory available to python

    returns:
           status: True or False """

    contacts = []
    samples = []
    plate_set = []
    projects = []
    metabolites = []
    status = True

    try:
        for i in glob.iglob(os.path.join(input_dir, '*.xml')):

            # f = open('/Users/Philippe/Documents/git/biocrates/Biocrates-TUM/
            # input-Biocrates-XML-files/'
            #          'all-biocrates-xml-files/'+i)

            # note the "xml" argument: this is to ensure that BeautifulSoup does
            # not lowercase attribute elements
            # (without, the resulting xml trips the xsl)
            # soup = BeautifulSoup(open('/Users/Philippe/Documents/git/
            # biocrates-DATA/Biocrates-TUM/input-Biocrates-XML-files/
            # all-biocrates-xml-files/'+i), "xml")

            soup = BeautifulSoup(open(i), "xml")

            contacts = contacts + soup.find_all('contact')
            samples = samples + soup.find_all('sample')
            projects = projects + soup.find_all('project')
            plate_set = plate_set + soup.find_all('plate')
            metabolites = metabolites + soup.find_all('metabolite')

        # fh = open("/Users/Philippe/Documents/git/biocrates-DATA/Biocrates-TUM/
        # biocrates-merged-output.xml",  'w+')
        fh = open("biocrates-merged-output.xml", 'w+')
        fh.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>")
        fh.write("<data xmlns=\"http://www.biocrates.com/metstat/result/xml_1.0\""
                 "swVersion=\"MetIQ_5.4.8-DB100-Boron-2607"
                 "-DB100-2607\""
                 "concentrationUnit=\"uM\""
                 "dateExport=\"2015-10-28T10:37:23.484+01:00\" user=\"labadmin\">")

        # the order in which these objects are written reflect the Biocrates XML
        # structure.
        # known issue: some elements (e.g. contacts may be duplicated but as the
        # objects differ from one attribute value, it is not possible to remove
        # them without further alignment heuristic

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

    except IOError as ioe:
        print("error in merge_biocrates_files function:", ioe)
        status = False

    return fh, status


def biocrates_to_isatab_convert(**kwargs):
    options = {
        'biocrates_filename': '',
        'saxon_jar_path': DEFAULT_SAXON_EXECUTABLE,
        'inputdir': BIOCRATES_DIR,
        'outputdir': '',
        'validate_option': ''
    }
    # biocrates_filename, saxon_jar_path=DEFAULT_SAXON_EXECUTABLE, outputdir,validation_option):
    """
    Given a directory containing one or more biocrates xml filename, the method
    convert it to ISA-tab using an XSL 2.0 transformation.
    If the directory contains more than one biocrates xml file corresponding to
    one same study, a method is called to merge the xml documents together
    prior to the transformation
    The XSLT is invoked using an executable script.

    Notice: this method depend on SAXON XSLT Processor

    Parameters:
         :param biocrates_filename (str or list) - if a string must contain
         only comma separated valid SRA accessionnumbers
         :param saxon_jar_path str - if provided, must be a valid path pointing
                                     to SAXON Java JAR file. Otherwise, the
                                     default Saxon HE JAR will be used, if
                                     installed

    # merged = merge_biocrates_files("/path/to/bag/of/biocrates-DATA/
    input-Biocrates-XML-files/")
    # biocrates_to_isatab_convert('biocrates-merged-output.xml',
    saxon_jar_path="/path/to/saxon9-he-processor/saxon9he.jar")

    Returns:zp
        :returns io.BytesIO if at least one of the SRA instances has been
        successfully converted
                 (NOTE: should I return StringIO instead?)
        :returns conversion_success
        :returns outputdir         
    """

    conversion_success = True

    # res = None
    # dir_name = uuid.uuid4().hex
    buffer = BytesIO()
    #
    # destination_dir = os.path.abspath(dir_name)
    # print('\nDestination dir is: ' + destination_dir)
    # logger.info('\nDestination dir is: ' + destination_dir)
    #
    # if os.path.exists(destination_dir):
    #     logger.debug('Removing dir' + destination_dir)
    #     print('Removing dir' + destination_dir)
    #     rmtree(destination_dir)

    try:
        options.update(kwargs)
        print("\nuser options:", options)
        input_dir = options['inputdir']
        biocrates_filename = options['biocrates_filename']
        saxon_jar_path = options['saxon_jar_path']
        destination_dir = options['outputdir']
        validate_option = options['validate_option']
        input = os.path.join(input_dir, biocrates_filename)
        saxon_command = ['java', '-jar', saxon_jar_path, input,
        BIOCRATES_META_XSL_FILE,
                        'biocrates_filename=' + biocrates_filename,
                               'outputdir=' + destination_dir,
                               "MYPATHVAR=" + destination_dir + "/"]
        print("saxon command: ", saxon_command)
        res = subprocess.call(saxon_command)

        print("SAXON invoke", res)
        logger.info('Subprocess Saxon exited with code: %d', res)

    except subprocess.CalledProcessError as err:
        logger.error("isatools.convert.biocrates2isatab: "
                     "CalledProcessError caught ", err.returncode)

        print("something went wrong during conversion:", err)
        conversion_success = False

    with ZipFile(buffer, 'w') as zip_file:
        # use relative dir_name to avoid absolute path on file names
        zipdir(destination_dir, zip_file)
        print("!", zip_file.namelist())

    # clean up the target directory after the ZIP file has been closed
    # rmtree(destination_dir)

    buffer.seek(0)
    # return conversion_success, buffer, validate_option
    return conversion_success, destination_dir, validate_option


def generate_polarity_attrs_dict(plate, polarity, my_attrs, my_metabolites, mydict):
    """
    __author___: alfie
    :param plate:
    :param polarity:
    :param my_attrs:
    :param my_metabolites:
    :param mydict:
    :returns: my_attrs, mydict

    """
    usedop = plate.get('usedop')
    platebarcode = plate.get('platebarcode')
    injection = plate.find_all('injection', {'polarity': polarity})
    if len(injection) > 0:
        for pi in injection:
            my_attr_list = []
            my_metabolites_list = []
            for p in pi.find_all('measure'):
                myrdfname = p.find_parent('injection').get(
                    'rawdatafilename').split('.')[0]
                for attr, value in p.attrs.items():
                    if attr != 'metabolite':
                        mydict[p.get('metabolite') + '-' + myrdfname + '-'
                               + attr + '-' + polarity.lower() + '-' + usedop
                               + '-' + platebarcode] = value
                        if attr not in my_attr_list:
                            my_attr_list.append(attr)
                myMblite = p.get('metabolite')
                if myMblite not in my_metabolites_list:
                    my_metabolites_list.append(myMblite)
            # it is assume that the rawdatafilename is unique in each of the
            # plate grouping and polarity
            my_attrs[pi.get('rawdatafilename').split('.')[0]] = my_attr_list
        my_metabolites[usedop + '-' + platebarcode + '-' + polarity.lower()] = \
            my_metabolites_list
    return my_attrs, mydict


def generate_attrs_dict(plate):
    # using dictionaries of lists
    pos_attrs = defaultdict(list)
    neg_attrs = defaultdict(list)
    pos_metabolites = defaultdict(list)
    neg_metabolites = defaultdict(list)
    mydict = {}
    pos_attrs, mydict = generate_polarity_attrs_dict(
        plate, 'POSITIVE', pos_attrs, pos_metabolites, mydict)
    neg_attrs, mydict = generate_polarity_attrs_dict(
        plate, 'NEGATIVE', neg_attrs, neg_metabolites, mydict)
    return pos_attrs, neg_attrs, pos_metabolites, neg_metabolites, mydict


def write_out_to_file(plate, polarity, usedop, platebarcode, output_dir,
                      unique_attrs, unique_metabolite_identifiers, mydict):
    pos_injection = plate.find_all('injection', {'polarity': polarity})
    if len(pos_injection) > 0:
        filename = 'm_MTBLSXXX_' + usedop + '_' + platebarcode + '_' + polarity.lower() \
            + '_maf.txt'
        print("filename: ", filename)
        with open(os.path.join(output_dir, filename), 'w') as file_handler:
            # writing out the header
            file_handler.write('metabolite_identification')
            for ua in unique_attrs:
                for myattr in unique_attrs[ua]:
                    file_handler.write('\t' + ua + '[' + myattr + ']')
            # now the rest of the rows
            for myMetabolite in unique_metabolite_identifiers[
                    usedop + '-'
                    + platebarcode + '-' + polarity.lower()]:
                file_handler.write('\n' + myMetabolite)
                for ua in unique_attrs:
                    for myattr in unique_attrs[ua]:
                        mykey = myMetabolite + '-' + ua + '-' + myattr \
                            + '-' + polarity.lower() + '-' + usedop \
                            + '-' + platebarcode
                        if mykey in mydict:
                            file_handler.write('\t' + mydict[mykey])
                        else:
                            file_handler.write('\t')
        file_handler.close()
        complete_maf(os.path.join(output_dir, filename))


def complete_maf(maf_stub):

    # data = pd_modin.read_csv(maf_stub, sep='\t')
    data = pd.read_csv(maf_stub, sep='\t')

    data.insert(1, "database_identifier", "")
    data.insert(2, "chemical_formula", "")
    data.insert(3, "smiles", "")
    data.insert(4, "inchi", "")
    data.insert(5, "mass_to_charge", "")
    data.insert(6, "modifications", "")
    data.insert(7, "charge", "")
    data.insert(8, "retention_time", "")
    data.insert(9, "taxid", "")
    data.insert(10, "species", "")
    data.insert(11, "database", "")
    data.insert(12, "database_version", "")
    data.insert(13, "reliability", "")
    data.insert(14, "uri", "")
    data.insert(15, "search_engine", "")
    data.insert(16, "search_engine_score", "")

    data.to_csv(maf_stub, sep='\t', encoding='utf-8', index=False)


def add_sample_metadata(sample_info_file, input_study_file):
    """
    Given an ISA Study File s_study.txt resulting from a biocrates2isa conversion,
    Given a Sample Metadata File in tab separated format,
    The method augments the ISA Study File with
    :param sample_info_file:
    :param input_study_file:
    :return:
    """

    s_study_loc = os.path.join(DESTINATION_DIR, input_study_file)
    print("study file location:", s_study_loc)

    # isa_study_df = pd_modin.read_csv(S_STUDY_LOC, sep='\t')
    isa_study_df = pd.read_csv(s_study_loc, sep='\t')
    print("study file:", isa_study_df)

    sample_metadata_loc = os.path.join(SAMPLE_METADATA_INPUT_DIR, sample_info_file)
    print("sample metadata file location:", sample_metadata_loc)

    # sample_metadata_df = pd_modin.read_csv(SAMPLE_METADATA_LOC)
    sample_metadata_df = pd.read_csv(sample_metadata_loc)
    print("sample metadata: ", sample_metadata_df)

    # data.join(sample_desc, on='Characteristics[barcode identifier]')

    # result = data.join(sample_desc, on='Characteristics[barcode identifier]')

    # result = pd_modin.merge(data, sample_desc, on='Characteristics[barcode identifier]', left_index=True, how='outer')
    result_df = pd.merge(isa_study_df, sample_metadata_df, on='Characteristics[barcode identifier]',
                         left_index=True, how='outer')
    cols = result_df.columns.tolist()
    print(cols)

    result_df = result_df[['Source Name', 'Material Type', 'Characteristics[barcode identifier]', 'internal_ID',
                           'resolute_ID',
                           'Characteristics[Organism]', 'Term Source REF', 'Term Accession Number',
                           'cellLine', 'cellosaurusID', 'Characteristics[chemical compound]',
                           'Protocol REF_x', 'Date', 'Sample Name', 'Characteristics[Organism part]',
                           'Term Source REF.1',
                           'Term Accession Number.1',
                           'Factor value [cellNumber]', 'Factor value [replicate]',
                           'Factor value [extractionVolume, µl]'
                           ]]

    result_df['cellosaurusID'] = result_df['cellosaurusID'].str.replace('cellosaurus:CVCL_',
                                                                        'https://web.expasy.org/cellosaurus/CVCL_')

    result_df = result_df.rename(columns={'internal_ID': 'Characteristics[internal_ID]',
                                          'resolute_ID': 'Characteristics[resolute_ID]',
                                          'Characteristics[chemical compound]': 'Characteristics[qc element]',
                                          'cellLine': 'Characteristics[cell line]',
                                          'cellosaurusID': 'Term Accession Number',
                                          'Protocol REF_x': 'Protocol REF',
                                          'Characteristics[Organism part]':'Characteristics[material type]',
                                          'Material Type': 'Characteristics[specimen type]',
                                          'Factor value [cellNumber]': 'Factor Value[cell seeding density]',
                                          'Factor value [replicate]': 'Factor Value[replicate number]',
                                          'Factor value [extractionVolume, µl]': 'Factor Value[extraction volume]'
                                          })

    study_factor_names = "Study Factor Name\"" + "\t" + "\"cell seeding density\"" + "\t" + "\"replicate number\"" + \
                         "\t" + "\"extraction volume"

    replaceAll(DESTINATION_DIR + "/i_inv_biocrates.txt", "Study Factor Name", study_factor_names)

    replaceAll(DESTINATION_DIR + "/i_inv_biocrates.txt","Study File Name	s_study_biocrates.txt", "Study File Name	s_study_biocrates_augmented.txt")

    result_df.insert(9, "Term Source REF.2", "cellosaurus")

    result_df.insert(21, "Unit", "µl")

    result_df = result_df.rename(columns={'Term Source REF.1': 'Term Source REF',
                                          'Term Source REF.2': 'Term Source REF',
                                          'Term Accession Number.1': 'Term Accession Number'
                                          })
    try:
        with open(os.path.join(DESTINATION_DIR, "s_study_biocrates_augmented.txt"), "w+") as isa_study_plus:
            result_df.to_csv(isa_study_plus, sep="\t", encoding='utf-8', index=False)
    except IOError as ioe:
        print("error: ", ioe)


def generate_maf_stub(biocrates_filename,inputdir, outputdir):
    """
    Given a biocrates xml file, the method
    extracts information to generate one or more Metabolite Assignment File(s).
    :param biocrates_filename:
    :param folder_name:
    :return: maf_success: True or False
    """

    maf_success = True
    try:

        output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  outputdir)

        # create the output directory if it does not exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # file = sys.argv[1]
        # file = biocrates_filename
        input_file = os.path.join(inputdir, biocrates_filename)
        # open and read up the file
        handler = open(input_file).read()
        soup = BeautifulSoup(handler, features="lxml")

        # get all the plates
        plates = soup.find_all('plate')
        for plate in plates:
            usedop = plate.get('usedop')
            # print(usedop)
            platebarcode = plate.get('platebarcode')
            # extracting the the distinct column labels, metabolites,
            # and rawdatafilename collect the data into a dictionary
            pos_attrs, neg_attrs, pos_metabolites, neg_metabolites, mydict = \
                generate_attrs_dict(plate)
            # and start creating the sample tab files
            write_out_to_file(plate, 'POSITIVE', usedop, platebarcode, output_dir,
                              pos_attrs, pos_metabolites, mydict)

            write_out_to_file(plate, 'NEGATIVE', usedop, platebarcode, output_dir,
                              neg_attrs, neg_metabolites, mydict)

    except Exception as pb_found:
        logger.error("isatools.convert.biocrates2isatab.generate_maf_stub: ", pb_found)
        print("something went wrong during conversion:", pb_found)
        maf_success = False

    return maf_success


if __name__ == "__main__":
    start = time()
    biocrates_to_isatab_convert(biocrates_filename='biocrates-merged-output.xml',  inputdir=BIOCRATES_DIR, outputdir=DESTINATION_DIR)
    generate_maf_stub(biocrates_filename='biocrates-merged-output.xml', inputdir=BIOCRATES_DIR, outputdir=DESTINATION_DIR)
    add_sample_metadata('EX0003_sample_metadata.csv', 's_study_biocrates.txt')
    end = time()
    print('The conversion took {:.2f} s.'.format(end - start))

# parseSample(sys.argv[1])
# uncomment to run test
# merged = merge_biocrates_files("/Users/Philippe/Documents/git/biocrates-DATA/Biocrates-TUM/input-Biocrates-XML-files/all-biocrates-xml-files/")

# Conc_R100028_export_incl_information_20200309.xml