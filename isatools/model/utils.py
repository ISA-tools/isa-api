import networkx as nx
import hashlib
import os

from isatools.model.datafile import DataFile, Comment
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

    :param *args: An argument list representing the process sequence prototype
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
                        process.inputs.append(material_a)
                    if isinstance(material_b, list):
                        process.outputs = material_b
                        for material in material_b:
                            material.derives_from = [material_a]
                    else:
                        process.outputs.append(material_b)
                        material_b.derives_from = [material_a]
                    process_sequence.append(process)
                material_a = material_b
                process = None
                material_b = None
    return process_sequence


def _deep_copy(isa_object):
    """
    Re-implementation of the deepcopy function that also increases and sets the object identifiers for copied objects.
    :param {Object} isa_object: the object to copy
    """
    from copy import deepcopy
    from isatools.model.process_sequence import ProcessSequenceNode
    new_obj = deepcopy(isa_object)
    if isinstance(isa_object, ProcessSequenceNode):
        new_obj.assign_identifier()
    return new_obj


def update_hash(path, file, hash_func):
    """
    a subfunction generating the hash using hashlib functions
    :param path:
    :param file:
    :param hash_func:
    :return:
    """

    with open(os.path.join(path, file), "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hash_func.update(byte_block)
    return hash_func.hexdigest()


def compute_checksum(path, isa_file_object: DataFile, checksum_type):
    """
    a helper function to compute file checksum given a file path, an isa data file name and a type of algorithm
    :param path:
    :param isa_file_object:
    :param checksum_type: enum
    :return:
    """

    if checksum_type not in ["md5", "sha1", "sha256", "blake2"]:
        raise ValueError("Invalid checksum type")
    else:
        file_checksum = None

        if checksum_type == "md5":
            hash_type = hashlib.md5()
            file_checksum = update_hash(path, isa_file_object.filename, hash_type)
            isa_file_object.comments.append(Comment(name="checksum type", value="md5"))

        if checksum_type == "sha256":
            hash_type = hashlib.sha256()
            file_checksum = update_hash(path, isa_file_object.filename, hash_type)
            isa_file_object.comments.append(Comment(name="checksum type", value="sha256"))

        if checksum_type == "sha1":
            hash_type = hashlib.sha1()
            file_checksum = update_hash(path, isa_file_object.filename, hash_type)
            isa_file_object.comments.append(Comment(name="checksum type", value="sha1"))

        if checksum_type == "blake2":
            hash_type = hashlib.blake2b()
            file_checksum = update_hash(path, isa_file_object.filename, hash_type)
            isa_file_object.comments.append(Comment(name="checksum type", value="blake2"))

        isa_file_object.comments.append(Comment(name="checksum", value=file_checksum))

    return isa_file_object
