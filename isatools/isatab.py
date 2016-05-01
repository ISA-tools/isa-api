from pandas.util.testing import assert_frame_equal
from .model.v1 import *
from isatools.io import isatab_parser
import os
import sys
import pandas as pd
import io
import networkx as nx
import itertools
import logging
import numpy as np
import re
from isatools.validate.utils import check_doi, check_encoding, is_iso8601_date, check_pubmed_id, ValidationReport, ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _read_investigation_file(fp, report=None):
    """Parses investigation file and returns a dictionary of dataframes of each section"""

    def _peek(f):
        position = f.tell()
        l = f.readline()
        f.seek(position)
        return l

    def _read_tab_section(f, sec_key, next_sec_key=None):

        line = f.readline()
        if not line.rstrip() == sec_key:
            raise ValidationError("Expected: " + sec_key + " section, but got: " + line)
        memf = io.StringIO()
        while not _peek(f=f).rstrip() == next_sec_key:
            line = f.readline()
            if not line:
                break
            if line.startswith('#'):
                pass  # skip reading lines beginning with a # as they are comments to be ignored
            else:
                memf.write(line.rstrip() + '\n')
        memf.seek(0)
        return memf

    def _build_section_df(f):
        import numpy as np
        try:
            df = pd.read_csv(f, sep='\t').T  # Load and transpose ISA file section
            df.replace(np.nan, '', regex=True, inplace=True)  # Strip out the nan entries
            df.reset_index(inplace=True)  # Reset index so it is accessible as column
            df.columns = df.iloc[0]  # If all was OK, promote this row to the column headers
            df = df.reindex(df.index.drop(0))  # Reindex the DataFrame
        except ValueError:
            report.fatal("A section of the investigation file has no content")
            raise ValidationError("A section of the investigation file has no content")
        return df

    df_dict = dict()

    # Read in investigation file into DataFrames first
    df_dict['ONTOLOGY SOURCE REFERENCE'] = _build_section_df(_read_tab_section(
        f=fp,
        sec_key='ONTOLOGY SOURCE REFERENCE',
        next_sec_key='INVESTIGATION'
    ))
    df_dict['INVESTIGATION'] = _build_section_df(_read_tab_section(
        f=fp,
        sec_key='INVESTIGATION',
        next_sec_key='INVESTIGATION PUBLICATIONS'
    ))
    df_dict['INVESTIGATION PUBLICATIONS'] = _build_section_df(_read_tab_section(
        f=fp,
        sec_key='INVESTIGATION PUBLICATIONS',
        next_sec_key='INVESTIGATION CONTACTS'
    ))
    df_dict['INVESTIGATION CONTACTS'] = _build_section_df(_read_tab_section(
        f=fp,
        sec_key='INVESTIGATION CONTACTS',
        next_sec_key='STUDY'
    ))
    if not {'Term Source Name', 'Term Source File', 'Term Source Version', 'Term Source Description'}\
            .issubset(set(df_dict['ONTOLOGY SOURCE REFERENCE'].columns)):
        logger.fatal("ONTOLOGY SOURCE REFERENCE section does not contain required fields")
        raise ValidationError("ONTOLOGY SOURCE REFERENCE section does not contain required fields")
    if not {'Investigation Identifier', 'Investigation Title', 'Investigation Description',
            'Investigation Submission Date', 'Investigation Public Release Date'}\
            .issubset(set(df_dict['INVESTIGATION'].columns)):
        logger.fatal("INVESTIGATION section does not contain required fields")
        raise ValidationError("INVESTIGATION section does not contain required fields")
    if not {'Investigation PubMed ID', 'Investigation Publication DOI', 'Investigation Publication Author List',
            'Investigation Publication Title', 'Investigation Publication Status',
            'Investigation Publication Status Term Accession Number',
            'Investigation Publication Status Term Source REF'}\
            .issubset(set(df_dict['INVESTIGATION PUBLICATIONS'].columns)):
        logger.fatal("INVESTIGATION PUBLICATIONS section does not contain required fields")
        raise ValidationError("INVESTIGATION PUBLICATIONS section does not contain required fields")
    if not {'Investigation Person Last Name', 'Investigation Person First Name', 'Investigation Person Mid Initials',
            'Investigation Person Email', 'Investigation Person Phone', 'Investigation Person Fax',
            'Investigation Person Address', 'Investigation Person Affiliation', 'Investigation Person Roles',
            'Investigation Person Roles Term Accession Number', 'Investigation Person Roles Term Source REF'}\
            .issubset(set(df_dict['INVESTIGATION CONTACTS'].columns)):
            logger.fatal("INVESTIGATION CONTACTS section does not contain required fields")
            raise ValidationError("INVESTIGATION CONTACTS section does not contain required fields")
    study_count = 0
    while _peek(fp):  # Iterate through STUDY blocks until end of file
        df_dict['STUDY.' + str(study_count)] = _build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY',
            next_sec_key='STUDY DESIGN DESCRIPTORS'
        ))
        df_dict['STUDY DESIGN DESCRIPTORS.' + str(study_count)] = _build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY DESIGN DESCRIPTORS',
            next_sec_key='STUDY PUBLICATIONS'
        ))
        df_dict['STUDY PUBLICATIONS.' + str(study_count)] = _build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY PUBLICATIONS',
            next_sec_key='STUDY FACTORS'
        ))
        df_dict['STUDY FACTORS.' + str(study_count)] = _build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY FACTORS',
            next_sec_key='STUDY ASSAYS'
        ))
        df_dict['STUDY ASSAYS.' + str(study_count)] = _build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY ASSAYS',
            next_sec_key='STUDY PROTOCOLS'
        ))
        df_dict['STUDY PROTOCOLS.' + str(study_count)] = _build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY PROTOCOLS',
            next_sec_key='STUDY CONTACTS'
        ))
        df_dict['STUDY CONTACTS.' + str(study_count)] = _build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY CONTACTS',
            next_sec_key='STUDY'
        ))
        if not {'Study Identifier', 'Study Title', 'Study Description'}\
                .issubset(set(df_dict['STUDY.' + str(study_count)].columns)):
            logger.fatal("STUDY section does not contain required fields")
            raise ValidationError("STUDY.{} section does not contain required fields".format(study_count))
        if not {'Study Design Type', 'Study Design Type Term Accession Number', 'Study Design Type Term Source REF'}\
                .issubset(set(df_dict['STUDY DESIGN DESCRIPTORS.' + str(study_count)].columns)):
            logger.fatal("STUDY DESIGN DESCRIPTORS.{} section does not contain required fields".format(study_count))
            raise ValidationError("STUDY DESIGN DESCRIPTORS.{} section does not contain required fields".format(study_count))
        if not {'Study PubMed ID', 'Study Publication DOI', 'Study Publication Author List', 'Study Publication Title',
                'Study Publication Status', 'Study Publication Status Term Accession Number',
                'Study Publication Status Term Source REF'}\
                .issubset(set(df_dict['STUDY PUBLICATIONS.' + str(study_count)].columns)):
            logger.fatal("STUDY PUBLICATIONS.{} section does not contain required fields".format(study_count))
            raise ValidationError("STUDY PUBLICATIONS.{} section does not contain required fields".format(study_count))
        if not {'Study Factor Name', 'Study Factor Type', 'Study Factor Type Term Accession Number',
                'Study Factor Type Term Source REF'}\
                .issubset(set(df_dict['STUDY FACTORS.' + str(study_count)].columns)):
            logger.fatal("STUDY FACTORS.{} section does not contain required fields".format(study_count))
            raise ValidationError("STUDY FACTORS.{} section does not contain required fields".format(study_count))
        if not {'Study Assay Measurement Type', 'Study Assay Measurement Type Term Accession Number',
                'Study Assay Measurement Type Term Source REF', 'Study Assay Technology Type',
                'Study Assay Technology Type Term Accession Number', 'Study Assay Technology Type Term Source REF',
                'Study Assay Technology Platform', 'Study Assay File Name'}\
                .issubset(set(df_dict['STUDY ASSAYS.' + str(study_count)].columns)):
            logger.fatal("STUDY ASSAYS.{} section does not contain required fields".format(study_count))
            raise ValidationError("STUDY ASSAYS.{} section does not contain required fields".format(study_count))
        if not {'Study Protocol Name', 'Study Protocol Type', 'Study Protocol Type Term Accession Number',
                'Study Protocol Type Term Source REF', 'Study Protocol Description', 'Study Protocol URI',
                'Study Protocol Version', 'Study Protocol Parameters Name',
                'Study Protocol Parameters Name Term Accession Number',
                'Study Protocol Parameters Name Term Source REF', 'Study Protocol Components Name',
                'Study Protocol Components Type', 'Study Protocol Components Type Term Accession Number',
                'Study Protocol Components Type Term Source REF'}\
                .issubset(set(df_dict['STUDY PROTOCOLS.' + str(study_count)].columns)):
            logger.fatal("STUDY PROTOCOLS.{} section does not contain required fields".format(study_count))
            raise ValidationError("STUDY PROTOCOLS.{} section does not contain required fields".format(study_count))
        if not {'Study Person Last Name', 'Study Person First Name', 'Study Person Mid Initials', 'Study Person Email',
                'Study Person Phone', 'Study Person Fax', 'Study Person Address', 'Study Person Affiliation',
                'Study Person Roles', 'Study Person Roles Term Accession Number', 'Study Person Roles Term Source REF'}\
                .issubset(set(df_dict['STUDY CONTACTS.' + str(study_count)].columns)):
            logger.fatal("STUDY CONTACTS.{} section does not contain required fields".format(study_count))
            raise ValidationError("STUDY CONTACTS.{} section does not contain required fields".format(study_count))
        study_count += 1
    return df_dict


def validate_tab(isatab_dir, reporting_level=logging.INFO):
    """Validate an ISA tab archive (directory)"""
    logging.basicConfig(level=reporting_level)
    # Check if an i_ file exists
    try:
        i_file = [fname for fname in os.listdir(isatab_dir) if fname.startswith('i_') and fname.endswith('.txt')]
        if len(i_file) > 1:
            logger.fatal("More than one investigation was found in the given directory")
            raise ValidationError
        validate_i_file(open(os.path.join(isatab_dir, i_file[0])))
    except ValidationError as i_file_validation_error:
        logger.fatal("There was an error when validating the structure of the ISA tab investigation file")
        raise i_file_validation_error


def validate_i_file(i_fp):
    """Validate an ISA tab, starting from i_ file"""

    def _check_i_sections(fp, report):

        def _peek(f):
            position = f.tell()
            l = f.readline()
            f.seek(position)
            return l

        def _read_tab_section(f, sec_key, next_sec_key=None):

            line = f.readline()
            if not line.rstrip() == sec_key:
                report.fatal("Expected {} section but got {}".format(line.rstrip(), sec_key))
                raise ValidationError(report.generate_report())
            memf = io.StringIO()
            while not _peek(f=f).rstrip() == next_sec_key:
                line = f.readline()
                if not line:
                    break
                if line.startswith('#'):
                    pass  # skip reading lines beginning with a # as they are comments to be ignored
                else:
                    memf.write(line.rstrip() + '\n')
            memf.seek(0)
            return memf

        file_section_dict = dict()
        # Split up sections of the i file first
        file_section_dict['ONTOLOGY SOURCE REFERENCE'] = _read_tab_section(
            f=fp,
            sec_key='ONTOLOGY SOURCE REFERENCE',
            next_sec_key='INVESTIGATION',
        )
        file_section_dict['INVESTIGATION'] = _read_tab_section(
            f=fp,
            sec_key='INVESTIGATION',
            next_sec_key='INVESTIGATION PUBLICATIONS'
        )
        file_section_dict['INVESTIGATION PUBLICATIONS'] = _read_tab_section(
            f=fp,
            sec_key='INVESTIGATION PUBLICATIONS',
            next_sec_key='INVESTIGATION CONTACTS'
        )
        file_section_dict['INVESTIGATION CONTACTS'] = _read_tab_section(
            f=fp,
            sec_key='INVESTIGATION CONTACTS',
            next_sec_key='STUDY'
        )

        study_count = 0
        while _peek(fp):
            file_section_dict['STUDY.{}'.format(study_count)] = _read_tab_section(
                f=fp,
                sec_key='STUDY',
                next_sec_key='STUDY DESIGN DESCRIPTORS'
            )
            file_section_dict['STUDY DESIGN DESCRIPTORS.{}'.format(study_count)] = _read_tab_section(
                f=fp,
                sec_key='STUDY DESIGN DESCRIPTORS',
                next_sec_key='STUDY PUBLICATIONS'
            )
            file_section_dict['STUDY PUBLICATIONS.{}'.format(study_count)] = _read_tab_section(
                f=fp,
                sec_key='STUDY PUBLICATIONS',
                next_sec_key='STUDY FACTORS'
            )
            file_section_dict['STUDY FACTORS.{}'.format(study_count)] = _read_tab_section(
                f=fp,
                sec_key='STUDY FACTORS',
                next_sec_key='STUDY ASSAYS'
            )
            file_section_dict['STUDY ASSAYS.{}'.format(study_count)] = _read_tab_section(
                f=fp,
                sec_key='STUDY ASSAYS',
                next_sec_key='STUDY PROTOCOLS'
            )
            file_section_dict['STUDY PROTOCOLS.{}'.format(study_count)] = _read_tab_section(
                f=fp,
                sec_key='STUDY PROTOCOLS',
                next_sec_key='STUDY CONTACTS'
            )
            file_section_dict['STUDY CONTACTS.{}'.format(study_count)] = _read_tab_section(
                f=fp,
                sec_key='STUDY CONTACTS',
                next_sec_key='STUDY'
            )
            study_count += 1
        return file_section_dict

    def _check_i_section_shape(sec_memf_dict, report):

        def _build_section_df(sec_memf_dict, ref):
            import numpy as np
            df = None
            try:
                sec_memf = sec_memf_dict[ref]
                df = pd.read_csv(sec_memf, sep='\t', header=None).T  # Load and transpose ISA file section
                df.replace(np.nan, '', regex=True, inplace=True)  # Strip out the nan entries
                df.reset_index(inplace=True)  # Reset index so it is accessible as column
                df.columns = df.iloc[0]  # If all was OK, promote this row to the column headers
                df = df.reindex(df.index.drop(0))  # Reindex the DataFrame
            except ValueError:
                report.fatal("{} section of the investigation file has no content ".format(ref))
            return df

        sec_df_dict = dict()
        sec_df_dict['ONTOLOGY SOURCE REFERENCE'] = _build_section_df(sec_memf_dict, 'ONTOLOGY SOURCE REFERENCE')
        sec_df_dict['INVESTIGATION'] = _build_section_df(sec_memf_dict, 'INVESTIGATION')
        i_rows = len(sec_df_dict['INVESTIGATION'].index)
        if i_rows > 1: report.fatal("INVESTIGATION section should only have 1 record. Found {} records.".format(i_rows))
        sec_df_dict['INVESTIGATION PUBLICATIONS'] = _build_section_df(sec_memf_dict, 'INVESTIGATION PUBLICATIONS')
        sec_df_dict['INVESTIGATION CONTACTS'] = _build_section_df(sec_memf_dict, 'INVESTIGATION CONTACTS')
        for study_count in range(0, len([k for k in sec_memf_dict.keys() if k.startswith('STUDY.')])):
            sec_df_dict['STUDY.{}'.format(study_count)] = _build_section_df(sec_memf_dict, 'STUDY.{}'.format(study_count))
            s_rows = len(sec_df_dict['STUDY.{}'.format(study_count)].index)
            if s_rows > 1: report.fatal("STUDY.{0} section should only have 1 record. Found {1} records.".format(study_count, i_rows))
            sec_df_dict['STUDY DESIGN DESCRIPTORS.{}'.format(study_count)] = _build_section_df(sec_memf_dict, 'STUDY DESIGN DESCRIPTORS.{}'.format(study_count))
            sec_df_dict['STUDY PUBLICATIONS.{}'.format(study_count)] = _build_section_df(sec_memf_dict, 'STUDY PUBLICATIONS.{}'.format(study_count))
            sec_df_dict['STUDY FACTORS.{}'.format(study_count)] = _build_section_df(sec_memf_dict, 'STUDY FACTORS.{}'.format(study_count))
            sec_df_dict['STUDY ASSAYS.{}'.format(study_count)] = _build_section_df(sec_memf_dict, 'STUDY ASSAYS.{}'.format(study_count))
            sec_df_dict['STUDY PROTOCOLS.{}'.format(study_count)] = _build_section_df(sec_memf_dict, 'STUDY PROTOCOLS.{}'.format(study_count))
            sec_df_dict['STUDY CONTACTS.{}'.format(study_count)] = _build_section_df(sec_memf_dict, 'STUDY CONTACTS.{}'.format(study_count))
        return sec_df_dict

    def _check_i_sections_content(sec_df_dict, report):

        def _check_i_labels_values(sec_df_dict, sec_label, fields):
            sec_df = sec_df_dict[sec_label]

            # check if required labels exist
            # headers = [field['header'] for field in fields]
            headers_list = list()
            for field in fields:
                header = field['header']
                headers_list.append(header)
                if field['data-type'] == 'Ontology term':
                    headers_list.append(header + ' Term Accession Number')
                    headers_list.append(header + ' Term Source REF')
            headers = set(headers_list)
            if not headers.issubset(set(sec_df.columns)):
                report.fatal("{0} section does not contain all the required fields. Missing field(s): {1}".format(sec_label, headers - set(sec_df.columns)))

            # check if required values are set
            for i in range(0, len(sec_df.index)):
                for col in sec_df.columns:
                    flag = [field['is-required'] for field in fields if field['header'] == col]
                    if len(flag) > 0:
                        if sec_df.iloc[i][col] == '' and flag[0] is True:
                            if i > 0:
                                report.warn("Field '{0}' of entry {1} in {2} section is missing a required value".format(col, i+1, sec_label))
                            else:
                                report.warn("Field '{0}' in {1} section is missing a required value".format(col, sec_label))

            # check if values given are of correct data-type
            for i in range(0, len(sec_df.index)):
                for col in sec_df.columns:
                    fail = False
                    data_type = [field['data-type'] for field in fields if field['header'] == col]
                    value = sec_df.iloc[i][col]
                    if len(data_type) > 0:
                        if isinstance(value, str):
                            if data_type[0] == 'Date':
                                if not is_iso8601_date(value):
                                    report.warn("Value '{0}' in section {1} in field '{2}' does not conform to ISO8601 (date) formatting".format(value, sec_label, col))
                    if fail:
                        if i > 0:
                            report.warn("Field '{0}' of entry {1} in {2} section is missing a required value".format(col, i+1, sec_label))
                        else:
                            report.warn("Field '{0}' in {1} section is missing a required value".format(col, sec_label))

        from isatools.io import isatab_configurator
        config = isatab_configurator.load(os.path.join(os.path.dirname(__file__), '../tests/data/Configurations/isaconfig-default_v2015-07-02'))
        inv_config = config[('[investigation]', '')]
        i_fields = [field for field in inv_config['fields'] if field['section'] == 'INVESTIGATION']
        i_pub_fields = [field for field in inv_config['fields'] if field['section'] == 'INVESTIGATION PUBLICATIONS']
        i_contacts_fields = [field for field in inv_config['fields'] if field['section'] == 'INVESTIGATION CONTACTS']
        s_fields = [field for field in inv_config['fields'] if field['section'] == 'STUDY']
        s_des_desc_fields = [field for field in inv_config['fields'] if field['section'] == 'STUDY DESIGN DESCRIPTORS']
        s_pub_is_req = [field for field in inv_config['fields'] if field['section'] == 'STUDY PUBLICATIONS']
        s_factors_is_req = [field for field in inv_config['fields'] if field['section'] == 'STUDY FACTORS']
        s_assays_is_req = [field for field in inv_config['fields'] if field['section'] == 'STUDY ASSAYS']
        s_protocols_is_req = [field for field in inv_config['fields'] if field['section'] == 'STUDY PROTOCOLS']
        s_contacts_is_req = [field for field in inv_config['fields'] if field['section'] == 'STUDY CONTACTS']

        _check_i_labels_values(sec_df_dict, 'INVESTIGATION', i_fields)
        _check_i_labels_values(sec_df_dict, 'INVESTIGATION PUBLICATIONS', i_pub_fields)
        _check_i_labels_values(sec_df_dict, 'INVESTIGATION CONTACTS', i_contacts_fields)
        for study_count in range(0, len([k for k in sec_memf_dict.keys() if k.startswith('STUDY.')])):
            _check_i_labels_values(sec_df_dict, 'STUDY.' + str(study_count), s_fields)
            _check_i_labels_values(sec_df_dict, 'STUDY DESIGN DESCRIPTORS.' + str(study_count), s_des_desc_fields)
            _check_i_labels_values(sec_df_dict, 'STUDY PUBLICATIONS.' + str(study_count), s_pub_is_req)
            _check_i_labels_values(sec_df_dict, 'STUDY FACTORS.' + str(study_count), s_factors_is_req)
            _check_i_labels_values(sec_df_dict, 'STUDY ASSAYS.' + str(study_count), s_assays_is_req)
            _check_i_labels_values(sec_df_dict, 'STUDY PROTOCOLS.' + str(study_count), s_protocols_is_req)
            _check_i_labels_values(sec_df_dict, 'STUDY CONTACTS.' + str(study_count), s_contacts_is_req)

    report = ValidationReport(file_name=i_fp.name)
    check_encoding(fp=i_fp, report=report)  # check file encoding of i file
    sec_memf_dict = _check_i_sections(fp=i_fp, report=report)  # if successful, returns a dict of sections split into memory files
    sec_df_dict = _check_i_section_shape(sec_memf_dict=sec_memf_dict, report=report)  # if successful, returns dataframes of sections
    _check_i_sections_content(sec_df_dict=sec_df_dict, report=report)  # check if required labels and values are there (not ordered)

    # try and find linked files
    for study_count in range(0, len([k for k in sec_memf_dict.keys() if k.startswith('STUDY.')])):
        study_df = sec_df_dict['STUDY.' + str(study_count)]
        study_file_name = study_df.iloc[0]['Study File Name']
        if not os.path.isfile(os.path.join(os.path.dirname(i_fp.name), study_file_name)):
            report.fatal("The referenced study file '{}' does not exist or is not a file".format(study_file_name))
    for study_assay_count in range(0, len([k for k in sec_memf_dict.keys() if k.startswith('STUDY ASSAYS.')])):
        study_assay_df = sec_df_dict['STUDY ASSAYS.' + str(study_assay_count)]
        for i in range(0, len(study_assay_df.index)):
            assay_file_name = study_assay_df.iloc[i]['Study Assay File Name']
            if not os.path.isfile(os.path.join(os.path.dirname(i_fp.name), assay_file_name)):
                report.fatal("The referenced assay file '{}' does not exist or is not a file".format(assay_file_name))

    # if len(report.generate_report_json()['fatal']) > 0:
    report.print_report()
    return
    #
    # i_ont_src_headers = {
    #     'Term Source Name',
    #     'Term Source File',
    #     'Term Source Version',
    #     'Term Source Description'
    # }
    # if not i_ont_src_headers.issubset(set(sec_df_dict['ONTOLOGY SOURCE REFERENCE'].columns)):
    #     report.fatal("ONTOLOGY SOURCE REFERENCE section does not contain required fields\nSkipping Term Source REF checks")
    # else:
    #     ontology_source_references_dict = dict()  # key is Term Source Name
    #     for i, row in sec_df_dict['ONTOLOGY SOURCE REFERENCE'].iterrows():  # load ontology source references
    #         if row['Term Source Name'] == '':
    #             report.warn("Ontology source at position {} has no name so cannot be linked by Term Source REF")
    #         else:
    #             ontology_source_reference = OntologySourceReference(
    #                 name=row['Term Source Name'],
    #                 file=row['Term Source File'],
    #                 version=row['Term Source Version'],
    #                 description=row['Term Source Description']
    #             )
    #             ontology_source_references_dict[ontology_source_reference.name] = ontology_source_reference

    for study_count in range(0, len([k for k in sec_memf_dict.keys() if k.startswith('STUDY.')])):
        study_df = sec_df_dict['STUDY.' + str(study_count)]
        study_file_name = study_df.iloc[0]['Study File Name']
        validate_s_file(open(os.path.join(os.path.dirname(i_fp.name), study_file_name)))
    report.print_report()


def _is_valid_tab_header(header):
    char_regex = re.compile('Characteristics\[(.*?)\]')
    fv_regex = re.compile('Factor Value\[(.*?)\]')
    static_tab_headers = ['Source Name', 'Sample Name', 'Term Source REF', 'Term Accession Number', 'Protocol REF', 'Unit']
    return (header in static_tab_headers) or char_regex.match(header) is not None or fv_regex.match(header) is not None


def validate_s_file(s_fp):
    """Validate an ISA tab s_ file"""

    def _clean_comments_from_file(fp):
        memf = io.StringIO()
        for line in fp:
            if not line.startswith('#'):
             memf.write(line)
        memf.seek(0)
        return memf

    def _check_s_headers(fp, report):
        char_regex = re.compile('Characteristics\[(.*?)\]')
        fv_regex = re.compile('Factor Value\[(.*?)\]')
        # load line one, and tokenize it into column headers
        line = fp.readline()
        headers = line.rstrip().split('\t')
        fp.seek(0)

        # check if the tokens are all valid...
        prev_header = None
        for x, header in enumerate(headers):
            if header.startswith('"') and header.endswith('"'): header = header[1:-1]
            if not _is_valid_tab_header(header):
                report.fatal("Found an invalid header '{}' at column position {}.".format(header, x))
            if prev_header == header:
                report.warn("Consecutive duplicates not allows: header '{}' at column position {} is same as at position {2}.".format(header, x-1, x))
            # check for 'Term Accession Number' after 'Term Source REF' for Characteristics
            if char_regex.match(header):
                try:
                    if headers[x+1] == 'Term Source REF':
                        try:
                            if headers[x+2] != 'Term Accession Number':
                                report.fatal("Header '{}' at column position {} is missing 'Term Accession Number'".format(header, x+2))
                        except IndexError:
                            report.fatal("Header '{}' at column position {} is missing 'Term Accession Number'".format(header, x+2))
                except IndexError:
                    pass
            # check for 'Term Accession Number' after 'Term Source REF' for Factor Values
            if fv_regex.match(header):
                try:
                    if headers[x+1] == 'Term Source REF':
                        try:
                            if headers[x+2] != 'Term Accession Number':
                                report.fatal("Header '{}' at column position {} is missing 'Term Accession Number'".format(header, x+2))
                        except IndexError:
                            report.fatal("Header '{}' at column position {} is missing 'Term Accession Number'".format(header, x+2))
                except IndexError:
                    pass
            prev_header = header

    def _check_s_headers_against_config(df, report):
        from isatools.io import isatab_configurator
        config = isatab_configurator.load(os.path.join(os.path.dirname(__file__), '../tests/data/Configurations/isaconfig-default_v2015-07-02'))
        study_config = config[('[Sample]', '')]

        # Build list of headers from configuration. Prefix headers with an int indicating node ID
        headers_from_config = list()
        fields = study_config['fields']
        node_count = 0
        for x, field in enumerate(fields):
            try:
                header = field['header']
                if header == 'Source Name' or header == 'Sample Name':
                    headers_from_config.append(str(node_count) + '.' + header)
                    offset = 1
                    try:
                        while fields[x+offset]['header'].startswith('Characteristics[') or fields[x+offset]['header'].startswith('Factor Value['):
                            if fields[x+offset]['header'].startswith('Characteristics['):
                                headers_from_config.append(str(node_count) + '.' + fields[x+offset]['header'])
                                if fields[x+offset]['data-type'] == 'Ontology term':
                                    headers_from_config.append(str(node_count) + '.Term Source REF')
                                    headers_from_config.append(str(node_count) + '.Term Accession Number')
                            offset += 1
                    except KeyError:
                        pass
                    finally:
                        node_count += 1
            except KeyError:
                try:
                    if field['protocol-type'] != '':
                        headers_from_config.append(str(node_count) + '.Protocol REF')
                        offset = 1
                        try:
                            while fields[x+offset]['header'].startswith('Parameter Value['):
                                headers_from_config.append(str(node_count) + '.' + fields[x+offset]['header'])
                                offset += 1
                        except KeyError:
                            pass
                        finally:
                            node_count += 1
                except KeyError:
                    pass

        # Build list of headers from ISAtab. Prefix headers with an int indicating node ID
        node_count = 0
        cols_from_study_tab = list(df.columns)
        headers_from_tab = list()
        for x, col in enumerate(cols_from_study_tab):
            if col == 'Source Name' or col == 'Sample Name':
                headers_from_tab.append(str(node_count) + '.' + col)
                offset = 1
                try:
                    while cols_from_study_tab[x+offset].startswith('Characteristics[') or \
                            cols_from_study_tab[x+offset].startswith('Factor Value[') or \
                            cols_from_study_tab[x+offset].startswith('Term Source REF') or \
                            cols_from_study_tab[x+offset].startswith('Term Accession Number'):
                        if cols_from_study_tab[x+offset].startswith('Characteristics['):
                            headers_from_tab.append(str(node_count) + '.' + cols_from_study_tab[x+offset])
                        if cols_from_study_tab[x+offset].startswith('Factor Value['):
                            headers_from_tab.append(str(node_count) + '.' + cols_from_study_tab[x+offset])
                        if cols_from_study_tab[x+offset].startswith('Term Source REF'):
                            headers_from_tab.append(str(node_count) + '.Term Source REF')
                        if cols_from_study_tab[x+offset].startswith('Term Accession Number'):
                            headers_from_tab.append(str(node_count) + '.Term Accession Number')
                        # TODO: Deal with units?
                        offset += 1
                except KeyError:
                    pass
                except IndexError:
                    pass
                finally:
                    node_count += 1
            if col == 'Protocol REF':
                headers_from_tab.append(str(node_count) + '.Protocol REF')
                offset = 1
                try:
                    while cols_from_study_tab[x+offset].startswith('Parameter Value['):
                        headers_from_config.append(str(node_count) + '.' + cols_from_study_tab[x+offset])
                        offset += 1
                except KeyError:
                    pass
                finally:
                    node_count += 1

        # Now the node headers should match up, unless there's an extra node thrown in somewhere...
        if not set(headers_from_config).issubset(set(headers_from_tab)):
            report.fatal("Required node headers in study file '{0} are not present.\n"
                         "Configuration specifies: {1}\n"
                         "Found in ISAtab: {2}\n"
                         "Missing headers are {3}: ".format(s_fp.name, headers_from_config, headers_from_tab,
                                                            set(headers_from_config) - set(headers_from_tab)))

    report = ValidationReport(file_name=s_fp.name)
    check_encoding(fp=s_fp, report=report)  # check file encoding of i file
    clean_s_fp = _clean_comments_from_file(fp=s_fp)
    _check_s_headers(fp=clean_s_fp, report=report)
    study_tab_df = pd.read_csv(clean_s_fp, sep='\t')  # should fail is shape is wrong
    _check_s_headers_against_config(df=study_tab_df, report=report)
    # _check_s_content_against_i_content(i_df=inv_tab_df, study_df=study_tab_df, report=report)
    report.print_report()


def validate(isatab_dir, config_dir):
    """ Validate an ISA-Tab archive using the Java validator that is embedded in the Python ISA-API
    :param isatab_dir: Path to ISA-Tab files
    :param config_dir: Path to configuration XML files
    """
    if not os.path.exists(isatab_dir):
        raise IOError("isatab_dir " + isatab_dir + " does not exist")
    print("Using source ISA Tab folder: " + isatab_dir)
    print("ISA configuration XML folder: " + config_dir)
    convert_command = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "convert/isa_line_commands/bin/validate.sh -c " + config_dir + " " + isatab_dir)
    from subprocess import call
    try:
        return_code = call([convert_command], shell=True)
        if return_code < 0:
            print(sys.stderr, "Terminated by signal", -return_code)
        else:
            print(sys.stderr, "Returned", return_code)
    except OSError as e:
        print(sys.stderr, "Execution failed:", e)


def dump(isa_obj, output_path):

    def _build_roles_str(roles=list()):
        roles_names = ''
        roles_accession_numbers = ''
        roles_source_refs = ''
        for role in roles:
            roles_names += role.name + ';'
            roles_accession_numbers += role.term_accession + ';'
            roles_source_refs += role.term_source + ';'
        if len(roles) > 0:
            roles_names = roles_names[:-1]
            roles_accession_numbers = roles_accession_numbers[:-1]
            roles_source_refs = roles_source_refs[:-1]
        return roles_names, roles_accession_numbers, roles_source_refs

    def _build_contacts_section_df(prefix='Investigation', contacts=list()):
        contacts_df_cols = [prefix + ' Person Last Name',
                            prefix + ' Person First Name',
                            prefix + ' Person Mid Initials',
                            prefix + ' Person Email',
                            prefix + ' Person Phone',
                            prefix + ' Person Fax',
                            prefix + ' Person Address',
                            prefix + ' Person Affiliation',
                            prefix + ' Person Roles',
                            prefix + ' Person Roles Term Accession Number',
                            prefix + ' Person Roles Term Source REF']
        if len(contacts) > 0:
            for comment in contacts[0].comments:
                contacts_df_cols.append('Comment[' + comment.name + ']')
        contacts_df = pd.DataFrame(columns=tuple(contacts_df_cols))
        for i, contact in enumerate(contacts):
            roles_names, roles_accession_numbers, roles_source_refs = _build_roles_str(contact.roles)
            contacts_df_row = [
                contact.last_name,
                contact.first_name,
                contact.mid_initials,
                contact.email,
                contact.phone,
                contact.fax,
                contact.address,
                contact.affiliation,
                roles_names,
                roles_accession_numbers,
                roles_source_refs
            ]
            for comment in contact.comments:
                contacts_df_row.append(comment.value)
            contacts_df.loc[i] = contacts_df_row
        return contacts_df.set_index(prefix + ' Person Last Name').T

    def _build_publications_section_df(prefix='Investigation', publications=list()):
        publications_df_cols = pd.DataFrame(columns=(prefix + ' PubMed ID',
                                                     prefix + ' Publication DOI',
                                                     prefix + ' Publication Author List',
                                                     prefix + ' Publication Title',
                                                     prefix + ' Publication Status',
                                                     prefix + ' Publication Status Term Accession Number',
                                                     prefix + ' Publication Status Term Source REF'
                                                     )
                                            )
        if len(publications) > 0:
            for comment in publications[0].comments:
                publications_df_cols.append('Comment[' + comment.name + ']')
        publications_df = pd.DataFrame(columns=tuple(publications_df_cols))
        for i, publication in enumerate(publications):
            publications_df_row = [
                publication.pubmed_id,
                publication.doi,
                publication.author_list,
                publication.title,
                publication.status.name,
                publication.status.term_accession,
                publication.status.term_source,
            ]
            for comment in publication.comments:
                publications_df_row.append(comment.value)
            publications_df.loc[i] = publications_df_row
        return publications_df.set_index(prefix +' PubMed ID').T

    if os.path.exists(output_path):
        fp = open(os.path.join(output_path, 'i_investigation.txt'), 'w')
    else:
        raise FileNotFoundError("Can't find " + output_path)
    if not isinstance(isa_obj, Investigation):
        raise NotImplementedError("Can only dump an Investigation object")

    # Process Investigation object first to write the investigation file
    investigation = isa_obj

    # Write ONTOLOGY SOURCE REFERENCE section
    ontology_source_references_df = pd.DataFrame(columns=('Term Source Name',
                                                          'Term Source File',
                                                          'Term Source Version',
                                                          'Term Source Description'
                                                          )
                                                 )
    for i,  ontology_source_reference in enumerate(investigation.ontology_source_references):
        ontology_source_references_df.loc[i] = [
            ontology_source_reference.name,
            ontology_source_reference.file,
            ontology_source_reference.version,
            ontology_source_reference.description
        ]
    ontology_source_references_df = ontology_source_references_df.set_index('Term Source Name').T
    fp.write('ONTOLOGY SOURCE REFERENCE\n')
    ontology_source_references_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                         index_label='Term Source Name')  # Need to set index_label as top left cell
    #
    #  Write INVESTIGATION section
    inv_df_cols = ['Investigation Identifier',
                   'Investigation Title',
                   'Investigation Description',
                   'Investigation Submission Date',
                   'Investigation Public Release Date']
    for comment in sorted(investigation.comments, key=lambda x: x.name):
        inv_df_cols.append('Comment[' + comment.name + ']')
    investigation_df = pd.DataFrame(columns=tuple(inv_df_cols))
    inv_df_rows = [
        investigation.identifier,
        investigation.title,
        investigation.description,
        investigation.submission_date,
        investigation.public_release_date
    ]
    for comment in sorted(investigation.comments, key=lambda x: x.name):
        inv_df_rows.append(comment.value)
    investigation_df.loc[0] = inv_df_rows
    investigation_df = investigation_df.set_index('Investigation Identifier').T
    fp.write('INVESTIGATION\n')
    investigation_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                            index_label='Investigation Identifier')  # Need to set index_label as top left cell

    # Write INVESTIGATION PUBLICATIONS section
    investigation_publications_df = _build_publications_section_df(publications=investigation.publications)
    fp.write('INVESTIGATION PUBLICATIONS\n')
    investigation_publications_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                         index_label='Investigation PubMed ID')

    # Write INVESTIGATION CONTACTS section
    investigation_contacts_df = _build_contacts_section_df(contacts=investigation.contacts)
    fp.write('INVESTIGATION CONTACTS\n')
    investigation_contacts_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                     index_label='Investigation Person Last Name')

    # Write STUDY sections
    for study in investigation.studies:
        study_df_cols = ['Study Identifier',
                         'Study Title',
                         'Study Description',
                         'Study Submission Date',
                         'Study Public Release Date',
                         'Study File Name']
        for comment in sorted(study.comments, key=lambda x: x.name):
            study_df_cols.append('Comment[' + comment.name + ']')
        study_df = pd.DataFrame(columns=tuple(study_df_cols))
        study_df_row = [
            study.identifier,
            study.title,
            study.description,
            study.submission_date,
            study.public_release_date,
            study.filename
        ]
        for comment in sorted(study.comments, key=lambda x: x.name):
            study_df_row.append(comment.value)
        study_df.loc[0] = study_df_row
        study_df = study_df.set_index('Study Identifier').T
        fp.write('STUDY\n')
        study_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8', index_label='Study Identifier')

        # Write STUDY DESIGN DESCRIPTORS section
        study_design_descriptors_df = pd.DataFrame(columns=('Study Design Type',
                                                            'Study Design Type Term Accession Number',
                                                            'Study Design Type Term Source REF'
                                                            )
                                                   )
        for i, design_descriptor in enumerate(study.design_descriptors):
            study_design_descriptors_df.loc[i] = [
                design_descriptor.name,
                design_descriptor.term_accession,
                design_descriptor.term_source
            ]
            study_design_descriptors_df = study_design_descriptors_df.set_index('Study Design Type').T
            fp.write('STUDY DESIGN DESCRIPTORS\n')
            study_design_descriptors_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                               index_label='Study Design Type')

        # Write STUDY PUBLICATIONS section
        study_publications_df = _build_publications_section_df(prefix='Study', publications=study.publications)
        fp.write('STUDY PUBLICATIONS\n')
        study_publications_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8', index_label='Study PubMed ID')

        # Write STUDY FACTORS section
        study_factors_df = pd.DataFrame(columns=('Study Factor Name',
                                                 'Study Factor Type',
                                                 'Study Factor Type Term Accession Number',
                                                 'Study Factor Type Term Source REF'
                                                 )
                                        )
        for i, factor in enumerate(study.factors):
            study_factors_df.loc[i] = [
                factor.name,
                factor.factor_type.name,
                factor.factor_type.term_accession,
                factor.factor_type.term_source
            ]
        study_factors_df = study_factors_df.set_index('Study Factor Name').T
        fp.write('STUDY FACTORS\n')
        study_factors_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                index_label='Study Factor Name')

        # Write STUDY ASSAYS section
        study_assays_df = pd.DataFrame(columns=(
                                                'Study Assay File Name',
                                                'Study Assay Measurement Type',
                                                'Study Assay Measurement Type Term Accession Number',
                                                'Study Assay Measurement Type Term Source REF',
                                                'Study Assay Technology Type',
                                                'Study Assay Technology Type Term Accession Number',
                                                'Study Assay Technology Type Term Source REF',
                                                'Study Assay Technology Platform',
                                                )
                                       )
        for i, assay in enumerate(study.assays):
            study_assays_df.loc[i] = [
                assay.filename,
                assay.measurement_type.name,
                assay.measurement_type.term_accession,
                assay.measurement_type.term_source,
                assay.technology_type.name,
                assay.technology_type.term_accession,
                assay.technology_type.term_source,
                assay.technology_platform
            ]
        study_assays_df = study_assays_df.set_index('Study Assay File Name').T
        fp.write('STUDY ASSAYS\n')
        study_assays_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                               index_label='Study Assay File Name')

        # Write STUDY PROTOCOLS section
        study_protocols_df = pd.DataFrame(columns=('Study Protocol Name',
                                                   'Study Protocol Type',
                                                   'Study Protocol Type Term Accession Number',
                                                   'Study Protocol Type Term Source REF',
                                                   'Study Protocol Description',
                                                   'Study Protocol URI',
                                                   'Study Protocol Version',
                                                   'Study Protocol Parameters Name',
                                                   'Study Protocol Parameters Name Term Accession Number',
                                                   'Study Protocol Parameters Name Term Source REF',
                                                   'Study Protocol Components Name',
                                                   'Study Protocol Components Type',
                                                   'Study Protocol Components Type Term Accession Number',
                                                   'Study Protocol Components Type Term Source REF',
                                                   )
                                          )
        for i, protocol in enumerate(study.protocols):
            parameters_names = ''
            parameters_accession_numbers = ''
            parameters_source_refs = ''
            for parameter in protocol.parameters:
                parameters_names += parameter.parameter_name.name + ';'
                parameters_accession_numbers += parameter.parameter_name.term_accession + ';'
                if parameter.parameter_name.term_source == '':
                    parameters_source_refs += parameter.parameter_name.term_source + ';'
                elif isinstance(parameter.parameter_name.term_source, OntologySourceReference):
                    parameters_source_refs += parameter.parameter_name.term_source.name + ';'
            if len(protocol.parameters) > 0:
                parameters_names = parameters_names[:-1]
                parameters_accession_numbers = parameters_accession_numbers[:-1]
                parameters_source_refs = parameters_source_refs[:-1]
            component_names = ''
            component_types = ''
            component_types_accession_numbers = ''
            component_types_source_refs = ''
            for component in protocol.components:
                component_names += component.name + ';'
                component_types += component.component_type.name + ';'
                component_types_accession_numbers += component.component_type.term_accession + ';'
                component_types_source_refs += component.component_type.term_source + ';'
            if len(protocol.components) > 0:
                component_names = component_names[:-1]
                component_types = component_types[:-1]
                component_types_accession_numbers = component_types_accession_numbers[:-1]
                component_types_source_refs = component_types_source_refs[:-1]
            study_protocols_df.loc[i] = [
                protocol.name,
                protocol.protocol_type.name,
                protocol.protocol_type.term_accession,
                protocol.protocol_type.term_source,
                protocol.description,
                protocol.uri,
                protocol.version,
                parameters_names,
                parameters_accession_numbers,
                parameters_source_refs,
                component_names,
                component_types,
                component_types_accession_numbers,
                component_types_source_refs
            ]
        study_protocols_df = study_protocols_df.set_index('Study Protocol Name').T
        fp.write('STUDY PROTOCOLS\n')
        study_protocols_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                  index_label='Study Protocol Name')

        # Write STUDY CONTACTS section
        study_contacts_df = _build_contacts_section_df(prefix='Study', contacts=study.contacts)
        fp.write('STUDY CONTACTS\n')
        study_contacts_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                 index_label='Study Person Last Name')
    write_study_table_files(investigation, output_path)
    write_assay_table_files(investigation, output_path)

    fp.close()
    return investigation


def _get_start_end_nodes(G):
    start_nodes = list()
    end_nodes = list()
    for process in [n for n in G.nodes() if isinstance(n, Process)]:
        if process.prev_process is None:
            for material in [m for m in process.inputs if not isinstance(m, DataFile)]:
                start_nodes.append(material)
        outputs_no_data = [m for m in process.outputs if not isinstance(m, DataFile)]
        if process.next_process is None:
            if len(outputs_no_data) == 0:
                end_nodes.append(process)
            else:
                for material in outputs_no_data:
                    end_nodes.append(material)
    return start_nodes, end_nodes


def _longest_path_and_attrs(G):
    start_nodes, end_nodes = _get_start_end_nodes(G)
    from networkx.algorithms import all_simple_paths
    longest = (0, None)
    for start_node, end_node in itertools.product(start_nodes, end_nodes):
        for path in all_simple_paths(G, start_node, end_node):
            length = len(path)
            for n in path:
                if isinstance(n, Source):
                    length += len(n.characteristics)
                elif isinstance(n, Sample):
                    length += (len(n.characteristics) + len(n.factor_values))
                elif isinstance(n, Material):
                    length += (len(n.characteristics))
                elif isinstance(n, Process):
                    length += (len(n.additional_properties) + len([o for o in n.outputs if isinstance(o, DataFile)]))
                length += len(n.comments)
            if length > longest[0]:
                longest = (length, path)
    return longest[1]

prev = ''  # used in rolling_group(val) in write_assay_table_files(inv_obj, output_dir)


def _all_end_to_end_paths(G, start_nodes, end_nodes):
    paths = list()
    for start, end in itertools.product(start_nodes, end_nodes):
        paths += list(nx.algorithms.all_simple_paths(G, start, end))
    return paths

KEY_POSTFIX_UNIT = '_unit'
KEY_POSTFIX_TERMSOURCE = '_termsource'
KEY_POSTFIX_TERMACCESSION = '_termaccession'
LABEL_UNIT = 'Unit'
LABEL_TERM_SOURCE = 'Term Source REF'
LABEL_TERM_ACCESSION = 'Term Accession Number'
LABEL_PROTOCOL_REF = 'Protocol REF'


def _fv_label(factor_name): return 'Factor Value[' + factor_name + ']'


def _charac_label(charac_type_name): return 'Characteristics[' + charac_type_name + ']'


def _set_charac_cols(prefix, characteristics, cols, col_map):
    for c in sorted(characteristics, key=lambda x: id(x.category)):
        if c.category.name == '': print(c.value.name)
        obj_charac_key = prefix + '_char[' + c.category.name + ']'
        cols.append(obj_charac_key)
        col_map[obj_charac_key] = _charac_label(c.category.name)
        if isinstance(c.value, int) or isinstance(c.value, float):
            cols.extend((obj_charac_key + KEY_POSTFIX_UNIT,
                         obj_charac_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE,
                         obj_charac_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION))
            col_map[obj_charac_key + KEY_POSTFIX_UNIT] = LABEL_UNIT
            col_map[obj_charac_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE] = LABEL_TERM_SOURCE
            col_map[obj_charac_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION] = LABEL_TERM_ACCESSION
        elif isinstance(c.value, OntologyAnnotation):
            cols.extend((obj_charac_key + KEY_POSTFIX_TERMSOURCE,
                         obj_charac_key + KEY_POSTFIX_TERMACCESSION))
            col_map[obj_charac_key + KEY_POSTFIX_TERMSOURCE] = LABEL_TERM_SOURCE
            col_map[obj_charac_key + KEY_POSTFIX_TERMACCESSION] = LABEL_TERM_ACCESSION


def _set_charac_vals(prefix, characteristics, df, i):
    for c in sorted(characteristics, key=lambda x: id(x.category)):
        obj_charac_key = prefix + '_char[' + c.category.name + ']'
        df.loc[i, obj_charac_key] = c.value
        if isinstance(c.value, int) or isinstance(c.value, float):
            df.loc[i, obj_charac_key + KEY_POSTFIX_UNIT] = c.unit.name
            df.loc[i, obj_charac_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE] = c.unit.term_source
            df.loc[i, obj_charac_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION] = c.unit.term_accession
        elif isinstance(c.value, OntologyAnnotation):
            df.loc[i, obj_charac_key] = c.value.name
            df.loc[i, obj_charac_key + KEY_POSTFIX_TERMSOURCE] = c.value.term_source
            df.loc[i, obj_charac_key + KEY_POSTFIX_TERMACCESSION] = c.value.term_accession


def _set_factor_value_cols(prefix, factor_values, cols, col_map):
    for fv in sorted(factor_values, key=lambda x: id(x.category.factor_type.name)):
        factor_name = fv.category.factor_type.name
        obj_fv_key = prefix + '_fv[' + factor_name + ']'
        cols.append(obj_fv_key)
        col_map[obj_fv_key] = _fv_label(factor_name)
        if isinstance(fv.value, int) or isinstance(fv.value, float):
            cols.extend((obj_fv_key + KEY_POSTFIX_UNIT,
                         obj_fv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE,
                         obj_fv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION))
            col_map[obj_fv_key + KEY_POSTFIX_UNIT] = LABEL_UNIT
            col_map[obj_fv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE] = LABEL_TERM_SOURCE
            col_map[obj_fv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION] = LABEL_TERM_ACCESSION
        elif isinstance(fv.value, OntologyAnnotation):
            cols.extend((obj_fv_key + KEY_POSTFIX_TERMSOURCE,
                         obj_fv_key + KEY_POSTFIX_TERMACCESSION))
            col_map[obj_fv_key + KEY_POSTFIX_TERMSOURCE] = LABEL_TERM_SOURCE
            col_map[obj_fv_key + KEY_POSTFIX_TERMACCESSION] = LABEL_TERM_ACCESSION


def _set_factor_value_vals(prefix, factor_values, df, i):
    for fv in sorted(factor_values, key=lambda x: id(x.category.factor_type.name)):
        factor_name = fv.category.factor_type.name
        obj_fv_key = prefix + '_fv[' + factor_name + ']'
        df.loc[i, obj_fv_key] = fv.value
        if isinstance(fv.value, int) or isinstance(fv.value, float):
            df.loc[i, obj_fv_key + KEY_POSTFIX_UNIT] = fv.unit.name
            df.loc[i, obj_fv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE] = fv.unit.term_source
            df.loc[i, obj_fv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION] = fv.unit.term_accession
        elif isinstance(fv.value, OntologyAnnotation):
            df.loc[i, obj_fv_key] = fv.value.name
            df.loc[i, obj_fv_key + KEY_POSTFIX_TERMSOURCE] = fv.value.term_source
            df.loc[i, obj_fv_key + KEY_POSTFIX_TERMACCESSION] = fv.value.term_accession

KEY_POSTFIX_DATE = '_date'
LABEL_DATE = 'Date'
KEY_POSTFIX_PERFORMER = '_performer'
LABEL_PERFORMER = 'Performer'


def _parameter_value_label(parameter_name): return 'Parameter Value[' + parameter_name + ']'


def _set_protocol_cols(protrefcount, prottypes, process, cols, col_map):
    obj_process_key = 'protocol[' + str(protrefcount) + ']'
    cols.append(obj_process_key)
    col_map[obj_process_key] = LABEL_PROTOCOL_REF
    if process.date is not None:
        cols.append(obj_process_key + KEY_POSTFIX_DATE)
        col_map[obj_process_key + KEY_POSTFIX_DATE] = LABEL_DATE
    if process.performer is not None:
        cols.append(obj_process_key + KEY_POSTFIX_PERFORMER)
        col_map[obj_process_key + KEY_POSTFIX_PERFORMER] = LABEL_PERFORMER
    for pv in reversed(sorted(process.parameter_values, key=lambda x: x.category.parameter_name.name)):
        obj_process_pv_key = '_pv[' + pv.category.parameter_name.name + ']'
        if isinstance(pv.value, int) or isinstance(pv.value, float):
            cols.extend((obj_process_key + obj_process_pv_key,
                         obj_process_key + obj_process_pv_key + KEY_POSTFIX_UNIT,
                         obj_process_key + obj_process_pv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE,
                         obj_process_key + obj_process_pv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION))
            col_map[obj_process_key + obj_process_pv_key] = _parameter_value_label(pv.category.parameter_name.name)
            col_map[obj_process_key + obj_process_pv_key + KEY_POSTFIX_UNIT] = LABEL_UNIT
            col_map[obj_process_key + obj_process_pv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE] = LABEL_TERM_SOURCE
            col_map[obj_process_key + obj_process_pv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION] = LABEL_TERM_ACCESSION
        elif isinstance(pv.value, OntologyAnnotation):
            cols.extend((obj_process_key + obj_process_pv_key,
                         obj_process_key + obj_process_pv_key + KEY_POSTFIX_TERMSOURCE,
                         obj_process_key + obj_process_pv_key + KEY_POSTFIX_TERMACCESSION))
            col_map[obj_process_key + obj_process_pv_key] = _parameter_value_label(pv.category.parameter_name.name)
            col_map[obj_process_key + obj_process_pv_key + KEY_POSTFIX_TERMSOURCE] = LABEL_TERM_SOURCE
            col_map[obj_process_key + obj_process_pv_key + KEY_POSTFIX_TERMACCESSION] = LABEL_TERM_ACCESSION
        else:
            cols.append(obj_process_key + obj_process_pv_key)
            col_map[obj_process_key + obj_process_pv_key] = _parameter_value_label(pv.category.parameter_name.name)
    for prop in reversed(sorted(process.additional_properties.keys())):
        cols.append(obj_process_key + '_prop[' + prop + ']')
        col_map[obj_process_key + '_prop[' + prop + ']'] = prop
    for output in [x for x in process.outputs if isinstance(x, DataFile)]:
        cols.append('data[' + output.label + ']')
        col_map['data[' + output.label + ']'] = output.label
        for comment in output.comments:
            cols.append('data[' + output.label + ']_comment[' + comment.name + ']')
            col_map['data[' + output.label + ']_comment[' + comment.name + ']'] = 'Comment[' + comment.name + ']'
    if process.executes_protocol.protocol_type.name not in prottypes.values():
        prottypes[protrefcount] = process.executes_protocol.protocol_type.name
        protrefcount += 1


def write_assay_table_files(inv_obj, output_dir):
    """
        Writes out assay table files according to pattern defined by

        Sample Name,
        Protocol Ref: 'sample collection', [ ParameterValue[], ... ],
        Material Name, [ Characteristics[], ... ]
        [ FactorValue[], ... ]


    """
    if isinstance(inv_obj, Investigation):
        for study_obj in inv_obj.studies:
            for assay_obj in study_obj.assays:
                if assay_obj.graph is None: break
                cols = list()
                mcount = 0
                protrefcount = 0
                protnames = dict()
                col_map = dict()
                for node in _longest_path_and_attrs(assay_obj.graph):
                    if isinstance(node, Sample):
                        cols.append('sample')
                        col_map['sample'] = 'Sample Name'
                    elif isinstance(node, Material):
                        if node.type == 'Labeled Extract Name':
                            cols.append('lextract')
                            cols.append('lextract_label')
                            cols.append('lextract_label_termsource')
                            cols.append('lextract_label_termaccession')
                            col_map['lextract'] = 'Labeled Extract Name'
                            col_map['lextract_label'] = 'Label'
                            col_map['lextract_label_termsource'] = 'Term Source REF'
                            col_map['lextract_label_termaccession'] = 'Term Accession Number'
                        elif node.type == 'Extract Name':
                            cols.append('extract')
                            col_map['extract'] = 'Extract Name'
                            _set_charac_cols('extract', node.characteristics, cols, col_map)
                        else:
                            cols.append('material[' + str(mcount) + ']')
                            col_map['material[' + str(mcount) + ']'] = 'Material Name'
                            _set_charac_cols('material', node.characteristics, cols, col_map)
                            mcount += 1
                    elif isinstance(node, Process):
                        cols.append('protocol[' + str(protrefcount) + ']')
                        col_map['protocol[' + str(protrefcount) + ']'] = 'Protocol REF'
                        if node.date is not None:
                            cols.append('protocol[' + str(protrefcount) + ']_date')
                            col_map['protocol[' + str(protrefcount) + ']_date'] = 'Date'
                        if node.performer is not None:
                            cols.append('protocol[' + str(protrefcount) + ']_performer')
                            col_map['protocol[' + str(protrefcount) + ']_performer'] = 'Performer'
                        for pv in reversed(sorted(node.parameter_values, key=lambda x: x.category.parameter_name.name)):
                            if isinstance(pv.value, int) or isinstance(pv.value, float):
                                cols.extend(('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termsource',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termaccession'))
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = 'Parameter Value[' + pv.category.parameter_name.name + ']'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit'] = 'Unit'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termsource'] = 'Term Source REF'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termaccession'] = 'Term Accession Number'
                            elif isinstance(pv.value, OntologyAnnotation):
                                cols.extend(('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termsource',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termaccession',))
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = 'Parameter Value[' + pv.category.parameter_name.name + ']'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termsource'] = 'Term Source REF'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termaccession'] = 'Term Accession Number'
                            else:
                                cols.append('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']',)
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = 'Parameter Value[' + pv.category.parameter_name.name + ']'
                        for prop in reversed(sorted(node.additional_properties.keys())):
                            cols.append('protocol[' + str(protrefcount) + ']_prop[' + prop + ']')
                            col_map['protocol[' + str(protrefcount) + ']_prop[' + prop + ']'] = prop
                        for output in [x for x in node.outputs if isinstance(x, DataFile)]:
                            cols.append('data[' + output.label + ']')
                            col_map['data[' + output.label + ']'] = output.label
                            for comment in output.comments:
                                cols.append('data[' + output.label + ']_comment[' + comment.name + ']')
                                col_map['data[' + output.label + ']_comment[' + comment.name + ']'] = 'Comment[' + comment.name + ']'
                        if node.executes_protocol.name not in protnames.keys():
                            protnames[node.executes_protocol.name] = protrefcount
                            protrefcount += 1
                        # protrefcount = _set_protocol_cols(protrefcount, prottypes, node, cols, col_map)
                    elif isinstance(node, DataFile):
                        pass  # we process DataFile above inside Process
                import pandas as pd
                df = pd.DataFrame(columns=cols)
                i = 0
                start_nodes, end_nodes = _get_start_end_nodes(assay_obj.graph)
                for path in _all_end_to_end_paths(assay_obj.graph, start_nodes, end_nodes):
                    mcount = 0
                    compound_key = str()
                    for node in path:
                        if isinstance(node, Sample):
                            df.loc[i, 'sample'] = node.name
                            compound_key += node.name + '/'
                        elif isinstance(node, Material):
                            if node.type == 'Labeled Extract Name':
                                df.loc[i, 'lextract'] = node.name
                                compound_key += node.name + '/'
                                df.loc[i, 'lextract_label'] = node.characteristics[0].value.name
                                df.loc[i, 'lextract_label_termsource'] = node.characteristics[0].value.term_source
                                df.loc[i, 'lextract_label_termaccession'] = node.characteristics[0].value.term_accession
                            elif node.type == 'Extract Name':
                                df.loc[i, 'extract'] = node.name
                                compound_key += node.name + '/'
                                _set_charac_vals('extract', node.characteristics, df, i)
                            else:
                                df.loc[i, 'material[' + str(mcount) + ']'] = node.name
                                compound_key += node.name + '/'
                                _set_charac_vals('material', node.characteristics, df, i)
                                mcount += 1
                        elif isinstance(node, Process):
                            def find(n):
                                v = 0
                                for k, v in protnames.items():
                                    if k == n.executes_protocol.name:
                                        return v
                                return v
                            protrefcount = find(node)
                            df.loc[i, 'protocol[' + str(protrefcount) + ']'] = node.executes_protocol.name
                            compound_key += str(protrefcount) + '/' + node.name + '/'
                            if node.date is not None:
                                df.loc[i, 'protocol[' + str(protrefcount) + ']_date'] = node.date
                            if node.performer is not None:
                                df.loc[i, 'protocol[' + str(protrefcount) + ']_performer'] = node.performer
                            for pv in reversed(sorted(node.parameter_values, key=lambda x: x.category.parameter_name.name)):
                                if isinstance(pv.value, int) or isinstance(pv.value, float):
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = pv.value
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit'] = pv.unit.name
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termsource'] = pv.unit.term_source
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termaccession'] = pv.unit.term_accession
                                elif isinstance(pv.value, OntologyAnnotation):
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = pv.value.name
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termsource'] = pv.value.term_source
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termaccession'] = pv.value.term_accession
                                else:
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = pv.value
                            for prop in reversed(sorted(node.additional_properties.keys())):
                                df.loc[i, 'protocol[' + str(protrefcount) + ']_prop[' + prop + ']'] = node.additional_properties[prop]
                                compound_key += str(protrefcount) + '/' + prop + '/' + node.additional_properties[prop]
                            for output in [x for x in node.outputs if isinstance(x, DataFile)]:
                                df.loc[i, 'data[' + output.label + ']'] = output.filename
                                for comment in output.comments:
                                    df.loc[i, 'data[' + output.label + ']_comment[' + comment.name + ']'] = comment.value
                    df.loc[i, 'compound_key'] = compound_key
                    i += 1

                # reduce rows of data on separate lines

                # can we group by matching all columns minus the data columns?
                import re
                data_regex = re.compile('data\[(.*?)\]')
                # cols_no_data = [col for col in cols if not data_regex.match(col)]  # column list without data cols

                # calculate groupings
                def rolling_group(val):
                    global prev
                    if val != prev:
                        rolling_group.group += 1  # val != prev is signal to switch group; rows sorted by cols_no_data
                    prev = val
                    return rolling_group.group
                rolling_group.group = 0  # static variable
                groups = df.groupby(df['compound_key'].apply(rolling_group), as_index=True)  # groups by column 1 only

                # merge items in column groups
                def reduce(group, column):
                    col = group[column]
                    s = [str(each) for each in col if pd.notnull(each)]
                    if len(s) > 0:
                        return s[0]
                    else:
                        return ''
                df = groups.apply(lambda g: pd.Series([reduce(g, col) for col in g.columns], index=g.columns))

                #  cleanup column headers before writing out df
                # WARNING: don't just dump out col_map.values() as we need to put columns back in order
                df = df.sort_values(by=df.columns[0], ascending=True)  # arbitrary sort on column 0 (Sample name)
                del df['compound_key']  # release compound_key as we don't write it out
                for i, col in enumerate(df.columns):
                    cols[i] = col_map[col]
                    if col_map[col] == 'Characteristics[Material Type]':
                        cols[i] = 'Material Type'
                    elif col_map[col] == 'Parameter Value[Array Design REF]':
                        cols[i] = 'Array Design REF'
                    if data_regex.match(col) is not None:
                        if data_regex.findall(col)[0] == 'Raw Data File':
                            if assay_obj.technology_type.name == 'DNA microarray':
                                cols[i] = 'Array Data File'
                df.columns = cols  # reset column headers
                # drop completely empty columns
                df = df.replace('', np.nan)
                df = df.dropna(axis=1, how='all')
                assay_obj.df = df
                df.to_csv(path_or_buf=open(os.path.join(output_dir, assay_obj.filename), 'w'), index=False, sep='\t', encoding='utf-8',)


def write_study_table_files(inv_obj, output_dir):
    """
        Writes out study table files according to pattern defined by

        Source Name, [ Characteristics[], ... ],
        Protocol Ref*: 'sample collection', [ ParameterValue[], ... ],
        Sample Name, [ Characteristics[], ... ]
        [ FactorValue[], ... ]

        which should be equivalent to studySample.xml in default config

    """

    if not isinstance(inv_obj, Investigation):
        raise NotImplementedError
    for study_obj in inv_obj.studies:
        study_obj.build_graph()
        if study_obj.graph is None: break
        cols = list()
        protrefcount = 0
        protnames = dict()
        col_map = dict()

        for node in _longest_path_and_attrs(study_obj.graph):
            if isinstance(node, Source):
                cols.append('source')
                col_map['source'] = 'Source Name'
                _set_charac_cols('source', node.characteristics, cols, col_map)
            elif isinstance(node, Process):

                cols.append('protocol[' + str(protrefcount) + ']')
                col_map['protocol[' + str(protrefcount) + ']'] = 'Protocol REF'
                if node.date is not None:
                    cols.append('protocol[' + str(protrefcount) + ']_date')
                    col_map['protocol[' + str(protrefcount) + ']_date'] = 'Date'
                if node.performer is not None:
                    cols.append('protocol[' + str(protrefcount) + ']_performer')
                    col_map['protocol[' + str(protrefcount) + ']_performer'] = 'Performer'
                for pv in reversed(sorted(node.parameter_values, key=lambda x: x.category.parameter_name.name)):
                    if isinstance(pv.value, int) or isinstance(pv.value, float):
                        cols.extend(('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']',
                                     'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit',
                                     'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termsource',
                                     'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termaccession'))
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = 'Parameter Value[' + pv.category.parameter_name.name + ']'
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit'] = 'Unit'
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termsource'] = 'Term Source REF'
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termaccession'] = 'Term Accession Number'
                    elif isinstance(pv.value, OntologyAnnotation):
                        cols.extend(('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']',
                                     'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termsource',
                                     'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termaccession',))
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = 'Parameter Value[' + pv.category.parameter_name.name + ']'
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termsource'] = 'Term Source REF'
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termaccession'] = 'Term Accession Number'
                    else:
                        cols.append('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']')
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = 'Parameter Value[' + pv.category.parameter_name.name + ']'
                if node.executes_protocol.name not in protnames.keys():
                    protnames[node.executes_protocol.name] = protrefcount
                    protrefcount += 1
            elif isinstance(node, Sample):
                cols.append('sample')
                col_map['sample'] = 'Sample Name'
                _set_charac_cols('sample', node.characteristics, cols, col_map)
                _set_factor_value_cols('sample', node.factor_values, cols, col_map)
        import pandas as pd
        df = pd.DataFrame(columns=cols)
        i = 0

        start_nodes, end_nodes = _get_start_end_nodes(study_obj.graph)
        for path in _all_end_to_end_paths(study_obj.graph, start_nodes, end_nodes):
            for node in path:
                if isinstance(node, Source):
                    df.loc[i, 'source'] = node.name
                    _set_charac_vals('source', node.characteristics, df, i)
                elif isinstance(node, Process):
                    def find(n):
                        v = 0
                        for k, v in protnames.items():
                            if k == n.executes_protocol.name:
                                return v
                        return v
                    protrefcount = find(node)
                    df.loc[i, 'protocol[' + str(protrefcount) + ']'] = node.executes_protocol.name
                    if node.date is not None:
                        df.loc[i, 'protocol[' + str(protrefcount) + ']_date'] = node.date
                    if node.performer is not None:
                        df.loc[i, 'protocol[' + str(protrefcount) + ']_performer'] = node.performer
                    for pv in reversed(sorted(node.parameter_values, key=lambda x: x.category.parameter_name.name)):
                        if isinstance(pv.value, int) or isinstance(pv.value, float):
                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = pv.value
                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit'] = pv.unit.name
                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termsource'] = pv.unit.term_source
                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_unit_termaccession'] = pv.unit.term_accession
                        elif isinstance(pv.value, OntologyAnnotation):
                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']'] = pv.value.name
                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termsource'] = pv.value.term_source
                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.name + ']_termaccession'] = pv.value.term_accession
                        else:
                            df.loc[i, i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.characteristic_type.name + ']'] = pv.value
                elif isinstance(node, Sample):
                    df.loc[i, 'sample'] = node.name
                    _set_charac_vals('sample', node.characteristics, df, i)
                    _set_factor_value_vals('sample', node.factor_values, df, i)
            i += 1
        # WARNING: don't just dump out col_map.values() as we need to put columns back in order
        df = df.drop_duplicates()
        df = df.sort_values(by=df.columns[0], ascending=True)  # arbitrary sort on column 0 (Sample name)
        for i, col in enumerate(df.columns):
            if col_map[col] == 'Characteristics[Material Type]':
                cols[i] = 'Material Type'
            else:
                cols[i] = col_map[col]
        df.columns = cols  # reset column headers
        import numpy as np
        df = df.replace('', np.nan)
        df = df.dropna(axis=1, how='all')
        df = df.sort_values(by=df.columns[0], ascending=True)  # arbitrary sort on column 0
        df.to_csv(path_or_buf=open(os.path.join(output_dir, study_obj.filename), 'w'), index=False, sep='\t', encoding='utf-8',)


def assert_tab_content_equal(fp_x, fp_y):
    """
    Test for equality of tab files, only down to level of content - should not be taken as canonical equality, but
    rather that all the expected content matches to both input files, but not the order in which they appear.

    For more precise equality, you will need to apply a configuration
        - use assert_tab_equal_by_config(fp_x, fp_y, config)
    :param fp_x: File descriptor of a ISAtab file
    :param fp_y: File descriptor of another  ISAtab file
    :return: True or False plus any AssertionErrors
    """

    def _assert_df_equal(x, y):  # need to sort values to loosen up how equality is calculated
        try:
            assert_frame_equal(x.sort_values(by=x.columns[0]), y.sort_values(by=y.columns[0]))
            return True
        except AssertionError as e:
            print(e)
            return False

    from os.path import basename
    if basename(fp_x.name).startswith('i_'):
        df_dict_x = _read_investigation_file(fp_x)
        df_dict_y = _read_investigation_file(fp_y)
        eq = True
        for k in df_dict_x.keys():
            dfx = df_dict_x[k]
            dfy = df_dict_y[k]
            if not isinstance(dfx, list):
                if not _assert_df_equal(dfx, dfy):
                    eq = False
                    break
            else:
                try:
                    for x, y in zip(sorted(dfx), sorted(dfy)):
                        if not _assert_df_equal(x, y):
                            eq = False
                            break
                except ValueError as e:
                    print(e)
        return eq
    else:

        def diff(a, b):
            b = set(b)
            return [aa for aa in a if aa not in b]

        import numpy as np
        df_x = pd.read_csv(fp_x, sep='\t', encoding='utf-8')
        df_y = pd.read_csv(fp_y, sep='\t', encoding='utf-8')
        try:
            # drop empty columns
            df_x = df_x.replace('', np.nan)
            df_x = df_x.dropna(axis=1, how='all')
            df_x = df_x.replace(np.nan, '')
            df_y = df_y.replace('', np.nan)
            df_y = df_y.dropna(axis=1, how='all')
            df_y = df_y.replace(np.nan, '')

            is_cols_equal = set([x.split('.', 1)[0] for x in df_x.columns]) == set([x.split('.', 1)[0] for x in df_y.columns])
            if not is_cols_equal:
                print('x: ' + str(df_x.columns))
                print('y: ' + str(df_y.columns))
                print(diff(df_x.columns, df_y.columns))
                raise AssertionError("Columns in x do not match those in y")

            # reindex to add contexts for duplicate named columns (i.e. Term Accession Number, Unit, etc.)
            import re
            char_regex = re.compile('Characteristics\[(.*?)\]')
            pv_regex = re.compile('Parameter Value\[(.*?)\]')
            fv_regex = re.compile('Factor Value\[(.*?)\]')
            newcolsx = list()
            for col in df_x.columns:
                newcolsx.append(col)
            for i, col in enumerate(df_x.columns):
                if char_regex.match(col) or pv_regex.match(col) or fv_regex.match(col):
                    try:
                        if 'Unit' in df_x.columns[i+1]:
                            newcolsx[i+1] = col + '/Unit'
                            if 'Term Source REF' in df_x.columns[i+2]:
                                newcolsx[i+2] = col + '/Unit/Term Source REF'
                            if 'Term Accession Number' in df_x.columns[i+3]:
                                newcolsx[i+3] = col + '/Unit/Term Accession Number'
                        elif 'Term Source REF' in df_x.columns[i+1]:
                            newcolsx[i+1] = col + '/Term Source REF'
                            if 'Term Accession Number' in df_x.columns[i+2]:
                                newcolsx[i+2] = col + '/Term Accession Number'
                    except IndexError:
                        pass
            df_x.columns = newcolsx
            newcolsy = list()
            for col in df_y.columns:
                newcolsy.append(col)
            for i, col in enumerate(df_y.columns):
                if char_regex.match(col) or pv_regex.match(col) or fv_regex.match(col):
                    try:
                        if 'Unit' in df_y.columns[i+1]:
                            newcolsy[i+1] = col + '/Unit'
                            if 'Term Source REF' in df_y.columns[i+2]:
                                newcolsy[i+2] = col + '/Unit/Term Source REF'
                            if 'Term Accession Number' in df_y.columns[i+3]:
                                newcolsy[i+3] = col + '/Unit/Term Accession Number'
                        elif 'Term Source REF' in df_y.columns[i+1]:
                            newcolsy[i+1] = col + '/Term Source REF'
                            if 'Term Accession Number' in df_y.columns[i+2]:
                                newcolsy[i+2] = col + '/Term Accession Number'
                    except IndexError:
                        pass
            df_y.columns = newcolsy
            for colx in df_x.columns:
                for eachx, eachy in zip(df_x.sort_values(by=colx)[colx], df_y.sort_values(by=colx)[colx]):
                    if eachx != eachy:
                        print(df_x[colx])
                        print(df_y[colx])
                        raise AssertionError("Value: " + str(eachx) + ", does not match: " + str(eachy))
            # print("Well, you got here so the files must be same-ish... well done, you!")
            return True
        except AssertionError as e:
            print(str(e))
            return False


""" Everything below this line is work in progress. You're best off ignoring it! """


def load(isatab_dir):

    def _createOntologySourceReferences(ontology_refs):
        ontologies = []
        for ontology_ref in ontology_refs:
            ontology = OntologySourceReference(
                description=ontology_ref['Term Source Description'],
                file=ontology_ref['Term Source File'],
                name=ontology_ref['Term Source Name'],
                version=ontology_ref['Term Source Version'],
            )
            ontologies.append(ontology)
        return ontologies

    def _createPublications(isapubs, inv_or_study):
        publications = []
        for pub in isapubs:
            publication = Publication(
                pubmed_id=pub[inv_or_study+' PubMed ID'],
                doi=pub[inv_or_study+' Publication DOI'],
                author_list=pub[inv_or_study+' Publication Author List'],
                title=pub[inv_or_study+' Publication Title'],
                status=_createOntologyAnnotationForInvOrStudy(pub, inv_or_study, ' Publication Status')
            )
            publications.append(publication)
        return publications

    def _createOntologyAnnotationForInvOrStudy(object_, inv_or_study, type_):
        onto_ann = OntologyAnnotation(
                name=object_[inv_or_study+type_],
                term_source=object_[inv_or_study+type_+" Term Source REF"],
                term_accession=object_[inv_or_study+type_+" Term Accession Number"],
        )
        return onto_ann

    def _createContacts(contacts, inv_or_study):
        people_json = []
        for contact in contacts:
            person_json = Person(
                last_name=contact[inv_or_study+" Person Last Name"],
                first_name=contact[inv_or_study+" Person First Name"],
                mid_initials=contact[inv_or_study+" Person Mid Initials"],
                email=contact[inv_or_study+" Person Email"],
                phone=contact[inv_or_study+" Person Phone"],
                fax=contact[inv_or_study+" Person Fax"],
                address=contact[inv_or_study+" Person Address"],
                affiliation=contact[inv_or_study+" Person Affiliation"],
                # FIXME Parsing roles?
                roles=[]
            )
            people_json.append(person_json)
        return people_json


    def _createCharacteristicList(node_name, node):
        obj_list = []
        for header in node.metadata:
            if header.startswith("Characteristics"):
                characteristic = header.replace("]", "").split("[")[-1]
                characteristic_obj = Characteristic(
                    value=OntologyAnnotation(name=characteristic)
                )
                obj_item = dict([
                    ("characteristic", characteristic_obj)
                ])
                obj_list.append(obj_item)
        return obj_list

    def _createOntologyAnnotationListForInvOrStudy(array, inv_or_study, type_):
        onto_annotations = []
        for object_ in array:
            onto_ann = OntologyAnnotation(
                name=object_[inv_or_study+type_],
                term_source=object_[inv_or_study+type_+" Term Source REF"],
                term_accession=object_[inv_or_study+type_+" Term Accession Number"],
            )
            onto_annotations.append(onto_ann)
        return onto_annotations

    def _createProtocols(protocols):
        protocols_list = []
        for prot in protocols:
            protocol = Protocol(
                name=prot['Study Protocol Name'],
                protocol_type=_createOntologyAnnotationForInvOrStudy(prot, "Study", " Protocol Type"),
                description=prot['Study Protocol Description'],
                uri=prot['Study Protocol URI'],
                version=prot['Study Protocol Version'],
                parameters=_createProtocolParameterList(prot),
            )
            protocols_list.append(protocol)
        return protocols_list

    def _createProtocolParameterList(protocol):
        parameters_list = []
        parameters_annotations = _createOntologyAnnotationsFromStringList(protocol, "Study",
                                                                          " Protocol Parameters Name")
        for parameter_annotation in parameters_annotations:
            parameter = ProtocolParameter(
                # parameterName=parameter_annotation
            )
            parameters_list.append(parameter)
        return parameters_list

    def _createOntologyAnnotationsFromStringList(object_, inv_or_study, type_):
        #FIXME If empty string, it returns 1?
        name_array = object_[inv_or_study+type_].split(";")
        term_source_array = object_[inv_or_study+type_+" Term Source REF"].split(";")
        term_accession_array = object_[inv_or_study+type_+" Term Accession Number"].split(";")
        onto_annotations = []
        for i in range(0, len(name_array)):
             onto_ann = OntologyAnnotation(
                 name=name_array[i],
                 term_source=term_source_array[i],
                 term_accession=term_accession_array[i],
             )
             onto_annotations.append(onto_ann)
        return onto_annotations

    def _createDataFiles(nodes):
        obj_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype.endswith("Data File"):
                obj_item = DataFile(
                    filename=nodes[node_index].name,
                    label=nodes[node_index].ntype
                )
                obj_dict.update({node_index: obj_item})
        return obj_dict

    def _createProcessSequence(process_nodes, source_dict, sample_dict, data_dict):
        obj_list = []
        for process_node_name in process_nodes:
            try:
                measurement_type = process_nodes[process_node_name].study_assay.metadata["Study Assay Measurement Type"]
            except:
                measurement_type = ""

            try:
                platform = process_nodes[process_node_name].study_assay.metadata["Study Assay Technology Platform"]
            except:
                platform = ""

            try:
                technology = process_nodes[process_node_name].study_assay.metadata["Study Assay Technology Type"]
            except:
                technology = ""

            obj_item = Process(
                executes_protocol=_createExecuteStudyProtocol(process_node_name, process_nodes[process_node_name]),
                inputs=_createInputList(process_nodes[process_node_name].inputs, source_dict, sample_dict),
                outputs=_createOutputList(process_nodes[process_node_name].outputs, sample_dict)
            )
            obj_list.append(obj_item)
        return obj_list

    def _createExecuteStudyProtocol(process_node_name, process_node):
        json_item = dict([
                   # ("name", dict([("value", process_node_name)])),
                   # ("description", dict([("value", process_node_name)])),
                   # ("version", dict([("value", process_node_name)])),
                   # ("uri", dict([("value", process_node_name)])),
                   # ("parameters", self.createProcessParameterList(process_node_name, process_node))
                ])
        return json_item

    def _createInputList(inputs, source_dict, sample_dict):
        obj_list = list()
        for argument in inputs:
            try:
                obj_item = source_dict[argument]
                obj_list.append(obj_item)
            except KeyError:
                pass
            try:
                obj_item = sample_dict[argument]
                obj_list.append(obj_item)
            except KeyError:
                pass
        return obj_list

    def _createOutputList(arguments, sample_dict):
        obj_list = []
        for argument in arguments:
            try:
                obj_item = sample_dict[argument]
                obj_list.append(obj_item)
            except KeyError:
                pass
        return obj_list

    def _createStudyAssaysList(assays):
        json_list = list()
        for assay in assays:
            source_dict = _createSourceDictionary(assay.nodes)
            sample_dict = _createSampleDictionary(assay.nodes)
            data_dict = _createDataFiles(assay.nodes)
            json_item = Assay(
                filename=assay.metadata['Study Assay File Name'],
                measurement_type=OntologyAnnotation(
                    name=assay.metadata['Study Assay Measurement Type'],
                    term_source=assay.metadata['Study Assay Measurement Type Term Source REF'],
                    term_accession=assay.metadata['Study Assay Measurement Type Term Accession Number']),
                technology_type=OntologyAnnotation(
                    name=assay.metadata['Study Assay Technology Type'],
                    term_source=assay.metadata['Study Assay Technology Type Term Source REF'],
                    term_accession=assay.metadata['Study Assay Technology Type Term Accession Number']),
                technology_platform=assay.metadata['Study Assay Technology Platform'],
                process_sequence=_createProcessSequence(assay.process_nodes, source_dict, sample_dict, data_dict),
            )
            json_list.append(json_item)
        return json_list

    def _createValueList(column_name, node_name, node):
        obj_list = list()
        for header in node.metadata:
            if header.startswith(column_name):
                value_header = header.replace("]", "").split("[")[-1]
                value_attributes = node.metadata[header][0]
                value = value_attributes[0]  # In tab2json uses convert_num to recast string to int or float
                try:
                    if column_name == 'Characteristics':
                        value_obj = Characteristic(
                            category=value_header,
                            value=value,
                            unit=OntologyAnnotation(
                                name=value_attributes.Unit,
                                term_accession=value_attributes.Term_Accession_Number,
                                term_source=value_attributes.Term_Source_REF,
                            )
                        )
                    elif column_name == 'Factor Value':
                        value_obj = FactorValue(
                            # factorName=value_header,
                            value=value,
                            unit=OntologyAnnotation(
                                name=value_attributes.Unit,
                                term_accession=value_attributes.Term_Accession_Number,
                                term_source=value_attributes.Term_Source_REF,
                            )
                        )
                    obj_list.append(value_obj)
                    continue
                except AttributeError:
                    try:
                        if column_name == 'Characteristics':
                            value_obj = Characteristic(
                                category=value_header,
                                value=OntologyAnnotation(
                                    name=value,
                                    term_accession=value_attributes.Term_Accession_Number,
                                    term_source=value_attributes.Term_Source_REF,
                                )
                            )
                            obj_list.append(value_obj)
                        elif column_name == 'Factor Value':
                            value_obj = FactorValue(
                                # factorName=value_header,
                                value=OntologyAnnotation(
                                    name=value,
                                    term_accession=value_attributes.Term_Accession_Number,
                                    term_source=value_attributes.Term_Source_REF,
                                )
                            )
                        continue
                    except AttributeError:
                        if column_name == 'Characteristics':
                            value_obj = Characteristic(
                                category=value_header,
                                value=OntologyAnnotation(
                                    name=value
                                )
                            )
                        elif column_name == 'Factor Value':
                            value_obj = FactorValue(
                                # factorName=value_header,
                                value=OntologyAnnotation(
                                    name=value
                                )
                            )
                        obj_list.append(value_obj)
        return obj_list

    def _createSourceDictionary(nodes):
        obj_dict = dict([])
        for node_name in nodes:
            if nodes[node_name].ntype == "Source Name":
                reformatted_node_name = node_name[7:]  # Strip out the source- bit
                source_item = Source(
                    name=reformatted_node_name,
                    characteristics=_createValueList("Characteristics", node_name, nodes[node_name]),
                )
                obj_dict.update({node_name: source_item})
        return obj_dict

    def _createSampleDictionary(nodes):
        obj_dict = dict([])
        for node_index in nodes:
            if nodes[node_index].ntype == "Sample Name":
                reformatted_node_name = node_index[7:]  # Strip out the sample- bit
                try:
                    obj_item = Sample(
                        name=reformatted_node_name,
                        factor_values=_createValueList("Factor Value", node_index, nodes[node_index]),
                        characteristics=_createValueList("Characteristics", node_index, nodes[node_index]),
                        derives_from=nodes[node_index].metadata["Source Name"][0],
                    )
                    obj_dict.update({node_index: obj_item})
                except KeyError:
                    pass
        return obj_dict

    def _createStudies(studies):
        study_array = []
        for study in studies:
            sources = _createSourceDictionary(study.nodes)
            samples = _createSampleDictionary(study.nodes)
            data_dict = _createDataFiles(study.nodes)
            study_obj = Study(
                identifier=study.metadata['Study Identifier'],
                title=study.metadata['Study Title'],
                description=study.metadata['Study Description'],
                submission_date=study.metadata['Study Submission Date'],
                public_release_date=study.metadata['Study Public Release Date'],
                factors=None,
                filename=study.metadata['Study File Name'],
                design_descriptors=_createOntologyAnnotationListForInvOrStudy(study.design_descriptors, "Study",
                                                                              " Design Type"),
                publications=_createPublications(study.publications, "Study"),
                contacts=_createContacts(study.contacts, "Study"),
                protocols=_createProtocols(study.protocols),
                sources=list(sources.values()),
                samples=list(samples.values()),
                process_sequence=_createProcessSequence(study.process_nodes, sources, samples, data_dict),
                # assays=_createStudyAssaysList(study.assays),
            )
            study_array.append(study_obj)
        return study_array

    investigation = None
    isa_tab = isatab_parser.parse(isatab_dir)
    if isa_tab is None:
        raise IOError("There was problem parsing the ISA Tab")
    else:
        if isa_tab.metadata != {}:
            #print("isa_tab.metadata->",isa_tab.metadata)
            investigation = Investigation(
                identifier=isa_tab.metadata['Investigation Identifier'],
                title=isa_tab.metadata['Investigation Title'],
                description=isa_tab.metadata['Investigation Description'],
                submission_date=isa_tab.metadata['Investigation Submission Date'],
                public_release_date=isa_tab.metadata['Investigation Public Release Date'],
                ontology_source_references=_createOntologySourceReferences(isa_tab.ontology_refs),
                publications=_createPublications(isa_tab.publications, "Investigation"),
                contacts=_createContacts(isa_tab.contacts, "Investigation"),
                studies=_createStudies(isa_tab.studies),
            )
    return investigation


def read_study_file(fp):
    import re

    def _read_study_record_line(column_names, row_):
        characteristics_regex = re.compile('Characteristics\[(.*?)\]')
        factor_value_regex = re.compile('Factor Value\[(.*?)\]')
        if len(column_names) != len(row_):
            raise IOError
        source_ = Source()
        sample_ = Sample()
        for index, value in enumerate(column_names):
            if value == 'Source Name':
                source_.name = row_[index]
            if value == 'Sample Name':
                sample_.name = row_[index]
            if value == 'Material Type':
                pass
            if value == 'Protocol REF':
                processing_event_ = Process(
                    executes_protocol=row_[index],
                )
                try:
                    peek_column = column_names[index+1]
                    if peek_column == 'Date':
                        processing_event_.date_ = row_[index+1]
                        peek_column = column_names[index+2]
                        if peek_column == 'Performer':
                            processing_event_.performer = row_[index+2]
                    if peek_column == 'Performer':
                        processing_event_.performer = row_[index+1]
                        if peek_column == 'Date':
                            processing_event_.date = row_[index+2]
                except IndexError:
                    pass
            if characteristics_regex.match(value):
                characteristic = Characteristic()
                characteristic.category = characteristics_regex.findall(value)[0]
                try:
                    peek_column = column_names[index+1]
                    if peek_column == 'Term Source REF':
                        characteristic.value = OntologyAnnotation(
                            name=row_[index],
                            term_source=row_[index+1],
                            term_accession=row_[index+2],
                        )
                    else:
                        characteristic.value = row_[index]
                except IndexError:
                    pass
                finally:
                    if sample_.name == '':
                        source_.characteristics.append(characteristic)
                    else:
                        sample_.characteristics.append(characteristic)
            if factor_value_regex.match(value):
                factor_value = FactorValue()
                factor_value.factor_name = factor_value_regex.findall(value)[0]
                try:
                    peek_column = column_names[index+1]
                    if peek_column == 'Term Source REF':
                        factor_value.value = OntologyAnnotation(
                            name=row_[index],
                            term_source=row_[index+1],
                            term_accession=row_[index+2],
                        )
                    elif peek_column == 'Unit':
                        factor_value.value = row_[index]
                        factor_value.unit = OntologyAnnotation(
                            name=row_[index+1],
                            term_source=row_[index+2],
                            term_accession=row_[index+3],
                        )
                except IndexError:
                    pass
                finally:
                    sample_.factor_values.append(factor_value)
        return source_, sample_, processing_event_

    import csv
    study_reader = csv.reader(fp, delimiter='\t')
    fieldnames = next(study_reader)
    experimental_graph = dict()
    for row in study_reader:
        source, sample, processing_event = _read_study_record_line(column_names=fieldnames, row_=row)
        try:
            experimental_graph[source].append(processing_event)
        except KeyError:
            experimental_graph[source] = list()
            experimental_graph[source].append(processing_event)
        try:
            experimental_graph[processing_event].append(sample)
        except KeyError:
            experimental_graph[processing_event] = list()
            experimental_graph[processing_event].append(sample)
    return experimental_graph
