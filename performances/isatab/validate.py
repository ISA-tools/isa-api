"""
File to profile the validation functions of ISAtab.
Do not comment what look like unused imports. They are being called in the form of a string by runctx.
Profiles are dumped in /performances/profiles/ and can be visualized using the following command:
`snakeviz ./performances/profiles/` from the project root directory.
Author: D. Batista (@Terazus)
"""

from cProfile import runctx
from os import path

from isatools.isatab.validate.rules.core import validate as n_validate
from isatools.isatab.validate.core import validate as o_validate
from isatools.isatab.load import load

HERE_PATH = path.dirname(path.abspath(__file__))
OUTPUT_PATH = path.join(HERE_PATH, '..', 'profiles', 'isatab')


def profile_validation(filename=None, output_path=OUTPUT_PATH):
    if filename is None:
        input_data_path = path.join(HERE_PATH, '..', '..', 'tests', 'data', 'tab', 'BII-I-1/i_investigation.txt')
    else:
        input_data_path = filename
    with open(input_data_path, 'r') as data_file:
        output_data_path = path.join(output_path, 'new_validation')
        runctx('n_validate(data_file, mzml=True)', globals(), locals(), output_data_path)

    with open(input_data_path, 'r') as data_file:
        output_data_path = path.join(output_path, 'old_validation')
        runctx('o_validate(data_file)', globals(), locals(), output_data_path)


def profile_loader(filename=None, output_path=OUTPUT_PATH):
    if filename is None:
        input_data_path = path.join(HERE_PATH, '..', '..', 'tests', 'data', 'tab', 'BII-I-1/i_investigation.txt')
    else:
        input_data_path = filename
    output_data_path = path.join(output_path, 'load')
    with open(input_data_path, 'r') as data_file:
        runctx('load(data_file)', globals(), locals(), output_data_path)
