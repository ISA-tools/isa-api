from isatools import isajson, magetab
import logging
import isatools

logging.basicConfig(level=isatools.log_level)
LOG = logging.getLogger(__name__)


def convert(source_json_fp, out_path):
    """ Converter for ISA-JSON to MAGE-Tab.
    :param source_json_fp: File descriptor of input ISA JSON file
    :param out_path: Output path to write output MAGE-Tab to
    """
    LOG.info("loading isajson %s", source_json_fp.name)
    ISA = isajson.load(source_json_fp)
    LOG.info("dumping magetab %s", out_path)
    magetab.dump(ISA, out_path)