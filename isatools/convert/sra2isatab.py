import subprocess
import os
import re
from io import BytesIO
from zipfile import ZipFile

__author__ ='massi'

DESTINATION_DIR = 'output'


def zipdir(path, zip_file):
    "utility function to zip a whole directory"
    # zip_file is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_file.write(os.path.join(root, file))


def create_isatab_xslt(sra_acc_numbers, saxon_jar_path=None):
    """
    Given one or more SRA accession numbers (either to studies or submisssions),
    retrieve the files from the European Nucleotide Archive (ENA) server
    and convert them to ISA-tab using an XSL 2.0 transformation.
    The XSLT is invoked using an executable script.
     Notice: this method depend on SAXON XSLT Processor
    """
    cmd_map = dict(posix='batch_sra2isatab.sh', nt=None, java=None, ce=None)

    sra_acc_numbers = sra_acc_numbers.split(',') if isinstance(sra_acc_numbers, str) else sra_acc_numbers

    pattern = re.compile("^[ERA|SRA|ERP|SRP]")

    # filter and clean the elements in the input array tomatch valid SRA types
    sra_acc_numbers = [elem.strip().upper() for elem in sra_acc_numbers if pattern.match(elem)]

    # convert the list back to a comma-separated string to be fed to the script
    sra_acc_numbers_str = ",".join(sra_acc_numbers)

    cmd_path = os.path.join(os.path.dirname(__file__), 'isa_line_commands', 'bin', cmd_map[os.name])

    try:
        res = subprocess.call([cmd_path, sra_acc_numbers_str], shell=True)

        # put all files within a zip file and return the file handler
        file_like_obj = BytesIO()

        # return ZIP file conatining all the created ISA-tab documenets
        with ZipFile(file_like_obj) as zip_file:
            zipdir(DESTINATION_DIR, zip_file)
            return zip_file

    except subprocess.CalledProcessError as err:
        print("isatools.convert.sra2isatab: CalledProcessError caught ", err.returncode)
        return err.output


