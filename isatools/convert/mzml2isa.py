# -*- coding: utf-8 -*
"""Convert mzML to ISA-Tab"""
import logging
import os
from mzml2isa import __version__

from mzml2isa.parsing import convert as mzml_convert

from isatools import isatab


logger = logging.getLogger('isatools')
logger.setLevel(logging.INFO)


def convert(mzml_folder, out_folder, study_id, validate_output=False):
    """ Converter for MZML to ISA-Tab.
    :param mzml_folder: Path to folder containing mzml files.
    :param out_folder: Path to output folder to write ISA-Tab to.
    :param study_id: A study identifier.
    :param validate_output: Flag to indicate whether to validate the generated
                            ISA-Tab
    """
    logger.info("mzML2ISA package version: {}".format(__version__))
    print("mzML2ISA package version: {}".format(__version__))
    print(logger)

    if not os.path.exists(mzml_folder):
        raise FileNotFoundError("Could not find input mzml folder")
    mzml_convert(mzml_folder, out_folder, study_id)
    if validate_output and os.path.exists(out_folder):
        with open(os.path.join(out_folder, 'i_Investigation.txt'),
                  'r', encoding='utf-8') as i_fp:
            return isatab.validate(i_fp)
