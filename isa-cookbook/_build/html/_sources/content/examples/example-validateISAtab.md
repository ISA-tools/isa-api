validateISAtab.py
=================

An example program using the ISA-Tab validator to validate one or more
ISA-Tab archives.

```python
#!/usr/bin/env python

# Inspired by validateSBML.py example from libSBML Python API

from isatools import isatab
import sys
import os


def main(args):
    """usage: validateISAtab.py inputfile1 [inputfile2 ...]
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
        print("---------------------------------------------------------------------------")
        if not os.path.isfile(args[i]):
            print("Cannot open file {}, skipping".format(args[i]))
            skipped += 1
            numfiles += 1
        else:
            with open(args[i]) as fp:
                report = isatab.validate(fp)
                numerrors = len(report['errors'])
                numwarnings = len(report['warnings'])
                if numerrors > 0:
                    invalid += 1
                print("Validator found {} errors and {} warnings in this ISA-Tab archive".format(numerrors, numwarnings))
                totalerrors += numerrors
                totalwarnings += numwarnings
                numfiles += 1
    print("---------------------------------------------------------------------------")
    print("Validated {} ISA-Tab archives, {} valid ISA-Tab archives, {} invalid ISA-Tab archives"
          .format(numfiles - skipped, numfiles - invalid - skipped, invalid))
    print("Found {} errors and {} warnings in across all ISA-Tab archives".format(totalerrors, totalwarnings))

    if invalid > 0:
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv)
```
