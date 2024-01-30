from networkx import algorithms

from isatools.model import Source, Sample, Process, Material, DataFile
from isatools.isatab.defaults import log


def _all_end_to_end_paths(G, start_nodes):
    """Find all the end-to-end complete paths using a networkx algorithm that
    uses a modified depth-first search to generate the paths

    :param G: A DiGraph of all the assay graphs from the process sequences
    :param start_nodes: A list of start nodes
    :return: A list of paths from the start nodes
    """
    # we know graphs start with Source or Sample and end with Process
    paths = []
    num_start_nodes = len(start_nodes)
    message = 'Calculating for paths for {} start nodes: '.format(
        num_start_nodes)
    # log.info(start_nodes)
    start_node = G.indexes[start_nodes[0]]
    if isinstance(start_node, Source):
        message = 'Calculating for paths for {} sources: '.format(
            num_start_nodes)
    elif isinstance(start_node, Sample):
        message = 'Calculating for paths for {} samples: '.format(
            num_start_nodes)
    """if isa_logging.show_pbars:
        pbar = ProgressBar(
            min_value=0, max_value=num_start_nodes, widgets=[
                message, SimpleProgress(), Bar(left=" |", right="| "),
                ETA()]).start()
    else:
        def pbar(x): return x"""
    for start in start_nodes:
        # Find ends
        node = G.indexes[start]
        if isinstance(node, Source):
            # only look for Sample ends if start is a Source
            for end in [x for x in algorithms.descendants(G, start) if
                        isinstance(G.indexes[x], Sample) and len(G.out_edges(x)) == 0]:
                paths += list(algorithms.all_simple_paths(G, start, end))
        elif isinstance(node, Sample):
            # only look for Process ends if start is a Sample
            for end in [x for x in algorithms.descendants(G, start) if
                        isinstance(G.indexes[x], Process) and G.indexes[x].next_process is None]:
                paths += list(algorithms.all_simple_paths(G, start, end))
    # log.info("Found {} paths!".format(len(paths)))
    if len(paths) == 0:
        log.debug([G.indexes[x].name for x in start_nodes])
    return paths


def _longest_path_and_attrs(paths, indexes):
    """Function to find the longest paths and attributes to determine the
    most appropriate ISA-Tab header. This is calculated by adding up the length
    of each path with the number of attributes needed to describe each node in
    the graph.

    :param paths: List of end-to-end paths in the graphs
    :return: The longest path and attributes
    """
    longest = (0, None)
    # log.info(paths)
    for path in paths:
        length = len(path)
        for node in path:
            n = indexes[node]
            if isinstance(n, Source):
                length += len(n.characteristics)
            elif isinstance(n, Sample):
                length += (len(n.characteristics) + len(n.factor_values))
            elif isinstance(n, Material):
                length += (len(n.characteristics))
            elif isinstance(n, Process):
                length += len(
                    [o for o in n.outputs if isinstance(o, DataFile)])
                if n.date is not None:
                    length += 1
                if n.performer is not None:
                    length += 1
                if n.name != '':
                    length += 1
            if n.comments is not None:
                length += len(n.comments)
        if length > longest[0]:
            longest = (length, path)
    return longest[1]


def _get_start_end_nodes(G):
    """Find the start and end nodes of the graphs

    :param G: A DiGraph of process sequences
    :return: start nodes (Materials) and end nodes (Processes)
    """
    start_nodes = list()
    end_nodes = list()
    for process in [n for n in G.nodes() if isinstance(n, Process)]:
        if process.prev_process is None:
            for material in [m for m in process.inputs if not isinstance(m, DataFile)]:
                start_nodes.append(material)
        outputs_no_data = [
            m for m in process.outputs if not isinstance(m, DataFile)]
        if process.next_process is None:
            if len(outputs_no_data) == 0:
                end_nodes.append(process)
            else:
                for material in outputs_no_data:
                    end_nodes.append(material)
    return start_nodes, end_nodes
