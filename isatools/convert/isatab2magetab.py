from isatools import isatab, magetab
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def convert(source_inv_fp, output_path):
    """ Converter for ISA-Tab to MAGE-TAB.
    :param source_inv_fp: File descriptor of input investigation file
    :param output_dir: Path to directory to write output MAGE-TAB files to
    """
    ISA = isatab.load(source_inv_fp)
    magetab.dump(ISA, output_path)
