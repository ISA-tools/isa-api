import subprocess
import os
import re
from io import BytesIO, StringIO
from zipfile import ZipFile
from shutil import rmtree
import logging
import pdb
import uuid

__author__ ='massi'

DESTINATION_DIR = 'output'
DEFAULT_SAXON_DIR = os.path.join(os.path.expanduser('~'), 'Applications', 'SaxonHE')
DEFAULT_SAXON_EXECUTABLE = os.path.join(DEFAULT_SAXON_DIR, 'saxon9he.jar')
SRA_DIR = os.path.join(os.path.dirname(__file__), 'resources', 'sra')
INPUT_FILE = os.path.join(SRA_DIR, 'blank.xml')
SUBMISSION_XSL_FILE = os.path.join(SRA_DIR, 'sra-submission-embl-online2isatab-txt.xsl')
STUDY_XSL_FILE = os.path.join(SRA_DIR, 'sra-study-embl-online2isatab.xsl')

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def zipdir(path, zip_file):
    """utility function to zip a whole directory"""
    # zip_file is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_file.write(os.path.join(root, file))


def format_acc_numbers(sra_acc_numbers):

    sra_acc_numbers = sra_acc_numbers.split(',') if isinstance(sra_acc_numbers, str) else sra_acc_numbers

    # RegExp to validate the accession number
    pattern = re.compile("^(ERA|SRA|ERP|SRP)([0-9]+)$")

    # filter and clean the elements in the input array tomatch valid SRA types
    sra_acc_numbers = [elem.strip().upper() for elem in sra_acc_numbers]
    return [elem for elem in sra_acc_numbers if pattern.match(elem)]


def create_isatab_xslt(sra_acc_numbers, saxon_jar_path=None):
    """
    THIS METHOD IS DEPRECATED. USE sra_to_isatab_batch_convert INSTEAD.
    Given one or more SRA accession numbers (either to studies or submisssions),
    retrieve the files from the European Nucleotide Archive (ENA) server
    and convert them to ISA-tab using an XSL 2.0 transformation.
    The XSLT is invoked using an executable script.

    Notice: this method depend on SAXON XSLT Processor

    Parameters:
         :param sra_acc_numbers (str or list) - if a string must contain only comma separated valid SRA accession numbers
         :param saxon_jar_path str - if provided, must be a valid path pointing to SAXON Java JAR file. Otherwise, the
                                     default Saxon HE JAR will be used, if installed


    Returns:
        :returns zipfile.ZipFile if at least one of the SRA instances has been successfully converted
        :returns the output error otherwise (should this me modified?)

    """
    cmd_map = dict(posix='batch_sra2isatab.sh', nt=None, java=None, ce=None)

    formatted_sra_acc_numbers = format_acc_numbers(sra_acc_numbers)

    # convert the list back to a comma-separated string to be fed to the script
    sra_acc_numbers_str = ",".join(formatted_sra_acc_numbers)

    cmd_path = os.path.join(os.path.dirname(__file__), 'isa_line_commands', 'bin', cmd_map[os.name])
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
        logging.error("isatools.convert.sra2isatab: CalledProcessError caught ", err.returncode)
        return err.output


def sra_to_isatab_batch_convert(sra_acc_numbers, saxon_jar_path=DEFAULT_SAXON_EXECUTABLE):
    """
    Given one or more SRA accession numbers (either to studies or submisssions),
    retrieve the files from the European Nucleotide Archive (ENA) server
    and convert them to ISA-tab using an XSL 2.0 transformation.
    The XSLT is invoked using an executable script.

    Notice: this method depend on SAXON XSLT Processor

    Parameters:
         :param sra_acc_numbers (str or list) - if a string must contain only comma separated valid SRA accession numbers
         :param saxon_jar_path str - if provided, must be a valid path pointing to SAXON Java JAR file. Otherwise, the
                                     default Saxon HE JAR will be used, if installed


    Returns:zp
        :returns io.BytesIO if at least one of the SRA instances has been successfully converted
                 (NOTE: should I return StringIO instead?)

    """
    res = None
    dir_name = uuid.uuid4().hex
    formatted_sra_acc_numbers = format_acc_numbers(sra_acc_numbers)
    buffer = BytesIO()

    destination_dir = os.path.abspath(dir_name)
    print('Destination dir is: ' + destination_dir)
    logger.info('Destination dir is: ' + destination_dir)

    if os.path.exists(destination_dir):
        logger.debug('Removing dir' + destination_dir)
        print('Removing dir' + destination_dir)
        rmtree(destination_dir)

    for acc_number in formatted_sra_acc_numbers:
        try:

            if acc_number.startswith('SRA') or acc_number.startswith('ERA'):
                res = subprocess.call(['java', '-jar', saxon_jar_path, INPUT_FILE, STUDY_XSL_FILE,
                                       'acc-number='+acc_number, 'outputdir='+destination_dir])

            elif acc_number.startswith('SRP') or acc_number.startswith('ERP'):
                res = subprocess.call(['java', '-jar', saxon_jar_path, INPUT_FILE, SUBMISSION_XSL_FILE,
                                 'acc-number='+acc_number, 'outputdir='+destination_dir])

            logger.info('Subprocess Saxon exited with code: %d', res)

        except subprocess.CalledProcessError as err:
            logger.error("isatools.convert.sra2isatab: CalledProcessError caught ", err.returncode)

    with ZipFile(buffer, 'w') as zip_file:
        # use relative dir_name to avoid absolute path on file names
        zipdir(dir_name, zip_file)
        print(zip_file.namelist())

    # clean up the target directory after the ZIP file has been closed
    rmtree(destination_dir)

    buffer.seek(0)
    return buffer






