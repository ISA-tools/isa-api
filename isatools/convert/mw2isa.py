from urllib.request import urlopen
from bs4 import BeautifulSoup
from isatools import isatab
from isatools.model.v1 import *
from datetime import date
from collections import defaultdict
import urllib
import json
import ftplib
import os.path
import re
import logging


__author__ = 'proccaserra@gmail.com'

# a method to obtain a block of line between a start and an end marker
# this will be invoked to obtain raw data, metabolite identification,metabolite annotation and possible study factors
# parameters are a filehandle and 2 strings allowing the specify the section brackets



def getblock(container, start_marker, end_marker):
    try:
        begin = False
        block = []
        lines = str(container).split('\\n')
        # print("lines", str(lines),"\n")
        # lineElements = []
        for line in lines:
            # print("LINE:", line)
            line_elements = line.split('\\t')
            # print("STUFF",line_elements)
            if start_marker in str(line):
                # print("start", line)
                begin = True
            elif end_marker in str(line):
                # print("end", line)
                begin = False

            if begin:
                block.append(line_elements)
        # print("BLOCK",block)
        return block

    except Exception as e:
        logging.exception(e)
        print("Error: in getblock() method, situation not recognized")


# a method of download Metabolomics Workbench archived data from their anonymous FTP site
# input: a valid Metabolomics Workbench study accession number that should follow this pattern ^ST\d+[6]

def get_archived_file(mw_study_id):
        success = True
        archive2download = mw_study_id + ".zip"

        try:
            ftp = ftplib.FTP("metabolomicsworkbench.org")
            ftp.login()
            ftp.cwd('Studies')
            ftp.retrlines('LIST')
            ftp.retrbinary("RETR " + archive2download, open(archive2download, 'wb').write)
            ftp.close()
            return success

        except ConnectionRefusedError:
            print("connection refused \n")
        except FileNotFoundError:
            print("file not found on server \n")
        else:
            success = False
            # print("someone broke the internet")
            return success

# a method to create an EBI Metabolights MAF file from Metabolomics Workbench REST API over data and metabolites
# input: a valid Metabolomics Workbench study accession number that should follow this pattern ^ST\d+[6]


def generate_maf_file(write_dir,mw_study_id, mw_analysis_id):
    try:
        data_url = "http://www.metabolomicsworkbench.org/rest/study/study_id/" + mw_study_id + "/data"
        metabolites_url = "http://www.metabolomicsworkbench.org/rest/study/study_id/" + mw_study_id + "/metabolites"

        with urllib.request.urlopen(data_url) as url:
            data_response = url.read().decode('utf8')
            data = json.loads(data_response)

        with urllib.request.urlopen(metabolites_url) as url:
            metabolites_response = url.read().decode('utf8')
            metabolites = json.loads(metabolites_response)

        dd = defaultdict(list)
        if len(metabolites) != 0 or len(data) != 0:
            print("generating  maf_file from json API")
            for d in (metabolites, data):
                # you can list as many input dicts as you want here
                for key, value in d.items():
                    dd[key].append(value)

            # merging the 2 json feeds and removing duplicated key, since values are always the same
            for k, v in dd.items():
                # print({k: {i: j for x in v for i, j in x.items()}})
                dd[k] = {i: j for x in v for i, j in x.items()}

            if "other_id" in dd.items():
                data_rec_header = "metabolite number" + "\t" + "metabolite name" \
                                  + "\t" + "metabolite identifier" \
                                  + "\t" + "pubchem identifier" \
                                  + "\t" + "other id" \
                                  + "\t" + "other id type" \
                                  + '\t' + \
                                  ("(" + dd["1"]["units"] + ')\t').join(dd["1"]["DATA"].keys()) \
                                  + ("(" + dd["1"]["units"] + ")")

            elif "pubchem_id" in dd.items() :
                data_rec_header = "metabolite number" + "\t" + "metabolite name" \
                                  + "\t" + "metabolite identifier" \
                                  + "\t" + "pubchem identifier" \
                                  + '\t' + \
                                  ("(" + dd["1"]["units"] + ')\t').join(dd["1"]["DATA"].keys()) \
                                  + ("(" + dd["1"]["units"] + ")")

            else:
                data_rec_header = "metabolite number" + "\t" + "metabolite name" \
                                  + "\t" + "metabolite identifier" \
                                  + '\t' + \
                                  ("(" + dd["1"]["units"] + ')\t').join(dd["1"]["DATA"].keys()) \
                                  + ("(" + dd["1"]["units"] + ")")

            fh = open(write_dir + "/" + mw_study_id + "/data/" + mw_study_id + "_" + mw_analysis_id + "-maf-data-jsonparsing.txt", "w")
            # print("writing 'maf file document' to file from 'generate_maf_file' method:...")
            fh.writelines(data_rec_header)
            fh.writelines("\n")

            for key in dd:
                # print(dd[key]["analysis_id"])
                if dd[key]["analysis_id"] == mw_analysis_id:
                    if "other_id" in dd.items():
                        record_values = key + '\t' + dd[key]["metabolite_name"] + "\t" + dd[key]["metabolite_id"] \
                                        + "\t" + dd[key]["pubchem_id"] + "\t" + dd[key]["other_id"] + "\t" + dd[key][
                                            "other_id_type"]

                        for value in dd[key]["DATA"].values():
                            record_values = record_values + "\t" + str(value)
                        fh.writelines(record_values)
                        fh.writelines("\n")
                    elif "pubchem_id" in dd.items():
                        record_values = key + '\t' + dd[key]["metabolite_name"] + "\t" + dd[key]["metabolite_id"] \
                                        + "\t" + dd[key]["pubchem_id"] + "\t" + dd[key]["other_id"] + "\t" + dd[key][
                                            "other_id_type"]

                        for value in dd[key]["DATA"].values():
                            record_values = record_values + "\t" + str(value)
                        fh.writelines(record_values)
                        fh.writelines("\n")
                    else:
                        record_values = key + '\t' + dd[key]["metabolite_name"] + "\t" + dd[key]["metabolite_id"]

                        for value in dd[key]["DATA"].values():
                            record_values = record_values + "\t" + str(value)
                        fh.writelines(record_values)
                        fh.writelines("\n")

            # Output resulting json to file [Action Dissabled]
            # open("output.json", "w").write(
            #     json.dumps(dd, sort_keys=True, indent=4, separators=(',', ': '))
            # )

        else:
            if len(data) == 0:
                print("no json feed for data!")
            if len(metabolites) == 0:
                print("no json feed for metabolites!")

    except IOError:
        print("Error: in generate_maf_file() method, situation not recognized")

# a method to obtain the nature of the technology used in the analysis from a Metabolomics Workbench Header line
# the method takes one parameter as input: a filehandle
# the method returns a string holding the ISA technology type


def get_assay_type(container):
    assay_type = ""
    try:
        for line in container:
            if "AN:ANALYSIS_TYPE" in str(line):
                if "MS" in str(line):
                    assay_type = "mass spectrometry"
                    # print("assaytype from get_assay_type: ", assay_type)
                elif "NMR" in str(line):
                    assay_type = "nmr spectroscopy"
        return assay_type
    except Exception as e:
        logging.exception(e)
        print("Error: in get_assay_type() method, situation not recognized")


def write_assay(write_dir,technotype, accnum, mw_analysis_nb, assayrecords, assay_wf_header):
    try:
        # /Users/Philippe/Documents/git/MW2ISA/
        assayfileoutputpath = write_dir + "/" + accnum + "/"
        if not os.path.exists(assayfileoutputpath):
            os.makedirs(assayfileoutputpath)

        assay_file = open(assayfileoutputpath +"a_" + accnum + "_" + mw_analysis_nb + '.txt', 'w')
        print("writing 'assay information' to file...")
        # DOC: writing header for ISA assay file:
        for this_item in assay_wf_header:
            assay_file.write('"{0}"'.format(this_item))
            assay_file.write('\t')
            # print('"{0}"'.format(this_item))
        assay_file.write("\n")

        # DOC: now writing associated data records:
        if technotype == "mass spectrometry":
            for my_key in assayrecords:
                # print(my_key, str(assayrecords[my_key][0]))
                # DOC: performing insertion of sample identifier in the canonical workflow for ms assay
                assayrecords[my_key][0][0] = my_key
                assayrecords[my_key][0][2] = my_key
                assayrecords[my_key][0][18] = my_key
                assayrecords[my_key][0][19] = my_key + ".mzml"
                assayrecords[my_key][0][23] = my_key

                # writing the record to file
                for this_item in assayrecords[my_key][0]:
                    assay_file.write('"{0}"'.format(this_item))
                    assay_file.write('\t')
                assay_file.write("\n")
            assay_file.write("\n")

        elif technotype == "nmr spectroscopy":
            for my_key in assayrecords:
                # print("mickey: ", my_key)
                # DOC: performing insertion of sample identifier in the canonical workflow for ms assay
                assayrecords[my_key][0][0] = my_key
                assayrecords[my_key][0][2] = my_key
                assayrecords[my_key][0][19] = my_key
                assayrecords[my_key][0][20] = my_key + ".nmrml"
                assayrecords[my_key][0][23] = my_key

                # writing the record to file
                for this_item in assayrecords[my_key][0]:
                    assay_file.write('"{0}"'.format(this_item))
                    assay_file.write('\t')
                assay_file.write("\n")
            assay_file.write("\n")

        assay_file.close()
    except IOError:
        print("Error: in write_assay() method, situation not recognized")
# a method to create Metabolights formated data files which will be referenced in the ISA-Tab document
# the method takes 3 parameters as input: a filehandle, a MW identifier for the study, a MW identifier for the analysis
# the method return nothing but creates a raw signal quantification file and a metabolite assignment file.


def create_raw_data_files(write_dir, input_techtype, f, input_study_id, input_analysis_id):
    # print("file to download: ", f)
    try:
        # dlurl = urlopen(f)
        # saving a remote file to local drive
        # localcopy = open(studyID + "_" + analysisID + ".txt", 'w+')
        # localcopy.write(str(dlurl.read()))

        # the combination of MW study ID and analysis ID ensure unicity of file name.
        dataoutputdirectory = write_dir + "/" + input_study_id + "/data/"
        if not os.path.exists(dataoutputdirectory):
            os.makedirs(dataoutputdirectory)

        raw_data_file_name = input_study_id + '_' + input_analysis_id + '_raw_data.txt'
        maf_file_name = input_study_id + '_' + input_analysis_id + '_maf.txt'

        if input_techtype == "mass spectrometry":
            dlurl = urlopen(f).read()
            rawblock = getblock(dlurl, "MS_ALL_DATA_START", "MS_ALL_DATA_END")

            if len(rawblock) < 1:
                print("WARNING: no MS raw data reported in MWtab file")
            else:
                print("writing 'ms raw data' to file...")
                with open((dataoutputdirectory + raw_data_file_name), 'w+') as rawdata:
                    for item in rawblock:
                        print("item: ,", item)
                        rawdata.writelines("%s\t" % this_element for this_element in item)
                        rawdata.writelines(item)
                        rawdata.writelines("\n")
                        for this_element in item:
                            if "MS_ALL_DATA_START" in this_element:
                                rawdata.writelines("datatype:\t%s" % this_element)
                            elif "Bin range" in this_element:
                                rawdata.writelines("quantitationtype:   %s" % this_element)
                                rawdata.writelines('\n')
                            else:
                                rawdata.writelines('%s\t' % this_element)
                        rawdata.writelines('\n')

        elif input_techtype == "nmr spectroscopy":
            dlurl = urlopen(f).read()
            rawblock = getblock(dlurl, "NMR_BINNED_DATA_START", "NMR_BINNED_DATA_END")
            # rawdata.writelines("%s\n" % item.replace("\t","\\t") for item in rawblock)
            if len(rawblock)<1:
                print("WARNING: no nmr binned  data reported in MWtab file")
            else:
                print("writing 'nmr binned data' to file...")
                with open((dataoutputdirectory + raw_data_file_name), 'w+') as rawdata:
                    for item in rawblock:
                        # print(*item, sep='\t')
                        for this_element in item:
                            if "NMR_BINNED" in this_element:
                                rawdata.writelines("datatype:\t%s" % this_element)
                            elif "Bin range" in this_element:
                                rawdata.writelines("quantitationtype:   %s" % this_element)
                                rawdata.writelines('\n')
                            else:
                                rawdata.writelines('%s\t' % this_element)
                        rawdata.writelines('\n')

        # generate_maf_file(input_study_id)

        if input_techtype == "mass spectrometry":
            dlurl = urlopen(f).read()
            mafblock = getblock(dlurl, "MS_METABOLITE_DATA_START", "MS_METABOLITE_DATA_END")
            mafblock2 = getblock(dlurl, "METABOLITES_START", "METABOLITES_END")
            # print("mafblock2", mafblock2)
            with open((dataoutputdirectory + maf_file_name), 'w+') as mafdata:
                for item in mafblock:
                    mafdata.writelines("%s\t" % this_element for this_element in item)
                    mafdata.writelines("\n")
                for item in mafblock2:
                    mafdata.writelines("%s\t" % this_element for this_element in item)
                    mafdata.writelines("\n")
                # mafdata.writelines("%s\n" % item for item in mafblock)
                # mafdata.writelines("%s\n" % item for item in mafblock2)

        elif input_techtype == "nmr spectroscopy":
            dlurl = urlopen(f).read()
            nmr_mafblock = getblock(dlurl, "NMR_METABOLITE_DATA_START", "NMR_METABOLITE_DATA_END")
            if len(nmr_mafblock) < 1:
                print("WARNING: no nmr metabolite data reported in MWTab")
                # print("nmr_mafblodk:", len(nmr_mafblock))
            else:
                # print("nmr_mafblock", nmr_mafblock)
                # mafdata.writelines("%s\n" % item for item in mafblock)
                with open((dataoutputdirectory + maf_file_name), 'w+') as mafdata:
                    for item in nmr_mafblock:
                        mafdata.writelines("%s" % this_element for this_element in item)
    except Exception as e:
        logging.exception(e)
        print("Error in create_raw_data_files() methods, possibly when trying to write data files")

# a method to create ISA assay tables from an Metabolomics Workbench Study Identifier
# the method takes 3 parameters as input: a filehandle, a MW identifier for the study, a MW identifier for the analysis
# the method return nothing but creates as many as ISA assay files.


# a method to create an ISA assay table for NMR records
# the method takes a filehandle as input

def create_nmr_assay_records(lol, study_id, analysis_id, fv_records):

    try:
        # print(fv_records)
        # print("getting the nmr MWTab file: ", lol)
        pv_nmr_instrument = "not reported"
        pv_nmr_exprt_type = "not reported"
        pv_nmr_sw_version = "not reported"
        pv_nmr_frequency = "not reported"
        # pv_nmr_field_freq_lock = ""
        # pv_nmr_std_concentration = ""
        pv_nmr_probe = "not reported"
        pv_nmr_solvent = "not reported"
        pv_nmr_tube_size = "not reported"
        pv_nmr_shimming_method = "not reported"
        pv_nmr_pulse_sequence = "not reported"
        # pv_nmr_water_suppression = ""
        # pv_nmr_pulse_width = ""
        # pv_nmr_power_level = ""
        # pv_nmr_receiver_gain = ""
        # pv_nmr_offset_frequency = ""
        pv_nmr_chemical_shift_ref_compound = "not reported"
        # pv_nmr_temp = ""
        pv_nmr_numscan = "not reported"
        # pv_nmr_acquisitiontime = ""
        pv_nmr_acquisition_file = "not reported"
        pv_nmr_relaxationdelay = "not reported"
        # pv_nmr_spectralwidth = ""
        # pv_nmr_acquired_data_points = ""
        pv_nmr_zerofilling = "not reported"
        pv_nmr_apodization = "not reported"
        pv_nmr_baseline_correction_method = "not reported"
        pv_nmr_binned_increment = "not reported"
        pv_nmr_excluded_range = "not reported"
        nmr_rawdata_qt = "NA"
        nmr_maf_qt = "NA"
        assayrecords = []
        assay_wf_record = []

        raw_data_file = ""
        assay_wf_header = ["Sample Name",
                           "Protocol REF",
                           "Extract Name",
                           "Protocol REF",
                           "Parameter Value[nmr instrument]",
                           "Parameter Value[nmr type]",
                           "Parameter Value[nmr probe]",
                           "Parameter Value[spectrometer frequency]",
                           "Parameter Value[acquisition file]",
                           "Parameter Value[pulse program]",
                           "Parameter Value[nmr solvent]",
                           "Parameter Value[nmr tube size]",
                           "Parameter Value[shimming method]",
                           "Parameter Value[relaxation delay]",
                           "Parameter Value[number of scans]",
                           "Parameter Value[chemical shift reference compound]",
                           "Parameter Value[zero filling]",
                           "Parameter Value[apodization]",
                           "Parameter Value[baseline correction method]",
                           "Parameter Value[binned increment]",
                           "Parameter Value[binned data exclusion range ]",
                           "NMR Assay Name",
                           "Free Induction Data File",
                           "Protocol REF",
                           "Parameter Value[software]",
                           "Data Transformation Name",
                           "Derived Spectral Data File"]

        input_nmr_file = urlopen(lol).read()
        input_nmr_file = str(input_nmr_file).split('\\n')

        maf_file = str(study_id) + "_" + str(analysis_id) + "_maf_data.txt"

        for this_row in input_nmr_file:
            this_row = this_row.rstrip()
            this_row = str(this_row).split('\\t')
            # print(this_row)

            if "NM:NMR_EXPERIMENT_TYPE" in this_row[0]:
                pv_nmr_exprt_type = this_row[1]

            if "NM:INSTRUMENT_TYPE" in this_row[0]:
                pv_nmr_instrument = this_row[1]

            if "NM:NMR_PROBE" in this_row[0]:
                pv_nmr_probe = this_row[1]

            if "NM:SPECTROMETER_FREQUENCY" in this_row[0]:
                pv_nmr_frequency = this_row[1]

            if "AN:ACQUISITION_PARAMETERS_FILE" in this_row[0]:
                pv_nmr_acquisition_file = this_row[1]

            if "NM:CHEMICAL_SHIFT_REF_CPD" in this_row[0]:
                pv_nmr_chemical_shift_ref_compound = this_row[1]

            if "NM:PULSE_SEQUENCE" in this_row[0]:
                pv_nmr_pulse_sequence = this_row[1]

            if "NM:NUMBER_OF_SCANS" in this_row[0]:
                pv_nmr_numscan = this_row[1]
            #
            # if "AN:ACQUISITION_PARAMETERS_FILE" in row[0]:
            #     pv_nmr_acquisition_file = row[1]
            #     # protocol_files[3] = row[1]

            if "AN:SOFTWARE_VERSION" in this_row[0]:
                pv_nmr_sw_version = this_row[1]

            if "NMR_METABOLITE_DATA:UNITS" in this_row[0] and len(this_row) > 1:
                nmr_maf_qt = this_row[1]

            if "NMR_ALL_DATA:UNITS" in this_row[0] and len(this_row) > 1:
                nmr_rawdata_qt = this_row[1]

            # if "#ANALYSIS TYPE: NMR" in row[0]:
            #     tt = "nmr spectroscopy"
            # if "NM:NMR_EXPERIMENT_TYPE" in row[0]:
            #     pv_nmr_exprt_type = row[1]
            #
            # if "NM:FIELD_FREQUENCY_LOCK" in row[0]:
            #     pv_nmr_field_freq_lock = row[1]
            # if "NM:STANDARD_CONCENTRATION" in row[0]:
            #     pv_nmr_std_concentration = row[1]
            if "NM:NMR_SOLVENT" in this_row[0]:
                pv_nmr_solvent = this_row[1]
            # if "NM:NMR_TUBE_SIZE" in row[0]:
            #     pv_nmr_tube_size = row[1]
            # if "NM:SHIMMING_METHOD" in row[0]:
            #     pv_nmr_shimming_method = row[1]
            # if "NM:PULSE_SEQUENCE" in row[0]:
            #     pv_nmr_pulse_sequence = row[1]
            # if "NM:WATER_SUPPRESSION" in row[0]:
            #     pv_nmr_water_suppression = row[1]
            # if "NM:PULSE_WIDTH" in row[0]:
            #     pv_nmr_pulse_width = row[1]
            # if "NM:POWER_LEVEL" in row[0]:
            #     pv_nmr_power_level = row[1]
            # if "NM:RECEIVER_GAIN" in row[0]:
            #     pv_nmr_receiver_gain = row[1]
            # if "NM:OFFSET_FREQUENCY" in row[0]:
            #     pv_nmr_offset_frequency = row[1]
            # if "NM:CHEMICAL_SHIFT_REF_CPD " in row[0]:
            #     pv_nmr_chemical_shift_ref_compound = row[1]
            # if "NM:TEMPERATURE" in row[0]:
            #     pv_nmr_temp = row[1]

            # if "NM:DUMMY_SCANS" in this_row[0]:
            #     pv_nmr_dummyscans = this_row[1]
            # if "NM:ACQUISITION_TIME" in this_row[0]:
            #     pv_nmr_acquisitiontime = this_row[1]
            if "NM:RELAXATION_DELAY" in this_row[0]:
                pv_nmr_relaxationdelay = this_row[1]
            # if "NM:SPECTRAL_WIDTH" in this_row[0]:
            #     pv__nmr_spectralwidth = this_row[1]
            # if "NM:NUM_DATA_POINTS_ACQUIRED" in this_row[0]:
            #     pv_nmr_acquired_data_points = this_row[1]
            # if "NM:REAL_DATA_POINTS" in this_row[0]:
            #     pv_nmr_real_data_points = this_row[1]
            if "NM:BINNED_INCREMENT" in this_row[0]:
                pv_nmr_binned_increment = this_row[1]
            if "NM:BINNED_DATA_EXCLUDED_RANGE" in this_row[0]:
                pv_nmr_excluded_range = this_row[1]
            if "NM:ZERO_FILLING" in this_row[0]:
                pv_nmr_zerofilling = this_row[1]
            if "NM:APODIZATION" in this_row[0]:
                pv_nmr_apodization = this_row[1]
            if "NM:BASELINE_CORRECTION_METHOD" in this_row[0]:
                pv_nmr_baseline_correction_method = this_row[1]

            # if "NMR:NMR_EXPERIMENT_TYPE" in row[0]:
            #     pv_nmrexprt_type = row[1]

            # if "MS_METABOLITE_DATA_START" in row[0]:

        # print("assay workflow header:", assay_wf_header)

        assay_wf_backbone_record = ["",
                                    "metabolite extraction protocol",
                                    "",
                                    "nuclear magnetic resonance spectroscopy protocol",
                                    pv_nmr_instrument,
                                    pv_nmr_exprt_type,
                                    pv_nmr_probe,
                                    pv_nmr_frequency,
                                    pv_nmr_acquisition_file,
                                    pv_nmr_pulse_sequence,
                                    pv_nmr_solvent,
                                    pv_nmr_tube_size,
                                    pv_nmr_shimming_method,
                                    pv_nmr_relaxationdelay,
                                    pv_nmr_numscan,
                                    pv_nmr_chemical_shift_ref_compound,
                                    pv_nmr_zerofilling,
                                    pv_nmr_apodization,
                                    pv_nmr_baseline_correction_method,
                                    pv_nmr_binned_increment,
                                    pv_nmr_excluded_range,
                                    "",
                                    raw_data_file,
                                    "identification protocol",
                                    pv_nmr_sw_version,
                                    "",
                                    maf_file]

        # print("assay workflow backbone: ", assay_wf_backbone_record)
        # assayrecords.append(assay_wf_record)

        # creating assay records
        longrecords = {}
        full_assay_record = assay_wf_backbone_record
        for fv_record in fv_records:
            # print("factors:", fv_record)
            longrecords[fv_record[3]] = [full_assay_record]
            # print("records:", [full_assay_record])
            # print("full assay record: ",fv_record[3], ": ", longrecords[fv_record[3]])

        # print("QTs:", nmr_maf_qt, nmr_rawdata_qt)

        return longrecords, assay_wf_header, nmr_maf_qt, nmr_rawdata_qt

    except:
        print("Error in create_nmr_assay_records() method, possibly when trying to write nmr assay data files")


# a method to create an ISA assay table for MS records
# the method takes a filehandle as input

def create_ms_assay_records(lol, input_study_id, input_analysis_id, fv_records):

    try:
        # print("checking the factors from create_ms_assay_records: ", fv_records)

        pv_ch_instrument = ""
        pv_ch_column = ""
        pv_ch_flowrate = ""
        pv_ch_inj_temp = ""
        pv_ch_solvent_a = ""
        pv_ch_solvent_b = ""
        pv_ch_type = ""
        pv_ch_file = ""
        pv_ms_type = ""
        pv_ms_ion_mode = ""
        pv_ms_instrument = ""
        pv_ms_acquisitionfile = ""
        pv_ms_analysisfile = ""
        pv_ms_sw_version = ""
        raw_data_file = ""
        ms_rawdata_qt = "NA"
        maf_file = ""
        ms_maf_qt = "NA"

        assayrecords = []
        assay_wf_record = []
        assay_wf_header = ["Sample Name",
                           "Protocol REF",
                           "Extract Name",
                           "Protocol REF",
                           "Parameter Value[chromatography type]",
                           "Parameter Value[chromatography instrument]",
                           "Parameter Value[chromatography column]",
                           "Parameter Value[chromatography setting file]",
                           "Parameter Value[flow rate]",
                           "Parameter Value[injection temperature]",
                           "Parameter Value[solvent a]",
                           "Parameter Value[solvent b]",
                           "Protocol REF",
                           "Parameter Value[mass spectrometry instrument]",
                           "Parameter Value[mass spectrometry type]",
                           "Parameter Value[injection mode]",
                           "Parameter Value[ionization mode]",
                           "Parameter Value[acquisition file]",
                           "MS Assay Name",
                           "Raw Spectral Data File",
                           "Protocol REF",
                           "Parameter Value[analysis file]",
                           "Parameter Value[software]",
                           "Data Transformation Name",
                           "Derived Spectral Data File",
                           "Protocol REF",
                           "Data Transformation Name",
                           "Metabolite Annotation File"
                           ]

        input_ms_file = urlopen(lol).read()
        input_ms_file = str(input_ms_file).split('\\n')

        # print("content of ms file MS?: ", input_ms_file)

        for row_item in input_ms_file:

            row_item = row_item.rstrip()
            row_item = str(row_item).split('\\t')

            # if "AN:ANALYSIS_TYPE" in row_item[0]:
            #     ms_protocol_type = row_item[1].rstrip()
            #
            # if "AN:INSTRUMENT_NAME" in row_item[0]:
            #     pv_instrument = row_item[1]

            if "CH:INSTRUMENT_NAME" in row_item[0]:
                pv_ch_instrument = pv_ch_instrument + " " + row_item[1]

            if "CH:COLUMN_NAME" in row_item[0]:
                pv_ch_column = pv_ch_column + " " + row_item[1]

            if "CH:METHODS_FILENAME" in row_item[0]:
                pv_ch_file = row_item[1]

            if "CH:CHROMATOGRAPHY_TYPE" in row_item[0]:
                pv_ch_type = row_item[1]

            if "CH:INJECTION_TEMP" in row_item[0]:
                pv_ch_inj_temp = row_item[1]

            if "CH:FLOW_RATE" in row_item[0]:
                pv_ch_flowrate = row_item[1]

            if "CH:SOLVENT_A" in row_item[0]:
                pv_ch_solvent_a = pv_ch_solvent_a + " " + row_item[1]

            if "CH:SOLVENT_B" in row_item[0]:
                pv_ch_solvent_b = pv_ch_solvent_a + " " + row_item[1]

            if "MS:INSTRUMENT_NAME" in row_item[0]:
                pv_ms_instrument = row_item[1]

            if "MS:INSTRUMENT_TYPE" in row_item[0]:
                pv_ms_instrument_type = row_item[1]

            if "MS:MS_TYPE" in row_item[0]:
                pv_ms_type = row_item[1]

            if "MS:ION_MODE" in row_item[0]:
                pv_ms_ion_mode = row_item[1]

            if "AN:ACQUISITION_PARAMETERS_FILE" in row_item[0]:
                pv_ms_acquisitionfile = row_item[1]
                # protocol_files[3] = row_item[1]

            if "AN:SOFTWARE_VERSION" in row_item[0]:
                pv_ms_sw_version = row_item[1]

            if "MS_ALL_DATA:UNITS" in row_item[0] and len(row_item) > 1:
                ms_rawdata_qt = row_item[1]

            if "MS_ALL_DATA_START" in row_item[0]:
                raw_data_file = str(input_study_id) + "_" + str(input_analysis_id) + "_raw_data.txt"

            if "MS_METABOLITE_DATA:UNITS" in row_item[0] and len(row_item) > 1:
                ms_maf_qt = row_item[1]

        maf_file = str(input_study_id) + "_" + str(input_analysis_id) + "_maf_data.txt"
        # print("there", str(input_analysis_id))
        assay_wf_backbone_record = ["",
                                    "metabolite extraction protocol",
                                    "",
                                    "chromatography protocol",
                                    pv_ch_type,
                                    pv_ch_instrument,
                                    pv_ch_column,
                                    pv_ch_file,
                                    pv_ch_flowrate,
                                    pv_ch_inj_temp,
                                    pv_ch_solvent_a,
                                    pv_ch_solvent_b,
                                    "mass spectrometry protocol",
                                    pv_ms_instrument,
                                    pv_ms_instrument_type,
                                    pv_ms_type,
                                    pv_ms_ion_mode,
                                    pv_ms_acquisitionfile,
                                    "",
                                    raw_data_file,
                                    "identification protocol",
                                    pv_ms_analysisfile,
                                    pv_ms_sw_version,
                                    "",
                                    raw_data_file,
                                    "annotation protocol",
                                    "Metabolite Annotation",
                                    maf_file,
                                    ]

        # print("assay workflow: ", str(assay_wf_backbone_record))
        assayrecords.append(assay_wf_record)

        # creating assay records
        longrecords = {}
        full_assay_record = assay_wf_backbone_record

        for fv_record in fv_records:
            # print("factors:", fv_record)
            longrecords[fv_record[3]] = [full_assay_record]
            # print("full assay record: ",fv_record[3], ": ", longrecords[fv_record[3]])

        return longrecords, assay_wf_header, ms_rawdata_qt, ms_maf_qt
    except:
        print("Error: in create_ms_assay_records() method.")


def get_organism_with_taxid(lol):
    that_species = ""
    that_taxid = ""
    try:
        for this_row in lol:
            if "SU:SUBJECT_SPECIES" in this_row[0]:
                that_species = this_row[1]
            if "SU:TAXONOMY_ID" in this_row[0]:
                that_taxid = this_row[1]
        # print("species & TaxID :", that_species, that_taxid)
        return that_species, that_taxid
    except Exception as e:
        logging.exception(e)
        print("Error in get_organism_with_taxid() method")


def get_fv_records(lol):
    records = []
    factors = {}
    restofrecordheader = []

    for current_row in lol:
        if "SUBJECT_SAMPLE_FACTORS" in str(current_row) and "#" not in str(current_row):
            # print('row from get_fv_records', row)
            if len(current_row) > 2:
                newrecord = []
                if current_row[1] != "-":
                    newrecord.append(current_row[1])
                else:
                    newrecord.append(current_row[2])

                newrecord.append(current_row[2])

                if "|" in current_row[3]:
                    for item in current_row[3].split("|"):
                        factor, value = item.split(":")
                        factor = factor.strip()
                        newrecord.append(value.strip())

                        if factor in factors.keys():
                            factors[factor] += 1
                        else:
                            factors[factor] = 1
                else:
                    elements = current_row[3].split(":")
                    factor = elements[0]
                    if len(elements) > 2:
                        value = elements[1] + elements[2]
                    else:
                        value = elements[1]

                    if factor in factors.keys():
                        factors[factor] += 1
                    else:
                        factors[factor] = 1

                    newrecord.append(value)

                records.append(newrecord)

    for my_key in factors.keys():
                restofrecordheader.append("Factor Value[" + my_key + "]")

    return records, factors, restofrecordheader


def get_mwfile_as_lol(input_url):
    try:
        input_file = urlopen(input_url).read()
        input_file = str(input_file).split('\\n')
        mw_as_lol = []
        for line in input_file:
            lines = line.split('\\t')
            mw_as_lol.append(lines)

        return mw_as_lol
    except IOError:
        print("IOError in get_mwfile_as_lol() method: can not open file or read data ")

# a method to write an ISA study file
# a


def write_study_file(write_dir, study_acc_num, study_file_header, longrecords):

    try:
        this_study_filename = "s_" + study_acc_num + ".txt"
        # print("study filename: ",this_study_filename) /Users/Philippe/Documents/git/MW2ISA
        studyfilepath = write_dir + "/" + study_acc_num
        if not os.path.exists(studyfilepath):
            os.makedirs(studyfilepath)
        study_file = open((studyfilepath + "/" + this_study_filename), 'w')
        try:
            print("writing 'study sample information' to file...")
            # write study header to file
            # studyfileheader = studyfileheader+factorheader
            for this_element in study_file_header:
                study_file.write('"{0}"'.format(this_element))
                # print('"{0}"'.format(this_element))
                study_file.write('\t')
            study_file.write("\n")

            # writing study records to file
            for each in longrecords:
                # this is to reorder fields following the merge
                each[0], each[1], each[2], each[3] = each[3], each[0], each[1], each[2]
                each.insert(4, "sample collection protocol")
                each.insert(3, "")
                each[4], each[5] = each[5], each[4]
                each.insert(1, "specimen")

                for item in each:
                    study_file.write("\"" + item + "\"")
                    study_file.write('\t')
                study_file.write('\n')

            study_file.close()

        except IOError:
            print("IOError in write_study_file method(): can not write to file.")

        # else:
        #   print("Error in write_study_file method() -something went wrong while trying to write but don't know why!")

    except IOError:
        print("IOError in write_study_file() method: can not open file or read data ")
    # else:
    #     print("doh, something went wrong but don't know why in write_study_file method()!")


# METHOD: given a Metabolomics Workbench Identifier, download the corresponding zip archive via anonymous FTP


def get_raw_data(study_accession_number):
    study_accession_number = str(study_accession_number)
    try:
        ftp_download_url = "ftp://www.metabolomicsworkbench.org/Studies/" + study_accession_number + ".zip"
        urlopen(url=ftp_download_url)
    except IOError:
        print("IOError in get_raw_data() method: no permission to download or wrong url")

# METHOD:
#
# a function to iterate over a dictionary of study identifiers matched to a technology type: aim is to allow batch
#  processing/download from MW
# dictionary_of_input = {"ST000102": "NMR", "ST000056": "NMR", "ST000282": "MS", "ST000367": "MS", "ST000093": "MS",
#                       "ST000159": "MS", "ST000110": "MS", "ST000369": "MS"}
# //////////
# for key in dictionary_of_input.key():
#     page_url = baseurl + dictionary_of_input[key] + "Data&StudyID=" + key + "&StudyType=" +
# dictionary_of_input[key] + "&ResultType=1#DataTabs"
#
#     try:
#         process_entry(key, dictionary_of_input[key])
#     except IOError:
#         print()
#     except:
#         print("it does not cut no mustard, isn't it?")
# //////////

# MAIN METHOD:
# "ST000367"
# "ST000093"
# "ST000159"
# "ST000110"
# "ST00036"


def mw2isa_convert(**kwargs):
    options = {
        'studyid': '',
        'outputdir':'',
        'dl_option': '',
        'validate_option': ''}

    conversion_success = True
    try:

        options.update(kwargs)
        print("user options", options)
        studyid = options['studyid']
        outputdir = options['outputdir']
        dl_option = options['dl_option']
        validate_option = options['validate_option']
        # Retrieve DCC MW Webpage for an study entry and obtaining the list of associated 'analysis' (i.a. ISA assays)

        # studyid = input('Enter a study ID name: ')
        # dl_option = input('Download raw data file: yes/no')

        # checking MW study accession number is conform:
        if not re.match(r"(^ST\d{6})", studyid):

            print("this is not a MW accession number, please try again")

        else:
            study_url = "http://www.metabolomicsworkbench.org/rest/study/study_id/" + studyid + "/analysis"

            with urllib.request.urlopen(study_url) as url:
                study_response = url.read().decode('utf8')
                analyses = json.loads(study_response)
                # print("study analysis", analyses)
                if "1" in analyses.keys():
                    print("several analysis")
                    for key in analyses.keys():
                        tt = analyses[key]["analysis_type"]
                        print("analysis_type:", tt)
                else:
                    print("Technology is: ", analyses["analysis_type"])
                    tt = analyses["analysis_type"]

            print("proceeding with MW study identifier: ", studyid, "and technology:", tt)
            # studyid = "ST000367"
            # tt = "MS"
            outputpath = outputdir + "/" + studyid + "/"
            if not os.path.exists(outputpath):
                os.makedirs(outputpath)

            baseurl = "http://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&DataMode="
            page_url = baseurl + tt + "Data&StudyID=" + studyid + "&StudyType=" + tt + "&ResultType=1#DataTabs"
            page = urlopen(page_url).read()
            soup = BeautifulSoup(page, "html.parser")
            AnalysisParamTable = soup.findAll("table", {'class': "datatable2"})

            analysisid = ""
            assay_types = []
            isa_assay_names = []
            isa_assay_names_with_dlurl = {}

            downLoadURI = "http://www.metabolomicsworkbench.org/data/study_textformat_view.php?STUDY_ID=" + studyid \
                          + "&ANALYSIS_ID="

            study_assays_dict = {"study_id": studyid, "assays": []}
            for table in AnalysisParamTable:
                l = len(table)
                index = 0
                for index, obj in enumerate(table):
                    if "Analysis ID:" in str(obj):
                        tds = obj.find_all('td')
                        analysisid = tds[1].text
                        # print(index,"analysis ID", table.tr.next(), analysisid)
                        if "MS" in str(table.tr.next()):
                            tt = "mass spectrometry"
                            study_assays_dict["assays"].append({"analysis_id": analysisid, "techtype": tt})
                        elif "NMR" in str(table.tr.next()):
                            tt = "nmr spectroscopy"
                            study_assays_dict["assays"].append({"analysis_id": analysisid, "techtype": tt})

            # DOC: This print statement shows we are getting all the possible analysis for a given study
            # print("all analysis", study_assays_dict["assays"])

            # Initialization of a range of variables mapping to ISA investigation and study files
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
            mass_spec_protocol = ""
            nmrspc_protocol = ""

            chromatography_protocol_params = []
            ms_protocol_params = []
            nmr_protocol_params = []
            ms_analysis_params = []
            nmr_analysis_params = []
            ident_protocol_params = []

            mt = "metabolite profiling"

            protocol_names = ["", "", "", "", "", "", "", "", ""]
            protocol_types = ["sample collection", "treatment", "metabolite extraction", "sample preparation",
                              "chromatography",
                              "mass spectrometry", "nmr spectroscopy", "identification", "annotation"]
            protocol_descriptions = ["", "", "", "", "", "", "", "", ""]
            protocol_parameters = {"sample collection": [""], "treatment": [""], "metabolite extraction": [""],
                                   "sample preparation": [""], "chromatography": [""], "mass spectrometry": [""],
                                   "nmr spectroscopy": [""], "identification": [""], "annotation": [""]}
            protocol_files = ["", "", "", "", "", "", "", "", ""]

            study_person_firstname = ""
            study_person_lastname = ""
            study_person_email = ""
            study_person_affiliation = ""
            study_person_address = ""
            study_person_phone = ""
            study_person_fax = ""
            study_createdon = ""
            study_submittedon = ""
            study_convertedon = ""
            study_num_group = ""
            study_total_subj = ""
            study_version = ""

            material_type = ""
            sample_type = ""
            organism = ""

            study_factor_records = []
            study_factors = {}
            fv_record_header = []

            basestudysamplerecordheader = ["Source Name", "Material Type", "Characteristics[Organism]",
                                           "Term Accession Number",
                                           "Term Source REF", "Protocol REF", "Sample Name"]
            # //// END OF VARIABLE DECLARATION

            # Getting a MWTab file using the first analysis (There are as many MWTab file as there are analysis
            # and they all share common section and information about samples and protocols so we get the first file
            # to prime.
            analysisid = study_assays_dict["assays"][0]["analysis_id"]
            downLoadURI = downLoadURI + analysisid + "&MODE=d"
            # Going over the firt MWtab and loading it as an array of lines
            thisFileContent = get_mwfile_as_lol(downLoadURI)

            # Generating the ISA Study Sample Table stub from MW Tab file Factor section:
            study_factor_records, study_factors, fv_record_header = get_fv_records(thisFileContent)
            # Getting Sample Organism information:
            species, taxonid = get_organism_with_taxid(thisFileContent)
            # Inserting the taxonomic information in the ISA Study Sample Table stub.
            for each_record in study_factor_records:
                each_record.insert(0, species)
                each_record.insert(1, taxonid)

            # Building the Investigation Object and its elements:
            investigation = Investigation(identifier=studyid)
            investigation.comments.append(Comment(name="Primary Database", value="NIH Metabolomics Workbench"))
            investigation.comments.append(Comment(name="conversion date", value=str(date.today())))
            investigation.comments.append(Comment(name="conversion software", value="MW2ISA version 1.0"))
            investigation.comments.append(Comment(name="conversion performer email",
                                                  value="philippe.rocca-serra@oerc.ox.ac.uk"))

            investigation.studies.append(Study(identifier=studyid))
            study1 = investigation.studies[0]
            study1.comments = list()

            # Scannning the MWTab file for common information and setting values to variables
            for row in thisFileContent:

                if str(row[0]).startswith('VERSIO'):
                    study_version = row[1]
                    study1.comments.append(Comment(name="Version", value=row[1]))

                if row[0].find('CREATED_ON') != -1:
                    study_createdon = row[1]
                    study1.comments.append(Comment(name="MW creation date", value=row[1]))

                if row[0].find('ST:SUBMIT_DATE') != -1:
                    study_submittedon = row[1]
                    study1.comments.append(Comment(name="MW submission date", value=row[1]))

                if row[0].find('ST:NUM_GROUPS') != -1:
                    study_num_group = row[1]
                    study1.comments.append(Comment(name="number of study groups", value=row[1]))

                if row[0].find('ST:TOTAL_SUBJECTS') != -1:
                    study_total_subj = row[1]
                    study1.comments.append(Comment(name="total number of subjects", value=row[1]))

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
                    study_person_address = study_person_address + ", " + row[1]

                if row[0].find('PR:FUNDING_SOURCE') != -1:
                    study_funder = study_funder + " " + row[1]

                if row[0].find('CO:COLLECTION_SUMMARY') != -1:
                    collect_protocol = collect_protocol + " " + row[1]

                if row[0].find('TR:TREATMENT_SUMMARY') != -1:
                    treat_protocol = treat_protocol + " " + row[1]

                # GETTING CHROMATOGRAPHY PARAMETERS

                if row[0].find('CH:CHROMATOGRAPHY_SUMMARY') != -1:
                    chromatography_protocol = chromatography_protocol + " " + row[1]

                if row[0].find('CH:INSTRUMENT_NAME') != -1:
                    # chromatography_protocol = chromatography_protocol + " " + row[1]
                    chromatography_param_oa = OntologyAnnotation(term="chromatography instrument")
                    chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
                    chromatography_protocol_params.append(chromatography_param)

                if row[0].find('CH:CHROMATOGRAPHY_TYPE') != -1:
                    # protocol_parameters["chromatography"].append("chromatography type: "  + row[1])
                    chromatography_param_oa = OntologyAnnotation(term="chromatography type")
                    chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
                    chromatography_protocol_params.append(chromatography_param)

                if row[0].find('CH:COLUMN_NAME') != -1:
                    # protocol_parameters["chromatography"].append("chromatography column name: "  + row[1])
                    chromatography_param_oa = OntologyAnnotation(term="chromatography column")
                    chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
                    chromatography_protocol_params.append(chromatography_param)

                if row[0].find('CH:COLUMN_TEMPERATURE') != -1:
                    # protocol_parameters["chromatography"].append("chromatography temperature: "  + row[1])
                    chromatography_param_oa = OntologyAnnotation(term="chromatography column temperature")
                    chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
                    chromatography_protocol_params.append(chromatography_param)

                if row[0].find('CH:TRANSFERLINE_TEMPERATURE') != -1:
                    # protocol_parameters["chromatography"].append("transferline temperature: "  + row[1])
                    chromatography_param_oa = OntologyAnnotation(term="transferline temperature")
                    chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
                    chromatography_protocol_params.append(chromatography_param)

                if row[0].find('CH:WASHING_BUFFER') != -1:
                    # protocol_parameters["chromatography"].append("washing buffer: "  + row[1])
                    chromatography_param_oa = OntologyAnnotation(term="washing buffer")
                    chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
                    chromatography_protocol_params.append(chromatography_param)

                if row[0].find('CH:SAMPLE_LOOP_SIZE') != -1:
                    # protocol_parameters["chromatography"].append("sample loop size: "  + row[1])
                    chromatography_param_oa = OntologyAnnotation(term="sample loop size buffer")
                    chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
                    chromatography_protocol_params.append(chromatography_param)

                if row[0].find('CH:OVEN_TEMPERATURE') != -1:
                    # protocol_parameters["chromatography"].append("oven temperature: "  + row[1])
                    chromatography_param_oa = OntologyAnnotation(term="oven temperature")
                    chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
                    chromatography_protocol_params.append(chromatography_param)

                if row[0].find('CH:FLOW_RATE') != -1:
                    # protocol_parameters["chromatography"].append("flow rate: "  + row[1])
                    chromatography_param_oa = OntologyAnnotation(term="flow rate")
                    chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
                    chromatography_protocol_params.append(chromatography_param)

                if row[0].find('CH:SOLVENT_A') != -1:
                    # protocol_parameters["chromatography"].append("flow rate: "  + row[1])
                    chromatography_param_oa = OntologyAnnotation(term="solvent a")
                    chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
                    chromatography_protocol_params.append(chromatography_param)

                if row[0].find('CH:SOLVENT_B') != -1:
                    # protocol_parameters["chromatography"].append("flow rate: "  + row[1])
                    chromatography_param_oa = OntologyAnnotation(term="solvent b")
                    chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
                    chromatography_protocol_params.append(chromatography_param)

                if row[0].find('CH:INJECTION_TEMPERATURE') != -1:
                    # protocol_parameters["chromatography"].append("oven temperature: "  + row[1])
                    chromatography_param_oa = OntologyAnnotation(term="injection temperature")
                    chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
                    chromatography_protocol_params.append(chromatography_param)

                # GETTING MS PARAMETERS
                if row[0].find("MS:MS_COMMENTS") != -1:
                    mass_spec_protocol = mass_spec_protocol + " " + row[1]

                if row[0].find('MS:INSTRUMENT_NAME') != -1:
                    # protocol_parameters["mass spectrometry"].append("mass spectrometry instrument: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="mass spectrometry instrument")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:INSTRUMENT_TYPE') != -1:
                    # protocol_parameters["mass spectrometry"].append("mass spectrometry type: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="mass spectrometry instrument type")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:MS_TYPE') != -1:
                    # protocol_parameters["mass spectrometry"].append("inlet type: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="mass spectrometry type")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:ION_SOURCE_TEMPERATURE') != -1:
                    # protocol_parameters["mass spectrometry"].append("ion source temperature: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="ion source temperature")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:ION_MODE') != -1:
                    # protocol_parameters["mass spectrometry"].append("ion energy: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="ion mode")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:ION_ENERGY') != -1:
                    # protocol_parameters["mass spectrometry"].append("ion energy: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="ion energy")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:ION_SPRAY_VOLTAGE') != -1:
                    # protocol_parameters["mass spectrometry"].append("ion spray voltage: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="ion spray voltage")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:MASS_ACCURACY') != -1:
                    # protocol_parameters["mass spectrometry"].append("mass accuracy: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="mass accuracy")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:SOURCE_TEMPERATURE') != -1:
                    # protocol_parameters["mass spectrometry"].append("source temperature: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="source temperature")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:SCAN_RANGE_MOVERZ') != -1:
                    # protocol_parameters["mass spectrometry"].append("scan range (m/z): "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="scan range (m/z)")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:SCANNING_CYCLE') != -1:
                    # protocol_parameters["mass spectrometry"].append("scanning cycle: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="scan range (m/z)")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:SCANNING') != -1:
                    # protocol_parameters["mass spectrometry"].append("scanning: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="scanning")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:SCANNING_RANGE') != -1:
                    # protocol_parameters["mass spectrometry"].append("scanning range: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="canning range")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:CAPILLARY_TEMPERATURE') != -1:
                    # protocol_parameters["mass spectrometry"].append("capillary temperature: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="capillary temperature")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:SKIMMER_VOLTAGE') != -1:
                    # protocol_parameters["mass spectrometry"].append("skimmer voltage: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="skimmer voltage")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:TUBE_LENS_VOLTAGE') != -1:
                    # protocol_parameters["mass spectrometry"].append("tube lens voltage: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="tube lens voltage")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:CAPILLARY_VOLTAGE') != -1:
                    protocol_parameters["mass spectrometry"].append("capillary voltage: " + row[1])
                    ms_param_oa = OntologyAnnotation(term="capillary voltage")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:COLLISION_ENERGY') != -1:
                    protocol_parameters["mass spectrometry"].append("collision energy: " + row[1])
                    ms_param_oa = OntologyAnnotation(term="collision energy")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param_oa)

                if row[0].find('MS:COLLISION_GAS') != -1:
                    # protocol_parameters["mass spectrometry"].append("collision gas: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="collision gas")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:DRY_GAS_FLOW') != -1:
                    # protocol_parameters["mass spectrometry"].append("dry gas flow: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="dry flow gas")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:DRY_GAS_TEMPERATURE') != -1:
                    # protocol_parameters["mass spectrometry"].append("dry gas: " + row[1])
                    ms_param_oa = OntologyAnnotation(term="dry gas")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:FRAGMENT_VOLTAGE') != -1:
                    # protocol_parameters["mass spectrometry"].append("fragment voltage: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="fragment voltage")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:FRAGMENTATION_METHOD') != -1:
                    # protocol_parameters["mass spectrometry"].append("fragmentation method: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="fragmentation method")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:GAS_PRESSURE') != -1:
                    # protocol_parameters["mass spectrometry"].append("gas pressure: " + row[1])
                    ms_param_oa = OntologyAnnotation(term="gas pressure")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:HELIUM_FLOW') != -1:
                    # protocol_parameters["mass spectrometry"].append("helium flow: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="helium flow")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:DESOLVATION_GAS_FLOW') != -1:
                    # protocol_parameters["mass spectrometry"].append("desolvation gas flow: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="desolvation gas flow")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:DESOLVATION_TEMPERATURE') != -1:
                    # protocol_parameters["mass spectrometry"].append("desolvation temperature: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="desolvation temperature")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:ACTIVATION_PARAMETER') != -1:
                    # protocol_parameters["mass spectrometry"].append("activation parameter: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="activation parameter")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:ACTIVATION_TIME') != -1:
                    # protocol_parameters["mass spectrometry"].append("activation time: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="activation time")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:ATOM_GUN_CURRENT') != -1:
                    # protocol_parameters["mass spectrometry"].append("atom gun current: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="atom gum current")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:AUTOMATIC_GAIN_CONTROL') != -1:
                    # protocol_parameters["mass spectrometry"].append("automatic gain control: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="automatic gain control")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:BOMBARDMENT') != -1:
                    # protocol_parameters["mass spectrometry"].append("bombardment: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="bombardment")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:LASER') != -1:
                    # protocol_parameters["mass spectrometry"].append("laser: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="laser")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:MATRIX') != -1:
                    # protocol_parameters["mass spectrometry"].append("matrix: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="amtrix")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:NEBULIZER') != -1:
                    # protocol_parameters["mass spectrometry"].append("nebulizer: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="nebulizer")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:OCTPOLE_VOLTAGE') != -1:
                    # protocol_parameters["mass spectrometry"].append("octpole voltage: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="octpole voltage")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:IT_SIDE_OCTPOLES_BIAS_VOLTAGE') != -1:
                    # protocol_parameters["mass spectrometry"].append("IT side octpole bias voltage: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="IT side octpole bias voltage")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:CDL_SIDE_OCTPOLES_BIAS_VOLTAGE') != -1:
                    # protocol_parameters["mass spectrometry"].append("CDL side octpole bias voltage: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="CDL side octpole bias voltage")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:CDL_TEMPERATURE') != -1:
                    # protocol_parameters["mass spectrometry"].append("CDL temperature: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="CDL temperature")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:PROBE_TIP') != -1:
                    # protocol_parameters["mass spectrometry"].append("probe tip: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="probe tip")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:RESOLUTION_SETTING') != -1:
                    # protocol_parameters["mass spectrometry"].append("resolution setting: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="resolution setting")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                if row[0].find('MS:SAMPLE_DRIPPING') != -1:
                    # protocol_parameters["mass spectrometry"].append("sample dripping: "  + row[1])
                    ms_param_oa = OntologyAnnotation(term="sample dripping")
                    ms_param = ProtocolParameter(parameter_name=ms_param_oa)
                    ms_protocol_params.append(ms_param)

                # GETTING NMR PARAMETERS
                if row[0].find('NMR:NMR_SUMMARY') != -1:
                    nmrspc_protocol = nmrspc_protocol + " " + row[1]

                if row[0].find('NMR:INSTRUMENT_NAME') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("nmr instrument: "  + row[1])
                    nmr_param_oa = OntologyAnnotation(term="nmr instrument")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:EXPERIMENT_TYPE') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("nmr experiment type: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="nmr experiment type")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:RANDOMIZATION_ORDER') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("randomization order: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="randomization order")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:FIELD_FREQUENCY_LOCK') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("field frequency lock: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="field frequency lock")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:STANDARD_CONCENTRATION') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("standard concentration: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="standard concentration")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:SPECTROMETER FREQUENCY') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("spectrometer frequency: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="spectrometer frequency")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:NMR_PROBE') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("nmr probe: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="nmr probe")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:NMR_SOLVENT') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("nmr solvent: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="nmr solvent")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:NMR_TUBE_SIZE') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("nmr tube size: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="nmr tube size")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:SHIMMING_METHOD') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("shimming method: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="shimming method")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:NMR_PULSE_SEQUENCE') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("nmr pulse sequence: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="nmr pulse sequence")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:WATER_SUPPRESSION') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("water suppression: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="water suppression")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:PULSE_WIDTH') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("nmr pulse width: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="nmr pulse width")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:POWER_LEVEL') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("nmr power level: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="nmr power level")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:RECEIVER_GAIN') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("nmr receiver gain: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="nmr receiver gain")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:PRESATURATION_POWER_LEVEL') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("nmr presaturation power level: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="nmr presaturation power level")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:CHEMICAL_SHIFT REFERENCE COMPOUND') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("chemical shift reference compound: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="chemical shift reference compound")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:NUMBER_OF_SCANS') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("number of scans: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="number of scans")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:DUMMY_SCANS') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("dummy scans: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="dummy scans")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:ACQUISITION_TIME') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("acquisition time: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="acquisition time")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:RELAXATION_DELAY') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("relaxation delay: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="relaxation delay")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:SPECTRAL_WIDTH') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("spectral width: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="spectral width")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:LINE_BROADENING') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("line broadening: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="line broadering")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:ZERO_FILLING') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("zero filling: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="zero filling")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:APODIZATION') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("apodization: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="apodization")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('NMR:BASELINE_CORRECTION_METHOD') != -1:
                    # protocol_parameters["nmr spectroscopy"].append("baseline correction method: " + row[1])
                    nmr_param_oa = OntologyAnnotation(term="baseline correction method")
                    nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
                    nmr_protocol_params.append(nmr_param)

                if row[0].find('CO:COLLECTION_PROTOCOL_SUMMARY') != -1:
                    collect_protocol = collect_protocol + " " + row[1]

                if row[0].find('CO:COLLECTION_PROTOCOL_FILENAME') != -1:
                    protocol_files[3] = row[1]

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

            oa_st_design = OntologyAnnotation(term=study_design)
            # print(oa_st_design.name)

            study_filename = "s_" + studyid + ".txt"

            study1.title = study_title
            study1.description = str(study_desc)
            study1.submission_date = study_submittedon
            study1.public_release_date = study_createdon
            study1.design_descriptors = [oa_st_design]
            study1.filename = str(study_filename)

            for element in study_assays_dict["assays"]:
                # print("in study_assays_dict: ",element)
                if element["techtype"] == "mass spectrometry":
                    print("detected technology type:", element["techtype"])
                    orefTT = OntologySource(name="OBI", description="Ontology for Biomedical Investigation")
                    oaTT = OntologyAnnotation(term="metabolite profiling", term_accession="", term_source=orefTT)
                    orefMT = OntologySource(name="OBI", description="Ontology for Biomedical Investigation")
                    oaMT = OntologyAnnotation(term="mass spectrometry", term_accession="", term_source=orefMT)

                    this_assay_file = "a_" + str(studyid) + "_" + str(element["analysis_id"]) + ".txt"
                    # print("this assay_file:", this_assay_file)
                    this_assay = Assay(measurement_type=oaTT, technology_type=oaMT, filename=this_assay_file)
                    study1.assays.append(this_assay)

                    downLoadURI = "http://www.metabolomicsworkbench.org/data/study_textformat_view.php?STUDY_ID=" + studyid \
                                  + "&ANALYSIS_ID="

                    downLoadURI = downLoadURI + element["analysis_id"] + "&MODE=d"

                    create_raw_data_files(outputdir, tt, downLoadURI, studyid, element["analysis_id"])

                    generate_maf_file(outputdir, studyid,element["analysis_id"])

                    assay_records, assay_header, qt1, qt2 = create_ms_assay_records(downLoadURI, studyid,
                                                                                    element["analysis_id"],
                                                                          study_factor_records)

                    write_assay(outputdir, element["techtype"],studyid, element["analysis_id"], assay_records, assay_header)

                elif element["techtype"] == "nmr spectroscopy":
                    print("detected technology type:", element["techtype"])
                    orefTT = OntologySource(name="OBI", description="Ontology for Biomedical Investigation")
                    oaTT = OntologyAnnotation(term="metabolite profiling", term_accession="", term_source=orefTT)
                    orefMT = OntologySource(name="OBI", description="Ontology for Biomedical Investigation")
                    oaMT = OntologyAnnotation(term="nmr spectroscopy", term_accession="", term_source=orefMT)
                    this_assay_file = "a_" + str(studyid) + "_" + str(element["analysis_id"]) + ".txt"
                    # print("this NMR assay_file:", this_assay_file)
                    this_assay = Assay(measurement_type=oaTT, technology_type=oaMT, filename=this_assay_file)
                    study1.assays.append(this_assay)
                    # print("is it here?", study1.name)

                    downLoadURI = "http://www.metabolomicsworkbench.org/data/study_textformat_view.php?STUDY_ID=" +\
                                  studyid  + "&ANALYSIS_ID="

                    downLoadURI = downLoadURI + element["analysis_id"] + "&MODE=d"
                    print("invoking create_raw_data_method for NMR data now\n")
                    create_raw_data_files(outputdir, tt, downLoadURI, studyid, element["analysis_id"])

                    generate_maf_file(outputdir, studyid,element["analysis_id"])

                    assay_records, assay_header, qt1, qt2 = create_nmr_assay_records(downLoadURI, studyid,
                                                                                     element["analysis_id"],
                                                                                     study_factor_records)

                    write_assay(outputdir, element["techtype"], studyid, element["analysis_id"], assay_records, assay_header)

            chromatography_param_oa = OntologyAnnotation(term="injection temperature")
            chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
            chromatography_protocol_params.append(chromatography_param)
            chromatography_param_oa = OntologyAnnotation(term="flow rate")
            chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
            chromatography_protocol_params.append(chromatography_param)
            chromatography_param_oa = OntologyAnnotation(term="solvent a")
            chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
            chromatography_protocol_params.append(chromatography_param)
            chromatography_param_oa = OntologyAnnotation(term="solvent b")
            chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
            chromatography_protocol_params.append(chromatography_param)
            chromatography_param_oa = OntologyAnnotation(term="chromatography setting file")
            chromatography_param = ProtocolParameter(parameter_name=chromatography_param_oa)
            chromatography_protocol_params.append(chromatography_param)

            ms_param_oa = OntologyAnnotation(term="ionization mode")
            ms_param = ProtocolParameter(parameter_name=ms_param_oa)
            ms_protocol_params.append(ms_param)
            ms_param_oa = OntologyAnnotation(term="injection mode")
            ms_param = ProtocolParameter(parameter_name=ms_param_oa)
            ms_protocol_params.append(ms_param)
            ms_param_oa = OntologyAnnotation(term="acquisition file")
            ms_param = ProtocolParameter(parameter_name=ms_param_oa)
            ms_protocol_params.append(ms_param)

            nmr_param_oa = OntologyAnnotation(term="nmr tube size")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)
            nmr_param_oa = OntologyAnnotation(term="chemical shift reference compound")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)
            nmr_param_oa = OntologyAnnotation(term="nmr solvent")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)
            nmr_param_oa = OntologyAnnotation(term="zero filling")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)
            nmr_param_oa = OntologyAnnotation(term="spectrometer frequency")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)
            nmr_param_oa = OntologyAnnotation(term="relaxation delay")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)
            nmr_param_oa = OntologyAnnotation(term="apodization")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)
            nmr_param_oa = OntologyAnnotation(term="number of scans")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)
            nmr_param_oa = OntologyAnnotation(term="baseline correction method")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)
            nmr_param_oa = OntologyAnnotation(term="nmr solvent")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)
            nmr_param_oa = OntologyAnnotation(term="nmr probe")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)
            nmr_param_oa = OntologyAnnotation(term="nmr type")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)
            nmr_param_oa = OntologyAnnotation(term="shimming method")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)
            nmr_param_oa = OntologyAnnotation(term="nmr instrument")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)
            nmr_param_oa = OntologyAnnotation(term="pulse program")
            nmr_param = ProtocolParameter(parameter_name=nmr_param_oa)
            nmr_protocol_params.append(nmr_param)

            ident_param_oa = OntologyAnnotation(term="analysis file")
            ident_param = ProtocolParameter(parameter_name=ident_param_oa)
            ident_protocol_params.append(ident_param)
            ident_param_oa = OntologyAnnotation(term="software")
            ident_param = ProtocolParameter(parameter_name=ident_param_oa)
            ident_protocol_params.append(ident_param)

            oa_coll_prot = OntologyAnnotation(term="material collection")
            collection_protocol = Protocol(name="sample collection protocol", description=collect_protocol,
                                           uri=protocol_files[3], protocol_type=oa_coll_prot)
            study1.protocols.append(collection_protocol)

            oa_sample_prot = OntologyAnnotation(term="material preparation")
            sample_protocol = Protocol(name="metabolite extraction protocol", description=sampleprep_protocol,
                                       uri=protocol_files[2], protocol_type=oa_sample_prot)
            study1.protocols.append(sample_protocol)

            oa_treat = OntologyAnnotation(term="material processing")
            treatment_protocol = Protocol(name="treatment protocol", description=treat_protocol, uri=protocol_files[1],
                                          protocol_type=oa_treat)
            study1.protocols.append(treatment_protocol)

            oa_chromato_prot = OntologyAnnotation(term="chromatography")
            chromato_protocol = Protocol(name="chromatography protocol", description=chromatography_protocol,
                                         parameters=chromatography_protocol_params,
                                         uri="", protocol_type=oa_chromato_prot)
            study1.protocols.append(chromato_protocol)

            oa_ms_prot = OntologyAnnotation(term="mass spectrometry")
            ms_protocol = Protocol(name="mass spectrometry protocol", description=mass_spec_protocol,
                                   parameters=ms_protocol_params, uri="", protocol_type=oa_ms_prot)
            study1.protocols.append(ms_protocol)

            oa_nmr_prot = OntologyAnnotation(term="nmr spectroscopy")
            nmr_protocol = Protocol(name="nuclear magnetic resonance spectroscopy protocol",
                                    description=nmrspc_protocol,
                                    parameters=nmr_protocol_params, protocol_type=oa_nmr_prot)
            study1.protocols.append(nmr_protocol)

            oa_ident_prot = OntologyAnnotation(term="identification")
            ident_protocol = Protocol(name="identification protocol", description="ridiculous",
                                      protocol_type=oa_ident_prot,
                                      parameters=ident_protocol_params)
            study1.protocols.append(ident_protocol)

            study1.protocols.append(Protocol(name="annotation protocol", protocol_type=OntologyAnnotation(term="annotation")))

            publication = Publication(pubmed_id='12314444', status=OntologyAnnotation())
            study1.publications.append(publication)

            person1 = Person(first_name=study_person_firstname, last_name=study_person_lastname,
                             email=study_person_email,
                             address=study_person_address, affiliation=study_person_affiliation, fax=study_person_fax,
                             comments=list())
            person1.comments.append(Comment(name="Grant Information", value=study_funder))
            study1.contacts.append(person1)

            # Building Investigation Study Factor Section:
            factor_keys = study_factors.keys()
            for key in study_factors.keys():
                oref = OntologySource(name="OBI", description="Ontology for Biomedical Investigation")
                oa = OntologyAnnotation(term=key, term_accession="", term_source=oref)
                study1.factors.append(StudyFactor(name=key, factor_type=oa))

            protocol_descriptions[0] = collect_protocol
            protocol_descriptions[1] = treat_protocol
            protocol_descriptions[2] = sampleprep_protocol

            studyfileheader = basestudysamplerecordheader + fv_record_header

            # ATTEMPTING TO WRITE STUDY FILES:
            write_study_file(outputdir, studyid, studyfileheader, study_factor_records)

            # ATTEMPTING TO WRITE INVESTIGATION FILE:
            try:
                print("writing 'investigation information' to file...")
                print(isatab.dumps(investigation))
                isatab.dump(investigation, outputpath)
            except IOError:
                print("Error: in main() method can\'t open file or write data")
            # else:
            #  print("doh, something went wrong while writing investigation but don't know why!: from main method")

            # ATTEMPTING TO DOWNLOAD THE CORRESPONDING DATA ARCHIVE FROM MW ANONYMOUS FTP:
            if dl_option == 'yes':
                get_archived_file(studyid)
            elif dl_option == 'no':
                print('user elected not to dowload raw data')
            else:
                print('user input not recognized')

    except Exception as e:
        logging.exception(e)
        print("Error: in main() method something went wrong")
        print("conversion failed\n")
        conversion_success = False

    return conversion_success, studyid, validate_option

