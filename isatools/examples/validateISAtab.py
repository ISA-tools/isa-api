#!/usr/bin/env python

# Inspired by validateSBML.py example from libSBML Python API

import os
import sys

from isatools import isatab


def main(args):
    """usage: validateISAtab.py inputfile1 [inputfile2 ...]"""
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
            print(f"Cannot open file {args[i]}, skipping")
            skipped += 1
            numfiles += 1
        else:
            with open(args[i]) as fp:
                report = isatab.validate(fp)
                numerrors = len(report["errors"])
                numwarnings = len(report["warnings"])
                if numerrors > 0:
                    invalid += 1
                print(
                    f"Validator found {numerrors} errors and {numwarnings} warnings in this ISA-Tab archive"
                )
                totalerrors += numerrors
                totalwarnings += numwarnings
                numfiles += 1
        print("-" * 75)
    print(
        f"Validated {numfiles - skipped} ISA-Tab archives, {numfiles - invalid - skipped} valid ISA-Tab archives, {invalid} invalid ISA-Tab archives"
    )
    print(f"Found {totalerrors} errors and {totalwarnings} warnings in across all ISA-Tab archives")

    if invalid > 0:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
