import argparse
import sys
import os
import json


def main(argv=None):
    """Run **isatools** from the command line

    Arguments
        argv (list, optional): the list of arguments to run isatools
            with (if None, then sys.argv is used) [default: None]
    """
    p = argparse.ArgumentParser(prog=__name__,
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                description='''Create, convert, and manipulate ISA-formatted metadata''',
                                usage='isatools -c COMMAND [options]',
                                )

    p.add_argument('-c', dest='cmd', help='isatools API command to run', required=True,
                   choices=['isatab2json', 'json2isatab', 'sampletab2isatab', 'sampletab2json'])
    p.add_argument('-i', dest='in_path', help='in  (files or directory will be read from here)', required=True)
    p.add_argument('-o', dest='out_path', help='out (file will be written out here or written to directory if ISA-Tab '
                                               'archive out)', required=True)
    p.add_argument('--version', action='version', version='isatools {}'.format("0.7"))
    p.add_argument('-v', dest='verbose', help="show more output", action='store_true', default=False)

    args = p.parse_args(argv or sys.argv[1:])

    if args.verbose:
        print("{} input: {}".format(os.linesep, args.in_path))
        print("output: {}".format(args.out_path))

    if args.cmd == 'isatab2json':
        from isatools.convert import isatab2json
        J = isatab2json.convert(args.in_path)
        with open(args.out_path, 'w') as out_fp:
            json.dump(J, out_fp)

    elif args.cmd == 'json2isatab':
        from isatools.convert import json2isatab
        with open(args.in_path) as in_fp:
            json2isatab.convert(in_fp, args.out_path)

    elif args.cmd == 'sampletab2isatab':
        from isatools.convert import sampletab2isatab
        with open(args.in_path) as in_fp:
            sampletab2isatab.convert(in_fp, args.out_path)

    elif args.cmd == 'sampletab2json':
        from isatools.convert import sampletab2json
        with open(args.in_path) as in_fp:
            with open(args.out_path, 'w') as out_fp:
                sampletab2json.convert(in_fp, out_fp)

if __name__ == '__main__':
    main()
