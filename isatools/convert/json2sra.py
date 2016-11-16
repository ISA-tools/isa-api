# coding: utf-8
from isatools import isajson, sra

from glob import glob
import os
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def convert(json_fp, path, config_dir=None):
    """ Converter for ISA JSON to SRA.
    :param json_fp: File pointer to ISA JSON input
    :param path: Directory for output to be written
    :param config_dir: path to JSON configuration
    """
    from isatools.convert import json2isatab, isatab2sra
    json2isatab.convert(json_fp=json_fp, path=path, config_dir=config_dir)
    isatab2sra.create_sra(path, path)
    for f in glob(path + '/*.txt'):  # remove generated isatab files
        os.remove(f)


def convert2(json_fp, path, config_dir=None, sra_settings=None, datafilehashes=None, validate_first=True):
    """ (New) Converter for ISA JSON to SRA.
    :param json_fp: File pointer to ISA JSON input
    :param path: Directory for output to be written
    :param config_dir: path to JSON configuration. If none, uses default embedded in API
    :param sra_settings: SRA settings dict
    :param datafilehashes: Data files with hashes, in a dict
    """
    if validate_first:
        log_msg_stream = isajson.validate(fp=json_fp, config_dir=config_dir, log_level=logging.WARNING)
        if '(E)' in log_msg_stream.getvalue():
            logger.fatal("Could not proceed with conversion as there are some validation errors. Check log.")
            return
    i = isajson.load(fp=json_fp)
    sra.export(i, path, sra_settings=sra_settings, datafilehashes=datafilehashes)

"""
sra_settings = {
 "sra_center": “EI",
  "sra_broker": “EI",
  "sra_action": “ADD”,
 “sra_broker_inform_on_status”: “support@copo.org”,
 “sra_broker_inform_on_error”: “support@copo.org"
}
datafilehashes = {
   "myfile1.fastq": "3a7886617efd0c8f76c360e944149462",
   "myfile2.fastq": "9918006f1eeff68e695539c8843df334"
}
json2sra.convert(json_fp, path, sra_settings=sra_settings, filehashes=datafilehashes)

If files in filehashes dict don't map 1:1 to files found in ISA JSON content, raise Exception

json2sra.convert2(json_fp=open('/Users/dj/PycharmProjects/isa-api/copo.json'), path='/Users/dj/PycharmProjects/isa-api/tmp', sra_settings=)
"""
