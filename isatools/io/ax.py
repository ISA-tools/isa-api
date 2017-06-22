import ftplib
import logging
import os
import tempfile

EBI_FTP_SERVER = 'ftp.ebi.ac.uk'
AX_EXPERIMENT_BASE_DIR = '/pub/databases/arrayexpress/data/experiment/'

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def get(arrayexpress_id, target_dir=None):
    """
    This function downloads ISA content from the ArrayExpress FTP site.

    :param ax_experiment_id: Study identifier for ArrayExpress study to get, as a str (e.g. E-GEOD-59671)
    :param target_dir: Path to write files to. If None, writes to temporary directory (generated on the fly)
    :return: Path where the files were written to

    Example usage:
        AX.get_study('E-GEOD-59671', '/tmp/ax')
    """

    idbits = arrayexpress_id.split('-')
    exp_type = idbits[1]

    logging.info("Setting up ftp with {}".format(EBI_FTP_SERVER))
    ftp = ftplib.FTP(EBI_FTP_SERVER)
    logging.info("Logging in as anonymous user...")
    response = ftp.login()
    if '230' in response:  # 230 means Login successful
        logging.info("Log in successful!")
        try:
            logging.info("Looking for experiment '{}'".format(arrayexpress_id))
            ftp.cwd('{base_dir}/{exp_type}/{arrayexpress_id}'.format(base_dir=AX_EXPERIMENT_BASE_DIR, exp_type=exp_type,
                                                                     arrayexpress_id=arrayexpress_id))
            if target_dir is None:
                target_dir = tempfile.mkdtemp()
            logging.info("Using directory '{}'".format(target_dir))
            idf_filename = "{}.idf.txt".format(arrayexpress_id)
            with open(os.path.join(target_dir, idf_filename), 'wb') as out_file:
                logging.info("Retrieving file '{}'".format(EBI_FTP_SERVER + AX_EXPERIMENT_BASE_DIR + '/' + exp_type + '/' +
                                                           arrayexpress_id + '/' + idf_filename))
                ftp.retrbinary('RETR ' + idf_filename, out_file.write)
            sdrf_filename = "{}.sdrf.txt".format(arrayexpress_id)
            with open(os.path.join(target_dir, sdrf_filename), 'wb') as out_file:
                logging.info("Retrieving file '{}'".format(
                    EBI_FTP_SERVER + AX_EXPERIMENT_BASE_DIR + '/' + exp_type + '/' + arrayexpress_id + '/'
                    + sdrf_filename))
                ftp.retrbinary('RETR ' + sdrf_filename, out_file.write)
        except ftplib.error_perm as ftperr:
            logger.fatal("Could not retrieve ArrayExpress study '{study}': {error}".format(study=arrayexpress_id,
                                                                                           error=ftperr))
        finally:
            return target_dir
    else:
        raise ConnectionError("There was a problem connecting to ArrayExpress: " + response)
