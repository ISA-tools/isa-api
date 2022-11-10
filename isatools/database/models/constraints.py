from sqlalchemy import CheckConstraint


def build_comment_constraints():
    fields = (
        'investigation_id', 'study_id', 'person_id', 'process_id', 'publication_id', 'ontology_source_id',
        'ontology_annotation_id', "protocol_id", "source_id", "characteristic_id", "study_factor_id", "sample_id",
        "factor_value_id"
    )
    statement = make_must_have_one_only_statement(fields)
    return CheckConstraint(statement, name='comment_must_have_one_source_only')


def build_person_constraints():
    fields = ('investigation_id', 'study_id')
    statement_two = ' OR '.join([field + ' IS NOT NULL' for field in fields])
    return CheckConstraint(statement_two, name='person_has_at_least_one_source')


def build_characteristic_constraints():
    value_statement = 'NOT (value_int IS NOT NULL AND value_id IS NOT NULL)'
    value_constraints = CheckConstraint(value_statement, name='characteristic_must_have_one_value_only')

    unit_statement = 'NOT (unit_str IS NOT NULL AND unit_id IS NOT NULL)'
    unit_constraints = CheckConstraint(unit_statement, name='characteristic_cant_have_more_than_one_unit')

    unit_statement_two = 'NOT (value_id IS NOT NULL AND (unit_str IS NOT NULL OR unit_id IS NOT NULL))'
    unit_constraints_two = CheckConstraint(unit_statement_two, name='characteristic_cant_have_unit_if_value_is_OA')

    return value_constraints, unit_constraints, unit_constraints_two


def build_factor_value_constraints():
    statement = 'NOT (value_int IS NOT NULL AND value_oa_id IS NOT NULL AND value_str IS NOT NULL)'
    return CheckConstraint(statement, name='factor_value_must_have_one_value_only')


def make_must_have_one_only_statement(fields):
    statement_one = 'NOT (%s) ' % ' AND '.join([field + ' IS NOT NULL' for field in fields])
    statement_two = ' AND (%s) ' % ' OR '.join([field + ' IS NOT NULL' for field in fields])
    return '%s %s' % (statement_one, statement_two)
