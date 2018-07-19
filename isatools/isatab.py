"""Functions for reading, writing and validating ISA-Tab.

Don't forget to read the ISA-Tab spec:
http://isa-specs.readthedocs.io/en/latest/isatab.html
"""
from __future__ import absolute_import
import csv
import glob
import io
import iso8601
import logging
import math
import numpy as np
import os
import pandas as pd
import re
import shutil
import tempfile
from bisect import bisect_left
from bisect import bisect_right
from io import StringIO
from itertools import tee
from itertools import zip_longest
from pandas.io.parsers import ParserError
from progressbar import ProgressBar
from progressbar import SimpleProgress
from progressbar import Bar
from progressbar import ETA

from isatools import logging as isa_logging
from isatools.io import isatab_configurator
from isatools.model import *


log = logging.getLogger('isatools')


def xml_config_contents(filename):
    config_filepath = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'config',
        'xml',
        filename,
    )
    with open(config_filepath) as f:
        return f.read()


STUDY_SAMPLE_XML_CONFIG = xml_config_contents('studySample.xml')
NUMBER_OF_STUDY_GROUPS = 'Comment[Number of Study Groups]'


class _Defaults(object):

    def __init__(self):
        self._tab_options = {
            'readCellQuotes': False,  # read cell quotes as part of cell values
            'writeCellQuotes': True,  # write out cell values enclosed with quotes
            'forceFitColumns': True,
            'validateBeforeRead': False,
            'validateAfterWrite': False
        }
        self._show_progressbar = False
        self._log_level = logging.WARNING

    def set_tab_option(self, optname, optvalue):
        self._tab_options[optname] = optvalue

    def set_defaults(self, show_progressbar=None, log_level=None):
        if show_progressbar is not None:
            self._show_progressbar = show_progressbar
        if log_level is not None:
            self._log_level = log_level

    @property
    def tab_options(self):
        return self._tab_options

    @property
    def show_progressbar(self):
        return self._show_progressbar

    @property
    def log_level(self):
        return self._log_level


defaults = _Defaults()


def set_defaults(show_progressbar=None, log_level=None):
    """
    Set the default IsaTab options.
    """
    defaults.set_defaults(show_progressbar, log_level)


def set_tab_option(optname, optvalue):
    """
    Set the default value for one of the options that gets passed into the
    IsaTabParser or IsaTabWriter constructor.
    """
    defaults.tab_options[optname] = optvalue


class TransposedTabParser(object):
    """
    Parser for transposed tables, such as the ISA-Tab investigation table,
    or the MAGE-TAB IDF table. The headings are in column 0 with values,
    perhaps multiple, reading in columns towards the right. These tables do
    not necessarily have an even shape (row lengths may differ).

    This reads the transposed table into a dictionary where key is heading and
    value is a list of cell values for the heading. No relations between
    headings is assumed and the order of values is implied by the order of the
    cell value lists.

    Does not allow duplicate labels.
    """
    def __init__(self, tab_options=None, show_progressbar=None, log_level=None):
        if tab_options is None:
            self.tab_options = defaults.tab_options
        else:
            self.tab_options=tab_options
        if show_progressbar is None:
            self.show_progressbar = defaults.show_progressbar
        else:
            self.show_progressbar=show_progressbar
        if log_level is None:
            self.log_level = defaults.log_level
        else:
            if not isinstance(tab_options, dict):
                raise TypeError(
                    'tab_options must be dict, not {tab_options_type}'
                    .format(tab_options_type=type(tab_options))
                )
            self.log_level = log_level

        self._ttable_dict = dict(header=list(), table=dict())

    def parse(self, filename):
        try:
            with open(filename, encoding='utf-8') as unicode_file:
                ttable_reader = csv.reader(
                    filter(lambda r: r[0] != '#', unicode_file),
                    dialect='excel-tab')
                for row in ttable_reader:
                    if len(row) > 0:
                        key = get_squashed(key=row[0])
                        self._ttable_dict['header'].append(key)
                        self._ttable_dict['table'][key] = row[1:]
        except UnicodeDecodeError:
            with open(filename, encoding='ISO8859-2') as latin2_file:
                ttable_reader = csv.reader(
                    filter(lambda r: r[0] != '#', latin2_file),
                    dialect='excel-tab')
                for row in ttable_reader:
                    if len(row) > 0:
                        key = get_squashed(key=row[0])
                        self._ttable_dict['header'].append(key)
                        self._ttable_dict['table'][key] = row[1:]

        return self._ttable_dict


validator_errors = []
validator_warnings = []
validator_info = []

# REGEXES
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
_LABELS_MATERIAL_NODES = ['Source Name', 'Sample Name', 'Extract Name',
                          'Labeled Extract Name']
_LABELS_DATA_NODES = ['Raw Data File', 'Raw Spectral Data File',
                      'Derived Spectral Data File', 'Derived Array Data File',
                      'Array Data File', 'Protein Assignment File',
                      'Peptide Assignment File',
                      'Post Translational Modification Assignment File',
                      'Acquisition Parameter Data File',
                      'Free Induction Decay Data File',
                      'Derived Array Data Matrix File', 'Image File',
                      'Derived Data File', 'Metabolite Assignment File']
_LABELS_ASSAY_NODES = ['Assay Name', 'MS Assay Name',
                       'Hybridization Assay Name', 'Scan Name',
                       'Data Transformation Name', 'Normalization Name']


def dump(isa_obj, output_path, i_file_name='i_investigation.txt',
         skip_dump_tables=False, write_factor_values_in_assay_table=False):

    def _build_roles_str(roles):
        log.debug('building roles from: %s', roles)
        if roles is None:
            roles = list()
        roles_names = ''
        roles_accession_numbers = ''
        roles_source_refs = ''
        for role in roles:
            roles_names += (role.term if role.term else '') + ';'
            roles_accession_numbers += (role.term_accession if role.term_accession else '') + ';'
            roles_source_refs += (role.term_source.name if role.term_source else '') + ';'
        if len(roles) > 0:
            roles_names = roles_names[:-1]
            roles_accession_numbers = roles_accession_numbers[:-1]
            roles_source_refs = roles_source_refs[:-1]
        log.debug('role_names: %s', roles)
        log.debug('roles_accession_numbers: %s', roles)
        log.debug('roles_source_refs: %s', roles)
        return roles_names, roles_accession_numbers, roles_source_refs

    def _build_contacts_section_df(prefix='Investigation', contacts=list()):
        log.debug('building contacts from: %s', contacts)
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
        if len(contacts) > 0:
            max_comment = Person()
            for contact in contacts:
                if len(contact.comments) > len(max_comment.comments):
                    max_comment = contact
            for comment in max_comment.comments:
                if 'Comment[' + comment.name + ']' not in contacts_df_cols:
                    contacts_df_cols.append('Comment[' + comment.name + ']')
        contacts_df = pd.DataFrame(columns=tuple(contacts_df_cols))
        for i, contact in enumerate(contacts):
            log.debug('%s iteration, item=%s', i, contact)
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
            for j, _ in enumerate(max_comment.comments):
                log.debug('%s iteration, item=%s', j, _)
                try:
                    contacts_df_row.append(contact.comments[j].value)
                except IndexError:
                    contacts_df_row.append('')
            log.debug('row=%s', contacts_df_row)
            contacts_df.loc[i] = contacts_df_row
        return contacts_df.set_index(prefix + ' Person Last Name').T

    def _build_publications_section_df(prefix='Investigation', publications=list()):
        log.debug('building contacts from: %s', publications)
        publications_df_cols = [prefix + ' PubMed ID',
                                prefix + ' Publication DOI',
                                prefix + ' Publication Author List',
                                prefix + ' Publication Title',
                                prefix + ' Publication Status',
                                prefix + ' Publication Status Term Accession Number',
                                prefix + ' Publication Status Term Source REF']
        if len(publications) > 0:
            try:
                for comment in publications[0].comments:
                    publications_df_cols.append('Comment[' + comment.name + ']')
            except TypeError:
                pass
        publications_df = pd.DataFrame(columns=tuple(publications_df_cols))
        for i, publication in enumerate(publications):
            log.debug('%s iteration, item=%s', i, publication)
            if publication.status is not None:
                status_term = publication.status.term
                status_term_accession = publication.status.term_accession
                if publication.status.term_source is not None:
                    status_term_source_name = publication.status.term_source.name
                else:
                    status_term_source_name = ''
            else:
                status_term = ''
                status_term_accession = ''
                status_term_source_name = ''
            publications_df_row = [
                publication.pubmed_id,
                publication.doi,
                publication.author_list,
                publication.title,
                status_term,
                status_term_accession,
                status_term_source_name,
            ]
            try:
                for comment in publication.comments:
                    publications_df_row.append(comment.value)
            except TypeError:
                pass
            log.debug('row=%s', publications_df_row)
            publications_df.loc[i] = publications_df_row
        return publications_df.set_index(prefix +' PubMed ID').T

    if not _RX_I_FILE_NAME.match(i_file_name):
        log.debug('investigation filename=', i_file_name)
        raise NameError('Investigation file must match pattern i_*.txt, got {}'
                        .format(i_file_name))

    if os.path.exists(output_path):
        fp = open(os.path.join(output_path, i_file_name), 'w', encoding='utf-8')
    else:
        log.debug('output_path=', i_file_name)
        raise FileNotFoundError("Can't find " + output_path)

    if not isinstance(isa_obj, Investigation):
        log.debug('object type=', type(isa_obj))
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
        log.debug('%s iteration, item=%s', i, ontology_source_reference)
        ontology_source_references_df.loc[i] = [
            ontology_source_reference.name,
            ontology_source_reference.file,
            ontology_source_reference.version,
            ontology_source_reference.description
        ]
        log.debug('ontology_source_reference=%s', ontology_source_references_df.loc[i])
    ontology_source_references_df = ontology_source_references_df.set_index('Term Source Name').T
    fp.write('ONTOLOGY SOURCE REFERENCE\n')
    ontology_source_references_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
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
    investigation_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                            index_label='Investigation Identifier')  # Need to set index_label as top left cell

    # Write INVESTIGATION PUBLICATIONS section
    investigation_publications_df = _build_publications_section_df(publications=investigation.publications)
    fp.write('INVESTIGATION PUBLICATIONS\n')
    investigation_publications_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                         index_label='Investigation PubMed ID')

    # Write INVESTIGATION CONTACTS section
    investigation_contacts_df = _build_contacts_section_df(contacts=investigation.contacts)
    fp.write('INVESTIGATION CONTACTS\n')
    investigation_contacts_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
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
        study_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8', index_label='Study Identifier')

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
        study_design_descriptors_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                           index_label='Study Design Type')

        # Write STUDY PUBLICATIONS section
        study_publications_df = _build_publications_section_df(prefix='Study', publications=study.publications)
        fp.write('STUDY PUBLICATIONS\n')
        study_publications_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8', index_label='Study PubMed ID')

        # Write STUDY FACTORS section
        study_factors_df = pd.DataFrame(columns=('Study Factor Name',
                                                 'Study Factor Type',
                                                 'Study Factor Type Term Accession Number',
                                                 'Study Factor Type Term Source REF'
                                                 )
                                        )
        for i, factor in enumerate(study.factors):
            if factor.factor_type is not None:
                factor_type_term = factor.factor_type.term
                factor_type_term_accession = factor.factor_type.term_accession
                if factor.factor_type.term_source is not None:
                    factor_type_term_term_source_name = factor.factor_type.term_source.name
                else:
                    factor_type_term_term_source_name = ''
            else:
                factor_type_term = ''
                factor_type_term_accession = ''
                factor_type_term_term_source_name = ''
            study_factors_df.loc[i] = [
                factor.name,
                factor_type_term,
                factor_type_term_accession,
                factor_type_term_term_source_name
            ]
        study_factors_df = study_factors_df.set_index('Study Factor Name').T
        fp.write('STUDY FACTORS\n')
        study_factors_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                index_label='Study Factor Name')

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
        study_assays_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                               index_label='Study Assay File Name')

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
            parameters_names = ''
            parameters_accession_numbers = ''
            parameters_source_refs = ''
            for parameter in protocol.parameters:
                parameters_names += parameter.parameter_name.term + ';'
                parameters_accession_numbers += (parameter.parameter_name.term_accession if parameter.parameter_name.term_accession is not None else '') + ';'
                parameters_source_refs += (parameter.parameter_name.term_source.name if parameter.parameter_name.term_source else '') + ';'
            if len(protocol.parameters) > 0:
                parameters_names = parameters_names[:-1]
                parameters_accession_numbers = parameters_accession_numbers[:-1]
                parameters_source_refs = parameters_source_refs[:-1]
            component_names = ''
            component_types = ''
            component_types_accession_numbers = ''
            component_types_source_refs = ''
            for component in protocol.components:
                component_names += component.name + ';'
                component_types += component.component_type.term + ';'
                component_types_accession_numbers += component.component_type.term_accession + ';'
                component_types_source_refs += component.component_type.term_source.name if component.component_type.term_source else '' + ';'
            if len(protocol.components) > 0:
                component_names = component_names[:-1]
                component_types = component_types[:-1]
                component_types_accession_numbers = component_types_accession_numbers[:-1]
                component_types_source_refs = component_types_source_refs[:-1]
            protocol_type_term = ''
            protocol_type_term_accession = ''
            protocol_type_term_source_name = ''
            if protocol.protocol_type:
                protocol_type_term = protocol.protocol_type.term
                protocol_type_term_accession = protocol.protocol_type.term_accession
                if protocol.protocol_type.term_source:
                    protocol_type_term_source_name = protocol.protocol_type.term_source.name
            study_protocols_df.loc[i] = [
                protocol.name,
                protocol_type_term,
                protocol_type_term_accession,
                protocol_type_term_source_name,
                protocol.description,
                protocol.uri,
                protocol.version,
                parameters_names,
                parameters_accession_numbers,
                parameters_source_refs,
                component_names,
                component_types,
                component_types_accession_numbers,
                component_types_source_refs
            ]
        study_protocols_df = study_protocols_df.set_index('Study Protocol Name').T
        fp.write('STUDY PROTOCOLS\n')
        study_protocols_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                  index_label='Study Protocol Name')

        # Write STUDY CONTACTS section
        study_contacts_df = _build_contacts_section_df(prefix='Study', contacts=study.contacts)
        fp.write('STUDY CONTACTS\n')
        study_contacts_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                 index_label='Study Person Last Name')
    if skip_dump_tables:
        pass
    else:
        write_study_table_files(investigation, output_path)
        write_assay_table_files(
            investigation, output_path, write_factor_values_in_assay_table)

    fp.close()
    return investigation


def _get_start_end_nodes(G):
    start_nodes = list()
    end_nodes = list()
    for process in [n for n in G.nodes() if isinstance(n, Process)]:
        if process.prev_process is None:
            for material in [m for m in process.inputs if not isinstance(m, DataFile)]:
                start_nodes.append(material)
        outputs_no_data = [m for m in process.outputs if not isinstance(m, DataFile)]
        if process.next_process is None:
            if len(outputs_no_data) == 0:
                end_nodes.append(process)
            else:
                for material in outputs_no_data:
                    end_nodes.append(material)
    return start_nodes, end_nodes


def _longest_path_and_attrs(paths):
    longest = (0, None)
    for path in paths:
        length = len(path)
        for n in path:
            if isinstance(n, Source):
                length += len(n.characteristics)
            elif isinstance(n, Sample):
                length += (len(n.characteristics) + len(n.factor_values))
            elif isinstance(n, Material):
                length += (len(n.characteristics))
            elif isinstance(n, Process):
                length += len([o for o in n.outputs if isinstance(o, DataFile)])
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


def _all_end_to_end_paths(G, start_nodes):  # we know graphs start with Source or Sample and end with Process
    paths = []
    num_start_nodes = len(start_nodes)
    message = 'Calculating for paths for {} start nodes: '.format(num_start_nodes)
    if isinstance(start_nodes[0], Source):
        message = 'Calculating for paths for {} sources: '.format(num_start_nodes)
    elif isinstance(start_nodes[0], Sample):
        message = 'Calculating for paths for {} samples: '.format(num_start_nodes)
    if isa_logging.show_pbars:
        pbar = ProgressBar(min_value=0, max_value=num_start_nodes, widgets=[message,
                                                                            SimpleProgress(),
                                                                            Bar(left=" |", right="| "), ETA()]).start()
    else:
        pbar = lambda x: x
    for start in pbar(start_nodes):
        # Find ends
        if isinstance(start, Source):  # only look for Sample ends if start is a Source
            for end in [x for x in nx.algorithms.descendants(G, start) if
                        isinstance(x, Sample) and len(G.out_edges(x)) == 0]:
                paths += list(nx.algorithms.all_simple_paths(G, start, end))
        elif isinstance(start, Sample):  # only look for Process ends if start is a Sample
            for end in [x for x in nx.algorithms.descendants(G, start) if
                        isinstance(x, Process) and x.next_process is None]:
                paths += list(nx.algorithms.all_simple_paths(G, start, end))
    log.info("Found {} paths!".format(len(paths)))
    if len(paths) == 0:
        log.debug([x.name for x in start_nodes])
    return paths


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
        protrefcount = 0
        protnames = dict()

        flatten = lambda l: [item for sublist in l for item in sublist]
        columns = []

        # start_nodes, end_nodes = _get_start_end_nodes(study_obj.graph)
        paths = _all_end_to_end_paths(study_obj.graph, [x for x in study_obj.graph.nodes() if isinstance(x, Source)])
        sample_in_path_count = 0
        for node in _longest_path_and_attrs(paths):
            if isinstance(node, Source):
                olabel = "Source Name"
                columns.append(olabel)
                columns += flatten(
                    map(lambda x: get_characteristic_columns(olabel, x),
                        node.characteristics))
                columns += flatten(
                    map(lambda x: get_comment_column(olabel, x), node.comments))
            elif isinstance(node, Process):
                olabel = "Protocol REF.{}".format(node.executes_protocol.name)
                columns.append(olabel)
                if node.executes_protocol.name not in protnames.keys():
                    protnames[node.executes_protocol.name] = protrefcount
                    protrefcount += 1
                columns += flatten(map(lambda x: get_pv_columns(olabel, x),
                                       node.parameter_values))
                if node.date is not None:
                    columns.append(olabel + ".Date")
                if node.performer is not None:
                    columns.append(olabel + ".Performer")
                columns += flatten(
                    map(lambda x: get_comment_column(olabel, x), node.comments))

            elif isinstance(node, Sample):
                olabel = "Sample Name.{}".format(sample_in_path_count)
                columns.append(olabel)
                sample_in_path_count += 1
                columns += flatten(
                    map(lambda x: get_characteristic_columns(olabel, x),
                        node.characteristics))
                columns += flatten(
                    map(lambda x: get_comment_column(olabel, x), node.comments))
                columns += flatten(map(lambda x: get_fv_columns(olabel, x),
                                       node.factor_values))

        omap = get_object_column_map(columns, columns)
        # load into dictionary
        df_dict = dict(map(lambda k: (k, []), flatten(omap)))
        if isa_logging.show_pbars:
            pbar = ProgressBar(min_value=0, max_value=len(paths), widgets=['Writing {} paths: '.format(len(paths)),
                                                                           SimpleProgress(),
                                                                           Bar(left=" |", right="| "), ETA()]).start()
        else:
            pbar = lambda x: x
        for path in pbar(paths):
            for k in df_dict.keys():  # add a row per path
                df_dict[k].extend([""])

            sample_in_path_count = 0
            for node in path:
                if isinstance(node, Source):
                    olabel = "Source Name"
                    df_dict[olabel][-1] = node.name
                    for c in node.characteristics:
                        clabel = "{0}.Characteristics[{1}]".format(olabel, c.category.term)
                        write_value_columns(df_dict, clabel, c)
                    for co in node.comments:
                        colabel = "{0}.Comment[{1}]".format(olabel, co.name)
                        df_dict[colabel][-1] = co.value

                elif isinstance(node, Process):
                    olabel = "Protocol REF.{}".format(node.executes_protocol.name)
                    df_dict[olabel][-1] = node.executes_protocol.name
                    for pv in node.parameter_values:
                        pvlabel = "{0}.Parameter Value[{1}]".format(olabel, pv.category.parameter_name.term)
                        write_value_columns(df_dict, pvlabel, pv)
                    if node.date is not None:
                        df_dict[olabel + ".Date"][-1] = node.date
                    if node.performer is not None:
                        df_dict[olabel + ".Performer"][-1] = node.performer
                    for co in node.comments:
                        colabel = "{0}.Comment[{1}]".format(olabel, co.name)
                        df_dict[colabel][-1] = co.value

                elif isinstance(node, Sample):
                    olabel = "Sample Name.{}".format(sample_in_path_count)
                    sample_in_path_count += 1
                    df_dict[olabel][-1] = node.name
                    for c in node.characteristics:
                        clabel = "{0}.Characteristics[{1}]".format(olabel, c.category.term)
                        write_value_columns(df_dict, clabel, c)
                    for co in node.comments:
                        colabel = "{0}.Comment[{1}]".format(olabel, co.name)
                        df_dict[colabel][-1] = co.value
                    for fv in node.factor_values:
                        fvlabel = "{0}.Factor Value[{1}]".format(olabel, fv.factor_name.name)
                        write_value_columns(df_dict, fvlabel, fv)
        if isinstance(pbar, ProgressBar):  pbar.finish()

        DF = pd.DataFrame(columns=columns)
        DF = DF.from_dict(data=df_dict)
        DF = DF[columns]  # reorder columns
        DF = DF.sort_values(by=DF.columns[0], ascending=True)  # arbitrary sort on column 0

        for dup_item in set([x for x in columns if columns.count(x) > 1]):
            for j, each in enumerate([i for i, x in enumerate(columns) if x == dup_item]):
                columns[each] = dup_item + str(j)

        DF.columns = columns  # reset columns after checking for dups

        for i, col in enumerate(columns):
            if "Comment[" in col:
                columns[i] = col[col.rindex(".") + 1:]
            elif col.endswith("Term Source REF"):
                columns[i] = "Term Source REF"
            elif col.endswith("Term Accession Number"):
                columns[i] = "Term Accession Number"
            elif col.endswith("Unit"):
                columns[i] = "Unit"
            elif "Characteristics[" in col:
                if "material type" in col.lower():
                    columns[i] = "Material Type"
                else:
                    columns[i] = col[col.rindex(".") + 1:]
            elif "Factor Value[" in col:
                columns[i] = col[col.rindex(".") + 1:]
            elif "Parameter Value[" in col:
                columns[i] = col[col.rindex(".") + 1:]
            elif col.endswith("Date"):
                columns[i] = "Date"
            elif col.endswith("Performer"):
                columns[i] = "Performer"
            elif "Protocol REF" in col:
                columns[i] = "Protocol REF"
            elif col.startswith("Sample Name."):
                columns[i] = "Sample Name"

        log.info("Rendered {} paths".format(len(DF.index)))

        DF_no_dups = DF.drop_duplicates()
        if len(DF.index) > len(DF_no_dups.index):
            log.info("Dropping duplicates...")
            DF = DF_no_dups

        log.info("Writing {} rows".format(len(DF.index)))
        # reset columns, replace nan with empty string, drop empty columns
        DF.columns = columns
        DF = DF.replace('', np.nan)
        DF = DF.dropna(axis=1, how='all')

        with open(os.path.join(output_dir, study_obj.filename), 'w') as out_fp:
            DF.to_csv(path_or_buf=out_fp, index=False, sep='\t', encoding='utf-8')


def write_assay_table_files(inv_obj, output_dir, write_factor_values=False):
    """
        Writes out assay table files according to pattern defined by

        Sample Name,
        Protocol Ref: 'sample collection', [ ParameterValue[], ... ],
        Material Name, [ Characteristics[], ... ]
        [ FactorValue[], ... ]


    """

    if not isinstance(inv_obj, Investigation):
        raise NotImplementedError
    for study_obj in inv_obj.studies:
        for assay_obj in study_obj.assays:
            if assay_obj.graph is None: break
            protrefcount = 0
            protnames = dict()

            flatten = lambda l: [item for sublist in l for item in sublist]
            columns = []

            # start_nodes, end_nodes = _get_start_end_nodes(assay_obj.graph)
            paths = _all_end_to_end_paths(assay_obj.graph, [x for x in assay_obj.graph.nodes() if isinstance(x, Sample)])
            if len(paths) == 0:
                log.info("No paths found, skipping writing assay file")
                continue
            if _longest_path_and_attrs(paths) is None:
                raise IOError("Could not find any valid end-to-end paths in assay graph")
            for node in _longest_path_and_attrs(paths):
                if isinstance(node, Sample):
                    olabel = "Sample Name"
                    columns.append(olabel)
                    columns += flatten(
                        map(lambda x: get_comment_column(olabel, x),
                            node.comments))
                    if write_factor_values:
                        columns += flatten(
                            map(lambda x: get_fv_columns(olabel, x),
                                node.factor_values))

                elif isinstance(node, Process):
                    olabel = "Protocol REF.{}".format(
                        node.executes_protocol.name)
                    columns.append(olabel)
                    if node.executes_protocol.name not in protnames.keys():
                        protnames[node.executes_protocol.name] = protrefcount
                        protrefcount += 1
                    columns += flatten(map(lambda x: get_pv_columns(olabel, x),
                                           node.parameter_values))
                    oname_label = None
                    if node.executes_protocol.protocol_type:
                        if node.executes_protocol.protocol_type.term == "nucleic acid sequencing":
                            oname_label = "Assay Name"
                        elif node.executes_protocol.protocol_type.term == "data collection":
                            oname_label = "Scan Name"
                        elif node.executes_protocol.protocol_type.term == "mass spectrometry":
                            oname_label = "MS Assay Name"
                        elif node.executes_protocol.protocol_type.term == "data transformation":
                            oname_label = "Data Transformation Name"
                        elif node.executes_protocol.protocol_type.term == "sequence analysis data transformation":
                            oname_label = "Normalization Name"
                        elif node.executes_protocol.protocol_type.term == "normalization":
                            oname_label = "Normalization Name"
                        if node.executes_protocol.protocol_type.term == "unknown protocol":
                            oname_label = "Unknown Protocol Name"
                        if oname_label is not None:
                            columns.append(oname_label)
                        elif node.executes_protocol.protocol_type.term == "nucleic acid hybridization":
                            columns.extend(["Hybridization Assay Name", "Array Design REF"])
                    if node.date is not None:
                        columns.append(olabel + ".Date")
                    if node.performer is not None:
                        columns.append(olabel + ".Performer")
                    columns += flatten(
                        map(lambda x: get_comment_column(olabel, x),
                            node.comments))
                    for output in [x for x in node.outputs if
                                   isinstance(x, DataFile)]:
                        columns.append(output.label)
                        # columns += flatten(
                        #     map(lambda x: get_comment_column(output.label, x),
                        #         output.comments))

                elif isinstance(node, Material):
                    olabel = node.type
                    columns.append(olabel)
                    columns += flatten(
                        map(lambda x: get_characteristic_columns(olabel, x),
                            node.characteristics))
                    columns += flatten(
                        map(lambda x: get_comment_column(olabel, x),
                            node.comments))

                elif isinstance(node, DataFile):
                    pass  # handled in process

            omap = get_object_column_map(columns, columns)

            # load into dictionary
            df_dict = dict(map(lambda k: (k, []), flatten(omap)))

            if isa_logging.show_pbars:
                pbar = ProgressBar(min_value=0, max_value=len(paths), widgets=['Writing {} paths: '.format(len(paths)),
                                                                               SimpleProgress(),
                                                                               Bar(left=" |", right="| "), ETA()]).start()
            else:
                pbar = lambda x: x
            for path in pbar(paths):
                for k in df_dict.keys():  # add a row per path
                    df_dict[k].extend([""])

                for node in path:

                    if isinstance(node, Process):
                        olabel = "Protocol REF.{}".format(node.executes_protocol.name)
                        df_dict[olabel][-1] = node.executes_protocol.name
                        oname_label = None
                        if node.executes_protocol.protocol_type:
                            if node.executes_protocol.protocol_type.term == "nucleic acid sequencing":
                                oname_label = "Assay Name"
                            elif node.executes_protocol.protocol_type.term == "data collection":
                                oname_label = "Scan Name"
                            elif node.executes_protocol.protocol_type.term == "mass spectrometry":
                                oname_label = "MS Assay Name"
                            elif node.executes_protocol.protocol_type.term == "data transformation":
                                oname_label = "Data Transformation Name"
                            elif node.executes_protocol.protocol_type.term == "sequence analysis data transformation":
                                oname_label = "Normalization Name"
                            elif node.executes_protocol.protocol_type.term == "normalization":
                                oname_label = "Normalization Name"
                            if node.executes_protocol.protocol_type.term == "unknown protocol":
                                oname_label = "Unknown Protocol Name"
                            if oname_label is not None:
                                df_dict[oname_label][-1] = node.name
                            elif node.executes_protocol.protocol_type.term == "nucleic acid hybridization":
                                df_dict["Hybridization Assay Name"][-1] = node.name
                                df_dict["Array Design REF"][-1] = node.array_design_ref
                        if node.date is not None:
                            df_dict[olabel + ".Date"][-1] = node.date
                        if node.performer is not None:
                            df_dict[olabel + ".Performer"][-1] = node.performer
                        for pv in node.parameter_values:
                            pvlabel = "{0}.Parameter Value[{1}]".format(olabel, pv.category.parameter_name.term)
                            write_value_columns(df_dict, pvlabel, pv)
                        for co in node.comments:
                            colabel = "{0}.Comment[{1}]".format(olabel, co.name)
                            df_dict[colabel][-1] = co.value
                        for output in [x for x in node.outputs if isinstance(x, DataFile)]:
                            olabel = output.label
                            df_dict[olabel][-1] = output.filename
                            # for co in output.comments:
                            #     colabel = "{0}.Comment[{1}]".format(olabel, co.name)
                            #     df_dict[colabel][-1] = co.value

                    elif isinstance(node, Sample):
                        olabel = "Sample Name"
                        df_dict[olabel][-1] = node.name
                        for co in node.comments:
                            colabel = "{0}.Comment[{1}]".format(olabel, co.name)
                            df_dict[colabel][-1] = co.value
                        if write_factor_values:
                            for fv in node.factor_values:
                                fvlabel = "{0}.Factor Value[{1}]".format(
                                    olabel, fv.factor_name.name)
                                write_value_columns(df_dict, fvlabel, fv)

                    elif isinstance(node, Material):
                        olabel = node.type
                        df_dict[olabel][-1] = node.name
                        for c in node.characteristics:
                            clabel = "{0}.Characteristics[{1}]".format(olabel, c.category.term)
                            write_value_columns(df_dict, clabel, c)
                        for co in node.comments:
                            colabel = "{0}.Comment[{1}]".format(olabel, co.name)
                            df_dict[colabel][-1] = co.value

                    elif isinstance(node, DataFile):
                        pass  # handled in process

            if isinstance(pbar, ProgressBar):  pbar.finish()

            DF = pd.DataFrame(columns=columns)
            DF = DF.from_dict(data=df_dict)
            DF = DF[columns]  # reorder columns
            DF = DF.sort_values(by=DF.columns[0], ascending=True)  # arbitrary sort on column 0

            for dup_item in set([x for x in columns if columns.count(x) > 1]):
                for j, each in enumerate([i for i, x in enumerate(columns) if x == dup_item]):
                    columns[each] = ".".join([dup_item, str(j)])

            DF.columns = columns

            for i, col in enumerate(columns):
                if col.endswith("Term Source REF"):
                    columns[i] = "Term Source REF"
                elif col.endswith("Term Accession Number"):
                    columns[i] = "Term Accession Number"
                elif col.endswith("Unit"):
                    columns[i] = "Unit"
                elif "Characteristics[" in col:
                    if "material type" in col.lower():
                        columns[i] = "Material Type"
                    elif "label" in col.lower():
                        columns[i] = "Label"
                    else:
                        columns[i] = col[col.rindex(".") + 1:]
                elif "Factor Value[" in col:
                    columns[i] = col[col.rindex(".") + 1:]
                elif "Parameter Value[" in col:
                    columns[i] = col[col.rindex(".") + 1:]
                elif col.endswith("Date"):
                    columns[i] = "Date"
                elif col.endswith("Performer"):
                    columns[i] = "Performer"
                elif "Comment[" in col:
                    columns[i] = col[col.rindex(".") + 1:]
                elif "Protocol REF" in col:
                    columns[i] = "Protocol REF"
                elif "." in col:
                        columns[i] = col[:col.rindex(".")]

            log.info("Rendered {} paths".format(len(DF.index)))
            if len(DF.index) > 1:
                if len(DF.index) > len(DF.drop_duplicates().index):
                    log.debug("Dropping duplicates...")
                    DF = DF.drop_duplicates()

            log.info("Writing {} rows".format(len(DF.index)))
            # reset columns, replace nan with empty string, drop empty columns
            DF.columns = columns
            DF = DF.replace('', np.nan)
            DF = DF.dropna(axis=1, how='all')

            with open(os.path.join(output_dir, assay_obj.filename), 'w') as out_fp:
                DF.to_csv(path_or_buf=out_fp, index=False, sep='\t', encoding='utf-8')


def get_value_columns(label, x):
    if isinstance(x.value, (int, float)) and x.unit:
        if isinstance(x.unit, OntologyAnnotation):
            return map(lambda x: "{0}.{1}".format(label, x),
                       ["Unit", "Unit.Term Source REF", "Unit.Term Accession Number"])
        else:
            return ["{0}.Unit".format(label)]
    elif isinstance(x.value, OntologyAnnotation):
        return map(lambda x: "{0}.{1}".format(label, x), ["Term Source REF", "Term Accession Number"])
    else:
        return []


def get_characteristic_columns(label, c):
    columns = ["{0}.Characteristics[{1}]".format(label, c.category.term)]
    columns.extend(get_value_columns(columns[0], c))
    return columns


def get_fv_columns(label, fv):
    columns = ["{0}.Factor Value[{1}]".format(label, fv.factor_name.name)]
    columns.extend(get_value_columns(columns[0], fv))
    return columns


def get_comment_column(label, c):
    columns = ["{0}.Comment[{1}]".format(label, c.name)]
    return columns


def write_value_columns(df_dict, label, x):
    if isinstance(x.value, (int, float)) and x.unit:
        if isinstance(x.unit, OntologyAnnotation):
            df_dict[label][-1] = x.value
            df_dict[label + ".Unit"][-1] = x.unit.term
            df_dict[label + ".Unit.Term Source REF"][-1] = x.unit.term_source.name if x.unit.term_source else ""
            df_dict[label + ".Unit.Term Accession Number"][-1] = x.unit.term_accession
        else:
            df_dict[label][-1] = x.value
            df_dict[label + ".Unit"][-1] = x.unit
    elif isinstance(x.value, OntologyAnnotation):
        df_dict[label][-1] = x.value.term
        df_dict[label + ".Term Source REF"][-1] = x.value.term_source.name if x.value.term_source else ""
        df_dict[label + ".Term Accession Number"][-1] = x.value.term_accession
    else:
        df_dict[label][-1] = x.value


def get_pv_columns(label, pv):
    columns = None
    try:
        columns = ["{0}.Parameter Value[{1}]".format(label, pv.category.parameter_name.term)]
    except AttributeError:
        log.fatal(label, pv)
    columns.extend(get_value_columns(columns[0], pv))
    return columns


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
        df = pd.read_csv(f, names=range(0, 128), sep='\t', engine='python', encoding='utf-8',
                         comment='#').dropna(axis=1, how='all')
        df = df.T
        df.replace(np.nan, '', regex=True, inplace=True)  # Strip out the nan entries
        df.reset_index(inplace=True)  # Reset index so it is accessible as column
        df.columns = df.iloc[0]  # If all was OK, promote this row to the column headers
        df = df.reindex(df.index.drop(0))  # Reindex the DataFrame
        return df

    memf = io.StringIO()
    while True:
        line = fp.readline()
        if not line:
            break
        if not line.lstrip().startswith('#'):
            memf.write(line)
    memf.seek(0)

    df_dict = dict()

    # Read in investigation file into DataFrames first
    df_dict['ontology_sources'] = _build_section_df(_read_tab_section(
        f=memf,
        sec_key='ONTOLOGY SOURCE REFERENCE',
        next_sec_key='INVESTIGATION'
    ))
    # assert({'Term Source Name', 'Term Source File', 'Term Source Version', 'Term Source Description'}
    #        .issubset(set(ontology_sources_df.columns.values)))  # Check required labels are present
    df_dict['investigation'] = _build_section_df(_read_tab_section(
        f=memf,
        sec_key='INVESTIGATION',
        next_sec_key='INVESTIGATION PUBLICATIONS'
    ))
    df_dict['i_publications'] = _build_section_df(_read_tab_section(
        f=memf,
        sec_key='INVESTIGATION PUBLICATIONS',
        next_sec_key='INVESTIGATION CONTACTS'
    ))
    df_dict['i_contacts'] = _build_section_df(_read_tab_section(
        f=memf,
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
    while _peek(memf):  # Iterate through STUDY blocks until end of file
        df_dict['studies'].append(_build_section_df(_read_tab_section(
            f=memf,
            sec_key='STUDY',
            next_sec_key='STUDY DESIGN DESCRIPTORS'
        )))
        df_dict['s_design_descriptors'] .append(_build_section_df(_read_tab_section(
            f=memf,
            sec_key='STUDY DESIGN DESCRIPTORS',
            next_sec_key='STUDY PUBLICATIONS'
        )))
        df_dict['s_publications'].append(_build_section_df(_read_tab_section(
            f=memf,
            sec_key='STUDY PUBLICATIONS',
            next_sec_key='STUDY FACTORS'
        )))
        df_dict['s_factors'].append(_build_section_df(_read_tab_section(
            f=memf,
            sec_key='STUDY FACTORS',
            next_sec_key='STUDY ASSAYS'
        )))
        df_dict['s_assays'].append(_build_section_df(_read_tab_section(
            f=memf,
            sec_key='STUDY ASSAYS',
            next_sec_key='STUDY PROTOCOLS'
        )))
        df_dict['s_protocols'].append(_build_section_df(_read_tab_section(
            f=memf,
            sec_key='STUDY PROTOCOLS',
            next_sec_key='STUDY CONTACTS'
        )))
        df_dict['s_contacts'].append(_build_section_df(_read_tab_section(
            f=memf,
            sec_key='STUDY CONTACTS',
            next_sec_key='STUDY'
        )))
    return df_dict


def check_utf8(fp):
    """Used for rule 0010"""
    import chardet
    with open(fp.name, 'rb') as fp:
        charset = chardet.detect(fp.read())
        if charset['encoding'] is not 'UTF-8' and charset['encoding'] is not 'ascii':
            validator_warnings.append({
                "message": "File should be UTF8 encoding",
                "supplemental": "Encoding is '{0}' with confidence {1}".format(charset['encoding'], charset['confidence']),
                "code": 10
            })
            log.warning("File should be UTF-8 encoding but found it is '{0}' encoding with {1} confidence"
                        .format(charset['encoding'], charset['confidence']))
            raise SystemError()


def load_investigation(fp):
    """Used for rules 0005"""

    def check_labels(section, labels_expected, df):
        labels_found = set([x for x in df.columns if isinstance(x, str)])

        if not labels_expected.issubset(labels_found):
            missing_labels = labels_expected - labels_found
            log.fatal("(F) In {} section, expected labels {} not found in {}"
                      .format(section, missing_labels, labels_found))
        if len(labels_found - labels_expected) > 0:
            # check extra labels, i.e. make sure they're all comments
            extra_labels = labels_found - labels_expected
            for label in extra_labels:
                if _RX_COMMENT.match(label) is None:
                    log.fatal("(F) In {} section, label {} is not allowed".format(section, label))
                    validator_errors.append({
                        "message": "Invalid label found in investigation file",
                        "supplemental": "In {} section, label {} is not allowed".format(section, label),
                        "code": 5
                    })
                elif len(_RX_COMMENT.findall(label)) == 0:
                    log.warning("(W) In {} section, label {} is missing a name".format(section, label))
                    validator_warnings.append({
                        "message": "Missing name in Comment[] label",
                        "supplemental": "In {} section, label {} is missing a name".format(section, label),
                        "code": 4014
                    })

    df_dict = read_investigation_file(fp)  # Read in investigation file into DataFrames first
    log.info("Loading ONTOLOGY SOURCE REFERENCE section")
    labels_expected = {'Term Source Name', 'Term Source File', 'Term Source Version', 'Term Source Description'}
    check_labels('ONTOLOGY SOURCE REFERENCE', labels_expected, df_dict['ontology_sources'])

    log.info("Loading INVESTIGATION section")
    labels_expected = {'Investigation Identifier', 'Investigation Title', 'Investigation Description',
                       'Investigation Submission Date', 'Investigation Public Release Date'}
    check_labels('INVESTIGATION', labels_expected, df_dict['investigation'])

    log.info("Loading INVESTIGATION PUBLICATIONS section")
    labels_expected = {'Investigation PubMed ID', 'Investigation Publication DOI',
                       'Investigation Publication Author List', 'Investigation Publication Title',
                       'Investigation Publication Status', 'Investigation Publication Status Term Accession Number',
                       'Investigation Publication Status Term Source REF'}
    check_labels('INVESTIGATION PUBLICATIONS', labels_expected, df_dict['i_publications'])

    log.info("Loading INVESTIGATION CONTACTS section")
    labels_expected = {'Investigation Person Last Name', 'Investigation Person First Name',
                       'Investigation Person Mid Initials', 'Investigation Person Email',
                       'Investigation Person Phone', 'Investigation Person Fax',
                       'Investigation Person Address', 'Investigation Person Affiliation',
                       'Investigation Person Roles', 'Investigation Person Roles',
                       'Investigation Person Roles Term Accession Number',
                       'Investigation Person Roles Term Source REF'}
    check_labels('INVESTIGATION CONTACTS', labels_expected, df_dict['i_contacts'])
    for i in range(0, len(df_dict['studies'])):
        log.info("Loading STUDY section")
        labels_expected = {'Study Identifier', 'Study Title', 'Study Description',
                           'Study Submission Date', 'Study Public Release Date',
                           'Study File Name'}
        check_labels('STUDY', labels_expected, df_dict['studies'][i])

        log.info("Loading STUDY DESIGN DESCRIPTORS section")
        labels_expected = {'Study Design Type', 'Study Design Type Term Accession Number',
                           'Study Design Type Term Source REF'}
        check_labels('STUDY DESIGN DESCRIPTORS', labels_expected,
                     df_dict['s_design_descriptors'][i])

        log.info("Loading STUDY PUBLICATIONS section")
        labels_expected = {'Study PubMed ID', 'Study Publication DOI',
                           'Study Publication Author List', 'Study Publication Title',
                           'Study Publication Status',
                           'Study Publication Status Term Accession Number',
                           'Study Publication Status Term Source REF'}
        check_labels('STUDY PUBLICATIONS', labels_expected,
                     df_dict['s_publications'][i])

        log.info("Loading STUDY FACTORS section")
        labels_expected = {'Study Factor Name', 'Study Factor Type', 'Study Factor Type Term Accession Number',
                           'Study Factor Type Term Source REF'}
        check_labels('STUDY FACTORS', labels_expected, df_dict['s_factors'][i])

        log.info("Loading STUDY ASSAYS section")
        labels_expected = {'Study Assay Measurement Type', 'Study Assay Measurement Type Term Accession Number',
                           'Study Assay Measurement Type Term Source REF', 'Study Assay Technology Type',
                           'Study Assay Technology Type Term Accession Number',
                           'Study Assay Technology Type Term Source REF', 'Study Assay Technology Platform',
                           'Study Assay File Name'}
        check_labels('STUDY ASSAYS', labels_expected, df_dict['s_assays'][i])

        log.info("Loading STUDY PROTOCOLS section")
        labels_expected = {'Study Protocol Name', 'Study Protocol Type',
                           'Study Protocol Type Term Accession Number', 'Study Protocol Type Term Source REF',
                           'Study Protocol Description', 'Study Protocol URI', 'Study Protocol Version',
                           'Study Protocol Parameters Name', 'Study Protocol Parameters Name Term Accession Number',
                           'Study Protocol Parameters Name Term Source REF', 'Study Protocol Components Name',
                           'Study Protocol Components Type', 'Study Protocol Components Type Term Accession Number',
                           'Study Protocol Components Type Term Source REF'}
        check_labels('STUDY PROTOCOLS', labels_expected, df_dict['s_protocols'][i])

        log.info("Loading STUDY CONTACTS section")
        labels_expected = {'Study Person Last Name', 'Study Person First Name',
                           'Study Person Mid Initials', 'Study Person Email',
                           'Study Person Phone', 'Study Person Fax',
                           'Study Person Address', 'Study Person Affiliation',
                           'Study Person Roles', 'Study Person Roles',
                           'Study Person Roles Term Accession Number',
                           'Study Person Roles Term Source REF'}
        check_labels('STUDY CONTACTS', labels_expected,
                     df_dict['s_contacts'][i])
    return df_dict


def check_filenames_present(i_df):
    """Used for rule 3005"""
    for s_pos, study_df in enumerate(i_df['studies']):
        if study_df.iloc[0]['Study File Name'] is '':
            validator_warnings.append({
                "message": "Missing study file name",
                "supplemental": "STUDY.{}".format(s_pos),
                "code": 3005
            })
            log.warning("(W) A study filename is missing for STUDY.{}".format(s_pos))
        for a_pos, filename in enumerate(i_df['s_assays'][s_pos]['Study Assay File Name'].tolist()):
            if filename is '':
                validator_warnings.append({
                    "message": "Missing assay file name",
                    "supplemental": "STUDY.{}, STUDY ASSAY.{}".format(s_pos, a_pos),
                    "code": 3005
                })
                log.warning("(W) An assay filename is missing for STUDY ASSAY.{}".format(a_pos))


def check_date_formats(i_df):
    """Used for rule 3001"""
    def check_iso8601_date(date_str):
        if date_str is not '':
            try:
                iso8601.parse_date(date_str)
            except iso8601.ParseError:
                validator_warnings.append({
                    "message": "Date is not ISO8601 formatted",
                    "supplemental": "Found {} in date field".format(date_str),
                    "code": 3001
                })
                log.warning("(W) Date {} does not conform to ISO8601 format".format(date_str))
    import iso8601
    release_date_vals = i_df['investigation']['Investigation Public Release Date'].tolist()
    if len(release_date_vals) > 0:
        check_iso8601_date(release_date_vals[0])
    sub_date_values = i_df['investigation']['Investigation Submission Date'].tolist()
    if len(sub_date_values) > 0:
        check_iso8601_date(sub_date_values[0])
    for i, study_df in enumerate(i_df['studies']):
        release_date_vals = study_df['Study Public Release Date'].tolist()
        if len(release_date_vals) > 0:
            check_iso8601_date(release_date_vals[0])
        sub_date_values = study_df['Study Submission Date'].tolist()
        if len(sub_date_values) > 0:
            check_iso8601_date(sub_date_values[0])
        # for process in study['processSequence']:
        #     check_iso8601_date(process['date'])


def check_dois(i_df):
    """Used for rule 3002"""
    def check_doi(doi_str):
        if doi_str is not '':
            if not _RX_DOI.match(doi_str):
                validator_warnings.append({
                    "message": "DOI is not valid format",
                    "supplemental": "Found {} in DOI field".format(doi_str),
                    "code": 3002
                })
                log.warning("(W) DOI {} does not conform to DOI format".format(doi_str))
    for doi in i_df['i_publications']['Investigation Publication DOI'].tolist():
        check_doi(doi)
    for i, study_df in enumerate(i_df['s_publications']):
        for doi in study_df['Study Publication DOI'].tolist():
            check_doi(doi)


def check_pubmed_ids_format(i_df):
    """Used for rule 3003"""
    def check_pubmed_id(pubmed_id_str):
        if pubmed_id_str is not '':
            if (_RX_PMID.match(pubmed_id_str) is None) and (_RX_PMCID.match(pubmed_id_str) is None):
                validator_warnings.append({
                    "message": "PubMed ID is not valid format",
                    "supplemental": "Found PubMedID {}".format(pubmed_id_str),
                    "code": 3003
                })
                log.warning("(W) PubMed ID {} is not valid format".format(pubmed_id_str))
    for doi in i_df['i_publications']['Investigation PubMed ID'].tolist():
        check_pubmed_id(str(doi))
    for study_pubs_df in i_df['s_publications']:
        for doi in study_pubs_df['Study PubMed ID'].tolist():
            check_pubmed_id(str(doi))


def check_protocol_names(i_df):
    """Used for rule 1010"""
    for study_protocols_df in i_df['s_protocols']:
        for i, protocol_name in enumerate(study_protocols_df['Study Protocol Name'].tolist()):
            if protocol_name is '' or 'Unnamed: ' in protocol_name:  # DataFrames labels empty cells as 'Unnamed: n'
                validator_warnings.append({
                    "message": "Protocol missing name",
                    "supplemental": "pos={}".format(i),
                    "code": 1010
                })
                log.warning("(W) A Protocol at position {} is missing Protocol Name, so can't be referenced in "
                               "ISA-tab".format(i))


def check_protocol_parameter_names(i_df):
    """Used for rule 1011"""
    for study_protocols_df in i_df['s_protocols']:
        for i, protocol_parameters_names in enumerate(study_protocols_df['Study Protocol Parameters Name'].tolist()):
            if len(protocol_parameters_names.split(sep=';')) > 1:  # There's an empty cell if no protocols
                for protocol_parameter_name in protocol_parameters_names.split(sep=';'):
                    if protocol_parameter_name is '' or 'Unnamed: ' in protocol_parameter_name:
                        validator_warnings.append({
                            "message": "Protocol Parameter missing name",
                            "supplemental": "Protocol Parameter at pos={}".format(i),
                            "code": 1011
                        })
                        log.warning("(W) A Protocol Parameter used in Protocol position {} is missing a Name, so "
                                       "can't be referenced in ISA-tab".format(i))


def check_study_factor_names(i_df):
    """Used for rule 1012"""
    for study_protocols_df in i_df['s_factors']:
        for i, protocol_name in enumerate(study_protocols_df['Study Factor Name'].tolist()):
            if protocol_name is '' or 'Unnamed: ' in protocol_name:  # DataFrames labels empty cells as 'Unnamed: n'
                validator_warnings.append({
                    "message": "Study Factor missing name",
                    "supplemental": "Study Factor pos={}".format(i),
                    "code": 1012
                })
                log.warning("(W) A Study Factor at position {} is missing a name, so can't be referenced in ISA-tab"
                            .format(i))


def check_ontology_sources(i_df):
    """Used for rule 3008"""
    term_source_refs = []
    for i, ontology_source_name in enumerate(i_df['ontology_sources']['Term Source Name'].tolist()):
        if ontology_source_name is '' or 'Unnamed: ' in ontology_source_name:
            validator_warnings.append({
                "message": "Ontology Source missing name ref",
                "supplemental": "pos={}".format(i),
                "code": 3008
            })
            log.warning("(W) An Ontology Source Reference at position {} is missing Term Source Name, so can't be "
                           "referenced".format(i))
        else:
            term_source_refs.append(ontology_source_name)
    return term_source_refs


def check_table_files_read(i_df, dir_context):
    """Used for rules 0006 and 0008"""
    for i, study_df in enumerate(i_df['studies']):
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename is not '':
            try:
                with open(os.path.join(dir_context, study_filename), encoding='utf-8'):
                    pass
            except FileNotFoundError:
                validator_errors.append({
                    "message": "Missing study tab file(s)",
                    "supplemental": "Study File {} does not appear to exist".format(study_filename),
                    "code": 6
                })
                log.error("(E) Study File {} does not appear to exist".format(study_filename))
        for j, assay_filename in enumerate(i_df['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename is not '':
                try:
                    with open(os.path.join(dir_context, assay_filename), encoding='utf-8'):
                        pass
                except FileNotFoundError:
                    validator_errors.append({
                        "message": "Missing assay tab file(s)",
                        "supplemental": "Assay File {} does not appear to exist".format(assay_filename),
                        "code": 8
                    })
                    log.error("(E) Assay File {} does not appear to exist".format(assay_filename))


def check_table_files_load(i_df, dir_context):
    """Used for rules 0007 and 0009"""
    for i, study_df in enumerate(i_df['studies']):
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename is not '':
            try:
                with open(os.path.join(dir_context, study_filename), encoding='utf-8') as fp:
                    load_table_checks(fp)
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(i_df['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename is not '':
                try:
                    with open(os.path.join(dir_context, assay_filename), encoding='utf-8') as fp:
                        load_table_checks(fp)
                except FileNotFoundError:
                    pass


def check_samples_not_declared_in_study_used_in_assay(i_df, dir_context):
    for i, study_df in enumerate(i_df['studies']):
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename is not '':
            try:
                with open(os.path.join(dir_context, study_filename), encoding='utf-8') as s_fp:
                    study_df = load_table(s_fp)
                    study_samples = set(study_df['Sample Name'])
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(i_df['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename is not '':
                try:
                    with open(os.path.join(dir_context, assay_filename), encoding='utf-8') as a_fp:
                        assay_df = load_table(a_fp)
                        assay_samples = set(assay_df['Sample Name'])
                        if not assay_samples.issubset(study_samples):
                            log.error("(E) Some samples in an assay file {} are not declared in the study file {}: {}".format(assay_filename, study_filename, list(assay_samples - study_samples)))
                except FileNotFoundError:
                    pass


def check_protocol_usage(i_df, dir_context):
    """Used for rules 1007 and 1019"""
    for i, study_df in enumerate(i_df['studies']):
        protocols_declared = set(i_df['s_protocols'][i]['Study Protocol Name'].tolist())
        protocols_declared.add('')
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename is not '':
            try:
                protocol_refs_used = set()
                with open(os.path.join(dir_context, study_filename), encoding='utf-8') as s_fp:
                    study_df = load_table(s_fp)
                    for protocol_ref_col in [i for i in study_df.columns if i.startswith('Protocol REF')]:
                        protocol_refs_used = protocol_refs_used.union(study_df[protocol_ref_col])
                    protocol_refs_used = set([r for r in protocol_refs_used if pd.notnull(r)])
                    diff = list(protocol_refs_used - protocols_declared)
                    if len(diff) > 0:
                        validator_errors.append({
                            "message": "Missing Protocol declaration",
                            "supplemental": "protocols in study file {} are not declared in the investigation file: "
                                            "{}".format(study_filename, diff),
                            "code": 1007
                        })
                        log.error(
                            "(E) Some protocols used in a study file {} are not declared in the investigation file: "
                            "{}".format(study_filename, diff))
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(i_df['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename is not '':
                try:
                    protocol_refs_used = set()
                    with open(os.path.join(dir_context, assay_filename), encoding='utf-8') as a_fp:
                        assay_df = load_table(a_fp)
                        for protocol_ref_col in [i for i in assay_df.columns if i.startswith('Protocol REF')]:
                            protocol_refs_used = protocol_refs_used.union(assay_df[protocol_ref_col])
                        protocol_refs_used = set([r for r in protocol_refs_used if pd.notnull(r)])
                        diff = list(protocol_refs_used - protocols_declared)
                        if len(diff) > 0:
                            validator_errors.append({
                                "message": "Missing Protocol declaration",
                                "supplemental": "protocols in study file {} are not declared in the investigation file: "
                                                "{}".format(study_filename, diff),
                                "code": 1007
                            })
                            log.error("(E) Some protocols used in an assay file {} are not declared in the "
                                         "investigation file: {}".format(assay_filename, diff))
                except FileNotFoundError:
                    pass
        # now collect all protocols in all assays to compare to declared protocols
        protocol_refs_used = set()
        if study_filename is not '':
            try:
                with open(os.path.join(dir_context, study_filename), encoding='utf-8') as s_fp:
                    study_df = load_table(s_fp)
                    for protocol_ref_col in [i for i in study_df.columns if i.startswith('Protocol REF')]:
                        protocol_refs_used = protocol_refs_used.union(study_df[protocol_ref_col])
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(i_df['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename is not '':
                try:
                    with open(os.path.join(dir_context, assay_filename), encoding='utf-8') as a_fp:
                        assay_df = load_table(a_fp)
                        for protocol_ref_col in [i for i in assay_df.columns if i.startswith('Protocol REF')]:
                            protocol_refs_used = protocol_refs_used.union(assay_df[protocol_ref_col])
                except FileNotFoundError:
                    pass
        diff = protocols_declared - protocol_refs_used - {''}
        if len(diff) > 0:
            validator_warnings.append({
                "message": "Protocol declared but not used",
                "supplemental": "protocols declared in the file {} are not used in any assay file: "
                                "{}".format(study_filename, diff),
                "code": 1019
            })
            log.warning(
                "(W) Some protocols declared in the investigation file are not used neither in the study file {} nor in any related assay file: {}".format(
                    study_filename, list(diff)))


def load_table(fp):
    try:
        fp = strip_comments(fp)
        df = pd.read_csv(fp, dtype=str, sep='\t', encoding='utf-8').replace(np.nan, '')
    except UnicodeDecodeError:
        log.warning("Could not load file with UTF-8, trying ISO-8859-1")
        fp = strip_comments(fp)
        df = pd.read_csv(fp, dtype=str, sep='\t', encoding='latin1').replace(np.nan, '')
    labels = df.columns
    new_labels = []
    for label in labels:
        any_var_regex = re.compile('.*\[(.*?)\]')
        hits = any_var_regex.findall(label)
        if len(hits) > 0:
            val = hits[0].strip()
            if 'Comment' in label:
                new_label = 'Comment[{val}]'.format(val=val)
            elif 'Characteristics' in label:
                new_label = 'Characteristics[{val}]'.format(val=val)
            elif 'Parameter Value' in label:
                new_label = 'Parameter Value[{val}]'.format(val=val)
            elif 'Factor Value' in label:
                new_label = 'Factor Value[{val}]'.format(val=val)
            new_labels.append(new_label)
        else:
            new_labels.append(label)
    df.columns = new_labels
    return df


def load_table_checks(fp):

    df = load_table(fp)
    columns = df.columns
    for x, column in enumerate(columns):  # check if columns have valid labels
        if _RX_INDEXED_COL.match(column):
            column = column[:column.rfind('.')]
        if (column not in ['Source Name', 'Sample Name', 'Term Source REF', 'Protocol REF', 'Term Accession Number',
                           'Unit', 'Assay Name', 'Extract Name', 'Raw Data File', 'Material Type', 'MS Assay Name',
                           'Raw Spectral Data File', 'Labeled Extract Name', 'Label', 'Hybridization Assay Name',
                           'Array Design REF', 'Scan Name', 'Array Data File', 'Protein Assignment File',
                           'Peptide Assignment File', 'Post Translational Modification Assignment File',
                           'Data Transformation Name', 'Derived Spectral Data File', 'Normalization Name',
                           'Derived Array Data File', 'Image File', 'Metabolite Assignment File',
                           'Free Induction Decay File', 'Acquisition Parameter Data File']) and not _RX_CHARACTERISTICS.match(column) and not _RX_PARAMETER_VALUE.match(column) and not _RX_FACTOR_VALUE.match(column) and not _RX_COMMENT.match(column):
            log.error("Unrecognised column heading {} at column position {} in table file {}".format(column, x, os.path.basename(fp.name)))
        if _RX_COMMENT.match(column):
            if len(_RX_COMMENT.findall(column)) == 0:
                log.warning("(W) In file {}, label {} is missing a name".format(os.path.basename(fp.name), column))
                validator_warnings.append({
                    "message": "Missing name in Comment[] label",
                    "supplemental": "In file {}, label {} is missing a name".format(os.path.basename(fp.name), column),
                    "code": 4014
                })
        if _RX_CHARACTERISTICS.match(column):
            if len(_RX_CHARACTERISTICS.findall(column)) == 0:
                log.warning("(W) In file {}, label {} is missing a name".format(os.path.basename(fp.name), column))
                validator_warnings.append({
                    "message": "Missing name in Characteristics[] label",
                    "supplemental": "In file {}, label {} is missing a name".format(os.path.basename(fp.name), column),
                    "code": 4014
                })
        if _RX_PARAMETER_VALUE.match(column):
            if len(_RX_PARAMETER_VALUE.findall(column)) == 0:
                log.warning("(W) In file {}, label {} is missing a name".format(os.path.basename(fp.name), column))
                validator_warnings.append({
                    "message": "Missing name in Parameter Value[] label",
                    "supplemental": "In file {}, label {} is missing a name".format(os.path.basename(fp.name), column),
                    "code": 4014
                })
        if _RX_FACTOR_VALUE.match(column):
            if len(_RX_FACTOR_VALUE.findall(column)) == 0:
                log.warning("(W) In file {}, label {} is missing a name".format(os.path.basename(fp.name), column))
                validator_warnings.append({
                    "message": "Missing name in Factor Value[] label",
                    "supplemental": "In file {}, label {} is missing a name".format(os.path.basename(fp.name), column),
                    "code": 4014
                })
    norm_columns = list()
    for x, column in enumerate(columns):
        if _RX_INDEXED_COL.match(column):
            norm_columns.append(column[:column.rfind('.')])
        else:
            norm_columns.append(column)
    object_index = [i for i, x in enumerate(norm_columns) if x in ['Source Name', 'Sample Name', 'Protocol REF',
                                                              'Extract Name', 'Labeled Extract Name', 'Raw Data File',
                                                              'Raw Spectral Data File', 'Array Data File',
                                                              'Protein Assignment File', 'Peptide Assignment File',
                                                              'Post Translational Modification Assignment File',
                                                              'Derived Spectral Data File', 'Derived Array Data File']
                    or _RX_FACTOR_VALUE.match(x)]
    # this bit strips out the postfix .n that DataFrames adds to multiples of column labels
    object_columns_list = list()
    prev_i = object_index[0]
    for curr_i in object_index:  # collect each object's columns
        if prev_i == curr_i: pass  # skip if there's no diff, i.e. first one
        else: object_columns_list.append(norm_columns[prev_i:curr_i])
        prev_i = curr_i
    object_columns_list.append(norm_columns[prev_i:])  # finally collect last object's columns

    for object_columns in object_columns_list:
        prop_name = object_columns[0]
        if prop_name in ['Sample Name', 'Source Name']:
            for x, col in enumerate(object_columns[1:]):
                if col not in ['Term Source REF', 'Term Accession Number', 'Unit'] and not _RX_CHARACTERISTICS.match(col) and not _RX_FACTOR_VALUE.match(col) and not _RX_COMMENT.match(col):
                    log.error("(E) Expected only Characteristics, Factor Values or Comments following {} columns but found {} at offset {}".format(prop_name, col, x + 1))
        elif prop_name == 'Protocol REF':
            for x, col in enumerate(object_columns[1:]):
                if col not in ['Term Source REF', 'Term Accession Number', 'Unit', 'Assay Name',
                               'Hybridization Assay Name', 'Array Design REF', 'Scan Name'] and not _RX_PARAMETER_VALUE.match(col) and not _RX_COMMENT.match(col):
                    log.error("(E) Unexpected column heading following {} column. Found {} at offset {}".format(prop_name, col, x + 1))
        elif prop_name == 'Extract Name':
            if len(object_columns) > 1:
                log.error(
                    "Unexpected column heading(s) following {} column. Found {} at offset {}".format(prop_name, object_columns[1:], 2))
        elif prop_name == 'Labeled Extract Name':
            if len(object_columns) > 1:
                if object_columns[1] == 'Label':
                    for x, col in enumerate(object_columns[2:]):
                        if col not in ['Term Source REF', 'Term Accession Number']:
                            log.error("(E) Unexpected column heading following {} column. Found {} at offset {}".format(prop_name, col, x + 1))
                else:
                    log.error("(E) Unexpected column heading following {} column. Found {} at offset {}".format(prop_name, object_columns[1:], 2))
            else:
                log.error("Expected Label column after Labeled Extract Name but none found")
        elif prop_name in ['Raw Data File', 'Derived Spectral Data File', 'Derived Array Data File', 'Array Data File',
                           'Raw Spectral Data File', 'Protein Assignment File', 'Peptide Assignment File',
                           'Post Translational Modification Assignment File']:
            for x, col in enumerate(object_columns[1:]):
                if not _RX_COMMENT.match(col):
                    log.error("(E) Expected only Comments following {} columns but found {} at offset {}".format(prop_name, col, x + 1))
        elif _RX_FACTOR_VALUE.match(prop_name):
            for x, col in enumerate(object_columns[2:]):
                if col not in ['Term Source REF', 'Term Accession Number']:
                    log.error(
                        "(E) Unexpected column heading following {} column. Found {} at offset {}".format(prop_name,
                                                                                                      col, x + 1))
        else:
            log.info("Need to implement a rule for... " + prop_name)
            log.info(object_columns)
    return df


def check_study_factor_usage(i_df, dir_context):
    """Used for rules 1008 and 1021"""
    for i, study_df in enumerate(i_df['studies']):
        study_factors_declared = set(i_df['s_factors'][i]['Study Factor Name'].tolist())
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename is not '':
            try:
                study_factors_used = set()
                with open(os.path.join(dir_context, study_filename), encoding='utf-8') as s_fp:
                    study_df = load_table(s_fp)
                    study_factor_ref_cols = [i for i in study_df.columns if _RX_FACTOR_VALUE.match(i)]
                    for col in study_factor_ref_cols:
                        fv = _RX_FACTOR_VALUE.findall(col)
                        study_factors_used = study_factors_used.union(set(fv))
                    if not study_factors_used.issubset(study_factors_declared):
                        log.error(
                            "(E) Some factors used in an study file {} are not declared in the investigation file: {}".format(
                                study_filename, list(study_factors_used - study_factors_declared)))
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(i_df['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename is not '':
                try:
                    study_factors_used = set()
                    with open(os.path.join(dir_context, assay_filename), encoding='utf-8') as a_fp:
                        assay_df = load_table(a_fp)
                        study_factor_ref_cols = set([i for i in assay_df.columns if _RX_FACTOR_VALUE.match(i)])
                        for col in study_factor_ref_cols:
                            fv = _RX_FACTOR_VALUE.findall(col)
                            study_factors_used = study_factors_used.union(set(fv))
                        if not study_factors_used.issubset(study_factors_declared):
                            log.error(
                                "(E) Some factors used in an assay file {} are not declared in the investigation file: {}".format(
                                    assay_filename, list(study_factors_used - study_factors_declared)))
                except FileNotFoundError:
                    pass
        study_factors_used = set()
        if study_filename is not '':
            try:
                with open(os.path.join(dir_context, study_filename), encoding='utf-8') as s_fp:
                    study_df = load_table(s_fp)
                    study_factor_ref_cols = [i for i in study_df.columns if _RX_FACTOR_VALUE.match(i)]
                    for col in study_factor_ref_cols:
                        fv = _RX_FACTOR_VALUE.findall(col)
                        study_factors_used = study_factors_used.union(set(fv))
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(i_df['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename is not '':
                try:
                    with open(os.path.join(dir_context, assay_filename), encoding='utf-8') as a_fp:
                        assay_df = load_table(a_fp)
                        study_factor_ref_cols = set([i for i in assay_df.columns if _RX_FACTOR_VALUE.match(i)])
                        for col in study_factor_ref_cols:
                            fv = _RX_FACTOR_VALUE.findall(col)
                            study_factors_used = study_factors_used.union(set(fv))
                except FileNotFoundError:
                    pass
        if len(study_factors_declared - study_factors_used) > 0:
            log.warning(
                "(W) Some study factors declared in the investigation file are not used in any assay file: {}".format(
                    list(study_factors_declared - study_factors_used)))


def check_protocol_parameter_usage(i_df, dir_context):
    """Used for rules 1009 and 1020"""
    for i, study_df in enumerate(i_df['studies']):
        protocol_parameters_declared = set()
        protocol_parameters_per_protocol = set(i_df['s_protocols'][i]['Study Protocol Parameters Name'].tolist())
        for protocol_parameters in protocol_parameters_per_protocol:
            parameters_list = protocol_parameters.split(';')
            protocol_parameters_declared = protocol_parameters_declared.union(set(parameters_list))
        protocol_parameters_declared = protocol_parameters_declared - {''}  # empty string is not a valid protocol parameter
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename is not '':
            try:
                protocol_parameters_used = set()
                with open(os.path.join(dir_context, study_filename), encoding='utf-8') as s_fp:
                    study_df = load_table(s_fp)
                    parameter_value_cols = [i for i in study_df.columns if _RX_PARAMETER_VALUE.match(i)]
                    for col in parameter_value_cols:
                        pv = _RX_PARAMETER_VALUE.findall(col)
                        protocol_parameters_used = protocol_parameters_used.union(set(pv))
                    if not protocol_parameters_used.issubset(protocol_parameters_declared):
                        log.error(
                            "(E) Some protocol parameters referenced in an study file {} are not declared in the investigation file: {}".format(
                                study_filename, list(protocol_parameters_used - protocol_parameters_declared)))
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(i_df['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename is not '':
                try:
                    protocol_parameters_used = set()
                    with open(os.path.join(dir_context, assay_filename), encoding='utf-8') as a_fp:
                        assay_df = load_table(a_fp)
                        parameter_value_cols = [i for i in assay_df.columns if _RX_PARAMETER_VALUE.match(i)]
                        for col in parameter_value_cols:
                            pv = _RX_PARAMETER_VALUE.findall(col)
                            protocol_parameters_used = protocol_parameters_used.union(set(pv))
                        if not protocol_parameters_used.issubset(protocol_parameters_declared):
                            log.error(
                                "(E) Some protocol parameters referenced in an assay file {} are not declared in the investigation file: {}".format(
                                    assay_filename, list(protocol_parameters_used - protocol_parameters_declared)))
                except FileNotFoundError:
                    pass
        # now collect all protocol parameters in all assays to compare to declared protocol parameters
        protocol_parameters_used = set()
        if study_filename is not '':
            try:
                with open(os.path.join(dir_context, study_filename), encoding='utf-8') as s_fp:
                    study_df = load_table(s_fp)
                    parameter_value_cols = [i for i in study_df.columns if _RX_PARAMETER_VALUE.match(i)]
                    for col in parameter_value_cols:
                        pv = _RX_PARAMETER_VALUE.findall(col)
                        protocol_parameters_used = protocol_parameters_used.union(set(pv))
            except FileNotFoundError:
                pass
        for j, assay_filename in enumerate(i_df['s_assays'][i]['Study Assay File Name'].tolist()):
            if assay_filename is not '':
                try:
                    with open(os.path.join(dir_context, assay_filename), encoding='utf-8') as a_fp:
                        assay_df = load_table(a_fp)
                        parameter_value_cols = [i for i in assay_df.columns if _RX_PARAMETER_VALUE.match(i)]
                        for col in parameter_value_cols:
                            pv = _RX_PARAMETER_VALUE.findall(col)
                            protocol_parameters_used = protocol_parameters_used.union(set(pv))
                except FileNotFoundError:
                    pass
        if len(protocol_parameters_declared - protocol_parameters_used) > 0:
            log.warning(
                "(W) Some protocol parameters declared in the investigation file are not used in any assay file: {}".format(
                    list(protocol_parameters_declared - protocol_parameters_used)))


def get_ontology_source_refs(i_df):
    return i_df['ontology_sources']['Term Source Name'].tolist()


def check_term_source_refs_in_investigation(i_df):
    """Used for rules 3007 and 3009"""
    ontology_sources_list = get_ontology_source_refs(i_df)

    def check_study_term_sources_in_secton_field(section_label, pos, column_label):
        section_term_source_refs = [i for i in i_df[section_label][pos][column_label].tolist() if i != '']
        # this for loop deals with semicolon separated lists of term source refs
        section_term_source_refs_to_remove = list()
        for section_term_source_ref in section_term_source_refs:
            if ';' in section_term_source_ref:
                term_sources = [i for i in section_term_source_ref.split(';') if i != '']
                section_term_source_refs_to_remove.append(section_term_source_ref)
                section_term_source_refs.extend(term_sources)
        for section_term_source_ref_to_remove in section_term_source_refs_to_remove:
            section_term_source_refs.remove(section_term_source_ref_to_remove)
        diff = set(section_term_source_refs) - set(ontology_sources_list)
        if len(diff) > 0:
            validator_warnings.append({
                "message": "Missing Term Source",
                "supplemental": "Ontology sources missing {}".format(list(diff)),
                "code": 3009
            })
            log.warning("(W) In {} one or more of {} has not been declared in {}.{} section".format(
                column_label, section_term_source_refs, section_label, pos))

    i_publication_status_term_source_ref = [i for i in i_df['i_publications']['Investigation Publication Status Term Source REF'].tolist() if i != '']
    diff = set(i_publication_status_term_source_ref) - set(ontology_sources_list)
    if len(diff) > 0:
        validator_warnings.append({
            "message": "Missing Term Source",
            "supplemental": "Ontology sources missing {}".format(list(diff)),
            "code": 3009
        })
        log.warning("(W) Investigation Publication Status Term Source REF {} has not been declared in ONTOLOGY SOURCE "
                    "REFERENCE section".format(i_publication_status_term_source_ref))
    i_person_roles_term_source_ref = [i for i in i_df['i_contacts']['Investigation Person Roles Term Source REF'].tolist() if i != '']
    diff = set(i_person_roles_term_source_ref) - set(ontology_sources_list)
    if len(diff) > 0:
        validator_warnings.append({
            "message": "Missing Term Source",
            "supplemental": "Ontology sources missing {}".format(list(diff)),
            "code": 3009
        })
        log.warning("(W) Investigation Person Roles Term Source REF {} has not been declared in ONTOLOGY SOURCE "
                    "REFERENCE section".format(i_person_roles_term_source_ref))

    for i, study_df in enumerate(i_df['studies']):
        check_study_term_sources_in_secton_field('s_design_descriptors', i, 'Study Design Type Term Source REF')
        check_study_term_sources_in_secton_field('s_publications', i, 'Study Publication Status Term Source REF')
        check_study_term_sources_in_secton_field('s_assays', i, 'Study Assay Measurement Type Term Source REF')
        check_study_term_sources_in_secton_field('s_assays', i, 'Study Assay Technology Type Term Source REF')
        check_study_term_sources_in_secton_field('s_protocols', i, 'Study Protocol Type Term Source REF')
        check_study_term_sources_in_secton_field('s_protocols', i, 'Study Protocol Parameters Name Term Source REF')
        check_study_term_sources_in_secton_field('s_protocols', i, 'Study Protocol Components Type Term Source REF')
        check_study_term_sources_in_secton_field('s_contacts', i, 'Study Person Roles Term Source REF')


def check_term_source_refs_in_assay_tables(i_df, dir_context):
    """Used for rules 3007 and 3009"""
    import math
    ontology_sources_list = set(get_ontology_source_refs(i_df))
    for i, study_df in enumerate(i_df['studies']):
        study_filename = study_df.iloc[0]['Study File Name']
        if study_filename is not '':
            try:
                with open(os.path.join(dir_context, study_filename), encoding='utf-8') as s_fp:
                    df = load_table(s_fp)
                    columns = df.columns
                    object_index = [i for i, x in enumerate(columns) if x.startswith('Term Source REF')]
                    prev_i = object_index[0]
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
                                        validator_warnings.append({
                                            "message": "Missing Term Source",
                                            "supplemental": "Ontology sources missing {} at column position {} and row {} "
                                                            "in {} not declared in ontology "
                                                            "sources {}".format(row+1, object_index[x], y+1, study_filename,
                                                                                list(ontology_sources_list)),
                                            "code": 3009
                                        })
                                        log.warning("(W) Term Source REF {} at column position {} and row {} in {} not "
                                                    "declared in ontology sources {}".format(row+1, object_index[x], y+1,
                                                                                             study_filename,
                                                                                             list(ontology_sources_list)))
                                else:
                                    validator_warnings.append({
                                        "message": "Missing Term Source",
                                        "supplemental": "Ontology sources missing {} at column position {} and row {} "
                                                        "in {} not declared in ontology "
                                                        "sources {}".format(row + 1, object_index[x], y + 1, study_filename,
                                                                            list(ontology_sources_list)),
                                        "code": 3009
                                    })
                                    log.warning("(W) Term Source REF {} at column position {} and row {} in {} not in "
                                                "declared ontology sources {}"
                                                .format(row+1, object_index[x], y+1, study_filename,
                                                        list(ontology_sources_list)))
            except FileNotFoundError:
                pass
            for j, assay_filename in enumerate(i_df['s_assays'][i]['Study Assay File Name'].tolist()):
                if assay_filename is not '':
                    try:
                        with open(os.path.join(dir_context, assay_filename), encoding='utf-8') as a_fp:
                            df = load_table(a_fp)
                            columns = df.columns
                            object_index = [i for i, x in enumerate(columns) if x.startswith('Term Source REF')]
                            prev_i = object_index[0]
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
                                                validator_warnings.append({
                                                    "message": "Missing Term Source",
                                                    "supplemental": "Ontology sources missing {} at column position {} and "
                                                                    "row {} in {} not declared in ontology sources {}"
                                                        .format(row + 1, object_index[x], y + 1, study_filename,
                                                                list(ontology_sources_list)),
                                                    "code": 3009
                                                })
                                                log.warning("(W) Term Source REF {} at column position {} and row {} in {} "
                                                            "not declared in ontology sources {}"
                                                            .format(row+1, object_index[x], y+1, study_filename,
                                                                    list(ontology_sources_list)))
                                        else:
                                            validator_warnings.append({
                                                "message": "Missing Term Source",
                                                "supplemental": "Ontology sources missing {} at column position {} and row "
                                                                "{} in {} not declared in ontology sources {}"
                                                    .format(row + 1, object_index[x], y + 1, study_filename,
                                                            list(ontology_sources_list)),
                                                "code": 3009
                                            })
                                            log.warning("(W) Term Source REF {} at column position {} and row {} in {} not "
                                                        "in declared ontology sources {}"
                                                        .format(row+1, object_index[x], y+1, study_filename,
                                                                list(ontology_sources_list)))
                    except FileNotFoundError:
                        pass


def check_term_source_refs_usage(i_df, dir_context):
    check_term_source_refs_in_investigation(i_df)
    check_term_source_refs_in_assay_tables(i_df, dir_context)


def load_config(config_dir):
    """Rule 4001"""
    configs = None
    try:
        configs = isatab_configurator.load(config_dir)
    except FileNotFoundError:
        validator_errors.append({
            "message": "Configurations could not be loaded",
            "supplemental": "On loading {}".format(config_dir),
            "code": 4001
        })
        log.error("(E) FileNotFoundError on trying to load from {}".format(config_dir))
    if configs is None:
        validator_errors.append({
            "message": "Configurations could not be loaded",
            "supplemental": "On loading {}".format(config_dir),
            "code": 4001
        })
        log.error("(E) Could not load configurations from {}".format(config_dir))
    else:
        for k in configs.keys():
            log.info("Loaded table configuration '{}' for measurement and technology {}"
                     .format(str(configs[k].get_isatab_configuration()[0].table_name), str(k)))
    return configs


def check_measurement_technology_types(i_df, configs):
    """Rule 4002"""
    for i, assay_df in enumerate(i_df['s_assays']):
        measurement_types = assay_df['Study Assay Measurement Type'].tolist()
        technology_types = assay_df['Study Assay Technology Type'].tolist()
        if len(measurement_types) == len(technology_types):
            for x, measurement_type in enumerate(measurement_types):
                lowered_mt = measurement_types[x].lower()
                lowered_tt = technology_types[x].lower()
                if (lowered_mt, lowered_tt) not in configs.keys():
                    validator_errors.append({
                        "message": "Measurement/technology type invalid",
                        "supplemental": "Measurement {}/technology {}, STUDY ASSAY.{}"
                            .format(measurement_types[x], technology_types[x], i),
                        "code": 4002
                    })
                    log.error("(E) Could not load configuration for measurement type '{}' and technology type '{}' "
                                 "for STUDY ASSAY.{}'".format(measurement_types[x], technology_types[x], i))


def check_investigation_against_config(i_df, configs):

    def check_section_against_required_fields_one_value(section, required, i=0):
        fields_required = [i for i in section.columns if i in required]
        for col in fields_required:
            required_values = section[col]
            if len(required_values) > 0:
                for x, required_value in enumerate(required_values):
                    required_value = required_values.iloc[x]
                    if isinstance(required_value, float):
                        if math.isnan(required_value):
                            if i > 0:
                                validator_warnings.append({
                                    "message": "A required property is missing",
                                    "supplemental": "A property value in {}.{} of investigation file at column {} is "
                                                    "required".format(col, i + 1, x + 1),
                                    "code": 4003
                                })
                                log.warning(
                                    "(W) A property value in {}.{} of investigation file at column {} is required".format(
                                        col, i+1, x + 1))
                            else:
                                validator_warnings.append({
                                    "message": "A required property is missing",
                                    "supplemental": "A property value in {} of investigation file at column {} is "
                                                    "required".format(col, x + 1),
                                    "code": 4003
                                })
                                log.warning(
                                    "(W) A property value in {} of investigation file at column {} is required".format(
                                        col, x + 1))
                    else:
                        if required_value == '' or 'Unnamed: ' in required_value:
                            if i > 0:
                                validator_warnings.append({
                                    "message": "A required property is missing",
                                    "supplemental": "A property value in {}.{} of investigation file at column {} is "
                                                    "required".format(col, i+1, x + 1),
                                    "code": 4003
                                })
                                log.warning(
                                    "(W) A property value in {}.{} of investigation file at column {} is required".format(
                                        col, i+1, x + 1))
                            else:
                                validator_warnings.append({
                                    "message": "A required property is missing",
                                    "supplemental": "A property value in {} of investigation file at column {} is "
                                                    "required".format(col, x + 1),
                                    "code": 4003
                                })
                                log.warning(
                                    "(W) A property value in {} of investigation file at column {} is required".format(
                                        col, x + 1))

    required_fields = [i.header for i in configs[('[investigation]', '')].get_isatab_configuration()[0].get_field() if i.is_required]
    check_section_against_required_fields_one_value(i_df['investigation'], required_fields)
    check_section_against_required_fields_one_value(i_df['i_publications'], required_fields)
    check_section_against_required_fields_one_value(i_df['i_contacts'], required_fields)

    for x, study_df in enumerate(i_df['studies']):
        check_section_against_required_fields_one_value(i_df['studies'][x], required_fields, x)
        check_section_against_required_fields_one_value(i_df['s_design_descriptors'][x], required_fields, x)
        check_section_against_required_fields_one_value(i_df['s_publications'][x], required_fields, x)
        check_section_against_required_fields_one_value(i_df['s_factors'][x], required_fields, x)
        check_section_against_required_fields_one_value(i_df['s_assays'][x], required_fields, x)
        check_section_against_required_fields_one_value(i_df['s_protocols'][x], required_fields, x)
        check_section_against_required_fields_one_value(i_df['s_contacts'][x], required_fields, x)


def check_study_table_against_config(s_df, protocols_declared, config):
    # We are assuming the table load validation earlier passed

    # First check column order is correct against the configuration
    columns = s_df.columns
    object_index = [(x, i) for x, i in enumerate(columns) if i in ['Source Name', 'Sample Name',
                                                              'Extract Name', 'Labeled Extract Name', 'Raw Data File',
                                                              'Raw Spectral Data File', 'Array Data File',
                                                              'Protein Assignment File', 'Peptide Assignment File',
                                                              'Post Translational Modification Assignment File',
                                                              'Derived Spectral Data File',
                                                              'Derived Array Data File'] or 'Protocol REF' in i or
                    'Characteristics[' in i or 'Factor Value[' in i or 'Parameter Value[ in i']
    fields = [i.header for i in config.get_isatab_configuration()[0].get_field()]
    protocols = [(i.pos, i.protocol_type) for i in config.get_isatab_configuration()[0].get_protocol_field()]
    for protocol in protocols:
        fields.insert(protocol[0], 'Protocol REF')
    # strip out non-config columns
    object_index = [i for i in object_index if i[1] in fields]
    for x, object in enumerate(object_index):
        if fields[x] != object[1]:
            validator_warnings.append({
                "message": "The column order in assay table is not valid",
                "supplemental": "Unexpected heading found. Expected {} but found {} at column number {}"
                    .format(fields[x], object[1], object[0]),
                "code": 4005
            })
            log.warning("(W) Unexpected heading found. Expected {} but found {} at column number {}"
                        .format(fields[x], object[1], object[0]))

    # Second, check if Protocol REFs are of valid types
    for row in s_df['Protocol REF']:
        log.debug(row, protocols_declared[row] in [i[1] for i in protocols], [i[1] for i in protocols])
    # Third, check if required values are present


def check_assay_table_against_config(s_df, config):
    import itertools
    # We are assuming the table load validation earlier passed
    # First check column order is correct against the configuration
    columns = s_df.columns
    norm_columns = list()
    for x, column in enumerate(columns):
        if _RX_INDEXED_COL.match(column):
            norm_columns.append(column[:column.rfind('.')])
        else:
            norm_columns.append(column)
    norm_columns = [k for k, g in itertools.groupby(norm_columns)]  # remove adjacent dups - i.e. chained Protocol REFs
    object_index = [(x, i) for x, i in enumerate(norm_columns) if i in ['Source Name', 'Sample Name',
                                                              'Extract Name', 'Labeled Extract Name', 'Raw Data File',
                                                              'Raw Spectral Data File', 'Array Data File',
                                                              'Protein Assignment File', 'Peptide Assignment File',
                                                              'Post Translational Modification Assignment File',
                                                              'Derived Spectral Data File',
                                                              'Derived Array Data File', 'Assay Name'] or 'Protocol REF' in i or
                    'Characteristics[' in i or 'Factor Value[' in i or 'Parameter Value[ in i' or 'Comment[' in i]
    fields = [i.header for i in config.get_isatab_configuration()[0].get_field()]
    protocols = [(i.pos, i.protocol_type) for i in config.get_isatab_configuration()[0].get_protocol_field()]
    for protocol in protocols:
        fields.insert(protocol[0], 'Protocol REF')
    # strip out non-config columns
    object_index = [i for i in object_index if i[1] in fields]
    for x, object in enumerate(object_index):
        if fields[x] != object[1]:
            validator_warnings.append({
                "message": "The column order in assay table is not valid",
                "supplemental": "Unexpected heading found. Expected {} but found {} at column number {}"
                    .format(fields[x], object[1], object[0]),
                "code": 4005
            })
            log.warning("(W) Unexpected heading found. Expected {} but found {} at column number {}".format(fields[x], object[1], object[0]))


def cell_has_value(cell):
    if isinstance(cell, float):
        if math.isnan(cell):
            return True
        else:
            return False
    else:
        if cell.strip() == '':
            return False
        elif 'Unnamed: ' in cell:
            return False
        else:
            return True


def check_assay_table_with_config(df, config, filename, protocol_names_and_types):
    columns = list(df.columns)
    # Get required headers from config and check if they are present in the table; Rule 4010
    required_fields = [i.header for i in config.get_isatab_configuration()[0].get_field() if i.is_required]
    for required_field in required_fields:
        if required_field not in columns:
            validator_warnings.append({
                "message": "A required column in assay table is not present",
                "supplemental": "In {} the required column {} missing from column headings"
                    .format(filename, required_field),
                "code": 4010
            })
            log.warning("(W) In {} the required column {} missing from column headings".format(filename, required_field))
        else:
            # Now check that the required column cells all have values, Rules 4003-4008
            for y, cell in enumerate(df[required_field]):
                if not cell_has_value(cell):
                    validator_warnings.append({
                        "message": "A required cell value is missing",
                        "supplemental": "Cell at row {} in column '{}' has no value".format(y, required_field),
                        "code": 4012
                    })
                    log.warning("(W) Cell at row {} in column '{}' has no value, but it is required by the "
                                "configuration".format(y, required_field))

    # Check if protocol ref column values are consistently structured
    protocol_ref_index = [i for i in columns if 'protocol ref' in i.lower()]
    prots_ok = True
    for each in protocol_ref_index:
        prots_found = set()
        for cell in df[each]:
            prots_found.add(cell)
        if len(prots_found) > 1:
            validator_warnings.append({
                "message": "Multiple protocol references in Protocol REF column",
                "supplemental": "Multiple protocol references {} are found in {}".format(prots_found, each),
                "code": 4999
            })
            log.warning("(W) Multiple protocol references {} are found in {}".format(prots_found, each))
            log.warning("(W) Only one protocol reference should be used in a Protocol REF column.")
            prots_ok = False


def check_study_assay_tables_against_config(i_df, dir_context, configs):
    """Used for rules 4003-4008"""
    for i, study_df in enumerate(i_df['studies']):
        study_filename = study_df.iloc[0]['Study File Name']
        protocol_names = i_df['s_protocols'][i]['Study Protocol Name'].tolist()
        protocol_types = i_df['s_protocols'][i]['Study Protocol Type'].tolist()
        protocol_names_and_types = dict(zip(protocol_names, protocol_types))
        if study_filename is not '':
            try:
                with open(os.path.join(dir_context, study_filename), encoding='utf-8') as s_fp:
                    df = load_table(s_fp)
                    config = configs[('[sample]', '')]
                    log.info("Checking study file {} against default study table configuration...".format(study_filename))
                    check_assay_table_with_config(df, config, study_filename, protocol_names_and_types)
            except FileNotFoundError:
                pass
        for j, assay_df in enumerate(i_df['s_assays']):
            assay_filename = assay_df['Study Assay File Name'].tolist()[0]
            measurement_type = assay_df['Study Assay Measurement Type'].tolist()[0]
            technology_type = assay_df['Study Assay Technology Type'].tolist()[0]
            if assay_filename is not '':
                try:
                    with open(os.path.join(dir_context, assay_filename), encoding='utf-8') as a_fp:
                        df = load_table(a_fp)
                        lowered_mt = measurement_type.lower()
                        lowered_tt = technology_type.lower()
                        config = configs[(lowered_mt, lowered_tt)]
                        log.info(
                            "Checking assay file {} against default table configuration ({}, {})...".format(assay_filename, measurement_type, technology_type))
                        check_assay_table_with_config(df, config, assay_filename, protocol_names_and_types)
                        # check_assay_table_with_config(df, protocols, config, assay_filename)
                except FileNotFoundError:
                    pass
        # TODO: Check protocol usage - Rule 4009


def check_factor_value_presence(table):
    factor_fields = [i for i in table.columns if i.lower().startswith('factor value')]
    for factor_field in factor_fields:
        for x, cell_value in enumerate(table.fillna('')[factor_field]):
            if cell_value == '':
                validator_warnings.append({
                    "message": "A required node factor value is missing value",
                    "supplemental": "(W) Missing value for '" + factor_field + "' at row " + str(x) + " in " +
                                    table.filename,
                    "code": 4007
                })
                log.warning("(W) Missing value for '" + factor_field + "' at row " + str(x) + " in " + table.filename)


def check_required_fields(table, cfg):
    for fheader in [i.header for i in cfg.get_isatab_configuration()[0].get_field() if i.is_required]:
        found_field = [i for i in table.columns if i.lower() == fheader.lower()]
        if len(found_field) == 0:
            validator_warnings.append({
                "message": "A required column in assay table is not present",
                "supplemental": "Required field '" + fheader + "' not found in the file '" + table.filename + "'",
                "code": 4010
            })
            log.warning("(W) Required field '" + fheader + "' not found in the file '" + table.filename + "'")
        elif len(found_field) > 1:
            validator_warnings.append({
                "message": "Multiple columns found",
                "supplemental": "Field '" + fheader + "' cannot have multiple values in the file '" + table.filename,
                "code": 4013
            })
            log.warning("(W) Field '" + fheader + "' cannot have multiple values in the file '" + table.filename)


def check_sample_names(study_sample_table, assay_tables=[]):
    if len(assay_tables) > 0:
        study_samples = set(study_sample_table['Sample Name'])
        for assay_table in assay_tables:
            assay_samples = set(assay_table['Sample Name'])
            for assay_sample in assay_samples:
                if assay_sample not in study_samples:
                    validator_warnings.append({
                        "message": "Missing Sample",
                        "supplemental": "{} is a Sample Name in {}, but it is not defined in the Study Sample File {}."
                                .format(assay_sample, assay_table.filename, study_sample_table.filename),
                        "code": 1003
                    })
                    log.warning("(W) {} is a Sample Name in {}, but it is not defined in the Study Sample File {}."
                                .format(assay_sample, assay_table.filename, study_sample_table.filename))


def check_field_values(table, cfg):
    def check_single_field(cell_value, cfg_field):
        # First check if the value is required by config
        if isinstance(cell_value, float):
            if math.isnan(cell_value):
                if cfg_field.is_required:
                    validator_warnings.append({
                        "message": "A required column in assay table is not present",
                        "supplemental": "Missing value for the required field '" + cfg_field.header
                                        + "' in the file '" + table.filename + "'",
                        "code": 4010
                    })
                    log.warning("(W) Missing value for the required field '" + cfg_field.header + "' in the file '" +
                                table.filename + "'")
                return True
        elif isinstance(cell_value, str):
            value = cell_value.strip()
            if value == '':
                if cfg_field.is_required:
                    validator_warnings.append({
                        "message": "A required cell value is missing",
                        "supplemental": "Missing value for the required field '" + cfg_field.header + "' in the file '" +
                                table.filename + "'",
                        "code": 4012
                    })
                    log.warning("(W) Missing value for the required field '" + cfg_field.header + "' in the file '" +
                                table.filename + "'")
                return True
        is_valid_value = True
        data_type = cfg_field.data_type.lower().strip()
        if data_type in ['', 'string']:
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
        elif 'double' == data_type:
            try:
                float(cell_value)
            except ValueError:
                is_valid_value = False
        elif data_type == 'list':
            list_values = [i.lower() for i in cfg_field.list_values.split(',')]
            if cell_value.lower() not in list_values:
                is_valid_value = False
        elif data_type in ['ontology-term', 'ontology term']:
            return True  # Structure and values checked in check_ontology_fields()
        else:
            validator_warnings.append({
                "message": "Unknown data type found",
                "supplemental": "Unknown data type '" + data_type + "' for field '" + cfg_field.header +
                                "' in the file '" + table.filename + "'",
                "code": 4011
            })
            log.warning("(W) Unknown data type '" + data_type + "' for field '" + cfg_field.header +
                        "' in the file '" + table.filename + "'")
            return False
        if not is_valid_value:
            validator_warnings.append({
                "message": "A value does not correspond to the correct data type",
                "supplemental": "Invalid value '" + cell_value + "' for type '" + data_type + "' of the field '"
                                + cfg_field.header + "'",
                "code": 4011
            })
            log.warning("(W) Invalid value '" + cell_value + "' for type '" + data_type + "' of the field '" +
                        cfg_field.header + "'")
            if data_type == 'list':
                log.warning("(W) Value must be one of: " + cfg_field.list_values)
        return is_valid_value

    result = True
    for irow in range(len(table.index)):
        ncols = len(table.columns)
        for icol in range(0, ncols):
            cfields = [i for i in cfg.get_isatab_configuration()[0].get_field() if i.header == table.columns[icol]]
            if len(cfields) == 1:
                cfield = cfields[0]
                result = result and check_single_field(table.iloc[irow][cfield.header], cfield)
    return result


def check_unit_field(table, cfg):
    def check_unit_value(cell_value, unit_value, cfield, filename):
        if cell_has_value(cell_value) or cell_has_value(unit_value):
            validator_warnings.append({
                "message": "Cell found has unit but no value",
                "supplemental": "Field '" + cfield.header + "' has a unit but not a value in the file '" + filename
                                + "'",
                "code": 4999
            })
            log.warning("(W) Field '" + cfield.header + "' has a unit but not a value in the file '" + filename + "'")
            return False
        return True

    result = True
    for icol, header in enumerate(table.columns):
        cfields = [i for i in cfg.get_isatab_configuration()[0].get_field() if i.header == header]
        if len(cfields) != 1:
            continue
        cfield = cfields[0]
        ucfields = [i for i in cfg.get_isatab_configuration()[0].get_unit_field() if i.pos == cfield.pos + 1]
        if len(ucfields) != 1:
            continue
        ucfield = ucfields[0]
        if ucfield.is_required:
            rheader = None
            rindx = icol + 1
            if rindx < len(table.columns):
                rheader = table.columns[rindx]
            if rheader is None or rheader.lower() != 'unit':
                validator_warnings.append({
                    "message": "Cell requires a Unit",
                    "supplemental": "The field '" + header + "' in the file '" + table.filename + "' misses a required "
                                                                                                  "'Unit' column",
                    "code": 4999
                })
                log.warning("(W) The field '" + header + "' in the file '" + table.filename +
                            "' misses a required 'Unit' column")
                result = False
            else:
                for irow in range(len(table.index)):
                    result = result and check_unit_value(table.iloc[irow][icol], table.iloc[irow][rindx],
                                                         cfield, table.filename)
    return result


def check_protocol_fields(table, cfg, proto_map):
    from itertools import tee

    def pairwise(iterable):  # A lovely pairwise iterator
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    proto_ref_index = [i for i in table.columns if 'protocol ref' in i.lower()]
    result = True
    for each in proto_ref_index:
        prots_found = set()
        for cell in table[each]:
            prots_found.add(cell)
        if len(prots_found) > 1:
            log.warning("(W) Multiple protocol references {} are found in {}".format(prots_found, each))
            log.warning("(W) Only one protocol reference should be used in a Protocol REF column.")
            result = False
    if result:
        field_headers = [i for i in table.columns if
                         i.lower().endswith(' name') or i.lower().endswith(' data file') or i.lower().endswith(
                             ' data matrix file')]
        protos = [i for i in table.columns if i.lower() == 'protocol ref']
        if len(protos) > 0:
            last_proto_indx = table.columns.get_loc(protos[len(protos) - 1])
        else:
            last_proto_indx = -1
        last_mat_or_dat_indx = table.columns.get_loc(field_headers[len(field_headers) - 1])
        if last_proto_indx > last_mat_or_dat_indx:
            log.warning("(W) Protocol REF column without output in file '" + table.filename + "'")
        for left, right in pairwise(field_headers):
            cleft = None
            cright = None
            clefts = [i for i in cfg.get_isatab_configuration()[0].get_field() if i.header.lower() == left.lower()]
            if len(clefts) == 1:
                cleft = clefts[0]
            crights = [i for i in cfg.get_isatab_configuration()[0].get_field() if
                       i.header.lower() == right.lower()]
            if len(crights) == 1:
                cright = crights[0]
            if cleft is not None and cright is not None:
                cprotos = [i.protocol_type for i in cfg.get_isatab_configuration()[0].get_protocol_field() if
                           cleft.pos < i.pos and cright.pos > i.pos]
                fprotos_headers = [i for i in table.columns[
                                              table.columns.get_loc(cleft.header):table.columns.get_loc(
                                                  cright.header)] if
                                   'protocol ref' in i.lower()]
                fprotos = list()
                for header in fprotos_headers:
                    proto_name = table.iloc[0][header]
                    try:
                        proto_type = proto_map[proto_name]
                        fprotos.append(proto_type)
                    except KeyError:
                        validator_warnings.append({
                            "message": "Missing Protocol declaration",
                            "supplemental": " Could not find protocol type for protocol name '{}', trying to validate "
                                            "against name only".format(proto_name),
                            "code": 1007
                        })
                        log.warning("(W) Could not find protocol type for protocol name '{}', trying to validate "
                                    "against name only".format(proto_name))
                        fprotos.append(proto_name)
                invalid_protos = set(cprotos) - set(fprotos)
                if len(invalid_protos) > 0:
                    validator_warnings.append({
                        "message": "Missing Protocol declaration",
                        "supplemental": "Protocol(s) of type " + str(list(invalid_protos))
                                        + " defined in the ISA-configuration expected as a between '"
                                        + cleft.header + "' and '" + cright.header
                                        + "' but has not been found, in the file '" + table.filename + "'",
                        "code": 1007
                    })
                    log.warning("(W) Protocol(s) of type " + str(
                        list(invalid_protos)) + " defined in the ISA-configuration expected as a between '" +
                                cleft.header + "' and '" + cright.header + "' but has not been found, in the file '" + table.filename + "'")
                    result = False
    return result


def check_ontology_fields(table, cfg, tsrs):
    def check_single_field(cell_value, source, acc, cfield, filename):
        if (cell_has_value(cell_value) and not cell_has_value(
                source) and cell_has_value(acc)) or not cell_has_value(
                cell_value):
            validator_warnings.append({
                "message": "Missing Term Source REF in annotation or missing Term Source Name",
                "supplemental": "Incomplete values for ontology headers, for the field '"
                                + cfield.header + "' in the file '"
                                + filename + "'. Check that all the label/accession/source are provided.",
                "code": 3008
            })
            log.warning(
                "(W) Incomplete values for ontology headers, for the field '" + cfield.header + "' in the file '" +
                filename + "'. Check that all the label/accession/source are provided.")
            if source not in tsrs:
                validator_warnings.append({
                    "message": "Term Source REF reference broken",
                    "supplemental": "Term Source REF, for the field '"
                                    + cfield.header + "' in the file '"
                                    + filename + "' does not refer to a declared Ontology Source.",
                    "code": 3011
                })
                log.warning(
                    "(W) Term Source REF, for the field '" + cfield.header +
                    "' in the file '" + filename +
                    "' does not refer to a declared Ontology Source.")
            return False
        return True

    result = True
    nfields = len(table.columns)
    for icol, header in enumerate(table.columns):
        cfields = [i for i in cfg.get_isatab_configuration()[0].get_field() if i.header == header]
        if len(cfields) != 1:
            continue
        cfield = cfields[0]
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
            log.warning("(W) The Field '" + header
                        + "' should have values from ontologies and has no ontology headers instead")
            result = False
            continue

        for irow in range(len(table.index)):
            result = result and check_single_field(table.iloc[irow][icol], table.iloc[irow][rindx],
                                                   table.iloc[irow][rrindx], cfield, table.filename)

    return result


BASE_DIR = os.path.dirname(__file__)
default_config_dir = os.path.join(BASE_DIR, 'resources', 'config', 'xml')

def get_num_study_groups(study_sample_table, study_filename):
    num_study_groups = -1
    factor_columns = [x for x in study_sample_table.columns if x.startswith('Factor Value')]
    if factor_columns != []:
        num_study_groups = len(study_sample_table[factor_columns].drop_duplicates())
    else:
        log.info("No study factors found in {}".format(study_filename))
    return num_study_groups


def check_study_groups(table, filename, study_group_size_in_comment):
    num_study_groups = get_num_study_groups(table, filename)
    log.info('Found {} study groups in {}'.format(
            num_study_groups, filename))
    validator_info.append({
            'message': 'Found {} study groups in {}'.format(
                num_study_groups, filename),
            'supplemental': 'Found {} study groups in {}'.format(
                num_study_groups, filename),
            'code': 5001
    })
    if study_group_size_in_comment is not None and \
                        study_group_size_in_comment != num_study_groups:
            log.warning('Study group size reported as {} but found {} in {}'
                        .format(study_group_size_in_comment, num_study_groups, filename))
            validator_warnings.append({
                'message': 'Reported study group size does not match table'
                    .format(num_study_groups, filename),
                'supplemental': 'Study group size reported as {} but found {} '
                                'in {}'.format(
                    study_group_size_in_comment, num_study_groups, filename),
                'code': 5002
                })
            return False
    return True


def validate(fp, config_dir=default_config_dir, log_level=None):
    global validator_errors
    global validator_warnings
    global validator_info
    validator_errors = []
    validator_warnings = []
    validator_info = []
    if log_level in (
        logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING,
        logging.ERROR, logging.CRITICAL):
        log.setLevel(log_level)
    log.info("ISA tab Validator from ISA tools API v0.6")
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    log.addHandler(handler)
    validation_finished = False
    try:
        # check_utf8(fp)  # skip as does not correctly report right now
        log.info("Loading... {}".format(fp.name))
        i_df = load_investigation(fp=fp)
        log.info("Running prechecks...")
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
        term_source_refs = check_ontology_sources(i_df)  # Rule 3008
        log.info("Finished prechecks...")
        log.info("Loading configurations found in {}".format(config_dir))
        configs = load_config(config_dir)  # Rule 4001
        if configs is None:
            raise SystemError("No configuration to load so cannot proceed with validation!")
        log.info("Using configurations found in {}".format(config_dir))
        check_measurement_technology_types(i_df, configs)  # Rule 4002
        log.info("Checking investigation file against configuration...")
        check_investigation_against_config(i_df, configs)  # Rule 4003 for investigation file only
        log.info("Finished checking investigation file")
        for i, study_df in enumerate(i_df['studies']):
            study_group_size_in_comment = None
            if NUMBER_OF_STUDY_GROUPS in study_df.columns:
                study_group_sizes = study_df[NUMBER_OF_STUDY_GROUPS]
                study_group_size_in_comment = next(iter(study_group_sizes))
            study_filename = study_df.iloc[0]['Study File Name']
            study_sample_table = None
            assay_tables = list()
            if study_filename is not '':
                protocol_names = i_df['s_protocols'][i]['Study Protocol Name'].tolist()
                protocol_types = i_df['s_protocols'][i]['Study Protocol Type'].tolist()
                protocol_names_and_types = dict(zip(protocol_names, protocol_types))
                try:
                    log.info("Loading... {}".format(study_filename))
                    with open(os.path.join(os.path.dirname(fp.name), study_filename), encoding='utf-8') as s_fp:
                        study_sample_table = load_table(s_fp)
                        study_sample_table.filename = study_filename
                        config = configs[('[sample]', '')]
                        log.info(
                            "Validating {} against default study table configuration".format(study_filename))
                        log.info("Checking Factor Value presence...")
                        check_factor_value_presence(study_sample_table)  # Rule 4007
                        log.info("Checking required fields...")
                        check_required_fields(study_sample_table, config)  # Rule 4003-8, 4010
                        log.info("Checking generic fields...")
                        if not check_field_values(study_sample_table, config):  # Rule 4011
                            log.warning("(W) There are some field value inconsistencies in {} against {} "
                                        "configuration".format(study_sample_table.filename, 'Study Sample'))
                        log.info("Checking unit fields...")
                        if not check_unit_field(study_sample_table, config):
                            log.warning("(W) There are some unit value inconsistencies in {} against {} "
                                        "configuration".format(study_sample_table.filename, 'Study Sample'))
                        log.info("Checking protocol fields...")
                        if not check_protocol_fields(study_sample_table, config, protocol_names_and_types):  # Rule 4009
                            log.warning("(W) There are some protocol inconsistencies in {} against {} "
                                        "configuration".format(study_sample_table.filename, 'Study Sample'))
                        log.info("Checking ontology fields...")
                        if not check_ontology_fields(study_sample_table, config, term_source_refs):  # Rule 3010
                            log.warning("(W) There are some ontology annotation inconsistencies in {} against {} "
                                        "configuration".format(study_sample_table.filename, 'Study Sample'))
                        log.info("Checking study group size...")
                        check_study_groups(study_sample_table, study_filename, study_group_size_in_comment)
                        log.info("Finished validation on {}".format(study_filename))
                except FileNotFoundError:
                    pass
                assay_df = i_df['s_assays'][i]
                study_group_size_in_comment = None
                if NUMBER_OF_STUDY_GROUPS in assay_df.columns:
                    study_group_sizes = study_df[
                        NUMBER_OF_STUDY_GROUPS]
                    study_group_size_in_comment = next(iter(study_group_sizes))
                for x, assay_filename in enumerate(assay_df['Study Assay File Name'].tolist()):
                    measurement_type = assay_df['Study Assay Measurement Type'].tolist()[x]
                    technology_type = assay_df['Study Assay Technology Type'].tolist()[x]
                    if assay_filename is not '':
                        try:
                            lowered_mt = measurement_type.lower()
                            lowered_tt = technology_type.lower()
                            config = configs[(lowered_mt, lowered_tt)]
                        except KeyError:
                            log.error("Could not load config matching ({}, {})".format(measurement_type, technology_type))
                            log.warning("Only have configs matching:")
                            for k in configs.keys():
                                log.warning(k)
                            config = None
                        if config is None:
                            log.warning("Skipping configuration validation as could not load config...")
                        else:
                            try:
                                log.info("Loading... {}".format(assay_filename))
                                with open(os.path.join(os.path.dirname(fp.name), assay_filename), encoding='utf-8') as a_fp:
                                    assay_table = load_table(a_fp)
                                    assay_table.filename = assay_filename
                                    assay_tables.append(assay_table)
                                    log.info(
                                        "Validating {} against assay table configuration ({}, {})...".format(
                                            assay_filename, measurement_type, technology_type))
                                    log.info("Checking Factor Value presence...")
                                    check_factor_value_presence(assay_table)  # Rule 4007
                                    log.info("Checking required fields...")
                                    check_required_fields(assay_table, config)  # Rule 4003-8, 4010
                                    log.info("Checking generic fields...")
                                    if not check_field_values(assay_table, config):  # Rule 4011
                                        log.warning(
                                            "(W) There are some field value inconsistencies in {} against {} configuration".format(
                                                assay_table.filename, (measurement_type, technology_type)))
                                    log.info("Checking unit fields...")
                                    if not check_unit_field(assay_table, config):
                                        log.warning(
                                            "(W) There are some unit value inconsistencies in {} against {} configuration".format(
                                                assay_table.filename, (measurement_type, technology_type)))
                                    log.info("Checking protocol fields...")
                                    if not check_protocol_fields(assay_table, config, protocol_names_and_types):  # Rule 4009
                                        log.warning("(W) There are some protocol inconsistencies in {} against {} "
                                                    "configuration".format(assay_table.filename, (measurement_type, technology_type)))
                                    log.info("Checking ontology fields...")
                                    if not check_ontology_fields(assay_table, config, term_source_refs):  # Rule 3010
                                        log.warning("(W) There are some ontology annotation inconsistencies in {} against {} "
                                                    "configuration".format(assay_table.filename, (measurement_type, technology_type)))
                                    log.info("Checking study group size...")
                                    check_study_groups(assay_table, assay_filename, study_group_size_in_comment)
                                    log.info("Finished validation on {}".format(assay_filename))
                            except FileNotFoundError:
                                pass
                        if study_sample_table is not None:
                            log.info("Checking consistencies between study sample table and assay tables...")
                            check_sample_names(study_sample_table, assay_tables)
                            log.info("Finished checking study sample table against assay tables...")
            if len(validator_errors) != 0:
                log.info("Skipping pooling test as there are outstanding errors")
            else:
                from isatools import utils
                try:
                    fp.seek(0)
                    utils.detect_isatab_process_pooling(fp)
                except:
                    pass
        log.info("Finished validation...")
        validation_finished = True
    except ParserError as cpe:
        validator_errors.append({
            "message": "Unknown/System Error",
            "supplemental": "The validator could not identify what the error is: {}".format(str(cpe)),
            "code": 0
        })
        log.fatal("(F) There was an error when trying to parse the ISA tab")
        log.fatal(cpe)
    except ValueError as ve:
        validator_errors.append({
            "message": "Unknown/System Error",
            "supplemental": "The validator could not identify what the error is: {}".format(str(ve)),
            "code": 0
        })
        log.fatal("(F) There was an error when trying to parse the ISA tab")
        log.fatal(ve)
    except SystemError as se:
        validator_errors.append({
            "message": "Unknown/System Error",
            "supplemental": "The validator could not identify what the error is: {}".format(str(se)),
            "code": 0
        })
        log.fatal("(F) Something went very very wrong! :(")
        log.fatal(se)
    except Exception as e:
        validator_errors.append({
            "message": "Unknown/System Error",
            "supplemental": "The validator could not identify what the error is: {}".format(str(e)),
            "code": 0
        })
        log.fatal("(F) Something went very very wrong! :(")
        log.fatal(e)
    finally:
        handler.flush()
        return {
            "errors": validator_errors,
            "warnings": validator_warnings,
            "info": validator_info,
            "validation_finished": validation_finished
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
        log.info("***Validating {}***\n".format(tab_dir))
        i_files = glob.glob(os.path.join(tab_dir, 'i_*.txt'))
        if len(i_files) != 1:
            log.warning("Could not find an investigation file, skipping {}".format(tab_dir))
        else:
            with open(i_files[0], encoding='utf-8') as fp:
                batch_report['batch_report'].append(
                    {
                        "filename": fp.name,
                        "report": validate(fp)
                    }
                )
    return batch_report


def dumps(isa_obj, skip_dump_tables=False,
          write_factor_values_in_assay_table=False):
    tmp = None
    output = str()
    try:
        tmp = tempfile.mkdtemp()
        dump(isa_obj=isa_obj, output_path=tmp, skip_dump_tables=skip_dump_tables,
             write_factor_values_in_assay_table=
             write_factor_values_in_assay_table)
        with open(os.path.join(tmp, 'i_investigation.txt'), encoding='utf-8') as i_fp:
            output += os.path.join(tmp, 'i_investigation.txt') + '\n'
            output += i_fp.read()
        for s_file in glob.iglob(os.path.join(tmp, 's_*')):
            with open(s_file, encoding='utf-8') as s_fp:
                output += "--------\n"
                output += s_file + '\n'
                output += s_fp.read()
        for a_file in glob.iglob(os.path.join(tmp, 'a_*')):
            with open(a_file, encoding='utf-8') as a_fp:
                output += "--------\n"
                output += a_file + '\n'
                output += a_fp.read()
    finally:
        if tmp is not None:
            shutil.rmtree(tmp)
    return output


def dump_tables_to_dataframes(isa_obj):
    tmp = None
    output = dict()
    try:
        tmp = tempfile.mkdtemp()
        dump(isa_obj=isa_obj, output_path=tmp, skip_dump_tables=False)
        for s_file in glob.iglob(os.path.join(tmp, 's_*')):
            output[os.path.basename(s_file)] = read_tfile(s_file)
        for a_file in glob.iglob(os.path.join(tmp, 'a_*')):
            output[os.path.basename(a_file)] = read_tfile(a_file)
    finally:
        if tmp is not None:
            shutil.rmtree(tmp)
    return output


def load(isatab_path_or_ifile, skip_load_tables=False):  # from DF of investigation file

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
        accession_split = accessions.split(';')
        ts_refs_split = ts_refs.split(';')
        # if no acc or ts_refs
        if accession_split == [''] and ts_refs_split == ['']:
            for val in vals.split(';'):
                oa_list.append(OntologyAnnotation(term=val, ))
        else:  # try parse all three sections
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
            publication.comments = get_comments_row(section_df.columns, row)
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
            person.comments = get_comments_row(section_df.columns, row)
            contacts.append(person)

        return contacts

    def get_comments(section_df):

        comments = []
        for col in [
            x for x in section_df.columns if _RX_COMMENT.match(str(x))]:
            for _, row in section_df.iterrows():
                comment = Comment(
                    name=next(iter(_RX_COMMENT.findall(col))), value=row[col])
                comments.append(comment)
        return comments

    def get_comments_row(cols, row):
        comments = []
        for col in [x for x in cols if _RX_COMMENT.match(str(x))]:
            comment = Comment(
                name=next(iter(_RX_COMMENT.findall(col))), value=row[col])
            comments.append(comment)
        return comments

    FP = None

    if isinstance(isatab_path_or_ifile, str):
        if os.path.isdir(isatab_path_or_ifile):
            fnames = glob.glob(os.path.join(isatab_path_or_ifile, "i_*.txt"))
            assert len(fnames) == 1
            FP = open(fnames[0], encoding='utf-8')
    elif hasattr(isatab_path_or_ifile, 'read'):
        FP = isatab_path_or_ifile
    else:
        raise IOError("Cannot resolve input file")

    try:
        df_dict = read_investigation_file(FP)

        investigation = Investigation()

        for _, row in df_dict['ontology_sources'].iterrows():
            ontology_source = OntologySource(name=row['Term Source Name'],
                                             file=row['Term Source File'],
                                             version=row['Term Source Version'],
                                             description=row['Term Source Description'])
            investigation.ontology_source_references.append(ontology_source)

        ontology_source_map = dict(map(lambda x: (x.name, x), investigation.ontology_source_references))

        if len(df_dict['investigation'].index) > 0:
            row = df_dict['investigation'].iloc[0]
            investigation.identifier = row['Investigation Identifier']
            investigation.title = row['Investigation Title']
            investigation.description = row['Investigation Description']
            investigation.submission_date = row['Investigation Submission Date']
            investigation.public_release_date = row['Investigation Public Release Date']
            investigation.publications = get_publications(df_dict['i_publications'])
            investigation.contacts = get_contacts(df_dict['i_contacts'])
            investigation.comments = get_comments(df_dict['investigation'])

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
            study.comments = get_comments(df_dict['studies'][i])

            for _, row in df_dict['s_design_descriptors'][i].iterrows():
                design_descriptor = get_oa(row['Study Design Type'],
                                           row['Study Design Type Term Accession Number'],
                                           row['Study Design Type Term Source REF'])
                design_descriptor.comments = get_comments_row(df_dict['s_design_descriptors'][i].columns, row)
                study.design_descriptors.append(design_descriptor)

            for _, row in df_dict['s_factors'][i].iterrows():
                factor = StudyFactor(name=row['Study Factor Name'])
                factor.factor_type = get_oa(row['Study Factor Type'],
                                            row['Study Factor Type Term Accession Number'],
                                            row['Study Factor Type Term Source REF'])
                factor.comments = get_comments_row(df_dict['s_factors'][i].columns, row)
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
                protocol.comments = get_comments_row(df_dict['s_protocols'][i].columns, row)
                study.protocols.append(protocol)
                protocol_map[protocol.name] = protocol
            study.protocols = list(protocol_map.values())
            if skip_load_tables:
                pass
            else:
                study_tfile_df = read_tfile(os.path.join(os.path.dirname(FP.name), study.filename))
                sources, samples, _, __, processes, characteristic_categories, unit_categories = ProcessSequenceFactory(
                    ontology_sources=investigation.ontology_source_references, study_protocols=study.protocols,
                    study_factors=study.factors).create_from_df(study_tfile_df)
                study.sources = sorted(list(sources.values()), key=lambda x: x.name, reverse=False)
                study.samples = sorted(list(samples.values()), key=lambda x: x.name, reverse=False)
                study.process_sequence = list(processes.values())
                study.characteristic_categories = sorted(list(characteristic_categories.values()), key=lambda x: x.term, reverse=False)
                study.units = sorted(list(unit_categories.values()), key=lambda x: x.term, reverse=False)

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
                if skip_load_tables:
                    pass
                else:
                    assay_tfile_df = read_tfile(os.path.join(os.path.dirname(FP.name), assay.filename))
                    _, samples, other, data, processes, characteristic_categories, unit_categories = ProcessSequenceFactory(
                        ontology_sources=investigation.ontology_source_references,
                        study_samples=study.samples,
                        study_protocols=study.protocols,
                        study_factors=study.factors).create_from_df(assay_tfile_df)
                    assay.samples = sorted(list(samples.values()), key=lambda x: x.name, reverse=False)
                    assay.other_material = sorted(list(other.values()), key=lambda x:x.name, reverse=False)
                    assay.data_files = sorted(list(data.values()), key=lambda x:x.filename, reverse=False)
                    assay.process_sequence = list(processes.values())
                    assay.characteristic_categories = sorted(list(characteristic_categories.values()), key=lambda x: x.term, reverse=False)
                    assay.units = sorted(list(unit_categories.values()), key=lambda x: x.term, reverse=False)

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
    finally:
        FP.close()
    return investigation


def process_keygen(protocol_ref, column_group, object_label_index, all_columns, series, series_index, DF):
    name_column_hits = [n for n in column_group if n in _LABELS_ASSAY_NODES]
    if len(name_column_hits) == 1:
        return series[name_column_hits[0]]

    process_key = protocol_ref
    node_cols = [i for i, c in enumerate(all_columns) if c in _LABELS_MATERIAL_NODES + _LABELS_DATA_NODES]
    input_node_value = ''
    output_node_value = ''
    output_node_index = find_gt(node_cols, object_label_index)
    if output_node_index > -1:
        output_node_label = all_columns[output_node_index]
        output_node_value = str(series[output_node_label])

    input_node_index = find_lt(node_cols, object_label_index)
    if input_node_index > -1:
        input_node_label = all_columns[input_node_index]
        input_node_value = str(series[input_node_label])

    input_nodes_with_prot_keys = DF[[all_columns[object_label_index], all_columns[input_node_index]]].drop_duplicates()
    output_nodes_with_prot_keys = DF[[all_columns[object_label_index], all_columns[output_node_index]]].drop_duplicates()

    if len(input_nodes_with_prot_keys) > len(output_nodes_with_prot_keys):
        node_key = output_node_value
    else:
        node_key = input_node_value

    if process_key == protocol_ref:
        process_key += '-' + str(series_index)

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

    date_col_hits = [c for c in column_group if c.startswith('Date')]
    if len(date_col_hits) == 1:
        process_key = ':'.join([process_key, series[date_col_hits[0]]])

    performer_col_hits = [c for c in column_group if c.startswith('Performer')]
    if len(performer_col_hits) == 1:
        process_key = ':'.join([process_key, series[performer_col_hits[0]]])

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
                log.debug('term source: ', term_source_value, ' not found')

        term_accession_value = object_series[offset_2r_col]

        if term_accession_value is not '':
            value.term_accession = str(term_accession_value)

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
                    log.debug('term source: ', unit_term_source_value, ' not found')

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


class IsaTabSeries(pd.Series):
    @property
    def _consutrctor(self):
        return IsaTabSeries


class IsaTabDataFrame(pd.DataFrame):

    DATA_FILE_LABELS = [
        'Raw Data File', 'Derived Spectral Data File',
        'Derived Array Data File', 'Array Data File',
        'Protein Assignment File', 'Peptide Assignment File',
        'Post Translational Modification Assignment File',
        'Acquisition Parameter Data File', 'Free Induction Decay Data File',
        'Derived Array Data Matrix File', 'Image File', 'Derived Data File',
        'Metabolite Assignment File', 'Raw Spectral Data File']
    MATERIAL_LABELS = ['Source Name', 'Sample Name', 'Extract Name',
                       'Labeled Extract Name']
    OTHER_MATERIAL_LABELS = ['Extract Name', 'Labeled Extract Name']
    NODE_LABELS = DATA_FILE_LABELS + MATERIAL_LABELS + OTHER_MATERIAL_LABELS
    ASSAY_LABELS = ['Assay Name', 'MS Assay Name', 'Hybridization Assay Name',
                    'Scan Name', 'Data Transformation Name',
                    'Normalization Name', 'Array Design REF']
    QUALIFIER_LABELS = ['Protocol REF', 'Material Type', 'Term Source REF',
                        'Term Accession Number', 'Unit']
    ALL_LABELS = NODE_LABELS + ASSAY_LABELS + QUALIFIER_LABELS
    ALL_LABELS.append('Protocol REF')

    def __init__(self, *args, **kw):
        super(IsaTabDataFrame, self).__init__(*args, **kw)

    @property
    def _constructor(self):
        return IsaTabDataFrame

    _constructor_sliced = IsaTabSeries

    @staticmethod
    def _clean_label(label):
        for clean_label in IsaTabDataFrame.ALL_LABELS:
            if clean_label.lower() in label.strip().lower():
                return clean_label
            elif _RX_CHARACTERISTICS.match(label):
                return 'Characteristics[{val}]'.format(
                    val=next(iter(_RX_CHARACTERISTICS.findall(label))))
            elif _RX_PARAMETER_VALUE.match(label):
                return 'Parameter Value[{val}]'.format(
                    val=next(iter(_RX_PARAMETER_VALUE.findall(label))))
            elif _RX_FACTOR_VALUE.match(label):
                return 'Factor Value[{val}]'.format(
                    val=next(iter(_RX_FACTOR_VALUE.findall(label))))
            elif _RX_COMMENT.match(label):
                return 'Comment[{val}]'.format(
                    val=next(iter(_RX_COMMENT.findall(label))))

    @property
    def isatab_header(self):
        return list(map(lambda x: self._clean_label(x), self.columns))


def read_tfile(tfile_path, index_col=None, factor_filter=None):
    log.debug("Opening %s", tfile_path)
    with open(tfile_path, encoding='utf-8') as tfile_fp:
        log.debug("Reading file header")
        reader = csv.reader(tfile_fp, dialect='excel-tab')
        header = list(next(reader))
        tfile_fp.seek(0)
        log.debug("Reading file into DataFrame")
        tfile_fp = strip_comments(tfile_fp)
        tfile_df = pd.read_csv(tfile_fp, dtype=str, sep='\t', index_col=index_col,
                        memory_map=True, encoding='utf-8').fillna('')
        tfile_df.isatab_header = header
        # tfile_df = IsaTabDataFrame(
        #     pd.read_csv(tfile_fp, dtype=str, sep='\t', index_col=index_col,
        #                 memory_map=True, encoding='utf-8').fillna(''))
    if factor_filter:
        log.debug("Filtering DataFrame contents on Factor Value %s", factor_filter)
        return tfile_df[tfile_df['Factor Value[{}]'.format(factor_filter[0])] == factor_filter[1]]
    else:
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
    process_node_name_indices = [
        x for x, y in enumerate(columns) if y in _LABELS_ASSAY_NODES]
    missing_process_indices = list()
    protocol_ref_cols = [x for x in columns if x.startswith('Protocol REF')]
    num_protocol_refs = len(protocol_ref_cols)
    all_cols_indicies = [i for i, c in enumerate(columns) if c in
                         _LABELS_MATERIAL_NODES +
                         _LABELS_DATA_NODES +
                         _LABELS_ASSAY_NODES +
                         protocol_ref_cols]

    for i in process_node_name_indices:
        if not columns[
            find_lt(all_cols_indicies, i)].startswith('Protocol REF'):
            log.info('warning: Protocol REF missing between \'{}\' and \'{}\''
                     .format(
                columns[find_lt(all_cols_indicies, i)], columns[i]))
            missing_process_indices.append(i)

    # insert Protocol REF columns
    offset = 0

    for i in reversed(missing_process_indices):
        inferred_protocol_type = ''
        leftcol = columns[find_lt(all_cols_indicies, i)]
        rightcol = columns[i]
        if leftcol == 'Source Name' and rightcol == 'Sample Name':
            inferred_protocol_type = 'sample collection'
        elif leftcol == 'Sample Name' and rightcol == 'Extract Name':
            inferred_protocol_type = 'extraction'
        elif leftcol == 'Extract Name' and rightcol == 'Labeled Extract Name':
            inferred_protocol_type = 'labeling'
        elif leftcol == 'Labeled Extract Name' and rightcol in (
                'Assay Name', 'MS Assay Name'):
            inferred_protocol_type = 'library sequencing'
        elif leftcol == 'Extract Name' and rightcol in (
                'Assay Name', 'MS Assay Name'):
            inferred_protocol_type = 'library preparation'
        elif leftcol == 'Scan Name' and rightcol == 'Raw Data File':
            inferred_protocol_type = 'data acquisition'
        elif leftcol == 'Assay Name' and rightcol == 'Normalization Name':
            inferred_protocol_type = 'normalization'
        elif leftcol == 'Normalization Name' and \
                        rightcol == 'Data Transformation Name':
            inferred_protocol_type = 'data transformation'
        elif leftcol == 'Raw Data File' and \
                        rightcol == 'Metabolite Identification File':
            inferred_protocol_type = 'metabolite identification'
        elif leftcol == 'Raw Data File' and \
                        rightcol == 'Protein Identification File':
            inferred_protocol_type = 'metabolite identification'

        # Force use of unknown protocol always, until we can insert missing 
        # protocol from above inferences into study metadata
        inferred_protocol_type = ''
        log.info('Inserting protocol {} in between {} and {}'
                 .format(
            inferred_protocol_type if inferred_protocol_type != '' else 
            'unknown', leftcol, rightcol))
        DF.insert(i, 'Protocol REF.{}'.format(num_protocol_refs + offset), 
                  'unknown'  if inferred_protocol_type == '' else 
                  inferred_protocol_type)
        DF.isatab_header.insert(i, 'Protocol REF')
        offset += 1
    return DF


def get_object_column_map(isatab_header, df_columns):
    if set(isatab_header) == set(df_columns):
        object_index = [
            i for i, x in enumerate(
                df_columns) if x in _LABELS_MATERIAL_NODES +
                               _LABELS_DATA_NODES or 'Protocol REF' in x]
    else:
        object_index = [
            i for i, x in enumerate(
                isatab_header) if x in _LABELS_MATERIAL_NODES +
                                  _LABELS_DATA_NODES + ['Protocol REF']]

    # group headers regarding objects delimited by object_index by slicing up
    # the header list
    object_column_map = []
    prev_i = object_index[0]

    for curr_i in object_index:  # collect each object's columns

        if prev_i == curr_i:
            pass  # skip if there's no diff, i.e. first one
        else:
            object_column_map.append(df_columns[prev_i:curr_i])
        prev_i = curr_i

    # finally collect last object's columns
    object_column_map.append(df_columns[prev_i:])
    return object_column_map


class ProcessSequenceFactory:

    def __init__(self, ontology_sources=None, study_samples=None,
                 study_protocols=None, study_factors=None):
        self.ontology_sources = ontology_sources
        self.samples = study_samples
        self.protocols = study_protocols
        self.factors = study_factors

    def create_from_df(self, DF):  # from DF of a table file

        DF = preprocess(DF=DF)

        if self.ontology_sources is not None:
            ontology_source_map = dict(
                map(lambda x: (x.name, x), self.ontology_sources))
        else:
            ontology_source_map = {}

        if self.protocols is not None:
            protocol_map = dict(
                map(lambda x: (x.name, x), self.protocols))
        else:
            protocol_map = {}

        sources = {}
        other_material = {}
        data = {}
        processes = {}
        characteristic_categories = {}
        unit_categories = {}

        try:
            sources = dict(map(lambda x: ('Source Name:' + x, Source(name=x)),
                           [x for x in DF['Source Name'].drop_duplicates()
                            if x != '']))
        except KeyError:
            pass

        samples = {}
        try:
            if self.samples is not None:
                sample_map = dict(
                    map(lambda x: ('Sample Name:' + x.name, x), self.samples))
                sample_keys = list(
                    map(lambda x: 'Sample Name:' + x,
                        [str(x) for x in DF['Sample Name'].drop_duplicates()
                         if x != '']))
                for k in sample_keys:
                    try:
                        samples[k] = sample_map[k]
                    except KeyError:
                        log.warning(
                            'warning! Did not find sample referenced at assay '
                            'level in study samples')
            else:
                samples = dict(
                    map(lambda x: ('Sample Name:' + x, Sample(name=x)),
                        [str(x) for x in DF['Sample Name'].drop_duplicates()
                         if x != '']))
        except KeyError:
            pass

        try:
            extracts = dict(
                map(lambda x: ('Extract Name:' + x, Material(
                    name=x, type_='Extract Name')),
                    [x for x in DF['Extract Name'].drop_duplicates() if
                     x != '']))
            other_material.update(extracts)
        except KeyError:
            pass

        try:
            if 'Labeled Extract Name' in DF.columns:
                try:
                    category = characteristic_categories['Label']
                except KeyError:
                    category = OntologyAnnotation(term='Label')
                    characteristic_categories['Label'] = category
                for _, lextract_name in DF[
                    'Labeled Extract Name'].drop_duplicates().iteritems():
                    if lextract_name != '':
                        lextract = Material(
                            name=lextract_name, type_='Labeled Extract Name')
                        lextract.characteristics = [
                            Characteristic(
                                category=category,
                                value=OntologyAnnotation(
                                    term=DF.loc[_, 'Label'])
                            )
                        ]
                        other_material[
                            'Labeled Extract Name:' + lextract_name] = lextract
        except KeyError:
            pass

        for data_col in [x for x in DF.columns if x.endswith(" File")]:
            filenames = [x for x in DF[data_col].drop_duplicates() if x != '']
            data.update(
                dict(map(lambda x: (':'.join([data_col, x]),
                                    DataFile(filename=x, label=data_col)),
                         filenames)))

        node_cols = [
            i for i, c in enumerate(
                DF.columns) if c in _LABELS_MATERIAL_NODES + _LABELS_DATA_NODES]
        proc_cols = [
            i for i, c in enumerate(
                DF.columns) if c.startswith("Protocol REF")]

        try:
            object_column_map = get_object_column_map(
                DF.isatab_header, DF.columns)
        except AttributeError:
            object_column_map = get_object_column_map(
                DF.columns, DF.columns)

        def get_node_by_label_and_key(l, k):
            n = None
            lk = l + ':' + k
            if l == 'Source Name':
                n = sources[lk]
            if l == 'Sample Name':
                n = samples[lk]
            elif l in ('Extract Name', 'Labeled Extract Name'):
                n = other_material[lk]
            elif l.endswith(' File'):
                n = data[lk]
            return n

        for _cg, column_group in enumerate(object_column_map):
            # for each object, parse column group

            object_label = column_group[0]

            if object_label in _LABELS_MATERIAL_NODES:

                if isa_logging.show_pbars:
                    pbar = ProgressBar(
                        min_value=0, max_value=len(DF.index),
                        widgets=['Setting material objects: ',
                                 SimpleProgress(), Bar(left=" |", right="| "),
                                 ETA()]).start()
                else:
                    pbar = lambda x: x

                for _, object_series in pbar(
                        DF[column_group].drop_duplicates().iterrows()):
                    node_name = str(object_series[object_label])
                    node_key = ":".join([object_label, node_name])
                    material = None
                    if object_label == "Source Name":
                        try:
                            material = sources[node_key]
                        except KeyError:
                            pass  # skip if object not found
                    elif object_label == "Sample Name":
                        try:
                            material = samples[node_key]
                        except KeyError:
                            pass  # skip if object not found
                    else:
                        try:
                            material = other_material[node_key]
                        except KeyError:
                            pass  # skip if object not found

                    if material is not None:

                        for charac_column in [
                            c for c in column_group if c.startswith(
                                'Characteristics[')]:

                            category_key = next(iter(
                                _RX_CHARACTERISTICS.findall(charac_column)))

                            try:
                                category = characteristic_categories[
                                    category_key]
                            except KeyError:
                                category = OntologyAnnotation(term=category_key)
                                characteristic_categories[
                                    category_key] = category

                            characteristic = Characteristic(category=category)

                            v, u = get_value(
                                charac_column, column_group, object_series,
                                ontology_source_map, unit_categories)

                            characteristic.value = v
                            characteristic.unit = u

                            if characteristic.category.term in [
                                x.category.term for x in material.characteristics]:
                                log.warning(
                                    'Duplicate characteristic found for '
                                    'material, skipping adding to material '
                                    'object')
                            else:
                                material.characteristics.append(characteristic)

                        for comment_column in [
                            c for c in column_group if c.startswith(
                                'Comment[')]:
                            comment_key = next(iter(
                                _RX_COMMENT.findall(comment_column)))
                            if comment_key not in [
                                x.name for x in material.comments]:
                                material.comments.append(
                                    Comment(name=comment_key,
                                            value=str(
                                                object_series[comment_column])))

                for _, object_series in pbar(DF.drop_duplicates().iterrows()):
                    node_name = str(object_series['Sample Name'])
                    node_key = ":".join(['Sample Name', node_name])
                    material = None
                    try:
                        material = samples[node_key]
                    except KeyError:
                        pass  # skip if object not found
                    if isinstance(
                            material, Sample) and self.factors is not None:

                        for fv_column in [
                            c for c in DF.columns if c.startswith(
                                'Factor Value[')]:

                            category_key = next(iter(
                                _RX_FACTOR_VALUE.findall(fv_column)))

                            factor_hits = [
                                f for f in self.factors if
                                f.name == category_key]

                            if len(factor_hits) == 1:
                                factor = factor_hits[0]
                            else:
                                raise ValueError(
                                    'Could not resolve Study Factor from '
                                    'Factor Value ', category_key)
                            fv = FactorValue(factor_name=factor)

                            v, u = get_value(
                                fv_column, DF.columns, object_series,
                                ontology_source_map, unit_categories)

                            fv.value = v
                            fv.unit = u
                            fv_set = set(material.factor_values)
                            fv_set.add(fv)
                            material.factor_values = list(fv_set)

            elif object_label in _LABELS_DATA_NODES:
                if isa_logging.show_pbars:
                    pbar = ProgressBar(
                        min_value=0, max_value=len(DF.index), widgets=[
                            'Setting data objects: ', SimpleProgress(),
                            Bar(left=" |", right="| "), ETA()]).start()
                else:
                    pbar = lambda x: x
                for _, object_series in pbar(
                        DF[column_group].drop_duplicates().iterrows()):
                    try:
                        data_file = get_node_by_label_and_key(
                            object_label, str(object_series[object_label]))
                        for comment_column in [
                            c for c in column_group if c.startswith(
                                'Comment[')]:
                            comment_key = next(iter(
                                _RX_COMMENT.findall(comment_column)))
                            if comment_key not in [
                                x.name for x in data_file.comments]:
                                data_file.comments.append(
                                    Comment(
                                        name=comment_key,
                                        value=str(
                                            object_series[comment_column])))
                    except KeyError:
                        pass  # skip if object not found

            elif object_label.startswith('Protocol REF'):
                object_label_index = list(DF.columns).index(object_label)
                if isa_logging.show_pbars:
                    pbar = ProgressBar(
                        min_value=0, max_value=len(DF.index), 
                        widgets=['Generating process objects: ',
                                 SimpleProgress(), Bar(left=" |", right="| "),
                                 ETA()]).start()
                else:
                    pbar = lambda x: x
                    
                # don't drop duplicates
                for _, object_series in pbar(DF.iterrows()): 
                    # if _ == 0:
                    #     print('processing: ', object_series[object_label])
                    protocol_ref = str(object_series[object_label])
                    process_key = process_keygen(
                        protocol_ref, column_group, _cg, DF.columns, 
                        object_series, _, DF)

                    # TODO: Keep process key sequence here to reduce number of passes on Protocol REF columns?

                    try:
                        process = processes[process_key]
                    except KeyError:
                        process = Process(executes_protocol=protocol_ref)
                        processes.update(dict([(process_key, process)]))

                    output_node_index = find_gt(node_cols, object_label_index)
                    output_proc_index = find_gt(proc_cols, object_label_index)

                    if output_proc_index < output_node_index > -1:

                        output_node_label = DF.columns[output_node_index]
                        output_node_value = str(
                            object_series[output_node_label])

                        node_key = output_node_value

                        output_node = None

                        try:
                            output_node = get_node_by_label_and_key(
                                output_node_label, node_key)
                        except KeyError:
                            pass  # skip if object not found

                        if output_node is not None and \
                                        output_node not in process.outputs:
                            # print(process_key, 'output', output_node_label, node_key)
                            process.outputs.append(output_node)

                    input_node_index = find_lt(node_cols, object_label_index)
                    input_proc_index = find_lt(proc_cols, object_label_index)

                    if input_proc_index < input_node_index > -1:

                        input_node_label = DF.columns[input_node_index]
                        input_node_value = str(object_series[input_node_label])

                        node_key = input_node_value

                        input_node = None

                        try:
                            input_node = get_node_by_label_and_key(
                                input_node_label, node_key)
                        except KeyError:
                            pass  # skip if object not found

                        if input_node is not None and \
                                        input_node not in process.inputs:
                            # print(process_key, 'input', input_node_label, node_key)
                            process.inputs.append(input_node)

                    name_column_hits = [n for n in column_group 
                                        if n in _LABELS_ASSAY_NODES]

                    if len(name_column_hits) == 1:
                        process.name = str(object_series[name_column_hits[0]])

                    for pv_column in [c for c in column_group if c.startswith(
                            'Parameter Value[')]:

                        category_key = next(iter(
                            _RX_PARAMETER_VALUE.findall(pv_column)))

                        if category_key in [x.category.parameter_name.term 
                                            for x in process.parameter_values]:
                            pass
                        else:
                            try:
                                protocol = protocol_map[protocol_ref]
                            except KeyError:
                                raise ValueError(
                                    'Could not find protocol matching ', 
                                    protocol_ref)

                            param_hits = [
                                p for p in protocol.parameters 
                                if p.parameter_name.term == category_key]

                            if len(param_hits) == 1:
                                category = param_hits[0]
                            else:
                                raise ValueError(
                                    'Could not resolve Protocol parameter from '
                                    'Parameter Value ', category_key)

                            parameter_value = ParameterValue(category=category)
                            v, u = get_value(
                                pv_column, column_group, object_series,
                                ontology_source_map, unit_categories)

                            parameter_value.value = v
                            parameter_value.unit = u

                            process.parameter_values.append(parameter_value)

                    for comment_column in \
                            [c for c in column_group
                             if c.startswith('Comment[')]:
                        comment_key = next(iter(
                            _RX_COMMENT.findall(comment_column)))
                        if comment_key not in \
                                [x.name for x in process.comments]:
                            process.comments.append(
                                Comment(name=comment_key,
                                        value=str(
                                            object_series[comment_column])))

        # now go row by row pulling out processes and linking them accordingly
        if isa_logging.show_pbars:
            pbar = ProgressBar(
                min_value=0, max_value=len(DF.index),
                widgets=['Linking processes and other nodes in paths: ',
                         SimpleProgress(), Bar(left=" |", right="| "),
                         ETA()]).start()
        else:
            pbar = lambda x: x
        for _, object_series in pbar(DF.iterrows()):  # don't drop duplicates
            process_key_sequence = list()
            source_node_context = None
            sample_node_context = None
            for _cg, column_group in enumerate(object_column_map):
                # for each object, parse column group
                object_label = column_group[0]

                if object_label.startswith('Source Name'):
                    try:
                        source_node_context = get_node_by_label_and_key(
                            object_label, str(object_series[object_label]))
                    except KeyError:
                        pass  # skip if object not found

                if object_label.startswith('Sample Name'):
                    try:
                        sample_node_context = get_node_by_label_and_key(
                            object_label, str(object_series[object_label]))
                    except KeyError:
                        pass  # skip if object not found
                    if source_node_context is not None:
                        if source_node_context not in \
                                sample_node_context.derives_from:
                            sample_node_context.derives_from.append(
                                source_node_context)

                if object_label.startswith('Protocol REF'):
                    protocol_ref = str(object_series[object_label])
                    process_key = process_keygen(
                        protocol_ref, column_group, _cg, DF.columns,
                        object_series, _, DF)
                    process_key_sequence.append(process_key)

                if object_label.endswith(' File'):
                    data_node = None
                    try:
                        data_node = get_node_by_label_and_key(
                            object_label, str(object_series[object_label]))
                    except KeyError:
                        pass  # skip if object not found
                    if sample_node_context is not None and \
                                    data_node is not None:
                        if sample_node_context not in data_node.generated_from:
                            data_node.generated_from.append(sample_node_context)

            # print('key sequence = ', process_key_sequence)

            # Link the processes in each sequence
            for pair in pairwise(process_key_sequence):
                l = processes[pair[0]]  # get process on left of pair
                r = processes[pair[1]]  # get process on right of pair
                plink(l, r)

        return sources, samples, other_material, data, processes, \
               characteristic_categories, unit_categories


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


def merge_study_with_assay_tables(study_file_path, assay_file_path,
                                  target_file_path):
    """
        Utility function to merge a study table file with an assay table file. The merge uses the Sample Name as the
        key, so samples in the assay file must match those in the study file. If there are no matches, the function
        will output the joined header and no additional rows.

        Usage:

        merge_study_with_assay_tables('/path/to/study.txt', '/path/to/assay.txt', '/path/to/merged.txt')
    """
    log.info("Reading study file %s into DataFrame", study_file_path)
    study_DF = read_tfile(study_file_path)
    log.info("Reading assay file %s into DataFrame", assay_file_path)
    assay_DF = read_tfile(assay_file_path)
    log.info("Merging DataFrames...")
    merged_DF = pd.merge(study_DF, assay_DF, on='Sample Name')
    log.info("Writing merged DataFrame to file %s", target_file_path)
    with open(target_file_path, 'w', encoding='utf-8') as fp:
        merged_DF.to_csv(
            fp, sep='\t', index=False,
            header=study_DF.isatab_header + assay_DF.isatab_header[1:])


def squashstr(string):
    nospaces = "".join(string.split())
    return nospaces.lower()


def get_squashed(key):
    try:
        if '[' in key and ']' in key:
            return squashstr(key[0:key.index('[')]) + key[key.index('['):]
        else:
            return squashstr(key)
    except ValueError:
        return squashstr(key)


class IsaTabParser(object):

    """
        This replacement should be more robust than current i_*.txt file reader. Based on what I did for the
        MAGE-TAB IDF parser. INCOMPLETE - do not use!

        TODO: Work out how to add comments in correct contexts
        TODO: Parse Assay section
        TODO: Unit tests
    """

    def __init__(self):
        self.ISA = Investigation()
        self._ts_dict = {}

    def parse_investigation(self, in_filename):
        section_keys = ('ontologysourcereference',
                    'investigation',
                    'investigationpublications',
                    'investigationcontacts',
                    'study',
                    'studydesigndescriptors',
                    'studypublciations',
                    'studyfactors',
                    'studyassays',
                    'studyprotocols',
                    'studycontacts')
        isecdict = {}
        ssecdicts = []
        with open(in_filename, encoding='utf-8') as in_file:
            tabreader = csv.reader(
                filter(lambda r: r[0] != '#', in_file), dialect='excel-tab')
            current_section = ''
            for row in tabreader:
                key = get_squashed(key=row[0])
                if key in section_keys:
                    current_section = key
                if key.startswith('comment'):
                    key = '.'.join((current_section, key))
                if key == 'study':
                    ssecdicts.append({})
                if key.startswith('study'):
                    ssecdicts[-1][key] = row[1:]
                else:
                    isecdict[key] = row[1:]

        self.parse_ontology_sources_section(
            isecdict.get('termsourcename', []),
            isecdict.get('termsourcefile', []),
            isecdict.get('termsourceversion', []),
            isecdict.get('termsourcedescription'),
            {k: isecdict[k] for k in isecdict.keys()
             if k.startswith('ontologysourcereference.')})
        self.parse_investigation_section(
            isecdict.get('investigationidentifier', []),
            isecdict.get('investigationtitle', []),
            isecdict.get('investigationdescription', []),
            isecdict.get('investigationsubmissiondate', []),
            isecdict.get('investigationpublicreleasedate'),
            {k: isecdict[k] for k in isecdict.keys() if k.startswith('investigation.')})
        self.parse_publications_section(
            self.ISA,
            isecdict.get('investigationpubmedid', []),
            isecdict.get('investigationpublicationdoi', []),
            isecdict.get('investigationpublicationauthorlist', []),
            isecdict.get('investigationpublicationtitle', []),
            isecdict.get('investigationpublicationstatus', []),
            isecdict.get('investigationpublicationstatustermsourceref', []),
            isecdict.get('investigationpublicationstatustermaccessionnumber'),
            {k: isecdict[k] for k in isecdict.keys()
             if k.startswith('investigationpublications.')})
        self.parse_people_section(
            self.ISA,
            isecdict.get('investigationpersonlastname', []),
            isecdict.get('investigationpersonfirstname', []),
            isecdict.get('investigationpersonmidinitials', []),
            isecdict.get('investigationpersonemail', []),
            isecdict.get('investigationpersonphone', []),
            isecdict.get('investigationpersonfax', []),
            isecdict.get('investigationpersonaddress', []),
            isecdict.get('investigationpersonaffiliation', []),
            isecdict.get('investigationpersonroles', []),
            isecdict.get('investigationpersonrolestermaccessionnumber', []),
            isecdict.get('investigationpersonrolestermsourceref'),
            {k: isecdict[k] for k in isecdict.keys()
             if k.startswith('investigationcontacts.')})

        for ssecdict in ssecdicts:
            self.parse_study_section(
                ssecdict.get('studyidentifier', []),
                ssecdict.get('studytitle', []),
                ssecdict.get('studydescription', []),
                ssecdict.get('studysubmissiondate', []),
                ssecdict.get('studypublicreleasedate', []),
                ssecdict.get('studyfilename'))
            self.parse_study_design_section(
                self.ISA.studies[-1],
                ssecdict.get('studydesigntype', []),
                ssecdict.get('studydesigntypetermaccessionnumber', []),
                ssecdict.get('studydesigntypetermsourceref'))
            self.parse_publications_section(
                self.ISA.studies[-1],
                ssecdict.get('studypubmedid', []),
                ssecdict.get('studypublicationdoi', []),
                ssecdict.get('studypublicationauthorlist', []),
                ssecdict.get('studypublicationtitle', []),
                ssecdict.get('studypublicationstatus', []),
                ssecdict.get('studypublicationstatustermsourceref', []),
                ssecdict.get('studypublicationstatustermaccessionnumber'),
                {k: ssecdict[k] for k in ssecdict.keys()
                 if k.startswith('studypublications.')})
            self.parse_people_section(
                self.ISA.studies[-1],
                ssecdict.get('studypersonlastname', []),
                ssecdict.get('studypersonfirstname', []),
                ssecdict.get('studypersonmidinitials', []),
                ssecdict.get('studypersonemail', []),
                ssecdict.get('studypersonphone', []),
                ssecdict.get('studypersonfax', []),
                ssecdict.get('studypersonaddress', []),
                ssecdict.get('studypersonaffiliation', []),
                ssecdict.get('studypersonroles', []),
                ssecdict.get('studypersonrolestermaccessionnumber', []),
                ssecdict.get('studypersonrolestermsourceref'),
                {k: ssecdict[k] for k in ssecdict.keys()
                 if k.startswith('studycontacts.')})
            self.parse_study_factors_section(
                self.ISA.studies[-1],
                ssecdict.get('studyfactorname', []),
                ssecdict.get('studyfactorntype', []),
                ssecdict.get('studyfactortypetermaccessionnumber', []),
                ssecdict.get('studyfactortypetermsourceref'))

    def parse_ontology_sources_section(self, names, files, versions,
                                       descriptions, comments_dict):
        i = 0
        for name, file, version, description in zip_longest(
                names, files, versions, descriptions):
            i += 1
            os = OntologySource(
                name=name, file=file, version=version, description=description)
            for k, v in comments_dict.items():
                if i < len(v) > 0:
                    os.comments.append(
                        Comment(name=next(iter(_RX_COMMENT.findall(k))),
                                value=v[i]))
            self.ISA.ontology_source_references.append(os)
            self._ts_dict[name] = os

    def parse_investigation_section(
            self, identifiers, titles, descriptions, submissiondates,
            publicreleasedates, comments_dict):
        for identifier, title, description, submissiondate, \
            publicreleasedate in  zip_longest(
            identifiers, titles, descriptions, submissiondates,
            publicreleasedates):
            self.ISA.identifier = identifier
            self.ISA.title = title
            self.ISA.description = description
            self.ISA.submission_date = submissiondate
            self.ISA.public_release_date = publicreleasedate
            for k, v in comments_dict.items():
                if len(v) > 0:
                    self.ISA.comments.append(
                        Comment(name=next(iter(_RX_COMMENT.findall(k))),
                                value=';'.join(v) if len(v) > 1 else v[0]))
            break  # because there should only be one or zero rows

    def parse_study_section(self, identifiers, titles, descriptions,
                            submissiondates, publicreleasedates, filenames):
        for identifier, title, description, submissiondate, publicreleasedate,\
            filename in zip_longest(
            identifiers, titles, descriptions, submissiondates,
            publicreleasedates, filenames):
            study = Study(
                identifier=identifier, title=title, description=description,
                submission_date=submissiondate,
                public_release_date=publicreleasedate, filename=filename)
            self.ISA.studies.append(study)

    def parse_study_design_section(self, obj, dtypes, dtypetans, dtypetsrs):
        for dtype, dtypetan, dtypetsr in zip_longest(
                dtypes, dtypetans, dtypetsrs):
            dtypeoa = OntologyAnnotation(
                term=dtype, term_source=self._ts_dict.get(dtypetsr),
                term_accession=dtypetan)
            obj.design_type = dtypeoa
            break

    def parse_publications_section(
            self, obj, pubmedids, dois, authorlists, titles, statuses,
            statustans, statustsrs, comments_dict):
        i = 0
        for pubmedid, doi, authorlist, title, status, statustsr, statustan in \
                zip_longest(
                    pubmedids, dois, authorlists, titles, statuses, statustans,
                    statustsrs):
            i += 1
            statusoa = OntologyAnnotation(
                term=status, term_source=self._ts_dict.get(statustsr),
                term_accession=statustan)
            publication = Publication(
                pubmed_id=pubmedid, doi=doi, author_list=authorlist,
                title=title, status=statusoa)
            for k, v in comments_dict.items():
                if i < len(v) > 0:
                    publication.comments.append(
                        Comment(name=next(iter(_RX_COMMENT.findall(k))),
                                value=v[i]))
            obj.publications.append(publication)

    def parse_people_section(
            self, obj, lastnames, firstnames, midinitialss, emails, phones,
            faxes, addresses, affiliations, roles, roletans, roletrs,
            comments_dict):
        i = 0
        for lastname, firstname, midinitials, email, phone, fax, address, \
            affiliation, role, roletan, roletsr in \
                zip_longest(
                    lastnames, firstnames, midinitialss, emails, phones, faxes,
                    addresses, affiliations, roles, roletans, roletrs):
            i += 1
            rolesoa = OntologyAnnotation(
                term=role, term_source=self._ts_dict.get(roletsr),
                term_accession=roletan)
            person = Person(
                last_name=lastname, first_name=firstname,
                mid_initials=midinitials, email=email, phone=phone, fax=fax,
                address=address, affiliation=affiliation, roles=rolesoa)
            obj.contacts.append(person)
        for i, contact in enumerate(self.ISA.studies[-1].contacts):
            for k, v in comments_dict.items():
                if len(v) > 0:
                    contact.comments.append(
                        Comment(name=next(iter(_RX_COMMENT.findall(k))),
                                value=v[i]))

    def parse_study_factors_section(
            self, obj, fnames, ftypes, ftypetans, ftypetsrs):
        for fname, ftype, ftypetan, ftypetsr in zip_longest(
                fnames, ftypes, ftypetans, ftypetsrs):
            ftypeoa = OntologyAnnotation(
                term=ftype, term_source=self._ts_dict.get(ftypetsr),
                term_accession=ftypetan)
            factor = StudyFactor(name=fname, factor_type=ftypeoa)
            obj.factors.append(factor)


def parse_in(in_filename, in_format='isa-tab'):
    """ Parse the given input file using the in_format and return as ISA
    objects"""

    log.debug("parsing {0} in format {1}".format(in_filename, in_format))

    log.debug("starting to parse {0}".format(in_filename))

    parser = IsaTabParser()
    parser.parse_investigation(in_filename)


def strip_comments(in_fp):
    out_fp = StringIO()
    if not isinstance(in_fp, StringIO):
        out_fp.name = in_fp.name
    for line in in_fp.readlines():
        log.debug('processing line: {}'.format(line))
        if line.lstrip().startswith('#'):
            log.debug('stripping line:'.format(line))
        elif len(line.strip()) > 0:
            out_fp.write(line)
    out_fp.seek(0)
    return out_fp
