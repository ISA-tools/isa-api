from isatools import sampletab, isatab
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def convert(source_sampletab_fp, target_dir):
    """ Converter for ISA-JSON to SampleTab.
    :param source_sampletab_fp: File descriptor of input SampleTab file
    :param target_dir: Path to write out ISA-Tab files to
    """
    ISA = sampletab.load(source_sampletab_fp)
    isatab.dump(ISA, target_dir)


