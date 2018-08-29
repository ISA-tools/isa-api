#!/usr/bin/env python

# Inspired by validateSBML.py example from libSBML Python API

from isatools import isajson
import sys
import os


def main(args):
    """usage: validateISAjson.py inputfile1 [inputfile2 ...]
    """
    if len(args) < 1:
        print(main.__doc__)
        sys.exit(1)

    numfiles = 0
    invalid = 0
    skipped = 0

    totalerrors = 0
    totalwarnings = 0

    for i in range(1, len(args)):
        print("-" * 75)
        if not os.path.isfile(args[i]):
            print("Cannot open file {}, skipping".format(args[i]))
            skipped += 1
            numfiles += 1
        else:
            with open(args[i]) as fp:
                report = isajson.validate(fp)
                numerrors = len(report['errors'])
                numwarnings = len(report['warnings'])
                if numerrors > 0:
                    invalid += 1
                print("Validator found {} errors and {} warnings in this "
                      "ISA-JSON file".format(numerrors, numwarnings))
                totalerrors += numerrors
                totalwarnings += numwarnings
                numfiles += 1
        print("-" * 75)
    print("Validated {} ISA-JSONs, {} valid ISA-JSONs, {} invalid ISA-JSONs"
          .format(numfiles - skipped, numfiles - invalid - skipped, invalid))
    print("Found {} errors and {} warnings in across all ISA-JSONs".format(
        totalerrors, totalwarnings))

    if invalid > 0:
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
