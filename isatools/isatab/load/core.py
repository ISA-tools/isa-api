from os import path
from glob import glob
from re import compile

from pandas import merge, read_csv
from numpy import nan

from isatools.utils import utf8_text_file_open
from isatools.isatab.load.read import read_tfile, read_investigation_file
from isatools.isatab.load.ProcessSequenceFactory import ProcessSequenceFactory
from isatools.isatab.defaults import _RX_COMMENT, log
from isatools.isatab.utils import strip_comments
from isatools.model import (
    OntologyAnnotation,
    Publication,
    Person,
    Comment,
    Investigation,
    OntologySource,
    Study,
    StudyFactor,
    Protocol,
    ProtocolParameter,
    Assay
)


def load(isatab_path_or_ifile, skip_load_tables=False):
    """Load an ISA-Tab into ISA Data Model objects

    :param isatab_path_or_ifile: Full path to an ISA-Tab directory or file-like
    buffer object pointing to an investigation file
    :param skip_load_tables: Whether or not to skip loading the table files
    :return: Investigation objects
    """

    # from DF of investigation file

    def get_ontology_source(term_source_ref):
        try:
            current_onto_source = ontology_source_map[term_source_ref]
        except KeyError:
            current_onto_source = None
        return current_onto_source

    def get_oa(val, accession, ts_ref):
        """Gets a OntologyAnnotation for a give value, accession and
        term source REF

        :param val: Value of the OA
        :param accession: Term Accession Number of the OA
        :param ts_ref: Term Source REF of the OA
        :return: An OntologyAnnotation object
        """
        if val == '' and accession == '':
            return None
        else:
            return OntologyAnnotation(
                term=val,
                term_accession=accession,
                term_source=get_ontology_source(ts_ref)
            )

    def get_oa_list_from_semi_c_list(vals, accessions, ts_refs):
        """Gets a list of OntologyAnnotations from semi-colon delimited lists

        :param vals: A list of values, separated by semi-colons
        :param accessions: A list of accessions, separated by semi-colons
        :param ts_refs: A list of term source REFs, separated by semi-colons
        :return: A list of OntologyAnnotation objects
        """
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
        """Get a list of Publications from the relevant investigation file
        section

        :param section_df: A PUBLICATIONS section DataFrame
        :return: A list of Publication objects
        """
        if 'Investigation PubMed ID' in section_df.columns:
            prefix = 'Investigation '
        elif 'Study PubMed ID' in section_df.columns:
            prefix = 'Study '
        else:
            raise KeyError

        publications = []

        for _, current_row in section_df.iterrows():
            publication = Publication(pubmed_id=current_row[prefix + 'PubMed ID'],
                                      doi=current_row[prefix + 'Publication DOI'],
                                      author_list=current_row[
                                          prefix + 'Publication Author List'],
                                      title=current_row[prefix + 'Publication Title'])

            publication.status = get_oa(
                current_row[prefix + 'Publication Status'],
                current_row[prefix + 'Publication Status Term Accession Number'],
                current_row[prefix + 'Publication Status Term Source REF'])
            publication.comments = get_comments_row(section_df.columns, current_row)
            publications.append(publication)

        return publications

    def get_contacts(section_df):
        """Get a list of Person objects from the relevant investigation file
        section

        :param section_df: A CONTACTS section DataFrame
        :return: A list of Person objects
        """
        if 'Investigation Person Last Name' in section_df.columns:
            prefix = 'Investigation '
        elif 'Study Person Last Name' in section_df.columns:
            prefix = 'Study '
        else:
            raise KeyError

        contacts = []

        for _, current_row in section_df.iterrows():
            person = Person(last_name=current_row[prefix + 'Person Last Name'],
                            first_name=current_row[prefix + 'Person First Name'],
                            mid_initials=current_row[prefix + 'Person Mid Initials'],
                            email=current_row[prefix + 'Person Email'],
                            phone=current_row[prefix + 'Person Phone'],
                            fax=current_row[prefix + 'Person Fax'],
                            address=current_row[prefix + 'Person Address'],
                            affiliation=current_row[prefix + 'Person Affiliation'])

            person.roles = get_oa_list_from_semi_c_list(
                current_row[prefix + 'Person Roles'],
                current_row[prefix + 'Person Roles Term Accession Number'],
                current_row[prefix + 'Person Roles Term Source REF'])
            person.comments = get_comments_row(section_df.columns, current_row)
            contacts.append(person)

        return contacts

    def get_comments(section_df):
        """Get Comments from a section DataFrame

        :param section_df: A section DataFrame
        :return: A list of Comment objects as found in the section
        """
        comments = []
        for col in [x for x in section_df.columns if _RX_COMMENT.match(str(x))]:
            for _, current_row in section_df.iterrows():
                comment = Comment(
                    name=next(iter(_RX_COMMENT.findall(col))), value=current_row[col])
                comments.append(comment)
        return comments

    def get_comments_row(cols, row):
        """Get Comments in a given DataFrame row

        :param cols: List of DataFrame columns
        :param row: DataFrame row as a Series object
        :return: A list of Comment objects
        """
        comments = []
        for col in [x for x in cols if _RX_COMMENT.match(str(x))]:
            comment = Comment(
                name=next(iter(_RX_COMMENT.findall(col))), value=row[col])
            comments.append(comment)
        return comments

    FP = None

    if isinstance(isatab_path_or_ifile, str):
        if path.isdir(isatab_path_or_ifile):
            fnames = glob(path.join(isatab_path_or_ifile, "i_*.txt"))
            assert len(fnames) == 1
            FP = utf8_text_file_open(fnames[0])
    elif hasattr(isatab_path_or_ifile, 'read'):
        FP = isatab_path_or_ifile
    else:
        raise IOError("Cannot resolve input file")

    try:
        df_dict = read_investigation_file(FP)
        investigation = Investigation()

        for _, row in df_dict['ontology_sources'].iterrows():
            ontology_source = OntologySource(
                name=row['Term Source Name'],
                file=row['Term Source File'],
                version=row['Term Source Version'],
                description=row['Term Source Description'])
            investigation.ontology_source_references.append(ontology_source)

        ontology_source_map = dict(map(lambda x: (x.name, x), investigation.ontology_source_references))
        if not df_dict['investigation'].empty:
            row = df_dict['investigation'].iloc[0]
            investigation.identifier = str(row['Investigation Identifier'])
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
            study.identifier = str(row['Study Identifier'])
            study.title = row['Study Title']
            study.description = row['Study Description']
            study.submission_date = row['Study Submission Date']
            study.public_release_date = row['Study Public Release Date']
            study.filename = row['Study File Name']

            study.publications = get_publications(df_dict['s_publications'][i])
            study.contacts = get_contacts(df_dict['s_contacts'][i])
            study.comments = get_comments(df_dict['studies'][i])

            for _, row in df_dict['s_design_descriptors'][i].iterrows():
                design_descriptor = get_oa(
                    row['Study Design Type'],
                    row['Study Design Type Term Accession Number'],
                    row['Study Design Type Term Source REF'])
                these_comments = get_comments_row(
                    df_dict['s_design_descriptors'][i].columns, row)
                design_descriptor.comments = these_comments
                study.design_descriptors.append(design_descriptor)

            for _, row in df_dict['s_factors'][i].iterrows():
                factor = StudyFactor(name=row['Study Factor Name'])
                factor.factor_type = get_oa(
                    row['Study Factor Type'],
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
                protocol.protocol_type = get_oa(
                    row['Study Protocol Type'],
                    row['Study Protocol Type Term Accession Number'],
                    row['Study Protocol Type Term Source REF'])
                params = get_oa_list_from_semi_c_list(
                    row['Study Protocol Parameters Name'],
                    row['Study Protocol Parameters Name Term Accession Number'],
                    row['Study Protocol Parameters Name Term Source REF'])
                for param in params:
                    protocol_param = ProtocolParameter(parameter_name=param)
                    protocol.parameters.append(protocol_param)
                protocol.comments = get_comments_row(
                    df_dict['s_protocols'][i].columns, row)
                study.protocols.append(protocol)
                protocol_map[protocol.name] = protocol
            study.protocols = list(protocol_map.values())
            if skip_load_tables:
                pass
            else:
                study_tfile_df = read_tfile(path.join(path.dirname(FP.name), study.filename))
                iosrs = investigation.ontology_source_references
                sources, samples, _, __, processes, characteristic_categories, unit_categories = \
                    ProcessSequenceFactory(
                        ontology_sources=iosrs,
                        study_protocols=study.protocols,
                        study_factors=study.factors
                    ).create_from_df(study_tfile_df)
                study.sources = sorted(list(sources.values()), key=lambda x: x.name, reverse=False)
                study.samples = sorted(list(samples.values()), key=lambda x: x.name, reverse=False)
                study.process_sequence = list(processes.values())
                study.characteristic_categories = sorted(
                    list(characteristic_categories.values()),
                    key=lambda x: x.term,
                    reverse=False)
                study.units = sorted(list(unit_categories.values()), key=lambda x: x.term, reverse=False)

                for process in study.process_sequence:
                    try:
                        process.executes_protocol = protocol_map[process.executes_protocol]
                    except KeyError:
                        try:
                            unknown_protocol = protocol_map['unknown']
                        except KeyError:
                            description = "This protocol was auto-generated where a protocol could not be determined."
                            protocol_map['unknown'] = Protocol(name="unknown protocol", description=description)
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
                    iosrs = investigation.ontology_source_references
                    assay_tfile_df = read_tfile(path.join(path.dirname(FP.name), assay.filename))
                    _, samples, other, data, processes, characteristic_categories, unit_categories = \
                        ProcessSequenceFactory(
                            ontology_sources=iosrs,
                            study_samples=study.samples,
                            study_protocols=study.protocols,
                            study_factors=study.factors).create_from_df(
                            assay_tfile_df)
                    assay.samples = sorted(
                        list(samples.values()), key=lambda x: x.name,
                        reverse=False)
                    assay.other_material = sorted(
                        list(other.values()), key=lambda x: x.name,
                        reverse=False)
                    assay.data_files = sorted(
                        list(data.values()), key=lambda x: x.filename,
                        reverse=False)
                    assay.process_sequence = list(processes.values())
                    assay.characteristic_categories = sorted(
                        list(characteristic_categories.values()),
                        key=lambda x: x.term, reverse=False)
                    assay.units = sorted(
                        list(unit_categories.values()), key=lambda x: x.term,
                        reverse=False)

                    description = "This protocol was auto-generated where a protocol could not be determined."
                    for process in assay.process_sequence:
                        try:
                            process.executes_protocol = protocol_map[process.executes_protocol]
                        except KeyError:
                            try:
                                unknown_protocol = protocol_map['unknown']
                            except KeyError:
                                protocol_map['unknown'] = Protocol(name="unknown protocol", description=description)
                                unknown_protocol = protocol_map['unknown']
                                study.protocols.append(unknown_protocol)
                            process.executes_protocol = unknown_protocol

                study.assays.append(assay)
            investigation.studies.append(study)
    finally:
        FP.close()
    return investigation


def merge_study_with_assay_tables(study_file_path, assay_file_path, target_file_path):
    """
        Utility function to merge a study table file with an assay table
        file. The merge uses the Sample Name as the
        key, so samples in the assay file must match those in the study file.
        If there are no matches, the function
        will output the joined header and no additional rows.

        Usage:

        merge_study_with_assay_tables('/path/to/study.txt',
        '/path/to/assay.txt', '/path/to/merged.txt')
    """
    log.info("Reading study file %s into DataFrame", study_file_path)
    study_DF = read_tfile(study_file_path)
    log.info("Reading assay file %s into DataFrame", assay_file_path)
    assay_DF = read_tfile(assay_file_path)
    log.info("Merging DataFrames...")
    merged_DF = merge(study_DF, assay_DF, on='Sample Name')
    log.info("Writing merged DataFrame to file %s", target_file_path)
    with open(target_file_path, 'w', encoding='utf-8') as fp:
        merged_DF.to_csv(fp, sep='\t', index=False, header=study_DF.isatab_header + assay_DF.isatab_header[1:])


def load_table(fp):
    """Loads a ISA table file into a DataFrame

    :param fp: A file-like buffer object
    :return: DataFrame of the study or assay table
    """
    try:
        fp = strip_comments(fp)
        df = read_csv(fp, dtype=str, sep='\t', encoding='utf-8').replace(nan, '')
    except UnicodeDecodeError:
        log.warning("Could not load file with UTF-8, trying ISO-8859-1")
        fp = strip_comments(fp)
        df = read_csv(fp, dtype=str, sep='\t', encoding='latin1').replace(nan, '')
    labels = df.columns
    new_labels = []
    for label in labels:
        any_var_regex = compile(r'.*\[(.*?)\]')
        hits = any_var_regex.findall(label)
        if len(hits) > 0:
            val = hits[0].strip()
            new_label = ""
            if 'Comment' in label:
                new_label = 'Comment[{val}]'.format(val=val)
            elif 'Characteristics' in label:
                new_label = 'Characteristics[{val}]'.format(val=val)
            elif 'Parameter Value' in label:
                new_label = 'Parameter Value[{val}]'.format(val=val)
            elif 'Factor Value' in label:
                new_label = 'Factor Value[{val}]'.format(val=val)
            new_labels.append(new_label)
        elif label == "Material Type":
            new_label = 'Characteristics[Material Type]'
            new_labels.append(new_label)
        else:
            new_labels.append(label)
    df.columns = new_labels
    return df
