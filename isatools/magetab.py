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
import shutil


logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_sdrf_filenames(ISA):
    sdrf_filenames = []
    for study in ISA.studies:
        for assay in [x for x in study.assays if x.technology_type.term.lower() == "dna microarray"]:
            sdrf_filenames.append(study.filename[2:-3] + assay.filename[2:-3] + "sdrf.txt")
    return sdrf_filenames


def _build_metadata_df(ISA):
    metadata_df = pd.DataFrame(columns=(
        "MAGE-TAB Version",
        "Investigation Title",
        "Public Release Date",
        "SDRF File"
    ))
    sdrf_filenames = _get_sdrf_filenames(ISA)
    metadata_df.loc[0] = [
        "1.1",
        ISA.title,
        ISA.public_release_date,
        sdrf_filenames[0]
    ]
    for i, sdrf_filename in enumerate(sdrf_filenames):
        if i == 0:
            pass
        else:
            metadata_df.loc[i] = [
                "",
                "",
                "",
                sdrf_filename
            ]
    return metadata_df


def _build_exp_designs_df(ISA):
    exp_designs_df = pd.DataFrame(columns=(
        "Experimental Design",
        "Experimental Design Term Source REF",
        "Experimental Design Term Accession Number"))
    microarray_study_design = []
    for study in ISA.studies:
        if len([x for x in study.assays if x.technology_type.term.lower() == "dna microarray"]) > 0:
            microarray_study_design.extend(study.design_descriptors)
    for i, design_descriptor in enumerate(microarray_study_design):
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
    microarray_study_factors = []
    for study in ISA.studies:
        if len([x for x in study.assays if x.technology_type.term.lower() == "dna microarray"]) > 0:
            microarray_study_factors.extend(study.factors)
    for i, factor in enumerate(microarray_study_factors):
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
    microarray_study_protocols = []
    for study in ISA.studies:
        if len([x for x in study.assays if x.technology_type.term.lower() == "dna microarray"]) > 0:
            microarray_study_protocols.extend(study.protocols)
    for i, protocol in enumerate(microarray_study_protocols):
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
    with open(os.path.join(output_path, "{}.idf.txt".format(investigation.identifier if investigation.identifier != "" else investigation.filename[2:-3])), "w") as idf_fp:
        idf_df.to_csv(path_or_buf=idf_fp, index=True, sep='\t', encoding='utf-8', index_label="MAGE-TAB Version")


def write_sdrf_table_files(i, output_path):
    tmp = tempfile.mkdtemp()
    isatab.write_study_table_files(inv_obj=i, output_dir=tmp)
    isatab.write_assay_table_files(inv_obj=i, output_dir=tmp)
    for study in i.studies:
        for assay in [x for x in study.assays if x.technology_type.term.lower() == "dna microarray"]:
            sdrf_filename = study.filename[2:-3] + assay.filename[2:-3] + "sdrf.txt"
            print("Writing {}".format(sdrf_filename))
            try:
                isatab.merge_study_with_assay_tables(os.path.join(tmp, study.filename),
                                                     os.path.join(tmp, assay.filename),
                                                     os.path.join(output_path, sdrf_filename))
            except FileNotFoundError:
                raise IOError("There was a problem merging intermediate ISA-Tab files into SDRF")


def dump(inv_obj, output_path):
    num_microarray_assays = 0
    for study in inv_obj.studies:
        num_microarray_assays += len([x for x in study.assays if x.technology_type.term.lower() == "dna microarray"])

    if num_microarray_assays > 0:
        write_idf_file(inv_obj, output_path=output_path)
        write_sdrf_table_files(i=inv_obj, output_path=output_path)
    else:
        raise IOError("Input must contain at least one assay of type DNA microarray, halt writing MAGE-TAB")
    return inv_obj


def load(FP):
    # first cast to IDF
    idf_FP = cast_idf_to_inv(FP)
    df = pd.read_csv(idf_FP, names=range(0, 128), sep='\t', engine='python').dropna(axis=1, how='all')
    df = df.T  # transpose
    df.reset_index(inplace=True)  # Reset index so it is accessible as column
    df.columns = df.iloc[0]  # If all was OK, promote this row to the column headers
    # second set output s_ and a_ files
    sdrf_file = df["Comment[SDRF File]"].iloc[1]
    study_df, assay_df = split_tables(sdrf_path=os.path.join(os.path.dirname(FP.name), sdrf_file))
    study_df.columns = study_df.isatab_header
    print("s_" + os.path.basename(sdrf_file))
    assay_df.columns = assay_df.isatab_header
    print("a_" + os.path.basename(sdrf_file))


inv_to_idf_map = {
            "Study Title": "Investigation Title",
            "Study Description": "Experiment Description",
            "Study Design Type": "Experimental Design",
            "Study Design Type Term Accession Number": "Experimental Design Term Accession Number",
            "Study Design Type Ter Source REF": "Experimental Design Term Source REF",
            "Study Factor Name": "Experimental Factor Name",
            "Study Factor Type": "Experimental Factor Type",
            "Study Factor Type Term Accession Number": "Experimental Factor Type Term Accession Number",
            "Study Factor Type Ter Source REF": "Experimental Factor Type Term Source REF",
            "Study PubMed ID": "PubMed ID",
            "Study Publication DOI": "Publication DOI",
            "Study Publication Author List": "Publication Author List",
            "Study Publication Title": "Publication Title",
            "Study Publication Status": "Publication Status",
            "Study Publication Status Term Accession Number": "Publication Status Term Accession Number",
            "Study Publication Status Term Source REF": "Publication Status Term Source REF",
            "Study Person Last Name": "Person Last Name",
            "Study Person First Name": "Person First Name",
            "Study Person Mid Initials": "Person Mid Initials",
            "Study Person Email": "Person Email",
            "Study Person Phone": "Person Phone",
            "Study Person Address": "Person Address",
            "Study Person Affiliation": "Person Affiliation",
            "Study Person Roles": "Person Role",
            "Study Person Roles Term Accession Number": "Person Role Term Accession Number",
            "Study Person Roles Term Source REF": "Person Role Term Source REF",
            "Study Protocol Name": "Protocol Name",
            "Study Protocol Description": "Protocol Description",
            "Study Protocol Parameters": "Protocol Parameters",
            "Study Protocol Type": "Protocol Type",
            "Study Protocol Type Accession Number": "Protocol Term Accession Number",
            "Study Protocol Type Source REF": "Protocol Term Source REF",
            "Term Source Name": "Term Source Name",
            "Term Source File": "Term Source File",
            "Term Source Version": "Term Source Version"
        }  # Relabel these, ignore all other lines


def cast_inv_to_idf(FP):
    # Cut out relevant Study sections from Investigation file
    idf_FP = StringIO()
    for line in FP:
        if line.startswith(tuple(inv_to_idf_map.keys())) or line.startswith("Comment["):
            for k, v in inv_to_idf_map.items():
                line = line.replace(k, v)
            idf_FP.write(line)
    idf_FP.seek(0)
    idf_FP.name = FP.name
    return idf_FP


def cast_idf_to_inv(FP):
    # Cast relevant sections from IDF file into comments
    # insert Additional Investigation file labels
    idf_FP = StringIO()
    for line in FP:
        if line.startswith(tuple(inv_to_idf_map.values())) or line.startswith("Comment["):
            for k, v in inv_to_idf_map.items():
                line = line.replace(v, k)  # note k-v is reversed
        else:
            first_token = line[:line.index('\t')]
            line = line.replace(first_token, "Comment[{}]".format(first_token))
        idf_FP.write(line)
    idf_FP.seek(0)
    idf_FP.name = FP.name
    return idf_FP


def export_to_isatab(FP, output_dir):
    # Load and write the investigation section somewhere
    df = pd.read_csv(FP, names=range(0, 128), sep='\t', engine='python').dropna(axis=1, how='all')
    df = df.T  # transpose
    df.replace(np.nan, '', regex=True, inplace=True)  # Strip out the nan entries
    df.reset_index(inplace=True)  # Reset index so it is accessible as column
    df.columns = df.iloc[0]  # If all was OK, promote this row to the column headers
    df = df.reindex(df.index.drop(0))  # Reindex the DataFrame
    sdrf_filename = df.iloc[0]['SDRF File']
    sdrf_path = os.path.join(os.path.dirname(FP.name), sdrf_filename)
    study_df, assay_df = split_tables(sdrf_path=sdrf_path)
    with open(os.path.join(output_dir, "s_" + os.path.basename(sdrf_path)), 'w') as study_fp:
        study_df.to_csv(study_fp, sep='\t', index=False, header=study_df.isatab_header)
    with open(os.path.join(output_dir, "a_" + os.path.basename(sdrf_path)), 'w') as assay_fp:
        assay_df.to_csv(assay_fp, sep='\t', index=False, header=assay_df.isatab_header)


def split_tables(sdrf_path):
    sdrf_df = isatab.read_tfile(sdrf_path)
    sdrf_df_isatab_header = sdrf_df.isatab_header
    sample_name_index = list(sdrf_df.columns).index("Sample Name")
    study_df = sdrf_df[sdrf_df.columns[0:sample_name_index+1]].drop_duplicates()
    study_df.isatab_header = sdrf_df_isatab_header[0:sample_name_index+1]
    assay_df = sdrf_df[sdrf_df.columns[sample_name_index:]]
    assay_df.isatab_header = sdrf_df_isatab_header[sample_name_index:]
    return study_df, assay_df
