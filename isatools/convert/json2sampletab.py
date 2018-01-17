import logging


from isatools import isajson
from isatools import sampletab


log = logging.getLogger('isatools')


def convert(source_json_fp, target_fp):
    """ Converter for ISA-JSON to SampleTab.
    :param source_json_fp: File descriptor of input ISA JSON file
    :param target_fp: File descriptor to write output SampleTab to (must be writeable)
    """
    log.info("loading isajson %s", source_json_fp.name)
    ISA = isajson.load(source_json_fp)
    log.info("dumping sampletab %s", target_fp.name)
    sampletab.dump(ISA, target_fp)
