from os import path
from glob import iglob
from tempfile import mkdtemp
from shutil import rmtree
from pandas import DataFrame

from isatools.model import Investigation
from isatools.isatab.defaults import _RX_I_FILE_NAME, log
from isatools.utils import utf8_text_file_open
from isatools.isatab.load import read_tfile
from isatools.isatab.dump.write import write_study_table_files, write_assay_table_files
from isatools.isatab.dump.utils import (
    _build_ontology_reference_section,
    _build_contacts_section_df,
    _build_publications_section_df,
    _build_protocols_section_df,
    _build_assays_section_df,
    _build_factors_section_df,
    _build_design_descriptors_section
)


def dump(isa_obj, output_path,
         i_file_name='i_investigation.txt',
         skip_dump_tables=False,
         write_factor_values_in_assay_table=False):
    """Serializes ISA objects to ISA-Tab

    :param isa_obj: An ISA Investigation object
    :param output_path: Path to write the ISA-Tab files to
    :param i_file_name: Overrides the default name for the investigation file
    :param skip_dump_tables: Boolean flag on whether or not to write the
    study sample table files and assay table files
    :param write_factor_values_in_assay_table: Boolean flag indicating whether
    or not to write Factor Values in the assay table files
    :return: None
    """

    if not _RX_I_FILE_NAME.match(i_file_name):
        log.debug('investigation filename=', i_file_name)
        raise NameError('Investigation file must match pattern i_*.txt, got {}'.format(i_file_name))

    if path.exists(output_path):
        fp = open(path.join(output_path, i_file_name), 'wb')
    else:
        log.debug('output_path=', i_file_name)
        raise FileNotFoundError("Can't find " + output_path)

    if not isinstance(isa_obj, Investigation):
        log.debug('object type=', type(isa_obj))
        raise NotImplementedError("Can only dump an Investigation object")

    # Process Investigation object first to write the investigation file
    investigation = isa_obj

    # Write ONTOLOGY SOURCE REFERENCE section
    ontology_source_references_df = _build_ontology_reference_section(investigation.ontology_source_references)
    fp.write(b'ONTOLOGY SOURCE REFERENCE\n')
    #  Need to set index_label as top left cell
    ontology_source_references_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                         index_label='Term Source Name')

    #  Write INVESTIGATION section
    inv_df_cols = ['Investigation Identifier',
                   'Investigation Title',
                   'Investigation Description',
                   'Investigation Submission Date',
                   'Investigation Public Release Date']
    for comment in sorted(investigation.comments, key=lambda x: x.name):
        inv_df_cols.append('Comment[' + comment.name + ']')
    investigation_df = DataFrame(columns=tuple(inv_df_cols))
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
    fp.write(b'INVESTIGATION\n')
    investigation_df.to_csv(
        path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
        index_label='Investigation Identifier')

    # Write INVESTIGATION PUBLICATIONS section
    investigation_publications_df = _build_publications_section_df(
        prefix='Investigation',
        publications=investigation.publications
    )
    fp.write(b'INVESTIGATION PUBLICATIONS\n')
    investigation_publications_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                         index_label='Investigation PubMed ID')

    # Write INVESTIGATION CONTACTS section
    investigation_contacts_df = _build_contacts_section_df(
        contacts=investigation.contacts)
    fp.write(b'INVESTIGATION CONTACTS\n')
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
        study_df = DataFrame(columns=tuple(study_df_cols))
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
        fp.write(b'STUDY\n')
        study_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8', index_label='Study Identifier')
        study_design_descriptors_df = _build_design_descriptors_section(design_descriptors=study.design_descriptors)
        fp.write(b'STUDY DESIGN DESCRIPTORS\n')
        study_design_descriptors_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                           index_label='Study Design Type')

        # Write STUDY PUBLICATIONS section
        study_publications_df = _build_publications_section_df(prefix='Study', publications=study.publications)
        fp.write(b'STUDY PUBLICATIONS\n')
        study_publications_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                     index_label='Study PubMed ID')

        # Write STUDY FACTORS section
        study_factors_df = _build_factors_section_df(factors=study.factors)
        fp.write(b'STUDY FACTORS\n')
        study_factors_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                index_label='Study Factor Name')

        study_assays_df = _build_assays_section_df(assays=study.assays)
        fp.write(b'STUDY ASSAYS\n')
        study_assays_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                               index_label='Study Assay File Name')

        # Write STUDY PROTOCOLS section
        study_protocols_df = _build_protocols_section_df(protocols=study.protocols)
        fp.write(b'STUDY PROTOCOLS\n')
        study_protocols_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                  index_label='Study Protocol Name')

        # Write STUDY CONTACTS section
        study_contacts_df = _build_contacts_section_df(
            prefix='Study', contacts=study.contacts)
        fp.write(b'STUDY CONTACTS\n')
        study_contacts_df.to_csv(path_or_buf=fp, mode='a', sep='\t', encoding='utf-8',
                                 index_label='Study Person Last Name')

    if skip_dump_tables:
        pass
    else:
        write_study_table_files(investigation, output_path)
        write_assay_table_files(investigation, output_path, write_factor_values_in_assay_table)

    fp.close()
    return investigation


def dumps(isa_obj, skip_dump_tables=False,
          write_fvs_in_assay_table=False):
    """Serializes ISA objects to ISA-Tab to standard output

    :param isa_obj: An ISA Investigation object
    :param skip_dump_tables: Boolean flag on whether or not to write the
    :param  write_fvs_in_assay_table: Boolean flag indicating whether
        or not to write Factor Values in the assay table files
    :return: String output of the ISA-Tab files
    """
    tmp = None
    output = str()
    try:
        tmp = mkdtemp()
        dump(isa_obj=isa_obj, output_path=tmp,
             skip_dump_tables=skip_dump_tables,
             write_factor_values_in_assay_table=write_fvs_in_assay_table)
        with utf8_text_file_open(path.join(tmp, 'i_investigation.txt')) as i_fp:
            output += path.join(tmp, 'i_investigation.txt') + '\n'
            output += i_fp.read()
        for s_file in iglob(path.join(tmp, 's_*')):
            with utf8_text_file_open(s_file) as s_fp:
                output += "--------\n"
                output += s_file + '\n'
                output += s_fp.read()
        for a_file in iglob(path.join(tmp, 'a_*')):
            with utf8_text_file_open(a_file) as a_fp:
                output += "--------\n"
                output += a_file + '\n'
                output += a_fp.read()
    finally:
        if tmp is not None:
            rmtree(tmp)
    return output


def dump_tables_to_dataframes(isa_obj):
    """Serialize the table files only, to DataFrames

    :param isa_obj: An ISA Investigation object
    :return: A dictionary containing ISA table filenames as keys and the
    corresponding tables as DataFrames as the values
    """
    tmp = None
    output = dict()
    try:
        tmp = mkdtemp()
        dump(isa_obj=isa_obj, output_path=tmp, skip_dump_tables=False)
        for s_file in iglob(path.join(tmp, 's_*')):
            output[path.basename(s_file)] = read_tfile(s_file)
        for a_file in iglob(path.join(tmp, 'a_*')):
            output[path.basename(a_file)] = read_tfile(a_file)
    finally:
        if tmp is not None:
            rmtree(tmp)
    return output
