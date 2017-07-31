import logging

from isatools import config
from isatools import isatab
from isatools import sampletab

logging.basicConfig(level=config.log_level)
logger = logging.getLogger(__name__)


def convert(source_sampletab_fp, target_dir):
    """ Converter for ISA-JSON to SampleTab.
    :param source_sampletab_fp: File descriptor of input SampleTab file
    :param target_dir: Path to write out ISA-Tab files to
    """
    ISA = sampletab.load(source_sampletab_fp)
    isatab.dump(ISA, target_dir)


