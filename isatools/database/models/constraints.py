from sqlalchemy import CheckConstraint


def build_comment_constraints():
    fields = (
        'investigation_id', 'study_id', 'person_id', 'process_id', 'publication_id', 'ontology_source_id',
        'ontology_annotation_id', "protocol_id", "source_id"
    )
    statement_one = 'NOT (%s) ' % ' AND '.join([field + ' IS NOT NULL' for field in fields])
    statement_two = ' AND (%s) ' % ' OR '.join([field + ' IS NOT NULL' for field in fields])
    return CheckConstraint('%s %s' % (statement_one, statement_two), name='comment_must_have_one_source_only')


def build_person_constraints():
    fields = ('investigation_id', 'study_id')
    statement_two = ' OR '.join([field + ' IS NOT NULL' for field in fields])
    return CheckConstraint(statement_two, name='person_has_at_least_one_source')
