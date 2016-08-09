from isatools.convert import json2isatab, isatab2sra
from isatools import isajson, sra
from glob import glob
import os


def convert(json_fp, path, config_dir=None):
    """ Converter for ISA JSON to SRA.
    :param json_fp: File pointer to ISA JSON input
    :param path: Directory for output to be written
    :param config_dir: path to JSON configuration
    """
    json2isatab.convert(json_fp=json_fp, path=path, config_dir=config_dir)
    isatab2sra.create_sra(path, path)
    for f in glob(path + '/*.txt'):  # remove generated isatab files
        os.remove(f)


def convert2(json_fp, path, config_dir=None):
    """ (New) Converter for ISA JSON to SRA.
    :param json_fp: File pointer to ISA JSON input
    :param path: Directory for output to be written
    :param config_dir: path to JSON configuration
    """
    log_msg_stream = isajson.validate(fp=json_fp, config_dir=config_dir)
    if '(E)' not in log_msg_stream.getvalue():
        i = isajson.load(fp=json_fp)
        sra.export(i, path)
    else:
        raise ValueError("There was a problem when validating the input ISA JSON")
