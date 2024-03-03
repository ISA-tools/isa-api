from os import path

from pandas import notnull

from isatools.utils import utf8_text_file_open
from isatools.isatab.load import load_table
from isatools.isatab.defaults import _RX_FACTOR_VALUE, _RX_PARAMETER_VALUE, log
from isatools.isatab.validate.store import validator
from isatools.isatab.utils import cell_has_value


def check_samples_not_declared_in_study_used_in_assay(i_df_dict, dir_context):
    """Checks if samples found in assay tables are found in the study-sample table

    :param i_df_dict: A dictionary of  DataFrame and list of Dataframes representing the Investigation file
    :param dir_context: Path to where the investigation file is found
    :return: None
    """
    for i, study_df in enumerate(i_df_dict['studies']):
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename != '':
            try:
                with utf8_text_file_open(path.join(dir_context, study_filename)) as s_fp:
                    study_df = load_table(s_fp)
                    study_samples = set(study_df['Sample Name'])
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(i_df_dict['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename != '':
                try:
                    with utf8_text_file_open(path.join(dir_context, assay_filename)) as a_fp:
                        assay_df = load_table(a_fp)
                        assay_samples = set(assay_df['Sample Name'])
                        if not assay_samples.issubset(study_samples):
                            spl = ("Some samples in an assay file {} are not declared in the study file {}: "
                                   "{}").format(assay_filename, study_filename, list(assay_samples - study_samples))
                            msg = "Some samples are not declared in the study"
                            validator.add_error(message=msg, supplemental=spl, code=1013)
                except FileNotFoundError:
                    pass


def check_study_factor_usage(i_df_dict, dir_context):
    """Used for rules 1008 and 1021

    :param i_df_dict: A dictionary of  DataFrame and list of Dataframes representing the Investigation file
    :param dir_context: Path to where the investigation file is found
    :return: None
    """
    for i, study_df in enumerate(i_df_dict['studies']):
        study_factors_declared = set(i_df_dict['s_factors'][i]['Study Factor Name'].tolist())
        study_filename = study_df.iloc[0]['Study File Name']
        error_spl = "Some factors used in an study file {} are not declared in the investigation file: {}"
        error_msg = "Some factors are not declared in the investigation"
        if study_filename != '':
            try:
                study_factors_used = set()
                with utf8_text_file_open(path.join(dir_context, study_filename)) as s_fp:
                    study_df = load_table(s_fp)
                    study_factor_ref_cols = [i for i in study_df.columns if _RX_FACTOR_VALUE.match(i)]
                    for col in study_factor_ref_cols:
                        fv = _RX_FACTOR_VALUE.findall(col)
                        study_factors_used = study_factors_used.union(set(fv))
                    if not study_factors_used.issubset(study_factors_declared):
                        spl = error_spl.format(study_filename, list(study_factors_used - study_factors_declared))
                        validator.add_error(message=error_msg, supplemental=spl, code=1008)
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(i_df_dict['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename != '':
                try:
                    study_factors_used = set()
                    with utf8_text_file_open(path.join(dir_context, assay_filename)) as a_fp:
                        assay_df = load_table(a_fp)
                        study_factor_ref_cols = set([i for i in assay_df.columns if _RX_FACTOR_VALUE.match(i)])
                        for col in study_factor_ref_cols:
                            fv = _RX_FACTOR_VALUE.findall(col)
                            study_factors_used = study_factors_used.union(set(fv))
                        if not study_factors_used.issubset(study_factors_declared):
                            spl = error_spl.format(assay_filename, list(study_factors_used - study_factors_declared))
                            validator.add_error(message=error_msg, supplemental=spl, code=1008)
                except FileNotFoundError:
                    pass
        study_factors_used = set()
        if study_filename != '':
            try:
                with utf8_text_file_open(path.join(dir_context, study_filename)) as s_fp:
                    study_df = load_table(s_fp)
                    study_factor_ref_cols = [i for i in study_df.columns if _RX_FACTOR_VALUE.match(i)]
                    for col in study_factor_ref_cols:
                        fv = _RX_FACTOR_VALUE.findall(col)
                        study_factors_used = study_factors_used.union(set(fv))
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(i_df_dict['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename != '':
                try:
                    with utf8_text_file_open(path.join(dir_context, assay_filename)) as a_fp:
                        assay_df = load_table(a_fp)
                        study_factor_ref_cols = set([i for i in assay_df.columns if _RX_FACTOR_VALUE.match(i)])
                        for col in study_factor_ref_cols:
                            fv = _RX_FACTOR_VALUE.findall(col)
                            study_factors_used = study_factors_used.union(set(fv))
                except FileNotFoundError:
                    pass
        if len(study_factors_declared - study_factors_used) > 0:
            spl = "Some study factors declared in the investigation file  are not used in any assay file: "
            log.warning("(W) Some study factors declared in the investigation file  are not used in any assay file: {}"
                        .format(list(study_factors_declared - study_factors_used)))


def check_protocol_usage(i_df_dict, dir_context):
    """Used for rules 1007 and 1019

    :param i_df_dict: A dictionary of  DataFrame and list of Dataframes representing the Investigation file
    :param dir_context: Path to where the investigation file is found
    :return: None
    """
    for i, study_df in enumerate(i_df_dict['studies']):
        protocols_declared = set(i_df_dict['s_protocols'][i]['Study Protocol Name'].tolist())
        protocols_declared.add('')
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename != '':
            try:
                protocol_refs_used = set()
                with utf8_text_file_open(path.join(dir_context, study_filename)) as s_fp:
                    study_df = load_table(s_fp)
                    for protocol_ref_col in [i for i in study_df.columns if i.startswith('Protocol REF')]:
                        protocol_refs_used = protocol_refs_used.union(study_df[protocol_ref_col])
                    protocol_refs_used = set([r for r in protocol_refs_used if notnull(r)])
                    diff = list(protocol_refs_used - protocols_declared)
                    if len(diff) > 0:
                        spl = "protocols in study file {} are not declared in the investigation file: {}"
                        spl = spl.format(study_filename, diff)
                        validator.add_error(message="Missing Protocol declaration", supplemental=spl, code=1007)
                        log.error("(E) {}".format(spl))
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(i_df_dict['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename != '':
                try:
                    protocol_refs_used = set()
                    with utf8_text_file_open(path.join(dir_context, assay_filename)) as a_fp:
                        assay_df = load_table(a_fp)
                        for protocol_ref_col in [i for i in assay_df.columns if i.startswith('Protocol REF')]:
                            protocol_refs_used = protocol_refs_used.union(assay_df[protocol_ref_col])
                        protocol_refs_used = set([r for r in protocol_refs_used if notnull(r)])
                        diff = list(protocol_refs_used - protocols_declared)
                        if len(diff) > 0:
                            spl = "protocols in study file {} are not declared in the investigation file: {}"
                            spl = spl.format(study_filename, diff)
                            validator.add_error(message="Missing Protocol declaration", supplemental=spl, code=1007)
                            log.error("(E) {}".format(spl))
                except FileNotFoundError:
                    pass

        # now collect all protocols in all assays to compare to declared protocols
        protocol_refs_used = set()
        if study_filename != '':
            try:
                with utf8_text_file_open(path.join(dir_context, study_filename)) as s_fp:
                    study_df = load_table(s_fp)
                    for protocol_ref_col in [i for i in study_df.columns if i.startswith('Protocol REF')]:
                        protocol_refs_used = protocol_refs_used.union(study_df[protocol_ref_col])
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(
                i_df_dict['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename != '':
                try:
                    with utf8_text_file_open(path.join(dir_context, assay_filename)) as a_fp:
                        assay_df = load_table(a_fp)
                        for protocol_ref_col in [i for i in assay_df.columns if i.startswith('Protocol REF')]:
                            protocol_refs_used = protocol_refs_used.union(assay_df[protocol_ref_col])
                except FileNotFoundError:
                    pass
        diff = protocols_declared - protocol_refs_used - {''}
        if len(diff) > 0:
            spl = "protocols declared in the file {} are not used in any assay file: {}".format(study_filename, diff)
            warning = ("(W) Some protocols declared in the investigation file are not used neither in the study file {}"
                       " nor in any related assay file: {}").format(study_filename, list(diff))
            validator.add_warning(message="Protocol declared but not used", supplemental=spl, code=1019)
            log.warning(warning)


def check_protocol_parameter_usage(i_df_dict, dir_context):
    """Used for rules 1009 and 1020

    :param i_df_dict: A dictionary of  DataFrame and list of Dataframes representing the Investigation file
    :param dir_context: Path to where the investigation file is found
    :return: None
    """
    for i, study_df in enumerate(i_df_dict['studies']):
        protocol_parameters_declared = set()
        protocol_parameters_per_protocol = set(i_df_dict['s_protocols'][i]['Study Protocol Parameters Name'].tolist())
        for protocol_parameters in protocol_parameters_per_protocol:
            parameters_list = protocol_parameters.split(';')
            protocol_parameters_declared = protocol_parameters_declared.union(set(parameters_list))

        # empty string is not a valid protocol parameter
        protocol_parameters_declared = protocol_parameters_declared - {''}
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename != '':
            try:
                protocol_parameters_used = set()
                with utf8_text_file_open(path.join(dir_context, study_filename)) as s_fp:
                    study_df = load_table(s_fp)
                    parameter_value_cols = [i for i in study_df.columns if _RX_PARAMETER_VALUE.match(i)]
                    for col in parameter_value_cols:
                        pv = _RX_PARAMETER_VALUE.findall(col)
                        protocol_parameters_used = protocol_parameters_used.union(set(pv))
                    if not protocol_parameters_used.issubset(protocol_parameters_declared):
                        remain = list(protocol_parameters_used - protocol_parameters_declared)
                        error = ("(E) Some protocol parameters referenced in an study file {} are not declared in the "
                                 "investigation file: {}").format(study_filename, remain)
                        log.error(error)
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(i_df_dict['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename != '':
                try:
                    protocol_parameters_used = set()
                    with utf8_text_file_open(path.join(dir_context, assay_filename)) as a_fp:
                        assay_df = load_table(a_fp)
                        parameter_value_cols = [i for i in assay_df.columns if _RX_PARAMETER_VALUE.match(i)]
                        for col in parameter_value_cols:
                            pv = _RX_PARAMETER_VALUE.findall(col)
                            protocol_parameters_used = protocol_parameters_used.union(set(pv))
                        if not protocol_parameters_used.issubset(protocol_parameters_declared):
                            remain = list(protocol_parameters_used - protocol_parameters_declared)
                            error = ("(E) Some protocol parameters referenced in an assay file {} are not declared in "
                                     "the investigation file: {}").format(assay_filename, remain)
                            log.error(error)
                except FileNotFoundError:
                    pass

        # now collect all protocol parameters in all assays to compare to declared protocol parameters
        protocol_parameters_used = set()
        if study_filename != '':
            try:
                with utf8_text_file_open(path.join(dir_context, study_filename)) as s_fp:
                    study_df = load_table(s_fp)
                    parameter_value_cols = [i for i in study_df.columns if _RX_PARAMETER_VALUE.match(i)]
                    for col in parameter_value_cols:
                        pv = _RX_PARAMETER_VALUE.findall(col)
                        protocol_parameters_used = protocol_parameters_used.union(set(pv))
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(i_df_dict['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename != '':
                try:
                    with utf8_text_file_open(path.join(dir_context, assay_filename)) as a_fp:
                        assay_df = load_table(a_fp)
                        parameter_value_cols = [i for i in assay_df.columns if _RX_PARAMETER_VALUE.match(i)]
                        for col in parameter_value_cols:
                            pv = _RX_PARAMETER_VALUE.findall(col)
                            protocol_parameters_used = protocol_parameters_used.union(set(pv))
                except FileNotFoundError:
                    pass
        if len(protocol_parameters_declared - protocol_parameters_used) > 0:
            warning = ("(W) Some protocol parameters declared in the investigation file are not used in any assay file:"
                       " {}").format(list(protocol_parameters_declared - protocol_parameters_used))
            log.warning(warning)


def check_protocol_names(i_df_dict):
    """Used for rule 1010

    :param ii_df_dict: A dictionary of  DataFrame and list of Dataframes representing the Investigation file
    :return: None
    """
    for study_protocols_df in i_df_dict['s_protocols']:
        for i, protocol_name in enumerate(study_protocols_df['Study Protocol Name'].tolist()):
            # DataFrames labels empty cells as 'Unnamed: n'
            if protocol_name == '' or 'Unnamed: ' in protocol_name:
                validator.add_warning(message="Protocol missing name", supplemental="pos={}".format(i), code=1010)
                warning = "(W) A Protocol at position {} is missing Protocol Name, so can't be referenced in ISA-tab"
                warning = warning.format(i)
                log.warning(warning)


def check_protocol_parameter_names(i_df_dict):
    """Used for rule 1011

    :param i_df_dict: A dictionary of  DataFrame and list of Dataframes representing the Investigation file
    :return: None
    """
    for study_protocols_df in i_df_dict['s_protocols']:
        for i, protocol_parameters_names in enumerate(study_protocols_df['Study Protocol Parameters Name'].tolist()):
            # There's an empty cell if no protocols
            if len(protocol_parameters_names.split(sep=';')) > 1:
                for protocol_parameter_name in protocol_parameters_names.split(sep=';'):
                    if protocol_parameter_name == '' or 'Unnamed: ' in protocol_parameter_name:
                        spl = "Protocol Parameter at pos={}".format(i)
                        warning = ("(W) A Protocol Parameter used in Protocol position {} is missing a Name, "
                                   "so can't be referenced in ISA-tab").format(i)
                        validator.add_warning(message="Protocol Parameter missing name", supplemental=spl, code=1011)
                        log.warning(warning)


def check_study_factor_names(i_df_dict):
    """Used for rule 1012

    :param i_df_dict: A dictionary of  DataFrame and list of Dataframes representing the Investigation file
    :return: None
    """
    for study_factors_df in i_df_dict['s_factors']:
        for i, factor_name in enumerate(study_factors_df['Study Factor Name'].tolist()):
            # DataFrames labels empty cells as 'Unnamed: n'
            if factor_name == '' or 'Unnamed: ' in factor_name:
                spl = "Study Factor pos={}".format(i)
                warning = "(W) A Study Factor at position {} is missing a name, so can't be referenced in ISA-tab"
                warning = warning.format(i)
                validator.add_warning(message="Study Factor missing name", supplemental=spl, code=1012)
                log.warning(warning)


def check_unit_field(table, cfg):
    """Checks if unit columns are valid against a configuration

    :param table: Table DataFrame
    :param cfg: An ISA Configuration object
    :return: True if all unit columns in table are OK, False if not OK
    """

    def check_unit_value(cell_value, unit_value, cfield, filename):
        """Checks if a value cell that has a unit has correct unit columns
        according to the configuration

        :param cell_value: The cell value
        :param unit_value: The unit value
        :param cfield: Configuration field from the ISA Config
        :param filename: Filename of the table
        :return: True if the unit cells are OK, False if not
        """
        if cell_has_value(cell_value) or cell_has_value(unit_value):
            local_spl = "Field '{}' has a unit but not a value in the file '{}'".format(cfield.header, filename)
            validator.add_warning(message="Cell found has unit but no value", supplemental=local_spl, code=4999)
            log.warning("(W) {}".format(spl))
            return False
        return True

    result = True
    for icol, header in enumerate(table.columns):
        cfields = [i for i in cfg.get_isatab_configuration()[0].get_field() if i.header == header]
        if len(cfields) != 1:
            continue
        cfield = cfields[0]
        ucfields = [i for i in cfg.get_isatab_configuration()[0].get_unit_field() if i.pos == cfield.pos + 1]
        if len(ucfields) != 1:
            continue
        ucfield = ucfields[0]
        if ucfield.is_required:
            rheader = None
            rindx = icol + 1
            if rindx < len(table.columns):
                rheader = table.columns[rindx]
            if rheader is None or rheader.lower() != 'unit':
                spl = "The field '{}' in the file '{}' misses a required 'Unit' column".format(header, table.filename)
                validator.add_warning(message="Cell requires a Unit", supplemental=spl, code=4999)
                log.warning("(W) {}".format(spl))
                result = False
            else:
                for irow in range(len(table.index)):
                    check = check_unit_value(table.iloc[irow][icol], table.iloc[irow][rindx], cfield, table.filename)
                    result = result and check
    return result
