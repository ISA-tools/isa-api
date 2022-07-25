from math import isnan
import iso8601

from isatools.io import isatab_configurator
from isatools.isatab.validate.store import validator
from isatools.isatab.defaults import log


def check_investigation_against_config(i_df, configs):
    """Checks investigation file against the loaded configurations

    :param i_df: An investigation DataFrame
    :param configs: A dictionary of ISA Configuration objects
    :return: None
    """

    def check_section_against_required_fields_one_value(section, required, i=0):
        code = 4003
        fields_required = [i for i in section.columns if i in required]
        for col in fields_required:
            required_values = section[col]
            if len(required_values) > 0:
                for x, required_value in enumerate(required_values):
                    required_value = required_values.iloc[x]
                    if isinstance(required_value, float):
                        if isnan(required_value):
                            if i > 0:
                                spl = "A property value in {}.{} of investigation file at column {} is required"
                                spl = spl.format(col, i + 1, x + 1)
                                warning = "(W) A property value in {}.{} of investigation file at column {} is required"
                                warning = warning.format(col, i + 1, x + 1)
                                validator.add_warning(message="A required property is missing",
                                                      supplemental=spl,
                                                      code=code)
                                log.warning(warning)
                            else:
                                spl = "A property value in {} of investigation file at column {} is required"
                                spl = spl.format(col, x + 1)
                                warning = "(W) A property value in {} of  investigation file at column {} is required"
                                warning = warning.format(col, x + 1)
                                validator.add_warning(message="A required property is missing",
                                                      supplemental=spl,
                                                      code=code)
                                log.warning(warning)
                    else:
                        if required_value == '' or 'Unnamed: ' in required_value:
                            if i > 0:
                                spl = "A property value in {}.{} of investigation file at column {} is required"
                                spl = spl.format(col, i + 1, x + 1)
                                warning = "(W) A property value in {}.{} of investigation file at column {} is required"
                                warning = warning.format(col, i + 1, x + 1)
                                validator.add_warning(message="A required property is missing",
                                                      supplemental=spl,
                                                      code=code)
                                log.warning(warning)
                            else:
                                spl = "A property value in {} of investigation file at column {} is required"
                                spl = spl.format(col, x + 1)
                                warning = "(W) A property value in {} of investigation file at column {} is required"
                                warning = warning.format(col, x + 1)
                                validator.add_warning(message="A required property is missing",
                                                      supplemental=spl,
                                                      code=code)
                                log.warning(warning)

    required_fields = [
        i.header for i in configs[('[investigation]', '')].get_isatab_configuration()[0].get_field()
        if i.is_required
    ]
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


def load_config(config_dir):
    """Rule 4001

    :param config_dir: Path to a directory containing ISA Configuration XMLs
    :return: A dictionary of ISA Configuration objects
    """
    configs = None
    try:
        configs = isatab_configurator.load(config_dir)
    except FileNotFoundError:
        spl = "On loading {}".format(config_dir)
        validator.add_error(message="Configurations could not be loaded", supplemental=spl, code=4001)
        log.error("(E) FileNotFoundError on trying to load from {}".format(config_dir))
    if configs is None:
        spl = "On loading {}".format(config_dir)
        validator.add_error(message="Configurations could not be loaded", supplemental=spl, code=4001)
        log.error("(E) Could not load configurations from {}".format(config_dir))
    else:
        for k in configs.keys():
            message = "Loaded table configuration '{}' for measurement and technology {}"
            message = message.format(str(configs[k].get_isatab_configuration()[0].table_name), str(k))
            log.debug(message)
    return configs


def check_measurement_technology_types(i_df, configs):
    """Rule 4002

    :param i_df: An investigation DataFrame
    :param configs: A dictionary of ISA Configuration objects
    :return: None
    """
    for i, assay_df in enumerate(i_df['s_assays']):
        measurement_types = assay_df['Study Assay Measurement Type'].tolist()
        technology_types = assay_df['Study Assay Technology Type'].tolist()
        if len(measurement_types) == len(technology_types):
            for x, measurement_type in enumerate(measurement_types):
                lowered_mt = measurement_types[x].lower()
                lowered_tt = technology_types[x].lower()
                if (lowered_mt, lowered_tt) not in configs.keys():
                    spl = "Measurement {}/technology {}, STUDY ASSAY.{}"
                    spl = spl.format(measurement_types[x], technology_types[x], i)
                    error = ("(E) Could not load configuration for measurement type '{}' and technology type '{}' "
                             "for STUDY ASSAY.{}'").format(measurement_types[x], technology_types[x], i)
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
                spl = "(W) Missing value for '" + factor_field + "' at row " + str(x) + " in " + table.filename
                warning = "(W) Missing value for '" + factor_field + "' at row " + str(x) + " in " + table.filename
                validator.add_warning(message=msg, supplemental=spl, code=4007)
                log.warning(warning)


def check_required_fields(table, cfg):
    """Checks if the required fields by a configuration have empty cells

    :param table: Table as a DataFrame
    :param cfg: A ISA Configuration object
    :return: None
    """
    for fheader in [i.header for i in cfg.get_isatab_configuration()[0].get_field() if i.is_required]:
        found_field = [i for i in table.columns if i.lower() == fheader.lower()]
        if len(found_field) == 0:
            msg = "A required column in assay table is not present"
            spl = "Required field '" + fheader + "' not found in the file '" + table.filename + "'"
            warning = "(W) Required field '" + fheader + "' not found in the file '" + table.filename + "'"
            validator.add_warning(message=msg, supplemental=spl, code=4010)
            log.warning(warning)
        elif len(found_field) > 1:
            spl = "Field '" + fheader + "' cannot have multiple values in the file '" + table.filename
            warning = "(W) Field '" + fheader + "' cannot have multiple values in the file '" + table.filename
            validator.add_warning(message="Multiple columns found", supplemental=spl, code=4013)
            log.warning(warning)


def check_field_values(table, cfg):
    """Checks table fields against configuration

    :param table: Table DataFrame
    :param cfg: A ISA Configuration object
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

    result = True
    for irow in range(len(table.index)):
        ncols = len(table.columns)
        for icol in range(0, ncols):
            cfields = [i for i in cfg.get_isatab_configuration()[0].get_field() if i.header == table.columns[icol]]
            if len(cfields) == 1:
                cfield = cfields[0]
                result = result and check_single_field(table.iloc[irow][cfield.header], cfield)
    return result


def check_protocol_fields(table, cfg, proto_map):
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

    proto_ref_index = [i for i in table.columns if 'protocol ref' in i.lower()]
    result = True
    for each in proto_ref_index:
        prots_found = set()
        for cell in table[each]:
            prots_found.add(cell)
        if len(prots_found) > 1:
            log.warning("(W) Multiple protocol references {} are found in {}".format(prots_found, each))
            log.warning("(W) Only one protocol reference should be used in a Protocol REF column.")
            result = False
    if result:
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
            log.warning("(W) Protocol REF column without output in file '" + table.filename + "'")
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
                cprotos = [i.protocol_type for i in cfg.get_isatab_configuration()[0].get_protocol_field()
                           if cleft.pos < i.pos < cright.pos]
                raw_headers = table.columns[table.columns.get_loc(cleft.header):table.columns.get_loc(cright.header)]
                fprotos_headers = [i for i in raw_headers if 'protocol ref' in i.lower()]
                fprotos = list()
                for header in fprotos_headers:
                    proto_name = table.iloc[0][header]
                    try:
                        proto_type = proto_map[proto_name]
                        fprotos.append(proto_type)
                    except KeyError:
                        spl = ("Could not find protocol type for protocol name '{}', trying to validate against name "
                               "only").format(proto_name)
                        validator.add_warning(message="Missing Protocol declaration", supplemental=spl, code=1007)
                        log.warning("(W) {}".format(spl))
                        fprotos.append(proto_name)
                invalid_protos = set(cprotos) - set(fprotos)
                if len(invalid_protos) > 0:
                    spl = ("Protocol(s) of type {} defined in the ISA-configuration expected as a between '{}' and "
                           "'{}' but has not been found, in the file '{}'")
                    spl = spl.format(str(list(invalid_protos)), cleft.header, cright.header, table.filename)
                    validator.add_warning(message="Missing Protocol declaration", supplemental=spl, code=1007)
                    log.warning("(W) {}".format(spl))
                    result = False
    return result
