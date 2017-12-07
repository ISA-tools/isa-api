import json
import logging


from isatools import sampletab
from isatools.isajson import ISAJSONEncoder


logger = logging.getLogger('isatools')


def convert(source_sampletab_fp, target_json_fp):
    """ Converter for ISA-JSON to SampleTab.
    :param source_sampletab_fp: File descriptor of input SampleTab file
    :param target_json_fp: File descriptor to write output ISA JSON (must be writeable)
    """
    ISA = sampletab.load(source_sampletab_fp)
    json.dump(ISA, fp=target_json_fp, cls=ISAJSONEncoder)
