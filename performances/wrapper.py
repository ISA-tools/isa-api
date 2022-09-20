from cProfile import Profile

from isatools.isajson import load
from performances.defaults import DEFAULT_JSON_INPUT


def wrapper(fn, **kwargs):
    pr = Profile()
    pr.enable()
    fn(**kwargs)
    pr.disable()
    pr.print_stats(sort='cumtime')


if __name__ == '__main__':
    with open(DEFAULT_JSON_INPUT, 'r') as isajson_fp:
        wrapper(load, isajson_fp)
