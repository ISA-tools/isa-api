import ftplib
import logging
import os
import tempfile
import shutil
import json
from isatools.convert import isatab2json

MTBLS_FTP_SERVER = 'ftp.ebi.ac.uk'
MTBLS_BASE_DIR = '/pub/databases/metabolights/studies/public'
INVESTIGATION_FILENAME = 'i_Investigation.txt'

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_study(mtbls_study_id):
    logging.info("Setting up ftp with {}".format(MTBLS_FTP_SERVER))
    ftp = ftplib.FTP(MTBLS_FTP_SERVER)
    logging.info("Logging in as anonymous user...")
    response = ftp.login()
    if '230' in response:  # 230 means Login successful
        logging.info("Log in successful!")
        tmp_dir = None
        try:
            logging.info("Looking for study '{}'".format(mtbls_study_id))
            ftp.cwd('{base_dir}/{study}'.format(base_dir=MTBLS_BASE_DIR, study=mtbls_study_id))
            tmp_dir = tempfile.mkdtemp()
            logging.info("Created temporary directory '{}'".format(tmp_dir))
            out_file = open(os.path.join(tmp_dir, INVESTIGATION_FILENAME), 'wb')
            logging.info("Retrieving file '{}'".format(MTBLS_FTP_SERVER + MTBLS_BASE_DIR + '/' + mtbls_study_id + '/' + INVESTIGATION_FILENAME))
            ftp.retrbinary('RETR ' + INVESTIGATION_FILENAME, out_file.write)
            i_bytes = open(out_file.name).read()
            lines = i_bytes.splitlines()
            s_filenames = [l.split('\t')[1][1:-1] for l in lines if 'Study File Name' in l]
            for s_filename in s_filenames:
                out_file = open(os.path.join(tmp_dir, s_filename), 'wb')
                logging.info("Retrieving file '{}'".format(
                    MTBLS_FTP_SERVER + MTBLS_BASE_DIR + '/' + mtbls_study_id + '/' + s_filename))
                ftp.retrbinary('RETR ' + s_filename, out_file.write)
            a_filenames_lines = [l.split('\t') for l in lines if 'Study Assay File Name' in l]
            for a_filename_line in a_filenames_lines:
                for a_filename in [f[1:-1] for f in a_filename_line[1:]]:
                    out_file = open(os.path.join(tmp_dir, a_filename), 'wb')
                    logging.info("Retrieving file '{}'".format(
                        MTBLS_FTP_SERVER + MTBLS_BASE_DIR + '/' + mtbls_study_id + '/' + a_filename))
                    ftp.retrbinary('RETR ' + a_filename, out_file.write)

        except ftplib.error_perm as ftperr:
            logger.fatal("Could not retrieve MetaboLights study '{study}': {error}".format(study=mtbls_study_id, error=ftperr))
        finally:
            return tmp_dir
    else:
        raise ConnectionError("There was a problem connecting to MetaboLights: " + response)


def load(mtbls_study_id):
    tmp_dir = None
    try:
        tmp_dir = get_study(mtbls_study_id)
        isatab2json.convert(tmp_dir, tmp_dir)
        for file in os.listdir(tmp_dir):
            if file.endswith('.json'):
                return json.load(open(os.path.join(tmp_dir, file)))
    finally:
        if tmp_dir is not None:
            shutil.rmtree(tmp_dir)


def get_data_files_urls(mtbls_study_id, factor_selection=None):
    isa_json = load(mtbls_study_id)

