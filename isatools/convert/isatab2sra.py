import sys
import os


def create_sra(source_path="", dest_path=""):
    print("Source: " + source_path)
    print("Dest: " + dest_path)
    convert_command = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "isa_line_commands/bin/convert.sh -t sra " + source_path + " " + dest_path)
    from subprocess import call
    try:
        return_code = call([convert_command], shell=True)
        if return_code < 0:
            print(sys.stderr, "Terminated by signal", -return_code)
        else:
            print(sys.stderr, "Returned", return_code)
    except OSError as e:
        print(sys.stderr, "Execution failed:", e)

