import ftplib
import logging
import os

MTBLS_FTP_SERVER = 'ftp.ebi.ac.uk'
MTBLS_BASE_DIR = '/pub/databases/metabolights/studies/public'
INVESTIGATION_FILENAME = 'i_Investigation.txt'

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_study(mtbls_study_id, target_dir='./'):
    ftp = ftplib.FTP(MTBLS_FTP_SERVER)
    response = ftp.login()
    if '230' in response:  # 230 means Login successful
        try:
            ftp.cwd('{base_dir}/{study}'.format(base_dir=MTBLS_BASE_DIR, study=mtbls_study_id))
            out_file = open(os.path.join(target_dir, INVESTIGATION_FILENAME), 'wb')
            ftp.retrbinary('RETR ' + INVESTIGATION_FILENAME, out_file.write)
        except ftplib.error_perm as ftperr:
            logger.fatal("Could not retrieve MetaboLights study '{study}': {error}".format(study=mtbls_study_id, error=ftperr))
    else:
        raise ConnectionError("There was a problem connecting to MetaboLights: " + response)
