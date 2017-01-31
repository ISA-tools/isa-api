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
                   choices=['isatab2json', 'json2isatab', 'isatab2sra', 'json2sra', 'zipisatab'])
    p.add_argument('-i', dest='in_path', help='in folder (files will be read from here)', required=True)
    p.add_argument('-o', dest='out_path', help='out folder (a new directory will be created here)', required=True)
    p.add_argument('--version', action='version', version='isatools {}'.format("0.6"))
    p.add_argument('-v', dest='verbose', help="show more output", action='store_true', default=False)

    args = p.parse_args(argv or sys.argv[1:])

    if args.verbose:
        print("{} input path: {}".format(os.linesep, args.in_path))
        print("output path: {}".format(args.out_path))

    if args.cmd == 'isatab2json':
        from isatools.convert import isatab2json
        J = isatab2json.convert(args.in_path)
        with open(args.out_path, 'w') as out_fp:
            json.dump(J, out_fp)

    elif args.cmd == 'json2isatab':
        from isatools.convert import json2isatab
        with open(args.in_path) as in_fp:
            json2isatab.convert(in_fp, args.out_path)

    elif args.cmd == 'isatab2sra':
        raise NotImplementedError  # TODO: Finish this

    elif args.cmd == 'json2sra':
        raise NotImplementedError  # TODO: Finish this

    elif args.cmd == 'zipisatab':
        raise NotImplementedError  # TODO: Finish this

if __name__ == '__main__':
    main()
