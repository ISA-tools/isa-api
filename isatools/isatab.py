# coding: utf-8
from __future__ import absolute_import, unicode_literals

import os
import sys
import pandas as pd
from pandas.parser import CParserError
import networkx as nx
import itertools
import logging
import re
import math
import iso8601
import six
import contextlib
import functools
import glob

from .model.v1 import *
from .io import isatab_parser

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# This will remove the "'U' flag is deprecated" DeprecationWarning in Python3
open = functools.partial(open, mode='r') if six.PY3 else functools.partial(open, mode='rbU')

errors = list()
warnings = list()



def validate(isatab_dir, config_dir):
    """ Validate an ISA-Tab archive using the Java validator that is embedded in the Python ISA-API (deprecated)
    :param isatab_dir: Path to ISA-Tab files
    :param config_dir: Path to configuration XML fileshttps://download.sublimetext.com/Sublime%20Text%202.0.2%20x64.tar.bz
    """
    if not os.path.exists(isatab_dir):
        raise IOError("isatab_dir {} does not exist".format(isatab_dir))
    print("Using source ISA Tab folder: {}".format(isatab_dir))
    print("ISA configuration XML folder: {}".format(config_dir))
    convert_command = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "convert/isa_line_commands/bin/validate.sh -c " + config_dir + " " + isatab_dir)
    from subprocess import call
    try:
        return_code = call([convert_command], shell=True)
        if return_code < 0:
            print(sys.stderr, "Terminated by signal", -return_code)
        else:
            print(sys.stderr, "Returned", return_code)
    except OSError as e:
        print(sys.stderr, "Execution failed:", e)


def dump(isa_obj, output_path, i_file_name='i_investigation.txt'):

    def _build_roles_str(roles):
        roles = roles or []
        roles_names, roles_accession_numbers, roles_source_refs = [], [], []
        for role in roles:
            roles_names.append(role.term)
            roles_accession_numbers.append(role.term_accession)
            roles_source_refs.append(role.term_source.name if role.term_source else '')
        return ";".join(roles_names), ";".join(roles_accession_numbers), ";".join(roles_source_refs)

    def _build_contacts_section_df(prefix='Investigation', contacts=list()):
        contacts_df_cols = [prefix + ' Person Last Name',
                            prefix + ' Person First Name',
                            prefix + ' Person Mid Initials',
                            prefix + ' Person Email',
                            prefix + ' Person Phone',
                            prefix + ' Person Fax',
                            prefix + ' Person Address',
                            prefix + ' Person Affiliation',
                            prefix + ' Person Roles',
                            prefix + ' Person Roles Term Accession Number',
                            prefix + ' Person Roles Term Source REF']
        if contacts:
            if contacts[0].comments:
                for comment in contacts[0].comments:
                    contacts_df_cols.append('Comment[' + comment.name + ']')
        contacts_df = pd.DataFrame(columns=tuple(contacts_df_cols))
        for i, contact in enumerate(contacts):
            roles_names, roles_accession_numbers, roles_source_refs = _build_roles_str(contact.roles)
            contacts_df_row = [
                contact.last_name,
                contact.first_name,
                contact.mid_initials,
                contact.email,
                contact.phone,
                contact.fax,
                contact.address,
                contact.affiliation,
                roles_names,
                roles_accession_numbers,
                roles_source_refs
            ]
            if contact.comments:
                for comment in contact.comments:
                    contacts_df_row.append(comment.value)
            contacts_df.loc[i] = contacts_df_row
        return contacts_df.set_index(prefix + ' Person Last Name').T

    def _build_publications_section_df(prefix='Investigation', publications=list()):
        publications_df_cols = [prefix + ' PubMed ID',
                                prefix + ' Publication DOI',
                                prefix + ' Publication Author List',
                                prefix + ' Publication Title',
                                prefix + ' Publication Status',
                                prefix + ' Publication Status Term Accession Number',
                                prefix + ' Publication Status Term Source REF']
        if publications:
            try:
                for comment in publications[0].comments:
                    publications_df_cols.append('Comment[' + comment.name + ']')
            except TypeError:
                pass
        publications_df = pd.DataFrame(columns=tuple(publications_df_cols))
        for i, publication in enumerate(publications):
            publications_df_row = [
                publication.pubmed_id,
                publication.doi,
                publication.author_list,
                publication.title,
                publication.status.term,
                publication.status.term_accession,
                publication.status.term_source.name if publication.status.term_source else '',
            ]
            try:
                for comment in publication.comments:
                    publications_df_row.append(comment.value)
            except TypeError:
                pass
            publications_df.loc[i] = publications_df_row
        return publications_df.set_index(prefix +' PubMed ID').T
    import re
    if not re.compile('i_(.*?)\.txt').match(i_file_name):
        raise NameError("Investigation file must match pattern i_*.txt")
    if os.path.exists(output_path):
        fp = open(os.path.join(output_path, i_file_name), mode='w')
    else:
        raise IOError("Can't find " + output_path)
    if not isinstance(isa_obj, Investigation):
        raise NotImplementedError("Can only dump an Investigation object")

    # Process Investigation object first to write the investigation file
    investigation = isa_obj

    # Write ONTOLOGY SOURCE REFERENCE section
    ontology_source_references_df = pd.DataFrame(columns=('Term Source Name',
                                                          'Term Source File',
                                                          'Term Source Version',
                                                          'Term Source Description'
                                                          )
                                                 )
    for i,  ontology_source_reference in enumerate(investigation.ontology_source_references):
        ontology_source_references_df.loc[i] = [
            ontology_source_reference.name,
            ontology_source_reference.file,
            ontology_source_reference.version,
            ontology_source_reference.description
        ]
    ontology_source_references_df = ontology_source_references_df.set_index('Term Source Name').T
    fp.write('ONTOLOGY SOURCE REFERENCE\n')
    ontology_source_references_df.to_csv(path_or_buf=fp, mode='ab', sep=str('\t'), encoding='utf-8',
                                         index_label='Term Source Name')  # Need to set index_label as top left cell
    #
    #  Write INVESTIGATION section
    inv_df_cols = ['Investigation Identifier',
                   'Investigation Title',
                   'Investigation Description',
                   'Investigation Submission Date',
                   'Investigation Public Release Date']
    for comment in sorted(investigation.comments, key=lambda x: x.name):
        inv_df_cols.append('Comment[' + comment.name + ']')
    investigation_df = pd.DataFrame(columns=tuple(inv_df_cols))
    inv_df_rows = [
        investigation.identifier,
        investigation.title,
        investigation.description,
        investigation.submission_date,
        investigation.public_release_date
    ]
    for comment in sorted(investigation.comments, key=lambda x: x.name):
        inv_df_rows.append(comment.value)
    investigation_df.loc[0] = inv_df_rows
    investigation_df = investigation_df.set_index('Investigation Identifier').T
    fp.write('INVESTIGATION\n')
    investigation_df.to_csv(path_or_buf=fp, mode='a', sep=str('\t'), encoding='utf-8',
                            index_label='Investigation Identifier')  # Need to set index_label as top left cell

    # Write INVESTIGATION PUBLICATIONS section
    investigation_publications_df = _build_publications_section_df(publications=investigation.publications)
    fp.write('INVESTIGATION PUBLICATIONS\n')
    investigation_publications_df.to_csv(path_or_buf=fp, mode='a', sep=str('\t'), encoding='utf-8',
                                         index_label='Investigation PubMed ID')

    # Write INVESTIGATION CONTACTS section
    investigation_contacts_df = _build_contacts_section_df(contacts=investigation.contacts)
    fp.write('INVESTIGATION CONTACTS\n')
    investigation_contacts_df.to_csv(path_or_buf=fp, mode='a', sep=str('\t'), encoding='utf-8',
                                     index_label='Investigation Person Last Name')

    # Write STUDY sections
    for study in investigation.studies:
        study_df_cols = ['Study Identifier',
                         'Study Title',
                         'Study Description',
                         'Study Submission Date',
                         'Study Public Release Date',
                         'Study File Name']
        if study.comments is not None:
            for comment in sorted(study.comments, key=lambda x: x.name):
                study_df_cols.append('Comment[' + comment.name + ']')
        study_df = pd.DataFrame(columns=tuple(study_df_cols))
        study_df_row = [
            study.identifier,
            study.title,
            study.description,
            study.submission_date,
            study.public_release_date,
            study.filename
        ]
        if study.comments is not None:
            for comment in sorted(study.comments, key=lambda x: x.name):
                study_df_row.append(comment.value)
        study_df.loc[0] = study_df_row
        study_df = study_df.set_index('Study Identifier').T
        fp.write('STUDY\n')
        study_df.to_csv(path_or_buf=fp, mode='a', sep=str('\t'), encoding='utf-8',
                        index_label='Study Identifier')

        # Write STUDY DESIGN DESCRIPTORS section
        study_design_descriptors_df = pd.DataFrame(columns=('Study Design Type',
                                                            'Study Design Type Term Accession Number',
                                                            'Study Design Type Term Source REF'
                                                            )
                                                   )
        for i, design_descriptor in enumerate(study.design_descriptors):
            study_design_descriptors_df.loc[i] = [
                design_descriptor.term,
                design_descriptor.term_accession,
                design_descriptor.term_source.name if design_descriptor.term_source else ''
            ]
            study_design_descriptors_df = study_design_descriptors_df.set_index('Study Design Type').T
            fp.write('STUDY DESIGN DESCRIPTORS\n')
            study_design_descriptors_df.to_csv(path_or_buf=fp, mode='a', sep=str('\t'),
                                               encoding='utf-8', index_label='Study Design Type')

        # Write STUDY PUBLICATIONS section
        study_publications_df = _build_publications_section_df(prefix='Study', publications=study.publications)
        fp.write('STUDY PUBLICATIONS\n')
        study_publications_df.to_csv(path_or_buf=fp, mode='a', sep=str('\t'),
                                     encoding='utf-8', index_label='Study PubMed ID')

        # Write STUDY FACTORS section
        study_factors_df = pd.DataFrame(columns=('Study Factor Name',
                                                 'Study Factor Type',
                                                 'Study Factor Type Term Accession Number',
                                                 'Study Factor Type Term Source REF'
                                                 )
                                        )
        for i, factor in enumerate(study.factors):
            study_factors_df.loc[i] = [
                factor.name,
                factor.factor_type.term,
                factor.factor_type.term_accession,
                factor.factor_type.term_source.name if factor.factor_type.term_source else ''
            ]
        study_factors_df = study_factors_df.set_index('Study Factor Name').T
        fp.write('STUDY FACTORS\n')
        study_factors_df.to_csv(path_or_buf=fp, mode='a', sep=str('\t'),
                                encoding='utf-8', index_label='Study Factor Name')

        # Write STUDY ASSAYS section
        study_assays_df = pd.DataFrame(columns=(
                                                'Study Assay File Name',
                                                'Study Assay Measurement Type',
                                                'Study Assay Measurement Type Term Accession Number',
                                                'Study Assay Measurement Type Term Source REF',
                                                'Study Assay Technology Type',
                                                'Study Assay Technology Type Term Accession Number',
                                                'Study Assay Technology Type Term Source REF',
                                                'Study Assay Technology Platform',
                                                )
                                       )
        for i, assay in enumerate(study.assays):
            study_assays_df.loc[i] = [
                assay.filename,
                assay.measurement_type.term,
                assay.measurement_type.term_accession,
                assay.measurement_type.term_source.name if assay.measurement_type.term_source else '',
                assay.technology_type.term,
                assay.technology_type.term_accession,
                assay.technology_type.term_source.name if assay.technology_type.term_source else '',
                assay.technology_platform
            ]
        study_assays_df = study_assays_df.set_index('Study Assay File Name').T
        fp.write('STUDY ASSAYS\n')
        study_assays_df.to_csv(path_or_buf=fp, mode='a', sep=str('\t'),
                               encoding='utf-8',index_label='Study Assay File Name')

        # Write STUDY PROTOCOLS section
        study_protocols_df = pd.DataFrame(columns=('Study Protocol Name',
                                                   'Study Protocol Type',
                                                   'Study Protocol Type Term Accession Number',
                                                   'Study Protocol Type Term Source REF',
                                                   'Study Protocol Description',
                                                   'Study Protocol URI',
                                                   'Study Protocol Version',
                                                   'Study Protocol Parameters Name',
                                                   'Study Protocol Parameters Name Term Accession Number',
                                                   'Study Protocol Parameters Name Term Source REF',
                                                   'Study Protocol Components Name',
                                                   'Study Protocol Components Type',
                                                   'Study Protocol Components Type Term Accession Number',
                                                   'Study Protocol Components Type Term Source REF',
                                                   )
                                          )
        for i, protocol in enumerate(study.protocols):
            parameters_names, parameters_accession_numbers, parameters_source_refs = [], [], []
            for parameter in protocol.parameters:
                parameters_names.append(parameter.parameter_name.term)
                parameters_accession_numbers.append(parameter.parameter_name.term_accession)
                parameters_source_refs.append(parameter.parameter_name.term_source.name if parameter.parameter_name.term_source else '')
            component_names, component_types,  = [], []
            component_types_accession_numbers, component_types_source_refs = [], []
            for component in protocol.components:
                component_names.append(component.name)
                component_types.append(component.component_type.term)
                component_types_accession_numbers.append(component.component_type.term_accession)
                component_types_source_refs.append(component.component_type.term_source.name if component.component_type.term_source else '')
            study_protocols_df.loc[i] = [
                protocol.name,
                protocol.protocol_type.term,
                protocol.protocol_type.term_accession,
                protocol.protocol_type.term_source.name if protocol.protocol_type.term_source else '',
                protocol.description,
                protocol.uri,
                protocol.version,
                ';'.join(parameters_names),
                ';'.join(parameters_accession_numbers),
                ';'.join(parameters_source_refs),
                ';'.join(component_names),
                ';'.join(component_types),
                ';'.join(component_types_accession_numbers),
                ';'.join(component_types_source_refs)
            ]
        study_protocols_df = study_protocols_df.set_index('Study Protocol Name').T
        fp.write('STUDY PROTOCOLS\n')
        study_protocols_df.to_csv(path_or_buf=fp, mode='a', sep=str('\t'),
                                  encoding='utf-8', index_label='Study Protocol Name')

        # Write STUDY CONTACTS section
        study_contacts_df = _build_contacts_section_df(prefix='Study', contacts=study.contacts)
        fp.write('STUDY CONTACTS\n')
        study_contacts_df.to_csv(path_or_buf=fp, mode='a', sep=str('\t'),
                                 encoding='utf-8', index_label='Study Person Last Name')
    write_study_table_files(investigation, output_path)
    write_assay_table_files(investigation, output_path)

    fp.close()
    return investigation


def _get_start_end_nodes(G):
    start_nodes = list()
    end_nodes = list()
    for process in (n for n in G.nodes() if isinstance(n, Process)):
        if process.prev_process is None:
            for material in (m for m in process.inputs if not isinstance(m, DataFile)):
                start_nodes.append(material)
        outputs_no_data = [m for m in process.outputs if not isinstance(m, DataFile)]
        if process.next_process is None:
            if not outputs_no_data:
                end_nodes.append(process)
            else:
                for material in outputs_no_data:
                    end_nodes.append(material)
    return start_nodes, end_nodes


def _longest_path_and_attrs(G):
    start_nodes, end_nodes = _get_start_end_nodes(G)
    from networkx.algorithms import all_simple_paths
    longest = (0, None)
    for start_node, end_node in itertools.product(start_nodes, end_nodes):
        for path in all_simple_paths(G, start_node, end_node):
            length = len(path)
            for n in path:
                if isinstance(n, Source):
                    length += len(n.characteristics)
                elif isinstance(n, Sample):
                    length += len(n.characteristics) + len(n.factor_values)
                elif isinstance(n, Material):
                    length += len(n.characteristics)
                elif isinstance(n, Process):
                    length += len(n.additional_properties) + len([o for o in n.outputs if isinstance(o, DataFile)])
                if n.comments is not None:
                    length += len(n.comments)
            if length > longest[0]:
                longest = (length, path)
    return longest[1]

prev = ''  # used in rolling_group(val) in write_assay_table_files(inv_obj, output_dir)


def _all_end_to_end_paths(G, start_nodes, end_nodes):
    paths = list()
    for start, end in itertools.product(start_nodes, end_nodes):
        paths.extend(list(nx.algorithms.all_simple_paths(G, start, end)))
    return paths

KEY_POSTFIX_UNIT = '_unit'
KEY_POSTFIX_TERMSOURCE = '_termsource'
KEY_POSTFIX_TERMACCESSION = '_termaccession'
LABEL_UNIT = 'Unit'
LABEL_TERM_SOURCE = 'Term Source REF'
LABEL_TERM_ACCESSION = 'Term Accession Number'
LABEL_PROTOCOL_REF = 'Protocol REF'


def _fv_label(factor_name): return 'Factor Value[' + factor_name + ']'


def _charac_label(charac_type_name): return 'Characteristics[' + charac_type_name + ']'


def _set_charac_cols(prefix, characteristics, cols, col_map):
    for c in sorted(characteristics, key=lambda x: id(x.category)):
        obj_charac_key = prefix + '_char[' + c.category.term + ']'
        cols.append(obj_charac_key)
        col_map[obj_charac_key] = _charac_label(c.category.term)
        if isinstance(c.value, (int, float)):
            cols.extend((obj_charac_key + KEY_POSTFIX_UNIT,
                         obj_charac_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE,
                         obj_charac_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION))
            col_map[obj_charac_key + KEY_POSTFIX_UNIT] = LABEL_UNIT
            col_map[obj_charac_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE] = LABEL_TERM_SOURCE
            col_map[obj_charac_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION] = LABEL_TERM_ACCESSION
        elif isinstance(c.value, OntologyAnnotation):
            cols.extend((obj_charac_key + KEY_POSTFIX_TERMSOURCE,
                         obj_charac_key + KEY_POSTFIX_TERMACCESSION))
            col_map[obj_charac_key + KEY_POSTFIX_TERMSOURCE] = LABEL_TERM_SOURCE
            col_map[obj_charac_key + KEY_POSTFIX_TERMACCESSION] = LABEL_TERM_ACCESSION


def _set_charac_vals(prefix, characteristics, df, i):
    for c in sorted(characteristics, key=lambda x: id(x.category)):
        obj_charac_key = prefix + '_char[' + c.category.term + ']'
        df.loc[i, obj_charac_key] = c.value
        if isinstance(c.value, (int, float)):
            df.loc[i, obj_charac_key + KEY_POSTFIX_UNIT] = c.unit.term
            df.loc[i, obj_charac_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE] =  c.unit.term_source.name if c.unit.term_source else ''
            df.loc[i, obj_charac_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION] = c.unit.term_accession
        elif isinstance(c.value, OntologyAnnotation):
            df.loc[i, obj_charac_key] = c.value.term
            df.loc[i, obj_charac_key + KEY_POSTFIX_TERMSOURCE] = c.value.term_source.name if c.value.term_source else ''
            df.loc[i, obj_charac_key + KEY_POSTFIX_TERMACCESSION] = c.value.term_accession


def _set_factor_value_cols(prefix, factor_values, cols, col_map):
    for fv in sorted(factor_values, key=lambda x: id(x.factor_name)):
        obj_fv_key = prefix + '_fv[' + fv.factor_name.name + ']'
        cols.append(obj_fv_key)
        col_map[obj_fv_key] = _fv_label(fv.factor_name.name)
        if isinstance(fv.value, (int, float)):
            cols.extend((obj_fv_key + KEY_POSTFIX_UNIT,
                         obj_fv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE,
                         obj_fv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION))
            col_map[obj_fv_key + KEY_POSTFIX_UNIT] = LABEL_UNIT
            col_map[obj_fv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE] = LABEL_TERM_SOURCE
            col_map[obj_fv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION] = LABEL_TERM_ACCESSION
        elif isinstance(fv.value, OntologyAnnotation):
            cols.extend((obj_fv_key + KEY_POSTFIX_TERMSOURCE,
                         obj_fv_key + KEY_POSTFIX_TERMACCESSION))
            col_map[obj_fv_key + KEY_POSTFIX_TERMSOURCE] = LABEL_TERM_SOURCE
            col_map[obj_fv_key + KEY_POSTFIX_TERMACCESSION] = LABEL_TERM_ACCESSION


def _set_factor_value_vals(prefix, factor_values, df, i):
    for fv in sorted(factor_values, key=lambda x: id(x.factor_name)):
        obj_fv_key = prefix + '_fv[' + fv.factor_name.name + ']'
        df.loc[i, obj_fv_key] = fv.value
        if isinstance(fv.value, (int, float)):
            df.loc[i, obj_fv_key + KEY_POSTFIX_UNIT] = fv.unit.term
            df.loc[i, obj_fv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE] = fv.unit.term_source.name if fv.unit.term_source else ''
            df.loc[i, obj_fv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION] = fv.unit.term_accession
        elif isinstance(fv.value, OntologyAnnotation):
            df.loc[i, obj_fv_key] = fv.value.term
            df.loc[i, obj_fv_key + KEY_POSTFIX_TERMSOURCE] = fv.value.term_source.name if fv.value.term_source else ''
            df.loc[i, obj_fv_key + KEY_POSTFIX_TERMACCESSION] = fv.value.term_accession

KEY_POSTFIX_DATE = '_date'
LABEL_DATE = 'Date'
KEY_POSTFIX_PERFORMER = '_performer'
LABEL_PERFORMER = 'Performer'


def _parameter_value_label(parameter_name): return 'Parameter Value[' + parameter_name + ']'


def _set_protocol_cols(protrefcount, prottypes, process, cols, col_map):
    obj_process_key = 'protocol[' + str(protrefcount) + ']'
    cols.append(obj_process_key)
    col_map[obj_process_key] = LABEL_PROTOCOL_REF
    if process.date is not None:
        cols.append(obj_process_key + KEY_POSTFIX_DATE)
        col_map[obj_process_key + KEY_POSTFIX_DATE] = LABEL_DATE
    if process.performer is not None:
        cols.append(obj_process_key + KEY_POSTFIX_PERFORMER)
        col_map[obj_process_key + KEY_POSTFIX_PERFORMER] = LABEL_PERFORMER
    for pv in reversed(sorted(process.parameter_values, key=lambda x: x.category.parameter_name.name)):
        obj_process_pv_key = '_pv[' + pv.category.parameter_name.name + ']'
        if isinstance(pv.value, (int, float)):
            cols.extend((obj_process_key + obj_process_pv_key,
                         obj_process_key + obj_process_pv_key + KEY_POSTFIX_UNIT,
                         obj_process_key + obj_process_pv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE,
                         obj_process_key + obj_process_pv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION))
            col_map[obj_process_key + obj_process_pv_key] = _parameter_value_label(pv.category.parameter_name.name)
            col_map[obj_process_key + obj_process_pv_key + KEY_POSTFIX_UNIT] = LABEL_UNIT
            col_map[obj_process_key + obj_process_pv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMSOURCE] = LABEL_TERM_SOURCE
            col_map[obj_process_key + obj_process_pv_key + KEY_POSTFIX_UNIT + KEY_POSTFIX_TERMACCESSION] = LABEL_TERM_ACCESSION
        elif isinstance(pv.value, OntologyAnnotation):
            cols.extend((obj_process_key + obj_process_pv_key,
                         obj_process_key + obj_process_pv_key + KEY_POSTFIX_TERMSOURCE,
                         obj_process_key + obj_process_pv_key + KEY_POSTFIX_TERMACCESSION))
            col_map[obj_process_key + obj_process_pv_key] = _parameter_value_label(pv.category.parameter_name.name)
            col_map[obj_process_key + obj_process_pv_key + KEY_POSTFIX_TERMSOURCE] = LABEL_TERM_SOURCE
            col_map[obj_process_key + obj_process_pv_key + KEY_POSTFIX_TERMACCESSION] = LABEL_TERM_ACCESSION
        else:
            cols.append(obj_process_key + obj_process_pv_key)
            col_map[obj_process_key + obj_process_pv_key] = _parameter_value_label(pv.category.parameter_name.name)
    for prop in reversed(sorted(process.additional_properties.keys())):
        cols.append(obj_process_key + '_prop[' + prop + ']')
        col_map[obj_process_key + '_prop[' + prop + ']'] = prop
    for output in (x for x in process.outputs if isinstance(x, DataFile)):
        cols.append('data[' + output.label + ']')
        col_map['data[' + output.label + ']'] = output.label
        for comment in output.comments:
            cols.append('data[' + output.label + ']_comment[' + comment.name + ']')
            col_map['data[' + output.label + ']_comment[' + comment.name + ']'] = 'Comment[' + comment.name + ']'
    if process.executes_protocol.protocol_type.name not in prottypes.values():
        prottypes[protrefcount] = process.executes_protocol.protocol_type.name
        protrefcount += 1


def write_assay_table_files(inv_obj, output_dir):
    """
        Writes out assay table files according to pattern defined by

        Sample Name,
        Protocol Ref: 'sample collection', [ ParameterValue[], ... ],
        Material Name, [ Characteristics[], ... ]
        [ FactorValue[], ... ]


    """
    if isinstance(inv_obj, Investigation):
        for study_obj in inv_obj.studies:
            for assay_obj in study_obj.assays:
                if assay_obj.graph is None: break
                cols = list()
                mcount = 0
                protrefcount = 0
                protnames = {}
                col_map = {}
                for node in _longest_path_and_attrs(assay_obj.graph):
                    if isinstance(node, Sample):
                        cols.append('sample')
                        col_map['sample'] = 'Sample Name'
                    elif isinstance(node, Material):
                        if node.type == 'Labeled Extract Name':
                            cols.append('lextract')
                            cols.append('lextract_label')
                            cols.append('lextract_label_termsource')
                            cols.append('lextract_label_termaccession')
                            col_map['lextract'] = 'Labeled Extract Name'
                            col_map['lextract_label'] = 'Label'
                            col_map['lextract_label_termsource'] = 'Term Source REF'
                            col_map['lextract_label_termaccession'] = 'Term Accession Number'
                        elif node.type == 'Extract Name':
                            cols.append('extract')
                            col_map['extract'] = 'Extract Name'
                            _set_charac_cols('extract', node.characteristics, cols, col_map)
                        else:
                            cols.append('material[' + str(mcount) + ']')
                            col_map['material[' + str(mcount) + ']'] = 'Material Name'
                            _set_charac_cols('material', node.characteristics, cols, col_map)
                            mcount += 1
                    elif isinstance(node, Process):
                        cols.append('protocol[' + str(protrefcount) + ']')
                        col_map['protocol[' + str(protrefcount) + ']'] = 'Protocol REF'
                        if node.date is not None:
                            cols.append('protocol[' + str(protrefcount) + ']_date')
                            col_map['protocol[' + str(protrefcount) + ']_date'] = 'Date'
                        if node.performer is not None:
                            cols.append('protocol[' + str(protrefcount) + ']_performer')
                            col_map['protocol[' + str(protrefcount) + ']_performer'] = 'Performer'
                        for pv in reversed(sorted(node.parameter_values, key=lambda x: x.category.parameter_name.term)):
                            if isinstance(pv.value, (int, float)):
                                cols.extend(('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit_termsource',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit_termaccession'))
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']'] = 'Parameter Value[' + pv.category.parameter_name.term + ']'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit'] = 'Unit'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit_termsource'] = 'Term Source REF'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit_termaccession'] = 'Term Accession Number'
                            elif isinstance(pv.value, OntologyAnnotation):
                                cols.extend(('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_termsource',
                                             'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_termaccession',))
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']'] = 'Parameter Value[' + pv.category.parameter_name.term + ']'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_termsource'] = 'Term Source REF'
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_termaccession'] = 'Term Accession Number'
                            else:
                                cols.append('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']',)
                                col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']'] = 'Parameter Value[' + pv.category.parameter_name.term + ']'
                        # TODO Check how model objects are used, do all additional_prop now go into .name?
                        for prop in reversed(sorted(node.additional_properties.keys())):
                            cols.append('protocol[' + str(protrefcount) + ']_prop[' + prop + ']')
                            col_map['protocol[' + str(protrefcount) + ']_prop[' + prop + ']'] = prop
                        if node.executes_protocol.protocol_type.term == 'nucleic acid sequencing':
                            cols.append('protocol[' + str(protrefcount) + ']_prop[' + 'Assay Name' + ']')
                            col_map['protocol[' + str(protrefcount) + ']_prop[' + 'Assay Name' + ']'] = 'Assay Name'
                        elif node.executes_protocol.protocol_type.term == 'nucleic acid hybridization':
                            cols.append('protocol[' + str(protrefcount) + ']_prop[' + 'Hybridization Assay Name' + ']')
                            col_map['protocol[' + str(protrefcount) + ']_prop[' + 'Hybridization Assay Name' + ']'] = 'Hybridization Assay Name'
                            cols.append('protocol[' + str(protrefcount) + ']_prop[' + 'Array Design REF' + ']')
                            col_map['protocol[' + str(protrefcount) + ']_prop[' + 'Array Design REF' + ']'] = 'Array Design REF'
                        elif node.executes_protocol.protocol_type.term == 'data collection':
                            cols.append('protocol[' + str(protrefcount) + ']_prop[' + 'Scan Name' + ']')
                            col_map['protocol[' + str(protrefcount) + ']_prop[' + 'Scan Name' + ']'] = 'Scan Name'

                        for output in (x for x in node.outputs if isinstance(x, DataFile)):
                            cols.append('data[' + output.label + ']')
                            col_map['data[' + output.label + ']'] = output.label
                            if output.comments:
                                for comment in output.comments:
                                    cols.append('data[' + output.label + ']_comment[' + comment.name + ']')
                                    col_map['data[' + output.label + ']_comment[' + comment.name + ']'] = 'Comment[' + comment.name + ']'
                        if node.executes_protocol.name not in protnames:
                            protnames[node.executes_protocol.name] = protrefcount
                            protrefcount += 1
                        # protrefcount = _set_protocol_cols(protrefcount, prottypes, node, cols, col_map)
                    elif isinstance(node, DataFile):
                        pass  # we process DataFile above inside Process
                import pandas as pd
                df = pd.DataFrame(columns=cols)
                i = 0
                start_nodes, end_nodes = _get_start_end_nodes(assay_obj.graph)
                for path in _all_end_to_end_paths(assay_obj.graph, start_nodes, end_nodes):
                    mcount = 0
                    #compound_key = str()
                    compound_key = []
                    for node in path:
                        if isinstance(node, Sample):
                            df.loc[i, 'sample'] = node.name
                            #compound_key += node.name + '/'
                            compound_key.append(node.name)
                        elif isinstance(node, Material):
                            if node.type == 'Labeled Extract Name':
                                df.loc[i, 'lextract'] = node.name
                                #compound_key += node.name + '/'
                                compound_key.append(node.name)
                                df.loc[i, 'lextract_label'] = node.characteristics[0].value.term
                                df.loc[i, 'lextract_label_termsource'] = node.characteristics[0].value.term_source.name if node.characteristics[0].value.term_source else ''
                                df.loc[i, 'lextract_label_termaccession'] = node.characteristics[0].value.term_accession
                            elif node.type == 'Extract Name':
                                df.loc[i, 'extract'] = node.name
                                #compound_key += node.name + '/'
                                compound_key.append(node.name)
                                _set_charac_vals('extract', node.characteristics, df, i)
                            else:
                                df.loc[i, 'material[' + str(mcount) + ']'] = node.name
                                #compound_key += node.name + '/'
                                compound_key.append(node.name)
                                _set_charac_vals('material', node.characteristics, df, i)
                                mcount += 1
                        elif isinstance(node, Process):
                            def find(n):
                                v = 0
                                for k, v in six.iteritems(protnames):
                                    if k == n.executes_protocol.name:
                                        return v
                                return v
                            protrefcount = find(node)
                            df.loc[i, 'protocol[' + str(protrefcount) + ']'] = node.executes_protocol.name
                            #compound_key += str(protrefcount) + '/' + node.name + '/'
                            compound_key.extend([str(protrefcount), node.name])
                            if node.date is not None:
                                df.loc[i, 'protocol[' + str(protrefcount) + ']_date'] = node.date
                            if node.performer is not None:
                                df.loc[i, 'protocol[' + str(protrefcount) + ']_performer'] = node.performer
                            for pv in reversed(sorted(node.parameter_values, key=lambda x: x.category.parameter_name.term)):
                                if isinstance(pv.value, (int, float)):
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']'] = pv.value
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit'] = pv.unit.name
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit_termsource'] = pv.unit.term_source.name if pv.unit.term_source else ''
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit_termaccession'] = pv.unit.term_accession
                                elif isinstance(pv.value, OntologyAnnotation):
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']'] = pv.value.term
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_termsource'] = pv.value.term_source.name if pv.value.term_source else ''
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_termaccession'] = pv.value.term_accession
                                else:
                                    df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']'] = pv.value
                            # TODO Check how model objects are used, do all additional_prop now go into .name?
                            for prop in reversed(sorted(node.additional_properties.keys())):
                                df.loc[i, 'protocol[' + str(protrefcount) + ']_prop[' + prop + ']'] = node.additional_properties[prop]
                                #compound_key += str(protrefcount) + '/' + prop + '/' + node.additional_properties[prop]
                                compound_key.extend([str(protrefcount), prop, node.additional_properties[prop]])
                            if node.executes_protocol.protocol_type.term == 'nucleic acid sequencing':
                                df.loc[i, 'protocol[' + str(protrefcount) + ']_prop[' + 'Assay Name' + ']'] = node.name
                                #compound_key += str(protrefcount) + '/' + 'Assay Name' + '/' + node.name
                                compound_key.extend([str(protrefcount), 'Assay Name', node.name])
                            elif node.executes_protocol.protocol_type.term == 'nucleic acid hybridization':
                                df.loc[i, 'protocol[' + str(protrefcount) + ']_prop[' + 'Hybridization Assay Name' + ']'] = node.name
                                #compound_key += str(protrefcount) + '/' + 'Hybridization Assay Name' + '/' + node.name
                                compound_key.extend([str(protrefcount), 'Hybridization Assay Name', node.name])
                                df.loc[i, 'protocol[' + str(protrefcount) + ']_prop[' + 'Array Design REF' + ']'] = node.array_design_ref
                                #compound_key += str(protrefcount) + '/' + 'Array Design REF' + '/' + node.array_design_ref
                                compound_key.extend([str(protrefcount), 'Array Design REF', node.array_design_ref])
                            elif node.executes_protocol.protocol_type.term == 'data collection':
                                df.loc[i, 'protocol[' + str(protrefcount) + ']_prop[' + 'Scan Name' + ']'] = node.name
                                #compound_key += str(protrefcount) + '/' + 'Scan Name' + '/' + node.name
                                compound_key.extend([str(protrefcount), 'Scan Name', node.name])
                            for output in (x for x in node.outputs if isinstance(x, DataFile)):
                                df.loc[i, 'data[' + output.label + ']'] = output.filename
                                if output.comments:
                                    for comment in output.comments:
                                        df.loc[i, 'data[' + output.label + ']_comment[' + comment.name + ']'] = comment.value
                    df.loc[i, 'compound_key'] = '/'.join(compound_key)

                    i += 1

                # reduce rows of data on separate lines

                # can we group by matching all columns minus the data columns?
                import re
                data_regex = re.compile('data\[(.*?)\]')
                # cols_no_data = [col for col in cols if not data_regex.match(col)]  # column list without data cols

                # calculate groupings
                def rolling_group(val):
                    global prev
                    if val != prev:
                        rolling_group.group += 1  # val != prev is signal to switch group; rows sorted by cols_no_data
                    prev = val
                    return rolling_group.group
                rolling_group.group = 0  # static variable
                groups = df.groupby(df['compound_key'].apply(rolling_group), as_index=True)  # groups by column 1 only

                # merge items in column groups
                def reduce(group, column):
                    col = group[column]
                    s = [str(each) for each in col if pd.notnull(each)]
                    if s:
                        return s[0]
                    else:
                        return ''
                df = groups.apply(lambda g: pd.Series([reduce(g, col) for col in g.columns], index=g.columns))

                #  cleanup column headers before writing out df
                # WARNING: don't just dump out col_map.values() as we need to put columns back in order
                df = df.sort_values(by=df.columns[0], ascending=True)  # arbitrary sort on column 0 (Sample name)
                del df['compound_key']  # release compound_key as we don't write it out
                for i, col in enumerate(df.columns):
                    cols[i] = col_map[col]
                    if col_map[col] == 'Characteristics[Material Type]':
                        cols[i] = 'Material Type'
                    if col_map[col] == 'Parameter Value[Array Design REF]':
                        cols[i] = 'Array Design REF'
                    if data_regex.match(col) is not None:
                        if data_regex.findall(col)[0] == 'Raw Data File':
                            if assay_obj.technology_type.term == 'DNA microarray':
                                cols[i] = 'Array Data File'
                df.columns = cols  # reset column headers
                # drop completely empty columns
                import numpy as np
                df = df.replace('', np.nan)
                df = df.dropna(axis=1, how='all')
                assay_obj.df = df
                #with open(os.path.join(output_dir, assay_obj.filename)) as fp:
                df.to_csv(path_or_buf=os.path.join(output_dir, assay_obj.filename), mode='w', index=False, sep=str('\t'), encoding='utf-8',)


def write_study_table_files(inv_obj, output_dir):
    """
        Writes out study table files according to pattern defined by

        Source Name, [ Characteristics[], ... ],
        Protocol Ref*: 'sample collection', [ ParameterValue[], ... ],
        Sample Name, [ Characteristics[], ... ]
        [ FactorValue[], ... ]

        which should be equivalent to studySample.xml in default config

    """

    if not isinstance(inv_obj, Investigation):
        raise NotImplementedError
    for study_obj in inv_obj.studies:
        if study_obj.graph is None: break
        cols = list()
        protrefcount = 0
        protnames = {}
        col_map = {}

        for node in _longest_path_and_attrs(study_obj.graph):
            if isinstance(node, Source):
                cols.append('source')
                col_map['source'] = 'Source Name'
                _set_charac_cols('source', node.characteristics, cols, col_map)
            elif isinstance(node, Process):

                cols.append('protocol[' + str(protrefcount) + ']')
                col_map['protocol[' + str(protrefcount) + ']'] = 'Protocol REF'
                if node.date is not None:
                    cols.append('protocol[' + str(protrefcount) + ']_date')
                    col_map['protocol[' + str(protrefcount) + ']_date'] = 'Date'
                if node.performer is not None:
                    cols.append('protocol[' + str(protrefcount) + ']_performer')
                    col_map['protocol[' + str(protrefcount) + ']_performer'] = 'Performer'
                for pv in reversed(sorted(node.parameter_values, key=lambda x: x.category.parameter_name.term)):
                    if isinstance(pv.value, (int, float)):
                        cols.extend(('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']',
                                     'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit',
                                     'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit_termsource',
                                     'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit_termaccession'))
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']'] = 'Parameter Value[' + pv.category.parameter_name.term + ']'
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit'] = 'Unit'
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit_termsource'] = 'Term Source REF'
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit_termaccession'] = 'Term Accession Number'
                    elif isinstance(pv.value, OntologyAnnotation):
                        cols.extend(('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']',
                                     'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_termsource',
                                     'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_termaccession',))
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']'] = 'Parameter Value[' + pv.category.parameter_name.term + ']'
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_termsource'] = 'Term Source REF'
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_termaccession'] = 'Term Accession Number'
                    else:
                        cols.append('protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']')
                        col_map['protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']'] = 'Parameter Value[' + pv.category.parameter_name.term + ']'
                if node.executes_protocol.name not in protnames:
                    protnames[node.executes_protocol.name] = protrefcount
                    protrefcount += 1
            elif isinstance(node, Sample):
                cols.append('sample')
                col_map['sample'] = 'Sample Name'
                _set_charac_cols('sample', node.characteristics, cols, col_map)
                _set_factor_value_cols('sample', node.factor_values, cols, col_map)
        import pandas as pd
        df = pd.DataFrame(columns=cols)
        i = 0

        start_nodes, end_nodes = _get_start_end_nodes(study_obj.graph)
        for path in _all_end_to_end_paths(study_obj.graph, start_nodes, end_nodes):
            for node in path:
                if isinstance(node, Source):
                    df.loc[i, 'source'] = node.name
                    _set_charac_vals('source', node.characteristics, df, i)
                elif isinstance(node, Process):
                    def find(n):
                        v = 0
                        for k, v in six.iteritems(protnames):
                            if k == n.executes_protocol.name:
                                return v
                        return v
                    protrefcount = find(node)
                    df.loc[i, 'protocol[' + str(protrefcount) + ']'] = node.executes_protocol.name
                    if node.date is not None:
                        df.loc[i, 'protocol[' + str(protrefcount) + ']_date'] = node.date
                    if node.performer is not None:
                        df.loc[i, 'protocol[' + str(protrefcount) + ']_performer'] = node.performer
                    for pv in reversed(sorted(node.parameter_values, key=lambda x: x.category.parameter_name.term)):
                        if isinstance(pv.value, (int, float)):
                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']'] = pv.value
                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit'] = pv.unit.term
                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit_termsource'] = pv.unit.term_source.name if pv.unit.term_source else ''
                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_unit_termaccession'] = pv.unit.term_accession
                        elif isinstance(pv.value, OntologyAnnotation):
                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']'] = pv.value.term
                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_termsource'] = pv.value.term_source
                            df.loc[i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.parameter_name.term + ']_termaccession'] = pv.value.term_accession
                        else:
                            df.loc[i, i, 'protocol[' + str(protrefcount) + ']_pv[' + pv.category.characteristic_type.name + ']'] = pv.value
                elif isinstance(node, Sample):
                    df.loc[i, 'sample'] = node.name
                    _set_charac_vals('sample', node.characteristics, df, i)
                    _set_factor_value_vals('sample', node.factor_values, df, i)
            i += 1
        # WARNING: don't just dump out col_map.values() as we need to put columns back in order
        df = df.drop_duplicates()
        df = df.sort_values(by=df.columns[0], ascending=True)  # arbitrary sort on column 0 (Sample name)
        for i, col in enumerate(df.columns):
            if col_map[col] in {'Characteristics[Material Type]', 'Characteristics[material type]'}:
                cols[i] = 'Material Type'
            else:
                cols[i] = col_map[col]
        df.columns = cols  # reset column headers
        import numpy as np
        df = df.replace('', np.nan)
        df = df.dropna(axis=1, how='all')
        df = df.sort_values(by=df.columns[0], ascending=True)  # arbitrary sort on column 0
        df.to_csv(path_or_buf=os.path.join(output_dir, study_obj.filename), mode='w', index=False, sep=str('\t'), encoding='utf-8',)


def read_investigation_file(fp):

    def _peek(f):
        position = f.tell()
        l = f.readline()
        f.seek(position)

        if isinstance(l, six.binary_type):
            l = l.decode("utf-8")

        return l

    def _read_tab_section(f, sec_key, next_sec_key=None):

        line = f.readline()
        if isinstance(line, six.binary_type):
            line = line.decode("utf-8")

        normed_line = line.rstrip().strip('"')

        if not normed_line == sec_key:
            raise IOError("Expected: " + sec_key + " section, but got: " + normed_line)
        memf = six.StringIO()
        while not _peek(f=f).rstrip() == next_sec_key:

            line = f.readline()
            if isinstance(line, six.binary_type):
                line = line.decode("utf-8")

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

    df_dict = {}

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


def check_utf8(fp):
    """Used for rule 0010"""
    import chardet
    with open(fp.name, 'rb') as binary_fp:
        charset = chardet.detect(binary_fp.read())
    if charset['encoding'] not in {'UTF-8', 'ascii'}:
        warnings.append({
            "message": "File should be UTF8 encoding",
            "supplemental": "Encoding is '{0}' with confidence {1}".format(charset['encoding'], charset['confidence']),
            "code": 10
        })
        logger.warning("File should be UTF-8 encoding but found it is '{0}' encoding with {1} confidence"
                       .format(charset['encoding'], charset['confidence']))
        raise SystemError()


def load2(fp):
    """Used for rules 0005"""
    def _read_investigation_file(fp):

        def _peek(f):
            position = f.tell()
            try:
                l = _strip_label(f.readline())
            except IndexError:
                l = None
            finally:
                f.seek(position)

            #try:
            if isinstance(l, six.binary_type):
                l = l.decode('utf-8')

            return l
            # except AttributeError:
            #     return l
            # except UnicodeEncodeError:
            #     return l.encode("utf-8").decode("utf-8")

        def _strip_label(s):
            if isinstance(s, six.binary_type):
                s = s.decode('utf-8')

            return s.rstrip().strip('"')
            #try:
            #    return s.decode('utf-8').rstrip().strip('"')
            #except AttributeError:
            #    return s.rstrip().strip('"')

        def _read_tab_section(f, sec_key, next_sec_key=None):

            line = _strip_label(f.readline())

            if isinstance(line, six.binary_type):
                line = line.decode('utf-8')

            if not line == sec_key:
                raise IOError("Expected: " + sec_key + " section, but got: " + line)
            memf = six.StringIO()
            while not _peek(f=f) == next_sec_key:
                line = f.readline()

                if isinstance(line, six.binary_type):
                    line = line.decode('utf-8')

                if not line:
                    break
                memf.write(line.rstrip() + '\n')

            memf.seek(0)
            return memf

        def _build_section_df(f):
            import numpy as np
            df = pd.read_csv(f, sep='\t', error_bad_lines=False).T  # Load and transpose ISA file section
            df.replace(np.nan, '', regex=True, inplace=True)  # Strip out the nan entries
            df.reset_index(inplace=True)  # Reset index so it is accessible as column
            df.columns = df.iloc[0]  # If all was OK, promote this row to the column headers
            df = df.reindex(df.index.drop(0))  # Reindex the DataFrame
            return df

        df_dict = {}

        def check_labels(section, labels_expected, df):
            labels_found = set(df.columns)
            comment_regex = re.compile('Comment\[(.*?)\]')
            if not labels_expected.issubset(labels_found):
                missing_labels = labels_expected - labels_found
                logger.fatal("(F) In {} section, expected labels {} not found in {}"
                             .format(section, missing_labels, labels_found))
            if labels_found - labels_expected:
                # check extra labels, i.e. make sure they're all comments
                extra_labels = labels_found - labels_expected
                for label in extra_labels:
                    if comment_regex.match(label) is None:
                        logger.fatal("(F) In {} section, label {} is not allowed".format(section, label))

        # Read in investigation file into DataFrames first
        logger.info("Loading ONTOLOGY SOURCE REFERENCE section")
        df_dict['ONTOLOGY SOURCE REFERENCE'] = _build_section_df(_read_tab_section(
            f=fp,
            sec_key='ONTOLOGY SOURCE REFERENCE',
            next_sec_key='INVESTIGATION'
        ))
        labels_expected = {'Term Source Name', 'Term Source File', 'Term Source Version', 'Term Source Description'}
        check_labels('ONTOLOGY SOURCE REFERENCE', labels_expected, df_dict['ONTOLOGY SOURCE REFERENCE'])
        logger.info("Loading INVESTIGATION section")
        df_dict['INVESTIGATION'] = _build_section_df(_read_tab_section(
            f=fp,
            sec_key='INVESTIGATION',
            next_sec_key='INVESTIGATION PUBLICATIONS'
        ))
        labels_expected = {'Investigation Identifier', 'Investigation Title', 'Investigation Description',
                           'Investigation Submission Date', 'Investigation Public Release Date'}
        check_labels('INVESTIGATION', labels_expected, df_dict['INVESTIGATION'])
        logger.info("Loading INVESTIGATION PUBLICATIONS section")
        df_dict['INVESTIGATION PUBLICATIONS'] = _build_section_df(_read_tab_section(
            f=fp,
            sec_key='INVESTIGATION PUBLICATIONS',
            next_sec_key='INVESTIGATION CONTACTS'
        ))
        labels_expected = {'Investigation PubMed ID', 'Investigation Publication DOI',
                           'Investigation Publication Author List', 'Investigation Publication Title',
                           'Investigation Publication Status', 'Investigation Publication Status Term Accession Number',
                           'Investigation Publication Status Term Source REF'}
        check_labels('INVESTIGATION PUBLICATIONS', labels_expected, df_dict['INVESTIGATION PUBLICATIONS'])
        logger.info("Loading INVESTIGATION CONTACTS section")
        df_dict['INVESTIGATION CONTACTS'] = _build_section_df(_read_tab_section(
            f=fp,
            sec_key='INVESTIGATION CONTACTS',
            next_sec_key='STUDY'
        ))
        labels_expected = {'Investigation Person Last Name', 'Investigation Person First Name',
                           'Investigation Person Mid Initials', 'Investigation Person Email',
                           'Investigation Person Phone', 'Investigation Person Fax',
                           'Investigation Person Address', 'Investigation Person Affiliation',
                           'Investigation Person Roles', 'Investigation Person Roles',
                           'Investigation Person Roles Term Accession Number',
                           'Investigation Person Roles Term Source REF'}
        check_labels('INVESTIGATION CONTACTS', labels_expected, df_dict['INVESTIGATION CONTACTS'])

        df_dict['STUDY'] = list()
        df_dict['STUDY DESIGN DESCRIPTORS'] = list()
        df_dict['STUDY PUBLICATIONS'] = list()
        df_dict['STUDY FACTORS'] = list()
        df_dict['STUDY ASSAYS'] = list()
        df_dict['STUDY PROTOCOLS'] = list()
        df_dict['STUDY CONTACTS'] = list()
        while _peek(fp):  # Iterate through STUDY blocks until end of file
            logger.info("Loading STUDY section")
            df_dict['STUDY'].append(_build_section_df(_read_tab_section(
                f=fp,
                sec_key='STUDY',
                next_sec_key='STUDY DESIGN DESCRIPTORS'
            )))
            labels_expected = {'Study Identifier', 'Study Title', 'Study Description',
                               'Study Submission Date', 'Study Public Release Date',
                               'Study File Name'}
            check_labels('STUDY', labels_expected, df_dict['STUDY'][-1])
            logger.info("Loading STUDY DESIGN DESCRIPTORS section")
            df_dict['STUDY DESIGN DESCRIPTORS'] .append(_build_section_df(_read_tab_section(
                f=fp,
                sec_key='STUDY DESIGN DESCRIPTORS',
                next_sec_key='STUDY PUBLICATIONS'
            )))
            labels_expected = {'Study Design Type', 'Study Design Type Term Accession Number',
                               'Study Design Type Term Source REF'}
            check_labels('STUDY DESIGN DESCRIPTORS', labels_expected,
                         df_dict['STUDY DESIGN DESCRIPTORS'][-1])
            logger.info("Loading STUDY PUBLICATIONS section")
            df_dict['STUDY PUBLICATIONS'].append(_build_section_df(_read_tab_section(
                f=fp,
                sec_key='STUDY PUBLICATIONS',
                next_sec_key='STUDY FACTORS'
            )))
            labels_expected = {'Study PubMed ID', 'Study Publication DOI',
                               'Study Publication Author List', 'Study Publication Title',
                               'Study Publication Status',
                               'Study Publication Status Term Accession Number',
                               'Study Publication Status Term Source REF'}
            check_labels('STUDY PUBLICATIONS', labels_expected,
                         df_dict['STUDY PUBLICATIONS'][-1])
            logger.info("Loading STUDY FACTORS section")
            df_dict['STUDY FACTORS'].append(_build_section_df(_read_tab_section(
                f=fp,
                sec_key='STUDY FACTORS',
                next_sec_key='STUDY ASSAYS'
            )))
            labels_expected = {'Study Factor Name', 'Study Factor Type', 'Study Factor Type Term Accession Number',
                               'Study Factor Type Term Source REF'}
            check_labels('STUDY FACTORS', labels_expected, df_dict['STUDY FACTORS'][-1])
            logger.info("Loading STUDY ASSAYS section")
            df_dict['STUDY ASSAYS'].append(_build_section_df(_read_tab_section(
                f=fp,
                sec_key='STUDY ASSAYS',
                next_sec_key='STUDY PROTOCOLS'
            )))
            labels_expected = {'Study Assay Measurement Type', 'Study Assay Measurement Type Term Accession Number',
                               'Study Assay Measurement Type Term Source REF', 'Study Assay Technology Type',
                               'Study Assay Technology Type Term Accession Number',
                               'Study Assay Technology Type Term Source REF', 'Study Assay Technology Platform',
                               'Study Assay File Name'}
            check_labels('STUDY ASSAYS', labels_expected, df_dict['STUDY ASSAYS'][-1])
            logger.info("Loading STUDY PROTOCOLS section")
            df_dict['STUDY PROTOCOLS'].append(_build_section_df(_read_tab_section(
                f=fp,
                sec_key='STUDY PROTOCOLS',
                next_sec_key='STUDY CONTACTS'
            )))
            labels_expected = {'Study Protocol Name', 'Study Protocol Type',
                               'Study Protocol Type Term Accession Number', 'Study Protocol Type Term Source REF',
                               'Study Protocol Description', 'Study Protocol URI', 'Study Protocol Version',
                               'Study Protocol Parameters Name', 'Study Protocol Parameters Name Term Accession Number',
                               'Study Protocol Parameters Name Term Source REF', 'Study Protocol Components Name',
                               'Study Protocol Components Type', 'Study Protocol Components Type Term Accession Number',
                               'Study Protocol Components Type Term Source REF'}
            check_labels('STUDY PROTOCOLS', labels_expected, df_dict['STUDY PROTOCOLS'][-1])
            logger.info("Loading STUDY CONTACTS section")
            df_dict['STUDY CONTACTS'].append(_build_section_df(_read_tab_section(
                f=fp,
                sec_key='STUDY CONTACTS',
                next_sec_key='STUDY'
            )))
            labels_expected = {'Study Person Last Name', 'Study Person First Name',
                               'Study Person Mid Initials', 'Study Person Email',
                               'Study Person Phone', 'Study Person Fax',
                               'Study Person Address', 'Study Person Affiliation',
                               'Study Person Roles', 'Study Person Roles',
                               'Study Person Roles Term Accession Number',
                               'Study Person Roles Term Source REF'}
            check_labels('STUDY CONTACTS', labels_expected,
                         df_dict['STUDY CONTACTS'][-1])

        return df_dict

    i_dfs = _read_investigation_file(fp)
    return i_dfs


def check_filenames_present(i_df):
    """Used for rule 3005"""
    for s_pos, study_df in enumerate(i_df['STUDY']):
        if not study_df.iloc[0]['Study File Name']:
            warnings.append({
                "message": "Missing study file name",
                "supplemental": "STUDY.{}".format(s_pos),
                "code": 3005
            })
            logger.warning("(W) A study filename is missing for STUDY.{}".format(s_pos))
        for a_pos, filename in enumerate(i_df['STUDY ASSAYS'][s_pos]['Study Assay File Name'].tolist()):
            if not filename:
                warnings.append({
                    "message": "Missing assay file name",
                    "supplemental": "STUDY.{}, STUDY ASSAY.{}".format(s_pos, a_pos),
                    "code": 3005
                })
                logger.warning("(W) An assay filename is missing for STUDY ASSAY.{}".format(a_pos))


def check_date_formats(i_df):
    """Used for rule 3001"""
    def check_iso8601_date(date_str):
        if date_str:
            try:
                iso8601.parse_date(date_str)
            except iso8601.ParseError:
                warnings.append({
                    "message": "Date is not ISO8601 formatted",
                    "supplemental": "Found {} in date field".format(date_str),
                    "code": 3001
                })
                logger.warning("(W) Date {} does not conform to ISO8601 format".format(date_str))

    try: check_iso8601_date(i_df['INVESTIGATION']['Investigation Public Release Date'].tolist()[0])
    except IndexError: pass

    try: check_iso8601_date(i_df['INVESTIGATION']['Investigation Submission Date'].tolist()[0])
    except IndexError: pass

    for i, study_df in enumerate(i_df['STUDY']):
        try: check_iso8601_date(study_df['Study Public Release Date'].tolist()[0])
        except IndexError: pass

        try: check_iso8601_date(study_df['Study Submission Date'].tolist()[0])
        except IndexError: pass

        # for process in study['processSequence']:
        #     check_iso8601_date(process['date'])


def check_dois(i_df):
    """Used for rule 3002"""
    def check_doi(doi_str):
        if doi_str:
            regexDOI = re.compile('(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![%"#? ])\\S)+)')
            if not regexDOI.match(doi_str):
                warnings.append({
                    "message": "DOI is not valid format",
                    "supplemental": "Found {} in DOI field".format(doi_str),
                    "code": 3002
                })
                logger.warning("(W) DOI {} does not conform to DOI format".format(doi_str))
    import re
    for doi in i_df['INVESTIGATION PUBLICATIONS']['Investigation Publication DOI'].tolist():
        check_doi(doi)
    for i, study_df in enumerate(i_df['STUDY PUBLICATIONS']):
        for doi in study_df['Study Publication DOI'].tolist():
            check_doi(doi)


def check_pubmed_ids_format(i_df):
    """Used for rule 3003"""
    def check_pubmed_id(pubmed_id_str):
        if pubmed_id_str:
            pmid_regex = re.compile('[0-9]{8}')
            pmcid_regex = re.compile('PMC[0-9]{8}')
            if pmid_regex.match(pubmed_id_str) is None and pmcid_regex.match(pubmed_id_str) is None:
                warnings.append({
                    "message": "PubMed ID is not valid format",
                    "supplemental": "Found PubMedID {}".format(pubmed_id_str),
                    "code": 3003
                })
                logger.warning("(W) PubMed ID {} is not valid format".format(pubmed_id_str))
    import re
    for doi in i_df['INVESTIGATION PUBLICATIONS']['Investigation PubMed ID'].tolist():
        check_pubmed_id(doi)
    for study_pubs_df in i_df['STUDY PUBLICATIONS']:
        for doi in study_pubs_df['Study PubMed ID'].tolist():
            check_pubmed_id(doi)


def check_protocol_names(i_df):
    """Used for rule 1010"""
    for study_protocols_df in i_df['STUDY PROTOCOLS']:
        for i, protocol_name in enumerate(study_protocols_df['Study Protocol Name'].tolist()):
            if not protocol_name or 'Unnamed: ' in protocol_name:  #  DataFrames labels empty cells as 'Unnamed: n'
                warnings.append({
                    "message": "Protocol missing name",
                    "supplemental": "pos={}".format(i),
                    "code": 1010
                })
                logger.warning("(W) A Protocol at position {} is missing Protocol Name, so can't be referenced in "
                               "ISA-tab".format(i))

def check_protocol_parameter_names(i_df):
    """Used for rule 1011"""
    for study_protocols_df in i_df['STUDY PROTOCOLS']:
        for i, protocol_parameters_names in enumerate(study_protocols_df['Study Protocol Parameters Name'].tolist()):
            if len(protocol_parameters_names.split(';')) > 1:  # There's an empty cell if no protocols
                for protocol_parameter_name in protocol_parameters_names.split(';'):
                    if not protocol_parameter_name or 'Unnamed: ' in protocol_parameter_name:  # DataFrames labels empty cells as 'Unnamed: n'
                        warnings.append({
                            "message": "Protocol Parameter missing name",
                            "supplemental": "Protocol Parameter at pos={}".format(i),
                            "code": 1011
                        })
                        logger.warning(
                            "(W) A Protocol Parameter used in Protocol position {} is missing a Name, so can't be referenced in ISA-tab".format(i))

def check_study_factor_names(i_df):
    """Used for rule 1012"""
    for study_protocols_df in i_df['STUDY FACTORS']:
        for i, protocol_name in enumerate(study_protocols_df['Study Factor Name'].tolist()):
            if not protocol_name or 'Unnamed: ' in protocol_name:  #  DataFrames labels empty cells as 'Unnamed: n'
                warnings.append({
                    "message": "Study Factor missing name",
                    "supplemental": "Study Factor pos={}".format(i),
                    "code": 1012
                })
                logger.warning("(W) A Study Factor at position {} is missing a name, so can't be referenced in ISA-tab".format(i))


def check_ontology_sources(i_df):
    """Used for rule 3008"""
    for i, ontology_source_name in enumerate(i_df['ONTOLOGY SOURCE REFERENCE']['Term Source Name'].tolist()):
        if not ontology_source_name or 'Unnamed: ' in ontology_source_name:
            warnings.append({
                "message": "Ontology Source missing name ref",
                "supplemental": "pos={}".format(i),
                "code": 3008
            })
            logger.warning("(W) An Ontology Source Reference at position {} is missing Term Source Name, so can't be "
                           "referenced".format(i))


def check_table_files_read(i_df, dir_context):
    """Used for rules 0006 and 0008"""
    for i, study_df in enumerate(i_df['STUDY']):
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename and not os.path.exists(os.path.join(dir_context, study_filename)):
            errors.append({
                    "message": "Missing study tab file(s)",
                    "supplemental": "Study File {} does not appear to exist".format(study_filename),
                    "code": 6
            })
            logger.error("(E) Study File {} does not appear to exist".format(study_filename))
        # if study_filename:
        #     try:
        #         open(os.path.join(dir_context, study_filename)).close()
        #     except IOError:
        #         logger.error("(E) Study File {} does not appear to exist".format(study_filename))
        for j, assay_filename in enumerate(i_df['STUDY ASSAYS'][i]['Study Assay File Name'].tolist()):
            if assay_filename and not os.path.exists(os.path.join(dir_context, assay_filename)):
                errors.append({
                        "message": "Missing assay tab file(s)",
                        "supplemental": "Assay File {} does not appear to exist".format(assay_filename),
                        "code": 8
                })
                logger.error("(E) Assay File {} does not appear to exist".format(assay_filename))
            # if assay_filename:
            #     try:
            #         open(os.path.join(dir_context, assay_filename)).close()
            #     except IOError:
            #         logger.error("(E) Assay File {} does not appear to exist".format(assay_filename))



def check_table_files_load(i_df, dir_context):
    """Used for rules 0007 and 0009"""
    for i, study_df in enumerate(i_df['STUDY']):
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename:
            try:
                # with open(os.path.join(dir_context, study_filename)) as fp:
                #     load_table_checks(fp)
                load_table_checks(os.path.join(dir_context, study_filename))
            except IOError:
                pass
        for j, assay_filename in enumerate(i_df['STUDY ASSAYS'][i]['Study Assay File Name'].tolist()):
            if assay_filename:
                try:
                    # with open(os.path.join(dir_context, assay_filename)) as fp:
                    #     load_table_checks(fp)
                    load_table_checks(os.path.join(dir_context, assay_filename))
                except IOError:
                    pass


def check_samples_not_declared_in_study_used_in_assay(i_df, dir_context):
    for i, study_df in enumerate(i_df['STUDY']):
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename:
            try:
                study_df = load_table(os.path.join(dir_context, study_filename))
                study_samples = set(study_df['Sample Name'])
            except IOError:
                pass
        for j, assay_filename in enumerate(i_df['STUDY ASSAYS'][i]['Study Assay File Name'].tolist()):
            if assay_filename:
                try:
                    assay_df = load_table(os.path.join(dir_context, assay_filename))
                    assay_samples = set(assay_df['Sample Name'])
                    if not assay_samples.issubset(study_samples):
                        logger.error("(E) Some samples in an assay file {} are not declared in the study file {}: {}".format(assay_filename, study_filename, list(assay_samples - study_samples)))
                except IOError:
                    pass


def check_protocol_usage(i_df, dir_context):
    """Used for rules 1007 and 1019"""
    for i, study_df in enumerate(i_df['STUDY']):
        protocols_declared = set(i_df['STUDY PROTOCOLS'][i]['Study Protocol Name'].tolist())
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename:
            try:
                protocol_refs_used = set()
                study_df = load_table(os.path.join(dir_context, study_filename))
                for protocol_ref_col in (k for k in study_df.columns if k.startswith('Protocol REF')):
                    protocol_refs_used = protocol_refs_used.union(study_df[protocol_ref_col])
                protocol_refs_used = {r for r in protocol_refs_used if pd.notnull(r)}
                if not protocol_refs_used.issubset(protocols_declared):
                    errors.append({
                        "message": "Missing Protocol declaration",
                        "supplemental": "protocols in study file {} are not declared in the investigation file: "
                                        "{}".format(study_filename, diff),
                        "code": 1007
                    })
                    logger.error(
                        "(E) Some protocols used in a study file {} are not declared in the investigation file: {}".format(
                            study_filename, list(protocol_refs_used - protocols_declared)))
            except IOError:
                pass
        for j, assay_filename in enumerate(i_df['STUDY ASSAYS'][i]['Study Assay File Name'].tolist()):
            if assay_filename:
                try:
                    protocol_refs_used = set()
                    assay_df = load_table(os.path.join(dir_context, assay_filename))
                    for protocol_ref_col in (k for k in assay_df.columns if k.startswith('Protocol REF')):
                        protocol_refs_used = protocol_refs_used.union(assay_df[protocol_ref_col])
                    protocol_refs_used = {r for r in protocol_refs_used if pd.notnull(r)}
                    if not protocol_refs_used.issubset(protocols_declared):
                        errors.append({
                            "message": "Missing Protocol declaration",
                            "supplemental": "protocols in study file {} are not declared in the investigation file: "
                                            "{}".format(study_filename, diff),
                            "code": 1007
                        })
                        logger.error(
                            "(E) Some protocols used in an assay file {} are not declared in the investigation file: {}".format(
                                assay_filename, list(protocol_refs_used - protocols_declared)))
                except IOError:
                    pass
        # now collect all protocols in all assays to compare to declared protocols
        protocol_refs_used = set()
        if study_filename:
            try:
                study_df = load_table(os.path.join(dir_context, study_filename))
                for protocol_ref_col in (k for k in study_df.columns if k.startswith('Protocol REF')):
                    protocol_refs_used = protocol_refs_used.union(study_df[protocol_ref_col])
            except IOError:
                pass
        for j, assay_filename in enumerate(i_df['STUDY ASSAYS'][i]['Study Assay File Name'].tolist()):
            if assay_filename:
                try:
                    assay_df = load_table(os.path.join(dir_context, assay_filename))
                    for protocol_ref_col in (k for k in assay_df.columns if k.startswith('Protocol REF')):
                        protocol_refs_used = protocol_refs_used.union(assay_df[protocol_ref_col])
                except IOError:
                    pass
        diff = protocols_declared - protocol_refs_used
        if diff:
            warnings.append({
                "message": "Protocol declared but not used",
                "supplemental": "protocols declared in the file {} are not used in any assay file: "
                                "{}".format(study_filename, diff),
                "code": 1019
            })
            logger.warning(
                "(W) Some protocols declared in the investigation file {} are not used in any assay file: {}".format(
                    study_filename, list(diff)))

def load_table(fp):
    try:
        df = pd.read_csv(fp, sep='\t', encoding='utf-8')
    except UnicodeDecodeError:
        logger.warning("Could not load file with UTF-8, trying ISO-8859-1")
        df = pd.read_csv(fp, sep='\t', encoding='latin1')
    return df


def load_table_checks(f):
    characteristics_regex = re.compile('Characteristics\[(.*?)\]')
    parameter_value_regex = re.compile('Parameter Value\[(.*?)\]')
    factor_value_regex = re.compile('Factor Value\[(.*?)\]')
    comment_regex = re.compile('Comment\[(.*?)\]')
    indexed_col_regex = re.compile('(.*?)\.\d+')
    df = load_table(f)
    columns = df.columns
    for x, column in enumerate(columns):  # check if columns have valid labels
        if indexed_col_regex.match(column):
            column = column[:column.rfind('.')]
        if (column not in {'Source Name', 'Sample Name', 'Term Source REF', 'Protocol REF', 'Term Accession Number',
                           'Unit', 'Assay Name', 'Extract Name', 'Raw Data File', 'Material Type', 'MS Assay Name',
                           'Raw Spectral Data File', 'Labeled Extract Name', 'Label', 'Hybridization Assay Name',
                           'Array Design REF', 'Scan Name', 'Array Data File', 'Protein Assignment File',
                           'Peptide Assignment File', 'Post Translational Modification Assignment File',
                           'Data Transformation Name', 'Derived Spectral Data File', 'Normalization Name',
                           'Derived Array Data File', 'Image File'}) and not characteristics_regex.match(column) and not parameter_value_regex.match(column) and not factor_value_regex.match(column) and not comment_regex.match(column):
            logger.error("Unrecognised column heading {} at column position {} in table file {}".format(column, x, os.path.basename(fp.name)))
    norm_columns = list()
    for x, column in enumerate(columns):
        if indexed_col_regex.match(column):
            norm_columns.append(column[:column.rfind('.')])
        else:
            norm_columns.append(column)
    object_index = (k for k, x in enumerate(norm_columns) if x in {'Source Name', 'Sample Name', 'Protocol REF',
                                                              'Extract Name', 'Labeled Extract Name', 'Raw Data File',
                                                              'Raw Spectral Data File', 'Array Data File',
                                                              'Protein Assignment File', 'Peptide Assignment File',
                                                              'Post Translational Modification Assignment File',
                                                              'Derived Spectral Data File', 'Derived Array Data File'}
                    or factor_value_regex.match(x))
    # this bit strips out the postfix .n that DataFrames adds to multiples of column labels
    object_columns_list = list()
    prev_i = next(object_index) # this will also automatically skip first one
    for curr_i in object_index:  # collect each object's columns
        if prev_i == curr_i: pass  # skip if there's no diff, i.e. first one
        else: object_columns_list.append(norm_columns[prev_i:curr_i])
        prev_i = curr_i
    object_columns_list.append(norm_columns[prev_i:])  # finally collect last object's columns

    for object_columns in object_columns_list:
        prop_name = object_columns[0]
        if prop_name in {'Sample Name', 'Source Name'}:
            for x, col in enumerate(object_columns[1:]):
                if col not in {'Term Source REF', 'Term Accession Number', 'Unit'} and not characteristics_regex.match(col) and not factor_value_regex.match(col) and not comment_regex.match(col):
                    logger.error("(E) Expected only Characteristics, Factor Values or Comments following {} columns but found {} at offset {}".format(prop_name, col, x+1))
        elif prop_name == 'Protocol REF':
            for x, col in enumerate(object_columns[1:]):
                if col not in {'Term Source REF', 'Term Accession Number', 'Unit', 'Assay Name',
                               'Hybridization Assay Name', 'Array Design REF', 'Scan Name'} and not parameter_value_regex.match(col) and not comment_regex.match(col):
                    logger.error("(E) Unexpected column heading following {} column. Found {} at offset {}".format(prop_name, col, x+1))
        elif prop_name == 'Extract Name':
            if len(object_columns) > 1:
                logger.error(
                    "Unexpected column heading(s) following {} column. Found {} at offset {}".format(prop_name, object_columns[1:], 2))
        elif prop_name == 'Labeled Extract Name':
            if len(object_columns) > 1:
                if object_columns[1] == 'Label':
                    for x, col in enumerate(object_columns[2:]):
                        if col not in {'Term Source REF', 'Term Accession Number'}:
                            logger.error("(E) Unexpected column heading following {} column. Found {} at offset {}".format(prop_name, col, x+1))
                else:
                    logger.error("(E) Unexpected column heading following {} column. Found {} at offset {}".format(prop_name, object_columns[1:], 2))
            else:
                logger.error("Expected Label column after Labeled Extract Name but none found")
        elif prop_name in {'Raw Data File', 'Derived Spectral Data File', 'Derived Array Data File', 'Array Data File',
                           'Raw Spectral Data File', 'Protein Assignment File', 'Peptide Assignment File',
                           'Post Translational Modification Assignment File'}:
            for x, col in enumerate(object_columns[1:]):
                if not comment_regex.match(col):
                    logger.error("(E) Expected only Comments following {} columns but found {} at offset {}".format(prop_name, col, x+1))
        elif factor_value_regex.match(prop_name):
            for x, col in enumerate(object_columns[2:]):
                if col not in {'Term Source REF', 'Term Accession Number'}:
                    logger.error(
                        "(E) Unexpected column heading following {} column. Found {} at offset {}".format(prop_name,
                                                                                                      col, x + 1))
        else:
            logger.info("Need to implement a rule for... " + prop_name)
            logger.info(object_columns)
    return df


def check_study_factor_usage(i_df, dir_context):
    """Used for rules 1008 and 1021"""
    factor_value_regex = re.compile('Factor Value\[(.*?)\]')
    for i, study_df in enumerate(i_df['STUDY']):
        study_factors_declared = set(i_df['STUDY FACTORS'][i]['Study Factor Name'].tolist())
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename:
            try:
                study_factors_used = set()
                study_df = load_table(os.path.join(dir_context, study_filename))
                study_factor_ref_cols = (k for k in study_df.columns if factor_value_regex.match(k))
                for col in study_factor_ref_cols:
                    fv = factor_value_regex.findall(col)
                    study_factors_used = study_factors_used.union(set(fv))
                if not study_factors_used.issubset(study_factors_declared):
                    logger.error(
                        "(E) Some factors used in an study file {} are not declared in the investigation file: {}".format(
                            study_filename, list(study_factors_used - study_factors_declared)))
            except IOError:
                pass
        for j, assay_filename in enumerate(i_df['STUDY ASSAYS'][i]['Study Assay File Name'].tolist()):
            if assay_filename:
                try:
                    study_factors_used = set()
                    assay_df = load_table(os.path.join(dir_context, assay_filename))
                    study_factor_ref_cols = {k for k in assay_df.columns if factor_value_regex.match(k)}
                    for col in study_factor_ref_cols:
                        fv = factor_value_regex.findall(col)
                        study_factors_used = study_factors_used.union(set(fv))
                    if not study_factors_used.issubset(study_factors_declared):
                        logger.error(
                            "(E) Some factors used in an assay file {} are not declared in the investigation file: {}".format(
                                assay_filename, list(study_factors_used - study_factors_declared)))
                except IOError:
                    pass
        study_factors_used = set()
        if study_filename:
            try:
                study_df = load_table(os.path.join(dir_context, study_filename))
                study_factor_ref_cols = (k for k in study_df.columns if factor_value_regex.match(k))
                for col in study_factor_ref_cols:
                    fv = factor_value_regex.findall(col)
                    study_factors_used = study_factors_used.union(set(fv))
            except IOError:
                pass
        for j, assay_filename in enumerate(i_df['STUDY ASSAYS'][i]['Study Assay File Name'].tolist()):
            if assay_filename:
                try:
                    study_df = load_table(os.path.join(dir_context, assay_filename))
                    study_factor_ref_cols = (k for k in assay_df.columns if factor_value_regex.match(k))
                    for col in study_factor_ref_cols:
                        fv = factor_value_regex.findall(col)
                        study_factors_used = study_factors_used.union(set(fv))
                except IOError:
                    pass
        if study_factors_declared - study_factors_used:
            logger.warning(
                "(W) Some study factors declared in the investigation file are not used in any assay file: {}".format(
                    list(study_factors_declared - study_factors_used)))


def check_protocol_parameter_usage(i_df, dir_context):
    """Used for rules 1009 and 1020"""
    parameter_value_regex = re.compile('Parameter Value\[(.*?)\]')
    for i, study_df in enumerate(i_df['STUDY']):
        protocol_parameters_declared = set()
        protocol_parameters_per_protocol = set(i_df['STUDY PROTOCOLS'][i]['Study Protocol Parameters Name'].tolist())
        for protocol_parameters in protocol_parameters_per_protocol:
            parameters_list = protocol_parameters.split(';')
            protocol_parameters_declared = protocol_parameters_declared.union(set(parameters_list))
        protocol_parameters_declared = protocol_parameters_declared - {''}  # empty string is not a valid protocol parameter
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename:
            try:
                protocol_parameters_used = set()
                study_df = load_table(os.path.join(dir_context, study_filename))
                parameter_value_cols = (k for k in study_df.columns if parameter_value_regex.match(k))
                for col in parameter_value_cols:
                    pv = parameter_value_regex.findall(col)
                    protocol_parameters_used = protocol_parameters_used.union(set(pv))
                if not protocol_parameters_used.issubset(protocol_parameters_declared):
                    logger.error(
                        "(E) Some protocol parameters referenced in an study file {} are not declared in the investigation file: {}".format(
                            study_filename, list(protocol_parameters_used - protocol_parameters_declared)))
            except IOError:
                pass
        for j, assay_filename in enumerate(i_df['STUDY ASSAYS'][i]['Study Assay File Name'].tolist()):
            if assay_filename:
                try:
                    protocol_parameters_used = set()
                    assay_df = load_table(os.path.join(dir_context, assay_filename))
                    parameter_value_cols = (k for k in assay_df.columns if parameter_value_regex.match(k))
                    for col in parameter_value_cols:
                        pv = parameter_value_regex.findall(col)
                        protocol_parameters_used = protocol_parameters_used.union(set(pv))
                    if not protocol_parameters_used.issubset(protocol_parameters_declared):
                        logger.error(
                            "(E) Some protocol parameters referenced in an assay file {} are not declared in the investigation file: {}".format(
                                assay_filename, list(protocol_parameters_used - protocol_parameters_declared)))
                except IOError:
                    pass
        # now collect all protocol parameters in all assays to compare to declared protocol parameters
        protocol_parameters_used = set()
        if study_filename:
            try:
                study_df = load_table(os.path.join(dir_context, study_filename))
                parameter_value_cols = (k for k in study_df.columns if parameter_value_regex.match(k))
                for col in parameter_value_cols:
                    pv = parameter_value_regex.findall(col)
                    protocol_parameters_used = protocol_parameters_used.union(set(pv))
            except IOError:
                pass
        for j, assay_filename in enumerate(i_df['STUDY ASSAYS'][i]['Study Assay File Name'].tolist()):
            if assay_filename:
                try:
                    assay_df = load_table(os.path.join(dir_context, assay_filename))
                    parameter_value_cols = (k for k in assay_df.columns if parameter_value_regex.match(k))
                    for col in parameter_value_cols:
                        pv = parameter_value_regex.findall(col)
                        protocol_parameters_used = protocol_parameters_used.union(set(pv))
                except IOError:
                    pass
        if protocol_parameters_declared - protocol_parameters_used:
            logger.warning(
                "(W) Some protocol parameters declared in the investigation file are not used in any assay file: {}".format(
                    list(protocol_parameters_declared - protocol_parameters_used)))


def get_ontology_source_refs(i_df):
    return i_df['ONTOLOGY SOURCE REFERENCE']['Term Source Name'].tolist()


def check_term_source_refs_in_investigation(i_df):
    """Used for rules 3007 and 3009"""
    ontology_sources_list = get_ontology_source_refs(i_df)

    def check_study_term_sources_in_secton_field(section_label, pos, column_label):
        section_term_source_refs = (k for k in i_df[section_label][pos][column_label].tolist() if k)
        # this for loop deals with semicolon separated lists of term source refs
        section_term_source_refs_to_remove = list()
        for section_term_source_ref in section_term_source_refs:
            if ';' in section_term_source_ref:
                term_sources = [k for k in section_term_source_ref.split(';') if k]
                section_term_source_refs_to_remove.append(section_term_source_ref)
                section_term_source_refs.extend(term_sources)
        for section_term_source_ref_to_remove in section_term_source_refs_to_remove:
            section_term_source_refs.remove(section_term_source_ref_to_remove)
        if not set(section_term_source_refs).issubset(ontology_sources_list):
            warnings.append({
                "message": "Missing Term Source",
                "supplemental": "Ontology sources missing {}".format(list(set(ontology_sources_list) - set(section_term_source_refs))),
                "code": 3009
            })
            logger.warning("(W) In {} one or more of {} has not been declared in {}.{} section".format(column_label,
                                                                                                section_term_source_refs,
                                                                                                section_label, pos))

    i_publication_status_term_source_ref = [k for k in i_df['INVESTIGATION PUBLICATIONS']['Investigation Publication Status Term Source REF'].tolist() if k]
    if not set(i_publication_status_term_source_ref).issubset(ontology_sources_list):
        warnings.append({
            "message": "Missing Term Source",
            "supplemental": "Ontology sources missing {}".format(list(set(i_publication_status_term_source_ref) - set(ontology_sources_list))),
            "code": 3009
        })
        logger.warning("(W) Investigation Publication Status Term Source REF {} has not been declared in ONTOLOGY SOURCE REFERENCE section".format(i_publication_status_term_source_ref))
    i_person_roles_term_source_ref = [k for k in i_df['INVESTIGATION CONTACTS']['Investigation Person Roles Term Source REF'].tolist() if k]
    diff = set(i_person_roles_term_source_ref) - set(ontology_sources_list)
    if diff:
        warnings.append({
            "message": "Missing Term Source",
            "supplemental": "Ontology sources missing {}".format(list(diff)),
            "code": 3009
        })
        logger.warning("(W) Investigation Person Roles Term Source REF {} has not been declared in ONTOLOGY SOURCE "
                    "REFERENCE section".format(i_person_roles_term_source_ref))
    for i, study_df in enumerate(i_df['STUDY']):
        check_study_term_sources_in_secton_field('STUDY DESIGN DESCRIPTORS', i, 'Study Design Type Term Source REF')
        check_study_term_sources_in_secton_field('STUDY PUBLICATIONS', i, 'Study Publication Status Term Source REF')
        check_study_term_sources_in_secton_field('STUDY ASSAYS', i, 'Study Assay Measurement Type Term Source REF')
        check_study_term_sources_in_secton_field('STUDY ASSAYS', i, 'Study Assay Technology Type Term Source REF')
        check_study_term_sources_in_secton_field('STUDY PROTOCOLS', i, 'Study Protocol Type Term Source REF')
        check_study_term_sources_in_secton_field('STUDY PROTOCOLS', i, 'Study Protocol Parameters Name Term Source REF')
        check_study_term_sources_in_secton_field('STUDY PROTOCOLS', i, 'Study Protocol Components Type Term Source REF')
        check_study_term_sources_in_secton_field('STUDY CONTACTS', i, 'Study Person Roles Term Source REF')


def check_term_source_refs_in_assay_tables(i_df, dir_context):
    """Used for rules 3007 and 3009"""
    import math
    ontology_sources_list = set(get_ontology_source_refs(i_df))
    for i, study_df in enumerate(i_df['STUDY']):
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename:
            try:
                df = load_table(os.path.join(dir_context, study_filename))
                columns = df.columns
                object_index = (k for k, x in enumerate(columns) if x.startswith('Term Source REF'))
                prev_i = next(object_index)
                object_columns_list = [columns[prev_i]]
                for curr_i in object_index:  # collect each object's columns
                    if prev_i == curr_i:
                        pass  # skip if there's no diff, i.e. first one
                    else:
                        object_columns_list.append(columns[curr_i])
                    prev_i = curr_i
                for x, col in enumerate(object_columns_list):
                    for y, row in enumerate(df[col]):
                        if row not in ontology_sources_list:
                            if isinstance(row, float):
                                if not math.isnan(row):
                                    warnings.append({
                                        "message": "Missing Term Source",
                                        "supplemental": "Ontology sources missing {} at column position {} and row {} "
                                                        "in {} not declared in ontology "
                                                        "sources {}".format(row+1, object_index[x], y+1, study_filename,
                                                                            list(ontology_sources_list)),
                                        "code": 3009
                                    })
                                    logger.warning("(W) Term Source REF {} at column position {} and row {} in {} not declared in ontology sources {}".format(row+1, object_index[x], y+1, study_filename, list(ontology_sources_list)))
                            else:
                                warnings.append({
                                    "message": "Missing Term Source",
                                    "supplemental": "Ontology sources missing {} at column position {} and row {} "
                                                    "in {} not declared in ontology "
                                                    "sources {}".format(row + 1, object_index[x], y + 1, study_filename,
                                                                        list(ontology_sources_list)),
                                    "code": 3009
                                })
                                logger.warning("(W) Term Source REF {} at column position {} and row {} in {} not in declared ontology sources {}".format(row+1, object_index[x], y+1, study_filename, list(ontology_sources_list)))
            except IOError:
                pass
            for j, assay_filename in enumerate(i_df['STUDY ASSAYS'][i]['Study Assay File Name'].tolist()):
                if assay_filename:
                    try:
                        df = load_table(os.path.join(dir_context, assay_filename))
                        columns = df.columns
                        object_index = (k for k, x in enumerate(columns) if x.startswith('Term Source REF'))
                        prev_i = next(object_index)
                        object_columns_list = [columns[prev_i]]
                        for curr_i in object_index:  # collect each object's columns
                            if prev_i == curr_i:
                                pass  # skip if there's no diff, i.e. first one
                            else:
                                object_columns_list.append(columns[curr_i])
                            prev_i = curr_i
                        for x, col in enumerate(object_columns_list):
                            for y, row in enumerate(df[col]):
                                if row not in ontology_sources_list:
                                    if isinstance(row, float):
                                        if not math.isnan(row):
                                            warnings.append({
                                                "message": "Missing Term Source",
                                                "supplemental": "Ontology sources missing {} at column position {} and "
                                                                "row {} in {} not declared in ontology sources {}"
                                                    .format(row + 1, object_index[x], y + 1, study_filename,
                                                            list(ontology_sources_list)),
                                                "code": 3009
                                            })
                                            logger.warning(
                                                "(W) Term Source REF {} at column position {} and row {} in {} not declared in ontology sources {}".format(
                                                    row+1, object_index[x], y+1, study_filename,
                                                    list(ontology_sources_list)))
                                    else:
                                        warnings.append({
                                            "message": "Missing Term Source",
                                            "supplemental": "Ontology sources missing {} at column position {} and row "
                                                            "{} in {} not declared in ontology sources {}"
                                                .format(row + 1, object_index[x], y + 1, study_filename,
                                                        list(ontology_sources_list)),
                                            "code": 3009
                                        })
                                        logger.warning(
                                            "(W) Term Source REF {} at column position {} and row {} in {} not in declared ontology sources {}".format(
                                                row+1, object_index[x], y+1, study_filename, list(ontology_sources_list)))
                    except IOError:
                        pass


def check_term_source_refs_usage(i_df, dir_context):
    check_term_source_refs_in_investigation(i_df)
    check_term_source_refs_in_assay_tables(i_df, dir_context)


def load_config(config_dir):
    """Rule 4001"""
    from isatools.io import isatab_configurator
    configs = None
    try:
        configs = isatab_configurator.load(config_dir)
    except (IOError, OSError) as e:
        errors.append({
            "message": "Configurations could not be loaded",
            "supplemental": "On loading {}".format(config_dir),
            "code": 4001
        })
        logger.error("(E) {} on trying to load from {}".format(type(e).__name__, config_dir))
    if not configs:
        errors.append({
            "message": "Configurations could not be loaded",
            "supplemental": "On loading {}".format(config_dir),
            "code": 4001
        })
        logger.error("(E) Could not load configurations from {}".format(config_dir))
    else:
        for k in six.iterkeys(configs):
            logger.info("Loaded table configuration '{}' for measurement and technology {}"
                        .format(configs[k].get_isatab_configuration()[0].table_name, k))
    return configs


def check_measurement_technology_types(i_df, configs):
    """Rule 4002"""
    for i, assay_df in enumerate(i_df['STUDY ASSAYS']):
        measurement_types = assay_df['Study Assay Measurement Type'].tolist()
        technology_types = assay_df['Study Assay Technology Type'].tolist()
        if len(measurement_types) == len(technology_types):
            for x, measurement_type in enumerate(measurement_types):
                if (measurement_types[x], technology_types[x]) not in configs:
                    errors.append({
                        "message": "Measurement/technology type invalid",
                        "supplemental": "Measurement {}/technology {}, STUDY ASSAY.{}"
                            .format(measurement_types[x], technology_types[x], i),
                        "code": 4002
                    })
                    logger.error("(E) Could not load configuration for measurement type '{}' and technology type '{}' "
                                 "for STUDY ASSAY.{}'".format(measurement_types[x], technology_types[x], i))


def check_investigation_against_config(i_df, configs):
    import math

    def check_section_against_required_fields_one_value(section, required, i=0):
        fields_required = (k for k in section.columns if k in required)
        for col in fields_required:
            required_values = section[col]
            for x, required_value in enumerate(required_values):
                required_value = required_values.iloc[x]
                if isinstance(required_value, float):
                    if math.isnan(required_value):
                        if i > 0:
                            warnings.append({
                                "message": "A required property is missing",
                                "supplemental": "A property value in {}.{} of investigation file at column {} is "
                                                "required".format(col, i + 1, x + 1),
                                "code": 4003
                            })
                            logger.warning(
                                "(W) A property value in {}.{} of investigation file at column {} is required".format(
                                    col, i+1, x + 1))
                        else:
                            warnings.append({
                                "message": "A required property is missing",
                                "supplemental": "A property value in {} of investigation file at column {} is "
                                                "required".format(col, x + 1),
                                "code": 4003
                            })
                            logger.warning(
                                "(W) A property value in {} of investigation file at column {} is required".format(
                                    col, x + 1))
                else:
                    if not required_value or str('Unnamed: ') in required_value:
                        if i > 0:
                            warnings.append({
                                "message": "A required property is missing",
                                "supplemental": "A property value in {}.{} of investigation file at column {} is "
                                                "required".format(col, i+1, x + 1),
                                "code": 4003
                            })
                            logger.warning(
                                "(W) A property value in {}.{} of investigation file at column {} is required".format(
                                    col, i+1, x + 1))
                        else:
                            warnings.append({
                                "message": "A required property is missing",
                                "supplemental": "A property value in {} of investigation file at column {} is "
                                                "required".format(col, x + 1),
                                "code": 4003
                            })
                            logger.warning(
                                "(W) A property value in {} of investigation file at column {} is required".format(
                                    col, x + 1))

    required_fields = [k.header for k in configs[('[investigation]', '')].get_isatab_configuration()[0].get_field() if k.is_required]
    check_section_against_required_fields_one_value(i_df['INVESTIGATION'], required_fields)
    check_section_against_required_fields_one_value(i_df['INVESTIGATION PUBLICATIONS'], required_fields)
    check_section_against_required_fields_one_value(i_df['INVESTIGATION CONTACTS'], required_fields)

    for x, study_df in enumerate(i_df['STUDY']):
        check_section_against_required_fields_one_value(i_df['STUDY'][x], required_fields, x)
        check_section_against_required_fields_one_value(i_df['STUDY DESIGN DESCRIPTORS'][x], required_fields, x)
        check_section_against_required_fields_one_value(i_df['STUDY PUBLICATIONS'][x], required_fields, x)
        check_section_against_required_fields_one_value(i_df['STUDY FACTORS'][x], required_fields, x)
        check_section_against_required_fields_one_value(i_df['STUDY ASSAYS'][x], required_fields, x)
        check_section_against_required_fields_one_value(i_df['STUDY PROTOCOLS'][x], required_fields, x)
        check_section_against_required_fields_one_value(i_df['STUDY CONTACTS'][x], required_fields, x)


def check_study_table_against_config(s_df, protocols_declared, config):
    # We are assuming the table load validation earlier passed

    # First check column order is correct against the configuration
    columns = s_df.columns
    object_index = ((k, x) for k, x in enumerate(columns) if x in {'Source Name', 'Sample Name',
                                                              'Extract Name', 'Labeled Extract Name', 'Raw Data File',
                                                              'Raw Spectral Data File', 'Array Data File',
                                                              'Protein Assignment File', 'Peptide Assignment File',
                                                              'Post Translational Modification Assignment File',
                                                              'Derived Spectral Data File',
                                                              'Derived Array Data File'} or 'Protocol REF' in x or
                    'Characteristics[' in x or 'Factor Value[' in x or 'Parameter Value[' in x)
    fields = [k.header for k in config.get_isatab_configuration()[0].get_field()]
    protocols = [(i.pos, i.protocol_type) for i in config.get_isatab_configuration()[0].get_protocol_field()]
    for protocol in protocols:
        fields.insert(protocol[0], 'Protocol REF')
    # strip out non-config columns
    object_index = (k for k in object_index if k[1] in fields)
    for x, object in enumerate(object_index):
        if fields[x] != object[1]:
            warnings.append({
                "message": "The column order in assay table is not valid",
                "supplemental": "Unexpected heading found. Expected {} but found {} at column number {}"
                    .format(fields[x], object[1], object[0]),
                "code": 4005
            })
            logger.warning("(W) Unexpected heading found. Expected {} but found {} at column number {}"
                        .format(fields[x], object[1], object[0]))

    # Second, check if Protocol REFs are of valid types
    for row in s_df['Protocol REF']:
        print("{}: {} {}".format(row, protocols_declared[row] in [k[1] for k in protocols], [k[1] for k in protocols]))
    # Third, check if required values are present


def check_assay_table_against_config(s_df, config):
    import itertools
    indexed_col_regex = re.compile('(.*?)\.\d+')
    # We are assuming the table load validation earlier passed
    # First check column order is correct against the configuration
    columns = s_df.columns
    norm_columns = list()
    for x, column in enumerate(columns):
        if indexed_col_regex.match(column):
            norm_columns.append(column[:column.rfind('.')])
        else:
            norm_columns.append(column)
    norm_columns = (k for k, g in itertools.groupby(norm_columns))  # remove adjacent dups - i.e. chained Protocol REFs
    object_index = ((k, x) for k, x in enumerate(norm_columns) if x in {'Source Name', 'Sample Name',
                                                              'Extract Name', 'Labeled Extract Name', 'Raw Data File',
                                                              'Raw Spectral Data File', 'Array Data File',
                                                              'Protein Assignment File', 'Peptide Assignment File',
                                                              'Post Translational Modification Assignment File',
                                                              'Derived Spectral Data File',
                                                              'Derived Array Data File', 'Assay Name'} or 'Protocol REF' in x or
                    'Characteristics[' in x or 'Factor Value[' in x or 'Parameter Value[' in x or 'Comment[' in x)
    fields = [k.header for k in config.get_isatab_configuration()[0].get_field()]
    protocols = [(k.pos, k.protocol_type) for k in config.get_isatab_configuration()[0].get_protocol_field()]
    for protocol in protocols:
        fields.insert(protocol[0], 'Protocol REF')
    # strip out non-config columns
    object_index = (k for k in object_index if k[1] in fields)
    for x, object in enumerate(object_index):
        if fields[x] != object[1]:
            warnings.append({
                "message": "The column order in assay table is not valid",
                "supplemental": "Unexpected heading found. Expected {} but found {} at column number {}"
                    .format(fields[x], object[1], object[0]),
                "code": 4005
            })
            logger.warning("(W) Unexpected heading found. Expected {} but found {} at column number {}".format(fields[x], object[1], object[0]))


def cell_has_value(cell):
    if isinstance(cell, float):
        if math.isnan(cell):
            return True
        else:
            return False
    else:
        if not cell.strip():
            return False
        elif 'Unnamed: ' in cell:
            return False
        else:
            return True


def check_assay_table_with_config(df, config, filename, protocol_names_and_types):
    indexed_col_regex = re.compile('(.*?)\.\d+')
    columns = list(df.columns)
    # Get required headers from config and check if they are present in the table; Rule 4010
    required_fields = (k.header for k in config.get_isatab_configuration()[0].get_field() if k.is_required)
    for required_field in required_fields:
        if required_field not in columns:
            warnings.append({
                "message": "A required column in assay table is not present",
                "supplemental": "In {} the required column {} missing from column headings"
                    .format(filename, required_field),
                "code": 4010
            })
            logger.warning("(W) In {} the required column {} missing from column headings".format(filename, required_field))
        else:
            # Now check that the required column cells all have values, Rules 4003-4008
            for y, cell in enumerate(df[required_field]):
                if not cell_has_value(cell):
                    warnings.append({
                        "message": "A required cell value is missing",
                        "supplemental": "Cell at row {} in column '{}' has no value".format(y, required_field),
                        "code": 4012
                    })
                    logger.warning("(W) Cell at row {} in column '{}' has no value, but it is required by the "
                                "configuration".format(y, required_field))

    # Check if protocol ref column values are consistently structured
    protocol_ref_index = (k for k in columns if 'protocol ref' in k.lower())
    prots_ok = True
    for each in protocol_ref_index:
        prots_found = set()
        for cell in df[each]:
            prots_found.add(cell)
        if len(prots_found) > 1:
            warnings.append({
                "message": "Multiple protocol references in Protocol REF column",
                "supplemental": "Multiple protocol references {} are found in {}".format(prots_found, each),
                "code": 4999
            })
            logger.warning("(W) Multiple protocol references {} are found in {}".format(prots_found, each))
            logger.warning("(W) Only one protocol reference should be used in a Protocol REF column.")
            prots_ok = False


def check_study_assay_tables_against_config(i_df, dir_context, configs):
    """Used for rules 4003-4008"""
    for i, study_df in enumerate(i_df['STUDY']):
        study_filename = study_df.iloc[0]['Study File Name']
        protocol_names = i_df['STUDY PROTOCOLS'][i]['Study Protocol Name'].tolist()
        protocol_types = i_df['STUDY PROTOCOLS'][i]['Study Protocol Type'].tolist()
        protocol_names_and_types = dict(zip(protocol_names, protocol_types))
        if study_filename:
            try:
                df = load_table(os.path.join(dir_context, study_filename))
                config = configs[('[Sample]', '')]
                logger.info("Checking study file {} against default study table configuration...".format(study_filename))
                check_assay_table_with_config(df, config, study_filename, protocol_names_and_types)
            except IOError:
                pass
        for j, assay_df in enumerate(i_df['STUDY ASSAYS']):
            assay_filename = assay_df['Study Assay File Name'].tolist()[0]
            measurement_type = assay_df['Study Assay Measurement Type'].tolist()[0]
            technology_type = assay_df['Study Assay Technology Type'].tolist()[0]
            if assay_filename:
                try:
                    df = load_table(os.path.join(dir_context, assay_filename))
                    config = configs[(measurement_type, technology_type)]
                    logger.info(
                        "Checking assay file {} against default table configuration ({}, {})...".format(assay_filename, measurement_type, technology_type))
                    check_assay_table_with_config(df, config, assay_filename, protocol_names_and_types)
                    # check_assay_table_with_config(df, protocols, config, assay_filename)
                except IOError:
                    pass
        # TODO: Check protocol usage - Rule 4009


def check_factor_value_presence(table):
    factor_fields = (k for k in table.columns if k.lower().startswith('factor value'))
    for factor_field in factor_fields:
        for x, cell_value in enumerate(table.fillna('')[factor_field]):
            if not str(cell_value):
                warnings.append({
                    "message": "A required node factor value is missing value",
                    "supplemental": "(W) Missing value for '" + factor_field + "' at row " + str(x) + " in " +
                                    table.filename,
                    "code": 4007
                })
                logger.warning("(W) Missing value for '" + factor_field + "' at row " + str(x) + " in " + table.filename)


def check_required_fields(table, cfg):
    for fheader in (k.header for k in cfg.get_isatab_configuration()[0].get_field() if k.is_required):
        found_field = [k for k in table.columns if k.lower() == fheader.lower()]
        if not found_field:
            warnings.append({
                "message": "A required column in assay table is not present",
                "supplemental": "Required field '" + fheader + "' not found in the file '" + table.filename + "'",
                "code": 4010
            })
            logger.warning("(W) Required field '" + fheader + "' not found in the file '" + table.filename + "'")
        elif len(found_field) > 1:
            warnings.append({
                "message": "Multiple columns found",
                "supplemental": "Field '" + fheader + "' cannot have multiple values in the file '" + table.filename,
                "code": 4013
            })
            logger.warning("(W) Field '" + fheader + "' cannot have multiple values in the file '" + table.filename)


def check_sample_names(study_sample_table, assay_tables=list()):
    if assay_tables:
        study_samples = set(study_sample_table['Sample Name'])
        for assay_table in assay_tables:
            assay_samples = set(assay_table['Sample Name'])
            for assay_sample in assay_samples:
                if assay_sample not in study_samples:
                    warnings.append({
                        "message": "Missing Sample",
                        "supplemental": "{} is a Sample Name in {}, but it is not defined in the Study Sample File {}."
                                .format(assay_sample, assay_table.filename, study_sample_table.filename),
                        "code": 1003
                    })
                    logger.warning("(W) {} is a Sample Name in {}, but it is not defined in the Study Sample File {}."
                                .format(assay_sample, assay_table.filename, study_sample_table.filename))


def check_field_values(table, cfg):
    def check_single_field(cell_value, cfg_field):
        # First check if the value is required by config
        if isinstance(cell_value, float):
            if math.isnan(cell_value):
                if cfg_field.is_required:
                    warnings.append({
                        "message": "A required column in assay table is not present",
                        "supplemental": "Missing value for the required field '" + cfg_field.header
                                        + "' in the file '" + table.filename + "'",
                        "code": 4010
                    })
                    logger.warning("(W) Missing value for the required field '" + cfg_field.header + "' in the file '" +
                                table.filename + "'")
                return True
        elif isinstance(cell_value, str):
            value = cell_value.strip()
            if not value:
                if cfg_field.is_required:
                    warnings.append({
                        "message": "A required cell value is missing",
                        "supplemental": "Missing value for the required field '" + cfg_field.header + "' in the file '" +
                                table.filename + "'",
                        "code": 4012
                    })
                    logger.warning("(W) Missing value for the required field '" + cfg_field.header + "' in the file '" +
                                table.filename + "'")
                return True
        is_valid_value = True
        data_type = cfg_field.data_type.lower().strip()
        if not data_type or data_type == 'string':
            return True
        if 'boolean' == data_type:
            is_valid_value = 'true' == cell_value.strip() or 'false' == cell_value.strip()
        elif 'date' == data_type:
            try:
                iso8601.parse_date(cell_value)
            except iso8601.ParseError:
                is_valid_value = False
        elif 'integer' == data_type:
            try:
                int(cell_value)
            except ValueError:
                is_valid_value = False
        elif 'float' == data_type:
            try:
                float(cell_value)
            except ValueError:
                is_valid_value = False
        elif data_type == 'list':
            list_values = {k.lower() for k in cfg_field.list_values.split(',')}
            if cell_value.lower() not in list_values:
                is_valid_value = False
        elif data_type in {'ontology-term', 'ontology term'}:
            return True  # Structure and values checked in check_ontology_fields()
        else:
            warnings.append({
                "message": "Unknown data type found",
                "supplemental": "Unknown data type '" + data_type + "' for field '" + cfg_field.header +
                                "' in the file '" + table.filename + "'",
                "code": 4011
            })
            logger.warning("(W) Unknown data type '" + data_type + "' for field '" + cfg_field.header +
                        "' in the file '" + table.filename + "'")
            return False
        if not is_valid_value:
            warnings.append({
                "message": "A value does not correspond to the correct data type",
                "supplemental": "Invalid value '" + cell_value + "' for type '" + data_type + "' of the field '"
                                + cfg_field.header + "'",
                "code": 4011
            })
            logger.warning("(W) Invalid value '" + cell_value + "' for type '" + data_type + "' of the field '" +
                        cfg_field.header + "'")
            if data_type == 'list':
                logger.warning("(W) Value must be one of: " + cfg_field.list_values)
        return is_valid_value

    result = True
    for irow in six.moves.range(len(table.index)):
        ncols = len(table.columns)
        for icol in six.moves.range(ncols):
            # cfields = [k for k in cfg.get_isatab_configuration()[0].get_field() if k.header == table.columns[icol]]
            # if len(cfields) == 1:
            #     cfield = cfields[0]
            #     result = result and check_single_field(table.iloc[irow][cfield.header], cfield)
            try:
                cfield = next(k for k in cfg.get_isatab_configuration()[0].get_field() if k.header==table.columns[icol])
                result = result and check_single_field(table.iloc[irow][cfield.header], cfield)
            except StopIteration:
                pass

    return result


def check_unit_field(table, cfg):
    def check_unit_value(cell_value, unit_value, cfield, filename):
        if cell_has_value(cell_value) or cell_has_value(unit_value):
            warnings.append({
                "message": "Cell found has unit but no value",
                "supplemental": "Field '" + cfield.header + "' has a unit but not a value in the file '" + filename
                                + "'",
                "code": 4999
            })
            logger.warning("(W) Field '" + cfield.header + "' has a unit but not a value in the file '" + filename + "'")
            return False
        return True

    result = True
    for icol, header in enumerate(table.columns):

        try: cfield = next(k for k in cfg.get_isatab_configuration()[0].get_field() if k.header==header)
        except StopIteration: continue

        try: ucfield= next(k for k in cfg.get_isatab_configuration()[0].get_unit_field() if k.pos==cfield.pos+1)
        except StopIteration: continue

        if ucfield.is_required:
            rheader = None
            rindx = icol + 1
            if rindx < len(table.columns):
                rheader = table.columns[rindx]
            if rheader is None or rheader.lower() != 'unit':
                warnings.append({
                    "message": "Cell requires a Unit",
                    "supplemental": "The field '" + header + "' in the file '" + table.filename + "' misses a required "
                                                                                                  "'Unit' column",
                    "code": 4999
                })
                logger.warning("(W) The field '" + header + "' in the file '" + table.filename +
                            "' misses a required 'Unit' column")
                result = False
            else:
                for irow in six.moves.range(len(table.index)):
                    result = result and check_unit_value(table.iloc[irow][icol], table.iloc[irow][rindx],
                                                         cfield, table.filename)
    return result


def check_protocol_fields(table, cfg, proto_map):
    from itertools import tee

    def pairwise(iterable):  # A lovely pairwise iterator
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    proto_ref_index = (k for k in table.columns if 'protocol ref' in k.lower())
    result = True
    for each in proto_ref_index:
        prots_found = set()
        for cell in table[each]:
            prots_found.add(cell)
        if len(prots_found) > 1:
            logger.warning("(W) Multiple protocol references {} are found in {}".format(prots_found, each))
            logger.warning("(W) Only one protocol reference should be used in a Protocol REF column.")
            result = False
    if result:
        field_headers = [k for k in table.columns if
                         k.lower().endswith((' name', ' data file', ' data matrix file'))]
        protos = [k for k in table.columns if k.lower() == 'protocol ref']

        try: last_proto_indx = table.columns.get_loc(protos[-1])
        except IndexError: last_proto_indx = -1

        try: last_mat_or_dat_indx = table.columns.get_loc(field_headers[-1])
        except IndexError: last_mat_or_dat_indx = -1

        if last_proto_indx > last_mat_or_dat_indx:
            logger.warning("(W) Protocol REF column without output in file '{}'".format(table.filename))
        for left, right in pairwise(field_headers):
            cleft = next((k for k in cfg.get_isatab_configuration()[0].get_field() if k.header.lower()==left.lower()), None)
            cright = next((k for k in cfg.get_isatab_configuration()[0].get_field() if k.header.lower()==right.lower()), None)
            if cleft is not None and cright is not None:
                cprotos = {k.protocol_type for k in cfg.get_isatab_configuration()[0].get_protocol_field() if
                           cleft.pos < k.pos and cright.pos > k.pos}
                fprotos_headers = (k for k in table.columns[
                                              table.columns.get_loc(cleft.header):table.columns.get_loc(
                                                  cright.header)] if
                                   'protocol ref' in k.lower())
                fprotos = set()
                for header in fprotos_headers:
                    proto_name = table.iloc[0][header]
                    try:
                        proto_type = proto_map[proto_name]
                        fprotos.add(proto_type)
                    except KeyError:
                        warnings.append({
                            "message": "Missing Protocol declaration",
                            "supplemental": " Could not find protocol type for protocol name '{}', trying to validate "
                                            "against name only".format(proto_name),
                            "code": 1007
                        })
                        logger.warning("(W) Could not find protocol type for protocol name '{}', trying to validate "
                                    "against name only".format(proto_name))
                        fprotos.append(proto_name)
                invalid_protos = cprotos - fprotos
                if invalid_protos:
                    warnings.append({
                        "message": "Missing Protocol declaration",
                        "supplemental": "Protocol(s) of type " + str(list(invalid_protos))
                                        + " defined in the ISA-configuration expected as a between '"
                                        + cleft.header + "' and '" + cright.header
                                        + "' but has not been found, in the file '" + table.filename + "'",
                        "code": 1007
                    })
                    logger.warning("(W) Protocol(s) of type " + str(
                        list(invalid_protos)) + " defined in the ISA-configuration expected as a between '" +
                                cleft.header + "' and '" + cright.header + "' but has not been found, in the file '" + table.filename + "'")
                    result = False
    return result


def check_ontology_fields(table, cfg):
    def check_single_field(cell_value, source, acc, cfield, filename):
        if cell_has_value(cell_value) or cell_has_value(source) or cell_has_value(acc):
            warnings.append({
                "message": "Missing Term Source REF in annotation or missing Term Source Name",
                "supplemental": "Incomplete values for ontology headers, for the field '"
                                + cfield.header + "' in the file '"
                                + filename + "'. Check that all the label/accession/source are provided.",
                "code": 3008
            })
            logger.warning(
                "(W) Incomplete values for ontology headers, for the field '" + cfield.header + "' in the file '" +
                filename + "'. Check that all the label/accession/source are provided.")
            return False
        # TODO: Implement check against declared ontology sources in investigation file
        return True

    result = True
    nfields = len(table.columns)
    for icol, header in enumerate(table.columns):

        try: cfield = next(k for k in cfg.get_isatab_configuration()[0].get_field() if k.header==header)
        except StopIteration: continue

        if cfield.get_recommended_ontologies() is None:
            continue

        rindx = icol + 1
        rrindx = icol + 2
        rheader = ''
        rrheader = ''
        if rindx < nfields:
            rheader = table.columns[rindx]
        if rrindx < nfields:
            rrheader = table.columns[rrindx]
        if 'term source ref' not in rheader.lower() or 'term accession number' not in rrheader.lower():
            logger.warning(
                "(W) The Field '" + header + "' should have values from ontologies and has no ontology headers instead")
            result = False
            continue

        for irow in six.moves.range(len(table.index)):
            result = result and check_single_field(table.iloc[irow][icol], table.iloc[irow][rindx],
                                                   table.iloc[irow][rrindx], cfield, table.filename)

    return result


BASE_DIR = os.path.dirname(__file__)
default_config_dir = os.path.join(BASE_DIR, 'config', 'xml')


def validate2(fp, config_dir=default_config_dir, log_level=logging.INFO):
    global errors
    global warnings
    errors = list()
    warnings = list()
    logger.setLevel(log_level)
    logger.info("ISA tab Validator from ISA tools API v0.3")
    stream = six.StringIO()
    handler = logging.StreamHandler(stream)
    logger.addHandler(handler)
    try:
        # check_utf8(fp)  # skip as does not correctly report right now
        logger.info("Loading... {}".format(fp.name))
        i_df = load2(fp=fp)
        logger.info("Running prechecks...")
        check_filenames_present(i_df)  # Rule 3005
        check_table_files_read(i_df, os.path.dirname(fp.name))  # Rules 0006 and 0008
        # check_table_files_load(i_df, os.path.dirname(fp.name))  # Rules 0007 and 0009, covered by later validation?
        check_samples_not_declared_in_study_used_in_assay(i_df, os.path.dirname(fp.name))  # Rule 1003
        check_study_factor_usage(i_df, os.path.dirname(fp.name))  # Rules 1008 and 1021
        check_protocol_usage(i_df, os.path.dirname(fp.name))  # Rules 1007 and 1019
        check_protocol_parameter_usage(i_df, os.path.dirname(fp.name))  # Rules 1009 and 1020
        check_date_formats(i_df)  # Rule 3001
        check_dois(i_df)  # Rule 3002
        check_pubmed_ids_format(i_df)  # Rule 3003
        check_protocol_names(i_df)  # Rule 1010
        check_protocol_parameter_names(i_df)  # Rule 1011
        check_study_factor_names(i_df)  # Rule 1012
        check_ontology_sources(i_df)  # Rule 3008
        logger.info("Finished prechecks...")
        logger.info("Loading configurations found in {}".format(config_dir))
        configs = load_config(config_dir)  # Rule 4001
        if not configs:
            raise SystemError("No configuration to load so cannot proceed with validation!")
        logger.info("Using configurations found in {}".format(config_dir))
        check_measurement_technology_types(i_df, configs)  # Rule 4002
        logger.info("Checking investigation file against configuration...")
        check_investigation_against_config(i_df, configs)  # Rule 4003 for investigation file only
        logger.info("Finished checking investigation file")
        for i, study_df in enumerate(i_df['STUDY']):
            study_filename = study_df.iloc[0]['Study File Name']
            if study_filename:
                study_sample_table = None
                assay_tables = list()
                protocol_names = i_df['STUDY PROTOCOLS'][i]['Study Protocol Name'].tolist()
                protocol_types = i_df['STUDY PROTOCOLS'][i]['Study Protocol Type'].tolist()
                protocol_names_and_types = dict(zip(protocol_names, protocol_types))
                try:
                    logger.info("Loading... {}".format(study_filename))
                    study_sample_table = load_table(open(os.path.join(os.path.dirname(fp.name), study_filename)))
                    study_sample_table.filename = study_filename
                    config = configs[('[Sample]', '')]
                    logger.info(
                        "Validating {} against default study table configuration".format(study_filename))
                    logger.info("Checking Factor Value presence...")
                    check_factor_value_presence(study_sample_table)  # Rule 4007
                    logger.info("Checking required fields...")
                    check_required_fields(study_sample_table, config)  # Rule 4003-8, 4010
                    logger.info("Checking generic fields...")
                    if not check_field_values(study_sample_table, config):  # Rule 4011
                        logger.warning("(W) There are some field value inconsistencies in {} against {} "
                                    "configuration".format(study_sample_table.filename, 'Study Sample'))
                    logger.info("Checking unit fields...")
                    if not check_unit_field(study_sample_table, config):
                        logger.warning("(W) There are some unit value inconsistencies in {} against {} "
                                    "configuration".format(study_sample_table.filename, 'Study Sample'))
                    logger.info("Checking protocol fields...")
                    if not check_protocol_fields(study_sample_table, config, protocol_names_and_types):  # Rule 4009
                        logger.warning("(W) There are some protocol inconsistencies in {} against {} "
                                    "configuration".format(study_sample_table.filename, 'Study Sample'))
                    logger.info("Checking ontology fields...")
                    if not check_ontology_fields(study_sample_table, config):  # Rule 3010
                        logger.warning("(W) There are some ontology annotation inconsistencies in {} against {} "
                                    "configuration".format(study_sample_table.filename, 'Study Sample'))
                    logger.info("Finished validation on {}".format(study_filename))
                except IOError:
                    pass
                assay_df = i_df['STUDY ASSAYS'][i]
                for x, assay_filename in enumerate(assay_df['Study Assay File Name'].tolist()):
                    measurement_type = assay_df['Study Assay Measurement Type'].tolist()[x]
                    technology_type = assay_df['Study Assay Technology Type'].tolist()[x]
                    if assay_filename is not '':
                        try:
                            logger.info("Loading... {}".format(assay_filename))
                            assay_table = load_table(open(os.path.join(os.path.dirname(fp.name), assay_filename)))
                            assay_table.filename = assay_filename
                            assay_tables.append(assay_table)
                            config = configs[(measurement_type, technology_type)]
                            logger.info(
                                "Validating {} against assay table configuration ({}, {})...".format(
                                    assay_filename, measurement_type, technology_type))
                            logger.info("Checking Factor Value presence...")
                            check_factor_value_presence(assay_table)  # Rule 4007
                            logger.info("Checking required fields...")
                            check_required_fields(assay_table, config)  # Rule 4003-8, 4010
                            logger.info("Checking generic fields...")
                            if not check_field_values(assay_table, config):  # Rule 4011
                                logger.warning(
                                    "(W) There are some field value inconsistencies in {} against {} configuration".format(
                                        assay_table.filename, (measurement_type, technology_type)))
                            logger.info("Checking unit fields...")
                            if not check_unit_field(assay_table, config):
                                logger.warning(
                                    "(W) There are some unit value inconsistencies in {} against {} configuration".format(
                                        assay_table.filename, (measurement_type, technology_type)))
                            logger.info("Checking protocol fields...")
                            if not check_protocol_fields(assay_table, config, protocol_names_and_types):  # Rule 4009
                                logger.warning("(W) There are some protocol inconsistencies in {} against {} "
                                            "configuration".format(assay_table.filename, (measurement_type, technology_type)))
                            logger.info("Checking ontology fields...")
                            if not check_ontology_fields(assay_table, config):  # Rule 3010
                                logger.warning("(W) There are some ontology annotation inconsistencies in {} against {} "
                                            "configuration".format(assay_table.filename, (measurement_type, technology_type)))
                            logger.info("Finished validation on {}".format(assay_filename))
                        except IOError:
                            pass
                    if study_sample_table is not None:
                        logger.info("Checking consistencies between study sample table and assay tables...")
                        check_sample_names(study_sample_table, assay_tables)
                        logger.info("Finished checking study sample table against assay tables...")
                    logger.info("Finished validation...")
    except CParserError as cpe:
        errors.append({
            "message": "Unknown/System Error",
            "supplemental": "The validator could not identify what the error is: {}".format(str(cpe)),
            "code": 0
        })
        logger.fatal("(F) There was an error when trying to parse the ISA tab")
        logger.fatal(cpe)
    except ValueError as ve:
        errors.append({
            "message": "Unknown/System Error",
            "supplemental": "The validator could not identify what the error is: {}".format(str(ve)),
            "code": 0
        })
        logger.fatal("(F) There was an error when trying to parse the ISA tab")
        logger.fatal(ve)
    except SystemError as se:
        errors.append({
            "message": "Unknown/System Error",
            "supplemental": "The validator could not identify what the error is: {}".format(str(se)),
            "code": 0
        })
        logger.fatal("(F) Something went very very wrong! :(")
        logger.fatal(se)
    except BaseException as b:
        logger.fatal("(F) A {} was raised!".format(type(b).__name__))
        logger.fatal("Value: {}".format(b))
    finally:
        handler.flush()
        return {
            "errors": errors,
            "warnings": warnings,
            "validation_finished": True
        }


def batch_validate(tab_dir_list):
    """ Validate a batch of ISA-Tab archives
    :param tab_dir_list: List of file paths to the ISA-Tab archives to validate
    :return: batch report as JSON

    Example:
        from isatools import isatab
        my_tabs = [
            '/path/to/study1/',
            '/path/to/study2/'
        ]
        batch_report = isatab.batch_validate(my_tabs, '/path/to/report.txt')
    """
    batch_report = {
        "batch_report": []
    }
    for tab_dir in tab_dir_list:
        logger.info("***Validating {}***\n".format(tab_dir))
        try:
            i_file = next(glob.iglob(os.path.join(tab_dir, 'i_*.txt')))
            with open(i_file) as fp:
                batch_report['batch_report'].append(
                    {
                        "filename": fp.name,
                        "report": validate2(fp)
                    }
                )
        except StopIteration:
            logger.warning("Could not find an investigation file, skipping {}".format(tab_dir))
    return batch_report


def dumps(isa_obj):
    import tempfile
    import shutil
    tmp = None
    output = []
    try:
        tmp = tempfile.mkdtemp()
        dump(isa_obj=isa_obj, output_path=tmp)
        with open(os.path.join(tmp, 'i_investigation.txt')) as i_fp:
            output.append(os.path.join(tmp, 'i_investigation.txt'))
            output.append(i_fp.read())
        s_files = glob.iglob(os.path.join(tmp, 's_*'))
        for s_file in s_files:
            with open(s_file) as s_fp:
                output.append("--------")
                output.append(s_file)
                output.append(s_fp.read())
        a_files = glob.iglob(os.path.join(tmp, 'a_*'))
        for a_file in a_files:
            with open(a_file) as a_fp:
                output.append("--------")
                output.append(a_file)
                output.append(a_fp.read())
    finally:
        if tmp is not None:
            shutil.rmtree(tmp)
    return '\n'.join(output)
