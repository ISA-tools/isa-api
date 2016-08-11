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


def get_study(mtbls_study_id, target_dir=None):
    """
    This function downloads ISA content from the MetaboLights FTP site.

    :param mtbls_study_id: Study identifier for MetaboLights study to get, as a str (e.g. MTBLS1)
    :param target_dir: Path to write files to. If None, writes to temporary directory (generated on the fly)
    :return: Path where the files were written to

    Example usage:
        isa_json = MTBLS.get_study('MTBLS1', '/tmp/mtbls')
    """
    logging.info("Setting up ftp with {}".format(MTBLS_FTP_SERVER))
    ftp = ftplib.FTP(MTBLS_FTP_SERVER)
    logging.info("Logging in as anonymous user...")
    response = ftp.login()
    if '230' in response:  # 230 means Login successful
        logging.info("Log in successful!")
        try:
            logging.info("Looking for study '{}'".format(mtbls_study_id))
            ftp.cwd('{base_dir}/{study}'.format(base_dir=MTBLS_BASE_DIR, study=mtbls_study_id))
            if target_dir is None:
                target_dir = tempfile.mkdtemp()
            logging.info("Using directory '{}'".format(target_dir))
            out_file = open(os.path.join(target_dir, INVESTIGATION_FILENAME), 'wb')
            logging.info("Retrieving file '{}'".format(MTBLS_FTP_SERVER + MTBLS_BASE_DIR + '/' + mtbls_study_id + '/' + INVESTIGATION_FILENAME))
            ftp.retrbinary('RETR ' + INVESTIGATION_FILENAME, out_file.write)
            i_bytes = open(out_file.name).read()
            lines = i_bytes.splitlines()
            s_filenames = [l.split('\t')[1][1:-1] for l in lines if 'Study File Name' in l]
            for s_filename in s_filenames:
                out_file = open(os.path.join(target_dir, s_filename), 'wb')
                logging.info("Retrieving file '{}'".format(
                    MTBLS_FTP_SERVER + MTBLS_BASE_DIR + '/' + mtbls_study_id + '/' + s_filename))
                ftp.retrbinary('RETR ' + s_filename, out_file.write)
            a_filenames_lines = [l.split('\t') for l in lines if 'Study Assay File Name' in l]
            for a_filename_line in a_filenames_lines:
                for a_filename in [f[1:-1] for f in a_filename_line[1:]]:
                    out_file = open(os.path.join(target_dir, a_filename), 'wb')
                    logging.info("Retrieving file '{}'".format(
                        MTBLS_FTP_SERVER + MTBLS_BASE_DIR + '/' + mtbls_study_id + '/' + a_filename))
                    ftp.retrbinary('RETR ' + a_filename, out_file.write)

        except ftplib.error_perm as ftperr:
            logger.fatal("Could not retrieve MetaboLights study '{study}': {error}".format(study=mtbls_study_id, error=ftperr))
        finally:
            return target_dir
    else:
        raise ConnectionError("There was a problem connecting to MetaboLights: " + response)


def loadj(mtbls_study_id):
    """
    This function downloads the specified MetaboLights study and returns an ISA JSON representation of it

    :param mtbls_study_id: Study identifier for MetaboLights study to get, as a str (e.g. MTBLS1)
    :return: ISA JSON representation of the MetaboLights study

    Example usage:
        isa_json = MTBLS.loadj('MTBLS1')
    """
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


def get_data_files_urls(mtbls_isa_json, factor_selection=None):
    """
    This function gets the list of samples and related data file URLs for a given MetaboLights study, optionally
    filtered by factor values (can filter on multiple factors)

    :param mtbls_isa_json: ISA JSON representation of the MetaboLights study
    :param factor_selection: Selected factor values to filter on samples
    :return: A list of samples with associated data file URLs

    Example usage:
        mtbls1 = MTBLS.loadj('MTBLS1')
        datafiles = mtbls.get_data_files_urls(mtbls1, {'gender': 'male'})
    """
    def match(fvs_json, selection):
        if selection is None:
            return True
        for select_name, select_value in selection.items():
            print(select_name, select_value)

    datafiles = list()
    for study_json in mtbls_isa_json['studies']:
        for sample_json in study_json['materials']['samples']:
            if match(sample_json['factorValues'], factor_selection):
                hit = { "sample": sample_json['name'] }


def get_factor_names(mtbls_isa_json):
    """
    This function gets the factor names in a ISA JSON

    :param mtbls_isa_json: ISA JSON representation of the MetaboLights study
    :return: A list of factor names associated data the studies

    Example usage:
        mtbls1 = MTBLS.loadj('MTBLS1')
        factor_names = get_factor_names(mtbls1)
    """
    factors = list()
    for study_json in mtbls_isa_json['studies']:
        for factor_json in study_json['factors']:
            factors.append(factor_json['factorName'])
    return factors