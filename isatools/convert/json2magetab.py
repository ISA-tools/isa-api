from isatools import isajson, magetab, isatab
import tempfile
import logging
import shutil
import os

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def convert(source_json_fp, output_path):
    """ Converter for ISA-JSON to MAGE-TAB.
    :param source_json_fp: File descriptor of input ISA JSON file
    :param output_dir: Path to directory to write output MAGE-TAB files to
    """
    ISA = isajson.load(source_json_fp)
    tmp = tempfile.mkdtemp()
    try:
        isatab.dump(isa_obj=ISA, output_path=tmp)
        print(os.listdir(tmp))
        with open(os.path.join(tmp, 'i_investigation.txt')) as inv_fp:
            ISA = isatab.load(inv_fp)
            magetab.dump(ISA, output_path)
    finally:
        shutil.rmtree(tmp)
