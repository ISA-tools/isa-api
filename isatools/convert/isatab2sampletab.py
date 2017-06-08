from isatools import isatab, sampletab
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def convert(source_inv_fp, target_fp):
    """ Converter for ISA-Tab to SampleTab.
    :param source_inv_fp: File descriptor of input investigation file
    :param target_fp: File descriptor to write output SampleTab to (must be writeable)
    """
    ISA = isatab.load(source_inv_fp)
    sampletab.dump(ISA, target_fp)
