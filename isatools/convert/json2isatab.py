from isatools import isajson
from isatools import isatab
import os
import shutil
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def convert(json_fp, path, i_file_name='i_investigation.txt', config_dir=isajson.default_config_dir,
            validate_first=True):
    """ Converter for ISA JSON to ISA Tab. Currently only converts investigation file contents
    :param json_fp: File pointer to ISA JSON input
    :param path: Directory to ISA tab output
    :param i_file_name: Investigation file name, default is i_investigation.txt
    :param config_dir: Directory to config directory
    :param validate_first: Validate JSON before conversion, default is True

    Example usage:
        Read from a JSON and write to an investigation file, make sure to create/open relevant
        Python file objects.

        from isatools.convert import json2isatab
        json_file = open('BII-I-1.json', 'r')
        tab_file = open('i_investigation.txt', 'w')
        json2isatab.convert(json_file, path)

    """
    if validate_first:
        logger.info("Validating input JSON before conversion")
        report = isajson.validate(fp=json_fp, config_dir=config_dir, log_level=logging.ERROR)
        if len(report['errors']) > 0:
            logger.fatal("Could not proceed with conversion as there are some fatal validation errors. Check log.")
            return
        json_fp.seek(0)  # reset file pointer after validation
    logger.info("Loading source ISA JSON...")
    isa_obj = isajson.load(fp=json_fp)
    logger.info("Dumping target ISA-Tab...")
    isatab.dump(isa_obj=isa_obj, output_path=path, i_file_name=i_file_name)
    #  copy data files across from source directory where JSON is located
    logger.info("Copying data files from source to target...")
    for file in [f for f in os.listdir(os.path.dirname(json_fp.name))
                 if not (f.endswith('.txt') and (f.startswith('i_') or f.startswith('s_') or f.startswith('a_'))) and
                 not (f.endswith('.json'))]:
        filepath = os.path.join(os.path.dirname(json_fp.name), file)
        if os.path.isfile(filepath):
            shutil.copy(filepath, path)
