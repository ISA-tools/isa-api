from mzml2isa.parsing import full_parse
from isatools import isatab

import logging
import os

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def convert(mzml_folder, out_folder, study_id, validate_output=False):
    """ Converter for MZML to ISA-Tab.
    :param mzml_folder: Path to folder containing mzml files.
    :param out_folder: Path to output folder to write ISA-Tab to.
    :param study_id: A study identifier.
    :param validate_output: Flag to indicate whether to validate the generated ISA-Tab
    """
    if not os.path.exists(mzml_folder):
        raise FileNotFoundError("Could not find input mzml folder")
    full_parse(mzml_folder, out_folder, study_id)
    if validate_output and os.path.exists(out_folder):
        return isatab.validate2(open(os.path.join(out_folder, study_id, 'i_investigation.txt')))
