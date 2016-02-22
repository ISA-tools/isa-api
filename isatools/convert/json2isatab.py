from isatools import isajson
from isatools import isatab
import os
import shutil


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
    isatab.dump(isa_obj=isa_obj, output_path=path)
    #  copy data files across from source directory where JSON is located
    for file in [f for f in os.listdir(os.path.dirname(json_fp.name))
                 if not (f.endswith('.txt') and (f.startswith('i_') or f.startswith('s_') or f.startswith('a_'))) and
                 not (f.endswith('.json'))]:
        filepath = os.path.join(os.path.dirname(json_fp.name), file)
        if os.path.isfile(filepath):
            shutil.copy(filepath, path)
