from isatools import isatab, sampletab
import logging
import isatools

logging.basicConfig(level=isatools.log_level)
LOG = logging.getLogger(__name__)


def convert(source_inv_fp, target_fp):
    """ Converter for ISA-Tab to SampleTab.
    :param source_inv_fp: File descriptor of input investigation file
    :param target_fp: File descriptor to write output SampleTab to (must be writeable)
    """
    LOG.info("loading isatab %s", source_inv_fp.name)
    ISA = isatab.load(source_inv_fp)
    LOG.info("dumping sampletab %s", target_fp.name)
    sampletab.dump(ISA, target_fp)
