from isatools import isajson, magetab
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def convert(source_json_fp, out_path):
    """ Converter for ISA-JSON to MAGE-Tab.
    :param source_json_fp: File descriptor of input ISA JSON file
    :param out_path: Output path to write output MAGE-Tab to
    """
    ISA = isajson.load(source_json_fp)
    magetab.dump(ISA, out_path)