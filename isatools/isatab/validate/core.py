from __future__ import absolute_import
from typing import List, Dict

from os import path
from glob import glob
from io import StringIO
import logging

from pandas.errors import ParserError
from pandas import DataFrame

from isatools.utils import utf8_text_file_open
from isatools.isatab.load import read_investigation_file, load_table
from isatools.isatab.defaults import _RX_COMMENT, NUMBER_OF_STUDY_GROUPS, default_config_dir, log
from isatools.isatab.validate.rules import *
from isatools.isatab.validate.store import validator as message_handler


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
                    message_handler.add_error(message=msg, supplemental=spl, code= 5)
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


def validate_investigation(investigation_dataframe: DataFrame,
                           filepath: str,
                           config_dir: str) -> (List, Dict):
    """ Validate the investigation data frame

    :param investigation_dataframe: DataFrame containing the investigation data
    :param filepath: Path to the investigation file
    :param config_dir: Path to the config directory
    :param validation_config: Tuple of validation config rules identifiers

    :returns: a tuple containing a list of term source references and the configuration
    """
    check_filenames_present(investigation_dataframe)  # Rule 3005
    check_table_files_read(investigation_dataframe, filepath)  # Rules 0006 and 0008
    check_samples_not_declared_in_study_used_in_assay(investigation_dataframe, filepath)  # Rule 1003
    check_study_factor_usage(investigation_dataframe, filepath)  # Rules 1008 and 1021
    check_protocol_usage(investigation_dataframe, filepath)  # Rules 1007 and 1019
    check_protocol_parameter_usage(investigation_dataframe, filepath)  # Rules 1009 and 1020
    check_date_formats(investigation_dataframe)  # Rule 3001
    check_dois(investigation_dataframe)  # Rule 3002
    check_pubmed_ids_format(investigation_dataframe)  # Rule 3003
    check_protocol_names(investigation_dataframe)  # Rule 1010
    check_protocol_parameter_names(investigation_dataframe)  # Rule 1011
    check_study_factor_names(investigation_dataframe)  # Rule 1012
    term_source_refs = check_ontology_sources(investigation_dataframe)  # Rule 3008

    log.info("Finished prechecks...")
    log.info("Loading configurations found in {}".format(config_dir))
    configs = load_config(config_dir)  # Rule 4001
    log.info("Using configurations found in {}".format(config_dir))
    check_measurement_technology_types(investigation_dataframe, configs)  # Rule 4002
    log.info("Checking investigation file against configuration...")
    check_investigation_against_config(investigation_dataframe, configs)  # Rule 4003 for investigation file only (DONE)
    log.info("Finished checking investigation file")

    return term_source_refs, configs


def validate_study(investigation_dataframe: DataFrame,
                   study_filename: str,
                   configs: Dict,
                   term_source_refs: List,
                   study_index: int,
                   filepath: str,
                   study_group_size_in_comment: bool) -> (Dict, DataFrame):
    """ Validate the study data frame

    :param investigation_dataframe: DataFrame containing the investigation data
    :param study_filename: Name of the study file
    :param configs: Dictionary containing the configuration data
    :param term_source_refs: List of term source references
    :param study_index: Index of the study in the investigation data frame
    :param filepath: Path to the study file
    :param study_group_size_in_comment: Boolean indicating if the study group size is in the comment

    :returns: a dictionary containing the protocols names and types
    """
    protocol_names = investigation_dataframe['s_protocols'][study_index]['Study Protocol Name'].tolist()
    protocol_types = investigation_dataframe['s_protocols'][study_index]['Study Protocol Type'].tolist()
    protocol_names_and_types = dict(zip(protocol_names, protocol_types))
    study_sample_table = None
    try:
        log.info("Loading... {}".format(study_filename))
        with utf8_text_file_open(path.join(filepath, study_filename)) as s_fp:
            study_sample_table = load_table(s_fp)
            study_sample_table.filename = study_filename
            config = configs[('[sample]', '')]
            log.info("Validating {} against default study table configuration".format(study_filename))
            log.info("Checking Factor Value presence...")
            check_factor_value_presence(study_sample_table)  # Rule 4007
            log.info("Checking required fields...")
            check_required_fields(study_sample_table, config)  # Rule 4003-8, 4010

            log.info("Checking generic fields...")
            if not check_field_values(study_sample_table, config):  # Rule 4011
                warning = "(W) There are some field value inconsistencies in {} against 'Study Sample' configuration"
                log.warning(warning.format(study_sample_table.filename))
            log.info("Checking unit fields...")

            if not check_unit_field(study_sample_table, config):
                warning = "(W) There are some unit value inconsistencies in {} against 'Study Sample' configuration"
                log.warning(warning.format(study_sample_table.filename))

            # Rule 4009
            log.info("Checking protocol fields...")
            if not check_protocol_fields(study_sample_table, config, protocol_names_and_types):
                warning = "(W) There are some protocol inconsistencies in {} against 'Study Sample' configuration"
                log.warning(warning.format(study_sample_table.filename))

            # Rule 3010
            log.info("Checking ontology fields...")
            if not check_ontology_fields(study_sample_table, config, term_source_refs):
                warning = "(W) There are some ontology annotation inconsistencies in {} against {} configuration"
                log.warning(warning.format(study_sample_table.filename, 'Study Sample'))

            log.info("Checking study group size...")
            check_study_groups(study_sample_table, study_filename, study_group_size_in_comment)
            log.info("Finished validation on {}".format(study_filename))
    except FileNotFoundError:
        pass
    return protocol_names_and_types, study_sample_table


def validate_assays(investigation_dataframe: DataFrame,
                    study_dataframe: DataFrame,
                    assay_index: int,
                    configs: Dict,
                    term_source_refs: List,
                    protocol_names_and_types: Dict,
                    assay_tables: List,
                    study_sample_table: None,
                    filepath: str) -> None:
    assay_df = investigation_dataframe['s_assays'][assay_index]
    study_group_size_in_comment = None
    if NUMBER_OF_STUDY_GROUPS in assay_df.columns:
        study_group_sizes = study_dataframe[NUMBER_OF_STUDY_GROUPS]
        study_group_size_in_comment = next(iter(study_group_sizes))
    for x, assay_filename in enumerate(assay_df['Study Assay File Name'].tolist()):
        measurement_type = assay_df['Study Assay Measurement Type'].tolist()[x]
        technology_type = assay_df['Study Assay Technology Type'].tolist()[x]
        if assay_filename != '':
            try:
                lowered_mt = measurement_type.lower()
                lowered_tt = technology_type.lower()
                config = configs[(lowered_mt, lowered_tt)]
            except KeyError:
                err = "Could not load config matching ({}, {})".format(measurement_type, technology_type)
                log.error(err)
                log.warning("Only have configs matching:")
                for k in configs.keys():
                    log.warning(k)
                config = None
            if config is None:
                log.warning("Skipping configuration validation as could not load config...")
            else:
                try:
                    log.info("Loading... {}".format(assay_filename))
                    with utf8_text_file_open(path.join(filepath, assay_filename)) as a_fp:
                        assay_table = load_table(a_fp)
                        assay_table.filename = assay_filename
                        assay_tables.append(assay_table)
                        log.info("Validating {} against assay table configuration ({}, {})..."
                                 .format(assay_filename, measurement_type, technology_type))
                        log.info("Checking Factor Value presence...")
                        check_factor_value_presence(assay_table)  # Rule 4007
                        log.info("Checking required fields...")
                        check_required_fields(assay_table, config)  # Rule 4003-8, 4010

                        log.info("Checking generic fields...")  # Rule 4011
                        if not check_field_values(assay_table, config):
                            warning = ("(W) There are some field value inconsistencies in {} against {} "
                                       "configuration").format(assay_table.filename,
                                                               (measurement_type, technology_type))
                            log.warning(warning)
                        log.info("Checking unit fields...")
                        if not check_unit_field(assay_table, config): # Rule 1099
                            warning = ("(W) There are some unit value inconsistencies in {} against {} "
                                       "configuration").format(assay_table.filename,
                                                               (measurement_type, technology_type))
                            log.warning(warning)
                        log.info("Checking protocol fields...")

                        # Rule 4009
                        if not check_protocol_fields(assay_table, config, protocol_names_and_types):
                            warn = ("(W) There are some protocol inconsistencies in {} against {} "
                                    "configuration")
                            warn = warn.format(assay_table.filename, (measurement_type, technology_type))
                            log.warning(warn)
                        log.info("Checking ontology fields...")

                        # Rule 3010
                        if not check_ontology_fields(assay_table, config, term_source_refs):
                            warn = ("(W) There are some ontology annotation inconsistencies in {} "
                                    "against {} configuration").format(assay_table.filename,
                                                                       (measurement_type, technology_type))
                            log.warning(warn)
                        log.info("Checking study group size...")
                        check_study_groups(assay_table, assay_filename, study_group_size_in_comment)
                        log.info("Finished validation on {}".format(assay_filename))
                except FileNotFoundError:
                    pass
            if study_sample_table is not None:
                log.info("Checking consistencies between study sample table and assay tables...")

                check_sample_names(study_sample_table, assay_tables)
                log.info("Finished checking study sample table against assay tables...")


def validate(fp, config_dir=default_config_dir, log_level=None):
    """Runs the ISA-Tab validator and builds a validation report. Note that
    this function uses global variables to collect validation messages

    :param fp: A file-like buffer object pointing to the investigation file
    :param config_dir: Full path to the ISA XML configuration directory
    :param log_level: Logging level as defined by the logging module. e.g.
    logging.WARN, logging.DEBUG etc.
    :return: A JSON report containing validation messages of different levels,
    e.g. errors, warnings, info.
    """
    validator.reset_store()
    if log_level in (logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL):
        log.setLevel(log_level)
    log.debug("ISA tab Validator from ISA tools API v0.6")
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    log.addHandler(handler)
    validation_finished = False

    try:
        log.info("Loading... {}".format(fp.name))
        i_df = load_investigation(fp=fp)
        log.info("Running prechecks...")
        term_source_refs, configs = validate_investigation(i_df, path.dirname(fp.name), config_dir)

        for i, study_df in enumerate(i_df['studies']):
            study_group_size_in_comment = None
            if NUMBER_OF_STUDY_GROUPS in study_df.columns:
                study_group_sizes = study_df[NUMBER_OF_STUDY_GROUPS]
                study_group_size_in_comment = next(iter(study_group_sizes))
            study_filename = study_df.iloc[0]['Study File Name']
            assay_tables = list()
            if study_filename != '':
                protocol_names_and_types, study_sample_table = validate_study(i_df,
                                                                              study_filename,
                                                                              configs,
                                                                              term_source_refs,
                                                                              i,
                                                                              path.dirname(fp.name),
                                                                              study_group_size_in_comment)

                validate_assays(i_df,
                                study_df,
                                i,
                                configs,
                                term_source_refs,
                                protocol_names_and_types,
                                assay_tables,
                                study_sample_table,
                                path.dirname(fp.name))
        if len(validator.errors) != 0:
            log.info("Skipping pooling test as there are outstanding errors")
        else:
            from isatools import utils
            try:
                fp.seek(0)
                utils.detect_isatab_process_pooling(fp)
            except BaseException:
                pass
        log.info("Finished validation...")
        validation_finished = True
    except (Exception, ParserError, SystemError, ValueError) as e:
        spl = "The validator could not identify what the error is: {}".format(str(e))
        validator.add_error(message="Unknown/System Error", supplemental=spl, code=0)
        log.fatal("(F) Something went very very wrong! :(")
        log.fatal(e)
    finally:
        handler.flush()
        return {
            "errors": validator.errors,
            "warnings": validator.warnings,
            "info": validator.info,
            "validation_finished": validation_finished
        }


def batch_validate(tab_dir_list):
    """Validate a batch of ISA-Tab archives
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
