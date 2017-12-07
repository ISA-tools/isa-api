import logging


from isatools import isatab
from isatools import sampletab


logger = logging.getLogger('isatools')


def convert(source_sampletab_fp, target_dir):
    """ Converter for ISA-JSON to SampleTab.
    :param source_sampletab_fp: File descriptor of input SampleTab file
    :param target_dir: Path to write out ISA-Tab files to
    """
    ISA = sampletab.load(source_sampletab_fp)
    isatab.dump(ISA, target_dir)


