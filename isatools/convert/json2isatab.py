import os
import shutil
import logging


from isatools import isajson
from isatools import isatab


log = logging.getLogger('isatools')


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
        log.info("Validating input JSON before conversion")
        report = isajson.validate(fp=json_fp, config_dir=config_dir, log_level=logging.ERROR)
        if len(report['errors']) > 0:
            log.fatal("Could not proceed with conversion as there are some fatal validation errors. Check log.")
            return
        json_fp.seek(0)  # reset file pointer after validation
    log.info("Loading ISA-JSON from %s", json_fp.name)
    isa_obj = isajson.load(fp=json_fp)
    log.info("Dumping ISA-Tab to %s", path)
    log.debug("Using configuration from %s", config_dir)
    isatab.dump(isa_obj=isa_obj, output_path=path, i_file_name=i_file_name)
    #  copy data files across from source directory where JSON is located
    log.info("Copying data files from source to target")
    for file in [f for f in os.listdir(os.path.dirname(json_fp.name))
                 if not (f.endswith('.txt') and (f.startswith('i_') or f.startswith('s_') or f.startswith('a_'))) and
                 not (f.endswith('.json'))]:
        filepath = os.path.join(os.path.dirname(json_fp.name), file)
        if os.path.isfile(filepath):
            log.debug("Copying %s to %s", filepath, path)
            shutil.copy(filepath, path)
