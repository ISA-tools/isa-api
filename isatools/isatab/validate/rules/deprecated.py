from os import path

from isatools.utils import utf8_text_file_open
from isatools.isatab.defaults import (
    log,
    _RX_INDEXED_COL,
    _RX_CHARACTERISTICS,
    _RX_PARAMETER_VALUE,
    _RX_FACTOR_VALUE,
    _RX_COMMENT
)
from isatools.isatab.utils import cell_has_value, get_ontology_source_refs
from isatools.isatab.load import load_table


validator_errors = []
validator_warnings = []
validator_info = []


def load_table_checks(fp):
    """Checks that a table can be loaded and returns the loaded table, if
    successful

    :param fp: A file-like buffer object
    :return: DataFrame of the study or assay table
    """
    df = load_table(fp)
    columns = df.columns
    for x, column in enumerate(columns):  # check if columns have valid labels
        if _RX_INDEXED_COL.match(column):
            column = column[:column.rfind('.')]
        if (column not in ['Source Name', 'Sample Name', 'Term Source REF',
                           'Protocol REF', 'Term Accession Number',
                           'Unit', 'Assay Name', 'Extract Name',
                           'Raw Data File', 'Material Type', 'MS Assay Name', 'NMR Assay Name'
                                                                              'Raw Spectral Data File',
                           'Labeled Extract Name',
                           'Label', 'Hybridization Assay Name',
                           'Array Design REF', 'Scan Name', 'Array Data File',
                           'Protein Assignment File',
                           'Peptide Assignment File',
                           'Post Translational Modification Assignment File',
                           'Data Transformation Name',
                           'Derived Spectral Data File', 'Normalization Name',
                           'Derived Array Data File', 'Image File',
                           'Metabolite Assignment File',
                           'Free Induction Decay File',
                           'Acquisition Parameter Data File']) \
                and not _RX_CHARACTERISTICS.match(column) \
                and not _RX_PARAMETER_VALUE.match(column) \
                and not _RX_FACTOR_VALUE.match(column) \
                and not _RX_COMMENT.match(column):
            log.error("Unrecognised column heading {} at column position {} "
                      "in table file {}".format(column, x, path.basename(fp.name)))
        if _RX_COMMENT.match(column):
            if len(_RX_COMMENT.findall(column)) == 0:
                log.warning("(W) In file {}, label {} is missing a name"
                            .format(path.basename(fp.name), column))
                validator_warnings.append({
                    "message": "Missing name in Comment[] label",
                    "supplemental": "In file {}, label {} is missing a name"
                        .format(path.basename(fp.name), column),
                    "code": 4014
                })
        if _RX_CHARACTERISTICS.match(column):
            if len(_RX_CHARACTERISTICS.findall(column)) == 0:
                log.warning("(W) In file {}, label {} is missing a name"
                            .format(path.basename(fp.name), column))
                validator_warnings.append({
                    "message": "Missing name in Characteristics[] label",
                    "supplemental": "In file {}, label {} is missing a name"
                        .format(path.basename(fp.name), column),
                    "code": 4014
                })
        if _RX_PARAMETER_VALUE.match(column):
            if len(_RX_PARAMETER_VALUE.findall(column)) == 0:
                log.warning("(W) In file {}, label {} is missing a name"
                            .format(path.basename(fp.name), column))
                validator_warnings.append({
                    "message": "Missing name in Parameter Value[] label",
                    "supplemental": "In file {}, label {} is missing a name"
                        .format(path.basename(fp.name), column),
                    "code": 4014
                })
        if _RX_FACTOR_VALUE.match(column):
            if len(_RX_FACTOR_VALUE.findall(column)) == 0:
                log.warning("(W) In file {}, label {} is missing a name"
                            .format(path.basename(fp.name), column))
                validator_warnings.append({
                    "message": "Missing name in Factor Value[] label",
                    "supplemental": "In file {}, label {} is missing a name"
                        .format(path.basename(fp.name), column),
                    "code": 4014
                })
    norm_columns = list()
    for x, column in enumerate(columns):
        if _RX_INDEXED_COL.match(column):
            norm_columns.append(column[:column.rfind('.')])
        else:
            norm_columns.append(column)
    object_index = [i for i, x in enumerate(norm_columns)
                    if x in ['Source Name', 'Sample Name', 'Protocol REF',
                             'Extract Name', 'Labeled Extract Name',
                             'Raw Data File',
                             'Raw Spectral Data File', 'Array Data File',
                             'Protein Assignment File',
                             'Peptide Assignment File',
                             'Post Translational Modification Assignment File',
                             'Derived Spectral Data File',
                             'Derived Array Data File']
                    or _RX_FACTOR_VALUE.match(x)]
    object_columns_list = list()
    prev_i = object_index[0]
    for curr_i in object_index:
        if prev_i == curr_i:
            pass
        else:
            object_columns_list.append(norm_columns[prev_i:curr_i])
        prev_i = curr_i
    object_columns_list.append(norm_columns[prev_i:])

    for object_columns in object_columns_list:
        prop_name = object_columns[0]
        if prop_name in ['Sample Name', 'Source Name']:
            for x, col in enumerate(object_columns[1:]):
                if col not in ['Term Source REF', 'Term Accession Number',
                               'Unit'] and not _RX_CHARACTERISTICS.match(col) \
                        and not _RX_FACTOR_VALUE.match(col) \
                        and not _RX_COMMENT.match(col):
                    log.error("(E) Expected only Characteristics, "
                              "Factor Values or Comments following {} "
                              "columns but found {} at offset {}".format(prop_name, col, x + 1))
        elif prop_name == 'Protocol REF':
            for x, col in enumerate(object_columns[1:]):
                if col not in ['Term Source REF', 'Term Accession Number',
                               'Unit', 'Assay Name',
                               'Hybridization Assay Name', 'Array Design REF',
                               'Scan Name'] \
                        and not _RX_PARAMETER_VALUE.match(col) \
                        and not _RX_COMMENT.match(col):
                    log.error("(E) Unexpected column heading following {} "
                              "column. Found {} at offset {}".format(prop_name, col, x + 1))
        elif prop_name == 'Extract Name':
            if len(object_columns) > 1:
                log.error(
                    "Unexpected column heading(s) following {} column. "
                    "Found {} at offset {}".format(
                        prop_name, object_columns[1:], 2))
        elif prop_name == 'Labeled Extract Name':
            if len(object_columns) > 1:
                if object_columns[1] == 'Label':
                    for x, col in enumerate(object_columns[2:]):
                        if col not in ['Term Source REF',
                                       'Term Accession Number']:
                            log.error("(E) Unexpected column heading "
                                      "following {} column. Found {} at "
                                      "offset {}".format(prop_name, col, x + 1))
                else:
                    log.error("(E) Unexpected column heading following {} "
                              "column. Found {} at offset {}".format(prop_name, object_columns[1:], 2))
            else:
                log.error("Expected Label column after Labeled Extract Name "
                          "but none found")
        elif prop_name in ['Raw Data File', 'Derived Spectral Data File',
                           'Derived Array Data File', 'Array Data File',
                           'Raw Spectral Data File', 'Protein Assignment File',
                           'Peptide Assignment File',
                           'Post Translational Modification Assignment File']:
            for x, col in enumerate(object_columns[1:]):
                if not _RX_COMMENT.match(col):
                    log.error("(E) Expected only Comments following {} "
                              "columns but found {} at offset {}".format(prop_name, col, x + 1))
        elif _RX_FACTOR_VALUE.match(prop_name):
            for x, col in enumerate(object_columns[2:]):
                if col not in ['Term Source REF', 'Term Accession Number']:
                    log.error(
                        "(E) Unexpected column heading following {} column. "
                        "Found {} at offset {}".format(prop_name, col, x + 1))
        else:
            log.debug("Need to implement a rule for... " + prop_name)
            log.debug(object_columns)
    return df


def check_utf8(fp):
    """Used for rule 0010

    .. warning:: This is unused
    :param fp: A file-like buffer object
    :return: None
    """
    import chardet
    with utf8_text_file_open(fp.name) as fp:
        charset = chardet.detect(fp.read())
        if charset['encoding'] != 'UTF-8' and charset['encoding'] != 'ascii':
            validator_warnings.append({
                "message": "File should be UTF8 encoding",
                "supplemental": "Encoding is '{0}' with confidence {1}".format(
                    charset['encoding'], charset['confidence']),
                "code": 10
            })
            log.warning("File should be UTF-8 encoding but found it is '{0}' "
                        "encoding with {1} confidence".format(
                charset['encoding'], charset['confidence']))
            raise SystemError()


def check_table_files_load(i_df, dir_context):
    """Used for rules 0007 and 0009

    :param i_df: An investigation DataFrame
    :param dir_context: Path to where the investigation file is found
    :return: None
    """
    for i, study_df in enumerate(i_df['studies']):
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename != '':
            try:
                with utf8_text_file_open(path.join(
                        dir_context, study_filename)) as fp:
                    load_table_checks(fp)
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(
                i_df['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename != '':
                try:
                    with utf8_text_file_open(path.join(
                            dir_context, assay_filename)) as fp:
                        load_table_checks(fp)
                except FileNotFoundError:
                    pass


def check_term_source_refs_in_investigation(i_df):
    """Used for rules 3007 and 3009

    :param i_df: An investigation DataFrame
    :return: None
    """
    ontology_sources_list = get_ontology_source_refs(i_df)

    def check_study_term_sources_in_secton_field(
            section_label, pos, column_label):
        section_term_source_refs = [
            i for i in i_df[
                section_label][pos][column_label].tolist() if i != '']
        # this for loop deals with semicolon separated lists of term source
        # refs
        section_term_source_refs_to_remove = list()
        for section_term_source_ref in section_term_source_refs:
            if ';' in section_term_source_ref:
                term_sources = [
                    i for i in section_term_source_ref.split(';') if i != '']
                section_term_source_refs_to_remove.append(
                    section_term_source_ref)
                section_term_source_refs.extend(term_sources)
        for section_term_source_ref_to_remove \
                in section_term_source_refs_to_remove:
            section_term_source_refs.remove(section_term_source_ref_to_remove)
        diff = set(section_term_source_refs) - set(ontology_sources_list)
        if len(diff) > 0:
            validator_warnings.append({
                "message": "Missing Term Source",
                "supplemental": "Ontology sources missing {}".format(list(diff)),
                "code": 3009
            })
            log.warning("(W) In {} one or more of {} has not been declared in "
                        "{}.{} section".format(column_label,
                                               section_term_source_refs,
                                               section_label, pos))

    i_publication_status_term_source_ref = [
        i for i in i_df['i_publications']['Investigation Publication Status Term Source REF'].tolist() if i != '']
    diff = set(i_publication_status_term_source_ref) - set(ontology_sources_list)
    if len(diff) > 0:
        validator_warnings.append({
            "message": "Missing Term Source",
            "supplemental": "Ontology sources missing {}".format(list(diff)),
            "code": 3009
        })
        log.warning("(W) Investigation Publication Status Term Source REF {} "
                    "has not been declared in ONTOLOGY SOURCE "
                    "REFERENCE section".format(i_publication_status_term_source_ref))
    i_person_roles_term_source_ref = [
        i for i in i_df['i_contacts'][
            'Investigation Person Roles Term Source REF'].tolist() if i != '']
    diff = set(i_person_roles_term_source_ref) - set(ontology_sources_list)
    if len(diff) > 0:
        validator_warnings.append({
            "message": "Missing Term Source",
            "supplemental": "Ontology sources missing {}".format(list(diff)),
            "code": 3009
        })
        log.warning("(W) Investigation Person Roles Term Source REF {} has "
                    "not been declared in ONTOLOGY SOURCE "
                    "REFERENCE section".format(i_person_roles_term_source_ref))

    for i, study_df in enumerate(i_df['studies']):
        check_study_term_sources_in_secton_field(
            's_design_descriptors', i, 'Study Design Type Term Source REF')
        check_study_term_sources_in_secton_field(
            's_publications', i, 'Study Publication Status Term Source REF')
        check_study_term_sources_in_secton_field(
            's_assays', i, 'Study Assay Measurement Type Term Source REF')
        check_study_term_sources_in_secton_field(
            's_assays', i, 'Study Assay Technology Type Term Source REF')
        check_study_term_sources_in_secton_field(
            's_protocols', i, 'Study Protocol Type Term Source REF')
        check_study_term_sources_in_secton_field(
            's_protocols', i, 'Study Protocol Parameters Name Term Source REF')
        check_study_term_sources_in_secton_field(
            's_protocols', i, 'Study Protocol Components Type Term Source REF')
        check_study_term_sources_in_secton_field(
            's_contacts', i, 'Study Person Roles Term Source REF')


def check_term_source_refs_in_assay_tables(i_df, dir_context):
    """Used for rules 3007 and 3009

    :param i_df: An investigation DataFrame
    :param dir_context: a directory
    :return: None
    """

    import math
    ontology_sources_list = set(get_ontology_source_refs(i_df))
    for i, study_df in enumerate(i_df['studies']):
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename != '':
            try:
                with utf8_text_file_open(path.join(dir_context,
                                                   study_filename)) as s_fp:
                    df = load_table(s_fp)
                    columns = df.columns
                    object_index = [i for i, x in enumerate(
                        columns) if x.startswith('Term Source REF')]
                    prev_i = object_index[0]
                    object_columns_list = [columns[prev_i]]
                    for curr_i in object_index:
                        if prev_i == curr_i:
                            pass
                        else:
                            object_columns_list.append(columns[curr_i])
                        prev_i = curr_i
                    for x, col in enumerate(object_columns_list):
                        for y, row in enumerate(df[col]):
                            if row not in ontology_sources_list:
                                if isinstance(row, float):
                                    if not math.isnan(row):
                                        sup_msg = \
                                            "Ontology sources missing {} at " \
                                            "column position {} and row {} " \
                                            "in {} not declared in ontology " \
                                            "sources {}".format(
                                                row + 1,
                                                object_index[x],
                                                y + 1,
                                                study_filename,
                                                list(ontology_sources_list))
                                        validator_warnings.append({
                                            "message": "Missing Term Source",
                                            "supplemental": sup_msg,
                                            "code": 3009
                                        })
                                        oslist = ontology_sources_list
                                        log.warning("(W) Term Source REF {} "
                                                    "at column position {} "
                                                    "and row {} in {} not "
                                                    "declared in ontology "
                                                    "sources {}".format(
                                            row + 1,
                                            object_index[x],
                                            y + 1,
                                            study_filename,
                                            list(oslist)))
                                else:
                                    oslist = ontology_sources_list
                                    validator_warnings.append({
                                        "message": "Missing Term Source",
                                        "supplemental": "Ontology sources "
                                                        "missing {} at column "
                                                        "position {} and "
                                                        "row {} in {} not "
                                                        "declared in ontology "
                                                        "sources {}".format(
                                            row + 1,
                                            object_index[x],
                                            y + 1,
                                            study_filename,
                                            list(oslist)),
                                        "code": 3009
                                    })
                                    log.warning("(W) Term Source REF {} at "
                                                "column position {} and row "
                                                "{} in {} not in declared "
                                                "ontology sources {}"
                                        .format(
                                        row + 1,
                                        object_index[x],
                                        y + 1,
                                        study_filename,
                                        list(oslist)))
            except FileNotFoundError:
                pass
            for j, assay_filename in enumerate(
                    i_df['s_assays'][i]['Study Assay File Name'].tolist()):
                if assay_filename != '':
                    try:
                        with utf8_text_file_open(
                                path.join(
                                    dir_context, assay_filename)) as a_fp:
                            df = load_table(a_fp)
                            columns = df.columns
                            object_index = [i for i, x in enumerate(
                                columns) if x.startswith('Term Source REF')]
                            prev_i = object_index[0]
                            object_columns_list = [columns[prev_i]]
                            for curr_i in object_index:
                                if prev_i == curr_i:
                                    pass
                                else:
                                    object_columns_list.append(
                                        columns[curr_i])
                                prev_i = curr_i
                            for x, col in enumerate(object_columns_list):
                                for y, row in enumerate(df[col]):
                                    if row not in ontology_sources_list:
                                        if isinstance(row, float):
                                            if not math.isnan(row):
                                                oslist = ontology_sources_list
                                                sup_msg = \
                                                    "Ontology sources " \
                                                    "missing {} at column " \
                                                    "position {} and " \
                                                    "row {} in {} not " \
                                                    "declared in ontology " \
                                                    "sources {}".format(
                                                        row + 1,
                                                        object_index[x],
                                                        y + 1,
                                                        study_filename,
                                                        list(oslist))
                                                validator_warnings.append({
                                                    "message": "Missing "
                                                               "Term Source",
                                                    "supplemental": sup_msg,
                                                    "code": 3009
                                                })
                                                log.warning(
                                                    "(W) Term Source REF {} "
                                                    "at column position {} "
                                                    "and row {} in {} not "
                                                    "declared in ontology "
                                                    "sources {}".format(
                                                        row + 1,
                                                        object_index[x],
                                                        y + 1,
                                                        study_filename,
                                                        list(oslist)))
                                        else:
                                            sup_msg = \
                                                "Ontology sources missing " \
                                                "{} at column position {} " \
                                                "and row {} in {} not " \
                                                "declared in ontology " \
                                                "sources {}" \
                                                    .format(
                                                    row + 1,
                                                    object_index[x],
                                                    y + 1, study_filename,
                                                    list(
                                                        ontology_sources_list))
                                            validator_warnings.append({
                                                "message": "Missing "
                                                           "Term Source",
                                                "supplemental": sup_msg,
                                                "code": 3009
                                            })
                                            log.warning(
                                                "(W) Term Source REF {} at "
                                                "column position {} and row "
                                                "{} in {} not in declared "
                                                "ontology sources {}"
                                                    .format(
                                                    row + 1,
                                                    object_index[x],
                                                    y + 1, study_filename,
                                                    list(ontology_sources_list
                                                         )))
                    except FileNotFoundError:
                        pass


def check_term_source_refs_usage(i_df, dir_context):
    """Checks Term Source REF linkages in investigation, study and assay files

    :param i_df: An investigation DataFrame
    :param dir_context: Path to where the investigation file is found
    :return: None
    """
    check_term_source_refs_in_investigation(i_df)
    check_term_source_refs_in_assay_tables(i_df, dir_context)


def check_study_table_against_config(s_df, protocols_declared, config):
    """Checks a study-sample table against a given configuration

    :param s_df: A study-sample table DataFrame
    :param protocols_declared: List of protocols declared
    :param config: An ISA Configuration object
    :return: None
    """
    # We are assuming the table load validation earlier passed

    # First check column order is correct against the configuration
    columns = s_df.columns
    object_index = [(x, i) for x, i in enumerate(columns) if i in [
        'Source Name', 'Sample Name',
        'Extract Name', 'Labeled Extract Name', 'Raw Data File',
        'Raw Spectral Data File', 'Array Data File',
        'Protein Assignment File', 'Peptide Assignment File',
        'Post Translational Modification Assignment File',
        'Derived Spectral Data File',
        'Derived Array Data File']
                    or 'Protocol REF' in i
                    or 'Characteristics[' in i
                    or 'Factor Value[' in i
                    or 'Parameter Value[ in i']
    fields = [i.header for i in config.get_isatab_configuration()[0].get_field()]
    protocols = [(i.pos, i.protocol_type)
                 for i in config.get_isatab_configuration()[0].get_protocol_field()]
    for protocol in protocols:
        fields.insert(protocol[0], 'Protocol REF')
    # strip out non-config columns
    object_index = [i for i in object_index if i[1] in fields]
    for x, object in enumerate(object_index):
        if fields[x] != object[1]:
            validator_warnings.append({
                "message": "The column order in assay table is not valid",
                "supplemental": "Unexpected heading found. Expected {} but "
                                "found {} at column number {}"
                    .format(fields[x], object[1], object[0]),
                "code": 4005
            })
            log.warning("(W) Unexpected heading found. Expected {} but "
                        "found {} at column number {}"
                        .format(fields[x], object[1], object[0]))

    # Second, check if Protocol REFs are of valid types
    for row in s_df['Protocol REF']:
        log.debug(row, protocols_declared[row] in [
            i[1] for i in protocols], [i[1] for i in protocols])
    # Third, check if required values are present


def check_assay_table_against_config(s_df, config):
    """Checks a assay table against a given configuration

    :param s_df: An assay table DataFrame
    :param config: An ISA Configuration object
    :return: None
    """
    import itertools
    # We are assuming the table load validation earlier passed
    # First check column order is correct against the configuration
    columns = s_df.columns
    norm_columns = list()
    for x, column in enumerate(columns):
        if _RX_INDEXED_COL.match(column):
            norm_columns.append(column[:column.rfind('.')])
        else:
            norm_columns.append(column)
    # remove adjacent dups - i.e. chained Protocol REFs
    norm_columns = [k for k, g in itertools.groupby(norm_columns)]
    object_index = [(x, i) for x, i in enumerate(norm_columns) if i in [
        'Source Name', 'Sample Name',
        'Extract Name', 'Labeled Extract Name', 'Raw Data File',
        'Raw Spectral Data File', 'Array Data File',
        'Protein Assignment File', 'Peptide Assignment File',
        'Post Translational Modification Assignment File',
        'Derived Spectral Data File',
        'Derived Array Data File', 'Assay Name']
                    or 'Protocol REF' in i
                    or 'Characteristics[' in i
                    or 'Factor Value[' in i
                    or 'Parameter Value[ in i'
                    or 'Comment[' in i]
    fields = [i.header for i in config.get_isatab_configuration()[
        0].get_field()]
    protocols = [(i.pos, i.protocol_type)
                 for i in config.get_isatab_configuration()[0].get_protocol_field()]
    for protocol in protocols:
        fields.insert(protocol[0], 'Protocol REF')
    # strip out non-config columns
    object_index = [i for i in object_index if i[1] in fields]
    for x, current_object in enumerate(object_index):
        if fields[x] != current_object[1]:
            validator_warnings.append({
                "message": "The column order in assay table is not valid",
                "supplemental": "Unexpected heading found. Expected {} but "
                                "found {} at column number {}"
                    .format(fields[x], current_object[1], current_object[0]),
                "code": 4005
            })
            log.warning("(W) Unexpected heading found. Expected {} but found "
                        "{} at column number {}".format(
                fields[x], current_object[1], current_object[0]))


def check_assay_table_with_config(df, config, filename, protocol_names_and_types):
    """Checks a assay table against a given configuration

    :param df: A table DataFrame
    :param config: An ISA Configuration object
    :param filename: The filename of the table
    :param protocol_names_and_types: List of protocol names and types
    :return: None
    """
    columns = list(df.columns)
    # Get required headers from config and check if they are present in the
    # table; Rule 4010
    required_fields = [i.header for i in config.get_isatab_configuration()[
        0].get_field() if i.is_required]
    for required_field in required_fields:
        if required_field not in columns:
            validator_warnings.append({
                "message": "A required column in assay table is not present",
                "supplemental": "In {} the required column {} missing "
                                "from column headings"
                    .format(filename, required_field),
                "code": 4010
            })
            log.warning("(W) In {} the required column {} missing from "
                        "column headings".format(filename, required_field))
        else:
            # Now check that the required column cells all have values, Rules
            # 4003-4008
            for y, cell in enumerate(df[required_field]):
                if not cell_has_value(cell):
                    validator_warnings.append({
                        "message": "A required cell value is missing",
                        "supplemental": "Cell at row {} in column '{}' has "
                                        "no value".format(y, required_field),
                        "code": 4012
                    })
                    log.warning("(W) Cell at row {} in column '{}' has no "
                                "value, but it is required by the "
                                "configuration".format(y, required_field))

    # Check if protocol ref column values are consistently structured
    protocol_ref_index = [i for i in columns if 'protocol ref' in i.lower()]
    for each in protocol_ref_index:
        prots_found = set()
        for cell in df[each]:
            prots_found.add(cell)
        if len(prots_found) > 1:
            validator_warnings.append({
                "message": "Multiple protocol references in Protocol "
                           "REF column",
                "supplemental": "Multiple protocol references {} are found "
                                "in {}".format(prots_found, each),
                "code": 4999
            })
            log.warning(
                "(W) Multiple protocol references {} are found in {}".format(
                    prots_found, each))
            log.warning(
                "(W) Only one protocol reference should be used in a "
                "Protocol REF column.")


def check_study_assay_tables_against_config(i_df, dir_context, configs):
    """Used for rules 4003-4008. Checks all study and assay tables against
    the configurations, for a given ISA-Tab. It looks first at the
    study and assay tables that are referenced by the investigation.

    :param i_df: An investigation DataFrame dictionary
    :param dir_context: The path in which the ISA-Tab files are sourced
    :param configs: The loaded set of ISA Configuration XMLs as config objects
    :return: None
    """
    for i, study_df in enumerate(i_df['studies']):
        study_filename = study_df.iloc[0]['Study File Name']
        protocol_names = i_df['s_protocols'][i]['Study Protocol Name'].tolist()
        protocol_types = i_df['s_protocols'][i]['Study Protocol Type'].tolist()
        protocol_names_and_types = dict(zip(protocol_names, protocol_types))
        if study_filename != '':
            try:
                with utf8_text_file_open(path.join(
                        dir_context, study_filename)) as s_fp:
                    df = load_table(s_fp)
                    config = configs[('[sample]', '')]
                    log.debug("Checking study file {} against default study "
                              "table configuration...".format(study_filename))
                    check_assay_table_with_config(
                        df, config, study_filename, protocol_names_and_types)
            except FileNotFoundError:
                pass
        for j, assay_df in enumerate(i_df['s_assays']):
            assay_filename = assay_df['Study Assay File Name'].tolist()[0]
            measurement_type = assay_df[
                'Study Assay Measurement Type'].tolist()[
                0]
            technology_type = assay_df[
                'Study Assay Technology Type'].tolist()[
                0]
            if assay_filename != '':
                try:
                    with utf8_text_file_open(path.join(
                            dir_context, assay_filename)) as a_fp:
                        df = load_table(a_fp)
                        lowered_mt = measurement_type.lower()
                        lowered_tt = technology_type.lower()
                        config = configs[(lowered_mt, lowered_tt)]
                        log.debug("Checking assay file {} against default "
                                  "table configuration ({}, {})...".format(
                            assay_filename, measurement_type,
                            technology_type))
                        check_assay_table_with_config(
                            df, config, assay_filename,
                            protocol_names_and_types)
                        # check_assay_table_with_config(df, protocols, config,
                        # assay_filename)
                except FileNotFoundError:
                    pass
        # TODO: Check protocol usage - Rule 4009
