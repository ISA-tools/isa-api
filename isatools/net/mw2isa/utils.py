import re


def is_mw_id(mw_id):
    return re.match(r"(^ST\d{6})", mw_id)
