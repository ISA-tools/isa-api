import networkx as nx

from isatools.model.datafile import DataFile
from isatools.model.process import Process


def find(predictor, iterable):
    it = 0
    for element in iterable:
        if predictor(element):
            return element, it
        it += 1
    return None, it


def _build_assay_graph(process_sequence=None):
    """:obj:`networkx.DiGraph` Returns a directed graph object based on a
    given ISA process sequence."""
    g = nx.DiGraph()
    g.indexes = {}
    if process_sequence is None:
        return g
    for process in process_sequence:
        g.indexes[process.sequence_identifier] = process
        if process.next_process is not None or len(process.outputs) > 0:
            if len([n for n in process.outputs if not isinstance(n, DataFile)]) > 0:
                for output in [n for n in process.outputs if
                               not isinstance(n, DataFile)]:
                    g.add_edge(process.sequence_identifier, output.sequence_identifier)
                    g.indexes[output.sequence_identifier] = output
            else:
                next_process_identifier = getattr(process.next_process, "sequence_identifier", None)
                if next_process_identifier is not None:
                    g.add_edge(process.sequence_identifier, next_process_identifier)
                    g.indexes[next_process_identifier] = process.next_process

        if process.prev_process is not None or len(process.inputs) > 0:
            if len(process.inputs) > 0:
                for input_ in process.inputs:
                    g.add_edge(input_.sequence_identifier, process.sequence_identifier)
                    g.indexes[input_.sequence_identifier] = input_
            else:
                previous_process_identifier = getattr(process.prev_process, "sequence_identifier", None)
                if previous_process_identifier is not None:
                    g.add_edge(previous_process_identifier, process.sequence_identifier)
                    g.indexes[previous_process_identifier] = process.prev_process
    return g


def plink(p1, p2):
    """
    Function to create a link between two processes nodes of the isa graph
    :param Process p1: node 1
    :param Process p2: node 2
    """
    if isinstance(p1, Process) and isinstance(p2, Process):
        p1.next_process = p2
        p2.prev_process = p1
