from isatools import isajson
from isatools import isatab
import os


def convert(json_fp, path):
    """ Converter for ISA JSON to ISA Tab. Currently only converts investigation file contents
    :param json_fp: File pointer to ISA JSON input
    :param tab_fp: File pointer to ISA tab output

    Example usage:
        Read from a JSON and write to an investigation file, make sure to create/open relevant
        Python file objects.

        from isatools.convert import json2isatab
        json_file = open('BII-I-1.json', 'r')
        tab_file = open('i_investigation.txt', 'w')
        json2isatab.convert(json_file, tab_file)

    """
    isa_obj = isajson.load(fp=json_fp)
    isatab.dump(isa_obj=isa_obj, path=path)
