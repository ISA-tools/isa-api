import iso8601

from isatools.isatab.validate.store import validator
from isatools.isatab.defaults import log, _RX_DOI, _RX_PMID, _RX_PMCID
from isatools.isatab.utils import cell_has_value


def check_filenames_present(i_df_dict: dict) -> None:
    """ Used for rule 3005

    :param i_df_dict: A dictionary of  DataFrame and list of Dataframes representing the Investigation file
    :return: None
    """
    for s_pos, study_df in enumerate(i_df_dict['studies']):
        if study_df.iloc[0]['Study File Name'] == '':
            validator.add_warning(message="Missing Study File Name", supplemental="STUDY.{}".format(s_pos), code=3005)
            log.warning("(W) A study filename is missing for STUDY.{}".format(s_pos))
        for a_pos, filename in enumerate(i_df_dict['s_assays'][s_pos]['Study Assay File Name'].tolist()):
            if filename == '':
                spl = "STUDY.{}, STUDY ASSAY.{}".format(s_pos, a_pos)
                validator.add_warning.append(message="Missing assay file name", supplemental=spl, code=3005)
                log.warning("(W) An assay filename is missing for STUDY.{}, STUDY ASSAY.{}".format(s_pos, a_pos))


def check_date_formats(i_df_dict):
    """ Used for rule 3001

    :param i_df_dict: A dictionary of  DataFrame and list of Dataframes representing the Investigation file
    :return: None
    """

    def check_iso8601_date(date_str):
        """Checks if a string conforms to ISO8601 dates

        :param date_str: The string to check, expecting a date
        :return: None
        """
        if date_str != '':
            try:
                iso8601.parse_date(date_str)
            except iso8601.ParseError:
                spl = "Found {} in date field".format(date_str)
                validator.add_warning(message="Date is not ISO8601 formatted", supplemental=spl, code=3001)
                log.warning("(W) Date {} does not conform to ISO8601 format".format(date_str))

    release_date_vals = i_df_dict['investigation']['Investigation Public Release Date'].tolist()
    if len(release_date_vals) > 0:
        check_iso8601_date(release_date_vals[0])
    sub_date_values = i_df_dict['investigation']['Investigation Submission Date'].tolist()
    if len(sub_date_values) > 0:
        check_iso8601_date(sub_date_values[0])
    for i, study_df in enumerate(i_df_dict['studies']):
        release_date_vals = study_df['Study Public Release Date'].tolist()
        if len(release_date_vals) > 0:
            check_iso8601_date(release_date_vals[0])
        sub_date_values = study_df['Study Submission Date'].tolist()
        if len(sub_date_values) > 0:
            check_iso8601_date(sub_date_values[0])


def check_dois(i_df_dict):
    """ Used for rule 3002

    :param i_df_dict: A dictionary of  DataFrame and list of Dataframes representing the Investigation file
    :return: None
    """

    def check_doi(doi_str):
        """Check if a string is a valid DOI

        :param doi_str: A string, expecting a DOI
        :return: None
        """
        if doi_str != '':
            if not _RX_DOI.match(doi_str):
                spl = "Found {} in DOI field".format(doi_str)
                validator.add_warning(message="DOI is not valid format", supplemental=spl, code=3002)
                log.warning("(W) DOI {} does not conform to DOI format".format(doi_str))

    for doi in i_df_dict['i_publications']['Investigation Publication DOI'].tolist():
        check_doi(doi)
    for i, study_df in enumerate(i_df_dict['s_publications']):
        for doi in study_df['Study Publication DOI'].tolist():
            check_doi(doi)


def check_pubmed_ids_format(i_df_dict):
    """ Used for rule 3003

    :param i_df_dict: A dictionary of  DataFrame and list of Dataframes representing the Investigation file
    :return: None
    """

    def check_pubmed_id(pubmed_id_str):
        """ Checks if a string is a valid PubMed ID

        :param pubmed_id_str: String to check, expecting a PubMed ID
        :return: None
        """
        if pubmed_id_str != '':
            if (_RX_PMID.match(pubmed_id_str) is None) and (_RX_PMCID.match(pubmed_id_str) is None):
                spl = "Found PubMedID {}".format(pubmed_id_str)
                validator.add_warning(message="PubMed ID is not valid format", supplemental=spl, code=3003)
                log.warning("(W) PubMed ID {} is not valid format".format(pubmed_id_str))

    for doi in i_df_dict['i_publications']['Investigation PubMed ID'].tolist():
        check_pubmed_id(str(doi))
    for study_pubs_df in i_df_dict['s_publications']:
        for doi in study_pubs_df['Study PubMed ID'].tolist():
            check_pubmed_id(str(doi))


def check_ontology_sources(i_df_dict):
    """ Used for rule 3008

    :param i_df_dict: A dictionary of  DataFrame and list of Dataframes representing the Investigation file
    :return: None
    """
    term_source_refs = []
    for i, ontology_source_name in enumerate(i_df_dict['ontology_sources']['Term Source Name'].tolist()):
        if ontology_source_name == '' or 'Unnamed: ' in ontology_source_name:
            spl = "pos={}".format(i)
            warn = "(W) An Ontology Source Reference at position {} is missing Term Source Name, so can't be referenced"
            validator.add_warning(message="Ontology Source missing name ref", supplemental=spl, code=3008)
            log.warning(warn.format(i))
        else:
            term_source_refs.append(ontology_source_name)
    return term_source_refs


def check_ontology_fields(table, cfg, tsrs):
    """ Checks ontology annotation columns are correct for a given configuration
    in a table

    :param table: Table DataFrame
    :param cfg: An ISA Configuration object
    :param tsrs: List of Term Source References from the Ontology Source
    Reference section
    :return: True if OK, False if not OK
    """

    def check_single_field(cell_value, source, acc, config_field, filename):
        """ Checks ontology annotation columns are correct for a given
        configuration for a given cell value

        :param cell_value: Cell value
        :param source: Term Source REF value
        :param acc: Term Accession Number value
        :param config_field: The configuration specification from the ISA Config
        :param filename: Filename of the table
        :return: True if OK, False if not OK
        """
        return_value = True
        if ((cell_has_value(cell_value) and not cell_has_value(source) and cell_has_value(acc))
                or not cell_has_value(cell_value)):
            msg = "Missing Term Source REF in annotation or missing Term Source Name"
            spl = ("Incomplete values for ontology headers, for the field '{}' in the file '{}'. Check that all the "
                   "label/accession/source are provided.").format(config_field.header, filename)
            validator.add_warning(message=msg, supplemental=spl, code=3008)
            log.warning("(W) {}".format(spl))
            return_value = False
        if cell_has_value(source) and source not in tsrs:
            spl = ("Term Source REF, for the field '{}' in the file '{}' does not refer to a declared "
                   "Ontology Source.").format(cfield.header, filename)
            validator.add_warning(message="Term Source REF reference broken", supplemental=spl, code=3011)
            log.warning("(W) {}".format(spl))
            return_value = False
        return return_value

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
            warning = "(W) The Field '{}' should have values from ontologies and has no ontology headers instead"
            log.warning(warning.format(header))
            result = False
            continue

        for irow in range(len(table.index)):
            result = result and check_single_field(table.iloc[irow].iloc[icol],
                                                   table.iloc[irow].iloc[rindx],
                                                   table.iloc[irow].iloc[rrindx],
                                                   cfield,
                                                   table.filename)

    return result
