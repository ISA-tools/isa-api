"""
File to profile the validation functions of ISAtab.
Do not comment what look like unused imports. They are being called in the form of a string by runctx.
Profiles are dumped in /performances/profiles/ and can be visualized using the following command:
`snakeviz ./performances/profiles/` from the project root directory.
Author: D. Batista (@Terazus)
"""

from cProfile import runctx
from os import path

from isatools.isatab.defaults import log
from isatools.isatab.validate.core import validate as validate
from isatools.isatab.load import load
from performances.defaults import OUTPUT_PATH, DEFAULT_TAB_INPUT as DEFAULT_INPUT

log.disabled = True


def profile_validation(filename=None, output_path=None):
    input_data_path = filename if filename else DEFAULT_INPUT
    if output_path is None:
        output_path = OUTPUT_PATH

    with open(input_data_path, 'r') as data_file:
        output_data_path = path.join(output_path, 'isatab_validation_mzml')
        runctx('validate(data_file, mzml=True)', globals(), locals(), output_data_path)

    with open(input_data_path, 'r') as data_file:
        output_data_path = path.join(output_path, 'isatab_validation')
        runctx('validate(data_file)', globals(), locals(), output_data_path)


def profile_loader(filename=None, output_path=None):
    input_data_path = filename if filename else DEFAULT_INPUT
    if output_path is None:
        output_path = OUTPUT_PATH
    output_data_path = path.join(output_path, 'isatab_load')
    with open(input_data_path, 'r') as data_file:
        runctx('load(data_file)', globals(), locals(), output_data_path)


def profile_isatab(filename=None, output_path=None):
    profile_validation(filename, output_path)
    profile_loader(filename, output_path)
