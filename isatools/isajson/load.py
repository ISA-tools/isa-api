import json

from isatools.model import Investigation


def load(fp):
    """Loads an ISA-JSON file and returns an Investigation object.

    :param fp: A file-like object or a string containing the JSON data.
    :return: An Investigation object.
    """
    investigation_json = json.load(fp)
    investigation = Investigation()
    investigation.from_dict(investigation_json)
    return investigation
