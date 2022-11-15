from typing import Tuple

from sqlalchemy import CheckConstraint


def build_comment_constraints() -> CheckConstraint:
    """ Builds the constraints for the Comment model.

    :return: A CheckConstraint object used to validate the Comment table.
    """
    fields = (
        'investigation_id', 'study_id', 'person_id', 'process_id', 'publication_id', 'ontology_source_id',
        'ontology_annotation_id', "protocol_id", "source_id", "characteristic_id", "study_factor_id", "sample_id",
        "factor_value_id", "material_id", "assay_id", "datafile_id"
    )
    statement_one = 'NOT (%s) ' % ' AND '.join([field + ' IS NOT NULL' for field in fields])
    statement_two = ' AND (%s) ' % ' OR '.join([field + ' IS NOT NULL' for field in fields])
    statement = '%s %s' % (statement_one, statement_two)
    return CheckConstraint(statement, name='comment_must_have_one_source_only')


def build_characteristic_constraints() -> Tuple[CheckConstraint, CheckConstraint, CheckConstraint]:
    """ Builds the constraints for the Characteristic model.

    :return: A tuple of CheckConstraint objects used to validate the Characteristic table.
    """
    value_statement = 'NOT (value_int IS NOT NULL AND value_id IS NOT NULL)'
    value_constraints = CheckConstraint(value_statement, name='characteristic_must_have_one_value_only')

    unit_statement = 'NOT (unit_str IS NOT NULL AND unit_id IS NOT NULL)'
    unit_constraints = CheckConstraint(unit_statement, name='characteristic_cant_have_more_than_one_unit')

    unit_statement_two = 'NOT (value_id IS NOT NULL AND (unit_str IS NOT NULL OR unit_id IS NOT NULL))'
    unit_constraints_two = CheckConstraint(unit_statement_two, name='characteristic_cant_have_unit_if_value_is_OA')

    return value_constraints, unit_constraints, unit_constraints_two


def build_factor_value_constraints() -> CheckConstraint:
    """ Builds the constraints for the FactorValue model.

    :return: A CheckConstraint object used to validate the FactorValue table.
    """
    statement = 'NOT (value_int IS NOT NULL AND value_oa_id IS NOT NULL AND value_str IS NOT NULL)'
    return CheckConstraint(statement, name='factor_value_must_have_one_value_only')


def build_material_constraints() -> CheckConstraint:
    """ Builds the constraints for the Material model.

    :return: A CheckConstraint object used to validate the Material table.
    """
    statement = '''NOT (material_type IS NOT NULL 
                AND material_type != "Extract Name" AND material_type != "Labeled Extract Name")'''
    return CheckConstraint(statement, name='material_type_must_be_extract_name_or_labeled_extract_name')
