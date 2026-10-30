"""Functions for importing SRA from various sources"""


import logging
import pdb
import re
import subprocess
import tempfile
from io import BytesIO
from os import listdir, path, remove, walk
from shutil import rmtree
from zipfile import ZipFile

__author__ = "massi"

DESTINATION_DIR = "output"
DEFAULT_SAXON_EXECUTABLE = path.join(path.dirname(path.abspath(__file__)), "resources", "saxon9", "saxon9he.jar")
SRA_DIR = path.join(path.dirname(__file__), "resources", "sra")
INPUT_FILE = path.join(SRA_DIR, "blank.xml")
SUBMISSION_XSL_FILE = path.join(SRA_DIR, "sra-submission-embl-online2isatab-txt.xsl")
STUDY_XSL_FILE = path.join(SRA_DIR, "sra-study-embl-online2isatab.xsl")
_RX_ACCESSION_VALIDATION = re.compile(r"^(ERA|SRA|ERP|SRP)([0-9]+)$")

log = logging.getLogger("isatools")


def zipdir(_path, zip_file):
    """utility function to zip a whole directory"""
    [[zip_file.write(path.join(root, file)) for file in files] for root, dirs, files in walk(_path)]


def format_acc_numbers(sra_acc_numbers):
    sra_acc_numbers = sra_acc_numbers.split(",") if isinstance(sra_acc_numbers, str) else sra_acc_numbers
    sra_acc_numbers = [elem.strip().upper() for elem in sra_acc_numbers]
    return [elem for elem in sra_acc_numbers if _RX_ACCESSION_VALIDATION.match(elem)]


def sra_to_isatab_batch_convert(sra_acc_numbers, saxon_jar_path=DEFAULT_SAXON_EXECUTABLE):
    """
    Given one or more SRA accession numbers (either to studies or
    submisssions),
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

    log.info("This function uses The Saxon XSLT and XQuery Processor from Saxonica Limited (http://www.saxonica.com)")

    try:
        dir_name = tempfile.mkdtemp()
        formatted_sra_acc_numbers = format_acc_numbers(sra_acc_numbers)
        buffer = BytesIO()

        destination_dir = path.abspath(dir_name)
        log.info("Destination dir is: %s" % destination_dir)

        for acc_number in formatted_sra_acc_numbers:
            try:
                # TODO: Remove temporary subprocess output capture once Saxon diagnosis is complete.
                if acc_number.startswith("SRA") or acc_number.startswith("ERA"):
                    res = subprocess.run(
                        [
                            "java",
                            "-jar",
                            saxon_jar_path,
                            INPUT_FILE,
                            STUDY_XSL_FILE,
                            "acc-number=" + acc_number,
                            "outputdir=" + destination_dir,
                        ],
                        capture_output=True,
                        text=True,
                    )

                elif acc_number.startswith("SRP") or acc_number.startswith("ERP"):
                    res = subprocess.run(
                        [
                            "java",
                            "-jar",
                            saxon_jar_path,
                            INPUT_FILE,
                            SUBMISSION_XSL_FILE,
                            "acc-number=" + acc_number,
                            "outputdir=" + destination_dir,
                        ],
                        capture_output=True,
                        text=True,
                    )

                # TODO: Remove temporary diagnostics at ERROR level once Saxon diagnosis is complete.
                # ERROR ensures the diagnostics are visible with the default logging configuration.
                log.error(
                    "Saxon diagnostics for %s: exit code %d\nstdout:\n%s\nstderr:\n%s",
                    acc_number,
                    res.returncode,
                    res.stdout,
                    res.stderr,
                )
                log.info("Subprocess Saxon exited with code: %d", res.returncode)

                # post-process concatenation of a_ files written out
                output_folder = path.join(dir_name, acc_number)
                a_files = [f for f in listdir(output_folder) if f.startswith("a_")]
                if len(a_files) > 1:
                    import pandas as pd

                    df_list = list()
                    for a_file in a_files:
                        df = pd.DataFrame()
                        a_path = path.join(output_folder, a_file)
                        df_list.append(df.from_csv(a_path, sep="\t"))
                        remove(a_path)
                    merged_a_file = pd.concat(df_list)
                    merged_a_file.to_csv(path.join(dir_name, acc_number, f"a_{acc_number}.txt"), sep="\t")

                with ZipFile(buffer, "w") as zip_file:
                    zipdir(dir_name, zip_file)

            except subprocess.CalledProcessError as err:
                log.error("isatools.net.sra2isatab: CalledProcessError caught ", err.returncode)
        buffer.seek(0)
    finally:
        log.debug("Removing dir" + destination_dir)
        rmtree(destination_dir)
    return buffer
