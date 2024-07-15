from __future__ import absolute_import
from typing import TextIO

from os import path
from glob import glob
import logging

from pandas.errors import ParserError

from isatools.utils import utf8_text_file_open
from isatools.isatab.load import read_investigation_file
from isatools.isatab.defaults import _RX_COMMENT, default_config_dir, log
from isatools.isatab.validate.store import validator as message_handler
from isatools.isatab.validate.rules.core import (
    ISAInvestigationValidator, ISAStudyValidator, ISAAssayValidator, build_rules
)


def load_investigation(fp):
    """Used for rules 0005

    :param fp: A file-like buffer object pointing to an investigation file
    :return: Dictionary of DataFrames for each section
    """

    def check_labels(section, labels_expected, df):
        """Checks each section is syntactically structured correctly

        :param section: The section of interest
        :param labels_expected: The list of expected labels in the section
        :param df: The DataFrame slice of the investigation file we are
        checking
        :return: None
        """
        labels_found = set([x for x in df.columns if isinstance(x, str)])

        if not labels_expected.issubset(labels_found):
            missing_labels = labels_expected - labels_found
            spl = "In {} section, expected labels {} not found in {}".format(section, missing_labels, labels_found)
            msg = "Label not found"
            message_handler.add_error(message=msg, supplemental=spl, code=5)
        if len(labels_found - labels_expected) > 0:
            # check extra labels, i.e. make sure they're all comments
            extra_labels = labels_found - labels_expected
            for label in extra_labels:
                if _RX_COMMENT.match(label) is None:
                    msg = "Invalid label found in investigation file"
                    spl = "In {} section, label {} is not allowed".format(section, label)
                    message_handler.add_error(message=msg, supplemental=spl, code=5)
                elif len(_RX_COMMENT.findall(label)) == 0:
                    spl = "In {} section, label {} is missing a name".format(section, label)
                    msg = "Missing name in Comment[] label"
                    message_handler.add_error(message=msg, supplemental=spl, code=5)

    # Read in investigation file into DataFrames first
    df_dict = read_investigation_file(fp)
    log.debug("Loading ONTOLOGY SOURCE REFERENCE section")
    labels_expected = {'Term Source Name', 'Term Source File', 'Term Source Version', 'Term Source Description'}
    check_labels('ONTOLOGY SOURCE REFERENCE', labels_expected, df_dict['ontology_sources'])

    log.debug("Loading INVESTIGATION section")
    labels_expected = {'Investigation Identifier', 'Investigation Title',
                       'Investigation Description',
                       'Investigation Submission Date',
                       'Investigation Public Release Date'}
    check_labels('INVESTIGATION', labels_expected, df_dict['investigation'])

    log.debug("Loading INVESTIGATION PUBLICATIONS section")
    labels_expected = {
        'Investigation PubMed ID',
        'Investigation Publication DOI',
        'Investigation Publication Author List',
        'Investigation Publication Title',
        'Investigation Publication Status',
        'Investigation Publication Status Term Accession Number',
        'Investigation Publication Status Term Source REF'}
    check_labels('INVESTIGATION PUBLICATIONS', labels_expected, df_dict['i_publications'])

    log.debug("Loading INVESTIGATION CONTACTS section")
    labels_expected = {'Investigation Person Last Name',
                       'Investigation Person First Name',
                       'Investigation Person Mid Initials',
                       'Investigation Person Email',
                       'Investigation Person Phone',
                       'Investigation Person Fax',
                       'Investigation Person Address',
                       'Investigation Person Affiliation',
                       'Investigation Person Roles',
                       'Investigation Person Roles',
                       'Investigation Person Roles Term Accession Number',
                       'Investigation Person Roles Term Source REF'}
    check_labels('INVESTIGATION CONTACTS', labels_expected, df_dict['i_contacts'])
    for i in range(0, len(df_dict['studies'])):
        log.debug("Loading STUDY section")
        labels_expected = {'Study Identifier', 'Study Title',
                           'Study Description',
                           'Study Submission Date',
                           'Study Public Release Date',
                           'Study File Name'}
        check_labels('STUDY', labels_expected, df_dict['studies'][i])

        log.debug("Loading STUDY DESIGN DESCRIPTORS section")
        labels_expected = {'Study Design Type',
                           'Study Design Type Term Accession Number',
                           'Study Design Type Term Source REF'}
        check_labels('STUDY DESIGN DESCRIPTORS', labels_expected,
                     df_dict['s_design_descriptors'][i])

        log.debug("Loading STUDY PUBLICATIONS section")
        labels_expected = {'Study PubMed ID', 'Study Publication DOI',
                           'Study Publication Author List',
                           'Study Publication Title',
                           'Study Publication Status',
                           'Study Publication Status Term Accession Number',
                           'Study Publication Status Term Source REF'}
        check_labels('STUDY PUBLICATIONS', labels_expected,
                     df_dict['s_publications'][i])

        log.debug("Loading STUDY FACTORS section")
        labels_expected = {'Study Factor Name', 'Study Factor Type',
                           'Study Factor Type Term Accession Number',
                           'Study Factor Type Term Source REF'}
        check_labels('STUDY FACTORS', labels_expected, df_dict['s_factors'][i])

        log.debug("Loading STUDY ASSAYS section")
        labels_expected = {
            'Study Assay Measurement Type',
            'Study Assay Measurement Type Term Accession Number',
            'Study Assay Measurement Type Term Source REF',
            'Study Assay Technology Type',
            'Study Assay Technology Type Term Accession Number',
            'Study Assay Technology Type Term Source REF',
            'Study Assay Technology Platform',
            'Study Assay File Name'}
        check_labels('STUDY ASSAYS', labels_expected, df_dict['s_assays'][i])

        log.debug("Loading STUDY PROTOCOLS section")
        labels_expected = {
            'Study Protocol Name', 'Study Protocol Type',
            'Study Protocol Type Term Accession Number',
            'Study Protocol Type Term Source REF',
            'Study Protocol Description', 'Study Protocol URI',
            'Study Protocol Version',
            'Study Protocol Parameters Name',
            'Study Protocol Parameters Name Term Accession Number',
            'Study Protocol Parameters Name Term Source REF',
            'Study Protocol Components Name',
            'Study Protocol Components Type',
            'Study Protocol Components Type Term Accession Number',
            'Study Protocol Components Type Term Source REF'}
        check_labels('STUDY PROTOCOLS', labels_expected,
                     df_dict['s_protocols'][i])

        log.debug("Loading STUDY CONTACTS section")
        labels_expected = {
            'Study Person Last Name', 'Study Person First Name',
            'Study Person Mid Initials', 'Study Person Email',
            'Study Person Phone', 'Study Person Fax',
            'Study Person Address', 'Study Person Affiliation',
            'Study Person Roles', 'Study Person Roles',
            'Study Person Roles Term Accession Number',
            'Study Person Roles Term Source REF'}
        check_labels('STUDY CONTACTS', labels_expected,
                     df_dict['s_contacts'][i])

    return df_dict


def validate(fp: TextIO,
             config_dir: str = default_config_dir,
             origin: str or None = None,
             rules: dict = None,
             log_level=None) -> dict:
    """
    A function to validate an ISA investigation tab file
    :param fp: the investigation file handler
    :param config_dir: the XML configuration directory
    :param origin: value accepted = mzml2isa or None
    :param rules: optional rules to run (default: all rules)
    :param log_level: optional log level (default: INFO)
    :return: a dictionary of the validation results (errors, warnings and info)
    """
    if log_level is None:
        log.disabled = True
    else:
        log.setLevel(log_level)
    message_handler.reset_store()
    validated = False

    built_rules = build_rules(rules)
    try:
        i_df_dict = load_investigation(fp=fp)
        params = {
            "investigation_df_dict": i_df_dict,
            "dir_context": path.dirname(fp.name),
            "configs": config_dir,
        }
        investigation_validator = ISAInvestigationValidator(**params, **built_rules['investigation'])

        for i, study_df in enumerate(i_df_dict['studies']):
            study_filename = study_df.iloc[0]['Study File Name']
            study_validator = ISAStudyValidator(validator=investigation_validator, study_index=i,
                                                study_filename=study_filename, study_df=study_df,
                                                **built_rules['studies'])
            assay_tables = list()
            assay_df = study_validator.params['investigation_df_dict']['s_assays'][i]
            for x, assay_filename in enumerate(assay_df['Study Assay File Name'].tolist()):
                ISAAssayValidator(assay_tables=assay_tables, validator=study_validator, assay_index=x,
                                  assay_df=assay_df, assay_filename=assay_filename, **built_rules['assays'])
            if origin == "mzml2isa":
                validate_origin_mzml2isa(fp=fp)
        validated = True
    except (Exception, ParserError, SystemError, ValueError) as e:
        spl = "The validator could not identify what the error is: {}".format(str(e))
        message_handler.add_error(message="Unknown/System Error", supplemental=spl, code=0)
    return {
        "errors": message_handler.errors,
        "warnings": message_handler.warnings,
        "info": message_handler.info,
        "validation_finished": validated
    }


def validate_origin_mzml2isa(fp: TextIO) -> None:
    """ A function to validate an ISA-Tab generated from a collection of mzML files (mzml2isa component)

    :param fp: the investigation file handler
    """
    from isatools import utils
    try:
        fp.seek(0)
        report = utils.detect_isatab_process_pooling(fp)
    except BaseException:
        pass


def batch_validate(tab_dir_list):
    """ Validate a batch of ISA-Tab archives

    :param tab_dir_list: List of file paths to the ISA-Tab archives to validate_rules
    :return: batch report as JSON

    Example:
        from isatools import isatab
        my_tabs = [
            '/path/to/study1/',
            '/path/to/study2/'
        ]
        batch_report = isatab.batch_validate(my_tabs, '/path/to/report.txt')
    """
    batch_report = {"batch_report": []}
    for tab_dir in tab_dir_list:
        log.info("***Validating {}***\n".format(tab_dir))
        i_files = glob(path.join(tab_dir, 'i_*.txt'))
        if len(i_files) != 1:
            log.warning("Could not find an investigation file, skipping {}".format(tab_dir))
        else:
            with utf8_text_file_open(i_files[0]) as fp:
                batch_report['batch_report'].append({"filename": fp.name, "report": validate(fp)})
    return batch_report
