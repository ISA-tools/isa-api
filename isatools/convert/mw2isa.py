__author__ = 'prs'

import csv
import re

import urllib2
from bs4 import BeautifulSoup

from itertools import islice

# a method to obtain a block of line between a start and an end marker
#this will be invoked to obtain raw data, metabolite identification,metabolite annotation and possible study factors
#parameters are a filehandle and 2 strings allowing the specify the section brackets
def getblock(container, startMarker, endMarker):
    block = []
    for line in container:
        if line.strip() == startMarker:
            break
    for line in container:
        if line.strip() == endMarker:
            break
        block.append(line)
    return block


#a method to obtain the nature of the technology used in the analysis from a Metabolomics Workbench Header line
#the method takes one parameter as input: a filehandle
#the method returns a string holding the ISA technology type
def get_assay_type(container):
    assay_type = ""
    for line in container:
        if str(line).startswith("#ANALYSIS TYPE: MS;"):
            assay_type = "mass spectrometry"
        elif str(line).startswith("#ANALYSIS TYPE: NMR;"):
            assay_type = "nmr spectroscopy"
    print(assay_type)
    return assay_type


def write_assay(assay_filename, assayrecords, assay_wf_header):
    # print "from write function:", assay_filename
    assayfilepath = "/Users/Philippe/Documents/git/MW2ISA/" + "a_" + studyID + "_" + assay_filename + '.txt'
    assay_file = open(assayfilepath, 'w')
    #assay_file.write('\t'.join(assay_wf_header))
    # element=""
    for element in assay_wf_header:
        assay_file.write('"{0}"'.format(element))
        assay_file.write('\t')
        # print '"{0}"'.format(element)
    assay_file.write("\n")

    # each=[]
    for key in assayrecords:
        # print key,str(assayrecords[key][0])
        # key=""
        assayrecords[key][0][0] = key
        assayrecords[key][0][2] = key
        assayrecords[key][0][8] = key
        assayrecords[key][0][13] = key
        for item in assayrecords[key][0]:
            assay_file.write('"{0}"'.format(item))
            assay_file.write('\t')
        assay_file.write("\n")
    assay_file.write("\n")


#a method to create Metabolights formated data files which will be referenced in the ISA-Tab document
#the method takes 3 parameters as input: a filehandle, a MW identifier for the study, a MW identifier for the analysis
#the method return nothing but creates a raw signal quantification file and a metabolite assignment file.
def create_data_files(f, studyID, analysisID):
    print("file to download: ", f)

    dlurl = urllib2.urlopen(f)
    #saving a remote file to local drive
    localcopy = open(studyID + "_" + analysisID + ".txt", 'w+')
    localcopy.write(dlurl.read())

    #the combination of MW study ID and analysis ID ensure unicity of file name.
    raw_data_file_name = 'data/' + studyID + '_' + analysisID + '_raw_data.txt'
    with open(raw_data_file_name, 'w+') as rawdata:
        dlurl = urllib2.urlopen(f)
        at = get_assay_type(dlurl)
        if at == "mass spectrometry":
            dlurl = urllib2.urlopen(f)
            rawblock = getblock(dlurl, "MS_ALL_DATA_START", "MS_ALL_DATA_END")
            rawdata.writelines("%s" % item for item in rawblock)
        elif at == "nmr spectroscopy":
            dlurl = urllib2.urlopen(f)
            rawblock = getblock(dlurl, "NMR_ALL_DATA_START", "NMR_ALL_DATA_END")
            rawdata.writelines("%s" % item for item in rawblock)

    maf_file_name = 'data/' + studyID + '_' + analysisID + '_maf.txt'
    with open(maf_file_name, 'w+')  as mafdata:
        dlurl = urllib2.urlopen(f)
        at = get_assay_type(dlurl)
        if at == "mass spectrometry":
            dlurl = urllib2.urlopen(f)
            mafblock = getblock(dlurl, "MS_METABOLITE_DATA_START", "MS_METABOLITE_DATA_END")
            mafdata.writelines("%s" % item for item in mafblock)

        elif at == "nmr spectroscopy":
            dlurl = urllib2.urlopen(f)
            mafblock = getblock(dlurl, "NMR_METABOLITE_DATA_START", "NMR_METABOLITE_DATA_END")
            mafdata.writelines("%s" % item for item in mafblock)


#a method to create ISA assay tables from an Metabolomics Workbench Study Identifier
#the method takes 3 parameters as input: a filehandle, a MW identifier for the study, a MW identifier for the analysis
#the method return nothing but creates as many as ISA assay files.
def create_assay_file(container, studyID, analysisID):
    assay_filename = "a_" + str(studyID) + '_' + str(analysisID) + ".txt"

    IncomingData = []
    for line in container:
        lines = str(line).split('\t')
        IncomingData.append(lines)

    at = get_assay_type(container)

    if at == "nmr spectroscopy":
        create_nmr_assay_records(container)

    elif at == "mass spectrometry":
        create_ms_assay_records(container)

    return assay_filename


#a method to create an ISA assay table for NMR records
#the method takes a filehandle as input
def create_nmr_assay_records(f):
    pv_nmrexprt_type = ""
    pv_sw_version = ""
    pv_field_freq_lock = ""
    pv_std_concentration = ""
    pv_nmr_frequency = ""
    pv_nmr_probe = ""
    pv_nmr_solvent = ""
    pv_nmr_tube_size = ""
    pv_nmr_shimming_method = ""
    pv_nmr_pulse_sequence = ""
    pv_water_suppression = ""
    pv_pulse_width = ""
    pv_power_level = ""
    pv_receiver_gain = ""
    pv_offset_frequency = ""
    pv_chemical_shift_ref_compound = ""
    pv_nmr_temp = ""
    pv_numscan = ""
    pv_acquisitiontime = ""
    pv_relaxationdelay = ""
    pv_spectralwidth = ""
    pv_acquired_data_points = ""
    pv_zerofilling = ""
    pv_apodization = ""
    pv_baseline_correction_method = ""

    raw_data_file = ""
    maf_file = ""

    for row in lol:
        if "#ANALYSIS TYPE: NMR" in row[0]:
            tt = "nmr spectroscopy"
        if "NM:FIELD_FREQUENCY_LOCK" in row[0]:
            pv_field_freq_lock = row[1]
        if "NM:STANDARD_CONCENTRATION" in row[0]:
            pv_std_concentration = row[1]
        if "NM:SPECTROMETER_FREQUENCY" in row[0]:
            pv_spectrometer_freq = row[1]
        if "NM:NMR_PROBE" in row[0]:
            pv_nmr_probe = row[1]
        if "NM:NMR_SOLVENT" in row[0]:
            pv_nmr_solvent = row[1]
        if "NM:NMR_TUBE_SIZE" in row[0]:
            pv_nmr_tube_size = row[1]
        if "NM:SHIMMING_METHOD" in row[0]:
            pv_nmr_shimming_method = row[1]
        if "NM:PULSE_SEQUENCE" in row[0]:
            pv_nmr_pulse_sequence = row[1]
        if "NM:WATER_SUPPRESSION" in row[0]:
            pv_water_suppression = row[1]
        if "NM:PULSE_WIDTH" in row[0]:
            pv_pulse_width = row[1]
        if "NM:POWER_LEVEL" in row[0]:
            pv_power_level = row[1]
        if "NM:RECEIVER_GAIN" in row[0]:
            pv_receiver_gain = row[1]
        if "NM:OFFSET_FREQUENCY" in row[0]:
            pv_offset_frequency = row[1]
        if "NM:CHEMICAL_SHIFT_REF_CPD " in row[0]:
            pv_chemical_shift_ref_compound = row[1]
        if "NM:TEMPERATURE" in row[0]:
            pv_nmr_temp = row[1]
        if "NM:NUMBER_OF_SCANS" in row[0]:
            pv_numscan = row[1]
        if "NM:DUMMY_SCANS" in row[0]:
            pv_sw_version = row[1]
        if "NM:ACQUISITION_TIME" in row[0]:
            pv_acquisitiontime = row[1]
        if "NM:RELAXATION_DELAY" in row[0]:
            pv_relaxationdelay = row[1]
        if "NM:SPECTRAL_WIDTH" in row[0]:
            pv_spectralwidth = row[1]
        if "NM:NUM_DATA_POINTS_ACQUIRED" in row[0]:
            pv_acquired_data_points = row[1]
        if "NM:REAL_DATA_POINTS" in row[0]:
            pv_sw_version = row[1]
        if "NM:ZERO_FILLING" in row[0]:
            pv_zerofilling = row[1]
        if "NM:APODIZATION" in row[0]:
            pv_apodization = row[1]
        if "NM:BASELINE_CORRECTION_METHOD" in row[0]:
            pv_baseline_correction_method = row[1]
        if "NM:CHEMICAL_SHIFT_REF_STD" in row[0]:
            pv_chemical_shift_ref_compound = row[1]
        if "NMR:NMR_EXPERIMENT_TYPE" in row[0]:
            pv_nmrexprt_type = row[1]
        if "AN:ACQUISITION_PARAMETERS_FILE" in row[0]:
            pv_ms_acquisitionfile = row[1]
            protocol_files[3] = row[1]

        if "AN:SOFTWARE_VERSION" in row[0]:
            pv_sw_version = row[1]

        print(pv_sw_version)


#a method to create an ISA assay table for MS records
#the method takes a filehandle as input
def create_ms_assay_records(input, studyID, analysisID, fv_records):
    # print "study id invoked:", studyID, analysisID
    pv_ms_type = ""
    pv_ion_mode = ""
    pv_instrument = ""
    pv_ms_acquisitionfile = ""
    pv_ms_analysisfile = ""
    ms_protocol_type = ""
    raw_data_file = ""
    maf_file = ""

    assay_wf_header = ["Sample Name",
                       "Protocol REF",
                       "Extract Name",
                       "Protocol REF",
                       "Parameter Value[mass spectrometry instrument]",
                       "Parameter Value[injection type]",
                       "Parameter Value[ionization mode]",
                       "Parameter Value[acquisition file]",
                       "MS Assay Name",
                       "Raw Spectral Data File",
                       "Protocol REF",
                       "Parameter Value[analysis file]",
                       "Parameter Value[software]",
                       "Data Transformation Name",
                       "Derived Spectral Data File"]

    inputFile = urllib2.urlopen(str(input))

    for row in inputFile:

        row = row.rstrip()
        row = row.split('\t')

        #if len(row)>1:

        if "AN:ANALYSIS_TYPE" in row[0]:
            ms_protocol_type = row[1].rstrip()

        if "AN:INSTRUMENT_NAME" in row[0]:
            pv_instrument = row[1]

        if "MS:ION_MODE" in row[0]:
            pv_ion_mode = row[1]

        if "MS:MS_TYPE" in row[0]:
            pv_ms_type = row[1]

        if "AN:ACQUISITION_PARAMETERS_FILE" in row[0]:
            pv_ms_acquisitionfile = row[1]
            protocol_files[3] = row[1]

        if "AN:SOFTWARE_VERSION" in row[0]:
            pv_sw_version = row[1]
        else:
            pv_sw_version = ""

        if "MS_ALL_DATA:UNITS" in row[0] and len(row) > 1:
            ms_rawdata_qt = row[1]
        else:
            ms_rawdata_qt = "NA"

        if "MS_ALL_DATA_START" in row[0]:
            raw_data_file = str(studyID) + "_" + str(analysisID) + "_raw_data.txt"
            print(raw_data_file)

        if "MS_METABOLITE_DATA:UNITS" in row[0] and len(row) > 1:
            ms_maf_qt = row[1]
        else:
            ms_maf_qt = "NA"

        # if "MS_METABOLITE_DATA_START" in row[0]:
        maf_file = str(studyID) + "_" + str(analysisID) + "_maf_data.txt"
        # print maf_file
    # print "MAF File", maf_file
    #print "assay workflow: ", str(assay_wf_record)
    assay_wf_backbone_record = ["", "metabolite extraction","","data acquisition", pv_instrument, pv_ms_type, pv_ion_mode,
                                pv_ms_acquisitionfile, "", raw_data_file, "identification", pv_ms_analysisfile,
                                pv_sw_version, "", maf_file]
    # print "assay workflow: ", str(assay_wf_backbone_record)
    #assayrecords.append(assay_wf_record)
    #creating assay records


    longrecords = {}
    full_assay_record = assay_wf_backbone_record
    for fv_record in fv_records:

        #print fv_record[3]

        # if fv_record[3] in longrecords.keys():
        #
        #     full_assay_record[0] = fv_record[3]
        #     full_assay_record[6] = fv_record[3]
        #     full_assay_record[12] = fv_record[3]
        #     longrecords[fv_record[3]].append(full_assay_record)
        #     # print "current record:",full_assay_record
        # else:

            full_assay_record[0] = fv_record[3]
            full_assay_record[8] = fv_record[3]
            full_assay_record[13] = fv_record[3]
            # print "new key, new record:",full_assay_record
            longrecords[fv_record[3]]= [full_assay_record]
            # print "now storing:",longrecords[fv_record[3]]
        # longrecords[fv_record[0]] = longrecords[fv_record[0]].append(full_assay_record)
        # print "here", longrecords

    # print longrecords
    return longrecords, assay_wf_header


def get_organism_with_Taxid(lol):
    species = ""
    taxID = ""
    for row in lol:
        if "SU:SUBJECT_SPECIES" in row[0]:
            species = row[1]

        if "SU:TAXONOMY_ID" in row[0]:
            taxID = row[1]
            # records.insert(1,"NCBITax")
            # records.insert(2,row[1])
    #print "species & TaxID :", species, taxID
    return species, taxID


def get_fv_records(lol):
    records = []
    factors = {}
    for row in lol:
        if "SUBJECT_SAMPLE_FACTORS" in str(row) and "#" not in str(row):

            if len(row) > 2:
                newrecord = []
                if row[1] != "-":
                    newrecord.append(row[1])
                else:
                    newrecord.append(row[2])

                newrecord.append(row[2])

                if "|" in row[3]:
                    for item in row[3].split("|"):

                        factor, value = item.split(":")
                        # print "Factor Value value:", value
                        newrecord.append(value)

                        if factor in factors:
                            factors[factor] = factors[factor] + 1
                        else:
                            factors[factor] = 1

                else:
                    elements = row[3].split(":")
                    factor = elements[0]
                    if len(elements) > 2:
                        value = elements[1] + elements[2]
                    else:
                        value = elements[1]

                    if factor in factors:
                        factors[factor] = factors[factor] + 1
                    else:
                        factors[factor] = 1

                    newrecord.append(value)

                #print newrecord
                records.append(newrecord)

            restOfrecordheader = []
            for key in factors.keys():
                restOfrecordheader.append("Factor Value[" + key + "]")

    return records, factors, restOfrecordheader


def get_mwfile_as_Lol(inputFile):
    #    inputFile= urllib2.urlopen(downLoadURI).read()
    #   inputFile=inputFile.split('\n')
    mwAslol = []
    for line in inputFile:
        lines = line.split('\t')
        mwAslol.append(lines)

    return mwAslol


#a method to write an ISA investigation file
#the method takes an array of string as parameters, a dictionary of factors, an array of protocol descriptors
def write_investigation(study_accnum, study_title, study_subdate, study_releasedate, study_desc, study_design,
                        study_factors, mt, tt, isa_assay_names, protocol_types, protocol_descriptions, protocol_files,
                        study_person_lastname, study_person_firstname, study_person_email, study_person_phone,
                        study_person_fax, study_person_address, study_person_affiliation, study_funder):
    inv_filename = "i_" + study_accnum + ".txt"
    invfilepath = "/Users/Philippe/Documents/git/MW2ISA/" + inv_filename
    inv_file = open(invfilepath, 'w')
    inv_file.write('"ONTOLOGY SOURCE REFERENCE"\n')
    inv_file.write("\"Term Source Name\"\t\"OBI\"\t\"PSI-MS\"\n")
    inv_file.write("\"Term Source File\"\t\"OBI\"\t\"PSI-MS\"\n")
    inv_file.write("\"Term Source Version\"\t\"OBI\"\t\"PSI-MS\"\n")
    inv_file.write(
        "\"Term Source Description\"\t\"The Ontology for Biomedical Investigation\"\t\"PSI Mass Spectrometry\"\n")
    inv_file.write(""""INVESTIGATION"
"Investigation Identifier"
"Investigation Title"
"Investigation Description"
"Investigation Submission Date"
"Investigation Public Release Date"
"INVESTIGATION PUBLICATIONS"
"Investigation PubMed ID"
"Investigation Publication DOI"
"Investigation Publication Author List"
"Investigation Publication Title"
"Investigation Publication Status"
"Investigation Publication Status Term Accession Number"
"Investigation Publication Status Term Source REF"
"INVESTIGATION CONTACTS"
"Investigation Person Last Name"
"Investigation Person First Name"
"Investigation Person Mid Initials"
"Investigation Person Email"
"Investigation Person Phone"
"Investigation Person Fax"
"Investigation Person Address"
"Investigation Person Affiliation"
"Investigation Person Roles"
"Investigation Person Roles Term Accession Number"
"Investigation Person Roles Term Source REF"

"STUDY"
""")

    inv_file.write('\"Study Identifier\"\t"MTBLS_MW_' + study_accnum + '\"\n')
    inv_file.write('\"Comment[MW AccNum]\"\t"' + study_accnum + '\"\n')
    inv_file.write('\"Study Title\"\t"' + study_title + '\"\n')
    inv_file.write('\"Study Submission Date\"\t"' + study_subdate + '\"\n')
    inv_file.write('\"Study Public Release Date\"\t"' + study_releasedate + '\"\n')
    inv_file.write('\"Study Description\"\t"' + study_desc + '\"\n')
    inv_file.write('\"Study File Name\"\t"' + "s_" + study_accnum + ".txt" + '\"\n')

    inv_file.write('"STUDY DESIGN DESCRIPTORS"\n')
    inv_file.write('\"Study Design Type\"\t"' + study_design + '\"\n')
    inv_file.write(""""Study Design Type Term Accession Number"
"Study Design Type Term Source REF"
"STUDY PUBLICATIONS"
"Study PubMed ID"
"Study Publication DOI"
"Study Publication Author List"
"Study Publication Title"
"Study Publication Status"
"Study Publication Status Term Accession Number"
"Study Publication Status Term Source REF"
"STUDY FACTORS"
""")
    inv_file.write('\"Study Factor Name\"')

    for key in study_factors.keys():
        inv_file.write('\t\"' + key + '\"')

    inv_file.write("""
"Study Factor Type"
"Study Factor Type Term Accession Number"
"Study Factor Type Term Source REF"
"STUDY ASSAYS"
""")

    inv_file.write('\"Study Assay Measurement Type\"')
    for item in isa_assay_names:
        inv_file.write('\t\"' + mt + '\"')

    inv_file.write("""
"Study Assay Measurement Type Term Accession Number"
"Study Assay Measurement Type Term Source REF"
""")

    inv_file.write('\"Study Assay Technology Type\"')
    for item in isa_assay_names:
        inv_file.write('\t\"' + technology_type + '\"')

    inv_file.write("""
"Study Assay Technology Type Term Accession Number"
"Study Assay Technology Type Term Source REF"
"Study Assay Technology Platform"
""")

    inv_file.write('\"Study Assay File Name\"')
    for item in isa_assay_names:
        inv_file.write('\t\"' + item + '\"')

    inv_file.write("""
"STUDY PROTOCOLS"
"Study Protocol Name\"""""")

    for j in protocol_types:
        inv_file.write('\t')
        inv_file.write('"{0}"'.format(j))
    inv_file.write("\n")

    inv_file.write(""""Study Protocol Type\"""""")
    for j in protocol_types:
        inv_file.write('\t')
        inv_file.write('"{0}"'.format(j))
    inv_file.write("\n")

    inv_file.write(""""Study Protocol Type Term Accession Number"\t""\t""\t""\t""\t""
"Study Protocol Type Term Source REF"\t""\t""\t""\t""\t""
""""")

    inv_file.write(""""Study Protocol Description\"""""")
    for j in protocol_descriptions:
        inv_file.write('\t')
        inv_file.write('"{0}"'.format(j))
    inv_file.write("\n")

    inv_file.write(""""Study Protocol URI\"""""")
    for j in protocol_files:
        inv_file.write('\t')
        inv_file.write('"{0}"'.format(j))
    inv_file.write("\n")

    inv_file.write(""""Study Protocol Version"
"Study Protocol Parameters Name"
"Study Protocol Parameters Name Term Accession Number"
"Study Protocol Parameters Name Term Source REF"
"Study Protocol Components Name"
"Study Protocol Components Type"
"Study Protocol Components Type Term Accession Number"
"Study Protocol Components Type Term Source REF"
"STUDY CONTACTS"
""")

    inv_file.write('"Study Person Last Name"' + '\t\"' + study_person_lastname + '\"\n')
    inv_file.write('"Study Person First Name"' + '\t\"' + study_person_firstname + '\"\n')
    inv_file.write('"Study Person Mid Initials"' + '\t""\n')
    inv_file.write('"Study Person Email"' + '\t\"' + study_person_email + '\"\n')
    inv_file.write('"Study Person Phone"' + '\t\"' + study_person_phone + '\"\n')
    inv_file.write('"Study Person Fax"' + '\t\"' + study_person_fax + '\"\n')
    inv_file.write('"Study Person Affiliation"' + '\t\"' + study_person_affiliation + '\"\n')
    inv_file.write('"Study Person Address"' + '\t\"' + study_person_address + '\"\n')
    inv_file.write('\"Study Person Roles\"' + '\t\"' + 'submitter' + '\"\n')
    inv_file.write(""""Study Person Roles Term Accession Number"
"Study Person Roles Term Source REF"
""")
    inv_file.write('"Comment[Grant Numbers]"' + '\t\"' + study_funder + '\"\n')

    inv_file.close()


#a method to write an ISA study file
#a

def write_study_file(study_accnum, studyfileheader, longrecords):
    study_filename = "s_" + study_accnum + ".txt"
    studyfilepath = "/Users/Philippe/Documents/git/MW2ISA/" + study_filename
    study_file = open(studyfilepath, 'w')

    #write study header to file
    #studyfileheader=studyfileheader+factorheader
    for element in studyfileheader:
        study_file.write('"{0}"'.format(element))
        study_file.write('\t')
    study_file.write("\n")

    #writing study records to file
    for each in longrecords:
        #print "each:",each

        #this is to reorder fields following the merge
        each[0], each[1], each[2], each[3] = each[3], each[0], each[1], each[2]
        each.insert(4, "sample collection")
        each.insert(3, "")
        each[4], each[5] = each[5], each[4]
        each.insert(1,"specimen")
        temprecord = '\t'.join(map(str, each)).encode('utf-8').strip()
        #print "temp",temprecord
        study_file.write(temprecord)
        study_file.write("\n")

    study_file.close()


#MAIN METHOD:

baseurl = "http://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&DataMode="
studyID = "ST000102"
tt = "NMR"

pageurl = baseurl + tt + "Data&StudyID=" + studyID + "&StudyType=" + tt + "&ResultType=1#DataTabs"
print("pageurl:", pageurl)

concaturl1 = "Data&StudyID="
concaturl2 = "&StudyType=" + tt + "&ResultType=1#DataTabs"
url = "http://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&DataMode=NMRData&StudyID=ST000053&StudyType=NMR&ResultType=1#DataTabs"  # change to whatever your url is

page = urllib2.urlopen(pageurl).read()
soup = BeautifulSoup(page)
AnalysisParamTable = soup.findAll("table", {'class': "datatable2"})

analysisID = ""
isa_assay_names = []
assay_types = []

isa_assay_names_with_dlurl = {}

for table in AnalysisParamTable:
    for row in table:
        if "Analysis ID" in str(row):
            tds = row.find_all('td')
            analysisID = tds[1].text

            print("ID: ", analysisID)

            downLoadURI = "http://www.metabolomicsworkbench.org/data/study_textformat_view.php?STUDY_ID=" + studyID + "&ANALYSIS_ID="

            downLoadURI = downLoadURI + analysisID + "&MODE=d"

            create_data_files(downLoadURI, studyID, analysisID)

            isa_assay_names.append(create_assay_file(downLoadURI, studyID, analysisID))
            assay_types.append(create_assay_file(downLoadURI, studyID, analysisID)[1])

            isa_assay_names_with_dlurl[analysisID] = downLoadURI

print("all file names:", isa_assay_names)
print("all assay types:", assay_types)

inputFile = urllib2.urlopen(downLoadURI).read()
inputFile = inputFile.split('\n')

thisFileContent = get_mwfile_as_Lol(inputFile)


study_title = ""
study_desc = ""
study_design = ""
study_subdate = ""
study_releasedate = ""
study_accnum = ""
study_funder = ""

ms_protocol = ""
treat_protocol = ""
plant_treatment_protocol = ""
plant_plot_design = ""
plant_light_period = ""
plant_humidity = ""
plant_temperature = ""
plant_nutriregime = ""
plant_harvest_method = ""
quenching_method = ""

collect_protocol = ""
sampleprep_protocol = ""
chromatography_protocol = ""

protocol_names = ["", "", "", "", ""]
protocol_types = ["sample collection", "treatment","metabolite extraction", "sample preparation", "chromatography", "data acquisition","identification"]
protocol_descriptions = ["", "", "", "", ""]
protocol_parameters = []
protocol_files = ["", "", "", "", ""]

study_person_firstname = ""
study_person_lastname = ""
study_person_email = ""
study_person_affiliation = ""
study_person_address = ""
study_person_phone = ""
study_person_fax = ""

material_type = ""
sample_type = ""
organism = ""


#baserecord = []
fv_recordheader = []
basestudysamplerecordheader = ["Source Name","Material Type", "Characteristics[Organism]", "Term Accession Number", "Term Source REF",
                               "Protocol REF", "Sample Name"]

study_records = []
study_factors = {}

study_records, study_factors, fv_record_header = get_fv_records(thisFileContent)

# print "fv header", fv_record_header

species, taxonID = get_organism_with_Taxid(thisFileContent)

for each_record in study_records:
    each_record.insert(0, species)
    each_record.insert(1, taxonID)

mt = "metabolite profiling"

for row in thisFileContent:

    # if "#METABOLOMICS WORKBENCH TEXT OUTPUT STUDY_ID:" in row[0]:
    #
    #    m = re.search('#METABOLOMICS WORKBENCH TEXT OUTPUT STUDY_ID:(.+?) ANALYSIS_ID:', row[0])
    #    if m:
    #        study_accnum=m.group(1)

    if row[0].find('ST:STUDY_TITLE') != -1:
        study_title = study_title + row[1]

    if row[0].find('ST:STUDY_TYPE') != -1:
        study_design = row[1]

    if row[0].find('ST:STUDY_SUMMARY') != -1:
        study_desc = study_desc + " " + row[1]

    if row[0].find('ST:LAST_NAME') != -1:
        study_person_lastname = row[1]

    if row[0].find('ST:FIRST_NAME') != -1:
        study_person_firstname = row[1]

    if row[0].find('ST:EMAIL') != -1:
        study_person_email = row[1]

    if row[0].find('ST:PHONE') != -1:
        study_person_phone = row[1]

    if row[0].find('ST:SUBMIT_DATE') != -1:
        study_subdate = row[1]

    if row[0].find('ST:INSTITUTE') != -1:
        study_person_affiliation = row[1]

    if row[0].find('ST:DEPARTMENT') != -1:
        study_person_affiliation = study_person_affiliation + ", " + row[1]

    if row[0].find('ST:LABORATORY') != -1:
        study_person_affiliation = study_person_affiliation + ", " + row[1]

    if row[0].find('PR:ADDRESS') != -1:
        study_person_address = row[1]

    if row[0].find('PR:FUNDING_SOURCE') != -1:
        study_funder = study_funder + " " + row[1]

    if row[0].find('CO:COLLECTION_SUMMARY') != -1:
        collect_protocol = collect_protocol + " " + row[1]

    if row[0].find('TR:TREATMENT_SUMMARY') != -1:
        treat_protocol = treat_protocol + " " + row[1]

    if row[0].find('CH:CHROMATOGRAPHY_SUMMARY') != -1:
        chromatography_protocol = chromatography_protocol + " " + row[1]

    if row[0].find('TR:PLANT_GROWTH_SUPPORT') != -1:
        plant_treatment_prtcl = plant_treatment_prtcl + " " + row[1]

    if row[0].find('TR:PLANT_HARVEST_SUPPORT') != -1:
        plant_harvest_method = plant_harvest_method + " " + row[1]

    if row[0].find('TR:PLANT_PLOT_DESIGN') != -1:
        plant_plot_design = plant_plot_design + " " + row[1]

    if row[0].find('TR:PLANT_LIGHT_PERIOD') != -1:
        plant_light_period = plant_light_period + " " + row[1]

    if row[0].find('TR:PLANT_TEMP') != -1:
        plant_temperature = plant_temperature + " " + row[1]

    if row[0].find('TR:PLANT_NUTRITIONAL_REGIME') != -1:
        plant_nutriregime = plant_nutriregime + " " + row[1]

    if row[0].find('TR:PLANT_METAB_QUENCH_METHOD') != -1:
        quenching_method = quenching_method + " " + row[1]

    if row[0].find('SP:SAMPLEPREP_SUMMARY') != -1:
        sampleprep_protocol = sampleprep_protocol + " " + row[1]

    if row[0].find('TR:TREATMENT_PROTOCOL_FILENAME') != -1:
        protocol_files[1] = row[1]

    if row[0].find('SP:SAMPLEPREP_PROTOCOL_FILENAME') != -1:
        protocol_files[2] = row[1]

protocol_descriptions[0] = collect_protocol
protocol_descriptions[1] = treat_protocol
protocol_descriptions[2] = sampleprep_protocol

studyfileheader = basestudysamplerecordheader + fv_record_header

# print "study file header:", studyfileheader

# assay_records=[]
# for item in isa_assay_names:
# #assay_file_name=create_assay_file(lol,studyID,analysisID)
#     lol=get_mwfile_as_Lol()
#     assay_records,assay_header = create_ms_assay_records(lol,studyID,analysisID,study_records)
#     print "item:",item
#     print assay_header
#     print assay_records
#
#     write_assay(item,assay_records,assay_header)


for key in isa_assay_names_with_dlurl:
    # print "element:", key
    file = get_mwfile_as_Lol(isa_assay_names_with_dlurl[key])
    print("file to read: ", isa_assay_names_with_dlurl[key])

    assay_records, assay_header = create_ms_assay_records(isa_assay_names_with_dlurl[key], studyID, key, study_records)
    technology_type = "mass spectrometry"
    # print assay_header
    # print assay_records
    write_assay(key, assay_records, assay_header)

    #technology_type = get_assay_type(thisFileContent)
    #print "tech and measurement", technology_type

write_investigation(studyID, study_title, study_subdate, study_releasedate, study_desc, study_design, study_factors,
                    mt,technology_type, isa_assay_names, protocol_types, protocol_descriptions, protocol_files,
                    study_person_lastname, study_person_firstname, study_person_email, study_person_phone,
                    study_person_fax, study_person_address, study_person_affiliation, study_funder)

write_study_file(studyID, studyfileheader, study_records)




#
# if technology_type == "mass spectrometry":
#     create_ms_assay_records(lol,fv_records)
#
# elif technology_type == "nmr spectroscopy":
#     create_nmr_assay_records(lol)












