from .model.v1 import *
import os
import csv
import numpy as np
from bisect import bisect_left, bisect_right
from itertools import tee
import pandas as pd
import re
import io

## REGEXES
_RX_I_FILE_NAME = re.compile('i_(.*?)\.txt')
_RX_DATA = re.compile('data\[(.*?)\]')
_RX_COMMENT = re.compile('Comment\[(.*?)\]')
_RX_DOI = re.compile('(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![%"#? ])\\S)+)')
_RX_PMID = re.compile('[0-9]{8}')
_RX_PMCID = re.compile('PMC[0-9]{8}')
_RX_CHARACTERISTICS = re.compile('Characteristics\[(.*?)\]')
_RX_PARAMETER_VALUE = re.compile('Parameter Value\[(.*?)\]')
_RX_FACTOR_VALUE = re.compile('Factor Value\[(.*?)\]')
_RX_INDEXED_COL = re.compile('(.*?)\.\d+')

# column labels
_LABELS_MATERIAL_NODES = ['Source Name', 'Sample Name', 'Extract Name', 'Labeled Extract Name']
_LABELS_DATA_NODES = ['Raw Data File', 'Derived Spectral Data File', 'Derived Array Data File', 'Array Data File',
                      'Protein Assignment File', 'Peptide Assignment File',
                      'Post Translational Modification Assignment File', 'Acquisition Parameter Data File',
                      'Free Induction Decay Data File', 'Derived Array Data Matrix File']
_LABELS_ASSAY_NODES = ['Assay Name', 'MS Assay Name', 'Hybridization Assay Name', 'Scan Name',
                       'Data Transformation Name', 'Normalization Name']


def read_investigation_file(fp):

    def _peek(f):
        position = f.tell()
        l = f.readline()
        f.seek(position)
        return l

    def _read_tab_section(f, sec_key, next_sec_key=None):

        line = f.readline()
        normed_line = line.rstrip()
        if normed_line[0] == '"':
            normed_line = normed_line[1:]
        if normed_line[len(normed_line)-1] == '"':
            normed_line = normed_line[:len(normed_line)-1]
        if not normed_line == sec_key:
            raise IOError("Expected: " + sec_key + " section, but got: " + normed_line)
        memf = io.StringIO()
        while not _peek(f=f).rstrip() == next_sec_key:
            line = f.readline()
            if not line:
                break
            memf.write(line.rstrip() + '\n')
        memf.seek(0)
        return memf

    def _build_section_df(f):
        import numpy as np
        df = pd.read_csv(f, sep='\t').T  # Load and transpose ISA file section
        df.replace(np.nan, '', regex=True, inplace=True)  # Strip out the nan entries
        df.reset_index(inplace=True)  # Reset index so it is accessible as column
        df.columns = df.iloc[0]  # If all was OK, promote this row to the column headers
        df = df.reindex(df.index.drop(0))  # Reindex the DataFrame
        return df

    df_dict = dict()

    # Read in investigation file into DataFrames first
    df_dict['ontology_sources'] = _build_section_df(_read_tab_section(
        f=fp,
        sec_key='ONTOLOGY SOURCE REFERENCE',
        next_sec_key='INVESTIGATION'
    ))
    # assert({'Term Source Name', 'Term Source File', 'Term Source Version', 'Term Source Description'}
    #        .issubset(set(ontology_sources_df.columns.values)))  # Check required labels are present
    df_dict['investigation']  = _build_section_df(_read_tab_section(
        f=fp,
        sec_key='INVESTIGATION',
        next_sec_key='INVESTIGATION PUBLICATIONS'
    ))
    df_dict['i_publications']  = _build_section_df(_read_tab_section(
        f=fp,
        sec_key='INVESTIGATION PUBLICATIONS',
        next_sec_key='INVESTIGATION CONTACTS'
    ))
    df_dict['i_contacts']  = _build_section_df(_read_tab_section(
        f=fp,
        sec_key='INVESTIGATION CONTACTS',
        next_sec_key='STUDY'
    ))
    df_dict['studies'] = list()
    df_dict['s_design_descriptors'] = list()
    df_dict['s_publications'] = list()
    df_dict['s_factors'] = list()
    df_dict['s_assays'] = list()
    df_dict['s_protocols'] = list()
    df_dict['s_contacts'] = list()
    while _peek(fp):  # Iterate through STUDY blocks until end of file
        df_dict['studies'].append(_build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY',
            next_sec_key='STUDY DESIGN DESCRIPTORS'
        )))
        df_dict['s_design_descriptors'] .append(_build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY DESIGN DESCRIPTORS',
            next_sec_key='STUDY PUBLICATIONS'
        )))
        df_dict['s_publications'].append(_build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY PUBLICATIONS',
            next_sec_key='STUDY FACTORS'
        )))
        df_dict['s_factors'].append(_build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY FACTORS',
            next_sec_key='STUDY ASSAYS'
        )))
        df_dict['s_assays'].append(_build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY ASSAYS',
            next_sec_key='STUDY PROTOCOLS'
        )))
        df_dict['s_protocols'].append(_build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY PROTOCOLS',
            next_sec_key='STUDY CONTACTS'
        )))
        df_dict['s_contacts'].append(_build_section_df(_read_tab_section(
            f=fp,
            sec_key='STUDY CONTACTS',
            next_sec_key='STUDY'
        )))
    return df_dict


def load(FP):  # from DF of investigation file

    def get_ontology_source(term_source_ref):
        try:
            os = ontology_source_map[term_source_ref]
        except KeyError:
            os = None
        return os

    def get_oa(val, accession, ts_ref):
        if val == '' and accession == '':
            return None
        else:
            return OntologyAnnotation(
                term=val,
                term_accession=accession,
                term_source=get_ontology_source(ts_ref)
            )

    def get_oa_list_from_semi_c_list(vals, accessions, ts_refs):
        oa_list = []
        for _, val in enumerate(vals.split(';')):
            oa = get_oa(val, accessions.split(';')[_], ts_refs.split(';')[_])
            if oa is not None:
                oa_list.append(oa)
        return oa_list

    def get_publications(section_df):

        if 'Investigation PubMed ID' in section_df.columns:
            prefix = 'Investigation '
        elif 'Study PubMed ID' in section_df.columns:
            prefix = 'Study '
        else:
            raise KeyError

        publications = []

        for _, row in section_df.iterrows():
            publication = Publication(pubmed_id=row[prefix + 'PubMed ID'],
                                      doi=row[prefix + 'Publication DOI'],
                                      author_list=row[prefix + 'Publication Author List'],
                                      title=row[prefix + 'Publication Title'])

            publication.status = get_oa(row[prefix + 'Publication Status'],
                                        row[prefix + 'Publication Status Term Accession Number'],
                                        row[prefix + 'Publication Status Term Source REF'])

            publications.append(publication)

        return publications

    def get_contacts(section_df):

        if 'Investigation Person Last Name' in section_df.columns:
            prefix = 'Investigation '
        elif 'Study Person Last Name' in section_df.columns:
            prefix = 'Study '
        else:
            raise KeyError

        contacts = []

        for _, row in section_df.iterrows():
            person = Person(last_name=row[prefix + 'Person Last Name'],
                            first_name=row[prefix + 'Person First Name'],
                            mid_initials=row[prefix + 'Person Mid Initials'],
                            email=row[prefix + 'Person Email'],
                            phone=row[prefix + 'Person Phone'],
                            fax=row[prefix + 'Person Fax'],
                            address=row[prefix + 'Person Address'],
                            affiliation=row[prefix + 'Person Affiliation'])

            person.roles = get_oa_list_from_semi_c_list(row[prefix + 'Person Roles'],
                                                        row[prefix + 'Person Roles Term Accession Number'],
                                                        row[prefix + 'Person Roles Term Source REF'])

            contacts.append(person)

        return contacts

    df_dict = read_investigation_file(FP)

    from isatools.model.v1 import Investigation, Study
    investigation = Investigation()

    for _, row in df_dict['ontology_sources'].iterrows():
        ontology_source = OntologySource(name=row['Term Source Name'],
                                         file=row['Term Source File'],
                                         version=row['Term Source File'],
                                         description=row['Term Source Description'])
        investigation.ontology_source_references.append(ontology_source)

    ontology_source_map = dict(map(lambda x: (x.name, x), investigation.ontology_source_references))

    row = df_dict['investigation'].iloc[0]
    investigation.identifier = row['Investigation Identifier']
    investigation.title = row['Investigation Title']
    investigation.description = row['Investigation Description']
    investigation.submission_date = row['Investigation Submission Date']
    investigation.public_release_date = row['Investigation Public Release Date']
    investigation.publications = get_publications(df_dict['i_publications'])
    investigation.contacts = get_contacts(df_dict['i_contacts'])

    for i in range(0, len(df_dict['studies'])):
        row = df_dict['studies'][i].iloc[0]
        study = Study()
        study.identifier = row['Study Identifier']
        study.title = row['Study Title']
        study.description = row['Study Description']
        study.submission_date = row['Study Submission Date']
        study.public_release_date = row['Study Public Release Date']
        study.filename = row['Study File Name']
        study.publications = get_publications(df_dict['s_publications'][i])
        study.contacts = get_contacts(df_dict['s_contacts'][i])

        for _, row in df_dict['s_design_descriptors'][i].iterrows():
            design_descriptor = get_oa(row['Study Design Type'],
                                       row['Study Design Type Term Accession Number'],
                                       row['Study Design Type Term Source REF'])
            study.design_descriptors.append(design_descriptor)

        for _, row in df_dict['s_factors'][i].iterrows():
            factor = StudyFactor(name=row['Study Factor Name'])
            factor.factor_type = get_oa(row['Study Factor Type'],
                                        row['Study Factor Type Term Accession Number'],
                                        row['Study Factor Type Term Source REF'])
            study.factors.append(factor)

        protocol_map = {}
        for _, row in df_dict['s_protocols'][i].iterrows():
            protocol = Protocol()
            protocol.name = row['Study Protocol Name']
            protocol.description = row['Study Protocol Description']
            protocol.uri = row['Study Protocol URI']
            protocol.version = row['Study Protocol Version']
            protocol.protocol_type = get_oa(row['Study Protocol Type'],
                                            row['Study Protocol Type Term Accession Number'],
                                            row['Study Protocol Type Term Source REF'])
            params = get_oa_list_from_semi_c_list(
                row['Study Protocol Parameters Name'], row['Study Protocol Parameters Name Term Accession Number'],
                row['Study Protocol Parameters Name Term Source REF'])
            for param in params:
                protocol_param = ProtocolParameter(parameter_name=param)
                protocol.parameters.append(protocol_param)
            study.protocols.append(protocol)
            protocol_map[protocol.name] = protocol
        study.protocols = list(protocol_map.values())
        study_tfile_df = read_tfile(os.path.join(os.path.dirname(FP.name), study.filename))
        sources, samples, _, __, processes, characteristic_categories, unit_categories = ProcessSequenceFactory(
            investigation.ontology_source_references, study_protocols=study.protocols,
            study_factors=study.factors).create_from_df(study_tfile_df)
        study.materials['sources'] = list(sources.values())
        study.materials['samples'] = list(samples.values())
        study.process_sequence = list(processes.values())
        study.characteristic_categories = list(characteristic_categories.values())
        study.units = list(unit_categories.values())

        for process in study.process_sequence:
            try:
                process.executes_protocol = protocol_map[process.executes_protocol]
            except KeyError:
                try:
                    unknown_protocol = protocol_map['unknown']
                except KeyError:
                    protocol_map['unknown'] = Protocol(
                        name="unknown protocol",
                        description="This protocol was auto-generated where a protocol could not be determined.")
                    unknown_protocol = protocol_map['unknown']
                    study.protocols.append(unknown_protocol)
                process.executes_protocol = unknown_protocol

        for _, row in df_dict['s_assays'][i].iterrows():
            assay = Assay()
            assay.filename = row['Study Assay File Name']
            assay.measurement_type = get_oa(
                row['Study Assay Measurement Type'],
                row['Study Assay Measurement Type Term Accession Number'],
                row['Study Assay Measurement Type Term Source REF']
            )
            assay.technology_type = get_oa(
                row['Study Assay Technology Type'],
                row['Study Assay Technology Type Term Accession Number'],
                row['Study Assay Technology Type Term Source REF']
            )
            assay.technology_platform = row['Study Assay Technology Platform']

            assay_tfile_df = read_tfile(os.path.join(os.path.dirname(FP.name), assay.filename))
            _, samples, other, data, processes, characteristic_categories, unit_categories = ProcessSequenceFactory(
                investigation.ontology_source_references,
                study.materials['samples'],
                study.protocols,
                study.factors).create_from_df(assay_tfile_df)
            assay.materials['samples'] = list(samples.values())
            assay.materials['other_material'] = list(other.values())
            assay.data_files = list(data.values())
            assay.process_sequence = list(processes.values())
            assay.characteristic_categories = list(characteristic_categories.values())
            assay.units = list(unit_categories.values())

            for process in assay.process_sequence:
                try:
                    process.executes_protocol = protocol_map[process.executes_protocol]
                except KeyError:
                    try:
                        unknown_protocol = protocol_map['unknown']
                    except KeyError:
                        protocol_map['unknown'] = Protocol(
                            name="unknown protocol",
                            description="This protocol was auto-generated where a protocol could not be determined.")
                        unknown_protocol = protocol_map['unknown']
                        study.protocols.append(unknown_protocol)
                    process.executes_protocol = unknown_protocol

            study.assays.append(assay)

        investigation.studies.append(study)

    return investigation


def process_keygen(protocol_ref, column_group, object_label_index, all_columns, series, series_index, DF):
    process_key = protocol_ref
    node_cols = [i for i, c in enumerate(all_columns) if c in _LABELS_MATERIAL_NODES + _LABELS_DATA_NODES]
    input_node_value = ''
    output_node_value = ''
    output_node_index = find_gt(node_cols, object_label_index)
    if output_node_index > -1:
        output_node_label = all_columns[output_node_index]
        output_node_value = series[output_node_label]

    input_node_index = find_lt(node_cols, object_label_index)
    if input_node_index > -1:
        input_node_label = all_columns[input_node_index]
        input_node_value = series[input_node_label]

    input_nodes_with_prot_keys = DF[[all_columns[object_label_index], all_columns[input_node_index]]].drop_duplicates()
    output_nodes_with_prot_keys = DF[[all_columns[object_label_index], all_columns[output_node_index]]].drop_duplicates()

    if len(input_nodes_with_prot_keys) > len(output_nodes_with_prot_keys):
        node_key = output_node_value
    else:
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


def get_value(object_column, column_group, object_series, ontology_source_map, unit_categories):
    cell_value = object_series[object_column]
    if cell_value == '':
        return cell_value, None
    column_index = list(column_group).index(object_column)

    try:
        offset_1r_col = column_group[column_index + 1]
        offset_2r_col = column_group[column_index + 2]
    except IndexError:
        return cell_value, None

    if offset_1r_col.startswith('Term Source REF') and offset_2r_col.startswith('Term Accession Number'):

        value = OntologyAnnotation(term=str(cell_value))
        term_source_value = object_series[offset_1r_col]
        if term_source_value is not '':
            try:
                value.term_source = ontology_source_map[term_source_value]
            except KeyError:
                print('term source: ', term_source_value, ' not found')
        term_accession_value = object_series[offset_2r_col]
        if term_accession_value is not '':
            value.term_accession = term_accession_value
        return value, None

    try:
        offset_3r_col = column_group[column_index + 3]
    except IndexError:
        return cell_value, None

    if offset_1r_col.startswith('Unit') and offset_2r_col.startswith('Term Source REF') \
            and offset_3r_col.startswith('Term Accession Number'):
        category_key = object_series[offset_1r_col]
        try:
            unit_term_value = unit_categories[category_key]
        except KeyError:
            unit_term_value = OntologyAnnotation(term=category_key)
            unit_categories[category_key] = unit_term_value
            unit_term_source_value = object_series[offset_2r_col]
            if unit_term_source_value is not '':
                try:
                    unit_term_value.term_source = ontology_source_map[unit_term_source_value]
                except KeyError:
                    print('term source: ', unit_term_source_value, ' not found')
            term_accession_value = object_series[offset_3r_col]
            if term_accession_value is not '':
                unit_term_value.term_accession = term_accession_value

        return cell_value, unit_term_value

    else:
        return cell_value, None


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

    columns = DF.columns
    process_node_name_indices = [x for x, y in enumerate(columns) if y in _LABELS_ASSAY_NODES]
    missing_process_indices = list()
    protocol_ref_cols = [x for x in columns if x.startswith('Protocol REF')]
    num_protocol_refs = len(protocol_ref_cols)
    all_cols_indicies = [i for i, c in enumerate(columns) if c in
                         _LABELS_MATERIAL_NODES +
                         _LABELS_DATA_NODES +
                         _LABELS_ASSAY_NODES +
                         protocol_ref_cols]
    for i in process_node_name_indices:
        if not columns[find_lt(all_cols_indicies, i)].startswith('Protocol REF'):
            print('warning: Protocol REF missing before \'{}\', found \'{}\''.format(columns[i], columns[find_lt(all_cols_indicies, i)]))
            missing_process_indices.append(i)

    # insert Protocol REF columns
    offset = 0
    for i in reversed(missing_process_indices):
        DF.insert(i, 'Protocol REF.{}'.format(num_protocol_refs + offset), 'unknown')
        DF.isatab_header.insert(i, 'Protocol REF')
        offset += 1
    return DF


def drop_suffix(x):
    try:
        x.rindex('.')
    except ValueError:
        return x
    return x[:x.rindex('.')]


def get_object_column_map(df_columns):
    object_index = [i for i, x in enumerate(df_columns) if drop_suffix(x) in _LABELS_MATERIAL_NODES +
                    _LABELS_DATA_NODES + ['Protocol REF']]
    # group headers regarding objects delimited by object_index by slicing up the header list
    object_column_map = []
    prev_i = object_index[0]
    for curr_i in object_index:  # collect each object's columns
        if prev_i == curr_i:
            pass  # skip if there's no diff, i.e. first one
        else:
            object_column_map.append(df_columns[prev_i:curr_i])
        prev_i = curr_i
    object_column_map.append(df_columns[prev_i:])  # finally collect last object's columns
    return object_column_map


class ProcessSequenceFactory:

    def __init__(self, ontology_sources=None, study_samples=None, study_protocols=None, study_factors=None):
        self.ontology_sources = ontology_sources
        self.samples = study_samples
        self.protocols = study_protocols
        self.factors = study_factors

    def create_from_df(self, DF):  # from DF of a table file
        # DF = preprocess(DF=DF)
        if self.ontology_sources is not None:
            ontology_source_map = dict(map(lambda x: (x.name, x), self.ontology_sources))
        else:
            ontology_source_map = {}
        if self.protocols is not None:
            protocol_map = dict(map(lambda x: (x.name, x), self.protocols))
        else:
            protocol_map = {}
        if self.factors is not None:
            protocol_map = dict(map(lambda x: (x.name, x), self.factors))
        else:
            factor_map = {}

        # stuff to return
        sources = {}
        samples = {}
        other_material = {}
        data = {}
        processes = {}
        characteristic_categories = {}
        unit_categories = {}

        df_columns = list(DF.columns)
        column_map = get_object_column_map(df_columns)

        def build_node_objects(DF, targetClass):  # used to build Source, Sample, Extract, LabeledExtract

            def get_qualifiers(cols, row):
                qualifiers = []
                qindex = [_ for _, i in enumerate(cols) if i.startswith("Characteristics")
                          or i.startswith("Factor Value") or i.startswith("Comment")]
                for qi in qindex:
                    val = row[qi]
                    unit = None
                    term_source = None
                    term_access = None
                    offset1 = qi+1
                    offset2 = qi+2
                    offset3 = qi+3
                    if isinstance(val, str):
                        if offset1 < len(cols) and offset2 < len(cols) and offset1 not in qindex and offset2 not in qindex:
                            term_source = row[offset1]
                            term_access = row[offset2]
                        if term_source or term_access:
                            val = OntologyAnnotation(term=val, term_source=ontology_source_map[str(term_source)], term_accession=str(term_access))
                    elif isinstance(val, (int, float)) and offset1 < len(cols) and offset1 not in qindex:
                        unit = row[offset1]
                        if offset2 < len(cols) and offset3 < len(cols) and offset2 not in qindex and offset3 not in qindex:
                            term_source = row[offset2]
                            term_access = row[offset3]
                        if unit and term_source or term_access:
                            unit = OntologyAnnotation(term=unit, term_source=ontology_source_map[str(term_source)], term_accession=str(term_access))
                    qcol = cols[qi]
                    if qcol.startswith("Characteristics"):
                        qualifiers.append(Characteristic(value=val, category=cols[qi][16:-1], unit=unit))
                    elif qcol.startswith("Factor Value"):
                        qualifiers.append(FactorValue(value=val, factor_name=cols[qi][16:-1], unit=unit))
                    elif qcol.startswith("Comment"):
                        qualifiers.append(Comment(value=val, name=cols[qi][8:-1]))
                return qualifiers

            cols = list(DF.columns)
            objects = []
            for _, row in DF.iterrows():
                o = targetClass(row[cols[0]])
                for qualifier in get_qualifiers(cols, row):
                    if isinstance(qualifier, Characteristic):
                        o.characteristics.append(qualifier)
                    elif isinstance(qualifier, FactorValue):
                        o.factor_values.append(qualifier)
                    elif isinstance(qualifier, Comment):
                        o.comments.append(qualifier)
                objects.append(o)
            return objects

        # Build the Source objects using the column group beginning with Source Name
        source_object_columns_hits = [item for item in column_map if item[0] == "Source Name"]
        if len(source_object_columns_hits) == 1:  # Should only ever be 1 in a s_ file, otherwise skip
            source_object_columms = source_object_columns_hits[0]
            source_list = build_node_objects(DF[source_object_columms].drop_duplicates(), Source)
            sources = dict(map(lambda x: (':'.join([source_object_columms[0], x.name]), x), source_list))

        sample_object_columns_hits = [item for item in column_map if item[0].startswith("Sample Name")]
        sample_list = []
        for sample_object_columns in sample_object_columns_hits:  # Deal with multiple Sample Name columns
            sample_list += build_node_objects(DF[sample_object_columns].drop_duplicates(), Sample)
        if self.samples is not None:
            sample_map = dict(map(lambda x: ('Sample Name:' + x.name, x), self.samples))
            sample_keys = list(map(lambda x: 'Sample Name:' + x.name, sample_list))
            for k in sample_keys:
                samples[k] = sample_map[k]
        else:
            samples = dict(map(lambda x: ('Sample Name:' + x.name, x), sample_list))

        extract_object_columns_hits = [item for item in column_map if item[0] == "Extract Name"]
        if len(extract_object_columns_hits) == 1:  # Should only ever be 1 in an a_ file, otherwise skip
            extract_object_columns = extract_object_columns_hits[0]
            extract_list = build_node_objects(DF[extract_object_columns].drop_duplicates(), Extract)
            other_material.update(dict(map(lambda x: (':'.join([extract_object_columns[0], x.name]), x), extract_list)))

        lextract_object_columns_hits = [item for item in column_map if item[0] == "Labeled Extract Name"]
        if len(lextract_object_columns_hits) == 1:  # Should only ever be 1 in an a_ file, otherwise skip
            lextract_object_columns = lextract_object_columns_hits[0]
            lextract_list = build_node_objects(DF[lextract_object_columns].drop_duplicates(), LabeledExtract)
            other_material.update(dict(map(lambda x: (':'.join([lextract_object_columns[0], x.name]), x), lextract_list)))

        data_object_columns_hits = [item for item in column_map if " File" in item[0]]
        data_list = []
        for data_object_columns in data_object_columns_hits:  # There may be many File columns
            file_column_object_label = data_object_columns[0]
            dataFileClass = None
            if file_column_object_label == 'Raw Data File':
                dataFileClass = RawDataFile
            elif file_column_object_label == 'Raw Spectral Data File':
                dataFileClass = RawSpectralDataFile
            elif file_column_object_label == 'Derived Array Data File':
                dataFileClass = DerivedArrayDataFile
            elif file_column_object_label == 'Array Data File':
                dataFileClass = ArrayDataFile
            elif file_column_object_label == 'Derived Spectral Data File':
                dataFileClass = DerivedSpectralDataFile
            elif file_column_object_label == 'Protein Assignment File':
                dataFileClass = ProteinAssignmentFile
            elif file_column_object_label == 'Peptide Assignment File':
                dataFileClass = PeptideAssignmentFile
            elif file_column_object_label == 'Derived Array Data Matrix File':
                dataFileClass = DerivedArrayDataMatrixFile
            if dataFileClass:
                data_list += build_node_objects(DF[data_object_columns].drop_duplicates(), dataFileClass)
            else:
                raise NotImplementedError  # if column heading not recognized with current File heading types

        for datafile in data_list:
            data[':'.join([datafile.label, datafile.filename])] = datafile

        def build_process_object(cols, row, protocol_ref):

            def get_process_qualifiers(cols, row):
                qualifiers = []
                qindex = [_ for _, i in enumerate(cols) if i.endswith(" Name") or i.startswith("Parameter Value") or
                          i.startswith("Comment")]
                nindex = [_ for _, i in enumerate(cols) if i.endswith(" File") or i.startswith("Protocol REF") or
                          i.endswith(" Name")]
                ignore_index = nindex + qindex
                for qi in qindex:
                    val = row[qi]
                    unit = None
                    term_source = None
                    term_access = None
                    offset1 = qi + 1
                    offset2 = qi + 2
                    offset3 = qi + 3
                    if isinstance(val, str):
                        if offset1 < len(cols) and offset2 < len(cols) and offset1 not in ignore_index and offset2 not in ignore_index:
                            term_source = row[offset1]
                            term_access = row[offset2]
                        if term_source or term_access:
                            val = OntologyAnnotation(term=val, term_source=ontology_source_map[str(term_source)],
                                                     term_accession=str(term_access))
                    elif isinstance(val, (int, float)) and offset1 < len(cols) and offset1 not in qindex:
                        unit = row[offset1]
                        if offset2 < len(cols) and offset3 < len(cols) and offset2 not in ignore_index and offset3 not in ignore_index:
                            term_source = row[offset2]
                            term_access = row[offset3]
                        if unit and term_source or term_access:
                            unit = OntologyAnnotation(term=unit, term_source=ontology_source_map[str(term_source)],
                                                      term_accession=str(term_access))
                    qcol = cols[qi]
                    if qcol.startswith(" Name"):
                        qualifiers.append(Characteristic(value=val, category=cols[qi][16:-1], unit=unit))
                    elif qcol.startswith("Parameter Value"):
                        qualifiers.append(FactorValue(value=val, factor_name=cols[qi][16:-1], unit=unit))
                    elif qcol.startswith("Comment"):
                        qualifiers.append(Comment(value=val, name=cols[qi][8:-1]))
                return qualifiers

            o = Process(executes_protocol=protocol_map[protocol_ref])
            for qualifier in get_process_qualifiers(cols, row):
                if isinstance(qualifier, ParameterValue):
                    o.parameter_values.append(qualifier)
                elif isinstance(qualifier, Comment):
                    o.comments.append(qualifier)
            return o

        for _, object_series in DF.iterrows():  # don't drop duplicates
            process_key_sequence = []
            node_key_sequence = []
            for _cg, column_group in enumerate(column_map):
                # for each object, parse column group
                object_label = column_group[0]
                if object_label.startswith('Protocol REF'):
                    protocol_ref = object_series[object_label]
                    o = build_process_object(DF.columns, object_series, protocol_ref)
                    process_key = process_keygen(protocol_ref, column_group, _cg, DF.columns, object_series, _, DF)
                    processes[process_key] = o
                    process_key_sequence.append(process_key)
                    node_key_sequence.append(process_key)
                else:
                    node_key_sequence.append(':'.join([object_label, object_series[object_label]]))
            print('key sequence = ', process_key_sequence)
            print('node sequence = ', node_key_sequence)
            # Link the processes in each sequence
            for pair in pairwise(process_key_sequence):  # TODO: Make split/pool model with multi prev/next_process
                l = processes[pair[0]]  # get process on left of pair
                r = processes[pair[1]]  # get process on right of pair
                l.next_process = r
                r.prev_process = l

            for pair in pairwise(node_key_sequence):
                lkey = pair[0]
                rkey = pair[1]
                print('processing ', lkey, rkey)
                # add all inputs
                process_keys = processes.keys()
                if rkey in process_keys:
                    if 'Source' in lkey:
                        processes[rkey].inputs.append(sources[lkey])
                    elif 'Sample' in lkey:
                        processes[rkey].inputs.append(samples[lkey])
                    elif 'Extract' in lkey:
                        processes[rkey].inputs.append(other_material[lkey])
                    elif ' File' in lkey:
                        processes[rkey].inputs.append(data[lkey])
                elif lkey in process_keys:
                    if 'Source' in rkey:
                        processes[lkey].outputs.append(sources[rkey])
                    elif 'Sample' in rkey:
                        processes[lkey].outputs.append(samples[rkey])
                    elif 'Extract' in rkey:
                        processes[lkey].outputs.append(other_material[rkey])
                    elif ' File' in rkey:
                        processes[lkey].outputs.append(data[rkey])
                # add all outputs


        print(sources)
        print(samples)
        print(other_material)
        print(data)
        print([(i.inputs, i.outputs) for i in processes.values()])

        return sources, samples, other_material, data, processes, characteristic_categories, unit_categories


def find_in_between(a, x, y):
    result = []
    while True:
        try:
            element_gt = find_gt(a, x)
        except ValueError:
            return result

        if (element_gt > x and y==-1) or (element_gt > x and element_gt < y):
            result.append(element_gt)
            x = element_gt
        else:
            break

    while True:
        try:
            element_lt = find_lt(a, y)
        except ValueError:
            return result
        if element_lt not in result:
            if (element_lt < y and element_lt > x):
                result.append(element_lt)
                y = element_lt
            else:
                break
        else:
            break

    return result
