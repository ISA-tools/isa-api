import itertools
import networkx as nx

from isatools.model.datafile import DataFile
from isatools.model.process import Process
from isatools.model.source import Source
from isatools.model.sample import Sample
from isatools.model.material import Material


def find(predictor, iterable):
    it = 0
    for element in iterable:
        if predictor(element):
            return element, it
        it += 1
    return None, it


def _compute_combinations(identifier_list, identifiers_to_objects):
    """Compute the combinations of identifiers in identifier_list.

    Return a list of the combinations of identifiers in identifier_list based
    on the input/output type.

    :param list identifier_list: a list of identifiers to create combinations out of.
    :param dict identifiers_to_objects: a dictionary mapping the identifiers to objects, used to determine IO type.
    :returns: a list of tuples where each tuple is a combination of the identifiers.
    """
    io_types = {}
    for identifier in identifier_list:
        io_object = identifiers_to_objects[identifier]
        if isinstance(io_object, DataFile):
            label = io_object.label
            if label not in io_types:
                io_types[label] = [identifier]
            else:
                io_types[label].append(identifier)
        else:
            if "Material" not in io_types:
                io_types["Material"] = [identifier]
            else:
                io_types["Material"].append(identifier)
    combinations = [item for item in list(itertools.product(*[values for values in io_types.values()])) if item]
    return combinations


def _expand_path(path, identifiers_to_objects, dead_end_outputs):
    """Expand the path by adding additional nodes if possible.

    :param list path: a list of identifiers representing a path to be expanded.
    :param dict identifiers_to_objects: a dictionary mapping the identifiers to objects, used to determine IO type.
    :param set dead_end_outputs: a set of identifiers that are outputs which are not correspondingly inputs.
    :returns: a list of lists where each list is an expansion of the path, and a boolean that is true if the path was able to be expanded.
    """
    new_paths = []
    path_len = len(path)
    path_modified = False
    for i, identifier in enumerate(path):
        node = identifiers_to_objects[identifier]
        # If the node is a process at beginning of the path, add a path for each of its inputs.
        if i == 0 and isinstance(node, Process):
            identifier_list = [input_.sequence_identifier for input_ in node.inputs]
            combinations = _compute_combinations(identifier_list, identifiers_to_objects)
            for combo in combinations:
                new_path = list(combo) + path
                path_modified = True
                if new_path not in new_paths:
                    new_paths.append(new_path)
            continue

        # If the node is a process at the end of the path, add a path for each of its outputs.
        if i == path_len - 1 and isinstance(node, Process):
            identifier_list = [output.sequence_identifier for output in node.outputs]
            combinations = _compute_combinations(identifier_list, identifiers_to_objects)
            for combo in combinations:
                new_path = path + list(combo)
                path_modified = True
                if new_path not in new_paths:
                    new_paths.append(new_path)
            continue

        # If the node is a process in the middle of the path and the next node in the path is also a process,
        # add paths for each output that is also an input to the next process.
        if i + 1 < path_len and isinstance(identifiers_to_objects[path[i + 1]], Process) and i > 0 and isinstance(node,
                                                                                                                  Process):
            output_sequence_identifiers = {output.sequence_identifier for output in node.outputs}
            input_sequence_identifiers = {input_.sequence_identifier for input_ in
                                          identifiers_to_objects[path[i + 1]].inputs}
            identifier_intersection = list(output_sequence_identifiers.intersection(input_sequence_identifiers))

            combinations = _compute_combinations(identifier_intersection, identifiers_to_objects)
            for combo in combinations:
                new_path = path[0:i + 1] + list(combo) + path[i + 1:]
                path_modified = True
                if new_path not in new_paths:
                    new_paths.append(new_path)

            # Add outputs that aren't later used as inputs.
            for output in output_sequence_identifiers.intersection(dead_end_outputs):
                new_path = path[:i + 1] + [output]
                path_modified = True
                if new_path not in new_paths:
                    new_paths.append(new_path)
            continue
    return new_paths, path_modified


def _build_paths_and_indexes(process_sequence=None):
    """Find all the paths within process_sequence and all the nodes.

    :param list process_sequence: a list of processes.
    :returns: The paths from source/sample to end points and a mapping of sequence_identifier to object.
    """
    # Determining paths depends on processes having next and prev sequence, so add
    # them if they aren't there based on inputs and outputs.
    inputs_to_process = {id(p_input): {"process": process, "input": p_input} for process in process_sequence for p_input
                         in process.inputs}
    outputs_to_process = {id(output): {"process": process, "output": output} for process in process_sequence for output
                          in process.outputs}
    for output, output_dict in outputs_to_process.items():
        if output in inputs_to_process:
            if not inputs_to_process[output]["process"].prev_process:
                inputs_to_process[output]["process"].prev_process = output_dict["process"]
            if not output_dict["process"].next_process:
                output_dict["process"].next_process = inputs_to_process[output]["process"]

    paths = []
    identifiers_to_objects = {}
    all_inputs = set()
    all_outputs = set()
    # For each process in the process sequence create a list of sequence identifiers representing
    # the path obtained by simply following the next and prev sequences. Also create a dictionary,
    # identifiers_to_objects to be able to easily reference an object from its identifier later.
    for process in process_sequence:

        identifiers_to_objects[process.sequence_identifier] = process
        for output in process.outputs:
            identifiers_to_objects[output.sequence_identifier] = output
            all_outputs.add(output.sequence_identifier)
        for input_ in process.inputs:
            identifiers_to_objects[input_.sequence_identifier] = input_
            all_inputs.add(input_.sequence_identifier)

        original_process = process

        right_processes = []
        while next_process := process.next_process:
            right_processes.append(next_process.sequence_identifier)
            process = next_process

        left_processes = []
        process = original_process
        while prev_process := process.prev_process:
            left_processes.append(prev_process.sequence_identifier)
            process = prev_process
        left_processes = list(reversed(left_processes))

        paths.append(left_processes + [original_process.sequence_identifier] + right_processes)

    # Trim paths down to only the unique paths.
    unique_paths = [list(x) for x in set(tuple(x) for x in paths)]
    paths = unique_paths
    dead_end_outputs = all_outputs - all_inputs

    # Paths have to be expanded out combinatorially based on inputs and outputs.
    # paths is only processes, so expand them out to include inputs and outputs.
    str_path_to_path = {}
    was_path_modified = {}
    paths_seen = []
    paths_seen_twice = []
    # Keep looping until there are no new paths created.
    while True:
        new_paths = []
        paths_seen_changed = False
        for path in paths:
            str_path = str(path)
            str_path_to_path[str_path] = path
            if path not in paths_seen:
                paths_seen.append(path)
                paths_seen_changed = True
            else:
                paths_seen_twice.append(path)
                continue
            expanded_paths, path_modified = _expand_path(path, identifiers_to_objects, dead_end_outputs)
            new_paths += expanded_paths
            # This is supposed to catch different length paths.
            if not path_modified and path not in new_paths:
                new_paths.append(path)

            # Keep track of which paths are modified to use as a filter later.
            if str_path in was_path_modified:
                if path_modified:
                    was_path_modified[str_path] = path_modified
            else:
                was_path_modified[str_path] = path_modified
        if not paths_seen_changed:
            break
        paths = new_paths

    # Ultimately only keep the paths created in the loop that were never modified.
    paths = [str_path_to_path[path] for path, was_modified in was_path_modified.items() if not was_modified]

    return paths, identifiers_to_objects


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
    """Function to create a link between two processes nodes of the isa graph

    :param Process p1: node 1
    :param Process p2: node 2
    """
    if isinstance(p1, Process) and isinstance(p2, Process):
        p1.next_process = p2
        p2.prev_process = p1


def batch_create_materials(material=None, n=1):
    """Creates a batch of material objects (Source, Sample or Material) from a
    prototype material object

    :param material: existing material object to use as a prototype
    :param n: Number of material objects to create in the batch
    :returns: List of material objects

    :Example:

        # Create 10 sample materials derived from one source material

        source = Source(name='source_material')
        prototype_sample = Sample(name='sample_material', derives_from=[source])
        batch = batch_create_materials(prototype_sample, n=10)

        [Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>, Sample<>,
        Sample<>, Sample<>, Sample<>, ]

    """
    material_list = list()
    if isinstance(material, (Source, Sample, Material)):
        for x in range(0, n):
            new_obj = _deep_copy(material)
            new_obj.name = material.name + '-' + str(x)
            if hasattr(material, 'derives_from'):
                new_obj.derives_from = material.derives_from

            material_list.append(new_obj)

    return material_list


def batch_create_assays(*args, n=1):
    """Creates a batch of assay process sequences (Material->Process->Material)
    from a prototype sequence (currently works only as flat end-to-end
    processes of Material->Process->Material->...)

    # :param *args: An argument list representing the process sequence prototype
    :param n: Number of process sequences to create in the batch
    :returns: List of process sequences replicating the prototype sequence

    :Example:

        # Create 3 assays of (Sample -> Process -> Material -> Process ->
        LabeledExtract)

        sample = Sample(name='sample', derives_from=[Source(name='source')])
        data_acquisition = Process(name='data acquisition')
        material = Material(name='material')
        labeling = Process(name='labeling')
        extract = LabeledExtract(name='lextract')
        batch = batch_create_assays(sample, data_acquisition, material,
        labeling, extract, n=3)

        [Process<> Process<>, Process<> Process<>, Process<>, Process<>]

        # Create 3 assays of ([Sample, Sample] -> Process -> [Material,
        Material])

        sample1 = Sample(name='sample')
        sample2 = Sample(name='sample')
        process = Process(name='data acquisition')
        material1 = Material(name='material')
        material2 = Material(name='material')
        batch = batch_create_assays([sample1, sample2], process, [material1,
        material2], n=3)

    """

    process_sequence = []
    material_a = None
    process = None
    material_b = None
    for x in range(0, n):
        for arg in args:
            if isinstance(arg, list) and len(arg) > 0:
                if isinstance(arg[0], (Source, Sample, Material)):
                    if material_a is None:
                        material_a = _deep_copy(arg)
                        y = 0
                        for material in material_a:
                            material.name = material.name + '-' + str(x) + '-' + str(y)
                            y += 1
                    else:
                        material_b = _deep_copy(arg)
                        y = 0
                        for material in material_b:
                            material.name = material.name + '-' + str(x) + '-' + str(y)
                            y += 1
                elif isinstance(arg[0], Process):
                    process = _deep_copy(arg)
                    y = 0
                    for p in process:
                        p.name = p.name + '-' + str(x) + '-' + str(y)
                        y += 1
            if isinstance(arg, (Source, Sample, Material)):
                if material_a is None:
                    material_a = _deep_copy(arg)
                    material_a.name = material_a.name + '-' + str(x)
                else:
                    material_b = _deep_copy(arg)
                    material_b.name = material_b.name + '-' + str(x)
            elif isinstance(arg, Process):
                process = _deep_copy(arg)
                process.name = process.name + '-' + str(x)
            if material_a is not None and material_b is not None and process is not None:
                if isinstance(process, list):
                    for p in process:
                        if isinstance(material_a, list):
                            p.inputs = material_a
                        else:
                            p.inputs.append(material_a)
                        if isinstance(material_b, list):
                            p.outputs = material_b
                            for material in material_b:
                                material.derives_from = [material_a]
                        else:
                            p.outputs.append(material_b)
                            material_b.derives_from = [material_a]
                        process_sequence.append(process)
                else:
                    if isinstance(material_a, list):
                        process.inputs = material_a
                    else:
                        process.inputs = [material_a]  # /.append(material_a)
                    if isinstance(material_b, list):
                        process.outputs = material_b
                        for material in material_b:
                            material.derives_from = [material_a]
                    else:
                        process.outputs = [material_b]  # .append(material_b)
                        material_b.derives_from = [material_a]
                    process_sequence.append(process)
                material_a = material_b
                process = None
                material_b = None
    return process_sequence


def _deep_copy(isa_object):
    """Re-implementation of the deepcopy function that also increases and sets the object identifiers for copied objects.

    :param {Object} isa_object: the object to copy
    """
    from copy import deepcopy
    from isatools.model.process_sequence import ProcessSequenceNode
    new_obj = deepcopy(isa_object)
    if isinstance(isa_object, ProcessSequenceNode):
        new_obj.assign_identifier()
    return new_obj
