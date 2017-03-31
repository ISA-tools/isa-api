from isatools import isatab, magetab
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def convert(source_idf_fp, output_path):
    """ Converter for MAGE-TAB to ISA-Tab
    :param source_idf_fp: File descriptor of input IDF file
    :param output_dir: Path to directory to write output ISA-Tab files to
    """
    ISA = magetab.load(source_idf_fp)
    isatab.dump(ISA, output_path)
