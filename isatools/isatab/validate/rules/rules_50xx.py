from isatools.isatab.utils import get_num_study_groups
from isatools.isatab.defaults import log
from isatools.isatab.validate.store import validator


def check_study_groups(table, filename, study_group_size_in_comment):
    """Checks the number of study groups against an expected group size

    :param table: Table as a DataFrame
    :param filename: Filename of the table
    :param study_group_size_in_comment: Expected group size
    :return: True if computed group size matches expected group size, False if
    not
    """
    num_study_groups = get_num_study_groups(table, filename)
    log.debug('Found {} study groups in {}'.format(num_study_groups, filename))
    msg = 'Found {} study groups in {}'.format(num_study_groups, filename)
    spl = 'Found {} study groups in {}'.format(num_study_groups, filename)
    validator.add_info(message=msg, supplemental=spl, code=5001)

    if study_group_size_in_comment is not None and study_group_size_in_comment != num_study_groups:
        msg = 'Reported study group size does not match table'.format(num_study_groups, filename)
        spl = 'Study group size reported as {} but found {} in {}'
        spl = spl.format(study_group_size_in_comment, num_study_groups, filename)
        log.warning(spl)
        validator.add_warning(message=msg, supplemental=spl, code=5002)
        return False
    return True
