import logging


from isatools import isatab
from isatools import sampletab


log = logging.getLogger('isatools')


def convert(source_inv_fp, target_fp):
    """ Converter for ISA-Tab to SampleTab.
    :param source_inv_fp: File descriptor of input investigation file
    :param target_fp: File descriptor to write output SampleTab to (must be writeable)
    """
    log.info("loading isatab %s", source_inv_fp.name)
    ISA = isatab.load(source_inv_fp)
    log.info("dumping sampletab %s", target_fp.name)
    sampletab.dump(ISA, target_fp)
