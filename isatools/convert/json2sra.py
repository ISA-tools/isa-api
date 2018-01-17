import logging


from isatools import isajson
from isatools import sra



log = logging.getLogger('isatools')


def convert(json_fp, path, config_dir=None, sra_settings=None,
            datafilehashes=None, validate_first=True):
    """ Converter for ISA-JSON to SRA.
    :param json_fp: File pointer to ISA JSON input
    :param path: Directory for output SRA XMLs to be written
    :param config_dir: path to JSON configuration. If none, uses default
        embedded in API
    :param sra_settings: SRA settings dict
    :param datafilehashes: Data files with hashes, in a dict
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
json2sra.convert(json_fp, path, sra_settings=sra_settings,
filehashes=datafilehashes)

If files in filehashes dict don't map 1:1 to files found in ISA JSON content,
raise Exception

json2sra.convert(json_fp=open('/Users/dj/PycharmProjects/isa-api/copo.json'),
path='/Users/dj/PycharmProjects/isa-api/tmp', sra_settings=)
"""
