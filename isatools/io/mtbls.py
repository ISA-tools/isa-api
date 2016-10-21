import ftplib
import logging
import os
import tempfile
import shutil
import json
import six
import functools
from isatools.convert import isatab2json
from contextlib import closing

MTBLS_FTP_SERVER = 'ftp.ebi.ac.uk'
MTBLS_BASE_DIR = '/pub/databases/metabolights/studies/public'
INVESTIGATION_FILENAME = 'i_Investigation.txt'

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# This will remove the "'U' flag is deprecated" DeprecationWarning in Python3
open = functools.partial(open, mode='r') if six.PY3 else functools.partial(open, mode='rU')

_STRIPCHARS = "\"\'\r\n\t"

def get_study(mtbls_study_id):
    logging.info("Setting up ftp with {}".format(MTBLS_FTP_SERVER))
    with closing(ftplib.FTP(MTBLS_FTP_SERVER)) as ftp:
        logging.info("Logging in as anonymous user...")
        response = ftp.login()

        if not '230' in response:
            raise ConnectionError("There was a problem connecting to MetaboLights: {}".format(response))

        logging.info("Log in successful!")
        #tmp_dir = None
        try:
            logging.info("Looking for study '{}'".format(mtbls_study_id))
            ftp.cwd('{base_dir}/{study}'.format(base_dir=MTBLS_BASE_DIR, study=mtbls_study_id))
            tmp_dir = tempfile.mkdtemp()
            logging.info("Created temporary directory '{}'".format(tmp_dir))
            with open(os.path.join(tmp_dir, INVESTIGATION_FILENAME), mode='wb') as out_file:
                logging.info("Retrieving file '{}{}/{}/{}'".format(MTBLS_FTP_SERVER,MTBLS_BASE_DIR,mtbls_study_id,INVESTIGATION_FILENAME))
                ftp.retrbinary('RETR {}'.format(INVESTIGATION_FILENAME), out_file.write)
            with open(os.path.join(tmp_dir, INVESTIGATION_FILENAME)) as out_file:
                s_filenames = [l.split('\t')[1].strip(_STRIPCHARS)
                                for l in out_file if 'Study File Name' in l]
                out_file.seek(0)
                a_filenames = [x.strip(_STRIPCHARS)
                                for l in out_file if 'Study Assay File Name' in l
                                        for x in l.split('\t')[1:]]

            for s_filename in s_filenames:
                with open(os.path.join(tmp_dir, s_filename), mode='wb') as out_file:
                    logging.info("Retrieving file '{}{}/{}/{}'".format(
                        MTBLS_FTP_SERVER, MTBLS_BASE_DIR, mtbls_study_id, s_filename))
                    ftp.retrbinary('RETR {}'.format(s_filename), out_file.write)

            for a_filename in a_filenames:
                with open(os.path.join(tmp_dir, a_filename), mode='wb') as out_file:
                    logging.info("Retrieving file '{}{}/{}/{}'".format(
                        MTBLS_FTP_SERVER, MTBLS_BASE_DIR, mtbls_study_id, a_filename))
                    ftp.retrbinary('RETR {}'.format(a_filename), out_file.write)

        except ftplib.error_perm as ftperr:
            logger.fatal("Could not retrieve MetaboLights study '{study}': {error}".format(study=mtbls_study_id, error=ftperr))
        finally:
            return tmp_dir




def load(mtbls_study_id):
    tmp_dir = get_study(mtbls_study_id)
    if tmp_dir is None:
        raise IOError("There was a problem retrieving the study {}".format(mtbls_study_id))
    isa_json = isatab2json.convert(tmp_dir, identifier_type=isatab2json.IdentifierType.name, validate_first=False)
    return isa_json



def get_data_files_urls(mtbls_study_id, factor_selection=None):
    isa_json = load(mtbls_study_id)

