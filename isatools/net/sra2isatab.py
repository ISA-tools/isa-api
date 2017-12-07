from __future__ import absolute_import
import functools
import logging
import os
import re
import pdb
import subprocess
import tempfile
import uuid
import warnings
from io import BytesIO
from shutil import rmtree
from zipfile import ZipFile




def deprecated(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn(
            'Call to deprecated function {f}.'.format(f=func.__name__),
            category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)
        return func(*args, **kwargs)

    return new_func

__author__ ='massi'

DESTINATION_DIR = 'output'
DEFAULT_SAXON_EXECUTABLE = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)), 'resources', 'saxon9', 'saxon9he.jar')
SRA_DIR = os.path.join(os.path.dirname(__file__), 'resources', 'sra')
INPUT_FILE = os.path.join(SRA_DIR, 'blank.xml')
SUBMISSION_XSL_FILE = os.path.join(
    SRA_DIR, 'sra-submission-embl-online2isatab-txt.xsl')
STUDY_XSL_FILE = os.path.join(SRA_DIR, 'sra-study-embl-online2isatab.xsl')


log = logging.getLogger('isatools')

# REGEXES
_RX_ACCESSION_VALIDATION = re.compile("^(ERA|SRA|ERP|SRP)([0-9]+)$")


def zipdir(path, zip_file):
    """utility function to zip a whole directory"""
    # zip_file is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_file.write(os.path.join(root, file))


def format_acc_numbers(sra_acc_numbers):

    sra_acc_numbers = sra_acc_numbers.split(',') \
        if isinstance(sra_acc_numbers, str) else sra_acc_numbers

    # filter and clean the elements in the input array tomatch valid SRA types
    sra_acc_numbers = [elem.strip().upper() for elem in sra_acc_numbers]
    return [elem for elem in sra_acc_numbers
            if _RX_ACCESSION_VALIDATION.match(elem)]


@deprecated
def create_isatab_xslt(sra_acc_numbers, saxon_jar_path=None):
    """
    THIS METHOD IS DEPRECATED. USE sra_to_isatab_batch_convert INSTEAD.
    Given one or more SRA accession numbers (either to studies or submisssions),
    retrieve the files from the European Nucleotide Archive (ENA) server
    and convert them to ISA-tab using an XSL 2.0 transformation.
    The XSLT is invoked using an executable script.

    Notice: this method depend on SAXON XSLT Processor

    Parameters:
         :param sra_acc_numbers (str or list) - if a string must contain only
            comma separated valid SRA accession numbers
         :param saxon_jar_path str - if provided, must be a valid path
            pointing to SAXON Java JAR file. Otherwise, the
            default Saxon HE JAR will be used, if installed


    Returns:
        :returns zipfile.ZipFile if at least one of the SRA instances has been
            successfully converted
        :returns the output error otherwise (should this me modified?)

    """
    raise DeprecationWarning(
        'create_isatab_xslt() is deprecated, please use '
        'sra_to_isatab_batch_convert() instead')

    cmd_map = dict(posix='batch_sra2isatab.sh', nt=None, java=None, ce=None)

    formatted_sra_acc_numbers = format_acc_numbers(sra_acc_numbers)

    # convert the list back to a comma-separated string to be fed to the script
    sra_acc_numbers_str = ",".join(formatted_sra_acc_numbers)

    cmd_path = os.path.join(
        os.path.dirname(__file__), 'isa_line_commands', 'bin', cmd_map[os.name])
    pdb.set_trace()

    try:
        res = subprocess.check_output([cmd_path, sra_acc_numbers_str])

        # put all files within a zip file and return the file handler
        file_like_obj = BytesIO()

        # return ZIP file containing all the created ISA-tab documents
        with ZipFile(file_like_obj, 'w') as zip_file:
            zipdir(DESTINATION_DIR, zip_file)
            return zip_file

    except subprocess.CalledProcessError as err:
        logging.error(
            'isatools.convert.sra2isatab: CalledProcessError caught ',
            err.returncode)
        return err.output


def sra_to_isatab_batch_convert(
        sra_acc_numbers, saxon_jar_path=DEFAULT_SAXON_EXECUTABLE):
    """
    Given one or more SRA accession numbers (either to studies or submisssions),
    retrieve the files from the European Nucleotide Archive (ENA) server
    and convert them to ISA-tab using an XSL 2.0 transformation.
    The XSLT is invoked using an executable script.

    Notice: this method depends on The Saxon XSLT and XQuery Processor from
    Saxonica Limited (http://www.saxonica.com)

    Parameters:
         :param sra_acc_numbers (str or list) - if a string must contain only
            comma separated valid SRA accession numbers
         :param saxon_jar_path str - if provided, must be a valid path
            pointing to SAXON Java JAR file. Otherwise, the default Saxon HE
            JAR will be used, if installed


    Returns:zp
        :returns io.BytesIO if at least one of the SRA instances has been
        successfully converted (NOTE: should I return StringIO instead?)

    """
    res = None
    destination_dir = None

    log.info('This function utilises The Saxon XSLT and XQuery Processor from '
             'Saxonica Limited (http://www.saxonica.com)')

    try:
        dir_name = tempfile.mkdtemp()
        formatted_sra_acc_numbers = format_acc_numbers(sra_acc_numbers)
        buffer = BytesIO()

        destination_dir = os.path.abspath(dir_name)
        log.info('Destination dir is: ' + destination_dir)

        for acc_number in formatted_sra_acc_numbers:
            try:

                if acc_number.startswith('SRA') or acc_number.startswith('ERA'):
                    res = subprocess.call(
                        ['java', '-jar', saxon_jar_path, INPUT_FILE,
                         STUDY_XSL_FILE, 'acc-number='+acc_number,
                         'outputdir='+destination_dir])

                elif acc_number.startswith('SRP') or \
                        acc_number.startswith('ERP'):
                    res = subprocess.call(
                        ['java', '-jar', saxon_jar_path, INPUT_FILE,
                         SUBMISSION_XSL_FILE, 'acc-number='+acc_number,
                         'outputdir='+destination_dir])

                log.info('Subprocess Saxon exited with code: %d', res)

                # post-process concatenation of a_ files written out
                output_folder = os.path.join(dir_name, acc_number)
                a_files = [
                    f for f in os.listdir(output_folder) if f.startswith('a_')]
                if len(a_files) > 1:
                    import pandas as pd
                    df_list = list()
                    for a_file in a_files:
                        df = pd.DataFrame()
                        a_path = os.path.join(output_folder, a_file)
                        df_list.append(df.from_csv(a_path, sep='\t'))
                        os.remove(a_path)
                    merged_a_file = pd.concat(df_list)
                    merged_a_file.to_csv(
                        os.path.join(dir_name, acc_number,
                                     'a_{}.txt'.format(acc_number)), sep='\t')

                with ZipFile(buffer, 'w') as zip_file:
                    # use relative dir_name to avoid absolute path on file names
                    zipdir(dir_name, zip_file)

            except subprocess.CalledProcessError as err:
                log.error(
                    'isatools.convert.sra2isatab: CalledProcessError caught ',
                    err.returncode)
        # clean up the target directory after the ZIP file has been closed
        # rmtree(destination_dir)

        buffer.seek(0)
    finally:
        log.debug('Removing dir' + destination_dir)
        rmtree(destination_dir)
    return buffer

