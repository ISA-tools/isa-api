import logging


from isatools import isajson
from isatools import magetab


log = logging.getLogger('isatools')


def convert(source_json_fp, out_path):
    """ Converter for ISA-JSON to MAGE-Tab.
    :param source_json_fp: File descriptor of input ISA JSON file
    :param out_path: Output path to write output MAGE-Tab to
    """
    log.info("loading isajson %s", source_json_fp.name)
    ISA = isajson.load(source_json_fp)
    log.info("dumping magetab %s", out_path)
    magetab.dump(ISA, out_path)