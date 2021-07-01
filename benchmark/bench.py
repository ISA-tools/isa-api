from datetime import datetime
import os
from math import sqrt
from statistics import mean
from collections import namedtuple
from json import dump
from isatools.model import _build_assay_graph, Source
from isatools.isatab import _get_start_end_nodes, _longest_path_and_attrs, _all_end_to_end_paths

Series = namedtuple("Series", ["SD", "mean", "values"])


def benchmark_single_param(process_sequence, testable_function):
    """
    Benchmark the testable function and return the computed timer at that iterator
    :param process_sequence: the process_sequence to transform to a graph
    :param testable_function: function to test
    :return: the time it took to execute the function in microseconds
    """
    now = datetime.now()
    testable_function(process_sequence)
    after = datetime.now() - now
    return int(after.microseconds)


def benchmark_double_param(a, b, testable_function):
    """
    Benchmark the testable function and return the computed timer at that iterator
    :param a: first param
    :param b: second param
    :param testable_function: function to test
    :return: the time it took to execute the function in microseconds
    """
    now = datetime.now()
    testable_function(a, b)
    after = datetime.now() - now
    return int(after.microseconds)


def get_scores(series):
    """
    Returns a namedtuple containing the standard deviation (SD) and the mean of the given series
    :param series: the series to process
    :return {Namedtuple}
    """
    mean_value = mean(series)
    x = [abs(val - mean_value) ** 2 for val in series]
    return Series(sqrt(mean(x)), mean_value, series)


def bench(iterator, write=True):
    """
    Tests x times the given function the number where x = iterator
    :param iterator: the number of time to run the test
    :param write: save the output to file or not.
    :return {Namedtuple}: the output containing the SD and mean values for each series
    """

    from isatools.isatab import load
    filename = 'BII-S-3'
    input_filepath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        os.path.join('data', filename))
    investigation = load(input_filepath)
    Output = namedtuple("Timers", [
        "build_assay_graph",
        "get_start_end_nodes",
        "all_end_to_end_paths",
        "longest_path_and_attrs"
    ])
    graph = _build_assay_graph(investigation.studies[0].process_sequence)
    nodes = [x for x in investigation.studies[0].graph.nodes() if isinstance(x, Source)]
    paths = _all_end_to_end_paths(investigation.studies[0].graph, nodes)
    s1 = []
    s2 = []
    s3 = []
    s4 = []

    for i in range(iterator):
        timer1 = benchmark_single_param(investigation.studies[0].process_sequence, _build_assay_graph)
        timer2 = benchmark_single_param(graph, _get_start_end_nodes)
        timer3 = benchmark_double_param(investigation.studies[0].graph, nodes, _all_end_to_end_paths)
        timer4 = benchmark_single_param(paths, _longest_path_and_attrs)
        s1.append(timer1)
        s2.append(timer2)
        s3.append(timer3)
        s4.append(timer4)

    raw_output = Output(get_scores(s1), get_scores(s2), get_scores(s3), get_scores(s4))

    if write:
        with open('./benchmark/benchmark.json', 'w') as output_file:
            dump({
                "build_assay_graph": raw_output.build_assay_graph._asdict(),
                "get_start_end_nodes": raw_output.get_start_end_nodes._asdict(),
                "all_end_to_end_paths": raw_output.all_end_to_end_paths._asdict(),
                "longest_path_and_attrs": raw_output.longest_path_and_attrs._asdict()
            }, output_file, indent=4)
            output_file.close()


if __name__ == '__main__':
    bench(1000)

