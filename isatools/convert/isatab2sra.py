import sys
import os
import pdb
import subprocess
from io import BytesIO
from zipfile import ZipFile
from shutil import rmtree


def zipdir(path, zip_file):
    """utility function to zip a whole directory"""
    # zip_file is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_file.write(os.path.join(root, file),
                           arcname=os.path.join(os.path.basename(root), file))


def create_sra(source_path, dest_path, config_path):
    """ This function converts a set of ISA-Tab files into SRA XML format.

        The SRA conversion uses the Java compiled validator and converter, packaged
        under the isa_line_commands package. Take note that this requires bash and
        at least a Java Runtime Environment for Java 6.

        Args:
            source_path (str): Path to the source ISA-Tab files directory.
            dest_path (str): Path to the destination directory where SRA XML files
                will be written to. Note that the converter will automatically create
                sub-directory /sra under where you specify the dest_path.
            config_path (str): Path to the ISA Configuration XML files to validate
                the input ISA-Tab.
            log_file (str): the absolute or realtive path to the log file where

        Raises:
            TypeErrpr: If something goes wrong calling the shell commands to run the
            Java conversion, this will raise a TypeError (NOTE: should this error be customised?)

    """
    source_path = os.path.abspath(source_path)
    dest_path = os.path.abspath(dest_path)
    config_path = os.path.abspath(config_path)

    if not os.path.exists(source_path):
        raise IOError("source_path " + source_path + " does not exist")
    if not os.path.exists(dest_path):
        raise IOError("dest_path " + dest_path + " does not exist")
    if not os.path.exists(config_path):
        raise IOError("config_path " + config_path + " does not exist")
    print("Using source ISA Tab folder: " + source_path)
    print("Writing to destination SRA folder: " + dest_path)
    print("ISA configuration XML folder: " + config_path)
    convert_command = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "isa_line_commands/bin/convert.sh -t sra " +
                                   source_path + " " +
                                   dest_path + " " +
                                   config_path)
    print(convert_command)
    # subprocess.call(['java', '-version'])

    # return_code = subprocess.call([convert_command], shell=True)
    try:
        res = subprocess.check_output([convert_command], shell=True, stderr=subprocess.STDOUT)

        # with open(log_file, 'w') as logf:
        #     logf.write(str(res, encoding='utf-8'))

    except subprocess.CalledProcessError as err:
        print("Execution failed: ", err.output)
        error_message = str(err.output, encoding='utf-8')
        raise TypeError(error_message)

    # returns the buffer containing the SRA element(s) as an archive
    buffer = BytesIO()
    sra_dir = os.path.join(dest_path, 'sra')

    if os.path.isdir(sra_dir):
        with ZipFile(buffer, 'w') as zip_file:
            # use relative dir_name to avoid absolute path on file names
            zipdir(sra_dir, zip_file)
            print(zip_file.namelist())

            # clean up the target directory after the ZIP file has been closed
            # rmtree(sra_dir)

        buffer.seek(0)
        return buffer

    else:
        raise TypeError("The provided ISA tab could not be converted to SRA")



