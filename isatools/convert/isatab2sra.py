import sys
import os


def create_sra(source_path="", dest_path="", config_path=""):
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

        Raises:
            OSErrpr: If something goes wrong calling the shell commands to run the
            Java conversion, this will raise an OSError

    """
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
    from subprocess import call
    try:
        return_code = call([convert_command], shell=True)
        if return_code < 0:
            print(sys.stderr, "Terminated by signal", -return_code)
        else:
            print(sys.stderr, "Returned", return_code)
    except OSError as e:
        print(sys.stderr, "Execution failed:", e)

