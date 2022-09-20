from pandas import DataFrame

from isatools.isatab.defaults import log
from isatools.model import OntologyAnnotation


def get_seen_comments(target: list) -> dict:
    """ Generic method to build the seen comments

    :param target: The target object to get the seen comments from
    """
    seen_comments = {}
    for item in target:
        for current_comment in item.comments:
            if current_comment.name in seen_comments.keys():
                seen_comments[current_comment.name].append(current_comment.value)
            else:
                seen_comments[current_comment.name] = [current_comment.value]
    return seen_comments


def get_associated_comments(target, seen_comments, df_row):
    """ Generic method to build the associated comments """
    common_names = [current_comment.name for current_comment in target.comments]
    for key in seen_comments.keys():
        if key in common_names:
            for element in target.comments:
                if element.name == key:
                    df_row.append(element.value)
        else:
            df_row.append("")
    return df_row


def _build_roles_str(roles: list = None):
    """Build roles strings if multiple roles

    :param roles: A list of OntologyAnnotation objects describing the roles
    :return: Lists of strings corresponding to the list of role names,
    accession numbers and term source references.
    """
    # TODO: this is duplicated code in magetab.py
    if not roles:
        roles = list()
    log.debug('building roles from: %s', roles)
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


def _build_ontology_reference_section(ontologies: list = None) -> DataFrame:
    """Build ontology reference section DataFrame
    :param ontologies: List of Ontology objects describing the section's
    Ontology Resource
    :return: DataFrame corresponding to the ONTOLOGY REFERENCE section
    """
    if not ontologies:
        ontologies = list()
    log.debug('building ontology resource reference from: %s', ontologies)
    seen_comments = get_seen_comments(ontologies)
    onto_src_ref_cols = ['Term Source Name', 'Term Source File', 'Term Source Version', 'Term Source Description']
    for comment_name in seen_comments.keys():
        onto_src_ref_cols.append('Comment[' + comment_name + ']')
    onto_src_ref_df = DataFrame(columns=tuple(onto_src_ref_cols))
    for i, ontology in enumerate(ontologies):
        log.debug('%s iteration, item=%s', i, ontology)
        onto_src_ref_df_row = [ontology.name, ontology.file, ontology.version, ontology.description]
        onto_src_ref_df_row = get_associated_comments(ontology, seen_comments, onto_src_ref_df_row)
        onto_src_ref_df.loc[i] = onto_src_ref_df_row
    return onto_src_ref_df.set_index('Term Source Name').T


def _build_contacts_section_df(prefix='Investigation', contacts: list = None):
    """Build contacts section DataFrame

    :param prefix: Section prefix - Investigation or Study
    :param contacts: List of Person objects describing the section's
    contacts
    :return: DataFrame corresponding to the CONTACTS section
    """
    if not contacts:
        contacts = list()
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

    seen_comments = get_seen_comments(contacts)
    for comment_name in seen_comments.keys():
        contacts_df_cols.append('Comment[' + comment_name + ']')
    contacts_df = DataFrame(columns=tuple(contacts_df_cols))
    for i, contact in enumerate(contacts):
        log.debug('%s iteration, item=%s', i, contact)
        roles_names, roles_accession_numbers, roles_source_refs = _build_roles_str(contact.roles)
        contacts_df_row = [contact.last_name, contact.first_name, contact.mid_initials, contact.email,
                           contact.phone, contact.fax, contact.address, contact.affiliation, roles_names,
                           roles_accession_numbers, roles_source_refs]
        contacts_df_row = get_associated_comments(contact, seen_comments, contacts_df_row)
        log.debug('row=%s', contacts_df_row)
        contacts_df.loc[i] = contacts_df_row
    return contacts_df.set_index(prefix + ' Person Last Name').T


def _build_publications_section_df(prefix='Investigation', publications: list = None):
    """Build contacts section DataFrame

    :param prefix: Section prefix - Investigation or Study
    :param publications: List of Publications objects describing the
    section's publications
    :return: DataFrame corresponding to the PUBLICATIONS section
    """
    if not publications:
        publications = list()
    log.debug('building contacts from: %s', publications)
    publications_df_cols = [
        prefix + ' PubMed ID',
        prefix + ' Publication DOI',
        prefix + ' Publication Author List',
        prefix + ' Publication Title',
        prefix + ' Publication Status',
        prefix + ' Publication Status Term Accession Number',
        prefix + ' Publication Status Term Source REF']

    seen_comments = get_seen_comments(publications)
    for comment_name in seen_comments.keys():
        publications_df_cols.append('Comment[' + comment_name + ']')
    this_publications_df = DataFrame(columns=tuple(publications_df_cols))

    for i, publication in enumerate(publications):
        log.debug('%s iteration, item=%s', i, publication)
        status_term = ''
        status_term_accession = ''
        status_term_source_name = ''
        if publication.status is not None:
            status_term = publication.status.term
            status_term_accession = publication.status.term_accession
            status_term_source_name = ''
            if publication.status.term_source is not None:
                status_term_source_name = publication.status.term_source.name
        publications_df_row = [publication.pubmed_id, publication.doi, publication.author_list,
                               publication.title, status_term, status_term_accession, status_term_source_name]
        publications_df_row = get_associated_comments(publication, seen_comments, publications_df_row)
        log.debug('row=%s', publications_df_row)
        this_publications_df.loc[i] = publications_df_row

    return this_publications_df.set_index(prefix + ' PubMed ID').T


def _build_protocols_section_df(protocols: list = None):
    """Build Protocol section DataFrame
    :param protocols: List of Publications objects describing the
    section's protocols
    :return: DataFrame corresponding to the PROTOCOLS section
    """
    if not protocols:
        protocols = list()
    log.debug('building contacts from: %s', protocols)
    study_protocols_df_cols = [
        'Study Protocol Name',
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
    ]
    seen_comments = get_seen_comments(protocols)
    for comment_name in seen_comments.keys():
        study_protocols_df_cols.append('Comment[' + comment_name + ']')
    this_study_protocols_df = DataFrame(columns=tuple(study_protocols_df_cols))

    protocol_type_term = ''
    protocol_type_term_accession = ''
    protocol_type_term_source_name = ''
    for i, protocol in enumerate(protocols):
        parameters_names = ''
        parameters_accession_numbers = ''
        parameters_source_refs = ''
        for parameter in protocol.parameters:
            parameters_names += parameter.parameter_name.term + ';'
            parameters_accession_numbers += (parameter.parameter_name.term_accession
                                             if parameter.parameter_name.term_accession is not None
                                             else '') + ';'
            if isinstance(parameter.parameter_name, OntologyAnnotation):
                if parameter.parameter_name.term_source:
                    this_param_source = parameter.parameter_name.term_source
                    if type(parameter.parameter_name.term_source) != str:
                        this_param_source = parameter.parameter_name.term_source.name
                    parameters_source_refs += this_param_source + ';'
                else:
                    parameters_source_refs += ';'

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
            component_types_source_refs += (component.component_type.term_source.name
                                            if component.component_type.term_source else '' + ';')
        if len(protocol.components) > 0:
            component_names = component_names[:-1]
            component_types = component_types[:-1]
            component_types_accession_numbers = component_types_accession_numbers[:-1]
            component_types_source_refs = component_types_source_refs[:-1]

        if protocol.protocol_type is not None:
            protocol_type_term = protocol.protocol_type.term
            protocol_type_term_accession = protocol.protocol_type.term_accession
        if protocol.protocol_type.term_source:
            protocol_type_term_source_name = protocol.protocol_type.term_source.name

        study_protocols_df_row = [
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
        study_protocols_df_row = get_associated_comments(protocol, seen_comments, study_protocols_df_row)
        log.debug('row=%s', study_protocols_df_row)
        this_study_protocols_df.loc[i] = study_protocols_df_row

    return this_study_protocols_df.set_index('Study Protocol Name').T


def _build_assays_section_df(assays: list = None):
    """
    Build Factors section DataFrame
    :param assays: List of Study Assay objects describing the
    section's assays
    :return: DataFrame corresponding to the STUDY ASSAY section
    """
    if not assays:
        assays = list()
    log.debug('building contacts from: %s', assays)
    study_assays_df_cols = [
        'Study Assay File Name',
        'Study Assay Measurement Type',
        'Study Assay Measurement Type Term Accession Number',
        'Study Assay Measurement Type Term Source REF',
        'Study Assay Technology Type',
        'Study Assay Technology Type Term Accession Number',
        'Study Assay Technology Type Term Source REF',
        'Study Assay Technology Platform'
    ]

    seen_comments = get_seen_comments(assays)
    for comment_name in seen_comments.keys():
        study_assays_df_cols.append('Comment[' + comment_name + ']')
    this_study_assays_df = DataFrame(columns=tuple(study_assays_df_cols))

    for i, assay in enumerate(assays):
        term_sources = ['measurement_type', 'technology_type']
        sources = []
        for source_string in term_sources:
            source = getattr(assay, source_string)
            if (type(source.term_source) == str) or source.term_source is None:
                sources.append(source.term_source)
            else:
                sources.append(source.term_source.name)
        # NOTE: PRESERVE ORDER OF ELEMENTS IN THIS ARRAY
        study_assays_df_row = [
            assay.filename,
            assay.measurement_type.term,
            assay.measurement_type.term_accession,
            sources[0],
            assay.technology_type.term,
            assay.technology_type.term_accession,
            sources[1],
            assay.technology_platform
        ]
        study_assays_df_row = get_associated_comments(assay, seen_comments, study_assays_df_row)
        log.debug('row=%s', study_assays_df_row)
        this_study_assays_df.loc[i] = study_assays_df_row

    return this_study_assays_df.set_index('Study Assay File Name').T


def _build_factors_section_df(factors: list = None):
    """Build Factors section DataFrame

    :param factors: List of Study Factor objects describing the
    section's factor
    :return: DataFrame corresponding to the STUDY FACTORS section
    """
    if not factors:
        factors = list()
    log.debug('building contacts from: %s', factors)
    study_factors_df_cols = ['Study Factor Name',
                             'Study Factor Type',
                             'Study Factor Type Term Accession Number',
                             'Study Factor Type Term Source REF']

    seen_comments = get_seen_comments(factors)
    for comment_name in seen_comments.keys():
        study_factors_df_cols.append('Comment[' + comment_name + ']')
    this_study_factors_df = DataFrame(columns=tuple(study_factors_df_cols))
    for i, factor in enumerate(factors):
        # TODO: duplicated code from magetab 251 to 261
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
        study_factors_df_row = [factor.name, factor_type_term, factor_type_term_accession,
                                factor_type_term_term_source_name if factor.factor_type.term_source else '']
        study_factors_df_row = get_associated_comments(factor, seen_comments, study_factors_df_row)
        log.debug('row=%s', study_factors_df_row)
        this_study_factors_df.loc[i] = study_factors_df_row

    return this_study_factors_df.set_index('Study Factor Name').T


def _build_design_descriptors_section(design_descriptors: list = None):
    if not design_descriptors:
        design_descriptors = list()
    study_design_descriptors_df_cols = ['Study Design Type', 'Study Design Type Term Accession Number',
                                        'Study Design Type Term Source REF']
    seen_comments = get_seen_comments(design_descriptors)
    for comment_name in seen_comments.keys():
        study_design_descriptors_df_cols.append('Comment[' + comment_name + ']')
    this_study_design_descriptors_df = DataFrame(columns=tuple(study_design_descriptors_df_cols))

    for i, design_descriptor in enumerate(design_descriptors):
        study_design_descriptors_df_row = [
            design_descriptor.term,
            design_descriptor.term_accession,
            design_descriptor.term_source.name if design_descriptor.term_source else ''
        ]
        study_design_descriptors_df_row = get_associated_comments(design_descriptor, seen_comments,
                                                                  study_design_descriptors_df_row)
        log.debug('row=%s', study_design_descriptors_df_row)
        this_study_design_descriptors_df.loc[i] = study_design_descriptors_df_row

    return this_study_design_descriptors_df.set_index('Study Design Type').T
