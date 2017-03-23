from isatools import isatab
import os
import tempfile
from .model.v1 import *
import os
from pandas.parser import CParserError
import glob
import networkx as nx
import logging
import re
import math
import iso8601
import csv
import numpy as np
from bisect import bisect_left, bisect_right
from itertools import tee
import pandas as pd
from progressbar import ProgressBar, SimpleProgress, Bar, ETA
from io import StringIO


logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def _build_metadata_df(ISA):
    metadata_df = pd.DataFrame(columns=(
        "MAGE-TAB Version",
        "Investigation Title",
        "Public Release Date",
        "SDRF File"
    ))
    metadata_df.loc[0] = [
        "1.1",
        ISA.title,
        ISA.public_release_date,
        "sdrf.txt"
    ]
    return metadata_df


def _build_exp_designs_df(ISA):
    exp_designs_df = pd.DataFrame(columns=(
        "Experimental Design",
        "Experimental Design Term Source REF",
        "Experimental Design Term Accession Number"))
    for i, design_descriptor in enumerate(ISA.studies[0].design_descriptors):
        exp_designs_df.loc[i] = [
            design_descriptor.term,
            design_descriptor.term_source.name,
            design_descriptor.term_accession
        ]
    return exp_designs_df


def _build_exp_factors_df(ISA):
    exp_factors_df = pd.DataFrame(columns=(
        "Experimental Factor Name",
        "Experimental Factor Type",
        "Experimental Factor Term Source REF",
        "Experimental Factor Term Accession Number"))
    for i, factor in enumerate(ISA.studies[0].factors):
        exp_factors_df.loc[i] = [
            factor.name,
            factor.factor_type.term,
            factor.factor_type.term_source.name if factor.factor_type.term_source else "",
            factor.factor_type.term_accession if factor.factor_type.term_source else ""
        ]
    return exp_factors_df


def _build_roles_str(roles):
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
    return roles_names, roles_accession_numbers, roles_source_refs


def _build_people_df(ISA):
    people_df = pd.DataFrame(columns=("Person Last Name",
                                      "Person Mid Initials",
                                      "Person First Name",
                                      "Person Email",
                                      "Person Phone",
                                      "Person Fax",
                                      "Person Address",
                                      "Person Affiliation",
                                      "Person Roles",
                                      "Person Roles Term Source REF",
                                      "Person Roles Term Accession Number"))
    for i, contact in enumerate(ISA.contacts):
        roles_names, roles_accessions, roles_sources = _build_roles_str(contact.roles)
        people_df.loc[i] = [
            contact.last_name,
            contact.mid_initials,
            contact.first_name,
            contact.email,
            contact.phone,
            contact.fax,
            contact.address,
            contact.affiliation,
            roles_names,
            roles_sources,
            roles_accessions
        ]
    return people_df


def _build_protocols_df(ISA):
    protocols_df = pd.DataFrame(columns=('Protocol Name',
                                         'Protocol Type',
                                         'Protocol Term Accession Number',
                                         'Protocol Term Source REF',
                                         'Protocol Description',
                                         'Protocol Parameters',
                                         'Protocol Hardware',
                                         'Protocol Software',
                                         'Protocol Contact'
                                         )
                                )
    for i, protocol in enumerate(ISA.studies[0].protocols):
        parameters_names = ''
        parameters_accession_numbers = ''
        parameters_source_refs = ''
        for parameter in protocol.parameters:
            parameters_names += parameter.parameter_name.term + ';'
            parameters_accession_numbers += (
                                            parameter.parameter_name.term_accession if parameter.parameter_name.term_accession is not None else '') + ';'
            parameters_source_refs += (
                                      parameter.parameter_name.term_source.name if parameter.parameter_name.term_source else '') + ';'
        if len(protocol.parameters) > 0:
            parameters_names = parameters_names[:-1]
        if protocol.protocol_type:
            protocol_type_term = protocol.protocol_type.term
            protocol_type_term_accession = protocol.protocol_type.term_accession
            if protocol.protocol_type.term_source:
                protocol_type_term_source_name = protocol.protocol_type.term_source.name
                protocols_df.loc[i] = [
                    protocol.name,
                    protocol_type_term,
                    protocol_type_term_accession,
                    protocol_type_term_source_name,
                    protocol.description,
                    parameters_names,
                    "",
                    "",
                    ""
                ]
    return protocols_df


def _build_term_sources_df(ISA):
    term_sources_df = pd.DataFrame(columns=("Term Source Name", "Term Source File", "Term Source Version"))
    for i, term_source in enumerate(ISA.ontology_source_references):
        term_sources_df.loc[i] = [
            term_source.name,
            term_source.file,
            term_source.version
        ]
    return term_sources_df


def _build_publications_df(ISA):
    publications = ISA.studies[0].publications
    publications_df_cols = ['PubMed ID',
                            'Publication DOI',
                            'Publication Author List',
                            'Publication Title',
                            'Publication Status',
                            'Publication Status Term Accession Number',
                            'Publication Status Term Source REF']
    if len(publications) > 0:
        try:
            for comment in publications[0].comments:
                publications_df_cols.append('Comment[' + comment.name + ']')
        except TypeError:
            pass
    publications_df = pd.DataFrame(columns=tuple(publications_df_cols))
    for i, publication in enumerate(publications):
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
        publications_df.loc[i] = publications_df_row
    return publications_df


def _build_qc_df(ISA):
    qc_df = pd.DataFrame(columns=(
        "Quality Control Type",
        "Quality Control Term Accession Number",
        "Quality Control Term Source REF"))
    for i, qc_comment in enumerate([x for x in ISA.studies[0].comments if x.name == "Quality Control Type"]):
        qc_df.loc[i] = [
            qc_comment.value,
            "",
            ""
        ]
    return qc_df


def _build_replicates_df(ISA):
    replicates_df = pd.DataFrame(columns=(
        "Replicate Type",
        "Replicate Term Accession Number",
        "Replicate Term Source REF"))
    for i, replicate_comment in enumerate([x for x in ISA.studies[0].comments if x.name == "Replicate Type"]):
        replicates_df.loc[i] = [
            replicate_comment.value,
            "",
            ""
        ]
    return replicates_df


def _build_normalizations_df(ISA):
    normalizations_df = pd.DataFrame(columns=(
        "Normalization Type",
        "Normalization Term Accession Number",
        "Normalization Term Source REF"))
    for i, normalization_comment in enumerate([x for x in ISA.studies[0].comments if x.name == "Normalization Type"]):
        normalizations_df.loc[i] = [
            normalization_comment.value,
            "",
            ""
        ]
    return normalizations_df


def write_idf_file(inv_obj, output_path):
    investigation = inv_obj
    metadata_df = _build_metadata_df(investigation)
    exp_designs_df = _build_exp_designs_df(investigation)
    exp_factors_df = _build_exp_factors_df(investigation)

    qc_df = _build_qc_df(investigation)
    replicates_df = _build_replicates_df(investigation)
    normalizations_df = _build_normalizations_df(investigation)

    people_df = _build_people_df(investigation)
    publications_df = _build_publications_df(investigation)
    protocols_df = _build_protocols_df(investigation)
    term_sources_df = _build_term_sources_df(investigation)

    idf_df = pd.concat([
        metadata_df,
        exp_designs_df,
        exp_factors_df,
        qc_df,
        replicates_df,
        normalizations_df,
        people_df,
        publications_df,
        protocols_df,
        term_sources_df
    ], axis=1)
    idf_df = idf_df.set_index("MAGE-TAB Version").T
    idf_df = idf_df.replace('', np.nan)
    with open(os.path.join(output_path, "idf.txt"), "w") as idf_fp:
        idf_df.to_csv(path_or_buf=idf_fp, index=True, sep='\t', encoding='utf-8', index_label="MAGE-TAB Version")


def write_sdrf_table_file(inv_obj, output_path):
    tmp = tempfile.mkdtemp()
    isatab.write_study_table_files(inv_obj=inv_obj, output_dir=tmp)
    isatab.write_assay_table_files(inv_obj=inv_obj, output_dir=tmp)
    isatab.merge_study_with_assay_tables(os.path.join(tmp, inv_obj.studies[0].filename),
                                         os.path.join(tmp, inv_obj.studies[0].assays[0].filename),
                                         os.path.join(output_path, "sdrf.txt"))


def dump(inv_obj, output_path):
    write_idf_file(inv_obj, output_path=output_path)
    write_sdrf_table_file(inv_obj=inv_obj, output_path=output_path)
    return inv_obj