# -*- coding: utf-8 -*
"""Convert ISA-JSON to SRA-XML"""
import logging

from isatools import isajson, sra


log = logging.getLogger('isatools')


def convert(json_fp, path, config_dir=None, sra_settings=None,
            datafilehashes=None, validate_first=True):
    """ Converter for ISA-JSON to SRA.
    :param json_fp: File pointer to ISA JSON input
    :param path: Directory for output SRA XMLs to be written
    :param config_dir: path to JSON configuration. If none, uses default embedded in API
    :param sra_settings: SRA settings dict
    :param datafilehashes: Data files with hashes, in a dict
    :param validate_first: a boolean flag to indicate whether to validate or not before converting
    """

    if validate_first:
        log.info("Validating input JSON before conversion")
        report = isajson.validate(fp=json_fp, config_dir=config_dir,
                                  log_level=logging.ERROR)
        if len(report.get('errors')) > 0:
            log.fatal("Could not proceed with conversion as there are some "
                      "validation errors. Check log.")
            return
    log.info("Loading isajson {}".format(json_fp.name))
    isa = isajson.load(fp=json_fp)
    log.info("Exporting SRA to {}".format(path))
    log.debug("Using SRA settings ".format(sra_settings))
    sra.export(isa, path, sra_settings=sra_settings,
               datafilehashes=datafilehashes)

