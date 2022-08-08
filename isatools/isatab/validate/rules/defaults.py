from isatools.isatab.validate.rules.rules_00xx import check_table_files_read, check_sample_names
from isatools.isatab.validate.rules.rules_10xx import (
    check_samples_not_declared_in_study_used_in_assay as sample_not_declared,
    check_study_factor_usage,
    check_protocol_usage,
    check_protocol_parameter_usage,
    check_protocol_names,
    check_protocol_parameter_names,
    check_study_factor_names,
    check_unit_field
)
from isatools.isatab.validate.rules.rules_30xx import (
    check_dois,
    check_date_formats,
    check_pubmed_ids_format,
    check_ontology_sources,
    check_ontology_fields
)
from isatools.isatab.validate.rules.rules_40xx import (
    check_measurement_technology_types,
    check_investigation_against_config,
    check_factor_value_presence,
    check_required_fields,
    check_field_values,
    check_protocol_fields,
    load_config,
    load_table_checks
)
from isatools.isatab.validate.rules.rules_50xx import check_study_groups


INVESTIGATION_RULES_MAPPING = [
    {'rule': check_table_files_read, 'params': ['investigation_df', 'dir_context'], 'identifier': '0006'},

    {'rule': sample_not_declared, 'params': ['investigation_df', 'dir_context'], 'identifier': '1003'},
    {'rule': check_protocol_usage, 'params': ['investigation_df', 'dir_context'], 'identifier': '1007'},
    {'rule': check_study_factor_usage, 'params': ['investigation_df', 'dir_context'], 'identifier': '1008'},
    {'rule': check_protocol_parameter_usage, 'params': ['investigation_df', 'dir_context'], 'identifier': '1009'},
    {'rule': check_protocol_names, 'params': ['investigation_df'], 'identifier': '1010'},
    {'rule': check_protocol_parameter_names, 'params': ['investigation_df'], 'identifier': '1011'},
    {'rule': check_study_factor_names, 'params': ['investigation_df'], 'identifier': '1012'},

    {'rule': check_date_formats, 'params': ['investigation_df'], 'identifier': '3001'},
    {'rule': check_dois, 'params': ['investigation_df'], 'identifier': '3002'},
    {'rule': check_pubmed_ids_format, 'params': ['investigation_df'], 'identifier': '3003'},
    {'rule': check_ontology_sources, 'params': ['investigation_df'], 'identifier': '3008'},

    {'rule': load_config, 'params': ['configs'], 'identifier': '4001'},
    {'rule': check_measurement_technology_types, 'params': ['investigation_df', 'configs'], 'identifier': '4002'},
    {'rule': check_investigation_against_config, 'params': ['investigation_df', 'configs'], 'identifier': '4003'},

    # copies
    {'rule': check_table_files_read, 'params': ['investigation_df', 'dir_context'], 'identifier': '0008'},
    {'rule': check_protocol_usage, 'params': ['investigation_df', 'dir_context'], 'identifier': '1019'},
    {'rule': check_protocol_parameter_usage, 'params': ['investigation_df', 'dir_context'], 'identifier': '1020'},
    {'rule': check_study_factor_usage, 'params': ['investigation_df', 'dir_context'], 'identifier': '1021'},
]

STUDY_RULES_MAPPING = [

    {'rule': check_unit_field, 'params': ['study_sample_table', 'config'], 'identifier': '1099'},

    {
        'rule': check_ontology_fields,
        'params': ['study_sample_table', 'config', 'term_source_refs'],
        'identifier': '3010'
    },

    {'rule': check_required_fields, 'params': ['study_sample_table', 'config'], 'identifier': '4003'},
    {'rule': check_factor_value_presence, 'params': ['study_sample_table'], 'identifier': '4007'},
    {
        'rule': check_protocol_fields,
        'params': ['study_sample_table', 'config', 'protocol_names_and_types'],
        'identifier': '4009'
    },
    {'rule': check_field_values, 'params': ['study_sample_table', 'config'], 'identifier': '4011'},
    {'rule': load_table_checks, 'params': ['study_sample_table'], 'identifier': '4014'},

    {
        'rule': check_study_groups,
        'params': ['study_sample_table', 'study_filename', 'study_group_size_in_comment'],
        'identifier': '5001'
    },

    # copies
    {'rule': check_required_fields, 'params': ['study_sample_table', 'config'], 'identifier': '4008'},
    {'rule': check_required_fields, 'params': ['study_sample_table', 'config'], 'identifier': '4010'},
]

ASSAY_RULES_MAPPING = [
    {'rule': check_sample_names, 'params': ['study_sample_table', 'assay_tables'], 'identifier': '0000'},

    {'rule': check_unit_field, 'params': ['assay_table', 'config'], 'identifier': '1099'},

    {'rule': check_ontology_fields, 'params': ['assay_table', 'config', 'term_source_refs'], 'identifier': '3010'},

    {'rule': check_required_fields, 'params': ['assay_table', 'config'], 'identifier': '4003'},
    {'rule': check_factor_value_presence, 'params': ['assay_table'], 'identifier': '4007'},
    {
        'rule': check_protocol_fields,
        'params': ['assay_table', 'config', 'protocol_names_and_types'],
        'identifier': '4009'
    },
    {'rule': check_field_values, 'params': ['assay_table', 'config'], 'identifier': '4011'},
    {'rule': load_table_checks, 'params': ['assay_table'], 'identifier': '4014'},

    # copies
    {'rule': check_required_fields, 'params': ['study_sample_table', 'config'], 'identifier': '4008'},
    {'rule': check_required_fields, 'params': ['study_sample_table', 'config'], 'identifier': '4010'},

    {
        'rule': check_study_groups,
        'params': ['assay_table', 'assay_filename', 'study_group_size_in_comment'],
        'identifier': '5001'
    }
]


# ORDER MATTERS IN THE DEFAULTS RULES!
DEFAULT_INVESTIGATION_RULES = (
    '4001',
    '0006', '1003', '1007', '1008', '1009', '1010', '1011', '1012', '3001', '3002', '3003', '3008', '4002', '4003'
)
DEFAULT_STUDY_RULES = ('4014', '4007', '4003', '4011', '1099', '4009', '3010', '5001')
DEFAULT_ASSAY_RULES = ('4014', '4007', '4003', '4011', '1099', '4009', '3010', '0000', '5001')
