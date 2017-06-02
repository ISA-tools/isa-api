from isatools import isatab
import tempfile
from .model.v1 import *
import os
import logging
import csv
import numpy as np
import pandas as pd
from io import StringIO


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


def load(FP):  # loads IDF file
    # first cast to IDF
    inv_fp = cast_idf_to_inv(FP)
    df = pd.read_csv(inv_fp, names=range(0, 128), sep='\t', engine='python', encoding='utf-8', comment='#').dropna(axis=1, how='all')
    df = df.T  # transpose
    df.reset_index(inplace=True)  # Reset index so it is accessible as column
    df.columns = df.iloc[0]  # If all was OK, promote this row to the column headers
    # second set output s_ and a_ files
    sdrf_file = df["Study File Name"].iloc[1]
    study_df, assay_df = split_tables(sdrf_path=os.path.join(os.path.dirname(FP.name), sdrf_file))
    study_df.columns = study_df.isatab_header
    assay_df.columns = assay_df.isatab_header
    # write out ISA files
    tmp = "/Users/dj/PycharmProjects/isa-api/tests/data/tmp"
    inv_fp.seek(0)
    # print("Writing i_investigation.txt to {}".format(tmp))
    print("Writing s_{0} to {1}".format(tmp, os.path.basename(sdrf_file)))
    with open(os.path.join(tmp, "s_" + os.path.basename(sdrf_file)), "w") as s_fp:
        study_df.to_csv(path_or_buf=s_fp, mode='a', sep='\t', encoding='utf-8', index=False,)
    print("Writing a_{0} to {1}".format(tmp, os.path.basename(sdrf_file)))
    with open(os.path.join(tmp, "a_" + os.path.basename(sdrf_file)), "w") as a_fp:
        assay_df.to_csv(path_or_buf=a_fp, mode='a', sep='\t', encoding='utf-8', index=False,)
    # with open(os.path.join(tmp, "i_investigation.txt")) as tmp_inv_fp:
    ISA = isatab.load(inv_fp)
    ISA.studies[0].filename = "s_" + os.path.basename(sdrf_file)
    ISA.studies[0].assays = [Assay(filename="a_" + os.path.basename(sdrf_file))]
    return ISA


inv_to_idf_map = {
            "Study File Name": "SDRF File",
            "Study Title": "Investigation Title",
            "Study Description": "Experiment Description",
            "Study Public Release Date": "Public Release Date",
            "Comment[MAGETAB TimeStamp_Version]": "MAGETAB TimeStamp_Version",
            "Comment[ArrayExpressReleaseDate]": "ArrayExpressReleaseDate",
            "Comment[Date of Experiment]": "Date of Experiment",
            "Comment[AEMIAMESCORE]": "AEMIAMESCORE",
            "Comment[Submitted Name]": "Submitted Name",
            "Comment[ArrayExpressAccession]": "ArrayExpressAccession",
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
            "Study Person Fax": "Person Fax",
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
            "Comment[Protocol Software]": "Protocol Software",
            "Comment[Protocol Hardware]": "Protocol Hardware",
            "Comment[Protocol Contact]": "Protocol Contact",
            "Term Source Name": "Term Source Name",
            "Term Source File": "Term Source File",
            "Term Source Version": "Term Source Version",
            "Term Source Description": "Term Source Description"
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
    idf_dict = {}
    for line in FP:
        if line.startswith(tuple(inv_to_idf_map.values())) or line.startswith("Comment["):
            for k, v in inv_to_idf_map.items():
                line = line.replace(v, k)  # note k-v is reversed
        else:
            first_token = line[:line.index('\t')]
            line = line.replace(first_token, "Comment[{}]".format(first_token))
        # idf_FP.write(line)
        idf_dict[line[:line.index('\t')]] = line
    # idf_FP.seek(0)
    idf_FP.name = FP.name
    with open(os.path.join(os.path.dirname(__file__), 'resources', 'tab_templates', 'i_mage_template.txt')) as i_template_FP:
        for line in i_template_FP:
            try:
                try:
                    line = idf_dict[line[:line.index('\t')]]
                except ValueError:
                    line = idf_dict[line[:line.index('\n')]]
            except KeyError:
                pass
            idf_FP.write(line)
    # for key in [x for x in idf_dict.keys() if x.startswith("Comment[")]:
    #     idf_FP.write(idf_dict[key])
    idf_FP.seek(0)
    return idf_FP


def export_to_isatab(FP, output_dir):
    # Load and write the investigation section somewhere
    df = pd.read_csv(FP, names=range(0, 128), sep='\t', engine='python', encoding='utf-8', comment='#').dropna(axis=1, how='all')
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


idf_map = {
    "MAGE-TAB Version": "magetab_version",
    "Investigation Title": "investigation_title",
    "Investigation Accession": "investigation_accession",
    "Investigation Accession Term Source REF": "investigation_accession_term_source_ref",
    "Experimental Design": "experimental_design",
    "Experimental Design Term Source REF": "experimental_design_term_source_ref",
    "Experimental Design Term Accession Number": "experimental_design_term_accession_number",
    "Experimental Factor Name": "experimental_factor",
    "Experimental Factor Term Source REF": "experimental_factor_term_source_ref",
    "Experimental Factor Term Accession Number": "experimental_factor_term_accession_number",

    "Person Last Name": "person_last_name",
    "Person First Name": "person_first_name",
    "Person Mid Initials": "person_mid_initials",
    "Person Email": "person_email",
    "Person Phone": "person_phone",
    "Person Fax": "person_fax",
    "Person Address": "person_address",
    "Person Affiliation": "person_affiliation",
    "Person Roles": "person_roles",
    "Person Roles Term Source REF": "person_roles_term_source_ref",
    "Person Roles Term Accession Number": "person_roles_term_accession_number",

    "Quality Control Type": "quality_control_type",
    "Quality Control Term Source REF": "quality_control_term_source_ref",
    "Quality Control Term Accession Number": "quality_control_term_accession_number",
    "Replicate Type": "replicate_type",
    "Replicate Term Source REF": "replicate_term_source_ref",
    "Replicate Term Accession Number": "replicate_term_accession_number",
    "Normalization Type": "normalization_type",
    "Normalization Term Source REF": "normalization_term_source_ref",
    "Normalization Term Accession Number": "normalization_term_accession_number",

    "Date of Experiment": "date_of_experiment",
    "Public Release Date": "public_release_date",

    "PubMed ID": "publication_pubmed_id",
    "Publication DOI": "publication_doi",
    "Publication Author List": "publication_author_list",
    "Publication Title": "publication_title",
    "Publication Status": "publication_status",
    "Publication Status Term Source REF": "publication_status_term_source_ref",
    "Publication Status Term Accession Number": "publication_status_term_accession_number",

    "Experimental Description": "experimental_description",

    "Protocol Name": "protocol_name",
    "Protocol Type": "protocol_type",
    "Protocol Term Source REF": "protocol_term_source_ref",
    "Protocol Term Accession Number": "protocol_term_accession_number",
    "Protocol Description": "protocol_description",
    "Protocol Parameters": "protocol_parameters",
    "Protocol Hardware": "protocol_hardware",
    "Protocol Software": "protocol_software",
    "Protocol Contact": "protocol_contact",

    "SDRF File": "sdrf_file",

    "Term Source Name": "term_source_name",
    "Term Source File": "term_source_file",
    "Term Source Version": "term_source_version",

}


def parse(magetab_idf_path, technology_type, measurement_type):
    idf_dict = {}

    with open(magetab_idf_path, "r", encoding="utf-8") as magetab_idf_file:
        magetab_idf_reader = csv.reader(filter(lambda r: r[0] != '#', magetab_idf_file), dialect='excel-tab')

        for row in magetab_idf_reader:
            if not row[0].startswith("Comment["):
                try:
                    idf_dict[idf_map[row[0]]] = row[1:]
                except KeyError:
                    pass

    ISA = Investigation(identifier="Investigation")

    ontology_source_dict = {}

    v = idf_dict['term_source_name']
    for i in range(0, len(v)):
        ontology_source = OntologySource(name=v[i])
        ontology_source.file = idf_dict['term_source_file'][i]
        ontology_source.version = idf_dict['term_source_version'][i]
        ISA.ontology_source_references.append(ontology_source)
        ontology_source_dict[ontology_source.name] = ontology_source

    S = Study(identifier="Study")

    for k, v in idf_dict.items():
        if k == 'investigation_title' and len([x for x in v if x != '']) == 1:
            ISA.title = v[0]
            S.title = v[0]
        if k == 'experimental_description' and len([x for x in v if x != '']) == 1:
            ISA.description = v[0]
        elif k in ('investigation_accession',
                   'investigation_accession_term_source_ref',
                   'date_of_experiment',
                   'magetab_version') and len([x for x in v if x != '']) == 1:
            S.comments.append(Comment(name=k, value=v[0]))
        elif k == 'experimental_design':
            experimental_design_comment = Comment(name="Experimental Design")
            experimental_design_term_source_ref_comment = Comment(name="Experimental Design Term Source REF")
            experimental_factor_term_accession_number_comment = Comment(
                name="Experimental Design Term Accession Number")
            experimental_design_comment.value += ';'.join(idf_dict['experimental_design'])
            experimental_design_term_source_ref_comment.value = ';'.join(
                idf_dict['experimental_design_term_source_ref'])
            if 'experimental_design_term_accession_number' in idf_dict.keys():
                experimental_factor_term_accession_number_comment.value = ';'.join(
                    idf_dict['experimental_design_term_accession_number'])
            S.comments.append(experimental_design_comment)
            S.comments.append(experimental_design_term_source_ref_comment)
            S.comments.append(experimental_factor_term_accession_number_comment)

        elif k == 'public_release_date':
            ISA.public_release_date = v[0]
            S.public_release_date = v[0]
        elif k == 'person_last_name' and len(v) > 0:
            for i in range(0, len(v)):
                p = Person()
                p.last_name = v[i]
                p.first_name = idf_dict['person_first_name'][i]
                p.last_name = idf_dict['person_last_name'][i]
                try:
                    p.mid_initials = idf_dict['person_mid_initials'][i]
                except IndexError:
                    pass
                p.email = idf_dict['person_email'][i]
                p.phone = idf_dict['person_phone'][i]
                p.fax = idf_dict['person_fax'][i]
                p.address = idf_dict['person_address'][i]
                p.affiliation = idf_dict['person_affiliation'][i]
                roles_list = idf_dict['person_roles'][i].split(';')
                roles_term_source_ref_list = idf_dict['person_roles_term_source_ref'][i].split(';')
                if 'person_roles_term_accession_number' in idf_dict.keys():
                    roles_term_accession_number_list = idf_dict['person_roles_term_accession_number'][i].split(';')
                for j, term in enumerate([x for x in roles_list if x != '']):
                    role = OntologyAnnotation(term=term)
                    role_term_source_ref = roles_term_source_ref_list[j]
                    if role_term_source_ref != '':
                        role.term_source = ontology_source_dict[role_term_source_ref]
                    if 'person_roles_term_accession_number' in idf_dict.keys():
                        role.term_accession = roles_term_accession_number_list[j]
                    p.roles.append(role)
                S.contacts.append(p)
        elif k == 'publication_pubmed_id' and len(v) > 0:
            for i in range(0, len(v)):
                p = Publication()
                p.pubmed_id = v[i]
                p.doi = idf_dict['publication_doi'][i]
                p.author_list = idf_dict['publication_author_list'][i]
                p.title = idf_dict['publication_title'][i]
                p.doi = idf_dict['publication_doi'][i]
                status = OntologyAnnotation(term=idf_dict['publication_status'][i])
                if 'publication_status_term_source_ref' in idf_dict.keys():
                    try:
                        status.term_source = ontology_source_dict[idf_dict['publication_status_term_source_ref'][i]]
                    except IndexError:
                        pass
                    except KeyError:
                        pass
                if 'publication_status_term_accession_number' in idf_dict.keys():
                    status.term_accession = idf_dict['publication_status_term_accession_number'][i]
                p.status = status
                S.publications.append(p)
        elif k == 'protocol_name' and len(v) > 0:
            for i in range(0, len(v)):
                p = Protocol()
                p.name = v[i]
                protocol_type = OntologyAnnotation(term=idf_dict['protocol_type'][i])
                if 'publication_status_term_source_ref' in idf_dict.keys():
                    try:
                        protocol_type.term_source = ontology_source_dict[idf_dict['protocol_term_source_ref'][i]]
                    except IndexError:
                        pass
                    except KeyError:
                        pass
                if 'publication_status_term_accession_number' in idf_dict.keys():
                    protocol_type.term_accession = idf_dict['protocol_term_accession_number'][i]
                p.protocol_type = protocol_type
                p.description = idf_dict['protocol_description'][i]
                if 'protocol_parameters' in idf_dict.keys():
                    parameters_list = idf_dict['protocol_parameters'][i].split(';')
                    for item in parameters_list:
                        if item != '':
                            protocol_parameter = ProtocolParameter(parameter_name=OntologyAnnotation(term=item))
                            p.parameters.append(protocol_parameter)
                S.protocols.append(p)
        elif k == 'sdrf_file':
            S.filename = 's_{}'.format(v[0])
            S.assays = [
                Assay(filename='a_{}'.format(v[0]),
                      technology_type=OntologyAnnotation(term=technology_type),
                      measurement_type=OntologyAnnotation(term=measurement_type))
            ]
        ISA.studies = [S]
    return ISA