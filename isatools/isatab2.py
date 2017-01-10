import csv
import pandas as pd
import numpy as np
from bisect import bisect_left, bisect_right
from itertools import tee
from isatools.model.v1 import *

"""
In progress; do not use yet as contents of this package will move!!!
"""

_LABELS_MATERIAL_NODES = ['Source Name', 'Sample Name', 'Extract Name', 'Labeled Extract Name']
_LABELS_DATA_NODES = ['Raw Data File', 'Derived Spectral Data File', 'Derived Array Data File', 'Array Data File',
                      'Protein Assignment File', 'Peptide Assignment File',
                      'Post Translational Modification Assignment File', 'Acquisition Parameter Data File',
                      'Free Induction Decay Data File', 'Derived Array Data Matrix File']
_LABELS_ASSAY_NODES = ['Assay Name', 'MS Assay Name', 'Hybridization Assay Name', 'Scan Name',
                       'Data Transformation Name', 'Normalization Name']


# class ProcessSequence(object):
#
#     def __init__(self):
#         self.sources = list()
#         self.samples = list()
#         self.other_material = list()
#         self.data = list()
#         self.processes = list()
#
#
# class Material(object):
#
#     def __init__(self, name, characteristics=None):
#         self.name = name
#         if characteristics is None:
#             self.characteristics = []
#         else:
#             self.characteristics = characteristics
#
#
# class Source(Material):
#     pass
#
#
# class Sample(Material):
#     pass
#
#
# class Extract(Material):
#     pass
#
#
# class LabeledExtract(Material):
#     pass
#
#
# class Characteristic:
#
#     def __init__(self, category=None, value=str()):
#         self.category = category
#         self.value = value
#
#
# class DataFile:
#
#     def __init__(self, name):
#         self.name = name
#
#
# class RawDataFile(DataFile):
#     pass
#
#
# class DerivedSpectralDataFile(DataFile):
#     pass
#
#
# class DerivedArrayDataFile(DataFile):
#     pass
#
#
# class ArrayDataFile(DataFile):
#     pass
#
#
# class ProteinAssignmentFile(DataFile):
#     pass
#
#
# class PeptideAssignmentFile(DataFile):
#     pass
#
#
# class PostTranslationalModificationAssignmentFile(DataFile):
#     pass
#
#
# class Process:
#
#     def __init__(self, executes_protocol='', parameter_values=None, inputs=None, outputs=None):
#
#         self.executes_protocol = executes_protocol
#
#         if parameter_values is None:
#             self.parameter_values = []
#         else:
#             self.parameter_values = parameter_values
#
#         if inputs is None:
#             self.inputs = []
#         else:
#             self.inputs = inputs
#
#         if outputs is None:
#             self.outputs = []
#         else:
#             self.outputs = outputs
#         self.prev_process = None
#         self.next_process = None


class ParameterValue:

    def __init__(self, category=None, value=''):
        self.category = category
        self.value = value


class StudyFactory:

    def __init__(self):
        pass

    def create_from_fp(self, FP):  # from DF of investigation file

        from isatools.isatab import read_investigation_file
        df_dict = read_investigation_file(FP)

        from isatools.model.v1 import Investigation, Study
        investigation = Investigation()

        # TODO: build Ontology Source section, as needed for OntologyAnnotation references
        for _, row in df_dict['ontology_sources'].iterrows():
            ontology_source = OntologySource(name=row['Term Source Name'],
                                             file=row['Term Source File'],
                                             version=row['Term Source File'],
                                             description=row['Term Source Description'])
            investigation.ontology_source_references.append(ontology_source)

        row = df_dict['investigation'].iloc[0]
        investigation.identifier = row['Investigation Identifier']
        investigation.title = row['Investigation Title']
        investigation.description = row['Investigation Description']
        investigation.submission_date = row['Investigation Submission Date']
        investigation.public_release_date = row['Investigation Public Release Date']
        for i in range(0, len(df_dict['studies'])):
            row = df_dict['studies'][i].iloc[0]
            study = Study()
            study.identifier = row['Study Identifier']
            study.title = row['Study Title']
            study.description = row['Study Description']
            study.submission_date = row['Study Submission Date']
            study.public_release_date = row['Study Public Release Date']
            study.filename = row['Study File Name']

            # TODO: build Protocol section, as needed for tables
            protocol_map = {}
            for j in range(0, len(df_dict['s_protocols'][i])):
                row = df_dict['s_protocols'][i].iloc[j]
                protocol = Protocol()
                protocol.name = row['Study Protocol Name']
                protocol.description = row['Study Protocol Description']
                protocol.uri = row['Study Protocol URI']
                protocol.version = row['Study Protocol Version']
                protocol.protocol_type = OntologyAnnotation()
                protocol.protocol_type.term = row['Study Protocol Type']
                protocol.protocol_type.term_accession = row['Study Protocol Type Term Accession Number']
                term_source_hits = [os for os in investigation.ontology_source_references if os.name == row['Study Protocol Type Term Source REF']]
                if len(term_source_hits) == 1:
                    protocol.protocol_type.term_source = term_source_hits[0]
                else:
                    protocol.protocol_type.term_source = None
                study.protocols.append(protocol)
                protocol_map[protocol.name] = protocol

            import os
            study_tfile_df = read_tfile(os.path.join(os.path.dirname(FP.name), study.filename))
            so, sa, o, d, processes, ps = ProcessSequenceFactory(investigation).create_from_df(study_tfile_df)
            study.process_sequence = list(processes.values())

            for process in study.process_sequence:
                process.executes_protocol = protocol_map[process.executes_protocol]

            investigation.studies.append(study)

        return investigation


class ProcessSequenceFactory:

    def __init__(self, I=None):
        self.I = I


    def create_from_df(self, DF):  # from DF of a table file

        DF = preprocess(DF=DF)

        if self.I is not None:
            ontology_source_map = dict(map(lambda x: (x.name, x), self.I.ontology_source_references))
        else:
            ontology_source_map = {}

        sources = {}
        samples = {}
        other_material = {}
        data = {}
        processes = {}
        # TODO: Handle comment columns

        try:
            sources = dict(map(lambda x: (x, Source(name=x)), DF['Source Name'].drop_duplicates()))
        except KeyError:
            pass

        try:
            samples = dict(map(lambda x: (x, Sample(name=x)), DF['Sample Name'].drop_duplicates()))
        except KeyError:
            pass

        try:
            extracts = dict(map(lambda x: ('Extract Name:' + x, Material(name=x, type_='Extract Name')), DF['Extract Name'].drop_duplicates()))
            other_material.update(extracts)
        except KeyError:
            pass

        try:
            # TODO: Add label to LabeledExtract objects
            labeled_extracts = dict(map(lambda x: ('Labeled Extract Name:' + x,  Material(name=x, type_='Labeled Extract Name')),
                                        DF['Labeled Extract Name'].drop_duplicates()))
            other_material.update(labeled_extracts)
        except KeyError:
            pass

        try:
            raw_data_files = dict(map(lambda x: ('Raw Data File:' + x, DataFile(filename=x, label='Raw Data File')), DF['Raw Data File'].drop_duplicates()))
            data.update(raw_data_files)
        except KeyError:
            pass

        try:
            derived_spectral_data_files = dict(map(lambda x: ('Derived Spectral Data File:' + x, DataFile(filename=x, label='Derived Spectral Data File')),
                                                  DF['Derived Spectral Data File'].drop_duplicates()))
            data.update(derived_spectral_data_files)
        except KeyError:
            pass

        try:
            derived_array_data_files = dict(map(lambda x: ('Derived Array Data File:' + x, DataFile(filename=x, label='Derived Array Data File')),
                                                DF['Derived Array Data File'].drop_duplicates()))
            data.update(derived_array_data_files)
        except KeyError:
            pass

        try:
            array_data_files = dict(map(lambda x: ('Array Data File:' + x, DataFile(filename=x, label='Array Data File')), DF['Array Data File'].drop_duplicates()))
            data.update(array_data_files)
        except KeyError:
            pass

        try:
            protein_assignment_files = dict(map(lambda x: ('Protein Assignment File:' + x, DataFile(filename=x, label='Protein Assignment File')),
                                                DF['Protein Assignment File'].drop_duplicates()))
            data.update(protein_assignment_files)
        except KeyError:
            pass

        try:
            peptide_assignment_files = dict(map(lambda x: ('Peptide Assignment File:' + x, DataFile(filename=x, label='Peptide Assignment File')),
                                                DF['Peptide Assignment File'].drop_duplicates()))
            data.update(peptide_assignment_files)
        except KeyError:
            pass

        try:
            post_translational_modification_assignment_files = \
                dict(map(lambda x: ('Post Translational Modification Assignment File:' + x, DataFile(filename=x, label='Post Translational Modification Assignment File')),
                         DF['Post Translational Modification Assignment File'].drop_duplicates()))
            data.update(post_translational_modification_assignment_files)
        except KeyError:
            pass

        try:
            acquisition_parameter_data_files = dict(map(lambda x: ('Acquisiton Parameter Data File' + x, DataFile(filename=x, label='Acquisiton Parameter Data File')),
                                                DF['Acquisiton Parameter Data File'].drop_duplicates()))
            data.update(acquisition_parameter_data_files)
        except KeyError:
            pass

        try:
            post_translational_modification_assignment_files = \
                dict(map(lambda x: ('Free Induction Decay Data File:' + x, DataFile(filename=x, label='Free Induction Decay Data File')),
                         DF['Free Induction Decay Data File'].drop_duplicates()))
            data.update(post_translational_modification_assignment_files)
        except KeyError:
            pass

        isatab_header = DF.isatab_header
        object_index = [i for i, x in enumerate(isatab_header) if x in _LABELS_MATERIAL_NODES + _LABELS_DATA_NODES
                        + ['Protocol REF']]

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

        node_cols = [i for i, c in enumerate(DF.columns) if c in _LABELS_MATERIAL_NODES + _LABELS_DATA_NODES]

        for _cg, column_group in enumerate(object_column_map):
            # for each object, parse column group
            object_label = column_group[0]

            if object_label in _LABELS_MATERIAL_NODES:  # characs

                for _, object_series in DF[column_group].drop_duplicates().iterrows():
                    node_key = object_series[column_group[0]]
                    material = None

                    try:
                        material = sources[node_key]
                    except KeyError:
                        pass

                    try:
                        material = samples[node_key]
                    except KeyError:
                        pass

                    try:
                        material = other_material[column_group[0] + ':' + node_key]
                    except KeyError:
                        pass

                    if material is not None:
                        for charac_column in [c for c in column_group if c.startswith('Characteristics[')]:
                            #  TODO: Link Characteristics to Characteristic categories
                            #  TODO: Handle multiple data types including OntologyAnnotations, Units
                            characteristic = Characteristic(category=OntologyAnnotation(
                                term=charac_column[16:-1]))

                            cell_value = object_series[charac_column]

                            charac_column_index = list(column_group).index(charac_column)

                            offset_1r_col = DF.columns[charac_column_index + 1]
                            offset_2r_col = DF.columns[charac_column_index + 2]
                            offset_3r_col = DF.columns[charac_column_index + 3]

                            # Determine if the cell value is an OntologyAnnotation, and cast it if it is
                            if offset_1r_col.startswith('Term Source REF'):
                                cell_value = object_series[charac_column]
                                if cell_value is not '':
                                    value = OntologyAnnotation(
                                        term=str(cell_value)
                                    )
                                    term_source_value = object_series[offset_1r_col]
                                    if term_source_value is not '':
                                        try:
                                            value.term_source = ontology_source_map[term_source_value]
                                        except KeyError:
                                            print('term source: ', type(term_source_value), ' not declared')
                                    term_accession_value = object_series[offset_2r_col]
                                    if term_accession_value is not '':
                                        value.term_accession = term_accession_value

                            # Determine if a numeric value has an associated Unit
                            # TODO: Check and fix Unit parsing
                            if offset_1r_col.startswith('Unit') or isinstance(cell_value, (int, float)):
                                unit_term = object_series[offset_1r_col]
                                unit = OntologyAnnotation(
                                    term=unit_term
                                )
                                term_source_value = object_series[offset_2r_col]
                                try:
                                    unit.term_source = ontology_source_map[term_source_value]
                                except KeyError:
                                    print('term source: ', term_source_value, ' not declared, not linking')
                                term_accession_value = object_series[offset_3r_col]
                                unit.term_accession = str(term_accession_value)

                                characteristic.unit = unit

                            characteristic.value = cell_value
                            material.characteristics.append(characteristic)

            elif object_label.startswith('Protocol REF'):

                for _, object_series in DF.iterrows():  # don't drop duplicates
                    protocol_ref = object_series[column_group[0]]

                    input_node = None
                    output_node = None

                    output_node_index = find_gt(node_cols, _cg)  # TODO: Fix how far right we look for outputs

                    if output_node_index > -1:

                        output_node_label = DF.columns[output_node_index]
                        output_node_value = object_series[output_node_label]

                        node_key = output_node_value

                        if output_node_label == 'Sample Name':
                            output_node = samples[node_key]
                        elif output_node_label == 'Extract Name':
                            output_node = other_material['Extract Name:' + node_key]
                        elif DF.columns[output_node_index] == 'Labeled Extract Name':
                            output_node = other_material['Labeled Extract Name:' + node_key]
                        elif output_node_label == 'Raw Data File':
                            output_node = data['Raw Data File:' + node_key]
                        elif output_node_label == 'Derived Spectral Data File':
                            output_node = data['Derived Spectral Data File:' + node_key]
                        elif output_node_label == 'Derived Array Data File':
                            output_node = data['Derived Array Data File:' + node_key]
                        elif output_node_label == 'Array Data File':
                            output_node = data['Array Data File:' + node_key]
                        elif output_node_label == 'Protein Assignment File':
                            output_node = data['Protein Assignment File:' + node_key]
                        elif output_node_label == 'Peptide Assignment File':
                            output_node = data['Peptide Assignment File:' + node_key]
                        elif output_node_label == 'Post Translational Modification Assignment File':
                            output_node = data['Post Translational Modification Assignment File:' + node_key]
                        elif output_node_label == 'Acquisition Parameter Data File':
                            output_node = data['Acquisition Parameter Data File:' + node_key]
                        elif output_node_label == 'Free Induction Decay Data File':
                            output_node = data['Free Induction Decay Data File:' + node_key]

                    input_node_index = find_lt(node_cols, _cg)  # TODO: Fix how far left we look for outputs

                    if input_node_index > -1:

                        input_node_label = DF.columns[input_node_index]
                        input_node_value = object_series[input_node_label]

                        node_key = input_node_value

                        if input_node_label == 'Source Name':
                            input_node = sources[node_key]
                        elif input_node_label == 'Sample Name':
                            input_node = samples[node_key]
                        elif input_node_label == 'Extract Name':
                            input_node = other_material['Extract Name:' + node_key]
                        elif input_node_label == 'Labeled Extract Name':
                            input_node = other_material['Labeled Extract Name:' + node_key]
                        elif input_node_label == 'Raw Data File':
                            input_node = data['Raw Data File:' + node_key]
                        elif input_node_label == 'Derived Spectral Data File':
                            input_node = data['Derived Spectral Data File:' + node_key]
                        elif input_node_label == 'Derived Array Data File':
                            input_node = data['Derived Array Data File:' + node_key]
                        elif input_node_label == 'Array Data File':
                            input_node = data['Array Data File:' + node_key]
                        elif input_node_label == 'Protein Assignment File':
                            input_node = data['Protein Assignment File:' + node_key]
                        elif input_node_label == 'Peptide Assignment File':
                            input_node = data['Peptide Assignment File:' + node_key]
                        elif input_node_label == 'Post Translational Modification Assignment File':
                            input_node = data['Post Translational Modification Assignment File:' + node_key]
                        elif input_node_label == 'Acquisition Parameter Data File':
                            input_node = data['Acquisition Parameter Data File:' + node_key]
                        elif input_node_label == 'Free Induction Decay Data File':
                            input_node = data['Free Induction Decay Data File:' + node_key]

                    process_key = process_keygen(protocol_ref, column_group, _cg, DF.columns, object_series, _)

                    try:
                        process = processes[process_key]
                    except KeyError:
                        #  TODO: point to Protocol object
                        process = Process(executes_protocol=object_series[object_label])
                        processes.update(dict([(process_key, process)]))

                    name_column_hits = [n for n in column_group if n in _LABELS_ASSAY_NODES]
                    if len(name_column_hits) == 1:
                        process.name = name_column_hits[0]

                    for pv_column in [c for c in column_group if c.startswith('Parameter Value[')]:
                        process.parameter_values.append(ParameterValue(category=pv_column[16:-1],
                                                                       value=object_series[pv_column]))

                    if input_node is not None and input_node not in process.inputs:
                        process.inputs.append(input_node)

                    if output_node is not None and output_node not in process.outputs:
                        process.outputs.append(output_node)

        process_sequences = list()

        # now go row by row pulling out processes and linking them accordingly

        for _, object_series in DF.iterrows():  # don't drop duplicates

            process_key_sequence = list()

            for _cg, column_group in enumerate(object_column_map):

                # for each object, parse column group

                object_label = column_group[0]

                if object_label.startswith('Protocol REF'):

                    protocol_ref = object_series[column_group[0]]

                    process_key = process_keygen(protocol_ref, column_group, _cg, DF.columns, object_series, _)

                    process_key_sequence.append(process_key)

            # print('key sequence = ', process_key_sequence)

            # Link the processes in each sequence
            for pair in pairwise(process_key_sequence):  # TODO: Make split/pool model with multi prev/next_process

                l = processes[pair[0]]  # get process on left of pair
                r = processes[pair[1]]  # get process on right of pair

                l.next_process = r
                r.prev_process = l

        return sources, samples, other_material, data, processes, process_sequences


def process_keygen(protocol_ref, column_group, cg_index, all_columns, series, series_index):

    process_key = protocol_ref

    node_key = None

    node_cols = [i for i, c in enumerate(all_columns) if c in _LABELS_MATERIAL_NODES + _LABELS_DATA_NODES]

    output_node_index = find_gt(node_cols, cg_index)

    if output_node_index > -1:

        output_node_label = all_columns[output_node_index]
        output_node_value = series[output_node_label]

        node_key = output_node_value

    input_node_index = find_lt(node_cols, cg_index)

    if input_node_index > -1:

        input_node_label = all_columns[input_node_index]
        input_node_value = series[input_node_label]

        node_key = input_node_value

    if process_key == protocol_ref:

        process_key += '-' + str(series_index)

    name_column_hits = [n for n in column_group if n in _LABELS_ASSAY_NODES]

    if len(name_column_hits) == 1:
        process_key = series[name_column_hits[0]]
    else:
        pv_cols = [c for c in column_group if c.startswith('Parameter Value[')]

        if len(pv_cols) > 0:
            # 2. else try use protocol REF + Parameter Values as key
            if node_key is not None:
                process_key = node_key + \
                              ':' + protocol_ref + \
                              ':' + '/'.join([str(v) for v in series[pv_cols]])
            else:
                process_key = protocol_ref + \
                              ':' + '/'.join([str(v) for v in series[pv_cols]])
        else:
            # 3. else try use input + protocol REF as key
            # 4. else try use output + protocol REF as key
            if node_key is not None:
                process_key = node_key + '/' + protocol_ref

    return process_key


def pairwise(iterable):
    """Pairwise iterator"""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def read_tfile(tfile_path, index_col=None):
    with open(tfile_path) as tfile_fp:
        reader = csv.reader(tfile_fp, delimiter='\t')
        header = list(next(reader))
        tfile_fp.seek(0)
        tfile_df = pd.read_csv(tfile_fp, sep='\t', index_col=index_col).fillna('')
        tfile_df.isatab_header = header
    return tfile_df


def get_multiple_index(file_index, key):
    return np.where(np.array(file_index) in key)[0]


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


def preprocess(DF):
    """Check headers, and insert Protocol REF if needed"""

    headers = DF.columns

    process_node_name_indices = [x for x, y in enumerate(headers) if y in _LABELS_ASSAY_NODES]

    process_cols = [i for i, c in enumerate(DF.columns) if c.startswith('Protocol REF')]

    missing_process_indices = list()

    num_protocol_refs = len([x for x in headers if x.startswith('Protocol REF')])

    for i in process_node_name_indices:

        if not headers[find_lt(process_cols, i)].startswith('Protocol REF'):
            print('warning: Protocol REF missing before \'{}\', found \'{}\''.format(headers[i], headers[i - 1]))
            missing_process_indices.append(i)

    # insert Protocol REF columns
    offset = 0

    for i in reversed(missing_process_indices):

        DF.insert(i, 'Protocol REF.{}'.format(num_protocol_refs + offset), 'unknown')

        headers.insert(i, 'Protocol REF')

        print('inserting Protocol REF.{}'.format(num_protocol_refs + offset), 'at position {}'.format(i))
        offset += 1

    return DF
