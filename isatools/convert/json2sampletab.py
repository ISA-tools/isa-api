from isatools import isajson, sampletab
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def convert(source_json_fp, target_fp):
    """ Converter for ISA-JSON to SampleTab.
    :param source_json_fp: File descriptor of input ISA JSON file
    :param target_fp: File descriptor to write output SampleTab to (must be writeable)
    """
    ISA = isajson.load(source_json_fp)
    sampletab.dump(ISA, target_fp)
