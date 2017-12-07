"""Functions for retrieving metadata from ArrayExpress.

This module connects to the European Bioinformatics Institute's
ArrayExpress database. If you have problems with it, check that
it's working at http://www.ebi.ac.uk/arrayexpress/
"""
from __future__ import absolute_import
import csv
import ftplib
import logging
import os
import shutil
import tempfile


from isatools.convert import magetab2isatab
from isatools.convert import magetab2json

EBI_FTP_SERVER = 'ftp.ebi.ac.uk'
AX_EXPERIMENT_BASE_DIR = '/pub/databases/arrayexpress/data/experiment'


log = logging.getLogger('isatools')


def get(arrayexpress_id, target_dir=None):
    """
    This function downloads MAGE-TAB content from the ArrayExpress FTP site.

    :param ax_experiment_id: Experiment identifier for ArrayExpress study to get, as a str (e.g. E-GEOD-59671)
    :param target_dir: Path to write MAGE-TAB files to. If None, writes to temporary directory (generated on the fly)
    :return: Path where the files were written to

    Example usage:
        from isatools.io import ax as AX
        AX.get('E-GEOD-59671', '/tmp/ax')
    """

    idbits = arrayexpress_id.split('-')
    exp_type = idbits[1]

    log.info("Setting up ftp with {}".format(EBI_FTP_SERVER))
    ftp = ftplib.FTP(EBI_FTP_SERVER)
    log.info("Logging in as anonymous user...")
    response = ftp.login()

    if '230' in response:  # 230 means Login successful
        log.info("Log in successful!")
        try:
            logging.info("Looking for experiment '{}'".format(arrayexpress_id))
            ftp.cwd('{base_dir}/{exp_type}/{arrayexpress_id}'.format(base_dir=AX_EXPERIMENT_BASE_DIR, exp_type=exp_type,
                                                                     arrayexpress_id=arrayexpress_id))
            if target_dir is None:
                target_dir = tempfile.mkdtemp()
                log.info("Using directory '{}'".format(target_dir))
            idf_filename = "{}.idf.txt".format(arrayexpress_id)
            with open(os.path.join(target_dir, idf_filename), 'wb') as out_file:
                log.info("Retrieving file '{}'".format(EBI_FTP_SERVER + AX_EXPERIMENT_BASE_DIR + '/' + exp_type +
                                                           '/' + arrayexpress_id + '/' + idf_filename))
                ftp.retrbinary('RETR ' + idf_filename, out_file.write)
            try:
                with open(os.path.join(target_dir, idf_filename), encoding='utf-8') as unicode_idf_file:
                    reader = csv.reader(filter(lambda r: r.startswith('SDRF File'), unicode_idf_file), dialect='excel-tab')
                    for line in reader:
                        for sdrf_filename in line[1:]:
                            with open(os.path.join(target_dir, sdrf_filename), 'wb') as out_file:
                                log.info("Retrieving file '{}'".format(
                                    EBI_FTP_SERVER + AX_EXPERIMENT_BASE_DIR + '/' + exp_type + '/' + arrayexpress_id + '/'
                                    + sdrf_filename))
                                ftp.retrbinary('RETR ' + sdrf_filename, out_file.write)
            except UnicodeDecodeError:
                with open(os.path.join(target_dir, idf_filename), encoding='ISO8859-2') as latin2_idf_file:
                    reader = csv.reader(filter(lambda r: r.startswith('SDRF File'), latin2_idf_file), dialect='excel-tab')
                    for line in reader:
                        for sdrf_filename in line[1:]:
                            with open(os.path.join(target_dir, sdrf_filename), 'wb') as out_file:
                                log.info("Retrieving file '{}'".format(
                                    EBI_FTP_SERVER + AX_EXPERIMENT_BASE_DIR + '/' + exp_type + '/' + arrayexpress_id + '/'
                                    + sdrf_filename))
                                ftp.retrbinary('RETR ' + sdrf_filename, out_file.write)
        except ftplib.error_perm as ftperr:
            log.fatal("Could not retrieve ArrayExpress study '{study}': {error}".format(study=arrayexpress_id,
                                                                                        error=ftperr))
        finally:
            ftp.close()
            return target_dir
    else:
        ftp.close()
        raise ConnectionError("There was a problem connecting to ArrayExpress: " + response)


def get_isatab(arrayexpress_id, target_dir=None):
    """
    This function downloads MAGE-TAB content as ISA-Tab from the ArrayExpress FTP site.

    :param ax_experiment_id: Experiment identifier for ArrayExpress study to get, as a str (e.g. E-GEOD-59671)
    :param target_dir: Path to write ISA-Tab files to. If None, writes to temporary directory (generated on the fly)
    :return: Path where the files were written to

    Example usage:
        from isatools.io import ax as AX
        AX.get_isatab('E-GEOD-59671', '/tmp/ax')
    """
    tmp_dir = tempfile.mkdtemp()
    try:
        get(arrayexpress_id=arrayexpress_id, target_dir=tmp_dir)
        if target_dir is None:
            target_dir = tempfile.mkdtemp()
            log.info("Using directory '{}'".format(target_dir))
        magetab2isatab.convert(os.path.join(tmp_dir, "{}.idf.txt".format(arrayexpress_id)), output_path=target_dir)
    except Exception as e:
        log.fatal("Something went wrong: {}".format(e))
    finally:
        shutil.rmtree(tmp_dir)
        return target_dir


def getj(arrayexpress_id):
    """
    This function downloads MAGE-TAB content as ISA-JSON from the ArrayExpress FTP site.

    :param ax_experiment_id: Experiment identifier for ArrayExpress study to get, as a str (e.g. E-GEOD-59671)
    :return: ISA-JSON representation of the MAGE-TAB content

    Example usage:
        from isatools.io import ax as AX
        my_json = AX.getj('E-GEOD-59671')
    """
    tmp_dir = tempfile.mkdtemp()
    mage_json = None
    try:
        get(arrayexpress_id=arrayexpress_id, target_dir=tmp_dir)
        mage_json = magetab2json.convert(os.path.join(tmp_dir, "{}.idf.txt".format(arrayexpress_id)))
    except Exception as e:
        log.fatal("Something went wrong: {}".format(e))
    finally:
        shutil.rmtree(tmp_dir)
        return mage_json
