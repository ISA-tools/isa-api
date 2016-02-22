from isatools.convert import json2isatab, isatab2sra
from glob import glob
import os


def convert(json_fp, path, config):
    """ Converter for ISA JSON to SRA.
    :param json_fp: File pointer to ISA JSON input
    :param path: Directory for output to be written

    """
    json2isatab.convert(json_fp, path)
    isatab2sra.create_sra(path, path, config)
    for f in glob(path + '/*.txt'):  # remove generated isatab files
        os.remove(f)