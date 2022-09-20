import argparse
import sys


from performances.isatab import profile_isatab
from performances.isajson import profile_isajson


def main(argv=None):
    parser = argparse.ArgumentParser(description='CLI tool for profiling isa-tools',
                                     usage='python -m performances [options]')
    parser.add_argument('-j', '--json',
                        help='Run performance tests on the given ISA json', required=False, dest='json', type=str,
                        const='./tests/data/json/BII-S-3/BII-S-3.json', nargs='?')
    parser.add_argument('-t', '--tab',
                        help='Run performance tests on the given ISA tab', required=False, dest='tab', type=str,
                        const='./tests/data/tab/BII-S-3/i_gilbert.txt', nargs='?')
    parser.add_argument('-o', '--output',
                        help='Output path for the profiles', required=False, dest='output', type=str)
    args = parser.parse_args(argv or sys.argv[1:])

    if not args.tab and not args.json:
        profile_isajson()
        profile_isatab()

    if args.tab:
        profile_isatab(args.tab, args.output)

    if args.json:
        profile_isajson(args.json, args.output)


if __name__ == '__main__':
    main()
