import csv
import pandas as pd
import numpy as np
from bisect import bisect_left, bisect_right

"""
In progress; do not use!
"""

class ProcessSequence(object):

    def __init__(self):
        self.sources = list()
        self.samples = list()
        self.other_material = list()
        self.data = list()
        self.processes = list()


class Material(object):

    def __init__(self, name, characteristics=list()):
        self._name = name
        self._characteristics = characteristics

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self._name = name
        else:
            raise TypeError

    @property
    def characteristics(self):
        return self._characteristics

    @characteristics.setter
    def characteristics(self, characteristics):
        if isinstance(characteristics, list):
            self._characteristics = characteristics
        else:
            raise TypeError


class Source(Material):
    pass


class Sample(Material):
    pass


class Extract(Material):
    pass


class LabeledExtract(Material):
    pass


class Characteristic:

    def __init__(self, category=None, value=str()):
        self.category = category
        self.value = value


class DataFile:

    def __init__(self, name):
        self.name = name


class RawDataFile(DataFile):
    pass


class DerivedSpectralDataFile(DataFile):
    pass


class DerivedArrayDataFile(DataFile):
    pass


class ArrayDataFile(DataFile):
    pass


class ProteinAssignmentFile(DataFile):
    pass


class PeptideAssignmentFile(DataFile):
    pass


class PostTranslationalModificationAssignmentFile(DataFile):
    pass


class Process:

    def __init__(self, executes_protocol='', parameter_values=list(), inputs=list(), outputs=list()):
        self.executes_protocol = executes_protocol
        self.parameter_values = parameter_values
        self.inputs = inputs
        self.outputs = outputs


class ParameterValue:

    def __init__(self, category=None, value=str()):
        self.category = category
        self.value = value


class ProcessSequenceFactory(object):

    def __init__(self, xml_configuration=None):
        self._xml_configuration = xml_configuration

    def create_from_df(self, DF):

        config = self._xml_configuration

        sources = {}
        samples = {}
        other_material = {}
        data = {}
        processes = {}

        try:
            sources = dict(map(lambda x: (x, Source(name=x)), DF['Source Name'].drop_duplicates()))
        except KeyError:
            pass

        try:
            samples = dict(map(lambda x: (x, Sample(name=x)), DF['Sample Name'].drop_duplicates()))
        except KeyError:
            pass

        try:
            extracts = dict(map(lambda x: ('Extract Name:' + x, Extract(name=x)), DF['Extract Name'].drop_duplicates()))
            other_material.update(extracts)
        except KeyError:
            pass

        try:
            labeled_extracts = dict(map(lambda x: ('Labeled Extract Name:' + x,  LabeledExtract(name=x)),
                                        DF['Labeled Extract Name'].drop_duplicates()))
            other_material.update(labeled_extracts)
        except KeyError:
            pass

        try:
            raw_data_files = dict(map(lambda x: (x, RawDataFile(name=x)), DF['Raw Data File'].drop_duplicates()))
            data.update(raw_data_files)
        except KeyError:
            pass

        try:
            derived_spectral_data_files = dict(map(lambda x: (x, DerivedSpectralDataFile(name=x)),
                                                  DF['Derived Spectral Data File'].drop_duplicates()))
            data.update(derived_spectral_data_files)
        except KeyError:
            pass

        try:
            derived_array_data_files = dict(map(lambda x: (x, DerivedArrayDataFile(name=x)),
                                                DF['Derived Array Data File'].drop_duplicates()))
            data.update(derived_array_data_files)
        except KeyError:
            pass

        try:
            array_data_files = dict(map(lambda x: (x, ArrayDataFile(name=x)), DF['Array Data File'].drop_duplicates()))
            data.update(array_data_files)
        except KeyError:
            pass

        try:
            protein_assignment_files = dict(map(lambda x: (x, ProteinAssignmentFile(name=x)),
                                                DF['Protein Assignment File'].drop_duplicates()))
            data.update(protein_assignment_files)
        except KeyError:
            pass

        try:
            peptide_assignment_files = dict(map(lambda x: (x, PeptideAssignmentFile(name=x)),
                                                DF['Peptide Assignment File'].drop_duplicates()))
            data.update(peptide_assignment_files)
        except KeyError:
            pass

        try:
            post_translational_modification_assignment_files = \
                dict(map(lambda x: (x, PostTranslationalModificationAssignmentFile(name=x)),
                         DF['Post Translational Modification Assignment File'].drop_duplicates()))
            data.update(post_translational_modification_assignment_files)
        except KeyError:
            pass

        try:
            for protocol_ref_col in [c for c in DF.columns if c.startswith('Protocol REF')]:
                processes_list = list()
                for i, protocol_ref in enumerate(DF[protocol_ref_col]):
                    processes_list.append((protocol_ref + '-' + str(i), Process(executes_protocol=protocol_ref)))
                processes.update(dict(processes_list))
        except KeyError:
            pass

        isatab_header = DF.isatab_header
        object_index = [i for i, x in enumerate(isatab_header) if x in
                        ['Source Name', 'Sample Name', 'Extract Name', 'Labeled Extract Name', 'Protocol REF']]

        # group headers regarding objects delimited by object_index by slicing up the header list
        object_column_map = list()
        prev_i = object_index[0]
        for curr_i in object_index:  # collect each object's columns
            if prev_i == curr_i:
                pass  # skip if there's no diff, i.e. first one
            else:
                object_column_map.append(DF.columns[prev_i:curr_i])
            prev_i = curr_i
        object_column_map.append(DF.columns[prev_i:])  # finally collect last object's columns

        for column_group in object_column_map:
            # for each object, parse column group
            object_label = column_group[0]

            if object_label in ['Source Name', 'Sample Name', 'Extract Name', 'Labeled Extract Name']:  # characs

                for _, object_series in DF[column_group].drop_duplicates().iterrows():
                    material_name = object_series[column_group[0]]
                    material = None

                    try:
                        material = sources[material_name]
                    except KeyError:
                        pass

                    try:
                        material = samples[material_name]
                    except KeyError:
                        pass

                    try:
                        material = other_material[material_name]
                    except KeyError:
                        pass

                    if material is not None:
                        for charac_column in [c for c in column_group if c.startswith('Characteristics[')]:
                            material.characteristics.append(Characteristic(category=charac_column[16:-1],
                                                                           value=object_series[charac_column]))

            elif object_label.startswith('Protocol REF'):  # parameter vals

               for _, object_series in DF[column_group].iterrows():  # don't drop duplicates
                    protocol_ref = object_series[column_group[0]]
                    process = None

                    try:
                        process = processes[protocol_ref + '-' + str(_)]
                    except KeyError:
                        pass

                    if process is not None:
                        for pv_column in [c for c in column_group if c.startswith('Parameter Value[')]:
                            process.parameter_values.append(ParameterValue(category=pv_column[16:-1],
                                                                           value=object_series[pv_column]))

        process_cols = [i for i, c in enumerate(DF.columns) if c.startswith('Protocol REF')]
        node_cols = [i for i, c in enumerate(DF.columns) if c in ['Source Name', 'Sample Name', 'Extract Name',
                                                                  'Labeled Extract Name']]

        process_sequences = list()
        for _, process_series in DF[sorted(process_cols + node_cols)].iterrows():  # don't drop dups
            process_sequence = list()
            for process_col in process_cols:

                try:

                    process_key = process_series[DF.columns[process_col]] + '-' + str(_)
                    process = processes[process_key]
                    
                    input_node_index = find_lt(sorted(process_cols + node_cols), process_col)

                    if (input_node_index > -1) and (input_node_index not in process_cols):
                        input_node = None
                        node_key = process_series[DF.columns[input_node_index]]

                        if DF.columns[input_node_index] == 'Source Name':
                            input_node = sources[node_key]
                        elif DF.columns[input_node_index] == 'Sample Name':
                            input_node = samples[node_key]
                        elif DF.columns[input_node_index] == 'Extract Name':
                            input_node = other_material['Extract Name:' + node_key]
                        elif DF.columns[input_node_index] == 'Labeled Extract Name':
                            input_node = other_material['Labeled Extract Name:' + node_key]

                        if input_node is not None:
                            # print('adding ', input_node, ' to ', 'process input', process_key)
                            process.inputs.append(input_node)

                    output_node_index = find_gt(sorted(process_cols + node_cols), process_col)

                    if (output_node_index > -1) and (output_node_index not in process_cols):
                        output_node = None
                        node_key = process_series[DF.columns[output_node_index]]

                        if DF.columns[output_node_index] == 'Sample Name':
                            output_node = samples[node_key]
                        elif DF.columns[output_node_index] == 'Extract Name':
                            output_node = other_material['Extract Name:' + node_key]
                        elif DF.columns[output_node_index] == 'Labeled Extract Name':
                            output_node = other_material['Labeled Extract Name:' + node_key]

                        if output_node is not None:
                            # print('adding ', output_node, ' to ', 'process output', process_key)
                            process.outputs.append(output_node)
                            
                    process_sequence.append(process)

                except KeyError as ke:
                    print('Key error:', ke)

            process_sequences.append(process_sequence)

        return sources, samples, other_material, data, processes, process_sequences


def read_tfile(tfile_path, index_col=None):
    with open(tfile_path) as tfile_fp:
        reader = csv.reader(tfile_fp, delimiter='\t')
        header = list(next(reader))
        tfile_fp.seek(0)
        tfile_df = pd.read_csv(tfile_fp, sep='\t', index_col=index_col)
        tfile_df.isatab_header = header
    return tfile_df


def get_multiple_index(file_index, key):
    return np.where(np.array(file_index) == key)[0]


def find_lt(a, x):
    i = bisect_left(a, x)
    if i:
        return a[i - 1]
    else:
        return -1


def find_gt(a, x):
    i = bisect_right(a, x)
    if i != len(a):
        return a[i]
    else:
        return -1