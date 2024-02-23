from math import isnan
import iso8601

from isatools.io import isatab_configurator
from isatools.isatab.validate.store import validator
from isatools.isatab.defaults import (
    log,
    _RX_INDEXED_COL,
    _RX_CHARACTERISTICS,
    _RX_PARAMETER_VALUE,
    _RX_FACTOR_VALUE,
    _RX_COMMENT
)


def check_investigation_against_config(i_df, configs, no_config):
    """Checks investigation file against the loaded configurations

    :param i_df_dict: A dictionary of DataFrames and lists of DataFrames representing the investigation file
    :param configs: A dictionary of ISA Configuration objects
    :param no_config: whether or not to validate against configs
    :return: None
    """

    code = 4003
    message = "A required property is missing"

    def add_warning(index, column, value_index):
        if index > 0:
            spl = "A property value in {}.{} of investigation file at column {} is required"
            spl = spl.format(column, index + 1, value_index + 1)
            validator.add_warning(message=message, supplemental=spl, code=code)
            log.warning("(W) {}".format(spl))
        else:
            spl = "A property value in {} of investigation file at column {} is required"
            spl = spl.format(column, value_index + 1)
            validator.add_warning(message=message, supplemental=spl, code=code)
            log.warning("(W) {}".format(spl))

    def check_section_against_required_fields_one_value(section, required, i=0):
        fields_required = [i for i in section.columns if i in required]
        for col in fields_required:
            required_values = section[col]
            if len(required_values) > 0:
                for x, required_value in enumerate(required_values):
                    required_value = required_values.iloc[x]
                    if isinstance(required_value, float):
                        if isnan(required_value):
                            add_warning(i, col, x)
                    else:
                        if required_value == '' or 'Unnamed: ' in required_value:
                            add_warning(i, col, x)

    if ('[investigation]', '') in configs and not no_config:
        config_fields = configs[('[investigation]', '')].get_isatab_configuration()[0].get_field()
        required_fields = [i.header for i in config_fields if i.is_required]
        check_section_against_required_fields_one_value(i_df['investigation'], required_fields)
        check_section_against_required_fields_one_value(i_df['i_publications'], required_fields)
        check_section_against_required_fields_one_value(i_df['i_contacts'], required_fields)

        for x, study_df in enumerate(i_df['studies']):
            check_section_against_required_fields_one_value(i_df['studies'][x], required_fields, x)
            check_section_against_required_fields_one_value(i_df['s_design_descriptors'][x], required_fields, x)
            check_section_against_required_fields_one_value(i_df['s_publications'][x], required_fields, x)
            check_section_against_required_fields_one_value(i_df['s_factors'][x], required_fields, x)
            check_section_against_required_fields_one_value(i_df['s_assays'][x], required_fields, x)
            check_section_against_required_fields_one_value(i_df['s_protocols'][x], required_fields, x)
            check_section_against_required_fields_one_value(i_df['s_contacts'][x], required_fields, x)


def load_config(config_dir, no_config):
    """Rule 4001

    :param config_dir: Path to a directory containing ISA Configuration XMLs
    :param no_config: whether or not to validate against configs
    :return: A dictionary of ISA Configuration objects
    """
    if no_config:
        return {}

    configs = None
    try:
        configs = isatab_configurator.load(config_dir)
    except FileNotFoundError:
        spl = "On loading {}".format(config_dir)
        validator.add_error(message="Configurations could not be loaded", supplemental=spl, code=4001)
        log.error("(E) FileNotFoundError on trying to load from {}".format(config_dir))
    if not configs:
        spl = "On loading {}".format(config_dir)
        validator.add_warning(message="Configurations could not be loaded", supplemental=spl, code=4001)
        log.warning("(W) No configurations were loaded from the '{}' directory".format(config_dir))
    else:
        for k in configs.keys():
            message = "Loaded table configuration '{}' for measurement and technology {}"
            log.debug(message.format(str(configs[k].get_isatab_configuration()[0].table_name), str(k)))
    return configs


def check_measurement_technology_types(i_df, configs, no_config):
    """Rule 4002

    :param i_df_dict: A dictionary of DataFrames and lists of DataFrames representing the investigation file
    :param configs: A dictionary of ISA Configuration objects
    :param no_config: whether or not to validate against configs
    :return: None
    """
    if no_config:
        return

    for i, assay_df in enumerate(i_df['s_assays']):
        measurement_types = assay_df['Study Assay Measurement Type'].tolist()
        technology_types = assay_df['Study Assay Technology Type'].tolist()
        if len(measurement_types) == len(technology_types):
            for x, measurement_type in enumerate(measurement_types):
                lowered_mt = measurement_types[x].lower()
                lowered_tt = technology_types[x].lower()
                if (lowered_mt, lowered_tt) not in configs.keys():
                    spl = "Measurement {}/technology {}, STUDY.{}, STUDY ASSAY.{}"
                    spl = spl.format(measurement_types[x], technology_types[x], i, x)
                    error = ("(E) Could not load configuration for measurement type '{}' and technology type '{}' "
                             "for STUDY.{}, STUDY ASSAY.{}'").format(measurement_types[x], technology_types[x], i, x)
                    validator.add_error(message="Measurement/technology type invalid", supplemental=spl, code=4002)
                    log.error(error)


def check_factor_value_presence(table):
    """Checks if a Factor Value cell is empty

    :param table: Table as a DataFrame
    :return: None
    """
    factor_fields = [i for i in table.columns if i.lower().startswith('factor value')]
    for factor_field in factor_fields:
        for x, cell_value in enumerate(table.fillna('')[factor_field]):
            if cell_value == '':
                msg = "A required node factor value is missing value"
                spl = "Missing value for '{}' at row {} in {}".format(factor_field, str(x), table.filename)
                validator.add_warning(message=msg, supplemental=spl, code=4007)
                log.warning("(W) {}".format(spl))


def check_required_fields(table, cfg, no_config):
    """Checks if the required fields by a configuration have empty cells

    :param table: Table as a DataFrame
    :param cfg: A ISA Configuration object
    :param no_config: whether or not to validate against configs
    :return: None
    """
    if cfg.get_isatab_configuration() and not no_config:
        for fheader in [i.header for i in cfg.get_isatab_configuration()[0].get_field() if i.is_required]:
            found_field = [i for i in table.columns if i.lower() == fheader.lower()]
            if len(found_field) == 0:
                msg = "A required column in assay table is not present"
                spl = "Required field '{}' not found in the file '{}'".format(fheader, table.filename)
                validator.add_warning(message=msg, supplemental=spl, code=4010)
                log.warning("(W) {}".format(spl))
            elif len(found_field) > 1:
                spl = "Field '{}' cannot have multiple values in the file '{}'".format(fheader, table.filename)
                validator.add_warning(message="Multiple columns found", supplemental=spl, code=4013)
                log.warning("(W) {}".format(spl))


def check_field_values(table, cfg, no_config):
    """Checks table fields against configuration

    :param table: Table DataFrame
    :param cfg: A ISA Configuration object
    :param no_config: whether or not to validate against configs
    :return: None
    """

    def check_single_field(cell_value, cfg_field):
        """Checks a single cell against the configuration field required

        :param cell_value: Value taken from a table cell
        :param cfg_field: Field configuration
        :return: Returns True if OK, False if not OK
        """

        spl = "Missing value for the required field '{}' in the file '{}'".format(cfg_field.header, table.filename)
        warning = "(W) {}".format(spl)

        # First check if the value is required by config
        if isinstance(cell_value, float):
            if isnan(cell_value):
                if cfg_field.is_required:
                    msg = "A required column in assay table is not present"
                    validator.add_warning(message=msg, supplemental=spl, code=4010)
                    log.warning(warning)
            return True
        elif isinstance(cell_value, str):
            value = cell_value.strip()
            if value == '':
                if cfg_field.is_required:
                    validator.add_warning(message="A required cell value is missing", supplemental=spl, code=4012)
                    log.warning(warning)
                return True
        is_valid_value = True
        data_type = cfg_field.data_type.lower().strip()
        if data_type in ['', 'string']:
            return True
        if 'boolean' == data_type:
            is_valid_value = 'true' == cell_value.strip() or 'false' == cell_value.strip()
        elif 'date' == data_type:
            try:
                iso8601.parse_date(cell_value)
            except iso8601.ParseError:
                is_valid_value = False
        elif 'integer' == data_type:
            try:
                int(cell_value)
            except ValueError:
                is_valid_value = False
        elif 'double' == data_type:
            try:
                float(cell_value)
            except ValueError:
                is_valid_value = False
        elif data_type == 'list':
            list_values = [i.lower() for i in cfg_field.list_values.split(',')]
            if cell_value.lower() not in list_values:
                is_valid_value = False
        elif data_type in ['ontology-term', 'ontology term']:
            # Structure and values checked in check_ontology_fields()
            return True
        else:
            spl = "Unknown data type '{}' for field '{}' in the file '{}'"
            spl = spl.format(data_type, cfg_field.header, table.filename)
            validator.add_warning(message="Unknown data type found", supplemental=spl, code=4011)
            log.warning("(W) {}".format(spl))
            return False
        if not is_valid_value:
            msg = "A value does not correspond to the correct data type"
            spl = "Invalid value '{}' for type '{}' of the field '{}'"
            spl = spl.format(cell_value, data_type, cfg_field.header)
            validator.add_warning(message=msg, supplemental=spl, code=4011)
            log.warning("(W) {}".format(spl))
            if data_type == 'list':
                log.warning("(W) Value must be one of: " + cfg_field.list_values)
        return is_valid_value

    if cfg.get_isatab_configuration() and not no_config:
        for irow in range(len(table.index)):
            ncols = len(table.columns)
            for icol in range(0, ncols):
                cfields = [i for i in cfg.get_isatab_configuration()[0].get_field() if i.header == table.columns[icol]]
                if len(cfields) == 1:
                    cfield = cfields[0]
                    check_single_field(table.iloc[irow][cfield.header], cfield)


def check_protocol_fields(table, cfg, proto_map, no_config):
    from itertools import tee

    def pairwise(iterable):
        """A lovely pairwise iterator, e.g.

        [a, b, c, d] -> [(a, b), (b, c), (c, d)]

        :param iterable: A Python iterable
        :return: A pairwise generator
        """
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    field_headers = [i for i in table.columns
                     if i.lower().endswith(' name')
                     or i.lower().endswith(' data file')
                     or i.lower().endswith(' data matrix file')]
    protos = [i for i in table.columns if i.lower() == 'protocol ref']
    if len(protos) > 0:
        last_proto_index = table.columns.get_loc(protos[len(protos) - 1])
    else:
        last_proto_index = -1
    last_mat_or_dat_index = table.columns.get_loc(field_headers[len(field_headers) - 1])
    if last_proto_index > last_mat_or_dat_index:
        spl = "(W) Protocol REF column is not followed by a material or data node in file '" + table.filename + "'"
        validator.add_warning(message="Missing Protocol Value", supplemental=spl, code=1007)
        log.warning(spl)
    if cfg.get_isatab_configuration() and not no_config:
        for left, right in pairwise(field_headers):
            cleft = None
            cright = None
            clefts = [i for i in cfg.get_isatab_configuration()[0].get_field() if i.header.lower() == left.lower()]
            if len(clefts) == 1:
                cleft = clefts[0]
            crights = [i for i in cfg.get_isatab_configuration()[0].get_field() if i.header.lower() == right.lower()]
            if len(crights) == 1:
                cright = crights[0]
            if cleft is not None and cright is not None:
                protocols_fields = cfg.get_isatab_configuration()[0].get_protocol_field()
                cprotos = [i.protocol_type for i in protocols_fields if cleft.pos < i.pos < cright.pos]
                raw_headers = table.columns[table.columns.get_loc(cleft.header):table.columns.get_loc(cright.header)]
                fprotos_headers = [i for i in raw_headers if 'protocol ref' in i.lower()]
                fprotos = list()
                for header in fprotos_headers:
                    proto_names = list(table.loc[:, header].unique())
                    for proto_name in proto_names:
                        proto_type = proto_map.get(proto_name)
                        if not proto_type and proto_name:
                            spl = ("Could not find protocol type for protocol name '{}' in file '{}'" ).format(proto_name, table.filename)
                            validator.add_warning(message="Missing Protocol Declaration", supplemental=spl, code=1007)
                            log.warning("(W) {}".format(spl))
                        else:
                            fprotos.append(proto_type)
                invalid_protos = set(cprotos) - set(fprotos)
                if len(invalid_protos) > 0:
                    spl = ("Protocol(s) of type {} defined in the ISA-configuration expected as a between '{}' and "
                           "'{}' but has not been found, in the file '{}'")
                    spl = spl.format(str(list(invalid_protos)), cleft.header, cright.header, table.filename)
                    validator.add_warning(message="Missing Protocol declaration", supplemental=spl, code=1007)
                    log.warning("(W) {}".format(spl))


def load_table_checks(df, filename):
    """Checks that a table can be loaded and returns the loaded table, if
    successful

    :param df: Study dataFrame
    :param filename: Name of the file
    :return: DataFrame of the study or assay table
    """
    columns = df.columns
    for x, column in enumerate(columns):  # check if columns have valid labels
        if _RX_INDEXED_COL.match(column):
            column = column[:column.rfind('.')]
        if (column not in [
            'Source Name',
            'Sample Name',
            'Term Source REF',
            'Protocol REF',
            'Term Accession Number',
            'Unit',
            'Assay Name',
            'Extract Name',
            'Raw Data File',
            'Material Type',
            'MS Assay Name',
            'NMR Assay Name',
            'Raw Spectral Data File',
            'Labeled Extract Name',
            'Label', 'Hybridization Assay Name',
            'Array Design REF',
            'Scan Name',
            'Array Data File',
            'Protein Assignment File',
            'Peptide Assignment File',
            'Post Translational Modification Assignment File',
            'Data Transformation Name',
            'Derived Data File',
            'Derived Spectral Data File',
            'Normalization Name',
            'Derived Array Data File',
            'Image File',
            "Free Induction Decay Data File",
            'Metabolite Assignment File',
            "Performer",
            "Date",
            "Array Data Matrix File",
            'Free Induction Decay File',
            "Derived Array Data Matrix File",
            'Acquisition Parameter Data File'
        ]) \
                and not _RX_CHARACTERISTICS.match(column) \
                and not _RX_PARAMETER_VALUE.match(column) \
                and not _RX_FACTOR_VALUE.match(column) \
                and not _RX_COMMENT.match(column):
            error_msg = "Unrecognised column heading {} at column position {} in table file {}".format(column, x,
                                                                                                       filename)
            log.error(error_msg)
            error = {
                "message": "Unrecognised header",
                "supplemental": error_msg,
                "code": 4014
            }
            validator.add_error(**error)

        if _RX_COMMENT.match(column):
            if len(_RX_COMMENT.findall(column)) == 0:
                log.warning("(W) In file {}, label {} is missing a name".format(filename, column))
                warning = {
                    "message": "Missing name in Comment[] label",
                    "supplemental": "In file {}, label {} is missing a name".format(filename, column),
                    "code": 4014
                }
                validator.add_warning(**warning)
        if _RX_CHARACTERISTICS.match(column):
            if len(_RX_CHARACTERISTICS.findall(column)) == 0:
                log.warning("(W) In file {}, label {} is missing a name".format(filename, column))
                warning = {
                    "message": "Missing name in Characteristics[] label",
                    "supplemental": "In file {}, label {} is missing a name".format(filename, column),
                    "code": 4014
                }
                validator.add_warning(**warning)
        if _RX_PARAMETER_VALUE.match(column):
            if len(_RX_PARAMETER_VALUE.findall(column)) == 0:
                log.warning("(W) In file {}, label {} is missing a name".format(filename, column))
                warning = {
                    "message": "Missing name in Parameter Value[] label",
                    "supplemental": "In file {}, label {} is missing a name".format(filename, column),
                    "code": 4014
                }
                validator.add_warning(**warning)
        if _RX_FACTOR_VALUE.match(column):
            if len(_RX_FACTOR_VALUE.findall(column)) == 0:
                log.warning("(W) In file {}, label {} is missing a name".format(filename, column))
                warning = {
                    "message": "Missing name in Factor Value[] label",
                    "supplemental": "In file {}, label {} is missing a name".format(filename, column),
                    "code": 4014
                }
                validator.add_warning(**warning)
    norm_columns = list()
    for x, column in enumerate(columns):
        if _RX_INDEXED_COL.match(column):
            norm_columns.append(column[:column.rfind('.')])
        else:
            norm_columns.append(column)
    allowed_fields = [
        'Source Name',
        'Sample Name',
        'Protocol REF',
        'Extract Name',
        'Labeled Extract Name',
        'Raw Data File',
        'Raw Spectral Data File',
        'Array Data File',
        'Protein Assignment File',
        'Peptide Assignment File',
        'Post Translational Modification Assignment File',
        'Derived Data File',
        'Derived Spectral Data File',
        'Derived Array Data File'
    ]
    object_index = [i for i, x in enumerate(norm_columns)
                    if x in allowed_fields
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
        elif prop_name in [
            'Raw Data File',
            'Derived Data File',
            'Derived Spectral Data File',
            'Derived Array Data File',
            'Array Data File',
            'Raw Spectral Data File',
            'Protein Assignment File',
            'Peptide Assignment File',
            'Post Translational Modification Assignment File'
        ]:
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
